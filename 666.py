#!/usr/bin/env python
# coding=utf-8
# @Time    : 2020/2/24 23:39
# @Author  : 亦轩
# @File    : 666.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import random
import requests
from lxml import html as htmlss
import html as htmls
from lxml import etree
url = 'http://dy.163.com/v2/article/detail/DIU0H2JI0516EBHL.html'
res = requests.post(url)
html = res.text
div = etree.HTML(html)
table = div.xpath('//div[@id="content"]')[0]
content = etree.tostring(table, method='html')
content_ls = htmls.unescape(content.decode('utf-8'))
htmlres = res.text
# html = etree.HTML(html)
tree = htmlss.fromstring(htmlres)
content_ls = ''

namelist = tree.xpath('//div[@id="content"]')

name1 = html.tostring(namelist[0])
content_ls += htmls.unescape(name1.decode('gbk'))

