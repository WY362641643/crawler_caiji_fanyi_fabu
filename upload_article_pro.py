# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from requests_toolbelt import MultipartEncoder
from PIL import Image, ImageDraw, ImageFont
from selenium.webdriver.common.by import By
from selenium import webdriver
from tqdm import tqdm
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
# 织梦文章上传
class img_upload():
    def __init__(self,url,phpid,contents):
        self.contents = contents
        af = url.split("/")
        self.url = "/".join(af[0:-2]) + "/include/dialog/select_images_post.php"
        self.phpid = phpid
    # 上传图片
    def upload_img(self):
        php_id = "PHPSESSID=%s;" % (self.phpid)
        querystring = {"CKEditor": "body","CKEditorFuncNum":"2","langCode":"zh-cn"}
        img_name = str(int(time.time())) + "_" + str(random.randint(1000,9999)) + ".png"
        img_path1 = "img/" + img_name
        filename = self.img_out(img_path1)
        headers = {
            'Cookie': php_id,
        }
        payload = {
            "upload": (img_name, open(filename, 'rb'), "image/png")
        }
        m = MultipartEncoder(payload)
        headers['Content-Type'] = m.content_type
        response = requests.request("POST", self.url, data=m, headers=headers, params=querystring)
        response_text = response.text
        link = response_text.split(",")
        img_link = link[1][2:-1]
        return img_link
    # 获取txt文件内容
    def get_txt(self,file_name):
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                print(f)
        with open(file_name, "r", encoding='UTF-8') as f:
            textS = f.read()
            return textS
    # 获取所有字体文件
    def ttf_file_name(self,file_dir):
        L = []
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.ttf':
                    L.append(os.path.join(root, file))
        return random.choice(L)
    # 获取随机颜色
    def getRandomColor(self):
        '''获取一个随机颜色(r,g,b)格式的'''
        c1 = random.randint(0,255)
        c2 = random.randint(0,255)
        c3 = random.randint(0,255)
        return (c1,c2,c3)
    # 生成图片
    def img_out(self,filename):
        # 初始化图片的一些参数
        scale = 0.6198 # 图片高宽比例
        width = random.randrange(200,450) # 随机生成图片宽度
        height = int(width*scale) # 根据比例计算出图片高度
        color = self.getRandomColor()
        width_line = 3 # 内边框的框厚度
        line_length = 15 # 内边框距离
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
        pos_y_1 = int(height*0.5) - txtSize_1[1] - int(height * 0.05)
        # 计算第二段文字位置
        txtSize_2 = draw.textsize(self.contents[1], font1)
        pos_x_2 = (width - txtSize_2[0]) / 2
        pos_y_2 = int(height*0.5) + int(height * 0.05)
        # 开始绘制文字
        font_color = "#FFFFFF"
        draw.text((pos_x_1, pos_y_1), self.contents[0], fill=(font_color), font=font1)
        draw.text((pos_x_2, pos_y_2), self.contents[1], fill=(font_color), font=font1)
        draw.line([(line_length, line_length), (width - line_length, line_length),
                   (width - line_length, height - line_length), (line_length, height - line_length), (line_length, line_length)],
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
def content_to_html(content,background_link,phpid,web_type):
    # 开始提炼文章的关键词
    text = html_to_content(content)
    keyword_str = text_to_keywords(text)
    # 开始生成并上传第一张图片
    ac = img_upload(background_link,phpid,keyword_str)
    img_src_1 = ac.upload_img()
    keywords_str = "_".join(keyword_str)
    img_html_1 = "{{/content}}<img src='%s' alt='%s'>\n{{title}}" % (img_src_1,keywords_str)
    # 开始生成并上传第二张图片
    sql = "select * from web_keyword"
    web_keywords = sql_table_list(sql,"网站信息")
    keywords = web_keywords[int(web_type)][2]
    keywords_list = keywords.split("|")
    keywords_list = random.sample(keywords_list, 2)
    ac = img_upload(background_link, phpid, keywords_list)
    img_src_2 = ac.upload_img()
    img_alt_2 = "_".join(keywords_list)
    img_html_2 = "{{/content}}<img src='%s' alt='%s'>\n{{title}}" % (img_src_2,img_alt_2)
    content = content.replace("{{/content}}{{title}}", img_html_1, 1)
    content = content.replace("{{/content}}{{title}}", img_html_2, 1)
    content = content.replace("{{title}}", "<h2>")
    content = content.replace("{{/title}}", "</h2>\n")
    content = content.replace("{{content}}", "<p>")
    content = content.replace("{{/content}}", "</p>\n")
    content = content.replace("{{}}", "</p>\n<p>")
    print("图片一：{} 图片二：{}".format(img_src_1,img_src_2))
    return content
# 开始上传文章。
def push_article(session_id, add_article_url, title, content, description, type_id, excel_sheet):
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
        "typeid": type_id,  # 文章栏目
        "typeid2": "",  # 文章副栏目
        "keywords": "",  # 关键字9
        "autokey": 1,  # 自动获取关键字 1 为自动获取
        "description": description,  # 内容摘要
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
    php_id = "PHPSESSID=%s;" % (session_id)
    headers = {
        'Cookie': php_id,
    }
    response = requests.request("POST", add_article_url, data=payload, headers=headers, timeout=10)
    if "成功发布文章" in response.text:
        print("网站：%s，成功发布:%s" % (excel_sheet,title))
        return "yes"
    else:
        print("网站：%s，文章发布失败:%s" % (excel_sheet,title))
        print(response.text)
        return "no"
# 获取织梦session_id。
def get_phpid(background_link,user_name,password):
    try:
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
            text = "[{}]：网站：{}，已经登录成功！\n".format(yun_times,background_link)
            create_str_to_txt(text)
            print("域名：%s，已经登录成功！" % (background_link))
            cookies = browser.get_cookies()
            for cookie in cookies:
                if cookie["name"] == "PHPSESSID":
                    return cookie['value']
            browser.quit()
        else:
            browser.quit()
            yun_times = time.strftime("%Y-%m-%d", time.localtime())
            text = "[{}]：网站：{}，登录失败,请检查网站后台链接和账号密码是否正确？\n".format(yun_times,background_link)
            create_str_to_txt(text)
            print("域名：%s，登录失败,请检查网站后台链接和账号密码是否正确？" % (background_link))
            return "fail"
    except BaseException:
        yun_times = time.strftime("%Y-%m-%d", time.localtime())
        text = "[{}]：网站：{}，登录失败,请检查网站网络是否出现问题。\n".format(yun_times,background_link)
        create_str_to_txt(text)
        print("域名：%s，登录失败,请检查网站后台链接和账号密码是否正确？" % (background_link))
        return "fail"
# 文章上传管理程序。
def push_allin(session_id,db_article,background_link,type_id,excel_sheet,web_type):
    add_article_url = background_link + "article_add.php"
    article_id = db_article[0]
    title = db_article[1]
    content = content_to_html(db_article[2],background_link,session_id,web_type)
    description = db_article[3]
    try:
        status = push_article(session_id, add_article_url, title, content, description, type_id, excel_sheet)
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
    type_id = table[6]
    web_type = table[8]
    session_id = get_phpid(background_link, username, password)
    if session_id == "fail":
        return "no"
    else:
        time.sleep(1)
        sql = "select * from %s" % (excel_sheet)
        db_articles = sql_table_list(sql,"网站文章存储")
        print("网站：%s，需要推送：%d 条，开始推送。" % (excel_sheet, len(db_articles)))
        for db_article in db_articles:
            push_allin(session_id,db_article,background_link,type_id,excel_sheet,web_type)
def zon_print(table):
    excel_sheets = table[1]
    # 开始创建日志数据库
    create_article(excel_sheets)
    yun_times = time.strftime("%Y-%m-%d", time.localtime())
    # 开始获取内容
    sql = "select * from %s" % (excel_sheets)
    db_articles = sql_table_list(sql, "网站文章存储")
    yun_times = time.strftime("%Y-%m-%d", time.localtime())
    sql = "select * from %s where upload_time='%s'" % (excel_sheets, yun_times)
    # 获取今日上传总数
    upload_log = sql_table_list(sql, "站群运行日志")
    if upload_log:
        print("{}找到日志：{}".format(excel_sheets,upload_log[0][1]))
        pass
    else:
        # 创建该网站当天的数据
        sql = "insert into {} (upload_num,upload_time) values (0,'{}')".format(excel_sheets, yun_times)
        sql_insert_web(sql, "站群运行日志")
    # 获取需要上传数量
    # 开始获取
    if 
    if len(db_articles) > 2:
        try:
            upload_articles(table)
        except BaseException:
            yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            text = "[{}]：网站：{}，发布文章时出错。\n".format(yun_times, excel_sheets)
            create_str_to_txt(text)
            print("网站：%s，发布文章时出错。" % (excel_sheets))
    else:
        yun_times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        text = "[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。\n".format(yun_times, excel_sheets)
        create_str_to_txt(text)
        print("[{}]：网站：{}，剩余文章数量不足，不满足发布的条件。".format(yun_times, excel_sheets))
def clear_img():
    rootdir = "img/"
    filelist=os.listdir(rootdir)              #列出该目录下的所有文件名
    pbar = tqdm(filelist)
    for a in pbar:
        path = rootdir + a
        os.remove(path)
        pbar.set_description("正在删除[{0}]:".format(a))
def general_img():
    path_img = "img/"
    for a in range(1000):
        path = path_img + str(a) + ".png"
        ac = img_upload("1","a",[str(a),str(a)])
        ac.img_out(path)

if __name__ == '__main__':
    # 删除图片文件
    clear_img()
    # 开始上传织梦文章
    sql = "select * from web where push_platform='dede'"
    db_name = "网站信息"
    tables = sql_table_list(sql, db_name)
    for table in tables:
        try:
            zon_print(table)
        except BaseException as e:
            print(e)
            time.sleep(10)
    # 开始上茶u你