import pandas as pd
from pytube import YouTube
import os
from tqdm import tqdm

# 创建一个空集合用于存储行
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

def is_download_complete(file_path, expected_size):
    # 获取下载文件的大小
    file_size = os.path.getsize(file_path)
    if file_size == expected_size:
        return True
    else:
        return False
# 下载视频的函数
def download_video(video_id, url, path, log_file, fail_log):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4')
        # 尝试选择指定清晰度的视频
        selected_stream = stream.order_by('resolution').desc().first()
        if selected_stream:
            video_id = yt.video_id
            filename = f"{video_id}.mp4"
            filename = os.path.join(path, filename)
            if os.path.exists(filename):
                # 获取预期的文件大小
                expected_size = selected_stream.filesize
                # 检查文件是否完整下载
                if is_download_complete(filename, expected_size):
                    append_to_file(video_id, log_file)
                    print(f"{filename} 已存在，跳过下载！")
                    return True
                else:
                    print(f"{filename} 文件下载不完整，重新下载！")
            selected_stream.download(filename=filename)
            append_to_file(video_id, log_file)
            print(f"{filename} 视频下载完成！")
            return True
        else:
            append_to_file(video_id, fail_log)
            return False
    except Exception as e:
        append_to_file(video_id, fail_log)
        print("下载视频时出现错误：", e)
        return False

if __name__ == "__main__":
    log_file = 'panda_70.log'
    fail_log = 'fail_log.log'
    csv_file = 'panda70_aerial.csv'
    path = 'download'
    df = pd.read_csv(csv_file)
    total_count = len(df)
    success_count = 0
    fail_count = 0
    read_file_to_set(log_file)
    read_file_to_set(fail_log)
    # 创建进度条
    with tqdm(total=total_count, desc="下载进度") as pbar:
        for index, row in df.iterrows():
            if row[0] in lines_set:
                success_count = success_count + 1
                print(f"{row[0]} 已存在，跳过下载！")
                continue
            video_url = row[1]
            if download_video(row[0], video_url, path, log_file, fail_log):
                success_count = success_count +1
            else:
                fail_count = fail_count +1
            pbar.update(1)  # 更新进度条
            print(f"成功下载{success_count}个视频，失败{fail_count}个视频。")
