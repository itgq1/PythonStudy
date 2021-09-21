# -*- coding: utf-8 -*-
# @Time    : 2021/4/30 14:40
# @Author  : Lxsky
# @File    : main.py
# @Software: PyCharm

import requests
import json
import lxml


class Ticketing(object):

    def __init__(self):



if __name__ == '__main__':

    with open('./city.json', 'r', encoding='utf-8') as f:  # 一定要加encoding='utf-8'进行编码的转换
        j = json.load(f)
    print(j['北京'])
