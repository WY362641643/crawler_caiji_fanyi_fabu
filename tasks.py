# -*- coding: utf-8 -*-
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests
import platform
import random
import socket
import time
import json
import sys
import re
sys.path.append("path")
def get_ip():
    html = ""
    try:
        html = requests.get("http://kuyukuyu.com/agents/get?uuid=e9297c14-a9f4-4cb2-ad23-1456cbbc5ef3").text
    except:
        time.sleep(1)
        html = get_ip()
    print(html)
    return html

# 句子切割
def cut_sent(para):
    para = re.sub('([。！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.replace("\n\n","{{_changed_}}\n")
    zon = para.split("\n")
    af_zon = []
    for zo in zon:
        zo = zo.replace("{{_changed_}}","\n")
        af_zon.append(zo)
    return af_zon
# 获取数据
def sql_task(sql,db_name):
    ip_ = "192.168.0.158"
    url = "http://" + ip_ + "/index.php"
    querystring = {
        "db_name": "信息存贮/" + db_name + ".db",
        "sql_str": sql
        }
    response = requests.request("GET", url, params=querystring)#  headers=headers,
    json_text = response.text
    task = json.loads(json_text)
    return task

# 获取本机的局域网IP
def get_local_ip():
    def getip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('www.baidu.com', 0))
            ip = s.getsockname()[0]
        except:
            ip = "x.x.x.x"
        finally:
            s.close()
        return ip
    ip_address = "0.0.0.0"
    sysstr = platform.system()
    if sysstr == "Windows":
        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address
    elif sysstr == "Linux":
        ip_address = getip()
        return ip_address
    elif sysstr == "Darwin":
        ip_address = socket.gethostbyname(socket.gethostname())
        return ip_address
    else:
        print("Other System @ some ip")

# 获取关键词并改变其任务状态
def get_keyword():
    sql = "select * from task_pool where status='need_crawl' limit 1"
    db_name = "任务池"
    task = re_try(sql, db_name, 1)
    sql = "update task_pool set machine='%s', status='%s' where id=%d" % (get_local_ip(), "crawling", task[0]['id'])
    re_try(sql, db_name, 1)
    return task[0]

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
    def json_get(self,json_text):
        json_ = json.loads(json_text)
        text_zon = ""
        for js in json_[0]:
            if js[0]:
                text_zon += js[0]
        return text_zon
    def conect_html(self,url):
        # try:
        proxy = {
            'https' : 'https://' + self.ip_port,
            'http': "http://" + self.ip_port
            }
        response = requests.get(url, headers=self.headers, proxies=proxy,timeout=60)
        # except:
        #     time.sleep(2)
        #     self.ip_port = get_ip()
        #     re = self.conect_html(url)
        #     return re
        # else:
        return response.text
    def trans(self):
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q=" + quote(self.content)
        json_text = self.conect_html(url)
        text_af = self.json_get(json_text)
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=" + quote(text_af)
        json_text = self.conect_html(url)
        text_af = self.json_get(json_text)
        return text_af

class User_Agent(object):
    """
        直接将 网页的源码复制下载之后, 可以使用此类进行解析
        self.user_agent_data 是 读取 文件的,
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

# 搜狗问答聚合
class sogouSpider(object):
    # 初始化所有变量
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = "https://www.sogou.com/sogou?query=%s&ie=utf8&insite=wenwen.sogou.com" % (self.keyword)
        ua = User_Agent()
        user_agent = ua.random()
        self.ip_port = get_ip()
        self.headers = {
        'User-Agent': user_agent,
        }
    def conect_html(self,url):
        try:
            proxy = {
            'https' : 'https://' + self.ip_port,
            'http': "http://" + self.ip_port
            }
            response = requests.get(url, headers=self.headers, proxies=proxy,timeout=60)
        except:
            time.sleep(2)
            self.ip_port = get_ip()
            re = self.conect_html(url)
            return re
        else:
            return response.text
    # 过滤联系方式
    def filter(self, text):
        emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", text)
        if emails:
            return emails
        mobiles = re.findall(r"1\d{10}", text)
        if mobiles:
            return mobiles
        urls = re.findall(
            r"(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)", text)
        if urls:
            return urls
        qq = re.findall(r"[1-9]\\d{4,11}", text)
        if qq:
            return qq
        null = ""
        return null
    # 获取问答内容
    def article_gen(self, href):
        real_url = self.conect_html(href)
        real_url = re.findall("URL='(.*?)'",real_url)[0]
        html = self.conect_html(real_url)
        soup = BeautifulSoup(html, "html.parser")
        try:
            title = soup.select_one("#question_title_val").text
            content = soup.select_one(".replay-info-txt").text
        except BaseException:
            self.article_gen(href)
        paragraphs = content.split("\n")
        content_after = ""
        for paragraph in paragraphs:
            lin_t = self.filter(paragraph)
            if lin_t:
                pass
            else:
                content_after += paragraph + "\n"
        zon = [title, content_after]
        return zon
    # 转义
    def trans(self,content):
        contents = []
        # 开始切割字符串
        if len(content) > 800:
            # 大于800字开始切割
            text_ls = ""
            # 将文章打散成句子
            content_org = cut_sent(content)
            # 开始创建数据队列
            for content_o in content_org:
                text_a = text_ls + content_o
                if len(text_a) < 800:
                    text_ls = text_a
                else:
                    contents.append(text_ls)
                    text_ls = content_o
            contents.append(text_ls)
        else:
            # 小于800字不需要切割
            contents.append(content)
        trans_af = ""
        # 开始伪原创
        for con_a in contents:
            trans = google_trans(con_a)
            af = trans.trans()
            # t_sp = random.uniform(0,2)
            trans_af += af
        return trans_af
    # 获取内容数据
    def get_html(self):
        print("开始获取目标页面")
        html = self.conect_html(self.url)
        soup = BeautifulSoup(html, "html.parser")
        ae = 1
        num = 3
        mix_zon = []
        # 开始循环获取所有链接内容
        print("开始循环获取所有链接内容")
        while ae == 1:
            href = ""
            xpath = "#sogou_vr_30000201_%d" % (num)
            try:
                # 开始获取加密的内容链接
                print("开始获取加密的内容链接")
                href = soup.select(xpath)[0].attrs['href']
            except IndexError:
                if num > 10:
                    # 采集完成开始退出采集
                    print("此页内容已经采集完成")
                    ae = 2
            else:
                if href[-1] == ".":# 判读是否是有效链接
                    pass
                else:
                    
                    href = "https://www.sogou.com" + href
                    print(href)
                    zon = self.article_gen(href)
                    # 判断是否是有效文本
                    if zon != "none":
                        mix_zon.append(zon)
                    else:
                        print("已经去掉无效文本")
            num += 1
        print("开始转译")
        if mix_zon:
            mix_z = []
            for ace in mix_zon:
                conten = self.trans(ace[1])
                print("完成{0}".format(ace[0]))
                mix_z.append([ace[0],conten])
            return mix_z
        else:
            return "none"
    def zon(self):
        zon = self.get_html()
        if zon == "none":
            print("%s未找到满足条件的内容" % self.keyword)
            return "none"
        else:
            return zon

# 获取内容
def get_content(keyword):
    ac = sogouSpider(keyword)
    zon = ac.zon()
    description = ""
    content = ""
    for za in zon:
        description += za[0] + " "
        content += "{{title}}" + za[0] + "{{/title}}{{content}}" + za[1] + "{{/content}}"
    description = description.replace("%", "%%")
    description = description.replace("'", "''")
    content = content.replace("%", "%%")
    content = content.replace("'", "''")
    return [description, content]

# 总程序
def re_try(sql, db, retry_time):
    try:
        ac = sql_task(sql, db)
    except BaseException:
        print("重新尝试中。。。。")
        time.sleep(10)
        retry_time += 1
        if retry_time > 2:
            return "none"
        else:
            ac = re_try(sql, db, retry_time)
            return ac
    else:
        return ac

def zon():
    # 开始从集群总机获取任务
    task = get_keyword()
    print("任务获取成功，关键词为：" + task['title'] + "网站为：" + task['belong_web'])
    ids = ""
    # 开始采集内容并进行伪原创
    zon = get_content(task['title'])
    description = zon[0]
    content = zon[1].replace("\n","{{}}")
    # 采集完成将其从任务池中删除
    print("网站：%s，文章名：%s" % (task["belong_web"], task['title']))
    sql = "delete from task_pool where id=%d" % (task['id'])
    re_try(sql, "任务池", 1)
    # 将采集完成的内容开始插入到文章数据库中
    yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO %s (title, content, description, crawl_times, is_publish) VALUES ('%s', '%s', '%s', '%s', '%s')" % (task['belong_web'], task['title'], content, description, yun_times, "0")
    re_try(sql, "网站文章存储", 1)
    # 开始删除重复的数据
    sql = "select * from %s where title='%s'" % (task['belong_web'], task['title'])#
    ids = sql_task(sql, "网站文章存储")
    id_zon = []
    for id_ in ids:
        id_zon.append(id_['id'])
    try:
        id_zon.remove(max(id_zon))
    except BaseException:
        print("文章")
    # 采集完成返回成功信息并修改任务状态
    for id_z in id_zon:
        sql = "delete from %s where id=%d" % (task['belong_web'],id_z)
        sql_task(sql, "网站文章存储")
        
if __name__ == '__main__':
    a = 1
    while a == 1:
        yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("运行开始时间：" + yun_times)
        try:
            zon()
        except BaseException as e:
            print(e)
            print("没有任务，等待任务发布")
            yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("运行结束时间：" + yun_times)
            time.sleep(1.2)
        else:
            yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print("运行结束时间：" + yun_times)
