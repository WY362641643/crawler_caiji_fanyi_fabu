#!/usr/bin/env python
# coding: utf-8
# @Time    : 2020/2/9 13:32
# @Author  : 亦轩
# @File    : crawler_redis.py
# @Email   : 362641643@qq.com
# @Software: win10 python3.7.2
import redis
import pymysql
import time
from hashlib import md5
import datetime
import os

# 数据库接口配置

HOST = '127.0.0.1'
RedisPORT = 6379
SQLPORT = 3306


# 加密
def get_md5(text):
    if isinstance(text, str):
        text = text.encode('utf-8')
    m = md5()
    m.update(text)
    return m.hexdigest()


def get_nowtime():
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
    return nowTime


# 获取url和关键字
class MySQL_My(object):
    def __init__(self):
        self.host = HOST
        self.user = 'tp5admin'
        self.pwd = 'HKxGpYfC5MmhPWe4'
        self.dbname = "tp5admin"
        self.port = SQLPORT

    def run(self):
        data_changgui = []
        data_zhineng = []
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port, charset='utf8')  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        lens = 0
        try:
            # sql = "update mainurl set isActivate=0  where isActivate=2"
            # cursor.execute(sql)
            # sql = "update mainurlzhineng set isActivate=0  where isActivate=2"
            # sql = 'ALTER TABLE `errmainurl` ADD UNIQUE(`ids`)'
            # cursor.execute(sql)
            # conn.commit()
            # sql = "update webnumber set numb=0"
            # cursor.execute(sql)
            # 查询网站数量 -p
            sql = "select id,`name`,maxnumb,numb,isActivate,`colum`,author,weblink,`describe`,isActivateTime,ratioimg,cms,title,pattern,lexicon_id,lexiconz_id from admin_webnumber"
            cursor.execute(sql)  # 执行
            result = cursor.fetchall()  # result是元
            for ids, webname, maxnb, nb, isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms, selecttitle, pattern, lexicon, lexiconz in result:
                # number = maxnb - nb
                # if number > 5000:
                #     number = 5000
                number = maxnb
                # if ids != 14:
                #     continue
                if number > 0:
                    if pattern == '1':
                        # 查询普通模式 url链接，关键字
                        sql = "select id,title,url,isActivate,web_id from admin_mainurl where isActivate=0 and web_id=%d limit %d" % (
                            ids, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_mainurl set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        sql = 'select isActivate from admin_mainurl where isActivate=0 and web_id=%d' % ids
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        if not result:
                            sql = 'update admin_webnumber set lexiconResidue=0 where id=%d' % ids
                        else:
                            sql = 'update admin_webnumber set lexiconResidue=%d where id=%d' % (len(tuple_number), ids)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_changgui.append(
                            [webname, ids, isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                    elif pattern == '2':
                        # 查询 智能 模式 url链接，关键字
                        sql = "select id,title,isActivate,web_id from admin_mainurlzhineng where isActivate=0 and web_id=%d limit %d" % (
                            ids, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_mainurlzhineng set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        sql = 'select isActivate from admin_mainurlzhineng where isActivate=0 and web_id=%d' % ids
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        # 更改此网站的 剩余数量
                        if not result:
                            sql = 'update admin_webnumber set zlexiconResidue=0 where id=%d' % ids
                        else:
                            sql = 'update admin_webnumber set zlexiconResidue=%d where id=%d' % (len(tuple_number), ids)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_zhineng.append(
                            [webname, ids, isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                    elif pattern == '12':
                        # 采集为双模式
                        sql = "select id,title,url,isActivate,web_id from admin_mainurl where isActivate=0 and web_id=%d limit %d" % (
                            ids, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_mainurl set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        sql = 'select isActivate from admin_mainurl where isActivate=0 and web_id=%d' % ids
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        if not result:
                            sql = 'update admin_webnumber set lexiconResidue=0 where id=%d' % ids
                        else:
                            sql = 'update admin_webnumber set lexiconResidue=%d where id=%d' % (len(tuple_number), ids)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_changgui.append(
                            [webname, ids, isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                        # 查询 智能 模式 url链接，关键字
                        sql = "select id,title,isActivate,web_id from admin_mainurlzhineng where isActivate=0 and web_id=%d limit %d" % (
                            ids, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_mainurlzhineng set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        sql = 'select isActivate from admin_mainurlzhineng where isActivate=0 and web_id=%d' % ids
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        # 更改此网站的 剩余数量
                        if not result:
                            sql = 'update admin_webnumber set zlexiconResidue=0 where id=%d' % ids
                        else:
                            sql = 'update admin_webnumber set zlexiconResidue=%d where id=%d' % (len(tuple_number), ids)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_zhineng.append(
                            [webname, ids, isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                    elif '-' == pattern:
                        # 查询 常规词库 url链接，关键字
                        if not lexicon:
                            print('\t\t\t\t\t\t\t\t\t\t\t\t错误:  网站: {}，常规词库未选择'.format(webname))
                            continue
                        sql = "select id,title,url,isActivate,web_id from admin_lexiconurl where isActivate=0 and web_id=%d limit %d" % (
                            lexicon, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_lexiconurl set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        # 查询剩余未发布数量
                        sql = 'select isActivate from admin_lexiconurl where isActivate=0 and web_id=%d' % lexicon
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        # 更改此网站的 剩余数量
                        if not result:
                            sql = 'update admin_lexicon set `number`=0 where id=%d' % lexicon
                        else:
                            sql = 'update admin_lexicon set `number`=%d where id=%d' % (len(tuple_number), lexicon)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_changgui.append(
                            [webname, str(ids) + 'l', isActivate, column, author, weblink, describe, isActivateTime,
                             ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                    elif '+' == pattern:
                        # 查询 智能词库 url链接，关键字
                        if not lexiconz:
                            print('\t\t\t\t\t\t\t\t\t\t\t\t错误:  网站: {}，智能词库未选择'.format(webname))
                            continue
                        sql = "select id,title,isActivate,web_id from admin_lexiconzhinengurl where isActivate=0 and web_id=%d limit %d" % (
                            lexiconz, number)
                        cursor.execute(sql)
                        result = cursor.fetchall()
                        if not result:
                            continue
                        # 更改 url 状态为 正在 采集
                        for dat_a in result:
                            sql = 'update admin_lexiconzhinengurl set isActivate=2 where id="%d"' % dat_a[0]
                            cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        # 查询剩余未发布数量
                        sql = 'select isActivate from admin_lexiconzhinengurl where isActivate=0 and web_id=%d' % lexiconz
                        cursor.execute(sql)  # 执行
                        tuple_number = cursor.fetchall()  # result是元
                        # 更改此网站的 剩余数量
                        if not result:
                            sql = 'update admin_lexiconzhineng set `number`=0 where id=%d' % lexiconz
                        else:
                            sql = 'update admin_lexiconzhineng set `number`=%d where id=%d' % (
                            len(tuple_number), lexiconz)
                        cursor.execute(sql)  # 执行
                        conn.commit()  # 提交事务
                        data_zhineng.append(
                            [webname, str(ids) + 'l', isActivate, column, author, weblink, describe, isActivateTime,
                             ratioimg, cms,
                             selecttitle, result])
                        lens += len(result)
                    elif pattern == '+-':
                        # 采集为双词库模式
                        # 查询 常规词库 url链接，关键字
                        if lexicon:
                            sql = "select id,title,url,isActivate,web_id from admin_lexiconurl where isActivate=0 and web_id=%d limit %d" % (
                                lexicon, number)
                            cursor.execute(sql)
                            result = cursor.fetchall()
                            if not result:
                                continue
                            # 更改 url 状态为 正在 采集
                            for dat_a in result:
                                sql = 'update admin_lexiconurl set isActivate=2 where id="%d"' % dat_a[0]
                                cursor.execute(sql)  # 执行
                            conn.commit()  # 提交事务
                            # 查询剩余未发布数量
                            sql = 'select isActivate from admin_lexiconurl where isActivate=0 and web_id=%d' % lexicon
                            cursor.execute(sql)  # 执行
                            tuple_number = cursor.fetchall()  # result是元
                            # 更改此网站的 剩余数量
                            if not result:
                                sql = 'update admin_lexicon set `number`=0 where id=%d' % lexicon
                            else:
                                sql = 'update admin_lexicon set `number`=%d where id=%d' % (len(tuple_number), lexicon)
                            cursor.execute(sql)  # 执行
                            conn.commit()  # 提交事务
                            data_changgui.append(
                                [webname, ids, isActivate, column, author, weblink, describe, isActivateTime, ratioimg,
                                 cms,
                                 selecttitle, result])
                            lens += len(result)
                        else:
                            print('\t\t\t\t\t\t\t\t\t\t\t\t错误:  网站: {}，双线词库模式中, 常规词库未选择'.format(webname))
                        # 查询 智能词库 url链接，关键字
                        if lexiconz:
                            sql = "select id,title,isActivate,web_id from admin_lexiconzhinengurl where isActivate=0 and web_id=%d limit %d" % (
                                lexiconz, number)
                            cursor.execute(sql)
                            result = cursor.fetchall()
                            if not result:
                                continue
                            # 更改 url 状态为 正在 采集
                            for dat_a in result:
                                sql = 'update admin_lexiconzhinengurl set isActivate=2 where id="%d"' % dat_a[0]
                                cursor.execute(sql)  # 执行
                            conn.commit()  # 提交事务
                            # 查询剩余未发布数量
                            sql = 'select isActivate from admin_lexiconzhinengurl where isActivate=0 and web_id=%d' % lexiconz
                            cursor.execute(sql)  # 执行
                            tuple_number = cursor.fetchall()  # result是元
                            # 更改此网站的 剩余数量
                            if not result:
                                sql = 'update admin_lexiconzhineng set `number`=0 where id=%d' % lexiconz
                            else:
                                sql = 'update admin_lexiconzhineng set `number`=%d where id=%d' % (
                                    len(tuple_number), lexiconz)
                            cursor.execute(sql)  # 执行
                            conn.commit()  # 提交事务
                            data_zhineng.append(
                                [webname, str(ids) + 'l', isActivate, column, author, weblink, describe, isActivateTime,
                                 ratioimg,
                                 cms,
                                 selecttitle, result])
                            lens += len(result)
                        else:
                            print('\t\t\t\t\t\t\t\t\t\t\t\t错误:  网站: {}，双线词库模式中, 智能词库未选择'.format(webname))
                else:
                    # print('网站: {}，今日文章已发表完成'.format(webname))
                    print('\t\t\t\t\t\t\t\t\t\t\t\t错误:  网站: {}，今日文章发表完成为空'.format(webname))
        except Exception as e:
            print(e)
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
        print('从数据库中查询到常规模式{}个网站链接,智能模式{}个网站链接,共{}条'.format(len(data_changgui), len(data_zhineng), lens))
        return data_changgui, data_zhineng

    def updateDate(self, data_list, state):
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port)  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        try:
            if state:
                date = datetime.datetime.now().strftime('%Y-%m-%d')
                # 发布成功的 数据
                for item in data_list:
                    try:
                        if not item[0] and not item[1]:
                            # 不是词库, 不是智能采集
                            sql = "update admin_mainurl set `date`='{}',`isActivate`=1 where id={}".format(date,
                                                                                                           item[2])
                            cursor.execute(sql)
                            sql = 'UPDATE admin_webnumber set numb= numb + 1 where id="%d"' % item[3]
                            cursor.execute(sql)
                        elif item[0] and not item[1]:
                            # 是词库, 不是智能采集
                            sql = "update admin_lexiconurl set `date`='{}',`isActivate`=1 where id={}".format(date,
                                                                                                              item[2])
                            cursor.execute(sql)
                            sql = 'UPDATE admin_webnumber set numb= numb + 1 where id="%d"' % item[3]
                            cursor.execute(sql)
                        elif item[0] and item[1]:
                            # 是词库, 是智能采集
                            if len(item) == 5:
                                sql = "update admin_lexiconzhinengurl set `date`='{}',`isActivate`=1,url='{}' where id={}".format(
                                    date, item[4], item[2])
                            else:
                                sql = "update admin_lexiconzhinengurl set `date`='{}',`isActivate`=1 where id={}".format(
                                    date, item[2])
                            cursor.execute(sql)
                            sql = 'UPDATE admin_webnumber set numb= numb + 1 where id="%d"' % item[3]
                            cursor.execute(sql)
                        elif not item[0] and item[1]:

                            # 不是词库, 是智能采集
                            if len(item) == 5:
                                sql = "update admin_mainurlzhineng set `date`='{}',`isActivate`=1,url='{}' where id={}".format(
                                    date, item[4], item[2])
                            else:
                                sql = "update admin_mainurlzhineng set `date`='{}',`isActivate`=1 where id={}".format(
                                    date, item[2])
                            cursor.execute(sql)
                            sql = 'UPDATE admin_webnumber set numb= numb + 1 where id="%d"' % item[3]
                            cursor.execute(sql)
                    except Exception as e:
                        print('插入数据库发生错误,', e, item)
            else:
                for webid, img_isActivate, column, author, weblink, describe, id, title, url, isActivate, errdescribe in data_list:
                    sql = """INSERT INTO `admin_errmainurl` (`TITLE`,`URL`,`WEB_ID`,`IDS`,`describe`) VALUES (%s,%s,%s,%s,%s)"""
                    cursor.executemany(sql, [title, weblink, webid, id, errdescribe])
            conn.commit()
        except Exception as e:
            print('插入成功上传的数据失败：{}', data_list, e)
            time.sleep(5)
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接

    def select_webname(self):
        '''
        获取 所有网站名称
        :return:
        '''
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port)  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        result = False
        try:
            sql = "select `name` from admin_webnumber"
            cursor.execute(sql)  # 执行
            result = cursor.fetchall()  # result是元
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
        return result

    def xpath(self):
        xpath_l = {}
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port)  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        try:
            # 查询网站数量
            sql = "select webdoma,xpath from admin_contentxpath"
            cursor.execute(sql)  # 执行
            result = cursor.fetchall()  # result是元
            for webdoma, xpath in result:
                xpath_l[webdoma] = xpath
        except Exception as e:
            print('修改数据库 url 时间失败：{}，ID：{}'.format(e, id))
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接
        return xpath_l

    def zero_stting(self):
        conn = pymysql.connect(self.host, self.user, self.pwd, self.dbname, port=self.port, charset='utf8')  # 连接数据库
        cursor = conn.cursor()  # 获取游标
        try:
            # sql = "update admin_mainurl set isActivate=0"
            # sql = 'ALTER TABLE `errmainurl` ADD UNIQUE(`ids`)'
            # cursor.execute(sql)
            sql = "update admin_webnumber set numb=0"
            cursor.execute(sql)
            conn.commit()
            print('========== *** 昨日下载数量置零完成 *** ===========')
        finally:
            cursor.close()  # 关闭游标
            conn.close()  # 关闭连接


class Redis_my(object):
    def __init__(self):
        self.r = redis.Redis(host=HOST, port=RedisPORT, db=0, decode_responses=True)
        self.pipe = self.r.pipeline()  # 减少对服务器的请求数  #减少服务器客户端之间连接损耗
        self.mysql_my = MySQL_My()
        self.webname_list = []  # 存放 mysql的 网站名称 便于从redis中查询
        self.all_web_data = []  # 存放 从 redis 中查询到的数据 [表名称,表数据] 用于删除redis上的数据

    def hash_set(self, data_changgui, mainurlzhineng):
        '''
        从 mysql 中插入数据至redis
        :param data_changgui:
        :return:
        '''
        for webname, webid, img_isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms, selecttitle, result in data_changgui:
            if webname not in self.webname_list:
                self.webname_list.append(webname)
            if not result:
                continue
            if 'l' in str(webid):
                # 词库模式
                webid = int(webid[:-1])
                for id, title, url, isActivate, web_id in result:
                    self.pipe.rpush('await:' + str(webname),
                                    [webid, img_isActivate, column, author, weblink, describe, isActivateTime,
                                     str(id) + 'l',
                                     title,
                                     url, isActivate, ratioimg, cms, selecttitle])
            else:
                for id, title, url, isActivate, web_id in result:
                    self.pipe.rpush('await:' + str(webname),
                                    [webid, img_isActivate, column, author, weblink, describe, isActivateTime, id,
                                     title,
                                     url, isActivate, ratioimg, cms, selecttitle])
                # self.pipe.hset('await:'+str(webname),
                #                get_md5(url),
                #                [webid,img_isActivate,column,author,weblink,describe,id,title,url,isActivate]
                #                )
            self.pipe.execute()
        for webname, webid, img_isActivate, column, author, weblink, describe, isActivateTime, ratioimg, cms, selecttitle, result in mainurlzhineng:
            if webname not in self.webname_list:
                self.webname_list.append(webname)
            if not result:
                continue
            if 'l' in str(webid):
                # 词库模式
                webid = int(webid[:-1])
                for id, title, isActivate, web_id in result:
                    self.pipe.rpush('zawait:' + str(webname),
                                    [webid, img_isActivate, column, author, weblink, describe, isActivateTime,
                                     str(id) + 'l',
                                     title,
                                     isActivate, ratioimg, cms, selecttitle])
            else:
                for id, title, isActivate, web_id in result:
                    self.pipe.rpush('zawait:' + str(webname),
                                    [webid, img_isActivate, column, author, weblink, describe, isActivateTime, id,
                                     title,
                                     isActivate, ratioimg, cms, selecttitle])
                # self.pipe.hset('await:'+str(webname),
                #                get_md5(url),
                #                [webid,img_isActivate,column,author,weblink,describe,id,title,url,isActivate]
                #                )
            self.pipe.execute()

    def zrem_my(self, flag):
        '''
        移除redis中的元素
        :param flag:
        :param data_list:
        :return:
        '''
        if flag:
            for webname, item in self.all_web_data:
                self.pipe.zrem(webname, item)

    def set_mysql(self):
        '''
        将发布成功的链接同步至数据库  未使用
        :return:
        '''
        data_list = []
        zrems = []
        for webname in self.webname_list:
            data = self.r.zrangebyscore(webname, 0, 2)
            if not data:
                continue
            else:
                zrems.append([])
                data_list.append(data)
                self.all_web_data.append([webname, data])
        if data_list:
            self.mysql_my.updateDate(data_list, state=True)
            self.zrem_my(flag=True)

    def select_redis_value0(self):
        '''
        查询 redis 表中是否还有未发布的链接
        :return:
        '''
        for webname in self.webname_list:
            data_changgui = self.r.llen('await:' + str(webname))
            if not data_changgui:
                continue
            else:
                return True
        return False

    def lpopOKWebsite(self):
        '''
        将发布成功的链接同步至数据库
        :return:
        '''
        number = self.r.llen('have_published')
        info = []
        for i in range(number):
            info.append(eval(self.r.lpop('have_published')))
        if info:
            self.mysql_my.updateDate(info, True)

    def main(self):
        self.lpopOKWebsite()
        webnames = self.mysql_my.select_webname()
        if webnames:
            for webname in webnames:
                self.webname_list.append(webname[0])
        # if not self.select_redis_value0():
        #     data_changgui = self.mysql_my.run()
        #     self.hash_set(data_changgui)
        #     print('添加完成',get_nowtime())
        # else:
        #     print('还有数据正在采集中',get_nowtime())
        data_changgui, mainurlzhineng = self.mysql_my.run()
        self.hash_set(data_changgui, mainurlzhineng)
        print('添加完成', get_nowtime())


if __name__ == '__main__':
    while True:
        # MySQL_My().zero_stting()
        # Redis_my().main()
        # time.sleep(3600)
        # time.sleep(3600)
        if datetime.datetime.now().hour == 0:
            MySQL_My().zero_stting()
        Redis_my().main()
        time.sleep(3600)

        path = 'files\\'
        for i in os.listdir(path):
            try:
                path_file = os.path.join(path, i)  # 取文件路径
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    for f in os.listdir(path_file):
                        path_file2 = os.path.join(path_file, f)
                        if os.path.isfile(path_file2):
                            os.remove(path_file2)
            except:
                continue
