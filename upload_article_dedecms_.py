# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlrd
import requests
import time
# 引入自定义函数
import post_img
import datetime
import sqlite3

def E_trans_to_C(string):
    E_pun = u',.!?[]()<>"\''
    C_pun = u'，。！？【】（）《》“‘'
    table= {ord(f):ord(t) for f,t in zip(E_pun,C_pun)}
    return string.translate(table)
def deal_it(content):
    contents = content.replace("{{}}", "</p><p>")
    contents = contents.replace("{{title}}", "<h2>")
    contents = contents.replace("{{/title}}", "</h2>")
    contents = contents.replace("{{content}}", "<p>")
    content = contents.replace("{{/content}}", "</p>")
    return content

def push_article(phpid,url,title,content,typeid,descrption,id,sheet):
    # 标题
    # 文章内容
    content = deal_it(content)
    # title = con_zon[1]

    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S');
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
        "writer": "",  # 作者
        "typeid": typeid,  # 文章栏目
        "typeid2": "",  # 文章副栏目
        "keywords": "",  # 关键字9
        "autokey": 1,  # 自动获取关键字 1 为自动获取
        "description": descrption,  # 内容摘要
        "remote": 1,  # 下载远程图片和资源
        "autolitpic": 1,  # 自动提取第一个图片为缩略图
        "dellink": "", #自动删除非站内链接
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
        "pubdate": time_now,  # 发布日期
        "ishtml": 1,  # 是否生成html 1：生成html 0：动态浏览
        "title": title,  # 文章标题
    }
    # 织梦会话ID
    php_id = "PHPSESSID=%s;" % (phpid)
    headers = {
        'Cookie': php_id,
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if "成功发布文章" in response.text:
        print("成功发布:%s" % (title))
        # sql = "DELETE FROM %s WHERE id = %d" % (sheet, id)
        # sqlite_del(sql)
        return "yes"
    else:
        print("文章发布失败:%s" % (title))
        print(response.text)
        return "no"
def get_phpid(url,user_name,password):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-gpu')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    wait = WebDriverWait(browser, 20)
    wait.until(EC.presence_of_element_located((By.NAME, 'sm1')))
    user_input = browser.find_element_by_name("userid")
    user_input.send_keys(user_name)
    password_input = browser.find_element_by_name("pwd")
    password_input.send_keys(password)
    browser.find_element_by_name("sm1").click()
    code = browser.page_source
    if "成功登录" in code:
        print("已经登录成功")
        cookies = browser.get_cookies()
        for cookie in cookies:
            if cookie["name"] == "PHPSESSID":
                return cookie['value']
        browser.quit()
    else:
        browser.quit()
        print("登录失败,请检查网站后台链接和账号密码是否正确")
        return "fail"

def keyword_input():
    # 获取所有锚文本信息
    file_path = "信息存贮/模板文章关键词.xlsx"
    links = []
    sheet = "Sheet1"
    with xlrd.open_workbook(file_path) as f:
        table = f.sheet_by_name(sheet)
        nrows_num = table.nrows
        ncols_num = table.ncols
        for nrows in range(nrows_num):
            link = []
            for ncols in range(ncols_num):
                cell_value = table.cell(nrows, ncols).value
                link.append(cell_value)
            links.append(link)
    return links

def setting_excel():
    # 获取所有锚文本信息
    file_path = "信息存贮/网站配置.xlsx"
    links = []
    with xlrd.open_workbook(file_path) as f:
        table = f.sheet_by_name('Sheet1')
        nrows_num = table.nrows
        ncols_num = table.ncols
        for nrows in range(nrows_num):
            link = []
            for ncols in range(ncols_num):
                if nrows == 0:
                    aca = ""
                else:
                    cell_value = table.cell(nrows, ncols).value
                    link.append(cell_value)
            if link:
                links.append(link)
    return links
def sqlite(sql1):
    conn = sqlite3.connect("信息存贮/网站文章存储.db")
    cursor = conn.cursor()  # IF NOT EXISTS
    value = cursor.execute(sql1)
    a_list = []
    for a in value:
        a_list.append(a)
    cursor.close() # 关闭游标：
    conn.commit() # 提交事物
    conn.close() # 关闭连接
    return a_list
def sqlite_del(sql1):
    conn = sqlite3.connect("信息存贮/网站文章存储.db")
    cursor = conn.cursor()  # IF NOT EXISTS
    cursor.execute(sql1)
    cursor.close() # 关闭游标：
    conn.commit() # 提交事物
    conn.close() # 关闭连接
    return
def push_allin(text, url, web_link, phpid, title, typeid, descrption, id, sheet):
    ac = text
    url = url + "article_add.php"
    # 上传图片的链接
    url2 = web_link + "include/dialog/select_images_post.php"
    img_links = []
    for img_name in img_names:
        img_links.append(post_img.upload_img(url2, img_name, phpid))
    # img_link1 = img_links[0]
    # img_link2 = img_links[1]
    # content = ac.replace("*_img_src_1_*", img_link1)
    # content = content.replace("*_img_src_2_*", img_link2)
    content = text
    push_article(phpid, url, title, content, typeid, descrption, id, sheet)


# noinspection PyInterpreter
if __name__ == '__main__':
    # links = setting_excel()
    # num_list = 1
    # num_re = 0
    # for link in links:
    #     print("%d.域名为：%s" % (num_list, link[1]))
    #     num_list += 1
    #     # 获取所有先关网站信息
    #     a_real = num_re
    #     url = links[a_real][1]
    #     # 获取所有网站先关信息
    #     ad = url.split("/")
    #     web_link = ad[0] + "//" + ad[2] + "/"
    #     sheet = links[a_real][0]
    #     user_name = links[a_real][2]
    #     password = links[a_real][3]
    #     typeid = links[a_real][5]
    #     url_phpID = url
    #     sql_count = "SELECT COUNT(*) FROM %s" % (sheet)
    #     b_list = sqlite(sql_count)
    #     art_num = int(b_list[0][0])
    #     num = links[a_real][4]
    #     print("%s剩余文章数为：%d个" % (sheet, art_num))
    #     # push_num = input("请输入要发布的文章数：")
    #     num_re += 1
    #     if art_num == 0 or num == 0:
    #         pass
    #     else:
            url_phpID = 'http://xitong.baobanzhang.com/ymhack2020/index.php'
            user_name = 'admin'
            password = 'Bufuguowang123'
            phpID = get_phpid(url_phpID, user_name, password)
            # time.sleep(2)
            # sql1 = "select * from %s  order by id asc limit %d" % (sheet, num)
            # a_list = sqlite(sql1)
            for a in range(5):
                print("-----------------------------------")
                title = '爬虫测试'
                # img_names = []
                # for ad in range(2):
                #     img_names.append(post_img.img())
                # print(img_names)
                text = '爬虫测试文章内容'
                url = 'http://xitong.baobanzhang.com/ymhack2020/'
                web_link = ''
                typeid = 1
                descrption = '摘要'
                id = 0
                sheet= 0
                try:
                    push_allin(text, url, web_link, phpID, title, typeid, descrption, id, sheet)
                    # time.sleep(1)
                except BaseException as e:
                    print(e)
                    time.sleep(3)
                    push_allin(text, url, web_link, phpID, title, typeid, descrption, id, sheet)
