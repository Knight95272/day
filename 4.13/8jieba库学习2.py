# 采用jieba库提取关键字

import jieba

vocab = {} # 词表
cs = {} # 字表
text = ''
with open    ('./科技分库/481650.txt', 'r', encoding='utf-8', errors='ignore') as file:
    for line in file:
        line = line.strip()
        text += line
        # 处理字
        for c in line:
            cs[c] = 0
        # 分词
        for word in jieba.cut(line):
            vocab[word] = 0 # 去重
    # print(vocab)
    # print(vocab.keys())
    # print(cs.keys())


# UnicodeDecodeError: 'gbk' codec can't decode byte 0xad in position 28: illegal multibyte sequence
# gbk解码器去解码utf-8的字符串  需要指定文本的打开方式  encoding='gbk'
# 采用errors = 'ignore' 得到的结果编码错误  属于忽视特殊字符
# 文件格式是utf-8 所以编码器采用utf-8

# 保存字表
with open('testZi.txt','w') as csf:
    for c in cs.keys():
        csf.write(c)

# 保存词表
with open('testCi.txt','w') as csf:
    for c in vocab.keys():
        csf.write(c+'\t')

# 基于textRand的关键字提取
import jieba.analyse
# withWeight 权重
res = jieba.analyse.textrank(text,topK=5,withWeight=True)
# print(res)

# 基于 TF-IDF 算法的关键词抽取
res1 = jieba.analyse.extract_tags(text, topK=5, withWeight=True, allowPOS=())
# print(res1)

# ['运营商', '网络', '业务', '方面', '全球']
# ['GPON', 'EPON', '摩托罗拉', '运营商', 'FTTH']
# 可见基于TF-IDF的关键词抽取得到的效果更好

# 根据词性再次测试
res2 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='n') # 普通名词
res3 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='f') # 方位名词
res4 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='v') # 动词
res5 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='a') # 形容词
res6 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='PER') # 人名
res7 = jieba.analyse.extract_tags(text, topK=5, withWeight=False, allowPOS='LOC') # 地名
# print(res2)
# print(res3)
# print(res4)
# print(res5)
# print(res6)
# print(res7)

# 采用paddle模式
# 利用PaddlePaddle深度学习框架，训练序列标注（双向GRU）网络模型实现分词。同时支持词性标注。
# paddle模式使用需安装paddlepaddle-tiny，pip install paddlepaddle-tiny==1.6.1
jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
for str in strs:
    seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
    print("Paddle Mode: " + '/'.join(list(seg_list)))

seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print("Full Mode: " + "/ ".join(seg_list))  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式

seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print(", ".join(seg_list))