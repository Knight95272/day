# 根据检索值对 数据库中每一行元素进行匹配，将最优的3个获取
# 是否也需要对检索值进行分词？
# 数据库可以修改为 科技领域的某个特定领域的百科全书

# 1. 对检索值进行分词， 或者提取检索值
import jieba.analyse
text = "乔布斯病情引担忧 投资者要董事会公开详情"
# 基于 TF-IDF 算法的关键词抽取
res1 = jieba.analyse.extract_tags(text, topK=2, withWeight=False, allowPOS=())
print(res1)  # [('石墨', 1.4320683257616666), ('强度', 1.1502091974116666)]

# 2. 根据获得的检索值在数据库中进行搜索
# 2.1  将数据库中的内容按 文件名（key） ： 关键字10个(value  列表)（5个全文，5个标题） 的字典形式保存
# 2.2  字典中的value 10个关键字组成的列表   与  检索值提取出的俩个关键字通过计算余弦相似度进行匹配 ，得到俩个最优的余弦相似度相加保存为sum
# 2.3  构建新字典 key：value 为 文件名:sum
# 2.4  对sum进行排序，将最优的三个余弦相似度和的三个结果获得

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

# 从数据库中读取数据
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

# # 输出字典
# print(data_dict)  '481650.txt': ['GPON', 'EPON', '摩托罗拉', '运营商', 'FTTH', 'GPON', 'FTTH', 'EPON', '中比', '摩托罗拉']


# 2.2  字典中的value 10个关键字组成的列表   与  检索值提取出的俩个关键字通过计算余弦相似度进行匹配 ，得到俩个最优的余弦相似度相加保存为sum
# 2.3 构建新字典 key：value 为 文件名:sum
import torch
from simcse import SimCSE

model = SimCSE("princeton-nlp/sup-simcse-bert-base-uncased")

# 余弦相似度
# sentences_a = ['A woman is reading.', 'A man is playing a guitar.']
# sentences_b = ['He plays guitar.', 'A woman is making a photo.']
# similarities = model.similarity(sentences_a, sentences_b)  # 余弦相似度   [-1,1]  越靠近1相似度越大，越靠近-1相似度越小
# print(similarities)
# # 3. 将句子作为索引，进行搜索
# sentences = ['A woman is reading.', 'A man is playing a guitar.','A woman is playing a guitar.','man is playing a guitar.']
# model.build_index(sentences) # 构建索引
# results = model.search("He plays guitar.")  # 结果包含相似的结果，以及其余弦相似度
# print(results)
# 2.2  修改，不再采用俩俩比较，而是直接将values作为索引
# def get_max(searchs,values):  # 获取俩个检索值与当前这一列元素的最大余弦相似度
#     max_similar1 = -1
#     max_similar2 = -1
#     for var in values:
#         # 进行对比
#         similar1 = model.similarity(var,searchs[0])
#         similar2 = model.similarity(var,searchs[1])
#         # 保留最大值
#         if similar1 > max_similar1:
#             max_similar1 = similar1
#         if similar2 > max_similar2:
#             max_similar2 = similar2
#     return max_similar1+max_similar2  # 返回最大值之和

#  目前问题 采用jieba库进行分词的话出现搜索值不准确的情况下
#  该情况下  jieba会去除错别字   原：董事会   改：董事回   jieba: 董事
#  其次未对获取检索值的数量小于需要判定的数量的情况进行判断
#  ['乔布斯']    IndexError: list index out of range




def get_max2(searchs,values):  # 而是直接将values作为索引
    model.build_index(values)  # 构建索引
    if len(searchs) == 2:
        max_similar1 = model.search(searchs[0])  # 结果包含相似的结果，以及其余弦相似度
        max_similar2 = model.search(searchs[1])
        return max_similar1[0][1] + max_similar2[0][1]  # 返回最大值之和  第一个元素的余弦相似度 [0][1]
    else:
        return model.search(searchs[0])


# 2.3
similar_dict = {}
for key, value in data_dict.items():
    similar_dict[key] = get_max2(res1,value)
print(similar_dict)



# 缺点，运行时间过长
# 修改，将检索值直接与所有元素列表进行匹配，（不采用一个个获取余弦相似度），将得到最优的三个结果获取
# 获取方法，根据value对应的key值确定三篇文章
# 或者采用减少数据量的做法


# 2.4  对sum进行排序，将最优的三个余弦相似度和的三个结果获得

# # 当前数据量少，采用插入排序
# # sorted_dict = {}
# def get_sorted_dict(similar_dict):
#     for i in range(1,len(similar_dict)):
#         temp = similar_dict[i]
#         j = i-1
#         # 倒序遍历有序数组，将无序元素插入
#         while j>=0 and similar_dict[j]>temp:
#             similar_dict[j+1] = similar_dict[j]
#             j-=1
#         similar_dict[j+1] = temp
#     return similar_dict

sorted_dict = sorted(similar_dict.items(), key=lambda item: item[1], reverse=True)
# sorted()函数中的key=lambda item: item[1]表示按照字典中value的值进行排序，reverse=True表示按照降序排序
# print(sorted_dict)
# print(sorted_dict[:3])
top_three = [key for key, value in sorted_dict[:3]]  # 取前三个key值 放入列表
# print(top_three)
# [('481651.txt', 1.7407985925674438), ('481659.txt', 1.7355926632881165), ('481660.txt', 1.7341349124908447)]
# ['481651.txt', '481659.txt', '481660.txt']

#最后根据文件名打开文件，将内容放入UI界面即可
