import os
import xlrd
import pymysql

def listdir(path): #传入根目录
    if os.path.splitext(path)[1] == '.xls' or os.path.splitext(path)[1] == '.xlsx':  # 判断文件是否是Excel文件
        return path #返回Excel文件路径列表

def parse(file_path):
    file = xlrd.open_workbook(file_path)
    sheet_1 = file.sheet_by_index(0)
    report_name = sheet_1.row_values(2) #获取报表名称行数据
    row_num = sheet_1.nrows #获取行数
    report_num = sheet_1.ncols #获取列数
    data_list = [] # 存放数据
    for i in range(3,row_num): #循环每一行数据
        row = sheet_1.row_values(i) #获取行数据
        data = {}
        data['key']= "".join(row[0].split()) # 关键字
        data['url'] = "".join(str(row[1]).split()) # url链接
        # dict['partment'] = "".join(row[2].split()) #部门
        # dict['office'] = "".join(row[3].split()) #科室
        for j in range(2,report_num):
            if row[j] is not '': #如果行内没有数据，则对应报表名称无权限，设为0，否则为1
                data[report_name[j]] = 1
            else:
                data[report_name[j]] = 0
        data_list.append(data)
    insert_db(data_list)

def insert_db(data_list):
    db = pymysql.connect('localhost','root','root','python_gather')
    cusor = db.cursor()
    data=[]
    for data_d in data_list:
        data.append((data_d['key'],data_d['url'],0,0,1))
    sql = """INSERT INTO `MAINURL` (`TITLE`,`URL`,`AUTHOR`,`isActivate`,`date`,`WEB_ID`) VALUES (%s,%s,%s,%s,NOW(),%s)"""
    try:
        cusor.executemany(sql,data) #sql执行
        db.commit() #提交到数据库
    except Exception as e: #获取报错信息
        print(e)
    db.close()


if __name__ == '__main__':
    path = r'keyurl.xlsx'
    file_name = listdir(path)
    f = open('portal.txt','w',encoding='utf-8')
    print(file_name)
    print('start translating', file_name)
    parse(file_name)
    print('translate complete', file_name)
    # for file_name in file_list:
    #     print('start translating',file_name)
    #     parse(file_name)
    #     print('translate complete',file_name)
    f.close()
