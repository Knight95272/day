# 1. 首先需要安装库  pip install mysql-connector-python
# 连接前需要在管理中打开MySQL服务


# 2. 连接MySQL数据库，使用MySQL Connector Python提供的connect()方法连接到MySQL数据库。
import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="chen123456",
  database="DB",
  charset = 'utf8mb4'  # 指定字符集为utf8mb4
)
mycursor = mydb.cursor()

# 3. 创建表格，使用execute()方法执行CREATE TABLE语句以创建新表格。
# mycursor.execute("CREATE TABLE mytable (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), sentence VARCHAR(255))")

mycursor.execute("CREATE TABLE mytable (id INT AUTO_INCREMENT PRIMARY KEY,"
                 "title VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,"
                 "sentence TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL)"
                 "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
# 创建了一个名为mytable的新表格，该表格包含id，title和sentence三个字段。

# 4. 插入数据，您可以使用execute()方法插入数据到表格中。
sql = "INSERT INTO mytable (title, sentence) VALUES (%s, %s)"
val = ("标题", "这是一条句子。")
mycursor.execute(sql, val)

mydb.commit()   # 提交

print(mycursor.rowcount, "record inserted.")

# 5. 关闭连接
mydb.close()

