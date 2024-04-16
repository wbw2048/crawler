import multiprocessing
import concurrent.futures
import json
import os
import time

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
global_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()+1)


def get_html(url):
    # 发起HTTP GET请求获取页面内容
    response = requests.get(url, headers=headers)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    return None
def get_search_data(en):
    i = 1
    while True:
        time.sleep(1)
        url = f'https://www.1905.com/mdb/film/list/country-{en}/o0d0p{i}.html'
        soup = get_html(url)
        if soup is None:
            return None
        li_tags = soup.find_all('li', class_='fl line')
        if len(li_tags) == 0:
            return None
        i += 1
        for li_tag in li_tags:
            a_tag = li_tag.find('a')
            if a_tag:
                href = a_tag.get('href')
                yield href
        else:
            return None

def get_data_info(href):
    time.sleep(1)
    url = f'https://www.1905.com{href}/info'
    soup = get_html(url)
    if soup is None:
        return None
    dt_list = soup.find_all('dt')
    dd_list = soup.find_all('dd')
    片名 = soup.title.text
    info = {}
    for i in range(len(dt_list)):
        dt = dt_list[i].text.strip().replace(' ', '')
        dd = dd_list[i].text.strip().replace(' ', '')
        if dt != '' and dd != '':
            info[dt] = dd
    json_file = f'data{href}{片名}.json'
    if not os.path.exists(os.path.dirname(json_file)):
        os.makedirs(os.path.dirname(json_file))
    if not os.path.exists(json_file):
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(info, f, ensure_ascii=False, indent=4)
    return info

if __name__ == '__main__':
    futures =[]
    with open('country.txt', 'r', encoding='utf-8') as file:
        country = json.loads(file.read())
    for ct in country['nation']:
        for href in get_search_data(ct['en']):
            if href is not None:
                futures.append(global_thread_pool.submit(get_data_info, href))
            else:
                break
            if len(futures) > 20:
                for future in futures:
                    print(future.result())
                futures = []
