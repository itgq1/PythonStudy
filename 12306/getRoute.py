from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import time
from check_ticket import Check  # 余票查询模块
from captcha import Code  # 验证码处理模块


class Buy_Ticket():
    def __init__(self, start_station, end_station, date, username, password, purpose, names):
        self.num = 1
        self.start = start_station
        self.end = end_station
        self.date = date
        self.username = username
        self.password = password
        self.purpose = purpose
        self.all_names = names
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'

    # 模拟登录函数，包括自动填充用户名、密码、自动点击验证、最终自动登录
    def login(self):
        browser.get(self.login_url)
        time.sleep(0.5)
        try:
            wait.WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'login-hd-account'))).click()
            input_name = browser.find_element_by_id('J-userName')
            input_pd = browser.find_element_by_id('J-password')
            input_name.send_keys(self.username)
            input_pd.send_keys(self.password)
            start_end, check = self.add_cookie()
            # time.sleep(5)
            c = Code(browser)  # 调用验证码识别模块
            c.main()
            print('登录成功！')
            time.sleep(0.8)
            print(browser.current_url)
            # try:
            # wait.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CLASS_NAME,'btn.btn-primary.ok'))).click()
            # except NoSuchElementException:
            # pass
            self.check(start_end, check)
        except NoSuchElementException:
            print('没有找到元素')
            self.login()

    # 2020.12.19更新
    def add_cookie(self):
        check = Check(self.date, self.start, self.end, self.purpose)
        start_end = check.look_up_station()
        # cookie的添加，json.dumps把以汉字形式呈现的起始、终点站转化成unicode编码，可在审查元素里查看cookie
        browser.add_cookie({'name': '_jc_save_fromStation',
                            'value': json.dumps(self.start).strip('"').replace('\\', '%') + '%2C' + start_end[0]})
        browser.add_cookie({'name': '_jc_save_toStation',
                            'value': json.dumps(self.end).strip('"').replace('\\', '%') + '%2C' + start_end[1]})
        browser.add_cookie({'name': '_jc_save_fromDate', 'value': self.date})
        print('cookie添加完成！')
        return start_end, check

    # 余票查询函数，获取预定车次信息
    def check(self, start_end, check):
        # 调用余票查询模块
        browser.get(self.ticket_url)
        self.num = check.get_info(start_end, 1)
        browser.find_element_by_id('qd_closeDefaultWarningWindowDialog_id').click()
        button = wait.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.ID, 'query_ticket')))
        button.click()
        if self.purpose == '学生':
            browser.find_element_by_id('sf2').click()
            button.click()



    def check_date(self):
        # 12306学生票的时间是：暑假：6月1日-9月30日，寒假：12月1日-3月31日
        date = ''.join(self.date.split('-'))
        # 暑假
        if int(date[:4] + '0601') <= int(date) <= int(date[:4] + '0930'):
            return 1
        # 当年寒假，也就是当年的1、2、3月
        if int(date[:4] + '0101') <= int(date) <= int(date[:4] + '0331'):
            return 1
        # 这里处理的是从当年12月到第二年的3月，比如在2020-12-12买2021-01-18的学生票，那么就是在下面的处理区间
        next_year = str(int(date[:4]) + 1)
        if int(date[:4] + '1201') <= int(date) <= int(next_year + '0331'):
            return 1
        return 0

    # 车票预定函数
    def book_ticket(self):
        time.sleep(1.5)
        print('开始预订车票...')
        # 先查找出所有车次对应的预订按钮，再根据余票查询模块返回的车次序号，点击相应的预订按钮
        button = browser.find_elements_by_class_name('no-br')
        button[self.num - 1].click()
        time.sleep(1.5)
        # 选择乘车人
        # 获取所有乘车人的信息
        passengers = browser.find_element_by_id('normal_passenger_id')
        names = passengers.text.split('\n')
        for name in self.all_names:
            index = names.index(name)
            browser.find_element_by_id('normalPassenger_' + str(index)).click()
            if '学生' in name:
                if self.check_date():
                    browser.find_element_by_id('dialog_xsertcj_ok').click()

                else:
                    print('当前日期不在学生票可购买时间区间！')
                    print('学生票乘车时间为暑假6月1日至9月30日、寒假12月1日至3月31日！')
                    browser.find_element_by_id('dialog_xsertcj_cancel').click()
        # browser.close()
        browser.find_element_by_id('submitOrder_id').click()
        wait.WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.ID, 'qr_submit_id'))).click()
        print('车票预定成功！请在30分钟内完成付款！')

    def main(self):
        self.login()
        if self.num:
            self.book_ticket()
        else:
            browser.close()
            return


if __name__ == '__main__':
    begin = time.time()
    # 隐藏浏览器
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")  # 2020.03.28更新
    browser = webdriver.Chrome(options=options)
    browser.maximize_window()
    # Buy_Ticket类初始化参数，从左到右：出发站，终点站，出发日期，账号，密码，购票类型(默认购买成人票，若要购买学生票，
    # 添加乘客姓名时在后面加上(学生))，把要购买票的乘客姓名放在一个列表里
    b = Buy_Ticket('上海', '重庆', '2021-6-15', '15905628151', '121899gao', 'ADULT', ['乘客1姓名', '乘客2姓名(学生)']); b.main()
    end = time.time()
    print('总耗时：%d秒' % int(end - begin))
    # browser.close()