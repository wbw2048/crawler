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
lines_set = set()
def append_to_file(string, filename):
    try:
        # 打开文件，使用追加模式
        with open(filename, 'a') as file:
            # 写入字符串并换行
            file.write(string + '\n')
    except Exception as e:
        print(f"写入文件时出错：{e}")
def read_file_to_set(filename):
    try:
        # 打开文件，使用写入模式，如果文件不存在则创建文件
        with open(filename, 'a+') as file:
            # 将文件指针移到文件开头
            file.seek(0)
            # 逐行读取文件内容
            for line in file:
                # 去除行末的换行符，并将行添加到集合中
                lines_set.add(line.strip())
        return lines_set
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return None
def get_html(url):
    # 发起HTTP GET请求获取页面内容
    response = requests.get(url, headers=headers)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    return None
def get_search_data(en, type):
    i = 1
    while True:
        time.sleep(1)
        url = f'https://www.1905.com/mdb/film/list/country-{en}/mtype-{type}/o0d0p{i}.html'
        soup = get_html(url)
        if soup is None:
            continue
        li_tags = soup.find_all('li', class_='fl line')
        if len(li_tags) == 0:
            return None
        reuslt = []
        for li_tag in li_tags:
            a_tag = li_tag.find('a')
            if a_tag:
                href = a_tag.get('href')
                reuslt.append(href)
        yield reuslt
        i += 1
path = 'href.txt'
read_file_to_set(path)
if __name__ == '__main__':
    futures =[]
    with open('1905/country.txt', 'r', encoding='utf-8') as file:
        country = json.loads(file.read())
    for ct in country['nation']:
        for type in range(1,51):
            for href in get_search_data(ct['en'], type):
                if href is not None:
                    for e in href:
                        if e not in lines_set:
                            append_to_file(str(e), path)
                            lines_set.add(e)
                else:
                    break

