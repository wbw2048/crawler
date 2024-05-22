import os
import queue
import threading
from urllib.parse import quote

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
}
q = queue.Queue()

def search(key, page=1, pageSize=20):
    url = 'https://d.uniqlo.cn/p/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_CN'
    payload = {"url": f"/search.html?description={quote(key)}&searchType=2",
               "pageInfo": {"page": page, "pageSize": pageSize, "withSideBar": "Y"}, "belongTo": "pc",
               "rank": "overall",
               "priceRange": {"low": 0, "high": 0}, "color": [], "size": [], "season": [], "material": [], "sex": [],
               "categoryFilter": {}, "identity": [], "insiteDescription": "", "exist": [], "searchFlag": True,
               "description": f"{key}"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
def get_data(key):
    url = f'https://www.uniqlo.cn/data/products/zh_CN/{key}.json'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
def download_image(urls, path):
    host = 'https://www.uniqlo.cn'
    for url in urls:
        response = requests.get(host+url, headers=headers)
        if response.status_code == 200:
            name = url.split('/')[-1]
            file = os.path.join(path, name)
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, 'wb') as f:
                f.write(response.content)

def producer():
    for i in range(10):
        data = search("短袖", page=(i+1), pageSize=20)
        for item in data['resp'][1]:
            q.put(item['productCode'])
def consumer():
    while True:
        key = q.get()
        if key is None:
            break
        data = get_data(key)
        if 'main1000' in data:
            image_url_list = data['main1000']
        elif 'main561' in data:
            image_url_list = data['main561']
        elif 'main80' in data:
            image_url_list = data['main80']
        download_image(image_url_list, f"./data/{key}")
        q.task_done()


if __name__ == "__main__":
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


