# -*- coding: utf-8 -*-
import re
import requests
import time
import pymysql

class BaiduPush(object):
    def __init__(self):
        self.host = 'ymhack.wicp.net'
        self.user = 'python_gather'
        self.pwd = 'ebe1bc4806'
        self.dbname = "python_gather"
        self.port = 13306

    #获取百度收录信息
    def push_urls(self,url, urls):
        #url:根据百度站长提供的API推送链接
        #urls:需要提交的链接数据
        headers = {
            'User-Agent': 'curl/7.12.1',
            'Host': 'data.zz.baidu.com',
            'Content - Type': 'text/plain',
            'Content - Length': '83'
        }
        result = requests.post(url, headers=headers, data=urls, timeout=5).text
        print('推送百度返回的信息: ',result)
        return result

    def site_api_post(self):
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port, charset='utf8')  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        sql = 'SELECT weblink,baidupush FROM webnumber'
        cursor.execute(sql)  # 执行
        result = cursor.fetchall()  # result是元
        data = {
            'iscategory': 0,
            'isarticle': 1,
            'ispage': 0,
            'istag': 0,
        }
        for domain in result:
            weblink = domain[0]
            baidupush = domain[1]
            if not baidupush:
                continue
            post_url = weblink  + "/zb_users/plugin/baiduziyuan/sitemap.php"
            requests.post(post_url,data=data)
            url = weblink  + "/sitemap.xml"
            try:
                html = requests.get(url, timeout=15).text
                urls = re.findall('<loc>(.*?)</loc>', html)
                urls_str = '\n'.join(urls)
                # if len(urls_str) > 1990:
                #     urls = urls_str[]
                result = self.push_urls(baidupush,urls_str)
                if not eval(result)['success']:
                    print('推送错误, 错误原因',result)
                yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print("执行结果:"+result+'\n'"网站为："+weblink+"执行完成时间："+ yun_times)
            except:
                print('获取出错!!!')


if __name__ == '__main__':
    while True:
        BaiduPush().site_api_post()
        yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("程序执行完成!!!,结束时间："+ yun_times)
        time.sleep(8*60*60)

