from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import random
def read_file_to_set(filename):
    lines_set = set()
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
#.//img[@class="lazyload crop-image-container__img"]
if __name__ == '__main__':
    search = '旗袍'
    driver_path = './geckodriver'
    file_name = 'xiyin.txt'
    options = webdriver.FirefoxOptions()
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"'
    )
    service = Service(driver_path)
    driver = webdriver.Firefox(options=options, service=service)
    driver.get(f"https://www.shein.com.hk/pdsearch/{search}")
    total = driver.find_element(By.XPATH, './/span[@class="sui-pagination__total"]').text
    total = total[1:len(total)-1].strip()
    total = int(total)
    set_href = read_file_to_set(file_name)
    for i in range(total):
        for j in range(5):
            anchors = driver.find_elements(By.XPATH, './/section/.//a[@target="_blank"]')
            driver.execute_script("arguments[0].scrollIntoView();", anchors[len(anchors) - 1])
            time.sleep(random.uniform(0.5, 1.5))
        anchors = driver.find_elements(By.XPATH, './/section/.//a[@target="_blank"]')
        for anchor in anchors:
            href = anchor.get_attribute('href')
            href = href[:href.rfind('?')]
            if href not in set_href:
                append_to_file(href, file_name)
                set_href.add(href)
        if i +1 <total:
            driver.find_element(By.XPATH, './/span[@class="sui-pagination__next sui-pagination__btn sui-pagination__hover"]').click()