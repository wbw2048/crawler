import os
import queue
import threading

import requests
from lxml import etree
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
}
q = queue.Queue()

def download_image(urls, path):
    for url in urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            name = url.split('/')[-1]
            file = os.path.join(path, name)
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'wb') as f:
                f.write(response.content)
def search(key, page, pagesize):
    url = (
        f'https://hmsearch.applesay.cn/api-product-hm/product/textSearch?storeId=0&filters%5Bsize%5D={pagesize}&filters'
        f'%5Bsort%5D=stock&filters%5Bquery%5D={key}&filters%5Bfrom%5D={page}')
    res = requests.get(url, headers=headers)
    data = res.json()
    return data
def get_data(url):
    result = []
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    img_list = html.xpath('//div[@class="column main"]//div[@class="item"]/img')
    for img in img_list:
        srcset = img.xpath('./@srcset')
        srcset = str(srcset[0]).split(',')
        img_src = srcset[-1].split(' ')[0]
        result.append(img_src)
        print(img_src)
    return result

def producer():
    for i in range(10):
        data = search('短袖', 20*i, 20)
        for item in data['items']:
            q.put(item['url'])
def consumer():
    while True:
        key = q.get()
        if key is None:
            break
        image_url_list = get_data(key)
        path = key.split('/')[-1]
        path = path.split('.')[0]
        download_image(image_url_list, f"./data/{path}")
        q.task_done()

if __name__ == '__main__':
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    # 启动线程
    producer_thread.start()
    consumer_thread.start()
    producer_thread.join()
    q.join()
    q.put(None)
    consumer_thread.join()
    print("All tasks are done.")
