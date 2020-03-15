import requests
import re
import random
import html as htmls
from lxml import html
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests_toolbelt import MultipartEncoder
from DBUtils.PersistentDB import PersistentDB
from selenium.webdriver.common.by import By
from multiprocessing import Queue
from urllib import parse as up
from selenium import webdriver
from urllib.parse import quote
from threading import Thread
from hashlib import md5
from lxml import etree
from PIL import Image

import multiprocessing
import datetime
import requests
import pymysql
import random
import redis
import time
import json
import os
import re
from html.parser import HTMLParser #导入html解析库

def E_trans_to_C(string):
    E_pun = u',.!?[]()<>""\'\''
    C_pun = u'，。！？【】（）《》“”‘’'
    table= {ord(f):ord(t) for t,f in zip(E_pun,C_pun)}
    return string.translate(table)

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


# 获取IP
def get_ip():
    try:
        ips = requests.get("http://kuyukuyu.com/agents/get?uuid=d5a51445-b1bc-4ecb-81df-db794d704cbb").text
    except:
        time.sleep(0.5)
        ips = get_ip()
    return {
        'http':'http://'+ips,
        'https':'https://'+ips
    }
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


def google_(content):
    trans = google_trans(content)
    af = trans.trans()
    # t_sp = random.uniform(0, 2)
    return af


contents = '''
<article class="article" id="mp-editor">
    <!-- 政务处理 -->
          <p data-role="original-title" style="display:none">原标题：四柱预测详解</p>
            <p>所谓四柱预测学，其实等于把人们出身的年、月、日、时，这四个年光的天干地支作爲四个根柢元素，来猜度人们命运变革的学问，也能够鸣做中国前世算命术。人的出身年、月、日、时配以天干（即：甲、乙、丙、丁、戊、己、庚、辛、壬、癸）以及地支（子、丑、寅、卯、辰、巳、午、未、申、酉、戌、亥）来猜度人生福祸成败的手艺本领。前人认为年、月、日、时就象四根撑持命运的顶梁柱，看文生义，前人把他称爲“四柱”。而每一个柱子上有两个字，所以也称生辰八字。用出身的年柱，月柱，日柱，时柱来推算人的命运的学问鸣做“四柱预测学”。 </p> 
<p class="ql-align-center"><img src="http://5b0988e595225.cdn.sohucs.com/images/20181209/5a37740b02c7483c8df52c387bb40eef.png" max-width="600"></p> 
<p class="ql-align-center">虽然日之升落、月的盈亏、五星运转等等是伟人皆有目共睹的自然情形。但他们却是两个彻底不同的体验全国之象。这两个象，在它们各自所由生的体验全国中都具备真正的意义。天官书是科学不雅测的一个真实纪录，详细标清楚陰陽五行的天象： </p> 
<p>察日、月之行以揆岁星（木星）顺逆。曰西方木，主春，曰甲乙。义掉者，罚出岁星。 </p> 
<p>察刚气以处荧惑（火星），曰北方火，主夏，曰丙丁。礼掉者，罚出荧惑。 </p> 
<p>历斗之会以定镇星（土星）之位，曰地方土，计季夏，曰戊土，黄帝、主德、女主象也。察日行以位处太白（金星），曰东方金，主秋，曰庚金，主杀，杀掉者罚出太白。察日辰之会，以治辰星（水星）之位。曰南方水，太陰之精，主冬，曰壬癸。刑掉者，罚出辰星。天宫书对正常运转刻画的落脚点，却在于"掉行"。素问。气交变大论等也有观测五星测度祸福的纪录。素问曰："五行者，金木水火土，更贵更贱，以知逝世活，以决成败。"荧惑星（火星）、镇星（土星）、太白星（金星）、辰星（水星）的残暴、运转、遥近、留走而知其灾与德。对人类社会的意义而言，"掉行"的意义弘遥于正常运转，天变虽然是人世祸害的前兆，但其根由却在人之所爲。以陰陽五行所代表的干支四柱的掉衡来推知人的祸福，是前世中国的首要体验的结晶，以五行生中断化来均衡命之"掉行"，趋吉避凶，才是真正意义上的知命。 </p> 
<p>五行生克。五行之间存在着恶马恶人骑的规律。恶马恶人骑象陰陽同样是事物不成联系的两个方面，没有生就没有事物的发生气希看愤以及发铺；没有克就没有就不能保持事物在铺开以及变革中的均衡以及折衷。这类生中有克，克中有生，相反相成，互相爲用的干系，推入以及保持着事物的正常发铺、铺开以及变革。五行生克中有生我、克我的相生干系以及克我、我克的相克干系两个方面。 </p> 
<p><img src="http://5b0988e595225.cdn.sohucs.com/images/20181209/bdfd7a8009c040dfb9649f6a4cfe37d6.jpeg" max-width="600"></p> 
<p>五行相生：木生火，火生土，土生金，金生水，水生木；五行相生含义：木生火，是由于木性温热，火隐伏个中，钻木而生火，所以木生火；火生土，由于火炎暖，所以可以焚烧木，木被焚烧后就变成灰烬，灰即土，所以火生土；土生金，由于金需求暗躲在石里，寄托着山，津润润泽而生，聚土成山，有山必生石，所以土生金；金生水，由于少陰之气（金气）温润流泽，金靠水生，销锻金也可变爲水，所以金生水；水生木，由于水温润而使树木发铺出来，所以水生木。 </p> 
<p>五行相克：木克土，土克水，水克火，火克金，金克木。五行相克含义：五行之所以相克是由于寰宇之性：众胜寡，故水胜火；精胜坚，故火胜金；刚胜柔，故金克木；专胜散，故木胜土；实胜虚，故里胜水。 </p> 
<p>五行生克干系。五行相生是循环相生的干系；五行相克是隔位相克的干系。 </p> 
<p>五行生中断化宜忌。陰陽五行不光有生有克、相反相成又彼此制约的一方面，还有过火不及的另外一方面，这就使猜度变患上繁杂化。要想在入修中操作节制这方面的统逐个概干系、必需明宜明忌、变活通用。 </p> 
<p>金：金旺患上火，方成器皿。金能生水，水多金沉；强金患上水，方挫其锋。金能克木，木多金缺；木弱逢金，必爲砍折。金赖土生，土多金埋；土能生金，金多土变。 </p> 
<p>火：火旺患上水，方成相济。火能生土，土多火晦；强火患上土，方止其焰。火能克金，金多火熄；金弱遇火，必见销熔。火赖木生，木多火炽；木能生火，火多木焚。 </p> 
<p>水：水旺患上土，方成池沼。水能生木，木多水缩；强水患上木，方泄其势。水能克火，火多水干；火弱遇水，必不熄灭。水赖金生，金多水浊；金能生水，水多金沉。 </p> 
<p>土：土旺患上水，方能疏浚。土能生金，金多土变；强土患上金，方制其雍。土能克水，水多土流；水弱逢土，必爲淤塞。土赖火生，火多土焦；火能生土，土多火晦。 </p> 
<p>木：木旺患上金，方成栋梁。木能生火，火多木焚；强木患上火，方化其顽。木能克土，土多木折；土弱逢木，必爲倾陷。木赖水生，水多木漂；水能生木，木多水缩。五行与人的干系。周易说，人间万物都一概于太极。金、木、水、火、土这五行是万物最大最显然的，所以，人间万事万物都一概于陰陽五行，人是万物中的一种，自然要插手宇宙生生不休的行动。四柱猜度学，作爲"人生--小寰宇"的声名，是关于人的命运规律的学问，运用的等于五行规律表明人与寰宇的干系。 </p> 
<p>人之性，是与生俱来的本性。所谓性情，指喜怒哀乐恶欲之情以及仁义礼智信之性，离不开金木水火土的彼此干系。虽然人之性随后天之家庭、环境、教育等潜移默化的影响会有所窜改，但从人的四柱命局所显露的陰陽五行旺哀生克当中，仍能大体上瞅出人不随意马虎变换的天分本质的一壁。 </p> 
<p>五行所代表的性、情、色、味、人体、四季、方位等，是最根柢的特点。四柱中的五行有偏旺的一方面，便有偏弱的另外一方面。旺的一方面指特点突出的一壁；弱的一壁是特点隐藏、亏弱的一壁。命中所缺而相应地补，不掉爲明智的知命，可以亡羊补牢，趋吉避凶。如木旺之人，经过四柱综合均衡可以默示出木之性。若木欠缺，缺木，或者木受克，不光从身高、特点、长相、身段安康可以瞅出其欠缺，还可以推知该人平日普通的喜好。喜酸，等于一种生理上个性的补。那麼，经过四柱的综合均衡感性地补，于事业、前途、婚姻、财产、官禄、福寿、六亲、安康、行业选择等有益的补，自然是无益有害的。一个补字，从册本上开铺，就成为了人的人命行动规律的指南。全篇围绕着它作爲四柱猜度进门的金钥匙，无不进展初学者、兴趣者拿着它开启本人的聪颖之门，往挖掘周易术数的瑰宝。 </p> 
<p>怎样补？补气。常言道：人活一口吻。我国自古以来的陰陽五行学说，对秉寰宇之气而生的人来说，即是补金木水火土之气。陰陽五行之气，蕴含了年光以及空间的宇宙时空编制。"寰宇之气"等于人出身时出身地所禀受的五星在天体运转时辰的清浊之气。 </p> 
<p>人的禀性作古守理上可知，还可推及形面子貌辞吐运动善恶。往往高层次的猜度不单用一项，而是集命理，手相面相骨相便是一体的综合猜度，以命局爲主，相法爲辅，相反相成，互爲参用。这样的猜度切确率自然就高，由于这曾冲破了单一从四柱上瞅人的终生，而是连系表露个体祖荫风水、房屋、遗传、五行方位等诸多与他人不同的要素所下的结论，是针对一个特定的人而言的。 </p> 
<p>四柱性情如脾性应乎五行之气。 </p> 
<p>木主仁，其性直，其情以及。木盛的人长患上风味鲜艳，骨骼颀长，昆季细腻，日尖发美，面色皎洁皎洁。爲人有博爱浑水摸鱼，慈祥恺悌之意，得意美妙，纯朴无伪。木衰之人则个子瘦长，头发希罕，脾性偏狭，忌妒不仁。木气作古尽之人则眉眼不正，项长喉结，肌肉作枯燥，爲人鄙下小器。 </p> 
<p>火主礼，其性急，其情恭。火盛之人头小脚长，上尖下阔，浓眉小耳，肉体闪耀，爲人谦以及尊崇，老诚耐烦。火衰之人则黄瘦尖楞，言语妄诞，诡诈妒毒，处事虎头蛇尾。 </p> 
<p>土主信，其性重，其情厚。土盛的人圆腰阔鼻，贼眉鼠眼，辩才声重。爲人忠孝至诚，器度宽厚，言必信，行必果。洋气过火则思想僵化，愚拙不明，外向好静。不及之人面色忧滞，面扁鼻低，爲人恶毒激烈，不讲信用，不讲事理。金主义，其性刚，其情烈。金盛之人骨肉相等，面方白净，眉高眼深，体健神清。爲人坚定则毅，重义轻财，深知廉耻。过火则大智大勇，贪欲不仁。不及则身段肥大，爲人尖刻，喜婬好杀，小器贪心。水主智，其性聪，其情善。水旺之人面黑有彩，言语清以及，爲人沉思熟虑，神机妙算，学问过人。过火则好说黑白、漂荡贪婬。不及则人物短小，性情无常，焦急无略，行事几次。 </p> 
<p>干支。五行大义中说，干支是大挠创制的。大挠"采五行之情，占斗机所建，始作甲乙以名日，谓之干，作子丑以名月，谓之枝。有事于天则用日，有事于地则用辰，陰陽之别，故有枝干名也"。 </p> 
<p>十天干：甲乙丙丁戊己庚辛壬癸。 </p> 
<p>十二地支：子丑寅卯辰巳午未申酉戌亥。 </p> 
<p>干支的含义：群书考异中说：甲是折的意思，指万物剖符而出。乙是轧的意思，指万物初生，抽轧而出。丙是炳的意思。指万物炳然著见。丁是强的意思。指万物丁壮。戊是茂的意思。指万物蕃庑。己是纪的意思。指万物无形可纪识。庚是耕的意思，指万物收敛有实。辛是新的意思，指万物初新皆劳绩。壬是任的意思，指陽气任养万物于世界。癸是揆的意思，指万物可揆度。于是可知十天过问太陽出没有关，而太陽的循环去来交去周期，对万物间接发生着影响。 </p> 
<p>十二地支是用来刻画月亮运转周期的，群书考异中说：子是兹的意思，指万物兹萌于既动之陽气下。丑是纽、系的意思，继萌而系长。寅是移、引的意思，指物芽稍吐而伸之移出于地。卯是冒的意思，指万物冒地而出。辰是震的意思，物经震云贵而长。巳是起、已经的意思，指万物至此已经毕绝而起。午是仟的意思，指万物浩繁枝柯密布。未是昧的意思，指陰气已经长，万物稍衰，体暗昧。申是身的意思，指万物的身段都已经成熟。酉是老的意思，指万物老极而成熟。戌是灭的意思，指万物皆衰灭。亥是核的意思，指万物皆珍躲皆坚核。于是可知，十二地支与月亮的陰陽消长有关。而月亮的循环去来交去的同期异常对万物间接发生着影响。由于十天过问十二地支区分来自对日、月步履特性的瞅法，前人以日爲天、天爲陽，以月爲陰、地爲陰。因此，也就自然以十干配天，十二部署地，而称之爲"天干、地支"了。 </p> 
<p>天干喻人含义。天干在猜度命运中格外极度首要，每一个体出身之日，其日柱由日过问日支形成，日干旺相，不受克（后有细论），其喻人含义更贴切，也即某天干爲日干的赋性更大白，可作爲测脾性之参用。 </p> 
<p>甲（木）属陽。平常指森林大树，性质坚固。甲木爲木之兄，还含有刚正自律之意；乙（木）属陰。指小树，花草之类，性质软弱。乙木爲木之妹，还含有郑重坚强之意；丙（火）属陽。指太陽，炎炎炳照之意。丙火爲炎之兄，含有精神委顿、暖情广大奔放之意。还含有契合于各种交际步履，但也易被误会爲好大喜功；丁（火）属陰。指灯火、炉火等。火势不波动，患上时无力，掉时有力。丁火爲火之妹，具备外静内入，头脑周密的脾性；戊（土）属陽。指大地的土，广厚蕃庑。又指堤坝之土，可无力地胁制河川浩瀚。戊土爲土之兄，含有望重轮廓、善于交际、交际才华强的意思，但也有易掉主见，与人聚合无常之意；己（土）属陰。指家乡之土，不如戊土广厚但易栽植。己土爲土之妹，平常指心细，服务有规律，但也含有器量小之意；庚（金）属陽。指铁、刀剑、矿石等，性质坚韧。庚金爲金之兄，其人略具文才，夸张物质所长，有经济才能花腔；辛（金）属陰。指珠玉、宝石、砂金。辛金爲金之妹，它可以屡经考验而终成大事，同时也含有坚强之意；壬（水）属陽。指大海之水，壬水爲水之兄，含有清浊并容、宽庞娟秀之意，能暗藏以及容纳，反之也有依托性强，凡事掉落以轻心之意；癸（水）属陰。指雨露之水，也有闭躲以及内在萌发之意。癸水爲水之妹，其人正大勤奋，身处顺境也会斥地前途途。 </p> 
<p>地支掌诀图：四柱地支是与天干一同参断的均衡要素，爲方便记忆各种地支生合局会刑冲害的干系用于猜度，将十二地支化在手掌上，可以格外极度便利、抽象地记取各种有规律的干系，做到着手就来。其各种干系将在前面细论。 </p> 
<p>干支陰陽五行。干支陰陽之分，按周易中所说，太极是生两仪。五行的金木水火土之性是万物构成的根柢物质。其始也具太极，所以说：甲乙同一属木。继生两仪，甲爲陽干，乙爲陰干；丙丁同一属火。丙爲陽干，丁爲陰干；戊己同一属土。戊爲陽干，己爲陰干；庚辛同一属金。庚爲陽干，辛爲陰干；壬癸同一属水。壬爲陽干，癸爲陰干；寅卯同一属木。寅爲陽支，卯爲陰支；巳午同一属火。午爲陽支，巳爲陰支；申酉同一属金。申爲陽支，酉爲陰支；亥子同一属水。子爲陽支，亥爲陰支；土居四维，在四时之未，故辰戌丑未同一属土，辰戌爲陽支，丑未爲陰支。 </p> 
<p>干支陰陽表 </p> 
<p>陽干 甲 丙 戊 庚 壬 </p> 
<p>陰干 乙 丁 己 辛 癸 </p> 
<p>陽支 子 寅 辰 午 申 戌 </p> 
<p>陰支 丑 卯 巳 未 酉 亥 </p> 
<p>干支方位。 </p> 
<p>十干方位：甲乙西方木，丙丁北方火，戊己地方土，庚辛东方金，壬癸南方水。十二地支方位：寅卯西方木，巳午北方火，申酉东方金，亥子南方水，辰戌丑未四时土。 </p> 
<p>十支方位来自我国前世地理学家爲了不雅测天象及日、月、五星在天空中的运转，在黄道帝与赤道带的双侧绕天一周，拔取了二十八个星官（星官等于把多少好多颗恒星形成一组，每一组用地上的一种事物命名，这一组就称爲一个星官），作爲不雅测标记，称爲二十八宿。把二十八宿又分爲四组，每一组七宿，与东、南、西、北四个方位以及苍龙、白虎、朱雀、玄武四栽培物抽象相配，称爲四象、四方。 </p> 
<p>干支覆载。在四柱猜度中，不管是四柱命局的干支照旧大运的干支，抑或者流年（当年、去年）的干支，都是无机的扫数，是覆载的干系，即天干覆下爲地支，地支所承载的是天干，如天干甲或者乙是该四柱的日干即论命自身的五行所主。以日干来统瞅其他干支其强弱干系主要，若地支有寅、卯同类相帮，亥子相生者来承载甲或者乙，就可以使自身生旺，若是忌讳的申、酉承载，就会受克败伤，假定论命中地支寅或者卯很首要，那麼甲乙或者壬癸爲天干来覆载，就可以使寅或者卯生旺，若遇天干庚辛覆载，就会受克伤。所以，隐瞒或者承载的干系可以使某一五行无力。其二，天过问地支五行同类爲通根，天干通根于地支，甲有寅中甲草本气爲根，即是掉掉落了生扶，那麼天干的根就平稳，甲木遇卯支时，卯中躲同类乙木，其根气力次于寅中甲木。地支若遇上冲撞，那麼天干的根就会很随意马虎拔起。反之地支受天干的荫护，假定天干逢生扶，那麼地支所受的荫就更盛。假定天干逢凶克，那麼地支所受的荫就衰减。干支覆载对四柱命局的整体均衡有着相当首要的感召，初学者不应马虎这门根蒂根基课。干支五气淡季。寰宇万物终始，亦即五气"相次转用事"的历程，故每气都有隆替作古生之时。 </p> 
<p>盛之时，即爲应时。以干支表象则爲：甲乙寅卯木旺于春；丙丁巳午火旺于夏；庚辛申酉旺于秋；壬癸亥子水旺于冬；戊已经辰戌丑未土旺于四时。 </p> 
<p>在命运猜度中，前人总结出一整套科学的推算法度榜样，力图与天体的运转规律相符合，这即是经过个体出身之日的陰陽天干五行，关于所生之月个体所处的逆顺、衰旺以及厚薄的禀寰宇之气的状况，推出人终生的命运。如甲生寅月，今日干爲甲木，生于立春以后惊蛰以前，甲患上地利天时，禀气自然艰深深挚，故称"临官"。若生在申月，申的属性爲陽金，克木，申月在立秋以后白露以前，正值万木掉时掉势之时，老木刚刚作古往所生之木未成形之时，故木"尽"于申。其他所处月令蕴躲的命运信息也可一一推知。如"临官"、"尽"等十二阶段，象征一年十二个月的气味，他们的次第是长生、洗澡、冠带、临官、帝旺、衰、病、作古、墓、尽、胎、养。示意五行在十二地支中所默示的形态。 </p> 
<p>十天干案十二宫： </p> 
<p>"长生"就象人出身于世，或者诞生阶段，是指万物萌生之际。"洗澡"爲婴儿诞生后沐浴以吊销污垢，是指万物出身，蒙受大自然洗澡。"冠带"爲小儿可以穿衣戴帽了，是指万物渐荣。"临官"像人长成坚固，可以做官、化育、诱导人民，是指万物长成。"帝旺"象征人壮盛到极点，可帮手帝王在有作爲，是指万物效果。"衰"指盛极而气衰，是指万物初阶发生气希看愤衰变。"病"如人罹病，是指万物窘迫。"作古"如人断气，形体已经作古，是指万物断命。"墓"也称"库"，如人作古后回进于墓，是指万物乐成后回库。"尽"如人形体尽灭化回爲土，是指万物前气已经尽，后继之气还未到来，在地中未有其象。"胎"如人受父母之气结聚成胎，是指寰宇气交之际，后继之气来临，并且受胎；"养"像人养胎于母腹当中，以后又出身，是指万物在地中成形，继而又萌生，又患上经验一个生生灭灭永不中止的天道循环历程。 </p> 
<p>从长生次第经过十二辰推下往，富强盛年夜确定会坚固，盛极确定会败落，循环去来交去，这是四时之所以交错运转、五行之气之所以顺布的缘故，而土寄生于寅，是由于寅是正月孟春，这时候天气降落，地气上升，寰宇以及同，草木是以萌发。所以把土瞅作生于寅，是爲了顺照五行相一的挨次，是出自然之理。此外，陽天干作古那麼陰天干就生，陽天干在十二宫中顺推，陰天干逆推，这是陰陽二气的不同，吻合天道左旋，地道右迁之理。陽天干临官，那麼陰天干等于帝旺；陰天干临官，陽天干等于帝旺，这是四时之会。至天洗澡有败地之说，咱们认为此说有背自然之理。婴儿出身加于洗澡，作出气弱不能胜而爲败地这样的表明不能令人敬仰，且以万物萌生之际，果核、种子发芽，那麼芽的顶部的青壳也会自然告另外表明南辕北辙，更何况长生至帝旺渐至壮盛，纵使弱不经风，也不会影响其抽芽滋生。若表明爲败地，那麼怎样从新畅旺，接着的冠带、临官、帝旺又从何说起呢？ </p> 
<p>前人论十干就分陰陽，论五行等于陽统陰，其顺、逆、分、合都及有妙理，都是自然之理。在理论检讨中，非论是陽干顺推，陰干逆推，照旧洗澡爲日干生旺之地，都是切确的，读者也能够本人推验。记用十干寄十二宫的各个阶段旺衰格外极度首要，猜度中时辰少不它。记忆时，从掌诀图上按五陽干长生、洗澡、冠带、临官、帝旺、衰、病、作古、墓、尽等的挨次从日干的长生地顺推点读，五陰干按长生、洗澡......的挨次从日干的长生地逆推点读，只需记取是陽干甲、丙戊、庚、壬的长生区分是亥、寅、巳、申环手指顺点至出身之月便知其处何种形态；陰干乙、丁已经、辛、癸的长生区分是午、酉、子、卯，环手指逆推至欲推之月，便知其处何种形态，"十干长生顺逆掌诀图"的用法，谙练之下，条理分明，格外极度方便，随时可用。 </p> 
<p>日主定十神。日主爲我，爲己身。日主的五行之性与四柱中其他干支的五行之性的干系不外乎正偏，生克。陽日干见其他陽干爲异性相见，爲偏；陽日干见其他陰干爲异性相见，爲正。异常，陰日干见其他陰干爲异性相见，爲偏；陰日干见其他陽干爲异性相见，爲正。 </p> 
<p>其他各过问日主我有：生我，我生，克我，我克，同我五种干系。 </p> 
<p>生我者有父母之义，故立名印绶。印，荫也；绶，受也。譬喻父母有恩德，荫庇子孙。子孙患上受其福。国度设官分职，绶以权印，使之掌管，官无印，无所凭，如人无父母无所依其理一也。 </p> 
<p>我生者有儿女之义，故立名食神。食者，如爲虫食物则伤物，人食物则能造物。 </p> 
<p>克我者我受制于人之义，故立名官杀。国度封官与人，人身属公众，驱策终生作古然后已经。此言爲既患上官又爲官害之义。 </p> 
<p>我克者是人受制于我之义，故立名妻财。如人娶妻又有嫁妆田土陪嫁，财产供我享用，妻侍夫我，我患上妻室内人不致疲钝。 </p> 
<p>同我者如我兄弟之义，故立名比肩。 </p> 
<p>鄙人面的生中断化的干系中，日主的我爲陽干时，柱见陰干爲正，见陽干爲偏。如陽干日主，柱中生我的陰干爲正印，爲生母的话，柱中生我的陽干则爲偏，偏印则爲继母，庶母。所以，除了有五种干系之外，还有十神之别。 </p> 
<p>"生我"者爲父母。陰干生陽我，陽干生陰我爲正印；陽干生陽我，陰干生陰我爲偏印。 </p> 
<p>"我生"者爲儿女。陰我生陽干，陽我生陰干爲伤官；陰我生陰干，陽我生陽干爲食神。 </p> 
<p>"克我"者爲官杀。陰干克陽我，陽干克陰我爲正官；陰干克陰我，陽干克陽我爲七杀。 </p> 
<p>"我克"者爲妻财。陰我克陽干，陽我克陰干爲正财；陰我克陰干，陽我克陽干爲偏财。 </p> 
<p>"同我"者爲兄弟。陰干同陽我，陽干同陰我爲劫财；陰干同陰我，陽干同陽我爲比肩。 </p> 
<p>由上可知，我爲日主： </p> 
<p>克我，抑我者爲官杀。异性-偏官，异性-正官 </p> 
<p>生我、扶我者爲印星。异性-偏印，异性-正印 </p> 
<p>同我、助我者爲比劫。异性-比肩，异性-劫财 </p> 
<p>我生、泄我者爲食伤。异性-食神，异性-伤官 </p> 
<p>我克、耗我者爲财星。异性-偏财，异性-正财 </p> 
<p>天干十神的查法，如日主爲甲；四柱中其他三个天干见甲就爲比肩，见乙就爲劫财，见丙爲食神，其他仿此。 </p> 
<p>1、化合要则 </p> 
<p>首先，干支化合，有合化与只合不化之别。 </p> 
<p>天干合化与否，须以日干爲主，紧邻月干或者时干爲合，且月支须爲合化之同一五行方论合化。如甲与己合化土，须日干爲甲，月干或者时干爲己；日干爲己，月干或者时干爲甲，而且月支爲辰戌丑未土月生人，与合化之五行相反方可论化。 </p> 
<p>还有两种状况也可合化：一是年月天干相合，年支爲合化之五行有根患上化。如年庚月乙合金，年支爲申金。二这天过问月干或者日过问时干合，月支不化，所化五行在其他三支分化局或者会局也可论化。如庚日与乙月合金，月支不是申或者酉月，但年日时支分化了巳酉丑或者申酉戌，其化乐成。 </p> 
<p>地支合化与否，须两支紧邻相贴，且天干须透出地支合化之五行方可论化。如卯与戌合化火，天干透出丙火或者丁火，与地支合化之火爲同一五行而论化。 </p> 
<p>非相邻之合爲远合，其合力欠缺以成情形；相邻之合不化，以合无论化。其次，凡天合、地合，合化以后，以合化后的五行论，原五行掉却其感召；合而不化，爲独立五行，均再也不与其他干支论生克或者刑冲。但大运流年又呈现其一，爲媾合增其合力。 </p> 
<p>2、天干生克要则 </p> 
<p>天干相生：邻干之生，其生力大于隔干；异性之生，其生力大于异性；生者减气，受生者患上益。 </p> 
<p>天干相克：吉神相克爲凶，凶神相克爲吉；两干相克，邻干力大，隔干次之，遥干有力；两干异性相克之力大于异性相克；两干相克均受损伤、受克损伤大；隔干之克，中隔之干化克则不以克论。如丙火隔干克庚金，中隔土，是土泄火气而生金气，继承相生，故以生论不以克论。 </p> 
<p>克中有合，合往克则不作克论。如丙火克庚金，但柱中有辛，丙辛合水，水是克火的，丙火克不了庚金，故不以克论。 </p> 
<p>日干被他干克，又有他干的制，不作克论。如庚日干被丙月干克，丙月干则被壬年干制服，故不以丙庚克而作壬丙克论。 </p> 
<p>3、天干合化主事 </p> 
<p>天干合化爲真者，贫贱至名公巨卿。合化爲假者，则爲孤儿异性或者爲僧道。干合者，有晚婚之兆。下列爲方便入修者作备窥察验用，一因四柱不全不能盖论，二因前人对十干性质有纤细的精细美好故有待于在理论中一一论证。 </p> 
<p>甲己合化土：爲中正之合。主循规蹈矩、重信课本。若命局无它土，又带七杀，则欠缺友谊、设计多端、不知廉耻，性刚。 </p> 
<p>甲日干合己，遇乙木：妻财暗损；丁火：衣禄成空；辛金：贵要高门；戊土：家殷大富；癸水：一生发福；庚金：空空如也；丙火：禄享千钟。 </p> 
<p>己日合甲干，遇丁火：他人陵虐；乙木：本人遭受；辛金：家殷巨富；庚金：孤冷白屋；癸水：官职迁荣。 </p> 
<p>乙庚合化金：主仁义之合。刚柔兼备，重仁守义。若有偏官或者坐作古尽等弱运者，反坚强己见，轻仁寡义。 </p> 
<p>乙日干合庚，遇丙火：蹇难；癸水：繁荣；丁火：似春花之笑日；己土：合座金玉；辛金：若秋草逢霜；甲木：麻麦盈仓。 </p> 
<p>庚日干合乙，遇金：暗损；丙火：相煎；丁火：如蛟龙患上云雨；癸水：家乡漂零；壬水：财禄增迁；戊土：不可巨富，逢壬水助方永保长年。 </p> 
<p>丙辛合化水：主威严之合。仪表威严，智力优越。若带七杀或者坐作古尽者，反性酷无情，瑰异寡合。女命逢支冲，合化之水，主性感纵欲。 </p> 
<p>丙日干合辛，遇戊土：成名；乙木：官爵迁荣；癸水己土：家门煊赫；壬水辰土：祸败。 </p> 
<p>辛日干合丙，遇戊土庚金：功名。 </p> 
<p>丁壬合化木：主仁寿之合。心肠惨酷，龟龄多寿。妇命若命局水过旺泄木，则爲婬欲之合。若坐作古尽者，酒色破家。 </p> 
<p>丁日干合壬，遇丙火：历年闲适；辛金：一入优游，贫贱双全；戊土：活计消遣；癸水：生活生存孑立；乙木重重：财禄无成；庚金叠叠：功名莫看；喜甲临辰：禄封双美；喜已经共酉亦禄封双美。 </p> 
<p>壬日干合丁，遇甲木：多遭仆马；辛金：广置田庄；丙火：铁汉英雄；癸水：辛苦经商；己土：佩印乘轩；戊土：转蓬高卑潦倒；庚金：皓首无成；乙木：青年不遇。 </p> 
<p>戊癸合化火：主无情之合。容颜英俊，痴情乏义，男多抱玩世之心，女则多嫁俊夫。 </p> 
<p>戊日干合癸，遇乙木：终能闻达；壬水：伶仃丰隆；丙火：难寻福禄；庚金：易见利市；己土：妻子有损；辛金：策画爲拙。 </p> 
<p>癸日干合戊，遇丙辛：一世多成多败；甲已经：历年劳心劳力；丁火：仓库丰肥；庚金：田财殷实；乙木：官爵陆荣；壬水：，财禄兼顾；辛金：财缘患上掉；己土：仕途蹭蹬。 </p> 
<p><img src="http://5b0988e595225.cdn.sohucs.com/images/20181209/91bfef9880e4469f8e614f428f7c2ddb.jpeg" max-width="600"></p> 
<p>4、地支六冲主事 </p> 
<p>忌神冲，吉；喜神冲，凶。 </p> 
<p>子午冲：一身不安；卯酉冲：违约掉信，愁闷多劳，色情胶葛；寅申冲：多情且好管正事；巳亥冲：多事、喜助人；辰戌冲：克亲伤子寿短；丑未冲：事多阻逆；年与月支冲：离祖别乡；年与日支冲：与亲敦睦；年与时支冲：与子敦睦；年与日月时支冲：性焦躁或者易得疾；日冲月支：犯父母兄弟；四柱逢冲：多不居父母家；子午卯酉冲：地区之冲，指寓居地变迁，职业安定；寅申巳亥冲：职业之冲，指寓居地以及职业均窜改；辰戌丑未冲：职业之冲，指寓居地安定，职业变革。 </p> 
<p>5、地支相刑 </p> 
<p>寅刑巳，巳刑申，申刑寅：爲无恩之刑。 </p> 
<p>四柱有所刑者或者逢岁运相刑者：性情冷峭薄义，或者遭人谗谄及凶事发生气希看愤。若再坐十二宫作古尽者，更甚。女命遇此刑易损孕。 </p> 
<p>未刑丑，丑刑戌，戌刑未：爲恃势之刑。 </p> 
<p>四柱有所刑者，恃本人之势，过于大入，易遭故障掉败。与十二宫中长生、洗澡、冠带、临官、帝旺同柱：精神坚忍。与作古、尽同柱：卑屈或者多狡猾，常罹疾招灾。女命则孤傲。 </p> 
<p>子刑卯，卯刑子：爲无礼之刑。 </p> 
<p>四柱有所刑者，欠缺独立自主，行事虎头蛇尾，坚强已经见，常陷逆境，且面貌鄙劣，内心险毒。与作古尽同柱者。思考陋劣，重者致疾。生日有此刑，夫妻有疾；生时有此刑，子病弱。四柱有二组自刑者，其吉兆更甚；四柱命佳，反有贵之诱力。 </p> 
<p>6、地支相害主事 </p> 
<p>子未害：不能利润骨肉；丑午、卯辰害：逢旺易怒，欠缺忍受力，坐十二宫弱地，恐有残伤；寅巳害：重金者，疾病缠身；酉戌害：重聋哑或者头面多恶疮；月支害：孤傲薄命。女命更甚；日时害：老岁尾年残疾。第六节会局合冲总论要则 </p> 
<p>天干化合者，秀气也。地支合局者，福德也。 </p> 
<p>干合支合，爲以及顺谐调，平常爲多吉小凶。刑、害、冲是命局干支敦睦顺的默示，大多爲多凶小吉。详细要分析合爲喜照旧合爲用神所忌。刑、害、冲是于用神无益照旧有损。 </p> 
<p>三刑以及六害在款式中合论的不多。总之刑、害、冲只能一对一，一对三地刑或者冲或者害。在此只将三会、三合局、半合局、六冲、天地，在款式中呈现的各种状况的揣摸要则作个引见。平常说来三会局的气力大于别的气力，因三会成一方之气，其次是在合局，只需会局或者合局三支彻底，其他一支不会对他们有什麼阻截。三会与六冲相见以会论。三合局与六冲相见除合局中的子午卯酉被紧贴之支打破外，均以合论。三合局旺支合指长生与帝旺，帝旺与墓库半合（如亥与卯、卯与未），长生与墓库爲非旺支半合（亥与未半合几无合气）。旺支半合紧贴但遇旺支紧贴而冲，以冲论。半合紧贴遇非旺支冲，冲不动，以半合论。半合中隔冲支，以冲论。半合中隔一有关紧迫之支，若半合透出所化之五行（如亥卯半合中隔一他支爲无用，但三合局爲化木，多少好多透甲或者乙则可），以半合有用论。反之无用。旺支半合与天地相见，以半合论。六冲与天地相见，除了天地无力外，以冲论（如未年午月子时、午未合土未无力则不作子午冲）。冲支中有子午卯酉本气之冲，子冲午，了主克，午受克；卯冲酉，卯受克，酉主克，有相战之冲意，最爲凶悍。寅申、巳亥之冲次之。而辰戌冲，丑未冲是土之本气冲，因激发而旺，无战克之意，但个中气、余气所躲干之间另以生克论。遥隔相冲是有冲之心无冲之力，克性不大，冲力爲动而已经。准绳上：三会局>三合局>旺半合>天地>非旺半合.各合见冲,以要则爲准.总之,以合论有益命局爲喜,反之爲忌;以冲论益命局爲喜,反之爲忌。 </p> 
<p>天干化合者，秀气也。地支合局者，福德也。 </p> 
<p>干合支合，爲以及顺谐调，平常爲多吉小凶。刑、害、冲是命局干支敦睦顺的默示，大多爲多凶小吉。详细要分析合爲喜照旧合爲用神所忌。刑、害、冲是于用神无益照旧有损。 </p> 
<p>三刑以及六害在款式中合论的不多。总之刑、害、冲只能一对一，一对三地刑或者冲或者害。在此只将三会、三合局、半合局、六冲、天地，在款式中呈现的各种状况的揣摸要则作个引见。平常说来三会局的气力大于别的气力，因三会成一方之气，其次是在合局，只需会局或者合局三支彻底，其他一支不会对他们有什麼阻截。三会与六冲相见以会论。三合局与六冲相见除合局中的子午卯酉被紧贴之支打破外，均以合论。三合局旺支合指长生与帝旺，帝旺与墓库半合（如亥与卯、卯与未），长生与墓库爲非旺支半合（亥与未半合几无合气）。旺支半合紧贴但遇旺支紧贴而冲，以冲论。半合紧贴遇非旺支冲，冲不动，以半合论。半合中隔冲支，以冲论。半合中隔一有关紧迫之支，若半合透出所化之五行（如亥卯半合中隔一他支爲无用，但三合局爲化木，多少好多透甲或者乙则可），以半合有用论。反之无用。旺支半合与天地相见，以半合论。六冲与天地相见，除了天地无力外，以冲论（如未年午月子时、午未合土未无力则不作子午冲）。冲支中有子午卯酉本气之冲，子冲午，了主克，午受克；卯冲酉，卯受克，酉主克，有相战之冲意，最爲凶悍。寅申、巳亥之冲次之。而辰戌冲，丑未冲是土之本气冲，因激发而旺，无战克之意，但个中气、余气所躲干之间另以生克论。遥隔相冲是有冲之心无冲之力，克性不大，冲力爲动而已经。准绳上：三会局>三合局>旺半合>天地>非旺半合.各合见冲,以要则爲准.总之,以合论有益命局爲喜,反之爲忌;以冲论益命局爲喜,反之爲忌。 </p> 
<p>在命理中,非论这天干弱之又弱,照旧日干旺之又旺,都是病源、病根，有否补充但瞅用神。 </p> 
<p>日弱要生扶或者日旺要抑、耗、泄，而四柱又只要八个字，与一座天平同样，这边的砝码大了哪里就翘；哪里的砝码大了这边就翘。更抽象一些就如挑担。弱，等于小的一边，担轻的一边；旺，等于在的一边，担重的一边。用神等于把大的重的一边刚好给够小的轻的一边的阿谁份量。好运是用神到位即给够份量的命运到来之时（这是针对病重，四柱掉衡而言）。也即扁担前移或者后挪刚好能使先后的担子颠簸挑起阿谁着力点（这是针对四柱病不重，尽对均衡而言）。在命局中爲用神患上力，在运程中爲终生最佳的时期。 </p> 
<p>命中有用神，命运就均衡许多，用神无力活患上轻松；用神出瑕玷，辛苦一些；用神破坏，艰巨许多；用神单薄受克，不如命中无用神，靠运中用神来补充。用神于这天干旺照旧日干弱来定夺的。日干旺即身旺，反之爲弱。 </p> 
<p>对身旺照旧身弱的判别，是四柱猜度入进推算的首要末了。终生祸福的揣摸即是由此下手。第一节日干旺衰 </p> 
<p>日干旺蕴含四个方面：患上令、患上地、患上生、患上助。（一些书作患上令，患上时、掉势论）。患上令：日干旺于月支，处长生、洗澡、冠带、临官、帝旺之地爲患上论。患上地：日干在其他各支中患上长生（须陽日干）、禄刃（支中躲干的本气爲比，爲劫），或者逢墓库（陽日干逢墓库爲有根，陰日干无气，故无根）。患上生：日干患上四柱干支中的正偏印之生爲患上生。患上助：日过问四柱其他天干同类爲逢比肩劫财帮身，此爲患上助。 </p> 
<p>在四柱命局中，日旺与否在很大水平上瞅陰令对日干来说处于什麼形态，日干生在旺月爲患上令，但假定不患上地，不患上生、助，势必克泄耗大于生助，则旺而不旺了。日干处在衰月爲掉令，假定生助多而旺，则弱而不弱了。 </p> 
<p>身旺的判别条件。我从优越的古贤书以及少量的理论中发现：首先，日干患上令是判别身旺最首要的方面；其次，在患上令的前提下，患上地、患上生或者患上助再占其一，可以确定是身旺。占其二爲偏旺偏强。三者都占，就爲过旺至极；其三，在不患上令的状况下，患上地、患上生或者患上助占其二项以上，要无力又多助益，爲身旺或者偏旺；其四，在不患上令的状况下，患上地、患上生或者患上助只占一项，但四柱中三合局或者在三会局爲生身之印局，或者爲帮日干之身的比局，爲身旺；其五，在不患上令的状况下，假定患上地、患上生或者患上助无力且众，虽占二项仍爲身旺，但假定地中长生、禄、刃、墓中占的身分少，势必地支中克我，耗我，泄我的身分就多。日干便处于较均衡的不旺不弱之间，不随意马虎定出旺衰，用神就不好找，走什麼运更好就无从论起。在这类状况下：</p> 
<p>1，假定天干化合以及五行或者地支合化的五行是生身帮身，就爲身旺；是中断我，耗我气以及泄我气的，便爲身弱。</p> 
<p>2，地支半合或者半会生身帮身五行的，也爲身旺，反之爲弱。</p> 
<p>3，克我，耗我或者泄我之气的处在弱地（不患上令），而生我，帮我之气的处在旺地，则爲身旺，反之不弱；</p> 
<p>4，克我、耗我或者泄我的干支逢冲、被制服、被合往，或者离患上遥，仍爲身旺，反之爲弱。 </p> 
<p>再如干支患上生的成分几何也是异常事理。如甲日干身弱，患上地支亥、子，天干壬癸生日干，爲患上生，但干支都生以及只一二生日干，份量就要酌情加减来定旺衰强弱。 </p> 
<p>天干患上助的成分的几何也可依理参用，如甲日干身弱，患上其他天干之甲比肩，乙劫财帮身爲患上助，其帮身的份量几何蕴含合往照旧合来，也要酌情加减来定身旺照旧身弱。合往，在患上助的成分中要减力，如甲日，其他天干有乙与庚合金，不仅合往帮甲身的乙木，还分化克木之气，当然患上助的成分要减。如庚日，其他天干有乙与庚合金，不仅合往耗庚金日干的乙木，还合爲帮身之金，其患上助的份量即便正本不多也变许多了。 </p> 
<p>身弱的判别条件在操作节制了身旺的判别技艺以后，从反面加以相识就可以断了。对身旺身弱的操作节制，是推命最关头的第一环，繁杂在于对日干以外干支的强弱、遥近、生克、冲合的综合判别能否切确。推命技艺的高低，断事切确与否都基于此，也是最难教会，不仅要靠言传，而且要靠融合以及神领。 </p> 
<p>操作节制了鉴别各各五行的气力，掂量出日干隆替强弱，公平取用，就确定能操作节制住命脉，到达切确猜度的目的。 </p> 
<p>但凡日柱天干属木的人，确定要鉴别明白较着春木势的隆替、木重而水多，等于木势隆盛，应以适宜的金来削木，假定金太少，遇上土也好。木显患上单薄而金很刚强，等于木势败落，应用火制金，假定火太少，那麼遇木也好。至于水太盛木就会被漂走，用神应取土爲上，其次再用火；土过重木就会变患上健康，应取木爲上，其次用水。火太多木就会被焚烧，应吊水爲上，其次取金爲用神。 </p> 
<p>但凡日柱天干属火的人，确定要鉴别明白较着其火力是不够照旧欠缺。火势炽烈且木多，爲不够应用水来缓济火，假定水势健康，遇金也好。火势败落且水势茂盛，爲欠缺，应取土来制木，假定土健康，遇火也好。至于木多火势就炽暖，用神应吊水把握爲上，其次取金爲用神；金太多火会熄灭，应取火爲上，其次再用木；土太多火会隐晦不显，应取木爲上，其次再用水。 </p> 
<p>但凡日柱天干属土的人，确定要鉴别明白较着其土质是厚是薄。土质凝重且水少，爲厚，宜用木来疏土，假定木太弱，碰着水也好。土质轻快并且木浩繁，爲薄，宜用金制木，假定金太弱，遇上土也好。至于火太多，土就会被烤焦，用神应吊水制火爲上，其次再用金。水太多那麼土就会被冲走，应拔取土爲上，其次再用火；金太多，土就会变健康，应取火爲上，其次再用木。 </p> 
<p>但凡日柱天干属金的人，确定要鉴别明白较着其金质是钢是弱。金多且土厚，爲钢，宜用火来修炼金，如火太健康，碰着木也好。木很重且金又轻，爲弱，宜用土来发铺金，土太衰，碰着金也好；至于土太多，那麼金就会被隐藏，用神应取木爲上，蕨再用水；水太多那麼金就会沉潜于水中，这类状况应拔取土爲上，其次再用火。灼暖太炽暖，那麼金就会损伤，应吊水爲上，其次用金。 </p> 
<p>但凡日柱天干属水的人，确定要鉴别明白较着其势的大小。水不少且金又重，爲水大，宜用土来打击以及把握水，假定土太弱，碰着火也好。水很少土又多，爲水少，宜用木不制土，木太弱，碰着水也好。至于金太多，那麼水就会变患上浑浊，用神应取火爲上，其次再用木。火太炽烈，那麼水就会被烤干，应吊水爲上，其次再取金爲用。木太多，那麼水就会隐缩不畅，应拔取金爲上，其次再取土爲用神。 </p> 
<p>论四季之木宜忌 </p> 
<p>穷通宝鉴上说： </p> 
<p>春季的木，还带有残剩的冷气，假定碰着火来温热，才具贯注盘愚笨折屈身的祸害；假定是碰着水来润湿，就会感想熏染有益落索性舒坦的美丽。但假定水太多树木就会湿润腐烂，水太少树木就会枯毁，因此，必需水火都过度才最佳。至于假定土太多了，就会消耗树的内力，也是值患上忧郁的；假定土比照寒淡，那麼树木就会兴隆蕃庑。假定这时候的木碰着金，就会变患上坚韧，碰着火也没有大的损伤；倘使木曾很坚固了，碰着金也不怕，同样发铺。 </p> 
<p>夏天的木，根以及叶都很作枯燥，树木由初阶曲折屈身而挺直，由盘屈而伸铺；喜欢浩繁的水来潮湿它，忌怕炽烈的火来焚烧它；患上当发展于薄土而不宜厚土，土太厚对树木等于一种灾难；腻烦太多的金而不腻烦少金，由于金太多木就会被中断，那样就会像一层层的树木，兴隆蕃庑，只徒自成林，一叠叠的花朵，开患上大度，但终究照旧不成绩实。这等于所谓："重重见木，徒自成林，叠叠逢花，终无成绩。" </p> 
<p>秋天的木，轮廓逐渐干枯萧条。初秋的时分，还保管有火气，喜欢水土来滋养；中秋的时分，果实曾结成，喜欢刚硬的金来削落它；霜降以后，不患上当太盛的水，水太盛了木就会被漂起来；冷露以前，又患上当较强的火来加暖，灼暖那麼木就平稳。木多就有多材的美称，土太多太厚木就没法长生自立。 </p> 
<p>冬季的木，盘愚笨折屈身在地上，进展多一些土来培育晋升栽培晋升资养它，害怕水太多来沉没它的身段。金即便多，对它也没有损伤；假定火这时候再次呈现，对木就有温热之功。落饮水思源"复命"的时分，木的病衰之势是不能阻碍的，只是忌怕这时候作古尽了，应该长生，存活它。 </p> 
<p>论四季之火宜忌 </p> 
<p>春季的火，木与火母子（木生火）相旺，权力并行；喜欢木来扶持，但不应太茂盛，木太旺火就变患上火暖，进展水来缓济它，但不患上当太多，太多火就会被浇灭；土太多火就会变患上隐晦无光，火太盛就会狠恶高亢。假定碰着金正可以阐扬火的威势，即便碰着不少金也是好的。 </p> 
<p>夏天的火，正是掉势的时分。假定碰着水来制衡它，就会贯注自尊自焚的灾难；假定碰着木来扶持火势，就确定会有遭夭折的忧患；假定碰着金就更兴旺，碰着土也是好的。但金土虽然有益，没有水那麼金就作枯燥，土就焦烈，假定再加之火势太盛，必然会招致倾败殒命。 </p> 
<p>秋天的火，性情安全，身段休闲，假定碰着木来扶持有再次明旺的喜庆；假定碰着水来冲撞，就难藏匿熄灭的灾难。土太多就会掩往火的残暴，金太多就会夺往火的威势，火与火等于以辉想相见扶持的，因此，即便遇见不少也是有益的。 </p> 
<p>冬季的火，形体尽灭、消失。喜欢木来扶持才无效；碰着水来冲撞就遭殃了；进展土来对其加以把握，喜欢火来比肩副手，有益它的生计。这时候碰着金也难以克胜它，没有金就不会受到危害。 </p> 
<p>论四季之土宜忌 </p> 
<p>春季的土，它的权力最是清幽落寞，所以喜欢火来扶持，害怕木来中断；喜欢土来比肩助力，害怕水来扬波而冲流土。这时候碰着金来制伏木，土就会变患上弱小，但假定金太多过重又会盗泄洋气。 </p> 
<p>夏天的土，它的品性最作枯燥；碰着大水来潮湿它最佳；碰着旺火来烤焦就会更作枯燥，反而受益。木能扶持火势。所以木与火都辨别适土发铺。金能生水，富足的水就可以使夏天的土昌隆；这时候碰着土来比肩相助，土就偈弱小，反而有拥塞蹇滞不通之弊。因此，土假定过火弱小，又患上当木来竣事它。 </p> 
<p>秋天的土，土与金母衰子旺（土生金），金太多就会盗泄洋气；木假定太盛就会制伏土；火即便不少也不腻烦，只是水势浩瀚就不不祥了。这能遇土来比肩相助，就可以扶持其发铺；到霜降的时分没有比肩也是没有阻截的。 </p> 
<p>冬季的土，轮廓冰寒概况温暖。碰着弱小的水，土就更好；金假定太多，土也会变患上更加贫贱。火太盛只能使土更兴隆，木多也不盘曲。这时候能碰着土来相助就更好了。那就身段强壮更加短折。 </p> 
<p>论四季之金宜忌 </p> 
<p>春季的金，身上所余的冷气还未消绝，贵在有火气来使之发铺、兴隆；这时候的金身段赢弱品性柔嫩，进展掉掉落土来匡助才好。水太多金就会变患上冰寒，原先有用也便是无用；木假定太盛，金就随意马虎被折断，原先最刚硬的也变患上不刚硬了。金来比肩匡助，就最爲快乐了，但比肩而没有火，获患上同类也不是好的。 </p> 
<p>夏天的金，更加微弱虚弱，形体以及内质都未发铺十足，这时候更害怕身段变患上健康。弱小的水以夏天的金是不祥的，但火多了却不好。碰着金来扶持，就会使它更坚精、坚固。碰着木那等于助鬼伤身。土太厚就会隐藏金的光泽，土薄些对金的发铺才无益。 </p> 
<p>秋天的金，正是掉势的时分。火来修炼金，逐能成爲钟鼎般的好大材，土又来滋养发铺它，反而会使之带有顽浊之气；碰着水就肉体更加鲜艳；碰着木就恰恰砥砺斧削以施威。这时候掉掉落金来相助就变患上更刚强，只是要小心的是过刚强就会随意马虎折断。 </p> 
<p>冬季的金，形体冷凉品性寒僻。木假定太多就难于阐扬斧凿之功；水太盛就难免有使之漂泊的祸害；土可以制伏水，所以碰着土可以使金的身段变患上不那麼冰寒；火来生土，母子（火与土）俩都对金有长处；这时候喜欢金来比肩类聚相匡助，进展官印来温养就更美丽了。 </p> 
<p>论四季之水宜忌 </p> 
<p>春季的水，品性婬滥滔泛。假定碰着土来制伏它，便可贯注横流浩瀚的祸患；假定再逢水来相助，就确定会有崩堤决口的迫害。喜欢金来匡助，但不患上当金太多；进展火来周济，但不患上当火太炎。这时候碰着木便可以潮湿以施功，使之发铺兴隆；没有土来拥塞，水就会散漫开往。 </p> 
<p>夏天的水，轮廓实而内心虚。这时候正逢干涸的时分，所以进展患上遇水来比肩匡助；喜欢金来扶持自身；害怕火太旺太炎；木太盛就会耗泄水气，土太盛过重就会中断水的来源。 </p> 
<p>秋天的水，金与水母子相旺（金生水），碰着金相助水就变患上清莹、澄澈；逢遇茂盛的土，水就会变患上浑浊；火多对水极度有益，只是过火量又不应该。木多也能使水自身兴隆，但也以中以及过度爲贵。假定碰着太多的水，就会增添其浩瀚的忧郁；假定碰着一叠叠的土来拥塞水，才会有清平的情形。这等于所谓"重重见水，增其浩瀚之忧；叠叠逢土，始患上清平之象。" </p> 
<p>冬季的水，正是掉势的时分，，碰着火便可吊销自身的宇冷气。碰着土就有了回宿；金太多阐发水无义，木太盛就阐发水无情（水生木）。这时候水太遥大就喜欢比肩同类来相助，水太盛就喜欢筑土爲堤防。 </p> 
<p>十神是指天干透出之财官印星等，蕴含地支躲干。它们之间的生克干系，也即五行的生克干系。十神偏重人事分析，五行偏重个体禀气份量的轻重，两者相反相成，不成偏废。故章专论与十神有关之性质，随后章节也是有合论有分论，入修者可从中两者间的激情亲热接头。 </p> 
<p>十神相生：正偏财生官杀，官杀生枭印，印枭生日主劫比，劫比生伤食，伤食生正偏财。 </p> 
<p>十神相克：正偏财克枭印，枭印克伤食，伤食克官杀，官杀即日主劫比，劫比克正偏财。 </p> 
<p>十神生或者克，不是见生就吉见克就凶，其好命坏命也不于是生以及克来论，下面举食神生财爲好命，食神制（克）杀异常是好命，避实就虚地指出这一点，不是想把生以及克作繁杂的对比，而是想在入一步的入修以前，不要看克而生畏。 </p> 
<p>凡生克，无论陰陽，一行都可生可克，如甲木可克戊土，也可克已经土；甲木可生丙火，也可生丁火。但甲克戊，甲生丙爲陽克陽，陽生陽，异性相生或者相克力大。 </p> 
<p>凡论命，从十神透出上论生克，其生克气力的大小，则从天干五行的生克合化患上出（还蕴含地元人元的综合结论）。天干无论冲。 </p> 
<p>十神生克与陰陽五行的生克规律同步，是循环相生以及隔位相克的干系。十神生克宜忌：十神生克与五行生克同样既有相生又有相克。此外，当某神过强或者过弱则物极必反，原是生者反不能生，原是克者反受克，这个中的哲理与人之爲人，应从善如流而不应恶贯充斥是同样的事理。 </p> 
<p>在日干患上气、患上地、患上助、患上生与否认出后，身旺身弱已经有个定论了。但终于功能旺到什麼水平，弱又弱到什麼水平？ </p> 
<p>1、瞅日干的阁下。除瞅以上条件，还要瞅日干下坐的是什麼地支，今日干紧贴的日支或者扶或者抑，是喜照旧忌。和日干的左邻右舍，即月干时干的喜忌。若是喜，是旺照旧弱，这样有助于定出日干患上益的份量；若是弱，也可相应打折。再要瞅这些邻舍的喜是被合爲双喜照旧合走了喜，是被天克了照旧地冲了抑或者刑害了。然后才是离患上更遥的别的干支的扶抑喜忌，还须加分或者减分。若是忌，依理作出分析后斟情加减分。 </p> 
<p>2、察瞅其他干支的旺衰实力。年干、月干以及时干区分以该干在月气中所处的旺衰形态，定出量衰，再像日干察瞅邻居干系同样地察瞅该干阁下坐下之干系及其他干支的干系（喜以及忌）。最初综合起来，财的旺衰轻重，印的旺衰轻重......都有了底，用神，可能用神之喜忌扶抑的分寸也就操作节制住了。 </p> 
<p>3、再总瞅彼此干系。若年干透出财，与日干是耗身干系，月干透出是官，与日干是抑身干系，而财官是相生干系，假定日干势单力薄，必身弱。日干的旺衰违面已经讲患上很子细了，那麼财官各自的旺衰轻重鄙人面察瞅其他干支旺衰实力上已经讲了，两家的干系是相生，官的实力又徒增患上多，即日干的气力又要加分，就瞅日干蒙受患了与否。日干强弱隆替以及各方权力至此已经能定夺了。其他瞅法同理。日干五行旺衰断法其理也同出一辙，可独立揣摸，也可彼此参断。日旺日弱的分寸操作节制古书有详细而繁琐的计法，但命局变革无常，光六十年一个花甲就有五十二万多种彻底不同或者有纤细判另外四柱。对初学者来说，首先抓住进门编制，抓住次要矛盾，猜度的目的也就可以到达。从写书的角度来说，假定把一切对象一古脑写出来，大师一见进门有那麼厚厚一本诗人怕会对本人能否操作节制欠缺决心。再从古书的较量争辩法度榜样来说，四柱均衡精细美好一个生扶、中断、调候的手艺本领程度，个中的生克刑合会打破害等由于遥近、旺衰、五行之性刹那万变各各不同，日主患上气的分寸较量争辩反倒难靠患上住了。 </p> 
<p>正官固守 </p> 
<p>正官与日干的干系：正官是中断我（日干）的。是陽干见陰干克，或者陰干见陽干克。正官的本能机能：是美意之管，譬喻人类，必需从命政府与功令管教。正官平常以吉神论。 </p> 
<p>正官的扶抑才华：卫财、生印、抑身、制劫。身强财弱，喜官卫财。身强印弱，正官生印。日干茂盛，正官拘身。日旺劫多，正官制劫。 </p> 
<p>七杀固守 </p> 
<p>七杀与日干的干系：七杀是中断我（日干）的。是陽见陽克，或者陰见陰克。七杀的本能机能：杀身之对手，专以攻身爲尚，若无礼法制裁，必伤其主（日干），故有制（有食神、伤官中断）谓之偏官，无制爲七杀，平常以凶神论。 </p> 
<p>七杀的扶抑才华：耗财、生印、攻身、制劫，日强财弱，七杀耗财。日强印轻，七杀生印。印轻财重，七杀攻身。日强劫多，七杀制劫。 </p> 
<p>正偏财固守 </p> 
<p>正偏财与日干的干系：正偏财受我（日干）中断的。正财是陽干见陰干克，或者陰干见陽干克；偏财是陽见陽克，或者陰见陰克。正偏财的本能机能：是养命之物，大家所欲，但非大家可患上，古今皆然。平常以吉神论。 </p> 
<p>财星的扶抑才华：生官杀、泄食伤，制枭神、坏正印。日旺官杀弱，财生官杀。日旺财弱，财泄食伤。日旺枭神旺，偏财制枭神。日旺正印旺，正财坏正印。 </p> 
<p>正偏印固守 </p> 
<p>正偏印与日干的干系：正偏印是生我（日干）的。正印是陽干见陰干生，或者陰干见陽干生；偏印是陽见陽生，或者陰见陰生。正偏印的本能机能：我之气源。如父母生身之义。正印平常爲吉神，偏印平常爲凶神见食而夺爲枭神之故。 </p> 
<p>正偏印的扶抑才华：生身、泄官杀、御伤、挫食。日弱官杀强，印星泄官杀生身。日弱食伤重，正印御伤，偏印挫食。 </p> 
<p>伤官食神固守 </p> 
<p>伤食与日干的干系：伤食是我（日干）所生的。伤官是陽干见陰干生，或者陰干见陽干生；食神是陽见陽生，陰见陰生。伤食的本能机能：伤见官仗势克之，听凭日干礼法之外，故平常以凶神论；食见杀则能制服，使日干患上于平安无祸，故平常以吉神论。 </p> 
<p>伤食的扶抑才华：泄身、生财、敌杀、损官。身强财官弱，伤食泄身。身强财弱，伤食生财。身弱官杀重，伤食敌杀损官。 </p> 
<p>比劫固守比劫与日干的干系：比劫与我（日干）同类。劫财是陽干见陰干同，或者陰干见陽干同；比肩是陽见陽同，陰见陰同。比劫的本能机能：财之敌。日旺平常以凶神论。比劫的扶抑才华：帮身、任官杀、化泄、夺财。日弱有比劫帮身；日弱有比劫任官杀，日弱有比劫化泄，日旺有比侵夺财。 </p> 
<p>天干透出之十神，在猜度中还被表明爲天分的自然表露，正如五行之性所能代表的人的特点同样。天干透出，地支躲干的财官印等星，是人事生克的标记（地支循躲则含而不露）。在四柱命局中，我中断了你，你就没有了中断他的才华，他便呈现了。这个他，代表了破裂摧毁"你"后现出的"他"的心性。 </p> 
<p>"他"在四柱中是什麼角色？可以这天干，也可以是其他天干。这里其实不准备站在保重日干的角度来论心性，而是指四柱全部均衡中，当呈现一方克另外一方时，另外一方有力再克第三方，在四柱中已经显露了该人（第三方）的特点。既然是逃过灾难而患上生，在四柱均衡中就该当是较无力的一方。伤官星被破裂摧毁而克不了正官，从而正官无机遇呈现。克伤官者，除刑合冲害外，等于正印克伤官。正印不受制于伤官患上以出，其与日主或者扶或者抑的干系就处在很首要的职位，直接或者间接决意贪图着日主的旺衰，时常在成格败格上起着主导感召。 </p> 
<p>十神心性是："破则立"的干系： </p> 
<p>印克伤，伤不克官，正官心性现。 </p> 
<p>枭夺食，食不制杀，七杀心性现。 </p> 
<p>劫争才，才不损印，正印心性现。 </p> 
<p>比夺财，财不克枭，枭神心性现。 </p> 
<p>伤克官，官不制劫，劫财心性现。 </p> 
<p>食制杀，杀不制比，比肩心性现。 </p> 
<p>才损印，印不克伤，伤官心性现。 </p> 
<p>财制枭，枭不夺食，食神心性现。 </p> 
<p>官克劫，劫不破财，正财心性现。 </p> 
<p>杀制比，比不劫财，偏财心性现。 </p> 
<p>如日旺，年干爲才，月干爲印，时干爲伤，财较无力中断了印，印没有了克伤之力，伤不仅本身旺，而且还不受制。那麼，伤官的心性表现无疑。伤官人清傲慢气，连鬼神都敢骂，别说获咎当官的（所以是克官之星）。日旺更是无以复加。此人性格确定坏透了。当官的不敢惹他，连君子都敬而遥之。这个四柱命局中的伤官因身旺而喜。是用神之喜神，行财运，贫贱自然来。但假定伤官旺，而身弱之人会若何如何样样呢？身弱之人异常是伤官心性，只是尽对来说不那麼外露，不随意率性发怒，一旦发怒吓作古焦急鬼。 </p> 
<p>有的人很小就有小要运营才具以及天禀，即便没文明，卖对象秤还没放下话音已经落账报价，既快又准，让人着实信服。这种人每在命局中涌现的是正偏财心性。众命理上讲，财旺克印，印主文，财旺文明就少，这些人不爱读书，早早就出来处事了。这是财克印的寻惯例律，指的是身弱。身旺能胜财，若身旺财少就做不了生意，但印旺读书就好，故进展克印以免劫财。财透象征着美妙，财多财旺象征着密斯缘，故美妙风流但会嫌钱，平常都身财两旺，财爲用神。这是从心性反证命理，兴趣者不妨事在平日生计中多加观测，然后在猜度中结束验证。 </p> 
<p>十神心性 </p> 
<p>正官：代表官位、位置、考试、推选、学位、名誉、职位。女命代表夫缘子缘。男命代表女儿缘。 </p> 
<p>正官心性：正大累坠负责，矜重严峻，循规蹈矩，但易流于古板、抱残守缺，反爲意志不坚。 </p> 
<p>偏官：代表军警武职、法律之业、歹徒官位职级、考试推选等。女命代表夫缘、女儿缘；男命代表子缘。 </p> 
<p>偏官心性：宏放侠义，全力朝上入步，威严机伶，但易流于偏激，叛变王道反爲腐蚀极端。 </p> 
<p>正印：代表位置、权柄、学业、学术、事业、名誉、职位、福寿等，还代表母缘。 </p> 
<p>正印心性：聪慧惨酷，恬淡名利，逆来顺受，但易流于庸碌，欠缺朝上入步，反爲愚钝悲不雅。 </p> 
<p>偏印：代表偏业上之权位，如艺术、演艺、医业、律师、宗教、武艺、闲暇业、顺从业之效果、铺开、职位，还代表偏母缘。 </p> 
<p>偏印心性：精晓精干，应声灵活，多才多艺，但易流于孤傲，欠缺人情，反爲无私冷峭。 </p> 
<p>比肩：代表昆季、冤家、同事、合股事业、争利夺财、克妻克父、义气等。女命代表姐妹缘；男命代表兄弟缘。 </p> 
<p>比肩心性：稳妥坚忍，冒险大胆，全力朝上入步，但易流于孤僻，欠缺合群，反爲孤独寡合。 </p> 
<p>劫财：代表昆季、冤家等，还代表损财、夺财、夺妻、克父、争权夺利、汗漫。女命代表兄弟缘，男命代表姐妹缘。 </p> 
<p>劫财心性：激情亲近坦直，坚硬志旺，残杀不屈，但易流于肓目，欠缺明智，反爲强悍打动。 </p> 
<p>食神：代表福寿、发胖、退休、食禄等。女命代表女儿缘，男命代表子缘。 </p> 
<p>食神心性：温文随以及，待人宽厚，仁慈体恤，但易流于卖弄，欠缺黑白，反爲陈旧懦怯。 </p> 
<p>伤官：倒楣人家、倒楣夫、在职、褫职、进学、复学、掉权、丧位、落选、落榜等，女命代表子缘，男命代表女儿缘。 </p> 
<p>伤官心性：聪明生动，能力横溢，示弱好胜，但易流于任性，欠缺约束，反爲桀傲不驯。 </p> 
<p>正财：代表俸禄、财富、财运、薪资、妻缘等。 </p> 
<p>正财心性：勤恳节流，塌实激入，怨天尤人，但易流于等闲，欠缺朝上入步，反爲微弱虚弱炫目。 </p> 
<p>偏财：代表偏业之财，横财、暴发、中奖、，赌钱，父缘，男命代表妻缘。 </p> 
<p>偏财心性：美妙重情，聪敏缓慢，委靡广大奔放，但易流于塌实，欠缺垄断，反爲浮华风流。 </p> 
<p>以上讲的是"破则立"的干系。还有一种"不破也立"的状况，即当某一天干旺而不破坏，如日元一片比劫，命中无官星，就属于不受克，但比肩的心性也异常表现无遗。这类种状况虽然不可在破（克）的干系，依然具备独旺的与立异常的心性。 </p> 
<p>正官旺衰 </p> 
<p>正官，克我之官星。正者，正派黑暗；官者，管也，具约身引善之能。正官一位透出无偏官（七杀），谓之地道，身旺最贵。若正官过量，克抑过量，羁绊过甚，反显懦怯炫目。而且，官多爲杀，主家计不幸，仕途坏话多厄，若没有印枭来化来救（官生印，泄官气于印，印可生身）更无害有利。正官最怕见伤官，爲祸百端不测灾来，但官多喜伤则另当别论。 </p> 
<p>官星临长生、洗澡、冠带、临官、帝旺之月，无刑冲空破者，官位位置必高，契合公职。官星临衰、病、作古、墓、尽等掉令之地最差，胎养之地次之。宜贯注公职。 </p> 
<p>官现年柱：命喜官星者，在年干上透出主受祖荫力大。年柱指年少，故易少年掉意，且学业佳。这是指后天要素，还须合营后天雀跃的运程综合来瞅，若后天是读书人，但命运不佳，该人读书或者升学之时每受挫，这类状况的人，每在中年以至老岁尾年行运时才无机遇读书或者进修。 </p> 
<p>年干支皆正官，不被合往或者不忌，主出身在相称的家庭，如官宦之家或者外地有职位之家。也指自身有功名职位。 </p> 
<p>官现月柱：月干喜透官星或者官星喜在月支，身爲小弟，受父母心疼，终生少劳苦。爲人正大绝责，重信课本，学业功名能效果，月柱有指父母宫，多指兄弟姐妹。喜官者，主兄弟姐妹有功名福禄。 </p> 
<p>日坐官星：坐下官星主聪慧，具谋事应变力，身旺遇财运发大福。关于男命，坐支爲妻，故爲喜官者，主妻矜重贤慧多助益。关于女命喜官者，爲患上贵夫。 </p> 
<p>时柱官星：时干爲子时支爲女，喜官者，仆从息贤孝有成，自身老岁尾岁尾年患上享晚福。 </p> 
<p>这里的喜官，指身官相称，无非于受克抑此爲不忌官，即能胜官，官爲禄，自然功名有成。凡学命理首先要搞懂搞通喜忌，不然照本宣科地生搬硬套，势必搞巧成拙，贻笑小气。古书每有许几何量理论堆起的履历总结，用精粹的诗句顺唱出来，但不能够将身旺身弱，命喜命忌作爲前提一一写下，后学者确定要小心这个标的目的，活学活用，多检多验。 </p> 
<p>偏官旺衰 </p> 
<p>偏者不正或者非正统；官者，管也。违面讲过，命局有食神以及伤官制克爲偏官；无制者爲七杀。爲排四柱繁杂清楚，往往把有制无制都简写爲杀。 </p> 
<p>偏官一位不宜再见正官，有食神、伤官制者，主智足多谋有声望。食神制杀伤官克杀、合杀不宜多，多则反掉贵爲贱。故四柱七杀以身杀两停又有制爲贵。身旺杀弱财星旺爲好命，反之，身弱杀旺又逢财，清穷困难多厄，主要者遭杀身之祸。已经有偏官不宜再见正官，否则爲官杀混同，灾劫四伏，易犯牢役官司，逆多顺少难成大事且流于君子罪过比喻途，须食神伤官或者制或者合往一官或者一杀。 </p> 
<p>身弱杀旺要靠印来解。如四柱中身杀两停，杀印相生，主功名闻达，事业铺开、文武双全、权重威显。有杀无印爲少气派欠威风，刁滑多情，多愁善感。杀或者官太多，旺即日主，不吉，主脾性微弱虚弱炫目，既萎靡少语又易打动，有财星者，非灾则夭，或者肢体有损。 </p> 
<p>偏官临长生、洗澡、冠带、临官、帝旺官荣贵要。偏官临作古墓尽者，仕途不畅，官禄有损。 </p> 
<p>年柱偏官：生非长子，上有兄姊，或者穷苦家庭。年柱偏官有制，出身甲士武职世家；身弱无制出身繁华歹徒之家。 </p> 
<p>月柱偏官：年干时干有食神伤官制，贵命。 </p> 
<p>日支偏官：匹俦大都性烈坚忍，固执焦躁，。无食神制者，夫妻不睦，再逢冲，多灾多病。有食神制或者逢分化别象，可解。 </p> 
<p>时柱偏官：爲忌神，后世大都难言贤孝。有制者，反生贵子。时干制偏官一位，日元旺有财印星，无冲，大贵之命，多爲镇守边寨的将领，或者威名遥播边关的贵命。 </p> 
<p>正印旺衰 </p> 
<p>印者，玺也，代表权柄、职位、事业、学位等。正印属学术之星。日主弱，官杀旺者，喜印泄官，生扶弱身。印者爲我气之源，生我扶我之星，简称印。 </p> 
<p>日旺印多无制者爲过极，孤冷刑克之命。正印过旺，爲人小器喜迎合，少后世昆裔，见财星方有子。 </p> 
<p>正印临长生，主母亲端方惨酷短折。临洗澡，指自己职业多变革。临冠带，出身名门能显荣达。旺于临官，安泰有贤母。临帝旺，能出重新地。临衰，主终生庞大，家境萧条。临病作古墓尽之地，主母缘薄，身世不高。 </p> 
<p>年柱正印：命中喜印，主生于贫贱家，读书学业隹。月柱正印：心肠惨酷仁慈，聪慧安康，终生少病安适。四柱有偏官正官者可生印，爲厚富之命。四柱无偏财，则印不受克，文章成名。若月支有正印，与日支冲者，主母家零落败落。 </p> 
<p>日支正印：匹俦惨酷仁慈，聪慧狡黠，命中喜印爲多助益。 </p> 
<p>时柱正印：喜印，仆从女惨酷聪慧多贤孝。 </p> 
<p>偏印旺衰 </p> 
<p>偏者，不正或者非下统也。偏印不见食神，又称倒食，偏印见食爲枭神夺食，故简称枭。命有偏印身弱可扶。但见食爲牢役之命。身旺以食神泄秀。命中不忌伤官泄秀，故枭伤可同见。 </p> 
<p>偏印过量无解者福薄、不幸、灾疾或者后世缘薄，唯偏财可解厄逃灾，故有枭多爲忌时见财则喜。正偏印均现者，喜正副业兼操。身旺，四柱有枭另有财星必福贵。命有偏印又见官杀混同爲多成多败之命。 </p> 
<p>偏印临长生，与生母无缘；临洗澡，职业多变继母花俏；临冠带临官帝旺，与生母无缘但铺开副业有所效果。临衰病作古尽，一技在身到处奔忙劳苦，父母缘较少。临墓，作事好头不如好尾虎头蛇尾。临胎地，出身无母。 </p> 
<p>年柱偏印：爲忌神破祖业，损家名，掉家教。 </p> 
<p>月柱偏印：契合偏业铺开，如医界、艺术界、演艺界、闲暇业、顺从业、美容业等。与天月德同柱者，命佳性温以及。 </p> 
<p>日支偏印：爲忌时，男不患上良妻，女不患上良夫。 </p> 
<p>时柱偏印：爲忌时，后世倒楣。不随意马虎成才，不随意马虎涵养。 </p> 
<p>比肩旺衰 </p> 
<p>同我助我，日主健康比能帮身，简称比。 </p> 
<p>四柱比肩多而无制，昆季相争，冤家掉以及，异性缘差，瑰异寡合，迟婚，夫妻不睦。性刚较焦躁，孤傲离群，固执坚强，克父，克匹俦，劳苦不聚财。多性而有忌妒之争。 </p> 
<p>日干弱，喜比助身，财官多，比助身任抑耗。日干旺，有比者喜官杀、食伤、财星抑耗泄，无官星则少后世。 </p> 
<p>比肩临旺地，兄弟姐妹多，好强好胜鄙人级面前不讨巧，官遭排击。倒楣婚倒楣父。临作古墓尽：虽有兄弟，多早分袂。 </p> 
<p>年柱比肩：上有兄姊或者爲养子，有独立分炊倾向，家境穷苦，之前贫穷。 </p> 
<p>月柱比肩：有兄弟姐妹或者养子，有独立倾向，具掌财、理财之特点。 </p> 
<p>日支比肩：婚姻易变，迟婚或者再婚。克匹俦，多曲直优劣黑白。逢冲患上倒楣匹俦及倒楣遥行，客作古分乡。 </p> 
<p>时柱比肩：养子相继，少后世或者后世昆裔。 </p> 
<p>劫财旺衰 </p> 
<p>财爲马，劫财即克财，故称逐马神，或者败财，简称劫。 </p> 
<p>四柱劫财过量，男克妻，夺妻财，妻多病；女掉夫，争夫或者损财难聚财，昆季欠以及，招违信、毁谤。生性坚强，黑白不分，常招怨结怨。干支同爲比劫，克父克匹俦。劫财与偏财同柱，父倒楣，娶再婚密斯，命中喜财若被劫财克破，这破财、损妻、清穷困难。命中喜劫，但官来破，仆从女大都不孝忤逆，或者后世多有灾厄。 </p> 
<p>劫财旺衰形态主事与比肩同。 </p> 
<p>年柱劫财：上有兄弟，喜理财，重义气，婚变或者有异腹昆季。 </p> 
<p>月柱劫财：难聚财，好赌、投机，自信心强，喜饰轮廓，抱不平，有骂人癖。 </p> 
<p>日支劫财：迟婚、婚变或者再婚，男夺妻财。 </p> 
<p>时柱劫财：后世缘薄。经常伤官损子。 </p> 
<p>食神旺衰 </p> 
<p>食神一名爵星，别名寿星简称食。感召在泄身，生财、抑官杀。 </p> 
<p>食神一位，日坐正官，贫贱。干支皆食神，福禄丰厚，但不宜公职，作公同事业吉。女命则有凌夫之嫌。食多爲伤，易后世昆裔女克男人。四柱皆食神，贫命体弱，女堕风尘，只要偏印能救。食几何偏官者，无后世昆裔。食与杀同柱，有掌权之机，但易惹人厌，劳苦，灾厄而少后世昆裔。食神爲干，支有比肩，主亲戚冤家、昆季多助益。食神爲干，支有劫财，主财福之命，遇凶反患上利。食神带劫财、偏印者，寿短。财多者，艳福不浅。 </p> 
<p>食神临长生等旺地或者吉神：福禄之集，多爲福禄寿全之人。临作古尽病败地：福泽少，薄命人。临墓：早夭。 </p> 
<p>年柱食神：受祖上福荫，事业可铺开，以及平福禄 </p> 
<p>月柱食神：月干爲食支爲官，大兴旺之人，宜政界、公职拓铺。月支食神，主身段消瘦以及悦。 </p> 
<p>日支食神：匹俦消瘦，温良随以及，衣禄宽足。 </p> 
<p>时柱食神：老岁尾岁尾年受罪。但食神与偏印同柱主守空房。 </p> 
<p>伤官旺衰 </p> 
<p>伤官与食神同爲秀气之泄星。简称伤。 </p> 
<p>日旺多伤官，效果于宗教、艺术、演艺、武艺等偏业上。再逢财星、发福显荣。无财星，虽巧亦贫命或者虽慧黠但富不悠久。伤无印星，多爲利欲熏心之人。身弱伤官见偏官，凶厄，高山起风云。伤官不见正官偏官爲伤绝，身旺、财旺、印旺，大富大贵之命。但伤官伤绝若无财乃清穷困难之命。伤官多克后世。 </p> 
<p>伤官临旺地，夫克妻，妻克夫，有财者克性小。易受伤，倒楣家人。易犯官司口舌，提拔、褫职等。临衰地，忌妒心强。 </p> 
<p>年柱伤官：祖业招展。年干支皆伤官，寿短或者富不长。颜面易伤。 </p> 
<p>月柱伤官：昆季缘薄，离弃辨别，不敬父母，干支皆伤官，昆季佳耦别离。 </p> 
<p>日支伤官：男伤子，子宜绝。女克夫。 </p> 
<p>时柱伤官：子缘薄，子顽愚不孝。女多子少，晚运痛楚。 </p> 
<p>伤官爲忌神时，现年柱主父母、现月柱主昆季兄弟、现日支主匹俦、现时柱仆从女大都有不全之憾。 </p> 
<p>正财旺衰 </p> 
<p>财，我克耗我之星，财爲养命之源，财多者又怕身弱，如富屋穷汉；身强者能胜任财，但身强又怕无财。只要身财均衡才爲贫贱佳命。简称才，无论旺衰之财均好吃懒做，贪欲不勤，大都与诗书无缘。 </p> 
<p>日旺财旺，世界大亨，带正官，贫贱双全，男命患上妻贤多助。反之，身弱财旺不仅是富屋穷汉，求财辛苦，还主妻掌家权。（女命指婆姑掌家权）。 </p> 
<p>四柱多正财，爲情破财。财多克印倒楣母。财多不清，倒楣文，爲愚命。 </p> 
<p>支躲财爲财丰，透出美妙不聚财。财有财库，（假定乙爲财，其库爲木之未库）逢冲必发，也指男命金屋躲娇，性较小器。 </p> 
<p>命旺有正财又见食神，患上妻贤助。正财与劫财同现，主终生易逢君子而破财、耗财。正财遇旺官旺杀，妻必厌夫，夫怕妻。 </p> 
<p>正财临旺地，日旺则大富，反之非穷即灾。临衰地，少财。 </p> 
<p>年柱正财：身旺，祖上富有，月透官星，生于富 </p> 
<p>贵之家。月柱正财：勤恳节流，父母富有患上双亲荫助。日支正财：患上妻内人致富，遇刑冲撞害则夫妻敦睦。时柱正财：后世富有。 </p> 
<p>偏财衰旺。 </p> 
<p>财无论正偏均爲养命之源，偏财指父亲或者偏妻，横财，偏业之外财等，简称财。 </p> 
<p>身旺财旺官旺，名利双取贫贱双全。身旺有偏财，无刑冲比劫，人世大亨且短折。偏财透天干最忌比劫，既克父又妨妻。干支皆偏财，田园赤手安家立业致富、会当家理财，有女缘，财气佳。女命身弱忌财，大都爲父拖累操烦。 </p> 
<p>偏财坐长生等旺地：主父子或者妻妾后面，患上父财妻财；父妻皆短折且兴旺荣显。临洗澡：好色风流。临墓地：父或者妻妾早亡，临作古尽刑冲：父或者妻妾衰困不顺以至有难。 </p> 
<p>年柱偏财：年干偏财发达乡，但心杂。干支均偏财：少小多爲养子。年干偏财年比劫：父倒楣田园，客作古异方。 </p> 
<p>月柱偏财：年月干偏财均指父掌家权，或者幼爲养子。月偏财时比劫：先富后贫。日支偏财：妾夺妻权，不爱正妻偏幸妾。 </p> 
<p>时柱偏财：日时偏财无刑冲比劫主中老岁尾岁尾年兴旺。 </p> 
<p>四柱命局以用神爲中央，用神健全无力与否，影响人终生的命，用神补充与否，影响人终生的运。所以，用神不仅不成以损伤。而且要生助才好。 </p> 
<p>凡用神之力欠缺，四柱中有生助用神者，或者四柱刑冲撞害用神而能化凶神、制凶神、合往凶神者，就用神所喜的救应。关于命局缺用神的四柱来说，用神所喜之神好比否极泰来、禾苗雨露，令人切齿的救应干系，起补以及救用神的感召。关于命局五行生旺用神不太紧缺的四柱，贫贱悠悠无可置疑，即便利大官也不会有大灾，却能轻举妄动扶摇直上，这才是真实的贫贱命。有一些虽贫贱不及将相，也可身爲一方富绅或者中心长官，清淡顺顺无达起落。但这类四柱真正以及爲贵的比例极小。所以，从四柱中找准用神最紧迫，找出用神，所喜之神也就随意马虎找出了。至于其生扶以及克抑凶神气力的大小，要瞅无力与否。命局没有用神，喜神必需义不容辞地挑重担。但其命要次于第一用神，均衡尚有掉重心，还须凭仗岁运的补充。 </p> 
<p>凶神爲忌神，凡刑冲撞害合往用神或者危害喜神的，即爲忌神。忌神在命局中其灾就大，当忌神加临岁运，用神又在命运透出而有力，犹如槍打出面鸟，首当其冲受忌神克害。忌神在命局透出而无力、克害用神倍凶，其命不吉。 </p> 
<p>用神喜忌主事：正官或者偏官爲喜用神：贵人提扶，公职升官，考试中榜，推选当选，患上位名扬，威扬权显等。爲忌神：官符刑克，监仓之灾，名誉受损，数一数二，枉累管制。正印或者偏印爲喜用神：功成名就，选拔患上权，学术患上利，考试中榜等。爲忌神：身段掉以及，掉位丧权，名誉受损，题名落榜等。比肩或者劫财爲喜用神：夺利患上财，昆季匡助，娶妻纳妾，病除了身愈等。爲忌神：妻财有损，父道倒楣，昆季掉以及，亲友拖累等。食神或者伤官爲喜用神：天喜临门，患上子延寿，后世荣显，能力发扬，怎样升荣休等。爲忌神：后世拖累，身弱多病，提拔免位，进学失业等。正财或者偏财爲喜用神：娶妻纳妾，财利可患上，父荫妻助创业入职等。爲忌神：财多身弱，父妻无助，爲财困扰，患上掉相称等。 </p> 
<p>四柱以正官、正印、正财、食神爲吉神，但假定组合不好，或者偏枯则不吉。反之，四柱以伤官、偏财、偏印、七杀、比劫爲破败之神，但假定组合患上好，能补偏枯之不吉，反而爲吉。所以，用神、忌神是凭据每一个体不同的四柱组合来定的。 </p> 
<p>用神是中以及、均衡命局的关头，是论命造祸福的判别原则。其固守即锄强扶弱，使过旺之五行患上以抑、泄、耗；偏枯之五行患上以生扶，入而任务局强弱、旺衰、冷热趋于中以及、均衡，不致过火不及。 </p> 
<p>怎样从四柱中拔取用神，其取法不外乎扶抑、通关、调候三准绳爲依照。 </p> 
<p>1、扶抑。日干的用神是十神之一。日主以中战争衡爲顺，过火不及均爲命中有病。匡助，指生我之印星扶我，同我之比劫助我。这样命局就趋于辑睦了，克抑，指以克我之官星抑我，我生之食伤泄我，我克之财星耗我。日主健康，命局须匡助时，凭据忌神几何拔取用神。多官杀：取印星爲用神，泄官生身，若无印星则取比劫爲用神，以泄官助身。多财星：取比劫爲用神，抑财助身。若异样劫，则取印星爲用神，耗财生身。多食伤：取印星爲用神，抑食伤生身，故无印星则取比劫爲用神，助身补泄。 </p> 
<p>日主强旺：命局须抑耗泄时，亦凭据忌神几何拔取用神：多印星：取财星爲用神，抑印耗身。若无财星，则取官杀爲用神，抑身。或者取食伤爲用神，泄耗印。多比劫：取官杀爲用神，抑比劫旺身。若无官杀，取食伤爲用神，泄比劫泄旺身若无两者，取财星爲用神，耗比劫耗旺身。 </p> 
<p>2、通关。命局两种五行尽对峙，各有所长，相争之下，兼顾其美，此亦爲病。择其一能使两种五行生化不悖则命局气势魄力流利流通的用神，来补救，谓之通关。火金相战，以土通关；水火相战，以火通关；水火相战，以木通关；金木相战，以水通关。土水相战，以金通关。 </p> 
<p>如水与火不相容，以木爲用神，木泄水生火，五行之性继承爲相生，隔位爲相克，现化无情爲无情，化敌爲友，乃用神之收获也。 </p> 
<p>3、调候。天道有冷热，人采寰宇之气，故离不开冷热燥湿影响。人以生日爲主，月令爲撮要，依日干五行及月支论命局的冷热燥湿。太冷用热医，太热用冷治；过湿用燥医，过燥用湿治。使其适候，谓之调候。 </p> 
<p>夏月生人，无论日干五行爲何，因偏热过燥，四柱离不开五行之水冷湿调候，须以及扶抑一并参断。 </p> 
<p>冬月生人，无论日干五行爲何，因过冷偏湿，四柱离不开五行之火热燥调候，亦须以及扶抑一并参断。 </p> 
<p>年岁之月生人，则冷热适候，湿燥过度，水火不确定插手调候，只论五行生中断化。 </p> 
<p>如日干爲庚金，生于冬月，没有火热，则爲金冷水寒，庚主筋骨，筋骨处死地，气血不通而病痛，以至招致瘫疾。四柱命局如没有火，则爲缺调候。缺就要补，运上能补则爲顺通，到北方火地则是人爲地补，不仅对身段有益，也可理顺行运。此也是解灾的一个方面。 </p> 
<p>四时之未生人也有冷热燥湿之分。 </p> 
<p>五行畅旺各有确定的时分，只要土居地方，贯于八方，没有坚贞的处所，因而在每一个立春、立夏、立秋、立冬四立以前各旺十八天。下节将对补偏的应用从五行生中断化以及十神生中断化方面结束细论。 </p> 
<p>用神五行生中断经细论： </p> 
<p>一，日干弱，多官杀，用神取印星。 </p> 
<p>首先是泄官杀的感召，然后才是化敌爲友，爲我所用。泄，在五行中其理是爲：强金患上水，方挫其锋；强火患上土，方止其焰；强水患上木，方泄其势；强土患上金，方制其壅；强木患上火，方化其顽。（见第二章第二节） </p> 
<p>先挫其锐气，消其气焰，泄其气势魄力，才具谈患上上化而生身。按理说：金能生水，水多金沉；水能生木，木多水缩；木能生火，火多木焚；火能生土，土多火晦；土能生金，金多土变。这是指物及必反。但日干已经很弱，又那麼多官杀克我，光泄其病气欠缺于强身，还需求大补，不仅水不沉金，木不缩水，火不焚木，而且可金水相涵，水木相生，木火透明；；；这鸣矫枉过正。所以，日干弱爲水，克我者爲土，不仅要以金制其雍，还要以金生我身；日干弱爲火，克我者爲水，不仅要以木泄其势，还要以木生我身；日干弱爲土，克我者爲木，不仅要以火化其顽，还要以火生我身；日干弱爲金，克我者爲火，不仅要以土消其焰，还要以土生我身；日干弱爲木，克我者爲金，不仅要以水挫其锋，还要以水生我身。这等于好比一个体内火旺，但又肾陰虚，这对矛盾欠甜头理。而泰西参既泄火又滋陰，从而补救了这对矛盾，这类命理上的通关感召，正是有的放矢，而沉痾配重药，恰这天干弱又多官杀最佳的化解法度榜样，这在西医医治中起到了陰陽均衡而不有偏差的感召。。在四柱中，此用神如强旺，印枭之运即是人终生中最好的运程，不仅没出偏差，而且高官厚禄，权印在握，功名自有。 </p> 
<p>日干弱，又多官杀，在化敌爲友不可的状况下，即是四柱缺用神。要另寻阶梯才具抗衡浩瀚的矛命我身。这第二个用神即是比劫。比劫好比健壮的盾牌，可以起到抗衡克星，帮身护身的感召。凡日干弱又多官杀克、财耗、伤食泄，都是用神弱的默示，用神在命局中能补，十神生中断化组合较好爲之有救，命局中没有，指看喜神能调换用神使用本能机能，再等于靠运补充。日干弱爲木，不胜砍伐，木多爲林，胜伐而不倒；日干弱爲金，不胜熬炼，合金爲百炼成钢；日干弱爲火，不胜歼灭，燎原之火，胜灭而不熄；日干弱爲水，不胜游塞，奔驰之水，胜阻而不干；日干弱爲土，不胜密栽，中原之土，胜栽而不散。在四柱中，日弱官杀旺而用神爲比劫的命局，次于用神爲印星。从运程下往说，印枭之运爲走运用神，是命局中所缺之用神，能补命之欠缺，所以是最好运。比劫之支运只能是第二好运。 </p> 
<p>2、日干弱，多财星，用神首取比劫。 </p> 
<p>日弱财多，好比戴满了珠宝惹起贪财之人起贪婪，可叹没有一副坚固的身段来守住财宝，被抢想夺归，就要靠路人以及冤家帮；若是想夺归，就要无气力拚搏不致于丧掉，不然轻则赊财，重则惹来杀身之祸，落患上人财俱亡。所以比肩、劫财可补身弱财多之欠缺，以对抗来犯。以上可以瞅出财以及比劫是一对相克的干系，那麼，爲什麼要举这样一个不好的例子？只因身弱财多不仅挑不起财，求财辛苦，而且每在财到手之际同时也孕育了灾难，对这类命局来说，财可能是祸胎。从猜度的良多实例来瞅，当走财旺生财之运时，若命局组合不凶，那麼人格没有成效，财路也广，颇有一些运营个性。但患上财之时不是人仰等于马翻，赔人赔马最初把财都赔出来了事。若命局组合不善，易沦爲赌徒之流。瞅着赌台上大赢特赢的时分，象征着接上往连本带利，以至连夫人一同赔出来。身弱财多之人，总之是爲财掉事，蕴含妻财，这样的命局密斯缘分外好，但却要爲此支付綦重的价格，以至坐牢。那麼什麼时分可胜财？只要当行比劫之运时，方成情形。火，金爲旺财，火旺患上于炼；日干弱爲水，火爲旺财，水多方相济；日干弱爲土，水爲旺财，土多患上于围；日干弱爲木，土爲旺财，木众成绿洲；日干弱爲金，木爲旺财，，金利可削木成材。走比劫运不仅本人升官发家，兄弟姐妹也大获其利，其次是行印枭运。 </p> 
<p>日弱财多，若命局没有比劫，印星即爲替补用神即第二用神。印星与日干是相生的干系。所以，印星首先是起生身的感召。日干太弱又遇忌神财星，其弱之又弱好比雪上加霜，屋漏又逢连夜雨，要想使四柱到达均衡，正如违面所说的非患上矫狂过正不成。这里取用神的各种状况都是出自此理。 </p> 
<p>取印星爲日弱而财多的用神，还可以有耗财之用。财克印，好比这人打那人，这人本身也耗气力。但那人终于挨打，不如比劫帮身可以抗争。等于说，若我身强力壮，就不会需求别人爲我牵联受累。所以印星只能取作第二用神。其气力次于命局有比劫感召神。在运程中，比劫爲最好运，这时候期可成爲大亨，万事顺意，印枭运爲第二好运，还利文途。故日干弱爲金，木财盛，可以土印星爲生身耗财之用；日干弱爲木，土财盛，可以水印星爲生身耗财之用；日干弱爲土，水财盛，可以火印星爲生身耗财之用；日干弱爲水，火财盛，可以金印星爲生身耗财之用；日干弱爲火，金财盛，可以木印星爲生身耗财之用。 </p> 
<p>3、日弱，多食伤，首先要取印星爲用神。 </p> 
<p>印星是生身的，同时又中断忌神食伤，既扶弱又止泄。这同腹泻是一个事理，光止泻弗成，元气已经伤了，还患上直补才行，印星最有资历充任首选用神。故日干弱爲金，食伤之水多，爲过于泄身，以印星之土来制水生身；日干弱爲火，食伤之土多，爲过于泄身，以印星之木来制土生身；日干弱爲木，食伤之火多，爲过于泄身，以印星之水来制火生身；日干弱爲土，食伤之金多，爲过于泄身，以印星之火来制金生身；日干弱爲水，食伤之木多，爲过于泄身，以印星之金来制木生身。 </p> 
<p>若命局中无印星，只能退而求其次取比劫爲用神。不说比劫能何如食伤几许，最少是身子亏患上起。故日干弱爲金，多食伤之水，喜比劫之金帮身；日干弱爲火，多食伤之土，喜比劫之火帮身；日干弱爲木，多食伤之火，喜比劫之木帮身；日干弱爲土，多食伤之金，喜比劫之土帮身；日干弱爲水，多食伤之木，喜比劫之水帮身。 </p> 
<p>以上专论日干弱又逢克、泄、耗的各种状况及所需用神。反之，日干旺，又逢生身帮身，便过于旺了，大师懂患上黄金纯度越高，质地就越软；水到缸边爲满，过了就溢。日过弱之人中气欠缺，从脾性上说不爱多说话，脾性较外向，从后世缘来说，血气欠缺陰陽不均衡不随意马虎有后裔，，，，反之，身旺之人气盛，好胜好争。四柱中，年柱旺不受冲撞指父母身段安康，故其人兄弟姐妹必多，关于身旺之人，这个中的事理是同样的。日干强旺之命局，用神取抑、耗、泄。 </p> 
<p>4、日干强旺，多印星，取财星爲用神。 </p> 
<p>财星用神，既有能挑财患上财之用，又有制日干原神（此指生日干之印星），不致生身过火而劫财。日过问财是相克干系，如若日干已经旺，又患上印星生身爲强旺，财就过弱。金弱遇火，必见销熔；火弱逢水，必爲熄灭；水弱逢土，必爲淤塞；土弱逢木，必爲倾陷；木弱逢金，必爲砍折。故日干旺爲火，又患上木之印星生身更强旺，用神取金财可制印星木，耗日强旺之身；日干旺爲水，又患上金之印星生身更强旺，用神取火财可制印星金，耗日强旺之身；日干旺爲土，又患上火之印星生身更强旺，用神吊水财可制印星火，耗日强旺之身；日干旺爲木，又患上水之印星生身更强旺，用神取土财可制印星水，耗日强旺之身；日干旺爲金，又患上土之印星生身更强旺，用神取木财可制印星土，耗日强旺之身。 </p> 
<p>日干强旺多印星却没有财，命局就缺用神，第二用神可取官杀爲用神，其可取的地方在于克抑强旺之身。其实，取官杀只宜印星不旺的状况下，若太旺了，官生印的生身感召会过火官克身的用场，忌神就帮倒忙了。这类活用之法须在缓缓融会以及理论中掉掉落。当日干旺爲金，又有土印生身更强旺，取火之官星克金身；日干旺爲火，又有木印生身更强旺，吊水之官星克火身；日干旺爲土，又有火印生身更强旺，取木之官星克土身；日干旺爲木，又有水印生身更强旺，取金之官星克木身；日干旺爲水，又有金印生身更强旺，取土之官星克水身。 </p> 
<p>假定既无财星官杀爲用神，又是助旺印生身的话则不成取，当取食伤爲用神。其感召是泄日旺之身，耗强旺之印，因印是克食伤的，所以要靠耗其身旺之原神求患上命局大幅度地扯平。当日干旺爲金，又有土旺爲印星使身更强旺，可以水食伤来补救；日干旺爲火，又有木旺爲印星使身更强旺，可以土食伤来补救；日干旺爲土，又有火旺爲印星使身更强旺，可以金食伤来补救；日干旺爲水，又有金旺爲印星使身更强旺，可以木伤来补救；日干旺爲木，又有水旺爲印星使身更强旺，可以火食伤来补救。 </p> 
<p>5、日干强旺，多比劫。共三种状况。 </p> 
<p>首先，比劫是耗财之神，不中断比劫无从养命，更没法以财生官求贫贱繁荣。所以，官杀是制比劫的第一用神，命局有官或者杀，不仅可抑透出天干的比劫，还可克月令之禄刃。由于身旺是指天干比劫帮身或者印星生身过火，二是指日干应时，应时指日干在月支中临长生洗澡冠带临官帝旺之地，而且地支中特别是月支中，日干处临官之地时爲建禄。如日干爲甲，其禄爲寅，寅是甲的地元同类比肩，较之其他更有躲于人元之本气；其刃爲卯，卯是甲的地元同类劫财，月支中也加躲人元之本气。至于羊刃，爲凶神恶煞。羊刃者，羊言刚，刃取朋分之义，禄过则刃生，功成当退不退，则过越其分，如羊之在刃，言有伤也。既成而未极则爲福，已经极则反爲凶，羊刃正处于十干极盛之地，陰陽万物之理皆恶极盛，当其极处，火则焦灭，水则涌竟，金则折缺，土则坍毁，木则摧折。日旺也蕴含地支中年支、日支、时支中的禄、刃，但月令爲禄爲刃那真是穷善良极了。咱们在猜度中有这样一对例子，都是二十多岁的男青年，都是一片羊刃在地支，月令等于羊刃。这类命局做父母的有几何心都不敷操的，个中一个三天中间在里面爲冤家两肋插刀，遍身是伤屡犯官司，父母到处托人解救......别说到败运，等于流年遇羊刃都随时可以掉事的；另外一个照理也是这类状况，但由于算命教师煽动其从军，严明的队伍纪律制约他的特点，其羊刃的刚暴天分转化爲尽不听命的唆使员实质而连连进级。在五行中，日干旺爲强金，首取火之官星爲用神；日干旺爲强火，首取木之官星爲用神；日干旺爲强土，首取木之官星爲用神；日干旺爲强木，首取金之官星爲用神；日干旺爲强水，首取土之官星爲用神。 </p> 
<p>若身旺无官杀，次取食神爲第二用神，食伤可泄身旺，同时也可泄月令之旺气。食伤有生财之功，并且无官杀就不克第一用神。故日干旺爲金，无火之官星制抑，次吊水之伤食爲用神；日干旺爲火，次取土之伤食爲用神；日干旺爲土，无木之官星制抑，次取金之伤食爲用神；日干旺爲水，无土之官星制抑，次取木之伤食爲用神；日干旺爲木，无金之官星制抑，次取火之伤食爲用神。 </p> 
<p>借使身旺既无官杀又无食伤，那麼，这样的命局少了二行，只剩印星比星以及财星三行，实属格外极度偏枯，除财星就无药可救了。假定真是无药可救的四柱，那确定养不活或者早夭之命，所以不存在第四种状况。 </p> 
<p>五行有燥、湿之分，四季有热、冷之别。命局炎燥喜津润；命局冷湿喜热燠。此是专爲冬月夏月所人命局开具的补气之良方，调候之用神。 </p> 
<p>卯爲春天之纯木，酉爲春天之纯金，年岁仲月，冷热适中，故无理解理睬燥湿之分。子爲纯水，水当然爲湿；丑中己、辛爲湿土、湿金，因丑中躲癸水之故；寅中甲、戊爲燥木、燥土，因寅中有丙火的缘故原由；辰中的戊、乙爲湿土湿木，因辰中躲癸水之故；己中的庚、戊爲燥金、燥土，因己中躲有丙火的缘故原由；午中的己爲燥土，因午中躲有丁火之故；未中的己、乙爲燥土、燥木，因未中躲有丁火之故；申中的庚、戊爲湿金、湿土，因申中躲有壬水之故；戌戊、辛爲燥土、燥金，因戌中躲有丁火之故；亥中的甲爲湿木，因亥中躲有壬水之故。 </p> 
<p>土虽克水，但命局假定水过旺而浩瀚成灾，倘见辰、丑湿土，不仅不能止水，反而繁殖水势，只因辰爲水库，丑爲水之余气，土虽能泄火，但命局假定火过旺而炎烧爲患，倘见未燥土，不仅不能晦火，反而繁殖火势，只因戌爲火库，未爲火之余气。 </p> 
<p>调候好比天寒要穿衣，天暖要凉同样，用神等于人处身的体温，人的范例体温是37度。气温25度阁下是人体最能承受的摄氏温度，平常临连年岁之际。高于25度，外衣就穿不住，低于25度，穿衬衣就嫌微弱。所以高于常温显露春冬日的到来，命局五行中的火热燠了一切的五行，因而四柱偏热过燥。这样的四柱之人每火气盛，中气足，怕暖，喜欢泅水、冲凉、喝冰水寒饮，这等于个性的调溃散温。命理上的调候，即是对火旺特别这天干爲丙、丁火，患上令而身旺者言，命局确定要有水来调候，利南方水旺之地。这里的南方次要指长江以北，再一个是指父亲身世地的北边。由于每一个体的四柱信息都带有遗传基因，若已是长江以北生人，那麼便以祖籍（指父亲出身地）爲准的南方之不调候，经去后天的人爲雀跃，确定比不知调候者顺达许多。衣着也以黑色爲好，因水代表南方、代表黑，其全部气场信息都患上益于水的调候，用神使劲自然有益无弊，命忌生火的西方之木以及身旺之地北方火，须水调候的命局如没有水，四柱再均衡也是五行有缺（通关用神的四柱不确定五行俱全，而用神仍能无力；调候用神缺之病重）。但瞅运中天干庚辛壬癸，地支申酉戌亥子丑之运能否补济，有否合水局，会水方之救。患上遇便瓮中之鳖，似久旱逢雨露，不遇则差矣。 </p> 
<p>低于常温标记住夏季以及到来。命局五行中的水旺，等于偏冷过湿。这样的四柱之人，脾性不确定弱，气也还足，虽然四柱日旺于水，身旺即是元气足的象征，但过旺则另当别论。水旺，特别这天干爲壬癸水，患上令而身旺者，少数照旧惧冷，肾虚是过旺反致虚。这样的命局确定要用火来调候。特别是癸酉日生人是金神日，身旺往北方真是金神进火乡，贫贱世界响。水盛之人还可以西方木来泄水生火，所以命局有、运程喜甲乙丙丁寅卯辰巳午未之地爲调到了火候。调候用神与通关用神是帮手扶抑用神的，推命还须生扶用神爲主。 </p> 
<p>日弱生扶过火或者日旺克抑过火若何如何样办？借使匡助过火。中断其匡助的五行，也可称爲用神，其准绳于是于四柱均衡无益爲准。譬喻，木弱就有水来匡助它，水等于用神，水匡助过火就用土来把握水。土等于均衡四柱的用神。如木弱靠水匡助而又匡助过火，未等于印太多而致身旺，但日干到底是处健康以至是作古墓尽地。所以，再多的生扶也不会强过日干原先就患上令又患上印旺生身的强旺。日干由弱变强的状况下，以用神制印以免过于生身是对的，但也不用过火。日弱生扶过火的用神与身旺印旺的取用神法分比喻。 </p> 
<p>日弱帮身过火而致身旺，是命局中碰着的第二种状况，其用神与日旺比劫旺取用法同样，于是官杀爲用神。但日弱不患上令，再帮身也不会像原先就日干患上令又比劫旺助的情形，所以其用神官杀的感召不会要求患上太剧烈，点到爲止。 </p> 
<p>反之，木强，就用金来中断它，金应是木的用神，金中断患上过火，就用火来把握金，火等于木的用神；金中断患上不敷，就用土生金，土等于用神。 </p> 
<p>身强官杀更强，实践上等于没有印通关，身略弱。制官杀者爲食伤，而感召神的伤食的分寸定要操作节制好。由于食伤不仅制官杀，还泄身。所以，用神食伤不宜过旺。此伤食爲救应用神实践上等于官多喜伤。 </p> 
<p>身强官杀弱即是中断患上不敷，希财来生官，这个用神财星亦不能过旺，由于官杀不是没有，只是还差点情形而已经，不然针对变成身弱不胜财官而掉衡生灾。以上取用神法平常以无非扶抑爲准绳，也即扫数均衡中的分外状况的取用神法。算命教师在用姓名五行爲人补充时，素日酌作爲用神的份量。例如有人名字前须加三个水，爲涛、海，指水多多益善，有些只取露，细雨，稍加滋养，等于这个事理。若有人刨根问底：借应用神的用神被克、合、冲、刑或者有力若何如何样办？这等于其余一种命局了。五行生克是循环相生、隔位相克的干系，关健点是必定身旺身弱，然后取最间接最能均衡命局的用神。用神之用神后，是不会再取用神了。 </p> 
<p>1、官逢伤。即用神爲正官，忌神爲伤官。 </p> 
<p>四柱有忌神伤官克用神，有正印，便可制伤而护官。故正印是正官的救应。 </p> 
<p>2、官逢杀。即正官用神与偏官混同而不清。 </p> 
<p>四柱爲官要清贵，有五陰干伤官可合往七杀，如乙日干，见丙爲伤，丙可合往辛杀存庚官。另有五陽干劫财也可合往七杀，如甲日干，见乙爲劫，乙可合往庚杀存辛官。故五陽干劫财以及五陰干伤官是往杀留官显文贵的救应。 </p> 
<p>3、官逢刑冲。即地支中的正官用神被刑冲而破坏。 </p> 
<p>当用神被刑受伤，四柱有会有合来化刑。丙日干遇支中子水，子中躲癸干爲正官。正官用神被印刑伤，有亥、未与卯分化局，或者有寅、辰与卯会成方，或者有戌与卯天地，即可合住忌神，救患上正官用神。 </p> 
<p>当用神被打破，四柱异常有合可化冲。如丙日干遇支中子水，子中躲干爲正官，正官用神被午反冲而根底不牢。有未与午天地，即可合住忌神，救患上正官用神。故官逢刑冲合可解救。 </p> 
<p>4、财逢劫。即用神爲财，忌神爲劫财。 </p> 
<p>四柱有忌神劫财克用神，命有食神，便可泄劫财生财星。故食神是财星的救应之一。 </p> 
<p>四柱有忌神劫财克用神，命有官星，便可制抑劫财护财星，故官星是财星又一救应。 </p> 
<p>5、财逢杀。即用神爲财星，忌神爲七杀。 </p> 
<p>四柱以杀泄财气爲忌时，有食神，制杀生财，故食神是用神财星的救应之一。 </p> 
<p>四柱以杀泄财气爲忌时，五陰干伤官可合杀护财，如乙日干，见年爲七杀，丙伤官可合杀救财保财。五陽干劫财，也可合杀护财，，如甲日干，见庚爲七杀，乙劫财可合杀抗克守住财。故当七杀爲忌时，五陰干有伤官以及五陽干的劫财又是护财的救应宝贝。 </p> 
<p>6、印逢财。即用神爲印星忌见财星。 </p> 
<p>四柱印财同见而须往财存印时，有劫财，可制财存印。故劫财是用神救星之一。 </p> 
<p>四柱印财同见而须往财存印时，有合神，合往财星，印星不受克抑而解围。陽日干可合住财星而存印，如甲日干见癸爲印，见已经财爲合。五陰干枭神也可合住正财，都是用财正印的救应。 </p> 
<p>7、食逢枭。即食神爲用神忌见枭神。 </p> 
<p>用之食神不成夺，四柱枭食忌相见，即即是两停也宜从中有制有化，有七杀，可化险为夷，故七杀是用之食神的救应之一。 </p> 
<p>四柱枭神夺食，有财星，也可制枭护食，故偏财也是食神的救应。 </p> 
<p>8、食逢杀印。即食爲用神，忌神爲印星。 </p> 
<p>四柱食神制杀，印来帮倒忙，抑食护杀，有财星，可往印厚食，这鸣道高一尺，魔高一丈。其中的财星即是有印星的状况下用神食神的救应。 </p> 
<p>9、财逢伤杀。即用神爲财，忌神爲七杀。 </p> 
<p>四柱伤官生财，杀来化财爲忌时，有合杀者可护财。五陽干劫财可合杀，如甲日干，见庚爲杀，乙劫合庚杀。五陰干伤官可合杀，如乙日干，见辛爲杀，丙伤合辛杀。故五陽干劫财以及五陰干伤官都是用神财星的救应。 </p> 
<p>10、官逢伤（刃格）。杀逢食（刃格）。即官杀爲用神，伤食爲忌神。 </p> 
<p>四柱官无刃不显，杀无刃不威，忌制服过火。有重印星，可护官或者杀，又能约束伤食，使官或者杀有制有帮又有护，声望不成挡。故肋力之印星是官杀之救应。 </p> 
<p>1一、官逢伤（禄格）。即用神爲官，忌神爲伤。 </p> 
<p>四柱官星有禄，官高位显，最忌伤官。有合伤者可护官星。五陽干条神可合伤，如甲日干见壬爲枭，壬可合丁伤；五陰干七杀也可合伤，如乙日干见辛爲杀，辛可合丙伤。故五陽干等神以及五陰干七杀可合往伤官，成爲用神正官的保卫神。 </p> 
<p>十2、财逢杀（禄格）即用神爲财，忌神七杀。 </p> 
<p>四醉用神爲财不须七杀来化时，有合往七杀者可护财。五陽干劫财可合杀，如甲日干，见庚爲杀，乙劫可合庚杀；五陰干伤官可合杀，如乙日干，见辛爲杀，丙伤可合杀。故五陽干劫财以及五陰干伤官可合杀护财，是用神财星的救应。 </p> 
<p>四柱命局的成败救应，个中的轻重权宜十分活络，可以从以上点到的地方、还可从刑冲撞合救应上触类旁通、意会贯穿。 </p> 
<p>排大运以及起大运岁数，也是推命论运的根柢次第。大运以及起运数排挤后，标出每一步运所行的十神，根蒂根基义务约略完成，另有神煞须标记，下章节再论。四柱爲命，运程爲运，命以及运合爲人终生的命运，命运连系方知祸福。命与运，如船以及水，水能载船亦能覆船。俗云：命好不如运好，运好不如流年好。关于这句话，在初中检讨上，时有命好于运，运好于流年的相反结论。若是流年好，大运不好，流年又能好到那里往？所以，命、运、流年这三者是密不身分的扫数，没有好命，大运于事无补；流年好也贫贱不了，没有好运，命再好也违时，流年好也受到大运不好的规模；没有好的流年，四柱用神脱颖而出，大运虽好，详细应吉之期就不能兑现。大运于是四柱中的月柱来排定的，有男女顺逆之分，起运数较量争辩也有顺逆之别。 </p> 
<p>1、大运顺逆 </p> 
<p>男命逢子、寅、辰、午、申、戌陽支之年，大运以月柱爲准，顺排。如男命生于丙子年，庚寅月，子爲陽年，男命陽年生爲理顺成章，故大运以庚寅爲准顺排：辛卯、壬辰、癸巳、甲午、乙未、丙申、丁酉、戊戌。平常排八步运。排几步运，没有严明轨则，以平常寿数来排，每一步运指每一十年中或者吉或者凶或者平运的福祸水平的趋向。每一步运都是陽过问陽支或者陰过问陰支的组合。 </p> 
<p>女命陽年生爲逆，故大运爲月柱爲准，逆排。如女命生于丙子年庚寅月，子爲陽年，女命逆推，故大运以庚寅爲准逆排：已经丑、戊子、丁亥、丙戌、乙酉、甲申、癸未、壬午。 </p> 
<p>女命丑、卯、巳、未、酉、亥年生，女爲陰，陰年生陰年爲顺，故女命生于陰年大运以月柱爲准，顺排。如丁丑年壬寅月，女命以壬寅爲准排挤大运：癸卯、甲辰、乙巳、丙午、丁未、戊申、已经酉、庚戌。 </p> 
<p>男命逢陰年爲逆，故男生于陰年大运爲月柱爲准，逆排。如丁丑年壬寅月，男命以壬寅爲准逆推出大运：辛丑、庚子、已经亥、戊戌、丁酉、丙申、乙未、甲午。 </p> 
<p>2、起运数 </p> 
<p>大运的初阶有从一岁就步进大运，插手四柱论命运的。从一岁至十一岁的起运数都有。如第一步运爲二岁运，第二步运就爲十二岁运，…..第八步岁就爲七十二岁运. </p> 
<p>大运的起运数无论逆顺均按人的自然年光韶光递增,故无论运干支是顺推逆排,每一步运的起步数均以十年一步顺数递入. </p> 
<p>起运数的起法,以三天折合一岁计,即一天折合四个月,两天折合八个月。较量争辩时，如起运总数爲18天，除了3便是6，即爲6岁起大运；起运总数不能被3整除了时，多一天，即起运总数爲19天，按6岁零4个月计，或者只按6岁计，多两天，即运总数爲20天，按6岁零8个月计，或者按四舍五进按七岁计。 </p> 
<p>起运总数的较量争辩法度榜样。于是出身之日地址的月令，分男女顺逆算出，其顺逆与大运陽年生男命顺推女命逆推，陽年女命顺推男命逆推的排运法度榜样同步。 </p> 
<p>陽年生人，男命以出身之日数起至本月令终了，如寅月生人，其月令爲立春之月，立春终了之时，即惊蛰卯月交时令的前夕。如九四年陰历正月初八生男，陽年生男从初八数廿五日（二十五日立春终了交卯月惊蛰），共18天，除了3便是6，即爲6岁起大运，假定这一天生女，陽年生女从初八逆数至立春日（即陰历九三年十二月二十四日），共十四天，除了3便是4，余数爲2，即爲4岁8个月起大运，可四舍五进按5岁起大运计。 </p> 
<p>假定是陰年生女，其较量争辩法度榜样与陽年生男相反；假定是陰年生男，其起运数的法度榜样与陽年生女相反。读者可以丑、卯、未、酉、亥生年之人演习。 </p> 
<p>3、十神主运 </p> 
<p>大运以及起运数排挤后，每一步运的天干须与四柱命局中的日干论生克，排挤其十神，以便与四柱一同参论，大运十神与四柱透十神以及支躲十神同样从生克患上出。大运十神爲用神所喜即爲好运，大运十神爲用神所忌即爲坏运。当然好到何水平坏到何水平不是笼统的，对他们的组合生克刑冲等干系操作节制的越好，猜度的切确性越高，所测之事也就越强微大白。大运的十神喜忌，又干系到每一年（即流年）的命运诟谇，操作节制住了大运所喜所忌，也就操作节制了命脉，爲才是真正意义上的知命以及操作节制了命运。只要真实地感受到了命运的存在，才具谈患上趋吉避凶。将四柱的排法、四柱这出、地支循躲、地支所躲十神，和排大运、起大运数、运干所透十神的整排法示出。至此，四柱命运的根蒂根基才算完成，当前以后的福祸推算都基于此。 <a href="//www.sohu.com/?strategyid=00001%20" target="_blank" title="点击进入搜狐首页" id="backsohucom" style="white-space: nowrap;"><span class="backword"><i class="backsohu"></i>返回搜狐，查看更多</span></a></p>      <!-- 政务账号添加来源标示处理 -->
      <!-- 政务账号添加来源标示处理 -->
      <p data-role="editor-name">责任编辑：<span></span></p>
</article>


Process finished with exit code 0
'''

def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.replace("\n\n", "{{_changed_}}\n")
    zon = para.split("\n")
    af_zon = []
    for zo in zon:
        zo = zo.replace("{{_changed_}}", "\n")
        af_zon.append(zo)
    return af_zon

# print(cut_sent(contents))

url = 'http://www.sohu.com/a/280633415_100204322'
res = requests.get(url)
tree = html.fromstring(res.text)
name = tree.xpath('//article[@id="mp-editor"]')
name1 = html.tostring(name[0])
name2 = htmls.unescape(name1.decode('gbk'))
print(name2)