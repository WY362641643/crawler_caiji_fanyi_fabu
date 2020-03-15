# coding=utf-8
# !/usr/bin/env python
# from multiprocessing import Process
# from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests_toolbelt import MultipartEncoder
from selenium.webdriver.common.by import By
from multiprocessing import Queue
from urllib import parse as up
from selenium import webdriver
from urllib.parse import quote
from threading import Thread
from hashlib import md5
from lxml import etree
from lxml import html
from PIL import Image
import html as htmls
import datetime
import requests
import pymysql
import random
import redis
import time
import json
import os
import re
import jieba
import jieba.analyse

# 数据库接口配置
# HOST = 'ymhack.wicp.net'
# RedisPORT = 16379
# SQLPORT = 13306
HOST = '127.0.0.1'
RedisPORT = 6379
SQLPORT = 3306
SQLhost= '127.0.0.1'
SQLuser = "tp5admin"
SQLpwd = "HKxGpYfC5MmhPWe4"
SQLdbname = "tp5admin"


key_delet =[
    '<.*?>',
    '(原标题.*?)\n',
    '(本文原创.*?)\n',
    '(来源.*?)\n',
    "1[3458]\\d{9}",
    "[1-9]\\d{4,10}",
    '返回搜狐，查看更多',
    '返回搜狐并查看更多',
    '声明：.*?\n',
    '转载.*?\n',
    '注明出处',
    '联系我们',
    '公众号.*?\n'
    '微信',
    '展开全部',
    '来源',
    '百度首页\n登录\n个人中心\n帐号设置\n意见反馈\n退出\n',
    '负责编辑',
]

# 获取 User_Agent
class User_Agent(object):
    """
        直接将 网页的源码复制下载之后, 可以使用此类进行解析
        self.user_agent_data 是 读取 文件的,

        调用方式 User_Agent().random()
    """

    def __init__(self, json_file="user_agent.json"):
        """
        :param json_file: 下载后内容保存的文件
        """
        self.json_file = json_file
        self.ua_data = self.user_agent_data().get("browsers")
        self.b = ['chrome', 'opera', 'firefox', 'safari', 'internetexplorer']
        # -------
        self.chrome = lambda: random.choice(self.ua_data.get("chrome"))
        self.opera = lambda: random.choice(self.ua_data.get("opera"))
        self.firefox = lambda: random.choice(self.ua_data.get("firefox"))
        self.safari = lambda: random.choice(self.ua_data.get("safari"))
        self.ie = lambda: random.choice(self.ua_data.get("internetexplorer"))
        self.random = lambda: random.choice(self.ua_data.get(random.choice(self.b)))

    def user_agent_data(self):
        data = {
            "browsers": {
                "chrome": [
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.17 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 (KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14"
                ],
                "opera": [
                    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
                    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
                    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
                    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
                    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
                    "Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
                    "Opera/12.0(Windows NT 5.1;U;en)Presto/22.9.168 Version/12.00",
                    "Mozilla/5.0 (Windows NT 5.1) Gecko/20100101 Firefox/14.0 Opera/12.0",
                    "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
                    "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
                    "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
                    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/5.0 Opera 11.11",
                    "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.8.99 Version/11.10",
                    "Opera/9.80 (Windows NT 5.1; U; zh-tw) Presto/2.8.131 Version/11.10",
                    "Opera/9.80 (Windows NT 6.1; Opera Tablet/15165; U; en) Presto/2.8.149 Version/11.1",
                    "Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 6.1; U; en-US) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 6.1; U; cs) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 5.1; U;) Presto/2.7.62 Version/11.01",
                    "Opera/9.80 (Windows NT 5.1; U; cs) Presto/2.7.62 Version/11.01",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.13) Gecko/20101213 Opera/9.80 (Windows NT 6.1; U; zh-tw) Presto/2.7.62 Version/11.01",
                    "Mozilla/5.0 (Windows NT 6.1; U; nl; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
                    "Mozilla/5.0 (Windows NT 6.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.01",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; de) Opera 11.01",
                    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.6.37 Version/11.00",
                    "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
                    "Opera/9.80 (Windows NT 6.1; U; ko) Presto/2.7.62 Version/11.00",
                    "Opera/9.80 (Windows NT 6.1; U; fi) Presto/2.7.62 Version/11.00",
                    "Opera/9.80 (Windows NT 6.1; U; en-GB) Presto/2.7.62 Version/11.00",
                    "Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00",
                    "Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00"
                ],
                "firefox": [
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
                    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
                    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3",
                    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0",
                    "Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0",
                    "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0",
                    "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20130405 Firefox/22.0",
                    "Mozilla/5.0 (Microsoft Windows NT 6.2.9200.0); rv:22.0) Gecko/20130405 Firefox/22.0",
                    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
                    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1",
                    "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:21.0.0) Gecko/20121011 Firefox/21.0.0",
                    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20130514 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.2; rv:21.0) Gecko/20130326 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130401 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130331 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20130330 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130401 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20130328 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130401 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20130331 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 5.1; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 5.0; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "Mozilla/5.0 (Windows NT 6.2; Win64; x64;) Gecko/20100101 Firefox/20.0",
                    "Mozilla/5.0 (Windows x86; rv:19.0) Gecko/20100101 Firefox/19.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:6.0) Gecko/20100101 Firefox/19.0",
                    "Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/18.0.1",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0)  Gecko/20100101 Firefox/18.0"
                ],
                "internetexplorer": [
                    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
                    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0;  rv:11.0) like Gecko",
                    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 7.0; InfoPath.3; .NET CLR 3.1.40767; Trident/6.0; en-IN)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
                    "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
                    "Mozilla/4.0 (Compatible; MSIE 8.0; Windows NT 5.2; Trident/6.0)",
                    "Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
                    "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
                    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
                    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; Media Center PC 6.0; InfoPath.3; MS-RTC LM 8; Zune 4.7",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; InfoPath.3; MS-RTC LM 8; .NET4.0C; .NET4.0E)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; chromeframe/12.0.742.112)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 4.0; Tablet PC 2.0; InfoPath.3; .NET4.0C; .NET4.0E)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; yie8)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET CLR 1.1.4322; .NET4.0C; Tablet PC 2.0)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; FunWebProducts)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/13.0.782.215)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; chromeframe/11.0.696.57)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.1; SV1; .NET CLR 2.8.52393; WOW64; en-US)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; chromeframe/11.0.696.57)",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/4.0; GTB7.4; InfoPath.3; SV1; .NET CLR 3.1.76908; WOW64; en-US)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.8.36217; WOW64; en-US)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; .NET CLR 2.7.58687; SLCC2; Media Center PC 5.0; Zune 3.4; Tablet PC 3.6; InfoPath.3)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; Media Center PC 4.0; SLCC1; .NET CLR 3.0.04320)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 1.1.4322)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; SLCC1; .NET CLR 1.1.4322)",
                    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.0; Trident/4.0; InfoPath.1; SV1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 3.0.04506.30)",
                    "Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.0; Trident/4.0; FBSMTWB; .NET CLR 2.0.34861; .NET CLR 3.0.3746.3218; .NET CLR 3.5.33652; msn OptimizedIE8;ENUS)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; Media Center PC 6.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.3; .NET4.0C; .NET4.0E; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MS-RTC LM 8)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)",
                    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Zune 3.0)"
                ],
                "safari": [
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; fr-FR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; sv-SE) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; hu-HU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ja-JP) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; it-IT) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-HK) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; tr-TR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; nb-NO) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 6.0; fr-FR) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-TW) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
                    "Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5"
                ]
            },
            "spiders": {
                "360Spider": [
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider",
                    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0); 360Spider",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.2.2661.102 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.2.2661.102 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.4.2661.102 Safari/537.36; 360Spider",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.4.2661.102 Safari/537.36; 360Spider"
                ],
                "BaiduSpider": [
                    "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
                    "mozilla/5.0 (compatible; baiduspider/2.0; http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html",
                    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html）",
                    "Mozilla/5.0 (compatible;Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible;Baiduspider/2.0;+http://www.baidu.com/search/spider.html)",
                    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
                ],
                "SogouSpider": [
                    "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)"
                ]
            },
            "randomize": {
                "344": "chrome",
                "819": "firefox",
                "346": "chrome",
                "347": "chrome",
                "340": "chrome",
                "341": "chrome",
                "342": "chrome",
                "343": "chrome",
                "810": "internetexplorer",
                "811": "internetexplorer",
                "812": "internetexplorer",
                "813": "firefox",
                "348": "chrome",
                "349": "chrome",
                "816": "firefox",
                "817": "firefox",
                "737": "chrome",
                "719": "chrome",
                "718": "chrome",
                "717": "chrome",
                "716": "chrome",
                "715": "chrome",
                "714": "chrome",
                "713": "chrome",
                "712": "chrome",
                "711": "chrome",
                "710": "chrome",
                "421": "chrome",
                "129": "chrome",
                "420": "chrome",
                "423": "chrome",
                "422": "chrome",
                "425": "chrome",
                "619": "chrome",
                "424": "chrome",
                "427": "chrome",
                "298": "chrome",
                "299": "chrome",
                "296": "chrome",
                "297": "chrome",
                "294": "chrome",
                "295": "chrome",
                "292": "chrome",
                "293": "chrome",
                "290": "chrome",
                "291": "chrome",
                "591": "chrome",
                "590": "chrome",
                "593": "chrome",
                "592": "chrome",
                "595": "chrome",
                "594": "chrome",
                "597": "chrome",
                "596": "chrome",
                "195": "chrome",
                "194": "chrome",
                "197": "chrome",
                "196": "chrome",
                "191": "chrome",
                "190": "chrome",
                "193": "chrome",
                "192": "chrome",
                "270": "chrome",
                "271": "chrome",
                "272": "chrome",
                "273": "chrome",
                "274": "chrome",
                "275": "chrome",
                "276": "chrome",
                "277": "chrome",
                "278": "chrome",
                "279": "chrome",
                "569": "chrome",
                "497": "chrome",
                "524": "chrome",
                "525": "chrome",
                "526": "chrome",
                "527": "chrome",
                "520": "chrome",
                "521": "chrome",
                "522": "chrome",
                "523": "chrome",
                "528": "chrome",
                "529": "chrome",
                "449": "chrome",
                "448": "chrome",
                "345": "chrome",
                "443": "chrome",
                "442": "chrome",
                "441": "chrome",
                "440": "chrome",
                "447": "chrome",
                "446": "chrome",
                "445": "chrome",
                "444": "chrome",
                "47": "chrome",
                "108": "chrome",
                "109": "chrome",
                "102": "chrome",
                "103": "chrome",
                "100": "chrome",
                "101": "chrome",
                "106": "chrome",
                "107": "chrome",
                "104": "chrome",
                "105": "chrome",
                "902": "firefox",
                "903": "firefox",
                "39": "chrome",
                "38": "chrome",
                "906": "firefox",
                "907": "firefox",
                "904": "firefox",
                "905": "firefox",
                "33": "chrome",
                "32": "chrome",
                "31": "chrome",
                "30": "chrome",
                "37": "chrome",
                "36": "chrome",
                "35": "chrome",
                "34": "chrome",
                "641": "chrome",
                "640": "chrome",
                "643": "chrome",
                "642": "chrome",
                "645": "chrome",
                "644": "chrome",
                "438": "chrome",
                "439": "chrome",
                "436": "chrome",
                "437": "chrome",
                "434": "chrome",
                "435": "chrome",
                "432": "chrome",
                "433": "chrome",
                "430": "chrome",
                "431": "chrome",
                "826": "firefox",
                "339": "chrome",
                "338": "chrome",
                "335": "chrome",
                "334": "chrome",
                "337": "chrome",
                "336": "chrome",
                "331": "chrome",
                "330": "chrome",
                "333": "chrome",
                "332": "chrome",
                "559": "chrome",
                "745": "chrome",
                "854": "firefox",
                "818": "firefox",
                "856": "firefox",
                "857": "firefox",
                "850": "firefox",
                "851": "firefox",
                "852": "firefox",
                "0": "chrome",
                "858": "firefox",
                "859": "firefox",
                "748": "chrome",
                "6": "chrome",
                "43": "chrome",
                "99": "chrome",
                "98": "chrome",
                "91": "chrome",
                "90": "chrome",
                "93": "chrome",
                "92": "chrome",
                "95": "chrome",
                "94": "chrome",
                "97": "chrome",
                "96": "chrome",
                "814": "firefox",
                "815": "firefox",
                "153": "chrome",
                "740": "chrome",
                "741": "chrome",
                "742": "chrome",
                "743": "chrome",
                "744": "chrome",
                "558": "chrome",
                "746": "chrome",
                "747": "chrome",
                "555": "chrome",
                "554": "chrome",
                "557": "chrome",
                "556": "chrome",
                "551": "chrome",
                "550": "chrome",
                "553": "chrome",
                "552": "chrome",
                "238": "chrome",
                "239": "chrome",
                "234": "chrome",
                "235": "chrome",
                "236": "chrome",
                "237": "chrome",
                "230": "chrome",
                "231": "chrome",
                "232": "chrome",
                "233": "chrome",
                "1": "chrome",
                "155": "chrome",
                "146": "chrome",
                "147": "chrome",
                "618": "chrome",
                "145": "chrome",
                "142": "chrome",
                "143": "chrome",
                "140": "chrome",
                "141": "chrome",
                "612": "chrome",
                "613": "chrome",
                "610": "chrome",
                "611": "chrome",
                "616": "chrome",
                "617": "chrome",
                "148": "chrome",
                "149": "chrome",
                "46": "chrome",
                "154": "chrome",
                "948": "safari",
                "949": "safari",
                "946": "safari",
                "947": "safari",
                "944": "safari",
                "945": "safari",
                "942": "safari",
                "943": "safari",
                "940": "safari",
                "941": "safari",
                "689": "chrome",
                "688": "chrome",
                "685": "chrome",
                "684": "chrome",
                "687": "chrome",
                "686": "chrome",
                "681": "chrome",
                "680": "chrome",
                "683": "chrome",
                "682": "chrome",
                "458": "chrome",
                "459": "chrome",
                "133": "chrome",
                "132": "chrome",
                "131": "chrome",
                "130": "chrome",
                "137": "chrome",
                "136": "chrome",
                "135": "chrome",
                "134": "chrome",
                "494": "chrome",
                "495": "chrome",
                "139": "chrome",
                "138": "chrome",
                "490": "chrome",
                "491": "chrome",
                "492": "chrome",
                "493": "chrome",
                "24": "chrome",
                "25": "chrome",
                "26": "chrome",
                "27": "chrome",
                "20": "chrome",
                "21": "chrome",
                "22": "chrome",
                "23": "chrome",
                "28": "chrome",
                "29": "chrome",
                "820": "firefox",
                "407": "chrome",
                "406": "chrome",
                "405": "chrome",
                "404": "chrome",
                "403": "chrome",
                "402": "chrome",
                "401": "chrome",
                "400": "chrome",
                "933": "firefox",
                "932": "firefox",
                "931": "firefox",
                "930": "firefox",
                "937": "safari",
                "452": "chrome",
                "409": "chrome",
                "408": "chrome",
                "453": "chrome",
                "414": "chrome",
                "183": "chrome",
                "415": "chrome",
                "379": "chrome",
                "378": "chrome",
                "228": "chrome",
                "829": "firefox",
                "828": "firefox",
                "371": "chrome",
                "370": "chrome",
                "373": "chrome",
                "372": "chrome",
                "375": "chrome",
                "374": "chrome",
                "377": "chrome",
                "376": "chrome",
                "708": "chrome",
                "709": "chrome",
                "704": "chrome",
                "705": "chrome",
                "706": "chrome",
                "707": "chrome",
                "700": "chrome",
                "144": "chrome",
                "702": "chrome",
                "703": "chrome",
                "393": "chrome",
                "392": "chrome",
                "88": "chrome",
                "89": "chrome",
                "397": "chrome",
                "396": "chrome",
                "395": "chrome",
                "394": "chrome",
                "82": "chrome",
                "83": "chrome",
                "80": "chrome",
                "81": "chrome",
                "86": "chrome",
                "87": "chrome",
                "84": "chrome",
                "85": "chrome",
                "797": "internetexplorer",
                "796": "internetexplorer",
                "795": "internetexplorer",
                "794": "internetexplorer",
                "793": "internetexplorer",
                "792": "internetexplorer",
                "791": "internetexplorer",
                "790": "internetexplorer",
                "749": "chrome",
                "799": "internetexplorer",
                "798": "internetexplorer",
                "7": "chrome",
                "170": "chrome",
                "586": "chrome",
                "587": "chrome",
                "584": "chrome",
                "585": "chrome",
                "582": "chrome",
                "583": "chrome",
                "580": "chrome",
                "581": "chrome",
                "588": "chrome",
                "589": "chrome",
                "245": "chrome",
                "244": "chrome",
                "247": "chrome",
                "246": "chrome",
                "241": "chrome",
                "614": "chrome",
                "243": "chrome",
                "242": "chrome",
                "615": "chrome",
                "249": "chrome",
                "248": "chrome",
                "418": "chrome",
                "419": "chrome",
                "519": "chrome",
                "518": "chrome",
                "511": "chrome",
                "510": "chrome",
                "513": "chrome",
                "512": "chrome",
                "515": "chrome",
                "514": "chrome",
                "517": "chrome",
                "516": "chrome",
                "623": "chrome",
                "622": "chrome",
                "621": "chrome",
                "620": "chrome",
                "627": "chrome",
                "626": "chrome",
                "625": "chrome",
                "624": "chrome",
                "450": "chrome",
                "451": "chrome",
                "629": "chrome",
                "628": "chrome",
                "454": "chrome",
                "455": "chrome",
                "456": "chrome",
                "457": "chrome",
                "179": "chrome",
                "178": "chrome",
                "177": "chrome",
                "199": "chrome",
                "175": "chrome",
                "174": "chrome",
                "173": "chrome",
                "172": "chrome",
                "171": "chrome",
                "198": "chrome",
                "977": "opera",
                "182": "chrome",
                "975": "opera",
                "974": "opera",
                "973": "opera",
                "972": "opera",
                "971": "opera",
                "970": "opera",
                "180": "chrome",
                "979": "opera",
                "978": "opera",
                "656": "chrome",
                "599": "chrome",
                "654": "chrome",
                "181": "chrome",
                "186": "chrome",
                "187": "chrome",
                "184": "chrome",
                "185": "chrome",
                "652": "chrome",
                "188": "chrome",
                "189": "chrome",
                "658": "chrome",
                "653": "chrome",
                "650": "chrome",
                "651": "chrome",
                "11": "chrome",
                "10": "chrome",
                "13": "chrome",
                "12": "chrome",
                "15": "chrome",
                "14": "chrome",
                "17": "chrome",
                "16": "chrome",
                "19": "chrome",
                "18": "chrome",
                "863": "firefox",
                "862": "firefox",
                "865": "firefox",
                "864": "firefox",
                "867": "firefox",
                "866": "firefox",
                "354": "chrome",
                "659": "chrome",
                "44": "chrome",
                "883": "firefox",
                "882": "firefox",
                "881": "firefox",
                "880": "firefox",
                "887": "firefox",
                "886": "firefox",
                "885": "firefox",
                "884": "firefox",
                "889": "firefox",
                "888": "firefox",
                "116": "chrome",
                "45": "chrome",
                "657": "chrome",
                "355": "chrome",
                "322": "chrome",
                "323": "chrome",
                "320": "chrome",
                "321": "chrome",
                "326": "chrome",
                "327": "chrome",
                "324": "chrome",
                "325": "chrome",
                "328": "chrome",
                "329": "chrome",
                "562": "chrome",
                "201": "chrome",
                "200": "chrome",
                "203": "chrome",
                "202": "chrome",
                "205": "chrome",
                "204": "chrome",
                "207": "chrome",
                "206": "chrome",
                "209": "chrome",
                "208": "chrome",
                "779": "internetexplorer",
                "778": "internetexplorer",
                "77": "chrome",
                "76": "chrome",
                "75": "chrome",
                "74": "chrome",
                "73": "chrome",
                "72": "chrome",
                "71": "chrome",
                "70": "chrome",
                "655": "chrome",
                "567": "chrome",
                "79": "chrome",
                "78": "chrome",
                "359": "chrome",
                "358": "chrome",
                "669": "chrome",
                "668": "chrome",
                "667": "chrome",
                "666": "chrome",
                "665": "chrome",
                "664": "chrome",
                "663": "chrome",
                "662": "chrome",
                "661": "chrome",
                "660": "chrome",
                "215": "chrome",
                "692": "chrome",
                "693": "chrome",
                "690": "chrome",
                "691": "chrome",
                "696": "chrome",
                "697": "chrome",
                "694": "chrome",
                "695": "chrome",
                "698": "chrome",
                "699": "chrome",
                "542": "chrome",
                "543": "chrome",
                "540": "chrome",
                "541": "chrome",
                "546": "chrome",
                "547": "chrome",
                "544": "chrome",
                "545": "chrome",
                "8": "chrome",
                "548": "chrome",
                "549": "chrome",
                "598": "chrome",
                "869": "firefox",
                "868": "firefox",
                "120": "chrome",
                "121": "chrome",
                "122": "chrome",
                "123": "chrome",
                "124": "chrome",
                "125": "chrome",
                "126": "chrome",
                "127": "chrome",
                "128": "chrome",
                "2": "chrome",
                "219": "chrome",
                "176": "chrome",
                "214": "chrome",
                "563": "chrome",
                "928": "firefox",
                "929": "firefox",
                "416": "chrome",
                "417": "chrome",
                "410": "chrome",
                "411": "chrome",
                "412": "chrome",
                "413": "chrome",
                "920": "firefox",
                "498": "chrome",
                "922": "firefox",
                "923": "firefox",
                "924": "firefox",
                "925": "firefox",
                "926": "firefox",
                "927": "firefox",
                "319": "chrome",
                "318": "chrome",
                "313": "chrome",
                "312": "chrome",
                "311": "chrome",
                "310": "chrome",
                "317": "chrome",
                "316": "chrome",
                "315": "chrome",
                "314": "chrome",
                "921": "firefox",
                "496": "chrome",
                "832": "firefox",
                "833": "firefox",
                "830": "firefox",
                "831": "firefox",
                "836": "firefox",
                "837": "firefox",
                "834": "firefox",
                "835": "firefox",
                "838": "firefox",
                "839": "firefox",
                "3": "chrome",
                "368": "chrome",
                "369": "chrome",
                "366": "chrome",
                "367": "chrome",
                "364": "chrome",
                "365": "chrome",
                "362": "chrome",
                "363": "chrome",
                "360": "chrome",
                "361": "chrome",
                "218": "chrome",
                "380": "chrome",
                "861": "firefox",
                "382": "chrome",
                "383": "chrome",
                "384": "chrome",
                "385": "chrome",
                "386": "chrome",
                "387": "chrome",
                "388": "chrome",
                "389": "chrome",
                "784": "internetexplorer",
                "785": "internetexplorer",
                "786": "internetexplorer",
                "787": "internetexplorer",
                "780": "internetexplorer",
                "781": "internetexplorer",
                "782": "internetexplorer",
                "381": "chrome",
                "788": "internetexplorer",
                "789": "internetexplorer",
                "860": "firefox",
                "151": "chrome",
                "579": "chrome",
                "578": "chrome",
                "150": "chrome",
                "573": "chrome",
                "572": "chrome",
                "571": "chrome",
                "570": "chrome",
                "577": "chrome",
                "576": "chrome",
                "575": "chrome",
                "574": "chrome",
                "60": "chrome",
                "61": "chrome",
                "62": "chrome",
                "259": "chrome",
                "64": "chrome",
                "65": "chrome",
                "66": "chrome",
                "67": "chrome",
                "68": "chrome",
                "253": "chrome",
                "250": "chrome",
                "251": "chrome",
                "256": "chrome",
                "257": "chrome",
                "254": "chrome",
                "255": "chrome",
                "499": "chrome",
                "157": "chrome",
                "156": "chrome",
                "939": "safari",
                "731": "chrome",
                "730": "chrome",
                "733": "chrome",
                "938": "safari",
                "735": "chrome",
                "734": "chrome",
                "508": "chrome",
                "736": "chrome",
                "506": "chrome",
                "738": "chrome",
                "504": "chrome",
                "505": "chrome",
                "502": "chrome",
                "503": "chrome",
                "500": "chrome",
                "501": "chrome",
                "630": "chrome",
                "631": "chrome",
                "632": "chrome",
                "633": "chrome",
                "469": "chrome",
                "468": "chrome",
                "636": "chrome",
                "637": "chrome",
                "465": "chrome",
                "464": "chrome",
                "467": "chrome",
                "466": "chrome",
                "461": "chrome",
                "900": "firefox",
                "463": "chrome",
                "462": "chrome",
                "901": "firefox",
                "168": "chrome",
                "169": "chrome",
                "164": "chrome",
                "165": "chrome",
                "166": "chrome",
                "167": "chrome",
                "160": "chrome",
                "161": "chrome",
                "162": "chrome",
                "163": "chrome",
                "964": "safari",
                "965": "safari",
                "966": "safari",
                "967": "safari",
                "960": "safari",
                "961": "safari",
                "962": "safari",
                "963": "safari",
                "783": "internetexplorer",
                "968": "safari",
                "969": "opera",
                "936": "firefox",
                "935": "firefox",
                "934": "firefox",
                "908": "firefox",
                "909": "firefox",
                "722": "chrome",
                "426": "chrome",
                "878": "firefox",
                "879": "firefox",
                "876": "firefox",
                "877": "firefox",
                "874": "firefox",
                "875": "firefox",
                "872": "firefox",
                "873": "firefox",
                "870": "firefox",
                "871": "firefox",
                "9": "chrome",
                "890": "firefox",
                "891": "firefox",
                "892": "firefox",
                "893": "firefox",
                "894": "firefox",
                "647": "chrome",
                "896": "firefox",
                "897": "firefox",
                "898": "firefox",
                "899": "firefox",
                "646": "chrome",
                "649": "chrome",
                "648": "chrome",
                "357": "chrome",
                "356": "chrome",
                "809": "internetexplorer",
                "808": "internetexplorer",
                "353": "chrome",
                "352": "chrome",
                "351": "chrome",
                "350": "chrome",
                "803": "internetexplorer",
                "802": "internetexplorer",
                "801": "internetexplorer",
                "800": "internetexplorer",
                "807": "internetexplorer",
                "806": "internetexplorer",
                "805": "internetexplorer",
                "804": "internetexplorer",
                "216": "chrome",
                "217": "chrome",
                "768": "chrome",
                "769": "chrome",
                "212": "chrome",
                "213": "chrome",
                "210": "chrome",
                "211": "chrome",
                "762": "chrome",
                "763": "chrome",
                "760": "chrome",
                "761": "chrome",
                "766": "chrome",
                "767": "chrome",
                "764": "chrome",
                "765": "chrome",
                "40": "chrome",
                "41": "chrome",
                "289": "chrome",
                "288": "chrome",
                "4": "chrome",
                "281": "chrome",
                "280": "chrome",
                "283": "chrome",
                "282": "chrome",
                "285": "chrome",
                "284": "chrome",
                "287": "chrome",
                "286": "chrome",
                "678": "chrome",
                "679": "chrome",
                "674": "chrome",
                "675": "chrome",
                "676": "chrome",
                "677": "chrome",
                "670": "chrome",
                "671": "chrome",
                "672": "chrome",
                "673": "chrome",
                "263": "chrome",
                "262": "chrome",
                "261": "chrome",
                "260": "chrome",
                "267": "chrome",
                "266": "chrome",
                "265": "chrome",
                "264": "chrome",
                "269": "chrome",
                "268": "chrome",
                "59": "chrome",
                "58": "chrome",
                "55": "chrome",
                "54": "chrome",
                "57": "chrome",
                "56": "chrome",
                "51": "chrome",
                "258": "chrome",
                "53": "chrome",
                "52": "chrome",
                "537": "chrome",
                "536": "chrome",
                "535": "chrome",
                "63": "chrome",
                "533": "chrome",
                "532": "chrome",
                "531": "chrome",
                "530": "chrome",
                "152": "chrome",
                "539": "chrome",
                "538": "chrome",
                "775": "internetexplorer",
                "774": "internetexplorer",
                "982": "opera",
                "983": "opera",
                "980": "opera",
                "981": "opera",
                "777": "internetexplorer",
                "984": "opera",
                "50": "chrome",
                "115": "chrome",
                "252": "chrome",
                "117": "chrome",
                "776": "internetexplorer",
                "111": "chrome",
                "110": "chrome",
                "113": "chrome",
                "69": "chrome",
                "771": "chrome",
                "119": "chrome",
                "118": "chrome",
                "770": "chrome",
                "773": "internetexplorer",
                "772": "internetexplorer",
                "429": "chrome",
                "428": "chrome",
                "534": "chrome",
                "919": "firefox",
                "918": "firefox",
                "915": "firefox",
                "914": "firefox",
                "917": "firefox",
                "916": "firefox",
                "911": "firefox",
                "910": "firefox",
                "913": "firefox",
                "912": "firefox",
                "308": "chrome",
                "309": "chrome",
                "855": "firefox",
                "300": "chrome",
                "301": "chrome",
                "302": "chrome",
                "303": "chrome",
                "304": "chrome",
                "305": "chrome",
                "306": "chrome",
                "307": "chrome",
                "895": "firefox",
                "825": "firefox",
                "824": "firefox",
                "827": "firefox",
                "847": "firefox",
                "846": "firefox",
                "845": "firefox",
                "844": "firefox",
                "843": "firefox",
                "842": "firefox",
                "841": "firefox",
                "840": "firefox",
                "821": "firefox",
                "853": "firefox",
                "849": "firefox",
                "848": "firefox",
                "823": "firefox",
                "822": "firefox",
                "240": "chrome",
                "390": "chrome",
                "732": "chrome",
                "753": "chrome",
                "752": "chrome",
                "751": "chrome",
                "750": "chrome",
                "757": "chrome",
                "756": "chrome",
                "755": "chrome",
                "754": "chrome",
                "560": "chrome",
                "561": "chrome",
                "759": "chrome",
                "758": "chrome",
                "564": "chrome",
                "565": "chrome",
                "566": "chrome",
                "701": "chrome",
                "739": "chrome",
                "229": "chrome",
                "507": "chrome",
                "227": "chrome",
                "226": "chrome",
                "225": "chrome",
                "224": "chrome",
                "223": "chrome",
                "222": "chrome",
                "221": "chrome",
                "220": "chrome",
                "114": "chrome",
                "391": "chrome",
                "726": "chrome",
                "727": "chrome",
                "724": "chrome",
                "725": "chrome",
                "568": "chrome",
                "723": "chrome",
                "720": "chrome",
                "721": "chrome",
                "728": "chrome",
                "729": "chrome",
                "605": "chrome",
                "604": "chrome",
                "607": "chrome",
                "606": "chrome",
                "601": "chrome",
                "600": "chrome",
                "603": "chrome",
                "602": "chrome",
                "159": "chrome",
                "158": "chrome",
                "112": "chrome",
                "609": "chrome",
                "608": "chrome",
                "976": "opera",
                "634": "chrome",
                "399": "chrome",
                "635": "chrome",
                "959": "safari",
                "958": "safari",
                "398": "chrome",
                "48": "chrome",
                "49": "chrome",
                "951": "safari",
                "950": "safari",
                "953": "safari",
                "952": "safari",
                "42": "chrome",
                "954": "safari",
                "957": "safari",
                "956": "safari",
                "638": "chrome",
                "5": "chrome",
                "639": "chrome",
                "460": "chrome",
                "489": "chrome",
                "488": "chrome",
                "487": "chrome",
                "486": "chrome",
                "485": "chrome",
                "484": "chrome",
                "483": "chrome",
                "482": "chrome",
                "481": "chrome",
                "480": "chrome",
                "509": "chrome",
                "955": "safari",
                "472": "chrome",
                "473": "chrome",
                "470": "chrome",
                "471": "chrome",
                "476": "chrome",
                "477": "chrome",
                "474": "chrome",
                "475": "chrome",
                "478": "chrome",
                "479": "chrome"
            }
        }
        return data

user_agent = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
    "User-Agent:Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "User-Agent:Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
]

# 谷歌翻译
class google_trans(object):
    def __init__(self, content):
        self.content = content
        ua = User_Agent()
        user_agent = ua.random()
        self.ip_port = get_ip()
        self.headers = {
            'User-Agent': user_agent,
        }

    def json_get(self, json_text):
        try:
            json_ = json.loads(json_text)
            text_zon = ""
            for js in json_[0]:
                if js[0]:
                    text_zon += js[0]
        except:
            return ''
        return text_zon

    def conect_html(self, url):
        try:
            response = requests.get(url, headers=self.headers, proxies=self.ip_port, timeout=60)
        except:
            time.sleep(2)
            self.ip_port = get_ip()
            restext = self.conect_html(url)
            return restext
        return response.text

    def trans(self):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q=" + quote(
            self.content)
        json_text = self.conect_html(url)
        text_af = self.json_get(json_text)
        if not text_af:
            return text_af
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=" + quote(text_af)
        json_text = self.conect_html(url)
        text_af = self.json_get(json_text)
        return text_af

Redispool = redis.ConnectionPool(host=HOST, port=RedisPORT, db=0, max_connections=32)
Redisconn = redis.Redis(connection_pool=Redispool)

def SQLupdateDate(id, args, webid=1,url=''):
    conn = pymysql.connect(SQLhost, SQLuser, SQLpwd, SQLdbname,port=SQLPORT)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    try:
        if not args:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            try:
                if 'l' in str(id):
                    ids = int(id[:-1])
                    sql = "update admin_lexiconzhinengurl set `date`='{}',`isActivate`=1,url='{}',siteweb={} where id={}" .format(date,url,webid, ids)
                else:
                    sql = "update admin_mainurlzhineng set `date`='{}',`isActivate`=1,url='{}' where id={}".format(date,url,id)
                cursor.execute(sql)
                sql = 'UPDATE admin_webnumber set numb= numb + 1 where id="%d"' % webid
                cursor.execute(sql)  # 执行
                conn.commit()
            except:
                # 保存成功发布网站失败,
                RedisWebSiteOK(id,webid,url)
        else:
            sql = """INSERT INTO `admin_errmainurl` (`TITLE`,`URL`,`WEB_ID`,`IDS`,`describe`) VALUES (%s,%s,%s,%s,%s)"""
            cursor.executemany(sql, [args])
            conn.commit()
    except Exception as e:
        pass
        print('智能采集','修改数据库 url 失败：{}，ID：{} webid:{} arges:{}'.format(e,id,webid,args))
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接

def SQLselect_webname():
    conn = pymysql.connect(SQLhost, SQLuser, SQLpwd, SQLdbname,port=SQLPORT)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    result = False
    try:
        sql = "select `name` from admin_webnumber"
        cursor.execute(sql)  # 执行
        result = cursor.fetchall()  # result是元
    except:
        print('SQLselect_webname 发生错误')
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
    return result

def SQLselect_global():
    conn = pymysql.connect(SQLhost, SQLuser, SQLpwd, SQLdbname, port=SQLPORT)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    result = False
    try:
        sql = "select title,parameter,isActivate from admin_globaldata"
        cursor.execute(sql)  # 执行
        result = cursor.fetchall()  # result是元
    except:
        print('SQLselect_global 发生错误')
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
    return result

def SQLxpath():
    xpath_l = {}
    conn = pymysql.connect(SQLhost, SQLuser, SQLpwd, SQLdbname,port=SQLPORT)  # 连接数据库
    cursor = conn.cursor()  # 获取游标
    try:
        # 查询网站数量
        sql = "select webdoma,xpath from admin_contentxpath"
        cursor.execute(sql)  # 执行
        result = cursor.fetchall()  # result是元
        for webdoma, xpath in result:
            xpath_l[webdoma] = xpath
    except Exception:
        print('智能采集','查询 采集路径错误 ')
    finally:
        cursor.close()  # 关闭游标
        conn.close()  # 关闭连接
    return xpath_l

def RedisWebSiteOK(id,webid,url):
    '''(是否是词库,
        是否是智能采集
        采集源id
        采集的网站id
        被采集源 url
        )'''
    if 'l' in str(id):
        id = int(id[:-1])
        Redisconn.rpush('have_published',(True,True,id,webid,url))
    else:
        Redisconn.rpush('have_published', (True, True, id, webid,url))

def Rediswebname():
    webnames = SQLselect_webname()
    webname_list = []
    if webnames:
        for webname in webnames:
            webname_list.append(webname[0])
        return webname_list

def Redisselect(webname_list):
    all_list = {}
    for webname in webname_list:
        # if webname != 'www.qiongren.org琼人资讯':
        #     continue
        if Redisconn.llen('zawait:' + str(webname)):
            all = []
            for item in range(1):
                try:
                    info = eval(Redisconn.lpop('zawait:' + str(webname)))
                except:
                    continue
                if Redisde_weight(webname, info[8]):  # 查询此网站是否
                    continue
                all.append(info)
            all_list[webname] = all
    return all_list

def Redisde_weight(webname, url):
    # print('智能采集','查询 redis 已发布成功的数据: webname:{}, url:{}'.format(webname, url))
    key = get_md5(url)
    value = Redisconn.hget(name='zissue:' + str(webname), key=key)
    return value

def Redisset_hash(webname, url):
        # print('智能采集','插入 redis 已发布成功的数据: webname:{}, url:{}'.format(webname,url))
        Redisconn.hset(name='zissue:' + str(webname), key=get_md5(url), value=1)


# 下载保存图片
class Down_Compressimg(object):
    def get_size(self, file):
        # 获取文件大小:KB
        size = os.path.getsize(file)
        return size / 1024

    def get_outfile(self, infile, outfile):
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self, infile, quality=5):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        # o_size = get_size(infile)
        # if o_size <= mb:
        #     return infile
        # outfile = get_outfile(infile, outfile)
        # while o_size > mb:
        #     im = Image.open(infile)
        #     im.save(outfile, quality=quality)
        #     if quality - step < 0:
        #         break
        #     quality -= step
        #     o_size = get_size(outfile)
        # return outfile, get_size(outfile)
        im = Image.open(infile)
        im.save(infile, quality=quality)

    def resize_image(self, infile, outfile='', x_s=1376):
        """修改图片尺寸
        :param infile: 图片源文件
        :param outfile: 重设尺寸文件保存地址
        :param x_s: 设置的宽度
        :return:
        """
        im = Image.open(infile)
        x, y = im.size
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        outfile = self.get_outfile(infile, outfile)
        out.save(outfile)

    def getPage(self, keyword, page=2):
        keyword = up.quote(keyword, safe='/')
        url_begin = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='
        url = url_begin + keyword + '&pn=' + str(page) + '&gsm=' + str(
            hex(page)) + '&ct=&ic=0&lm=-1&width=0&height=0&z=1'
        return url

    def get_onepage_urls(self, onepageurl):
        try:
            html = requests.get(onepageurl, headers={'User-Agent': User_Agent().random()}, proxies=get_ip()).text
        except Exception as e:
            print('智能采集',e)
            pic_url = []
            return pic_url
        pic_url = re.findall('"objURL":"(.*?)"', html, re.S)
        return pic_url

    def down_pic(self, pic_urls, title, quality=80):
        Flag = False
        for i, pic_url, in enumerate(pic_urls):
            try:
                pic = requests.get(pic_url, headers={'User-Agent': random.choice(user_agent)}, timeout=15, proxies=get_ip())
                string = 'files/' + str(int(time.time())) + "_" + str(random.randint(1000, 9999)) + '.png'
                with open(string, 'wb') as f:
                    f.write(pic.content)
                    print('智能采集','成功下载图片%s' % pic_url, get_nowtime())
                    Flag = True
                if Flag:
                    time.sleep(1)
                    # try:
                    #     im = Image.open(string)
                    #     im.save(string, quality=quality)
                    # except:
                    #     continue
                    return string
                else:
                    continue
            except Exception as e:
                print('智能采集','下载图片出错,%s' % str(pic_url), get_nowtime())
                print('智能采集',e)
                continue

    def run(self, keyword):
        url = self.getPage(keyword)
        ongpage_urls = self.get_onepage_urls(url)
        file_path_img = self.down_pic(set(ongpage_urls), keyword)
        if file_path_img:
            writefile = int(time.time() * 1000)
            with open(file_path_img, "a") as f:
                f.write(str(writefile))
            time.sleep(2)
            return file_path_img
        return False


# 获取当前时间
def get_nowtime():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    return nowTime


# 获取IP
def get_ip():
    try:
        ips = requests.get("http://kuyukuyu.com/agents/get?uuid=d5a51445-b1bc-4ecb-81df-db794d704cbb").text
    except:
        time.sleep(0.5)
        ips = get_ip()
    return {
        'http': 'http://' + ips,
        'https': 'https://' + ips
    }


# 统计 汉字个数
def str_count(str):
    '''找出字符串中的中文个数'''
    count_zh = 0
    for s in str:
        # 中文
        if s.isalpha():
            count_zh += 1
    return count_zh


# 将中文符号转换成中文服务号
def E_trans_to_C(string):
    E_pun = u',.!?[]()<>""\'\'＃'
    C_pun = u'，。！？【】（）《》“”‘’#'
    table = {ord(f): ord(t) for f, t in zip(E_pun, C_pun)}
    return string.translate(table)


# 加密
def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    m = md5()
    m.update(text)
    return m.hexdigest()

    # 句子切割


def cut_sent(para):
    para = para.replace('。','。\n')
    para = para.replace('，','，\n')
    zon = para.split("\n")
    return zon


# 创建并写入txt内容
def create_str_to_txt(str_data):
    path_file_name = '信息存贮/{}.txt'.format("upload_log")
    if not os.path.exists(path_file_name):
        with open(path_file_name, "w") as f:
            pass
    with open(path_file_name, "a") as f:
        try:
            f.write(str_data)
        except Exception:
            # 处理中文编码问题
            doc = str_data.encode("GBK", 'ignore').decode("GBK", 'ignore')
            f.write(doc + "\n")


# 去除文章中 某些 标签
def content_delet_(content):
    # 将 </p> 替换成 \n
    content = content.replace('</p>','\n#')
    for key in key_delet:
        content = re.sub(key,'',content,flags=re.S)
    return content



# 文章添加 图片
def content_update_img(content, img_src):
    content = '<img src="{}" >'.format(img_src) + content
    return content


minNumberWords = 0
minNumberWordsisActivate = False  # 检查文章最少字数 默认关闭
key_url_query = Queue()  # url 队列
content_query = Queue()  # 网站抓取的文章 队列
formattedText_query = Queue()  # 文章整合队列
push_query = Queue()  # 谷歌翻译后的待发布的 文章队列
xpathcont = SQLxpath()
webNameListRedis = Rediswebname()
dedecms_session_ID = {}  # dedecms 的session值



# 获取随机时间
def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)


def randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return strTimeProp(start, end, random.random(), frmt)

# 获取织梦session_id。
def get_phpid(background_link, user_name, password):
    try:
        background_link += '/index.php'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('disable-infobars')
        options.add_argument('--disable-gpu')
        browser = webdriver.Chrome(chrome_options=options)
        browser.get(background_link)
        wait = WebDriverWait(browser, 20)
        wait.until(EC.presence_of_element_located((By.NAME, 'sm1')))
        user_input = browser.find_element_by_name("userid")
        user_input.send_keys(user_name)
        password_input = browser.find_element_by_name("pwd")
        password_input.send_keys(password)
        browser.find_element_by_name("sm1").click()
        code = browser.page_source
        if "成功登录" in code:
            yun_times = time.strftime("%Y-%m-%d", time.localtime())
            text = "[{}]：网站：{}，已经登录成功！\n".format(yun_times, background_link)
            # create_str_to_txt(text)
            print('智能采集',"域名：%s，已经登录成功！" % (background_link))
            cookies = browser.get_cookies()
            for cookie in cookies:
                if cookie["name"] == "PHPSESSID":
                    return cookie['value']
            browser.quit()
        else:
            browser.quit()
            yun_times = time.strftime("%Y-%m-%d", time.localtime())
            text = "[{}]：网站：{}，登录失败,请检查网站后台链接和账号密码是否正确？\n".format(yun_times, background_link)
            # create_str_to_txt(text)
            print('智能采集',"域名：%s，登录失败,请检查网站后台链接和账号密码是否正确？" % (background_link))
            return False
    except BaseException:
        yun_times = time.strftime("%Y-%m-%d", time.localtime())
        text = "[{}]：网站：{}，登录失败,请检查网站网络是否出现问题。\n".format(yun_times, background_link)
        # create_str_to_txt(text)
        print('智能采集',"域名：%s，登录失败,请检查网站后台链接和账号密码是否正确？" % (background_link))
        return False


# 织梦图片上传
def dedecms_upload_img(url, filename, phpid):
    af = url.split("/")
    url = "/".join(af[0:-1]) + "/include/dialog/select_images_post.php"
    phpid = phpid
    php_id = "PHPSESSID=%s;" % (phpid)
    querystring = {"CKEditor": "body", "CKEditorFuncNum": "2", "langCode": "zh-cn"}
    img_name = filename.split('/')[-1]
    print('智能采集','图片名称', img_name)
    # img_name = '1581827532_8539.png'
    # filename = "files/" + img_name
    # filename = .img_out(img_path1)  # 图片路径
    headers = {
        'Cookie': php_id,
    }
    payload = {
        "upload": (img_name, open(filename, 'rb'), "image/png")
    }
    m = MultipartEncoder(payload)
    headers['Content-Type'] = m.content_type
    response = requests.request("POST", url, data=m, headers=headers, params=querystring)
    response_text = response.text
    link = response_text.split(",")
    img_link = link[1][2:-1]
    return img_link


#  zblog  上传图片
def zblog_upload_img(url, img_path):
    querystring = {"CKEditor": "body", "CKEditorFuncNum": "2", "langCode": "zh-cn"}
    img_name = img_path.split('\\')[-1]
    img_name = str(time.time()) + "_" + str(random.randint(1000, 9999)) + str(img_name)
    payload = {
        "upload": (img_name, open(img_path, 'rb'), "image/png")
    }
    m = MultipartEncoder(payload)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
    }
    headers['Content-Type'] = m.content_type
    response = requests.request("POST", url, data=m, headers=headers, params=querystring)
    response_text = response.text
    if response_text == 'error':
        print('智能采集',response_text)
        print('智能采集','上传文件失败', get_nowtime())
    # else:
    # if (os.path.exists(img_path)):
    #     os.remove(img_path)
    #     print('智能采集','文件上传成功，已删除本地文件：%s' % (img_name))
    img_link = response_text
    return img_link

# 文章关键词挖掘
def text_to_keywords(text):
    keywords = jieba.analyse.extract_tags(text, topK=5, withWeight=False)
    keywords_length = []
    for keyword in keywords:
        length = len(keyword)
        utf8_length = len(keyword.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        keywords_length.append([int(length), 0])
    # keywords_str = []
    keywords_str = ''
    for list_num in range(len(keywords_length)):
        if keywords_length[list_num][1] == 0:
            keywords_length[list_num][1] = 1
            for list_num2 in range(len(keywords_length)):
                if keywords_length[list_num2][1] == 0:
                    sum_len = keywords_length[list_num2][1] + keywords_length[list_num][1]
                    if sum_len == 5:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        # keywords_str.append(str_keyword)
                        keywords_str += str_keyword + ','
                        break
                    elif sum_len < 6:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        # keywords_str.append(str_keyword)
                        keywords_str += str_keyword + ','
                        break
    return keywords_str

# 获取 redis 中的链接
def run():
    ''''''
    try:
        key_url_list = Redisselect(webNameListRedis)
        time.sleep(0.5)
        if key_url_list:
            for redis_name in key_url_list:
                for webid, img_isActivate, column, author, weblink, describe, isActivateTime, id, title, isActivate, ratioimg, cms, selecttitle in \
                        key_url_list[redis_name]:
                    crawlers(
                        [webid, img_isActivate, column, author, weblink, describe, id, title, redis_name,
                         isActivateTime, ratioimg, cms, selecttitle])
        else:
            print('智能采集','reids中没有 url链接', get_nowtime())
    except:
        pass


def crawlers(data):
    CollectingSource = [
    'https://www.baidu.com/s?wd=site%3Awww.sohu.com%20{}&pn={}',  # 搜狐站内搜索
    'https://www.baidu.com/s?wd=site%3Ajianshu.com%20{}&pn={}',  # 简书站内搜索
    'https://www.baidu.com/s?wd=site%3Abaijiahao.baidu.com%20{}&pn={}',  # 百家号
    'https://www.baidu.com/s?wd=site%3Ady.163.com%20{}&pn={}',  # 网易订阅
    # 'https://www.baidu.com/s?wd=site%3Ablog.sina.com.cn%20{}&pn={}',  # 新浪博客
    ]
    print('智能采集','爬虫函数', data, get_nowtime())
    related_title_list = []  # 存放百度相关标题 的列表
    keys = quote(data[7])
    urls = random.choice(CollectingSource)
    url = urls.format(keys,random.randint(1,3)*10)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'BIDUPSID=637278E20EE0D41462F4A952DD16C982; PSTM=1574332013; BAIDUID=83182CB7920E242C6FAD6A41EFA9DE64:FG=1; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_WISE_SIDS=138595_141762_135846_141002_140853_141707_140141_133995_138878_137979_141200_140174_131247_137746_138165_107320_138883_140259_141753_140202_138585_141650_138252_140113_141742_141659_140579_133847_140792_141807_131424_140312_140972_136537_110085_140987_141942_127969_140594_140864_139887_138425_139557_141191; MSA_WH=1473_841; MCITY=-%3A; BDUSS=lEQnRadlVaeE5qeUJmTUx0cnM0RlJlVUhFYi1acDAwUzdCWUthNTA5Vk1EMnBlRVFBQUFBJCQAAAAAAAAAAAEAAACnXWY60uDQ-V9fXwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEyCQl5MgkJeTD; H_PS_PSSID=30748_1427_21092_30823_26350; BD_HOME=1; delPer=0; BD_CK_SAM=1; PSINO=6; COOKIE_SESSION=793_0_3_3_8_1_0_0_3_1_0_0_10604_0_5_0_1582214942_0_1582214937%7C9%2397193_3_1581752559%7C2; sugstore=1; H_PS_645EC=d419%2BW7DSt07p2m8Z8b1Kr8kJSgrDcJUvvNHnJYqvBwCmRDsZ8qVRw5DBCc',
        'Host': 'www.baidu.com',
        'Pragma': 'no-cache',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(user_agent),
    }
    try:
        htmlres = requests.get(url,
                         headers=headers,
                         proxies=get_ip(), timeout=60).text
    except requests.exceptions.ProxyError:
        print('1932 请求超时')
        return
    urlpage = re.findall(r"""data-tools='\{"title":"(.*?)","url":"(.*?)"\}'>""", htmlres, re.S)
    if not urlpage:
        print('1932 urlpage 未获取到数据,',url)
        return
    if data[12] == '4':
        p = re.compile('相关搜索.*?<a.*?>.*?</a>.*?</th></tr></table></div>', flags=re.S)
        related_title_list_str = p.findall(htmlres)[0]
        related_title_list = re.findall('<a href="/s\?wd=.*?>(.*?)</a>', related_title_list_str, re.S)
        related_title = ''
        related_title_len = 0
        for i in related_title_list:
            if len(i) > related_title_len:
                related_title = i
                related_title_len = len(i)
    else:
        related_title =''
    for t,urlchild in urlpage:
        try:
            res = requests.get(urlchild,
                               headers={'User-Agent': User_Agent().random()},
                               proxies=get_ip(), timeout=60)
        except:
            print('智能采集','获取链接错误')
            continue
        if res.status_code == 200:
            urlchild = res.url
            webdoma = re.findall('site%3A(.*?)%', url, re.S)[0]
            htmlres = res.text
            tree = html.fromstring(htmlres)
            content_ls = ''
            for xpa in xpathcont[webdoma].split(','):
                namelist = tree.xpath(xpa)
                if namelist == []:
                    print('1951 xpath 未匹配到数据',xpa)
                    continue
                for name in namelist:
                    name1 = html.tostring(name)
                    content_ls += htmls.unescape(name1.decode('gbk'))
                if not content_ls:
                    print('1957 content_ls 未匹配到数据')
                    continue
                else:
                    break
            if not content_ls:
                print('1962 该链接未获取到数据',urlchild)
                continue
            else:
                if 'iframe' in content_ls:
                    print('该类型是 视频')
                    continue
                data.extend([urlchild,related_title,content_ls])
                data.insert(15, related_title_list)
                formattedTextPool(data)
                break

def formattedTextPool(data):
    if data[12] != '1':  # 查询是否打开了智能标题
        # 验证标题是字数是否合格
        if str_count(data[7]) < 9:
            title = data[7]
            if data[12] == '4':
                title += '(' + data[14]+')' + '!@#' + title
            else:
                keyword = quote(title)
                urls = 'http://suggestion.baidu.com/su?wd={}&sugmode=3&json=1'.format(keyword)
                res = requests.get(urls,
                                   headers={'User-Agent': User_Agent().random()},
                                   proxies=get_ip(), timeout=60)
                html = res.text
                s = re.findall(r's":(\[".*?"\])', html, re.S)
                if s:
                    restitle = random.choice(eval(s[0]))
                    if data[12] == '2':
                        title = restitle + '!@#' + title
                    else:
                        title += '_' + restitle + '!@#' + title
            data[7] = title
    print('智能采集','整合文章句子,ID：', data[0:9], os.getpid(), get_nowtime())
    conts = content_delet_(data[-1])
    # 判断文章字数是否达标
    if minNumberWordsisActivate and len(conts) < int(minNumberWords):
        print('字数未达标')
        return
    if len(conts) < 800:
        content_list = conts
    else:
        text_ls = cut_sent(conts)
        sentence = ''  # 整合的句子小于800
        content_list = []  # 存放用于整合后的文章
        for i, text_s in enumerate(text_ls):
            if len(text_s) + len(sentence) < 800:
                sentence += text_s
            else:
                # sentence 接近800字, 添加进列表,并分段,重置
                content_list.append(sentence)
                sentence = ''  # 重置整合的句子小于800
        content_list.append(sentence)
    data[-1] = content_list
    contnt_google(data)

def contnt_google(data):
    print('智能采集','翻译文章ID：', data[0:9], get_nowtime())
    if type(data[-1]) !=str:
        content = ''
        for texts in data[-1]:
            # print('智能采集',texts)
            content += google_(texts)
    else:
        content = google_(data[-1])
    content = E_trans_to_C(content)
    # 此处处理 正文内容格式 添加段落副标题
    content_list = content.split('#')
    intervalScale = len(content_list) // 6
    i = 0
    subhead_list = data[15]
    content = ''
    for index, info in enumerate(content_list):
        if index == 0 or index % intervalScale == 0 and info:
            info = re.sub('#', '</p><p>', info, flags=re.S)
            content += "<h3>" + subhead_list[i] + "</h3><p>" + info
            i += 1
        else:
            info = re.sub('#', '</p><p>', info, flags=re.S)
            content += info

    if not data[9]:
        random_time = int(time.time())
    else:
        now_time = int(time.time())
        time_array = time.localtime(now_time)
        start = time.strftime("%Y-%m-%d 00:00:00", time_array)
        end = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        random_time = randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S')
    if data[2]:
        cid = int(random.choice(data[2].split(',')))
    else:
        cid = ''
    if data[3]:
        uid = int(random.choice(data[3].split(',')))
    else:
        uid = ''
    if data[11] == '1':
        # zblog 类型
        if data[1]:
            # 获取随机比例
            randint_data = random.randint(1, 10) * 10
            if randint_data <= int(data[10]):
                # 下载图片,返回路径
                img_path = Down_Compressimg().run(data[7])
                # 上传图片 API
                # add_article_url = '{}/apis.php?act=upload_Img'.format('http://1.zhituicloud.com')
                add_article_url = '{}/apis.php?act=upload_Img'.format(data[4])
                # 上传图片
                try:
                    img_src = zblog_upload_img(add_article_url, img_path)
                    content = content_update_img(content, img_src)
                except:
                    print('智能采集','上传图片失败', get_nowtime())
        payload = {
            "log_CateID": cid,
            "log_AuthorID": uid,
            "log_Tag": "",
            "log_Status": 0,
            "log_Type": 0,
            "log_Alias": 0,
            "log_IsTop": 0,
            "log_IsLock": 0,
            "log_Title": data[7].split('!@#')[0],
            "log_Intro": '',
            "log_Content": content,
            "log_PostTime": random_time,
            "log_CommNums": 0,
            "log_ViewNums": 0,
            "log_Template": "",
            "log_Meta": "",
        }
    elif data[11] == '2':
        # dedecms 类型
        global dedecms_session_ID
        if data[4] not in dedecms_session_ID:
            session_id = get_phpid(data[4], 'admin', 'Bufuguowang123')
            if not session_id:
                print('智能采集','dedecms 登陆失败,')
                # continue
                return
            dedecms_session_ID[data[4]] = session_id
        if data[1]:
            # 获取随机比例
            randint_data = random.randint(1, 10) * 10
            # webid, img_isActivate, column, author, weblink, describe, id, title, redis_name, 8
            #                          isActivateTime, ratioimg, cms, selecttitle
            if randint_data <= int(data[10]):
                try:
                    # 下载图片,返回路径\
                    img_path = Down_Compressimg().run(data[7])
                    # 开始生成并上传第一张图片
                    img_src = dedecms_upload_img(data[4], img_path, dedecms_session_ID[data[4]])
                    content = content_update_img(content, img_src)
                except:
                    print('智能采集','上传图片失败', get_nowtime())
        payload = {
            "channelid": 1,  # 默认值
            "dopost": "save",
            "shorttitle": "",  # 缩略标题
            "redirecturl": "",  # 文章原文链接
            "tag": "",  # 标签
            "weight": 1,  # 文章权重
            "picname": "",  # 缩略图片名
            "litpic": "",  # 缩略图片上传路径
            "source": "",  # 文章来源名称
            "writer": uid,  # 作者
            "typeid": cid,  # 文章栏目
            "typeid2": "",  # 文章副栏目
            "keywords": "",  # 关键字9
            "autokey": 1,  # 自动获取关键字 1 为自动获取
            "description": '',  # 内容摘要
            "remote": 1,  # 下载远程图片和资源
            "autolitpic": 1,  # 自动提取第一个图片为缩略图
            "dellink": "",  # 自动删除非站内链接
            "needwatermark": "",  # 图片是否加水印
            "sptype": "hand",  # 分页方式 hand手动 auto自动
            "spsize": 5,  # 分页大小 k为单位
            "body": content,  # 文章
            "notpost": 0,  # 是否允许评论 0 允许 1禁止
            "click": 1,  # 浏览次数：
            "sortup": 0,  # 文章排序 0:默认排序 7：置顶一周 30：置顶一个月 90：置顶三个月 180：置顶半年 360：置顶一年
            "color": "",  # 文章标题颜色
            "arcrank": 0,  # 阅读权限 0开放浏览 1待审核
            "money": 0,  # 消费金币
            "pubdate": random_time,  # 发布日期
            "ishtml": 1,  # 是否生成html 1：生成html 0：动态浏览
            "title": data[7].split('!@#')[0],  # 文章标题
        }
    elif data[11] == '3':
        # mipcms 接口数据
        payload = {
            'password': 'www.mipjz.com',
            'title': data[7].split('!@#')[0],
            'content': content,
            'cid': cid,
            'uid': uid,
            'tags': text_to_keywords(content) + data[7].split('!@#')[-1]
        }
    else:
        # mipcms 接口数据
        payload = {
            'password': 'www.mipjz.com',
            'title': data[7].split('!@#')[0],
            'content': content,
            'cid': cid,
            'uid': uid,
            'tags': text_to_keywords(content) + data[7].split('!@#')[-1]
        }
    data[-1] = payload
    push_article(data)

# 开始上传文章。
def push_article(data ):
    print('智能采集','上传文章:', data[0:13], get_nowtime())
    if data[11] == '1':
        add_article_url = '{}/apis.php?act=article_Api'.format(data[4])
        # add_article_url = '{}/apis.php?act=article_Api'.format('http://1.zhituicloud.com')
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", add_article_url, data=data[-1], headers=headers)
        if "success" in response.text:
            # if response.status_code == 200:
            print('智能采集',"网站：%s，成功发布文章：%s" % (data[8], data[7]), get_nowtime())
            SQLupdateDate(data[6], False, data[0],data[13])
            Redisset_hash(data[8], data[7])
        else:
            print('智能采集 2235',"网站：%s，文章发布失败: %s" % (data[8], data[7]), get_nowtime())
            print('智能采集 2236',response.text)
            # SQLupdateDate(data[6],
            #                       (data[7], data[8], data[0], data[6], '发布失败,{}'.format(response.text)))
    elif data[11] == '2':
        # 织梦会话ID
        add_article_url = "{}/article_add.php".format(data[4])
        session_id = dedecms_session_ID[data[4]]
        php_id = "PHPSESSID=%s;" % (session_id)
        headers = {
            'Cookie': php_id,
        }
        response = requests.request("POST", add_article_url, data=data[-1], headers=headers, timeout=10)
        if "成功发布文章" in response.text:
            print('智能采集',"网站：%s，成功发布文章：%s" % (data[8], data[7]), get_nowtime())
            SQLupdateDate(data[6], False, data[0],data[13])
            Redisset_hash(data[8], data[7])
        else:
            print('智能采集 2253',"网站：%s，文章发布失败: %s" % (data[8], data[7]), get_nowtime())
            print('智能采集 2254',response.text)
            # SQLupdateDate(data[6],
            #                       (data[7], data[8], data[0], data[6], '发布失败,{}'.format(response.text)))
    elif data[11] == '3':
        add_article_url = '{}/collect/ApiUserHuochetou/articleAdd'.format(data[4])
        response = requests.request("POST", add_article_url, data=data[-1], timeout=60)
        if "发布成功" == response.text:
            # if response.status_code == 200:
            print('智能采集 2262', "网站：%s，成功发布文章：%s" % (data[9], data[7]), get_nowtime())
            SQLupdateDate(data[6], False, data[0], data[13])
            Redisset_hash(data[8], data[7])
        else:
            print('智能采集 2266', "网站：%s，文章发布失败: %s" % (data[8], data[7]), get_nowtime())
            print('智能采集 2267', response.text)
    else:
        # 集群
        add_article_url = '{}/index.php?s=/huochetou/ApiUserHuochetou/articleAdd'.format(data[4])
        response = requests.request("POST", add_article_url, data=data[-1], timeout=60)
        if "发布成功" == response.text:
            # if response.status_code == 200:
            print('智能采集', "网站：%s，成功发布文章：%s" % (data[9], data[7]), get_nowtime())
            SQLupdateDate(data[6], False, data[0], data[13])
            Redisset_hash(data[8], data[7])
        else:
            print('智能采集 2278', "网站：%s，文章发布失败: %s" % (data[8], data[7]), get_nowtime())
            print('智能采集 2279', response.text)

def google_(content):
    trans = google_trans(content)
    af = trans.trans()
    # t_sp = random.uniform(0, 2)
    return af



if __name__ == '__main__':
    SQLselect_global()
    run()


