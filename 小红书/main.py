import json
import os
import re
import time

import requests
import concurrent.futures
from PIL import Image
from io import BytesIO
from util import js, check_cookies, get_headers, get_search_data, get_note_data, handle_note_info

global_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)
cookies = None
headers = get_headers()
if cookies is None:
    cookies = check_cookies()
else:
    cookies = cookies
def search(query, sort = 'general',note_type = 0, page=1):
    data = get_search_data()
    data['sort'] = sort
    data['note_type'] = note_type
    api = '/api/sns/web/v1/search/notes'
    data = json.dumps(data, separators=(',', ':'))
    data = re.sub(r'"keyword":".*?"', f'"keyword":"{query}"', data)
    data = re.sub(r'"page":".*?"', f'"page":"{page}"', data)
    search_url = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
    ret = js.call('get_xs', api, data, cookies['a1'])
    headers['x-s'], headers['x-t'] = ret['X-s'], str(ret['X-t'])
    response = requests.post(search_url, headers=headers, cookies=cookies, data=data.encode('utf-8'))
    res = response.json()
    items = res['data']['items']
    return items
def get_one_note_info(uri):
    feed_url = 'https://edith.xiaohongshu.com/api/sns/web/v1/feed'
    note_id = uri.split('/')[-1]
    data = get_note_data(note_id)
    data = json.dumps(data, separators=(',', ':'))
    ret = js.call('get_xs', '/api/sns/web/v1/feed', data, cookies['a1'])
    headers['x-s'], headers['x-t'] = ret['X-s'], str(ret['X-t'])
    response = requests.post(feed_url, headers=headers, cookies=cookies, data=data)
    res = response.json()
    try:
        data = res['data']['items'][0]
    except:
        print(f'笔记 {note_id} 不允许查看')
        return
    note = handle_note_info(data)
    return note
def get_note_list(query, sort = 'general',note_type = 0):
    detail_url = 'https://www.xiaohongshu.com/explore/'
    page = 1
    while True:
        notes = search(query, sort, note_type, page)
        if len(notes) == 0:
            break
        for note in notes:
            note_id = note['id']
            note_url = detail_url + note_id
            print(note_url)
            note = get_one_note_info(note_url)
            if note is None:
                continue
            yield note
        page += 1
def norm_str(str):
    new_str = re.sub(r"|[\\/:*?\"<>| ]+", "", str).replace('\n', '').replace('\r', '')
    return new_str
def check_and_create_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return False
    return True
def download_media(path, name, url, type):
    # 5次错误机会
    for i in range(5):
        try:
            file_name = path + '/' + name + '.jpg'
            file_name = os.path.abspath(file_name)
            if os.path.exists(path + '/' + name + '.jpg'):
                print(file_name + ' already exists')
                return
            content = requests.get(url).content
            with open(file_name, mode="wb") as f:
                f.write(content)
            print(file_name + ' download')
            break
        except:
            print(f"第{i + 1}次下载失败，重新下载, 剩余{4 - i}次机会")
            continue

def save_one_note(note, keyword, dir_path='data'):
    nickname = norm_str(note.nickname)
    user_id = note.user_id
    title = norm_str(note.title)
    if title.strip() == '':
        title = f'无标题'
    path = f'./{dir_path}/{keyword}/{nickname}_{title}'
    check_and_create_path(path)
    note_type = note.note_type
    if note_type == 'normal':
        for img_index, img in enumerate(note.image_list):
            img_url = img['info_list'][1]['url']
            global_thread_pool.submit(download_media, path, f'image_{img_index}', img_url, 'image')
        time.sleep(1)

if __name__ == '__main__':
    query = '古装服装搭配'
    dir_path = 'data'
    for note in get_note_list(query):
        save_one_note(note, query, dir_path=dir_path)