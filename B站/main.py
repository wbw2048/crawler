import time

from B站.BilibiliInterface import BilibiliInterface
from B站.BilibiliSearch import BilibiliSearch
from B站.utils import user_manager

lines_set = set()
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

def append_to_file(string, filename):
    try:
        # 打开文件，使用追加模式
        with open(filename, 'a') as file:
            # 写入字符串并换行
            file.write(string + '\n')
    except Exception as e:
        print(f"写入文件时出错：{e}")
if __name__ == "__main__":
    key = '车祸'
    log_file = 'bilibili.log'
    user_manager.login()
    bilibili = BilibiliInterface()
    result = BilibiliSearch.search(key)
    for result in BilibiliSearch.search(key):
        try:
            video = bilibili.view_video(bvid=result["bvid"])
            cid, title, part_title, pic, is_dynamic = video.select_video()
            if is_dynamic:
                continue
            video.download_one(cid, pic_url=pic, title=title, part_title=part_title, base_dir=key, save_path="download")
            append_to_file(title, log_file)
            time.sleep(0.5)
        except Exception as e:
            print(f"下载视频时出错：{e}")
            time.sleep(2)