from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.action_chains import ActionChains

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


class SeleniumInitializer:
    def __init__(self, driver_path, headless=False):
        # 设置 Chrome WebDriver 的路径
        self.driver_path = driver_path

        # 配置 Chrome WebDriver 的选项
        options = webdriver.FirefoxOptions()
        options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0"'
        )
        service = Service(self.driver_path)
        # 创建WebDriver对象并打开
        self.driver = webdriver.Firefox(options=options, service=service)

    def get_driver(self):
        return self.driver

    def close_driver(self):
        self.driver.quit()


def on_click(driver, name):
    target_element = driver.find_element(By.XPATH,
                                         f'.//div[@dt-eid="choose_item" and @class="item" and normalize-space(text())="{name}"]')
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", target_element)
    # 点击元素
    target_element.click()


# 示例用法
if __name__ == "__main__":
    driver_path = "./geckodriver"  # Chrome WebDriver 的路径
    selenium_initializer = SeleniumInitializer(driver_path, headless=True)  # 初始化 SeleniumInitializer
    driver = selenium_initializer.get_driver()  # 获取 WebDriver 实例
    driver.get("https://v.qq.com/channel/variety/list")  # 打开网页
    action_chains = ActionChains(driver)
    timeout = 15
    file_name = 'te.csv'
    set_href = read_file_to_set(file_name)
    previous_hrefs = {}
    last_update_time = time.time()
    while True:
        anchors = driver.find_elements(By.XPATH, './/a[@class="card horizontal"]')
        for anchor in anchors:
            # 将元素滚动到视图中
            href = anchor.get_attribute('href')
            if anchor not in previous_hrefs or previous_hrefs[anchor] != href:
                print(f"Anchor href changed: {href}")
                previous_hrefs[anchor] = href
                last_update_time = time.time()
                if href not in set_href:
                    append_to_file(href, file_name)
        try:
            driver.execute_script("arguments[0].scrollIntoView();", anchors[len(anchors) - 1])
            time.sleep(random.uniform(0.5, 1.5))
        except Exception as e:
            print(e)
    selenium_initializer.close_driver()  # 关闭 WebDriver
