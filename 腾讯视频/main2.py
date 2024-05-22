import json
import re
import time

import requests
from bs4 import BeautifulSoup

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

headers = {
    "authority": "pbaccess.video.qq.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "origin": "https://v.qq.com",
    "referer": "https://v.qq.com/",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}



def get_html(url, path):
    # 发起HTTP GET请求获取页面内容
    response = requests.get(url, headers=headers)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        result_json = {
            '人员': {}
        }
        scripts = soup.select('script')
        for script in scripts:
            if script.text.strip().startswith('window.__PINIA__='):
                text = script.text.strip()[len('window.__PINIA__='):]
                text = text.replace('undefined', '"undefined"').replace('Array.prototype.slice.call(', '').replace(')','')
                json_data = json.loads(text)
                for item in json_data['introduction']['starData']['list']:
                    result_json['人员'][item['star_name']] = item['star_role_label']
                item = json_data['introduction']['introData']['list'][0]
                result_json['main_genres'] = item['item_params'].get('main_genres')
                result_json['title'] = item['item_params']['title']
                result_json['year'] = item['item_params'].get('year')
                result_json['sub_genre'] = item['item_params'].get('sub_genre')
                result_json['cover_description'] = item['item_params'].get('cover_description')
                result_json['hotval'] = item['item_params'].get('hotval')
                with open(path + item['item_params']['title'] + '.json', 'w', encoding='utf-8') as f:
                    json.dump(result_json, f, ensure_ascii=False, indent=4)
                    f.close()
                    return result_json

if __name__ == '__main__':
    set_list = read_file_to_set("s.txt")
    with open('te.csv', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line not in set_list:
                get_html(line, '综艺/')
                append_to_file(line, 's.txt')
                time.sleep(2)