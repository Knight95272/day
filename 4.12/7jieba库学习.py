# 1. 安装jiaba库  pip install jieba

# 2. 导入
import jieba

# 3. 基本分词
text = "我喜欢自然语言处理"
# 基础 将一个字符串分割成单个词语
words1 = jieba.cut(text)
# 全模式分词  将一个字符串中所有可能的词语都分出来
words2 = jieba.cut(text, cut_all=True)
# 搜索引擎模式分词  将一个字符串中较长的词语尽量分出来
words3 = jieba.cut_for_search(text)

print("1 基础")
for word in words1:
    print(word)

print("2 全模式")
for word in words2:
    print(word)

print("3 搜索")
for word in words3:
    print(word)


