
from selenium import webdriver
import time
import re
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import uuid
import os
import requests
from urllib.parse import urlsplit
import random
from collections import deque
import json

from selenium.webdriver.common.action_chains import ActionChains


from selenium.webdriver.chrome.service import Service

service = Service('./geckodriver')


def sub_num(link):
    parsed_url = urlsplit(link)
    path = parsed_url.path

    # 提取路径中的最后一个部分
    last_part = path.split('/')[-1]

    # 提取末尾的数字
    numbers = ''.join(filter(str.isdigit, last_part))

    return numbers


def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)


# 或者使用JavaScript直接滚动到页面的特定位置
def scroll_to_position(x_pixel, y_pixel):
    driver.execute_script(f"window.scrollTo({x_pixel}, {y_pixel});")


def open_link_and_write_file(line_index, movie_title, web_link, score):

    web_link_arr = web_link.split("?")
    web_link = web_link_arr[0]

    driver.maximize_window()
    ##打开当前链接
    driver.get(web_link)

    driver.implicitly_wait(2)

    current_url = driver.current_url
    if (current_url == 'https://www.youku.com/index/y404?type=showNoAccess&detail=dataError') :
        driver.get(web_link)
        driver.implicitly_wait(2)

    print(current_url)

    new_title_new_h3 = driver.find_element(By.CLASS_NAME, value="new-title-name")
    print("电影名：")
    item_title = new_title_new_h3.text

    title_wrap_root = driver.find_element(By.CLASS_NAME, value="new-title-wrap")
    title_wrap_name = title_wrap_root.find_element(By.CLASS_NAME, value="new-title-name-left")

    title_span_list = title_wrap_name.find_elements(By.TAG_NAME, value="span")

    title_line = ""
    for span_text in title_span_list:
        title_line = title_line + "|" + span_text.text

    title_line_arr = title_line.split("|")
    vip = ''
    if(len(title_line_arr) > 1) :
        vip = title_line_arr[1]

    print("视频简介：")
    print(title_line)

    try:
        new_title_feature_p = title_wrap_root.find_element(By.CLASS_NAME, value="new-title-feature")
        title_wrap_root_p = new_title_feature_p.find_element(By.TAG_NAME, value="p")
        title_wrap_root_p.click()
    except:
        print("出错了 ： " + link)
        try:
            baxia_dialog_root = title_wrap_root.find_element(By.CLASS_NAME, value="baxia-dialog")
            driver.execute_script("arguments[0].remove()", baxia_dialog_root)
            print("删除了拦截对话框 : " + link)
        except:
            print("删除异常：" + link)
        time.sleep(1)

        new_title_feature_p = title_wrap_root.find_element(By.CLASS_NAME, value="new-title-wrap")
        title_wrap_root_p = new_title_feature_p.find_element(By.TAG_NAME, value="p")
        title_wrap_root_p.click()

    new_intro_wrap_root = driver.find_element(By.CLASS_NAME, value="new-intro-wrap")
    new_intro_detail_content = new_intro_wrap_root.find_element(By.CLASS_NAME, value="new-intro-detail")

    detail_desc = new_intro_detail_content.find_element(By.CLASS_NAME, value="new-intro-desc")
    print("简介：")
    print(detail_desc.text)

    detail_desc_list = new_intro_detail_content.find_elements(By.CLASS_NAME, value="new-intro-desc")
    detail_desc_intro = detail_desc_list[len(detail_desc_list) - 1]

    print("演职人员：")
    print(detail_desc_intro.text)

    desc_arr = detail_desc_intro.text.split("\n")
    director = ''
    play_join_member = ''
    if len(desc_arr) > 1 :
        director = desc_arr[0]
        play_join_member = desc_arr[1]
    else:
        play_join_member = desc_arr[0]


    time.sleep(5)

    tabs_wrap_comment_text = str(0)

    try:
        listbox_new = driver.find_element(By.CLASS_NAME, value="listbox-new")
        tabs_wrap_list = listbox_new.find_element(By.CLASS_NAME, value="tabs-wrap")
        tabs_wrap_comment_list = tabs_wrap_list.find_elements(By.TAG_NAME, value="p")
        tabs_wrap_comment = tabs_wrap_comment_list.pop()
        tabs_wrap_comment_count_span = tabs_wrap_comment.find_element(By.TAG_NAME, value="span")

        tabs_wrap_comment_text = tabs_wrap_comment_count_span.text
    except:
        print("评论数量为空 : " + link)

    print("评论数量：")
    comment_count = tabs_wrap_comment_text


    file_name_pre = current_url.split("?")
    file_name_arr = file_name_pre[0].split("/")
    file_name = file_name_arr[len(file_name_arr) - 1].replace(".html","")

    with open('./movie_record/'+str(line_index) + "_"+file_name+'.json', 'w', encoding="utf-8") as file:
        data = {
            'title':item_title,
            'tag':vip,
            'score':score.replace('\n',''),
            'country': title_line,
            'comment':comment_count,
            'descript':detail_desc.text,
            'director':director.replace('导演：',''),
            'player':play_join_member.replace('主演：',''),
            'video_url':current_url
        }
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
        file.close()

        time.sleep(0)

#主程序
if __name__ == '__main__':
    # 设置Chrome浏览器选项
    options = webdriver.FirefoxOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"'
    )
    # 防止系统检测到自动化工具
    # options.set_preference('excludeSwitches',  ['enable-automation'])
    options.set_preference('useAutomationExtension',  False)

    #不加载图片和视频、音频
    options.set_preference('permissions.default.image', 2)
    options.set_preference('permissions.default.stylesheet', 2)

    options.add_argument("-disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-web-security")
    options.add_argument("--autoplay-policy=no-user-gesture-required")

    # 创建WebDriver对象并打开优酷
    driver = webdriver.Firefox(options=options, service=service)

    count = 0
    position = 0
#    special_index_position = 4204
#    special_index_position = 4283
#    special_index_position = 4291
    special_index_position = 0
    index_position = 8870

    error_txt = './youku-movie-error.txt'

    with open('./youku-movie-list-utf-8.txt', 'r', encoding="utf-8") as file:
        for line_index, line in enumerate(file.readlines(), 1):
            try:
                if line_index <= index_position:
                    if (line_index == special_index_position and special_index_position > 0):
                        count = count + 1
                        content = line.split("||")
                        title = content[0]
                        link = content[1]
                        score = content[2]

                        print("特殊处理 ：" + str(line_index) + "， 链接 ： " + line)
                        open_link_and_write_file(line_index, title, link, score)

                    print('已经爬取过了： ')
                    print(line_index)
                    print(line)
                    continue

                count = count + 1
                content = line.split("||")
                title = content[0]
                link = content[1]
                score = content[2]

                open_link_and_write_file(line_index, title, link, score)
                print("计数器：" + str(count))
            except Exception as e3:
                print("爬取失败： ")
                print(line)
                print(e3)
                with open(error_txt, 'a', encoding="utf-8") as error_file:
                    error_file.write(str(line_index) + "||" + line)
                    error_file.write("\n")
                time.sleep(60)
                continue

    # 关闭浏览器
    driver.quit()


