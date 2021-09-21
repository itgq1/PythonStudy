import time
from selenium import webdriver

# 1、创建Chrome实例 。
driver = webdriver.Chrome()
# 2、driver.get方法将定位在给定的URL的网页 。
driver.get(r"https://www.12306.cn/index/index.html")
# 3、定位元素 。
# 3.1、用id定位输入框对象，
# driver.find_element_by_id("kw").send_keys("python")
# 3.2、用id定位点击对象，用click()触发点击事件
# driver.find_element_by_id('qd_closeDefaultWarningWindowDialog_id').click()
# driver.find_element_by_id('query_ticket').click()
# time.sleep(3)  # 延迟3秒
# 4、退出访问的实例网站。
# driver.quit()

