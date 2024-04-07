import os
import execjs
import requests
theme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "info.js")
cookies_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cookies.txt")
print(theme_path)
js = execjs.compile(open(theme_path, 'r', encoding='utf-8').read())

class Note_Detail():
    def __init__(self, id, note_id, note_type, user_id, nickname, avatar, title, desc, liked_count, collected_count, comment_count, share_count, video_addr, image_list, tag_list, upload_time, ip_location):
        self.id = id
        self.note_id = note_id
        self.note_type = note_type
        self.user_id = user_id
        self.nickname = nickname
        self.avatar = avatar
        self.title = title
        self.desc = desc
        self.liked_count = liked_count
        self.collected_count = collected_count
        self.comment_count = comment_count
        self.share_count = share_count
        self.video_addr = video_addr
        self.image_list = image_list
        self.tag_list = tag_list
        self.upload_time = upload_time
        self.ip_location = ip_location

    def __str__(self):
        # 每个值都要换行
        return f'id: {self.id}\n' \
                f'note_id: {self.note_id}\n' \
                f'user_id: {self.user_id}\n' \
                f'nickname: {self.nickname}\n' \
                f'avatar: {self.avatar}\n' \
                f'title: {self.title}\n' \
                f'desc: {self.desc}\n' \
                f'liked_count: {self.liked_count}\n' \
                f'collected_count: {self.collected_count}\n' \
                f'comment_count: {self.comment_count}\n' \
                f'share_count: {self.share_count}\n' \
                f'video_addr: {self.video_addr}\n' \
                f'images: {self.image_list}\n' \
                f'tag_list: {self.tag_list}\n' \
                f'upload_time: {self.upload_time}\n' \
                f'note_ip_location: {self.ip_location}\n'
def get_search_data():
    return {
        "image_scenes": "FD_PRV_WEBP,FD_WM_WEBP",
        "keyword": "",
        "note_type": "0",
        "page": "",
        "page_size": "20",
        "search_id": "2c7hu5b3kzoivkh848hp0",
        "sort": "general"
    }
def get_headers():
    return {
        "authority": "edith.xiaohongshu.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.xiaohongshu.com",
        "referer": "https://www.xiaohongshu.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
        "x-s": "",
        "x-t": ""
    }
def get_params():
    return {
        "num": "30",
        "cursor": "",
        "user_id": "",
        "image_scenes": ""
    }
def get_note_data(note_id):
    return {
        "source_note_id": note_id,
        "image_scenes": [
            "CRD_PRV_WEBP",
            "CRD_WM_WEBP"
        ]
    }
def handle_note_info(data):
    note_id = data['id']
    note_type = data['note_card']['type']
    user_id = data['note_card']['user']['user_id']
    nickname = data['note_card']['user']['nickname']
    avatar = data['note_card']['user']['avatar']
    title = data['note_card']['title']
    desc = data['note_card']['desc']
    liked_count = data['note_card']['interact_info']['liked_count']
    collected_count = data['note_card']['interact_info']['collected_count']
    comment_count = data['note_card']['interact_info']['comment_count']
    share_count = data['note_card']['interact_info']['share_count']
    if note_type == 'video':
        video_addr = 'https://sns-video-bd.xhscdn.com/' + data['note_card']['video']['consumer']['origin_video_key']
    else:
        video_addr = ''
    image_list = data['note_card']['image_list']
    tags_temp = data['note_card']['tag_list']
    tags = []
    for tag in tags_temp:
        try:
            tags.append(tag['name'])
        except:
            pass
    upload_time = data['note_card']['time']
    if 'ip_location' in data['note_card']:
        ip_location = data['note_card']['ip_location']
    else:
        ip_location = '未知'
    note_detail = Note_Detail(None, note_id, note_type, user_id, nickname, avatar, title, desc, liked_count,
                              collected_count, comment_count, share_count, video_addr, image_list, tags, upload_time,
                              ip_location)
    return note_detail

def check_cookies():
    more_url = 'https://edith.xiaohongshu.com/api/sns/web/v1/user_posted'
    params = get_params()
    headers = get_headers()
    if not os.path.exists(cookies_path):
        raise Exception("获取cookie")
    test_user_id = '59e46bda4eacab0b31ada6df'
    with open(cookies_path, "r", encoding="utf-8") as f:
        cookies_obj = f.read()
    # 将字符串按分号分割成键值对列表
    cookies_list = cookies_obj.split("; ")
    # 初始化一个空字典
    cookies_local = {}
    # 遍历键值对列表，将每个键值对解析为字典的键值，并添加到字典中
    for pair in cookies_list:
        key, value = pair.split("=")
        cookies_local[key] = value
    params['user_id'] = test_user_id
    params['cursor'] = ''
    api = f"/api/sns/web/v1/user_posted?num=30&cursor=&user_id={test_user_id}&image_scenes="
    a1 = cookies_local['a1']
    ret = js.call('get_xs', api, '', a1)
    headers['x-s'], headers['x-t'] = ret['X-s'], str(ret['X-t'])
    response = requests.get(more_url, headers=headers, cookies=cookies_local, params=params)
    res = response.json()
    if not res["success"]:
        raise Exception("cookie失效")
    else:
        print("cookie有效")
        return cookies_local