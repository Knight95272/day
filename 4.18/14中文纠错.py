#  目前问题 采用jieba库进行分词的话出现搜索值不准确的情况下
#  该情况下  jieba会去除错别字   原：董事会   改：董事回   jieba: 董事

# 导入中文纠错库
# pip install pycorrector  先安装
# import os
#
# # 设置语言模型文件存储位置
# os.environ['PYCORRECTOR_HOME'] = 'D:\pycorrector'

import pycorrector
import jieba

# 创建纠错器对象
# 纠错操作
# corrector = Corrector()
#
# # 进行纠错
# search_value = "董事回"
# corrected_search_value = corrector.correct(search_value)
# print(corrected_search_value) # ('董事回', [])
#
# # 使用jieba进行分词
# seg_list = jieba.cut(corrected_search_value)
# print(seg_list)
# 纠正文本中的错别字
corrected_text = pycorrector.correct('我是中文用戶。')
print(corrected_text[0])  # 我是中文用户。
corrected_text = pycorrector.correct('董事荟')
print(corrected_text)  # ('董事荟', [])  不存在修改 检测不到





#  其次未对获取检索值的数量小于需要判定的数量的情况进行判断
#  ['乔布斯']    IndexError: list index out of range

#
# import torch
# from simcse import SimCSE
#
# model = SimCSE("princeton-nlp/sup-simcse-bert-base-uncased")
#
# def get_max2(searchs,values):  # 而是直接将values作为索引
#     model.build_index(values)  # 构建索引
#     if len(searchs) == 2:
#         max_similar1 = model.search(searchs[0])  # 结果包含相似的结果，以及其余弦相似度
#         max_similar2 = model.search(searchs[1])
#         return max_similar1[0][1] + max_similar2[0][1]  # 返回最大值之和  第一个元素的余弦相似度 [0][1]
#     else:
#         return model.search(searchs[0])