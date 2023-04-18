def get_res(search_value):
    # 改错
    import pycorrector
    def get_corrected(searchValue):  # 改错
        if len(searchValue) == 2:
            corrected1 = pycorrector.correct(searchValue[0])
            corrected2 = pycorrector.correct(searchValue[1])
            return [corrected1[0], corrected2[0]]
        else:
            return pycorrector.correct(searchValue[0])[0]

    # 1. 对检索值进行分词， 或者提取检索值
    import jieba.analyse
    text = search_value
    # 基于 TF-IDF 算法的关键词抽取
    key_word = jieba.analyse.extract_tags(text, topK=2, withWeight=False, allowPOS=())
    print(key_word)  #
    corrected_key_word = get_corrected(key_word)
    print(corrected_key_word)



    # 2.1  将数据库中的内容按 文件名（key） ： 关键字10个(value  列表)（5个全文，5个标题） 的字典形式保存
    import mysql.connector
    mydb = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      password="chen123456",
      database="DB",
      charset = 'utf8mb4'  # 指定字符集为utf8mb4
    )
    mycursor = mydb.cursor()

    # 从数据库中读取数据    采用较少数据库
    query = ("SELECT id, key1, key2, key3, key4, key5, title1, title2, title3, title4, title5, sentenceNum FROM dataTableChange1")
    mycursor.execute(query)

    # 将读取的数据保存到字典中
    data_dict = {}
    for (id, key1, key2, key3, key4, key5, key6, key7, key8, key9, key10, sentenceNum) in mycursor:
        key_list = [key1, key2, key3, key4, key5, key6, key7, key8, key9, key10]
        data_dict[sentenceNum] = key_list

    # 关闭数据库连接
    mycursor.close()
    mydb.close()


    # 2.2  字典中的value 10个关键字组成的列表   与  检索值提取出的俩个关键字通过计算余弦相似度进行匹配 ，得到俩个最优的余弦相似度相加保存为sum
    # 2.3 构建新字典 key：value 为 文件名:sum
    import torch
    from simcse import SimCSE

    model = SimCSE("princeton-nlp/sup-simcse-bert-base-uncased")

    def get_max2(searchs, values):  # 而是直接将values作为索引
        model.build_index(values)  # 构建索引
        if len(searchs) == 2:
            # pycorrector.correct(searchs[0])
            max_similar1 = model.search(searchs[0])  # 结果包含相似的结果，以及其余弦相似度
            max_similar2 = model.search(searchs[1])
            return max_similar1[0][1] + max_similar2[0][1]  # 返回最大值之和  第一个元素的余弦相似度 [0][1]
        else:  # 对小于1的情况进行直接跳过
            return model.search(searchs[0])

    # 2.3
    similar_dict = {}
    for key, value in data_dict.items():
        similar_dict[key] = get_max2(corrected_key_word,value)
    # print(similar_dict)

    sorted_dict = sorted(similar_dict.items(), key=lambda item: item[1], reverse=True)

    top_three = [key for key, value in sorted_dict[:3]]  # 取前三个key值 放入列表
    # print(top_three)
    # [('481651.txt', 1.7407985925674438), ('481659.txt', 1.7355926632881165), ('481660.txt', 1.7341349124908447)]
    # ['481651.txt', '481659.txt', '481660.txt']

    #最后根据文件名打开文件，将内容放入UI界面即可
    return top_three

def get_file(path,filename):  # 根据文件名获取文件内容
    import os

    folder_path = path  # 指定文件夹路径
    file_name = filename  # 指定文件名

    file_path = os.path.join(folder_path, file_name)  # 拼接文件路径

    if os.path.exists(file_path):  # 判断文件是否存在
        with open(file_path, 'r',encoding='utf-8') as f:  # 打开文件并读取内容
            content = f.read()
        return content
            # print(content)
    # else:
    #     # print("文件不存在")   不存在的情况直接跳过



# UnicodeDecodeError: 'gbk' codec can't decode byte 0xac in position 12: illegal multibyte sequence
# 打开时注意编码格式即可