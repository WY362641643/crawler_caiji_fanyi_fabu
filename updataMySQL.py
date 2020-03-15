#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/3/7 22:34
# @Author  : 亦轩
# @File    : updataMySQL.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
HOST = 'ymhack.wicp.net'
PORT = 13306
user = "python_gather"
# 数据库密码
password = "ebe1bc4806"
# 数据库名
database = "python_gather"
# HOST = '192.168.2.83'
# RedisPORT = 6379
# SQLPORT = 3306
import MySQLdb
# 打开数据库连接
db = MySQLdb.connect(HOST,user , password, database,PORT, charset='utf8')
# 使用cursor()方法获取操作游标
cursor = db.cursor()
# 使用execute方法执行SQL语句
sql = 'select id,`name` from webnumber'
cursor.execute(sql)
# 获取网站信息
data = cursor.fetchall()

# SQL 插入语句
sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
siteweb = ''
for info in data:
   siteweb += '   | {}\n'.format(info)
dayin ='''
   +----------------------------------------------------+
{}
请输入id: 
'''.format(siteweb)
while True:
   try:
      ids = int(input(dayin))
      break
   except:
      print('输入错误')
while True:
   try:
      num = int(input('''
      +--------------------------+
      |  1. 常规采集             |
      |  2. 智能采集             |
      |  3. 智能词库             |
      |  4. 常规词库             |
      +--------------------------|
      请选择序号:  '''))
      break
   except:
      print('输入错误')
if num == 1:
   sql = 'insert into '

with open('1.txt','r')as f:
   texts = f.read()
text_list = texts.split('\n')
for data in text_list:

   try:
      # 执行sql语句
      cursor.execute(sql)
      # 提交到数据库执行
      db.commit()
   except:
      # Rollback in case there is any error
      db.rollback()

# 关闭数据库连接
db.close()