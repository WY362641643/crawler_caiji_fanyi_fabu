#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/24 20:51
# @Author  : 亦轩
# @File    : 3333.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
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
from lxml import html
from PIL import Image
import jieba.analyse
import html as htmls
from DBUtils.PooledDB import PooledDB, SharedDBConnection
import datetime
import requests
import pymysql
import random
import jieba
import redis
import time
import json
import os
import re

key_delet = [
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

# config = {
#     "host": "ymhack.wicp.net",
#     "port": 13306,
#     "user": "python_gather",
#     "password": "ebe1bc4806",
#     "database": "python_gather",
# }
POOL = PooledDB(
    # 使用链接数据库的模块
    creator=pymysql,
    # 连接池允许的最大连接数，0和None表示不限制连接数
    maxconnections=6,
    # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    mincached=2,
    # 链接池中最多闲置的链接，0和None不限制
    maxcached=5,
    # 链接池中最多共享的链接数量，0和None表示全部共享。
    # 因为pymysql和MySQLdb等模块的 threadsafety都为1，
    # 所有值无论设置为多少，maxcached永远为0，所以永远是所有链接都共享。
    maxshared=3,
    # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用。
    #  如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    # # 主机地址
    host='ymhack.wicp.net',
    # # 端口
    port=13306,
    # 主机地址
    # host='192.168.2.83',
    # 端口
    # port=3306,
    # 数据库用户名
    user="python_gather",
    # 数据库密码
    password="ebe1bc4806",
    # 数据库名
    database="python_gather",
    # 字符编码
    charset='utf8'
)
# db_pool = PersistentDB(pymysql, **config)
# # 从数据库连接池是取出一个数据库连接
# SQLconn = db_pool.connection()
# SQLcursor = SQLconn.cursor()
# 创建连接,POOL数据库连接池中
SQLconn = POOL.connection()
# 创建游标
SQLcursor = SQLconn.cursor()
date = datetime.datetime.now().strftime('%Y-%m-%d')
id = 821896
webid = 37
if 'l' in str(id):
    ids = int(id[:-1])
    sql = "update lexiconurl set `date`='{}',`isActivate`=1 where id={}".format(date, ids)
else:
    sql = "update mainurl set `date`='{}',`isActivate`=1 where id={}".format(date, id)
SQLcursor.execute(sql)
sql = 'UPDATE webnumber set numb= numb + 1 where id="%d"' % webid
SQLcursor.execute(sql)  # 执行
SQLconn.commit()
print('执行成功')