#!/usr/bin/env python
# coding=utf-8
from requests_toolbelt import MultipartEncoder
from DBUtils.PersistentDB import PersistentDB
# from multiprocessing import Process
# from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue
from urllib.parse import quote
from urllib import parse as up
from threading import Thread
import datetime
from hashlib import md5
from lxml import etree
from PIL import Image
import multiprocessing
import requests
import pymysql
import random
import redis
import time
import json
import os
import re

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

# 获取url和关键字
class MySQL_My(object):
    def __init__(self):
        # self.host = 'ymhack.wicp.net'
        # self.user='python_gather'
        # self.pwd ='ebe1bc4806'
        # self.dbname = "python_gather"
        # self.port = 13306
        config = {
            "host": "ymhack.wicp.net",
            "port": 13306,
            "user": "python_gather",
            "password": "ebe1bc4806",
            "database": "python_gather"
        }
        db_pool = PersistentDB(pymysql, **config)
        # 从数据库连接池是取出一个数据库连接
        self.conn = db_pool.connection()
        self.cursor = self.conn.cursor()


    def updateDate(self,id,args,webid=1):
        try:
            # conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname,port=self.port)  # 连接数据库
            # cursor = conn.cursor()  # 获取游标
            if not args:
                sql = 'update mainurl set `date`=NOW(),`isActivate`=1 where id=%d'%id
                self.cursor.execute(sql)
                sql = 'UPDATE webnumber set numb= numb + 1 where id="%d"' % webid
                self.cursor.execute(sql)  # 执行
                self.conn.commit()
            else:
                sql = """INSERT INTO `errmainurl` (`TITLE`,`URL`,`WEB_ID`,`IDS`,`describe`) VALUES (%s,%s,%s,%s,%s)"""
                self.cursor.executemany(sql, [args])
                self.conn.commit()
        except Exception as e:
            pass
            # print('修改数据库 url 时间失败：{}，ID：{}'.format(e,id))
        finally:
            pass
            # self.cursor.close()  # 关闭游标
            # self.conn.close()  # 关闭连接

    def select_webname(self):
        # conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname,port=self.port)  # 连接数据库
        # cursor = conn.cursor()  # 获取游标
        result =False
        try:
            sql = "select `name` from webnumber"
            self.cursor.execute(sql)  # 执行
            result = self.cursor.fetchall()  # result是元
        finally:
            pass
            # self.cursor.close()  # 关闭游标
            # self.conn.close()  # 关闭连接
        return result

    def select_global(self):
        # conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port)  # 连接数据库
        # cursor = conn.cursor()  # 获取游标
        result = False
        try:
            sql = "select title,parameter,isActivate from globalsetting"
            self.cursor.execute(sql)  # 执行
            result = self.cursor.fetchall()  # result是元
        finally:
            pass
            # self.cursor.close()  # 关闭游标
            # self.conn.close()  # 关闭连接
        return result

    def xpath(self):
        xpath_l = {}
        # conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname,port=self.port)  # 连接数据库
        # cursor = conn.cursor()  # 获取游标
        try:
            # 查询网站数量
            sql = "select webdoma,xpath from contentxpath"
            self.cursor.execute(sql)  # 执行
            result = self.cursor.fetchall()  # result是元
            for webdoma,xpath in result:
                xpath_l[webdoma] = xpath
        except Exception as e:
            print('查询 采集路径错误 ')
        finally:
            pass
            # self.cursor.close()  # 关闭游标
            # self.conn.close()  # 关闭连接
        return xpath_l

    def mainurlzeor(self,id):
        # conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port)  # 连接数据库
        # cursor = conn.cursor()  # 获取游标
        try:
            sql = "update mainurl set isActivate=0  where id=%d"%id
            self.cursor.execute(sql)
            self.conn.commit()
        finally:
            pass
            # self.cursor.close()  # 关闭游标
            # self.conn.close()  # 关闭连接

# redis 操作
class Redis_my(object):
    def __init__(self):
        self.r = redis.Redis(host='ymhack.wicp.net',port=16379,db=0,decode_responses=True)
        self.pipe = self.r.pipeline()  #减少对服务器的请求数  #减少服务器客户端之间连接损耗

    def webname(self):
        webnames = MySQL_My().select_webname()
        webname_list =[]
        if webnames:
            for webname in webnames:
                webname_list.append(webname[0])
            return webname_list

    def select(self,webname_list):
        all_list = {}
        for webname in webname_list:
            if self.r.llen('await:'+str(webname)):
                all = []
                for item in range(50):
                    try:
                        info = eval(self.r.lpop('await:' + str(webname)))
                    except:
                        continue
                    if self.de_weight(webname, info[8]):
                        continue
                    all.append(info)
                all_list[webname]=all
        return all_list

    def de_weight(self,webname,url):
        # print('查询 redis 已发布成功的数据: webname:{}, url:{}'.format(webname, url))
        key = get_md5(url)
        value = self.r.hget(name='issue:'+str(webname),key=key)
        return value

    def set_hash(self,webname,url):
        # print('插入 redis 已发布成功的数据: webname:{}, url:{}'.format(webname,url))
        self.r.hset(name='issue:'+ str(webname),key=get_md5(url),value=1)

# 下载保存图片
class Down_Compressimg(object):
    def get_size(self,file):
        # 获取文件大小:KB
        size = os.path.getsize(file)
        return size / 1024

    def get_outfile(self,infile, outfile):
        if outfile:
            return outfile
        dir, suffix = os.path.splitext(infile)
        outfile = '{}-out{}'.format(dir, suffix)
        return outfile

    def compress_image(self,infile, quality=50):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param outfile: 压缩文件保存地址
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """
        # o_size = self.get_size(infile)
        # if o_size <= mb:
        #     return infile
        # outfile = self.get_outfile(infile, outfile)
        # while o_size > mb:
        im = Image.open(infile)
        im.save(infile, quality=quality)
        # if quality - step < 0:
        #     break
        # quality -= step
        # o_size = self.get_size(outfile)


    def resize_image(self,infile, outfile='', x_s=1376):
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

    def getPage(self,keyword,page=30):
        keyword = up.quote(keyword,safe='/')
        url_begin = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='
        url = url_begin + keyword +'&pn='+str(page) + '&gsm='+str(hex(page)) + '&ct=&ic=0&lm=-1&width=0&height=0'
        return url

    def get_onepage_urls(self,onepageurl):
        try:
            html = requests.get(onepageurl,headers={'User-Agent': User_Agent().random()},proxies=get_ip()).text
        except Exception as e:
            print(e)
            pic_url = []
            return pic_url
        pic_url = re.findall('"objURL":"(.*?)"',html,re.S)
        return pic_url

    def down_pic(self,pic_urls,title,quality=80):
        Flag = False
        for i,pic_url,in enumerate(pic_urls):
            try:
                pic = requests.get(pic_url,headers={'User-Agent': User_Agent().random()},timeout=15,proxies=get_ip())
                string = 'files/'+str(int(time.time())) + "_" + str(random.randint(1000, 9999)) + '.png'
                with open(string,'wb') as f:
                    f.write(pic.content)
                    print('成功下载图片%s'%pic_url,get_nowtime())
                    Flag= True
                if Flag:
                    time.sleep(1)
                    try:
                        im = Image.open(string)
                        im.save(string, quality=quality)
                    except:
                        continue
                    return string
            except Exception as e:
                print('下载图片出错,%s'%str(pic_url),get_nowtime())
                print(e)
                continue

    def run(self,keyword):
        url = self.getPage(keyword)
        ongpage_urls = self.get_onepage_urls(url)
        file_path_img = self.down_pic(set(ongpage_urls),keyword)
        if file_path_img:
            return file_path_img
        return False

def get_nowtime():
    nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#现在
    return nowTime
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

# 加密
def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    m = md5()
    m.update(text)
    return m.hexdigest()

    # 句子切割
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

minNumberWords = 0
minNumberWordsisActivate=False  # 检查文章最少字数 默认关闭
formattedText_query = Queue()  # 文章整合队列
key_url_query = Queue()  # url 队列
content_query = Queue()  # 网站抓取的文章 队列
content_google_query = Queue()  # 谷歌翻译后的文章队列
xpathcont = MySQL_My().xpath()
webNameListRedis = Redis_my().webname()

def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)

def randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return strTimeProp(start, end, random.random(), frmt)

def run():
    ''''''
    flag = False
    key_url_list = Redis_my().select(webNameListRedis)
    if key_url_list:
        globalSttines = MySQL_My().select_global()
        if globalSttines:
            for item in globalSttines:
                if item[2] and item[0] == '文章最少字数':
                    global minNumberWords,minNumberWordsisActivate
                    minNumberWords = item[1]
                    minNumberWordsisActivate = True

        for redis_name in key_url_list:
            for webid, img_isActivate, column, author, weblink, describe, isActivateTime, id, title, url, isActivate,ratioimg in \
            key_url_list[redis_name]:
                key_url_query.put(
                    [webid, img_isActivate, column, author, weblink, describe, id, title, url, redis_name,
                     isActivateTime,ratioimg])
        flag = True
    else:
        print('reids中没有 url链接',get_nowtime())
    return flag

def crawlers():
    '''爬虫函数'''
    while True:
        data = ''
        try:
            if not key_url_query.empty():
                #  webid,img_isActivate,column,author,weblink,describe,id,title,url,redis_name,isActivateTime,ratioimg= key_url_query.get(block=True,timeout=60)
                data = key_url_query.get()
                print('爬虫函数', data,get_nowtime(),get_nowtime())
                try:
                    res = requests.get(data[8],
                                       headers={'User-Agent': User_Agent().random()},
                                       proxies=get_ip(), timeout=60)
                except:
                    MySQL_My().mainurlzeor(data[6])
                    # continue
                if res.status_code == 200:
                    webdoma = up.urlparse(data[8])[1]
                    html = res.text
                    html = etree.HTML(html)
                    for xpa in xpathcont[webdoma].split(','):
                        content_ls = html.xpath(xpa)
                        if not content_ls:
                            continue
                        else:
                            break
                    if not content_ls:
                        # print(data[8],'未匹配到文章数据',xpa)
                        MySQL_My().updateDate(data[6], (data[7], data[8], data[0], data[6], '未匹配到文章数据'))
                    else:
                        data.append(content_ls)
                        content_query.put(data)
            # else:
                # break
                # time.sleep(2)
        except requests.exceptions.ConnectTimeout:
            print('url get请求,超时',data[2])
            MySQL_My().updateDate(data[6], (data[7],data[8],data[0],data[6],'url get请求,超时'))
        except:
            if data:
                print('爬虫函数发生错误', data[8])
                MySQL_My().updateDate(data[6], (data[7],data[8],data[0],data[6],'爬虫函数发生错误'))
            else:
                # print('爬虫函数为空')
                time.sleep(20)
        time.sleep(3)

def formattedTextPool():
    while True:
        try:
            if not content_query.empty():
                data = content_query.get()
                # t_start = time.time()
                print('整合文章句子,ID：', data[0:8], os.getpid(),get_nowtime())
                content = []
                sentence = ''  # 整合的句子小于800
                amount = 0  # 文字总量
                for texts in data[-1]:
                    lent = len(texts)
                    lens = len(sentence)
                    if not texts:
                        continue
                    if lent > 800:
                        # 大于800字开始切割
                        # 将文章打散成句子
                        text_ls = cut_sent(texts)
                        # 开始创建数据队列
                        for i, text_s in enumerate(text_ls):
                            if len(text_s) + lens < 800:
                                sentence += text_s
                            else:
                                # sentence 接近800字, 添加进列表,并分段,重置
                                content.append('\r\n\t' + sentence)
                                amount += lens
                                sentence = ''  # 整合的句子小于800
                    elif lent + lens < 800:
                        sentence += texts
                    else:
                        # sentence 接近800字, 添加进列表,并分段,重置
                        content.append('\r\n\t' + sentence)
                        amount += lens
                        sentence = ''  # 整合的句子小于800
                content.append('\r\n\t' + sentence)
                amount += len(sentence)
                # 判断文章字数是否达标
                if minNumberWordsisActivate and int(amount) < int(minNumberWords):
                    # return
                    continue
                data[-1] = content
                # print(data)
                formattedText_query.put(data)
                # t_stop = time.time()
                # print("%s执行完成，耗时%.2f" % (os.getpid(), t_stop - t_start))
                # return data
        except:
            print('%s进程发生错误'%os.getpid(),get_nowtime())

def contnt_google():
    '''将爬虫获取到的content 通过谷歌翻译'''
    while True:
        data = ''
        try:
            if not formattedText_query.empty():
                # webid,img_isActivate,column,author,weblink,describe,id,title,url,redis_name,isActivateTime,content = content_query.get(block=True,timeout=60)
                data = formattedText_query.get()
                print('翻译文章ID：', data[0:8],get_nowtime())
                content = ''
                for texts in data[-1]:
                    content += '\r\n\t' + google_(texts)
                if not data[-2]:
                    random_time = int(time.time())
                else:
                    now_time = int(time.time())
                    time_array = time.localtime(now_time)
                    start = time.strftime("%Y-%m-%d 00:00:00", time_array)
                    end = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
                    random_time = randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S')
                if data[1]:
                    # 获取随机比例
                    randint_data = random.randint(1, 10)*10
                    if randint_data <= int(data[11]):
                        # 下载图片,返回路径
                        img_path = Down_Compressimg().run(data[7])
                        # 上传图片 API
                        # add_article_url = '{}/apis.php?act=upload_Img'.format('http://1.zhituicloud.com')
                        add_article_url = '{}/apis.php?act=upload_Img'.format(data[4])
                        # 上传图片
                        try:
                            img_src = upload_img(add_article_url, img_path)
                            img_html = '<img src="%s" alt="%s">\n' % (img_src, data[7])
                            content += img_html
                        except:
                            print('上传图片失败',get_nowtime())
                payload = {
                    "log_CateID": int(random.choice(data[2].split(','))),
                    "log_AuthorID": int(random.choice(data[3].split(','))),
                    "log_Tag": "",
                    "log_Status": 0,
                    "log_Type": 0,
                    "log_Alias": 0,
                    "log_IsTop": 0,
                    "log_IsLock": 0,
                    "log_Title": data[7],
                    "log_Intro": '',
                    "log_Content": content,
                    "log_PostTime": random_time,
                    "log_CommNums": 0,
                    "log_ViewNums": 0,
                    "log_Template": "",
                    "log_Meta": "",
                }
                data[-1] = payload
                content_google_query.put(data)
            # else:
            #     break
            # #     print('谷歌翻译函数为空')
            time.sleep(3)
        except requests.exceptions.ProxyError:
            print('谷歌代理IP错误 :', data[8],get_nowtime())
            MySQL_My().updateDate(data[6], (data[7], data[8], data[0], data[6], '谷歌翻译函数 代理 IP 错误'))
        except:
            if data:
                print(data[5], '谷歌翻译函数发生错误',get_nowtime())
                MySQL_My().updateDate(data[6], (data[7], data[8], data[0], data[6], '谷歌翻译函数发生错误'))
            # else:
            #     print('谷歌翻译函数为空')
            #     time.sleep(20)
        # time.sleep(5)

# 上传图片
def upload_img( url, img_path):
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
        print(response_text)
        print('上传文件失败',get_nowtime())
    # else:
    # if (os.path.exists(img_path)):
    #     os.remove(img_path)
    #     print('文件上传成功，已删除本地文件：%s' % (img_name))
    img_link = response_text
    return img_link

# 开始上传文章。
def push_article():
    '''上传文章函数'''
    while True:
        data = ''
        try:
            if not content_google_query.empty():
                # webid, img_isActivate, column, author, weblink, describe, id, title, url, content_ls, redisName,content = content_query.get(block=True,timeout=60)
                data = content_google_query.get()
                print('上传文章:', data[0:11],get_nowtime())
                # if data[1]:
                #     # 下载图片,返回路径
                #     img_path = Down_Compressimg().run(data[7])
                #     # 上传图片 API
                #     add_article_url = '{}/apis.php?act=upload_Img'.format(data[4])
                #     # 上传图片
                #     img_src = upload_img(add_article_url,img_path)
                #     img_html_1 = '{{/content}}<img src="%s" alt="%s">\n{{title}}' % (img_src, data[7])
                # else:
                add_article_url = '{}/apis.php?act=article_Api'.format(data[4])
                # add_article_url = '{}/apis.php?act=article_Api'.format('http://1.zhituicloud.com')
                # 织梦会话ID
                headers = {'Content-Type': 'application/json'}
                response = requests.request("POST", add_article_url, data=data[-1], headers=headers)
                if "success" in response.text:
                    # if response.status_code == 200:
                    print("网站：%s，成功发布文章：%s" % (data[9], data[7]),get_nowtime())
                    MySQL_My().updateDate(data[6], False, data[0])
                    Redis_my().set_hash(data[9], data[8])
                else:
                    print("网站：%s，文章发布失败: %s" % (data[9], data[7]),get_nowtime())
                    print(response.text)
                    MySQL_My().updateDate(data[6],
                                          (data[7], data[8], data[0], data[6], '发布失败,{}'.format(response.text)))
            # else:
            #     break
            #     print('上传文章管道为空')
            # time.sleep(5)
        except:
            # if not data:
            #     time.sleep(20)
            print('上传文章函数发生错误',get_nowtime())
            # time.sleep(60)
        time.sleep(5)

def google_(content):
    trans = google_trans(content)
    af = trans.trans()
    # t_sp = random.uniform(0, 2)
    return af

def formattedText():
        '''将爬虫获取到的content 通过
        data :　redisName, webid, img_isActivate, column, author, weblink, describe, id, title, url, content_ls
        '''
        po = multiprocessing.Pool(5)
        #webid,img_isActivate,column,author,weblink,describe,id,title,url,redis_name,isActivateTime,content = content_query.get(block=True,timeout=60)
        # for i in range(content_query.qsize()):
        #     data= content_query.get()
        #     po.apply_async(formattedTextPool, (data,))
        # po.close()
        # po.join()
        res = po.map(formattedTextPool,[i for i in range(content_query.qsize())])
        print(res,get_nowtime())


if __name__ == '__main__':
    run()
    # crawlers()
    # formattedTextPool()
    # contnt_google()
    # push_article()
    # while True:
    #     flag = run()
    #     if not flag:
    #         time.sleep(5*60)
    #         continue
    #     with ThreadPoolExecutor(5) as executor:
    #         all = [executor.submit(crawlers,) for i in range(key_url_query.qsize())]
    #     # formattedText()
    #     with ThreadPoolExecutor(2) as executor:
    #         alle = [executor.submit(formattedTextPool,) for i in range(content_query.qsize())]
    #     with ThreadPoolExecutor(5) as executor:
    #         allg = [executor.submit(contnt_google,) for i in range(formattedText_query.qsize())]
    #     with ThreadPoolExecutor(5) as executor:
    #         allp = [executor.submit(push_article, ) for i in range(content_google_query.qsize())]
    c_list = []
    for i in range(5):
        t = Thread(target=crawlers)
        c_list.append(t)
        t.start()
    for i in range(3):
        p = Thread(target=formattedTextPool)
        c_list.append(p)
        p.start()
    for i in range(10):
        t = Thread(target=contnt_google)
        c_list.append(t)
        t.start()
    for i in range(5):
        t = Thread(target=push_article)
        c_list.append(t)
        t.start()
    time.sleep(5)
    while True:
        if content_query.empty() and key_url_query.empty() and formattedText_query.empty() and content_google_query.empty():
            run()
            print('\t\t\t\t\t\t\t\t\t\t获取url链接')
        time.sleep(60)

    # MainCrawler().upload_img('http://1.zhituicloud.com/apis.php?act=upload_Img','1581678455_8536.png')
    # s = Redis_my().de_weight('bxzphz.cn','https://baijiahao.baidu.com/s?id=1603170901791671174&wfr=spider&for=pc')
    # print(s)
    # strat = time.time()
    # print(strat)
    # MySQL_My().run()
    # end = time.time()
    # print('运行时间：',end-strat)

