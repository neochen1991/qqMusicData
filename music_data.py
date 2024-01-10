from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

# 指定Chrome驱动程序的路径
driver_path = './driver/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 创建Chrome浏览器的一个实例，并指定驱动程序路径
service = ChromeService(executable_path=driver_path)
chrome = webdriver.Chrome(service=service)

# 打开网站
url = 'https://tool.curleyg.info'
chrome.get(url)

