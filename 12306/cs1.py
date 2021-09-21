import time
from captcha import Code
from selenium import webdriver



username = '1'
password = '1'

# 1.打开浏览器
driver = webdriver.Chrome()
# 2.打开12306网页
driver.get('https://www.12306.cn/index/index.html')
# 3.登录模块
# 3.1点击登录
driver.find_element_by_link_text('登录').click()
time.sleep(0.2)
# 3.2点击账号登录
driver.find_element_by_link_text('账号登录').click()
# 3.3输入账号密码
# 3.3.1输入账号
driver.find_element_by_id('J-userName').send_keys(username)
# 3.3.2输入密码
driver.find_element_by_id('J-password').send_keys(password)
# 3.3.3验证码识别
c = Code(driver)
c.main()