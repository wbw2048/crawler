import multiprocessing
import concurrent.futures
import json
import os
import time
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from Proxy import Proxy

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
}
global_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()+1)
# proxy = Proxy()

def append_to_file(string, filename):
    try:
        # 打开文件，使用追加模式
        with open(filename, 'a') as file:
            # 写入字符串并换行
            file.write(string + '\n')
    except Exception as e:
        print(f"写入文件时出错：{e}")
def read_file_to_set(filename):
    lines_set = set()
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
    while True:
        # proxy_disc = proxy.get_proxy()
        authKey = 'CE14FC5C'
        password = 'E226226BF551'
        proxyAddr = 'tun-lreqvr.qg.net:15773'
        proxyUrl = "http://%(user)s:%(password)s@%(server)s" % {
            "user": authKey,
            "password": password,
            "server": proxyAddr,
        }
        proxies = {
            "http": proxyUrl,
            "https": proxyUrl,
        }
        try:
            response = requests.get(url, headers=headers, proxies=proxies)
            # 检查请求是否成功
            if response.status_code == 200:
                # 使用BeautifulSoup解析HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                return soup
            return None
        except Exception as e:
            pass
def get_data_info(href):
    try:
        time.sleep(1)
        url = f'http://www.1905.com{href}info'
        soup = None
        while soup is None:
            soup = get_html(url)
        dt_list = soup.find_all('dt')
        dd_list = soup.find_all('dd')
        info = {}
        for i in range(len(dt_list)):
            dt = dt_list[i].text.strip().replace(' ', '')
            dd = dd_list[i].text.strip().replace(' ', '')
            if dt != '' and dd != '':
                info[dt] = dd
        url = f'http://www.1905.com{href}scenario'
        soup = None
        while soup is None:
            soup = get_html(url)
        scenario = soup.find_all('li')
        scenario = scenario[len(scenario) - 1].text.replace('\n', '')
        info['scenario'] = scenario
        url = f'http://www.1905.com{href}performer'
        soup = None
        while soup is None:
            soup = get_html(url)
        h3_list = soup.find_all('h3')
        performer = {}
        for i in range(len(h3_list)-1):
            key = h3_list[i].text.strip().replace(' ', '')
            h3_li_list = h3_list[i].findParent('div').find_all('li', 'proList-conts-name')
            if len(h3_li_list) == 0:
                h3_li_list = h3_list[i].findParent('div').find_all('li')
            h_dice = {}
            for h3_li in h3_li_list:
                k = h3_li.find('a').text
                v = h3_li.find('em').text
                h_dice[k] = v
            performer[key] = h_dice
        info['performer'] = performer
        json_file = f'info{href[:len(href) - 1]}.json'
        if not os.path.exists(os.path.dirname(json_file)):
            os.makedirs(os.path.dirname(json_file))
        if not os.path.exists(json_file):
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=4)
        return True, href
    except Exception as e:
        return False, href
path = 'href.txt'
success_path = 'success.txt'
fial_path = 'fial.txt'
success_set = read_file_to_set(success_path)
fial_set = read_file_to_set(fial_path)

if __name__ == '__main__':
    while True:
        futures = []
        lines_set = read_file_to_set(path)
        for href in lines_set:

            if href in success_set and href in fial_set:
                continue
            futures.append(global_thread_pool.submit(get_data_info, href))
        total_count = len(futures)
        with tqdm(total=total_count, desc="下载进度") as pbar:
            for future in futures:
                is_success, href = future.result()
                if is_success:
                    success_set.add(href)
                    append_to_file(href, success_path)
                else:
                    fial_set.add(href)
                    append_to_file(href, fial_path)
                pbar.update(1)



