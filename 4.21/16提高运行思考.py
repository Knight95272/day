# 1. 将数据库中存储的数据转换为序列数据以供使用
# 2. 并行处理，多线程
# 从而减少搜索时间
# 测试将十个关键字组成句子计算余弦相似度

# SimCSE 模型
# 如何构建俩个句子的正样本
# dropout 随机将一个句子的特征去除  同个句子运行俩遍，都是随机去除部分特征，则这俩个句子为互为正样本

# SimCSE 模型是对句子进行判断相似度
# 直接将标题句子和txt名字存入数据库进行
# 通过构建一个列表，一个字典存储映射即可




import numpy as np
# 向量的维度和长度应当相同，否则计算余弦相似度时可能会出错。

def cosine_similarity(v1, v2):
    """
    计算两个向量的余弦相似度
    :param v1: 向量1
    :param v2: 向量2
    :return: 余弦相似度
    """
    dot_product = np.dot(v1, v2)  # 向量点乘
    norm_v1 = np.linalg.norm(v1)  # 向量的模
    norm_v2 = np.linalg.norm(v2)  # 向量的模
    similarity = dot_product / (norm_v1 * norm_v2)  # 余弦相似度
    return similarity

# 示例用法
v1 = np.array([1, 2, 3])
v2 = np.array([4, 5, 6])
similarity = cosine_similarity(v1, v2)
print("余弦相似度：", similarity)
