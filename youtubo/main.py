import requests
from pytube import YouTube
from youtube_search import YoutubeSearch
import concurrent.futures

global_thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# 将Cookie设置到pytube的请求中
def set_cookie_to_pytube(youtube_cookie):
    with open(youtube_cookie, "r", encoding="utf-8") as f:
        cookies_obj = f.read()
    # 将字符串按分号分割成键值对列表
    cookies_list = cookies_obj.split("; ")
    # 初始化一个空字典
    cookies_local = {}
    # 遍历键值对列表，将每个键值对解析为字典的键值，并添加到字典中
    for pair in cookies_list:
        try:
            key, value = pair.split("=")
            cookies_local[key] = value
        except ValueError:
            continue
    session = requests.Session()
    # 设置Cookie
    session.cookies.update(cookies_local)
    # 设置pytube的请求会话对象
    YouTube.requests = session
def search_videos(query):
    while True:
        for video in YoutubeSearch(query).videos:
            yield video
def download_videos(url_suffix,output_path='data'):
    set_cookie_to_pytube('cookies.txt')
    def on_progress(stream, chunk, remaining_bytes):
        total_size = stream.filesize
        bytes_downloaded = total_size - remaining_bytes
        progress = (bytes_downloaded / total_size) * 100
        print(
            f"Downloading: {stream.title} - {bytes_downloaded / 1024 / 1024:.2f}MB/{total_size / 1024 / 1024:.2f}MB ({progress:.2f}%)")
    url = 'https://www.youtube.com'+url_suffix
    yt = YouTube(url, on_progress_callback=on_progress)
    print("Title:", yt.title)
    print("Length:", yt.length, "seconds")
    print("Description:", yt.description)
    print("==================================")
    # 获取视频的最高质量的流
    stream = yt.streams.get_highest_resolution()
    # 下载视频并保存到指定目录
    stream.download(output_path)
    print("Download successful!")
if __name__ == '__main__':
    query = 'aerial photography'
    for video in search_videos(query):
        try:
            download_videos(video['url_suffix'])
        except Exception as e:
            print(e)
