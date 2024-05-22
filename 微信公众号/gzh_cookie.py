
import builtins
import json
import os
import random
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import numpy as np
import requests
from bs4 import BeautifulSoup
from retry import retry
import base64
from selenium.webdriver.chrome.service import Service

books=[]

class Urls:
    index = 'https://www.xiaohongshu.com'
    editor = 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=10&isMul=1&isNew=1&share=1&lang=zh_CN&token={token}'
    query_biz = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&token={token}&lang=zh_CN&f=json&ajax=1&random={random}&query={query}&begin={begin}&count={count}'
    query_arti = 'https://mp.weixin.qq.com/cgi-bin/appmsg?token={token}&lang=zh_CN&f=json&%E2%80%A65&action=list_ex&begin={begin}&count={count}&query={query}&fakeid={fakeid}&type=9'

class Session:
    token = ''
    cookies = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def set_cookies(driver, cookies):
    Session.cookies = {}
    for item in json.loads(base64.b64decode(cookies)):
        driver.add_cookie(item)
        Session.cookies[item['name']]=item['value']

class SpiderWeixin():
    def __init__(self): #构造函数不带参数
        print("jjj")
    def weixin_gzh_login(self):
        cookies_cache = "cookies_cache/"
        if not os.path.exists(cookies_cache):
            os.makedirs(cookies_cache)
        service = Service(executable_path="/usr/local/bin/chromedriver")
        driver = webdriver.Chrome(service=service)
        cookies = json.load(open(cookies_cache+'cookies.json', 'rb')) if os.path.isfile(cookies_cache+'cookies.json') else []
        driver.get(Urls.index)
        if not cookies:
            input("请先手动登录, 完成后按回车继续:")
            cookies = driver.get_cookies()
            open(cookies_cache+'cookies.json', 'wb').write(json.dumps(cookies).encode('utf-8'))
        cookie64 = base64.b64encode(json.dumps(cookies).encode('utf-8'))
        set_cookies(driver, cookie64)
        driver.get(Urls.index)
        '''url = driver.current_url
        if 'token' not in url:
            raise Exception(f"获取网页失败!")
        Session.token = re.findall(r'token=(\w+)', url)[0]
        '''
        print(cookie64)
if __name__ == '__main__':
    thread_nums=1
    #chrome_path,gzh_name,sleep_time,page,pagesize,cookies
    spiderWeixin = SpiderWeixin()
    spiderWeixin.weixin_gzh_login()



