import threading
import time

import requests
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self):
        self._lock = threading.RLock()
        self.index = 0
        self.proxy_list = []

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        }
        self.refresh_thread = threading.Thread(target=self.refresh_proxy)
        self.refresh_thread.start()

    def get_proxy(self):
        with self._lock:
            self.index += 1
            if self.index >= len(self.proxy_list):
                self.index = 0
            return self.proxy_list[self.index-1]
    def refresh_proxy(self):
        while True:
            proxy_list = []
            for i in range(1,10):
                url = f"http://www.kxdaili.com/dailiip/1/{i}.html"
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                ip_list = soup.find('table', {'class': 'active'}).find_all('tr')
                for ip in ip_list:
                    tds = ip.find_all('td')
                    if len(tds) > 0:
                        if 'HTTP' in tds[3].text:
                            ip_address = tds[0].text
                            ip_port = tds[1].text
                            proxy_list.append({
                                'http': "http://{0}:{1}".format(ip_address, ip_port),
                                # 'https': "https://{0}:{1}".format(ip_address, ip_port),
                            })
            self.proxy_list = proxy_list
            time.sleep(20)