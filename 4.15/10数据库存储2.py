# 修改想法 ，不再将全文保存到数据库，而是将txt文件的对应的文件序号名保存在数据库中
# 关键词分为俩个部分 分别为 全文的五个关键字 和 标题的 关键字

import mysql.connector

# 1. 连接数据库
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="chen123456",
  database="DB",
  charset = 'utf8mb4'  # 指定字符集为utf8mb4
)
mycursor = mydb.cursor()

# 2. 创建表格 分为 7个 字段 ，id和五个全文关键字和  文章序号  ，标题分词五个
mycursor.execute("CREATE TABLE dataTableChange1 (id INT AUTO_INCREMENT PRIMARY KEY,"
                 "key1 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "key2 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "key3 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "key4 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "key5 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "title1 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',"
                 "title2 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',"
                 "title3 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',"
                 "title4 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',"
                 "title5 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',"
                 "sentenceNum VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '')"
                 "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")

# filename = os.path.basename(file)   用于获取文件名


# 3. 读取每个文章，存入数据库中
import mysql.connector
import os
import glob
import jieba
import jieba.analyse
jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持

# def get_val(keys,titles,filename):  # 当获取的titles的分词少于5个时需要进行处理
#     num = len(titles)
#     if num == 1:
#         val = (keys[0],keys[1],keys[2],keys[3],keys[4],titles[0],filename)
#     elif num == 2:
#         val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1], filename)
#     elif num == 3:
#         val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1],titles[2], filename)
#     elif num == 4:
#         val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1], titles[2],titles[3],filename)
#     else:
#         val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0], titles[1],titles[2], titles[3],titles[4], filename)
#     return val


def get_val_sql(keys,titles,filename):  # 当获取的titles的分词少于5个时需要进行处理
    num = len(titles)
    if num == 1:
        val = (keys[0],keys[1],keys[2],keys[3],keys[4],titles[0],filename)
        sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,sentenceNum)" \
              " VALUES (%s,%s,%s,%s,%s, %s, %s)"
    elif num == 2:
        val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1], filename)
        sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,title2,sentenceNum)" \
              " VALUES (%s,%s,%s,%s,%s, %s,%s, %s)"
    elif num == 3:
        val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1],titles[2], filename)
        sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,title2,title3,sentenceNum)" \
              " VALUES (%s,%s,%s,%s,%s, %s,%s,%s, %s)"
    elif num == 4:
        val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0],titles[1], titles[2],titles[3],filename)
        sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,title2,title3,title4,sentenceNum)" \
              " VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s, %s)"
    else:
        val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0], titles[1],titles[2], titles[3],titles[4], filename)
        sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,title2,title3,title4,title5,sentenceNum)" \
              " VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s)"
    return val,sql


def read_txts(path):
    """
    读取每个文章，存入数据库中
    """
    txt_list = []
    # 获取所有txt文件的路径
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            f.seek(0)
            first_line = f.readline().strip()
            # 基于 TF-IDF 算法的关键词抽取
            keys = jieba.analyse.extract_tags(text, topK=6, withWeight=False, allowPOS=())
            # titles = jieba.cut_for_search(first_line) # 采用搜索引擎模式
            titles = jieba.analyse.extract_tags(first_line, topK=6, withWeight=False, allowPOS=())

            filename = os.path.basename(file)  # 获取文件名
            # sql = "INSERT INTO dataTableChange1 (key1,key2,key3,key4,key5,title1,title2,title3,title4,title5,sentenceNum)" \
            #       " VALUES (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s)"
            val,sql = get_val_sql(keys,titles,filename)
            # val = (keys[0], keys[1], keys[2], keys[3], keys[4], titles[0], titles[1], titles[2], titles[3], titles[4],filename)
            mycursor.execute(sql, val)

            mydb.commit()  # 提交



# read_txts("D:\\.8_python代码\\数据库\\科技")
read_txts("./科技分库")

# IndexError: list index out of range  超出范围，需要对titles数量进行分析

# mysql.connector.errors.ProgrammingError: Not enough parameters for the SQL statement
# val 改变的同时sql也改变


# mysql.connector.errors.DatabaseError: 1364 (HY000): Field 'title5' doesn't have a default value
# 需要在构建表的时候 设置默认值