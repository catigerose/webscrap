

import requests
import time
from bs4 import BeautifulSoup
from platform import system
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# 根据操作系统指定工作目录，使代码在linux和windows都能运行。
if system() == 'Linux':
    work_dir = "/home"
elif system() == 'Windows':
    work_dir = "."
else:
    print("waring： platform.system is not linux or windows")
    work_dir = "."

chromedriver_path = work_dir+'/chromedriver'  # chromedriver的路径


# 获取 任何网页的内容，返回bs4的soup文件


def get_soup(url, is_dynamic=False):

    if is_dynamic:
        options = Options()  # 实例化一个chrome浏览器实例对象
        options.add_argument("headless")  # 不打开浏览器窗口 运行selenium
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--disable-gpu")
        # options.add_argument("--remote-debugging-port=9222")  # this

        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        options.add_argument('--user-agent=%s' % user_agent)

        # 函数更新，使用service传参数，解决警告 DeprecationWarning: executable_path has been deprecated, please pass in a Service object
        s = Service(chromedriver_path)
        driver = Chrome(service=s, options=options)  # 新建driver
        driver.maximize_window()  # 最大化窗口

        driver.get(url)  # 获取页面内容
        time.sleep(2)  # 等待5s，等待加载完成

        page_source = driver.page_source  # 获取页面源码数据
        soup = BeautifulSoup(page_source, features="lxml")  # 用 BeautifulSoup解析
        driver.close()

    else:
        # 请求头
        headers = {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36", }
        ret = requests.get(url, headers=headers)
        ret.encoding = ret.apparent_encoding
        time.sleep(1)
        soup = BeautifulSoup(ret.text, 'html.parser')  # 构建beautifulsoup实例
    return soup



