# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests_toolbelt import MultipartEncoder
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver.common.by import By
from selenium import webdriver
import jieba
jieba.set_dictionary('dict.txt')
jieba.initialize()
from jieba import analyse
jieba.analyse.set_idf_path("idf.txt")
import requests
import datetime
import sqlite3
import random
import time
import os
import sys
# 织梦文章上传
class img_upload():

    def __init__(self,url,contents):
        self.contents = contents
        af = url.split("/")
        self.url = "/".join(af[0:-2]) + "/api/upload_images_api.php"

        # 上传图片
    def upload_img(self,background_link):
            querystring = {"CKEditor": "body", "CKEditorFuncNum": "2", "langCode": "zh-cn"}
            img_name = str(int(time.time())) + "_" + str(random.randint(1000, 9999)) + ".png"
            img_path1 = "img/" + img_name
            filename = self.img_out(img_path1)
            payload = {
                "upload": (img_name, open(filename, 'rb'), "image/png")
            }
            m = MultipartEncoder(payload)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
            }
            headers['Content-Type'] = m.content_type
            url = background_link + "/resultApi?act=upload_Img"
            response = requests.request("POST", url, data=m, headers=headers, params=querystring)
            response_text = response.text
            if response_text == 'error':
                print('上传文件失败')
            # else:
            #     if (os.path.exists(img_path1)):
            #         os.remove(img_path1)
            #         print('文件上传成功，已删除本地文件：%s' % (img_name))
            img_link = response_text
            return img_link


    def get_txt(self, file_name):
            if not os.path.exists(file_name):
                with open(file_name, "w") as f:
                    print(f)
            with open(file_name, "r", encoding='UTF-8') as f:
                textS = f.read()
                return textS

        # 获取所有字体文件
    def ttf_file_name(self, file_dir):
            L = []
            for root, dirs, files in os.walk(file_dir):
                for file in files:
                    if os.path.splitext(file)[1] == '.ttf':
                        L.append(os.path.join(root, file))
            return random.choice(L)

        # 获取随机颜色
    def getRandomColor(self):
            '''获取一个随机颜色(r,g,b)格式的'''
            c1 = random.randint(0, 255)
            c2 = random.randint(0, 255)
            c3 = random.randint(0, 255)
            return (c1, c2, c3)

        # 生成图片
    def img_out(self, filename):
            # 初始化图片的一些参数
            scale = 0.6198  # 图片高宽比例
            width = random.randrange(400, 700)  # 随机生成图片宽度
            height = int(width * scale)  # 根据比例计算出图片高度
            color = self.getRandomColor()
            width_line = 3  # 内边框的框厚度
            line_length = 15  # 内边框距离
            font_size = int(width * 0.16)
            im = Image.new('RGB', (width, height), color)
            draw = ImageDraw.Draw(im)
            # 设置字体
            font_set = 0
            while font_set == 0:
                try:
                    file_path = self.ttf_file_name("ttf/")
                    font1 = ImageFont.truetype(file_path, font_size)
                except BaseException:
                    print(file_path)
                else:
                    font_set = 1
            # 开始绘制噪点
            for i in range(int(width * 1.5)):  # random.randrange(400,1200)
                draw.point([random.randint(0, width), random.randint(0, height)], fill=self.getRandomColor())
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.getRandomColor())
            # 计算第一段文字位置
            txtSize_1 = draw.textsize(self.contents[0], font1)
            pos_x_1 = (width - txtSize_1[0]) / 2
            pos_y_1 = int(height * 0.5) - txtSize_1[1] - int(height * 0.05)
            # 计算第二段文字位置
            txtSize_2 = draw.textsize(self.contents[1], font1)
            pos_x_2 = (width - txtSize_2[0]) / 2
            pos_y_2 = int(height * 0.5) + int(height * 0.05)
            # 开始绘制文字
            font_color = "#FFFFFF"
            draw.text((pos_x_1, pos_y_1), self.contents[0], fill=(font_color), font=font1)
            draw.text((pos_x_2, pos_y_2), self.contents[1], fill=(font_color), font=font1)
            draw.line([(line_length, line_length), (width - line_length, line_length),
                       (width - line_length, height - line_length), (line_length, height - line_length),
                       (line_length, line_length)],
                      fill="#FFFFFF", width=width_line)
            im.save(filename)
            return filename

# 文章关键词挖掘
def text_to_keywords(text):
    keywords = jieba.analyse.extract_tags(text,topK=5,withWeight=False)
    keywords_length = []
    for keyword in keywords:
        length = len(keyword)
        utf8_length = len(keyword.encode('utf-8'))
        length = (utf8_length - length) / 2 + length
        keywords_length.append([int(length),0])
    keywords_str = []
    for list_num in range(len(keywords_length)):
        if keywords_length[list_num][1] == 0:
            keywords_length[list_num][1] = 1
            for list_num2 in range(len(keywords_length)):
                if keywords_length[list_num2][1] == 0:
                    sum_len = keywords_length[list_num2][1] + keywords_length[list_num][1]
                    if sum_len == 5:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        keywords_str.append(str_keyword)
                        break
                    elif sum_len < 6:
                        str_keyword = keywords[list_num] + " " + keywords[list_num2]
                        keywords_length[list_num2][1] = 1
                        keywords_str.append(str_keyword)
                        break
    return keywords_str

# 文章内容去标签化
def html_to_content(html):
    html = html.replace("{{title}}", "")
    html = html.replace("{{/title}}", "")
    html = html.replace("{{content}}", "")
    html = html.replace("{{/content}}", "")
    content = html.replace("{{}}", "")
    return content

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
# 数据库相关操作
# 创建文章发布日志数据：
def create_article(table_name):
    conn = sqlite3.connect("信息存贮/站群运行日志.db")
    cursor = conn.cursor()  # IF NOT EXISTS
    sql = """CREATE TABLE IF NOT EXISTS %s(
          id INTEGER PRIMARY KEY NOT NULL,
          upload_num text NOT NULL,
          upload_time text NOT NULL
        );""" % (table_name)
    cursor.execute(sql)
    cursor.close()# 关闭游标：
    conn.commit()# 提交事物
    conn.close()# 关闭连接
    return table_name
# 数据库插入和更新数据
def sql_insert_web(sql, db_name):
    conn = sqlite3.connect("信息存贮/%s.db" % (db_name))
    cursor = conn.cursor()  # IF NOT EXISTS
    value = cursor.execute(sql)
    cursor.close() # 关闭游标：
    conn.commit() # 提交事物
    conn.close() # 关闭连接
    return value
# 获取数据库所有信息。
def sql_table_list(sql1, table):
    conn = sqlite3.connect("信息存贮/%s.db" % (table))
    cursor = conn.cursor()  # IF NOT EXISTS
    value = cursor.execute(sql1)
    a_list = []
    for a in value:
        a_list.append(a)
    cursor.close()  # 关闭游标：
    conn.commit()  # 提交事物
    conn.close()  # 关闭连接
    return a_list
# 为文章内容生成标签。
def content_to_html(content,background_link,web_type):
    text = html_to_content(content)
    keyword_str = text_to_keywords(text)
    # 开始生成并上传第一张图片
    ac = img_upload(background_link,keyword_str)
    img_src_1 = ac.upload_img(background_link)
    keywords_str = "_".join(keyword_str)
    img_html_1 = '{{/content}}<img src="%s" alt="%s">\n{{title}}' % (img_src_1,keywords_str)
    # 开始生成并上传第二张图片
    sql = "select * from web_keyword"
    web_keywords = sql_table_list(sql,"网站信息")
    keywords = web_keywords[int(web_type)][2]
    keywords_list = keywords.split("|")
    keywords_list = random.sample(keywords_list, 2)
    ac = img_upload(background_link, keywords_list)
    img_src_2 = ac.upload_img(background_link)
    img_alt_2 = "_".join(keywords_list)
    img_html_2 = '{{/content}}<img src="%s" alt="%s">\n{{title}}' % (img_src_2,img_alt_2)
    content = content.replace("{{/content}}{{title}}", img_html_1, 1)
    content = content.replace("{{/content}}{{title}}", img_html_2, 1)
    content = content.replace("{{title}}", "<h2>")
    content = content.replace("{{/title}}", "</h2>\n")
    content = content.replace("{{content}}", "<p>")
    content = content.replace("{{/content}}", "</p>\n")
    content = content.replace("{{}}", "</p>\n<p>")

    return content

#获取当天随机时间戳
def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)

def randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S'):
    return strTimeProp(start, end, random.random(), frmt)

# 开始上传文章。
def push_article(add_article_url, title, content, description, excel_sheet,type_id):
    now_time = int(time.time())
    time_array = time.localtime(now_time)
    start = time.strftime("%Y-%m-%d 00:00:00", time_array)
    end = time.strftime("%Y-%m-%d 23:59:59", time_array)
    random_time=randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S')
    payload = {
            "log_CateID": type_id,
            "log_AuthorID":1,
            "log_Tag":"",
            "log_Status":0,
            "log_Type":0,
            "log_Alias":0,
            "log_IsTop":0,
            "log_IsLock":0,
            "log_Title":title,
            "log_Intro":description,
            "log_Content":content,
            "log_PostTime":random_time,
            "log_CommNums":0,
            "log_ViewNums":0,
            "log_Template":"",
            "log_Meta":"",
    }
    # 织梦会话ID
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", add_article_url, data=payload, timeout=10,headers = headers)
    if "success" in response.text:
        print("网站：%s，成功发布:%s" % (excel_sheet,title))
        print(1)
        return "yes"
    else:
        print("网站：%s，文章发布失败:%s" % (excel_sheet,title))
        print(response.text)
        return "no"

# 文章上传管理程序。
def push_allin(db_article,background_link,excel_sheet,web_type,type_id):
    add_article_url = background_link + "/api.php?act=article_Api"
    article_id = db_article[0]
    title = db_article[1]
    content = content_to_html(db_article[2],background_link,web_type)
    description = db_article[3]
    try:
        status = push_article( add_article_url, title, content, description, excel_sheet, type_id)
    except BaseException:

        pass
    else:
        if status == "yes":
            sql = "delete from %s where id=%s" % (excel_sheet,article_id)
            sql_insert_web(sql,"网站文章存储")
            # 开始插入日志
            yun_times = time.strftime("%Y-%m-%d", time.localtime())
            sql = "select * from %s where upload_time='%s'" % (excel_sheet, yun_times)
            upload_log = sql_table_list(sql, "站群运行日志")
            upload_num_today = str(int(upload_log[0][1]) + 1)
            sql = "update %s set upload_num=%s where upload_time='%s'" % (excel_sheet, upload_num_today, yun_times)
            sql_insert_web(sql, "站群运行日志")

# 总控程序。
def upload_articles(table):
    # 获取所有先关网站信息
    # id_s = table[0]
    excel_sheet = table[1]
    background_link = table[2]
    username = table[3]
    password = table[4]
    web_type = table[9]
    type_id = table[7]
    time.sleep(1)
    sql = "select * from %s" % (excel_sheet)
    db_articles = sql_table_list(sql,"网站文章存储")
    print("网站：%s，需要推送：%d 条，开始推送。" % (excel_sheet, len(db_articles)))
    for db_article in db_articles:
            push_allin(db_article,background_link,excel_sheet,web_type,type_id)


def zon_print(table):
    excel_sheets = table[1]
    # 开始创建日志数据库
    create_article(excel_sheets)
    # 开始获取内容
    sql = "select * from %s" % (excel_sheets)
    db_articles = sql_table_list(sql, "网站文章存储")
    yun_times = time.strftime("%Y-%m-%d", time.localtime())
    sql = "select * from %s where upload_time='%s'" % (excel_sheets, yun_times)
    upload_log = sql_table_list(sql, "站群运行日志")
    sql1 = "select upload_num from %s where upload_time='%s'" % (table[1], yun_times)
    result = sql_table_list(sql1, '站群运行日志')

    if result == [] :
        if upload_log:
            print("{}找到日志：{}".format(excel_sheets,upload_log[0][1]))
            pass
        else:
            sql = "insert into {} (upload_num,upload_time) values (0,'{}')".format(excel_sheets, yun_times)
            sql_insert_web(sql, "站群运行日志")
        if len(db_articles) > 2:
            try:
                upload_articles(table)
            except BaseException:
                upload_articles(table)
                yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                text = "[{}]：网站：{}，发布文章时出错。\n".format(yun_times, excel_sheets)
                create_str_to_txt(text)
                print("网站：%s，发布文章时出错。" % (excel_sheets))
        else:
            yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text = "[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。\n".format(yun_times, excel_sheets)
            create_str_to_txt(text)
            print("[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。".format(yun_times, excel_sheets))
            time.sleep(10)
    elif result[0][0] < int(table[6]) :
        if upload_log:
            print("{}找到日志：{}".format(excel_sheets,upload_log[0][1]))
            pass
        else:
            sql = "insert into {} (upload_num,upload_time) values (0,'{}')".format(excel_sheets, yun_times)
            sql_insert_web(sql, "站群运行日志")
        if len(db_articles) > 2:
            try:
                upload_articles(table)
            except BaseException:
                upload_articles(table)
                yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                text = "[{}]：网站：{}，发布文章时出错。\n".format(yun_times, excel_sheets)
                create_str_to_txt(text)
                print("网站：%s，发布文章时出错。" % (excel_sheets))
        else:
            yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text = "[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。\n".format(yun_times, excel_sheets)
            create_str_to_txt(text)
            print("[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。".format(yun_times, excel_sheets))
            time.sleep(10)
    else:
        if upload_log:
            print("{}找到日志：{}".format(excel_sheets,upload_log[0][1]))
            pass
        else:
            sql = "insert into {} (upload_num,upload_time) values (0,'{}')".format(excel_sheets, yun_times)
            sql_insert_web(sql, "站群运行日志")
        yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text = "[{}]：网站：{}，发布文章已达每日上限。\n".format(yun_times, excel_sheets)
        create_str_to_txt(text)
        print("[{}]：网站：{}，发布文章已达每日上限".format(yun_times, excel_sheets))
if __name__ == '__main__':
    now_time = int(time.time())
    time_array = time.localtime(now_time)
    start = time.strftime("%Y-%m-%d 00:00:00", time_array)
    end = time.strftime("%Y-%m-%d 23:59:59", time_array)
    random_time = randomTimestamp(start, end, frmt='%Y-%m-%d %H:%M:%S')



    # 开始生成并上传文章
    sql = "select * from web where push_platform='z_blog'"
    db_name = "网站信息"
    tables = sql_table_list(sql, db_name)
    for table in tables:
        yun_times = time.strftime("%Y-%m-%d", time.localtime())
        try:
            zon_print(table)
        except BaseException as e:
            print(e)
            time.sleep(10)
