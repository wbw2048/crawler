import multiprocessing
import concurrent.futures
import json
import os
import threading
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup

class Proxy:
    def __init__(self):
        self._lock = threading.RLock()
        self.index = 0
        self.proxy_list = []
        self.url = "https://www.zdaye.com/free/?ip=&adr=&checktime=&sleep=&cunhuo=&dengji=&nadr=&https=1&yys=&post=%E6%94%AF%E6%8C%81&px="
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        }
        self.refresh_proxy()

    def get_proxy(self):
        self.index += 1
        if self.index >= len(self.proxy_list):
            self.index = 0
        return self.proxy_list[self.index-1]
    def refresh_proxy(self):
        response = requests.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_list = soup.find('table', {'id': 'ipc'}).find_all('tr')
        proxy_list = []
        for ip in ip_list:
            tds = ip.select("td")
            ip_address = tds[0].text
            ip_port = tds[1].text
            proxy_list.append({
                'http': "http://{0}:{1}".format(ip_address, ip_port),
                'https': "https://{0}:{1}".format(ip_address, ip_port)
            })
