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


# import jieba.analyse
# lines = []
# with open('my_list.txt', 'r',encoding='utf-8') as f:
#     content = f.readlines()
#     for line in content:
#         line  = jieba.analyse.extract_tags(line.strip(), topK=5, withWeight=False, allowPOS=())
#         lines.append(line)
#     # lines = [line.strip() for line in content]
#
# # res1 = jieba.analyse.extract_tags(text, topK=5, withWeight=True, allowPOS=())
# print(lines)
# # [('GPON', 1.9924612504833332), ('FTTH', 1.9924612504833332),
# #   ('EPON', 1.9924612504833332), ('中比', 1.8174908964), ('摩托罗拉', 1.7340283484166665)]

# 2. 将文本导入存储在列表中
import os
import glob


def get_list(path):
    """
    读取每个文章，存入列表
    """
    txt_list = []
    text = []
    # 获取所有txt文件的路径
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                text += line

            txt_list.append([text])
    return txt_list

my_list = get_list("./科技分库")
# print(my_list)  过大打印不出


# 3. 创建表格 分为 7个 字段 ，id和五个关键字和文章全文
# mycursor.execute("CREATE TABLE dataTable (id INT AUTO_INCREMENT PRIMARY KEY,"
#                  "key1 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key2 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key3 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key4 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key5 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "sentence TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL)"
#                  "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")

# 4. 采用jiaba进行分词


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


# 2. 创建表格 分为 7个 字段 ，id和五个关键字和文章全文
# mycursor.execute("CREATE TABLE dataTable (id INT AUTO_INCREMENT PRIMARY KEY,"
#                  "key1 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key2 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key3 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key4 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "key5 VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
#                  "sentence TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL)"
#                  "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")


# 3. 将文本导入存储在数据库中
import os
import glob
import jieba.analyse

def read_txts(path):
    """
    读取每个文章，存入数据库中
    """
    txt_list = []
    text = ''
    # 获取所有txt文件的路径
    txt_files = glob.glob(os.path.join(path, "*.txt"))
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                text += line
            # 基于 TF-IDF 算法的关键词抽取
            keys = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS=())

            sql = "INSERT INTO dataTable (key1,key2,key3,key4,key5,sentence) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (keys[0],keys[1],keys[2],keys[3],keys[4],text.encode('utf-8'))
            mycursor.execute(sql, val)
    mydb.commit()  # 提交

my_list = read_txts("D:\\.8_python代码\\数据库\\科技")


# 还不能关闭连接
# AttributeError: 'list' object has no attribute 'decode'   # 需要在分词之前转换为str类型