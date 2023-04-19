# 循环神经网络  RNN
# 前部序列的信息处理后，作为输入信息传递到后续序列
# the courses are taught by flare zhao and David Chen
# 0   0     0   0   0   1   1   0   1   1   0
# 词汇数值化  建立   词汇key-数值value   对应字典   将输入词汇 转化为  数值矩阵
#  one-hot 独热编码    根据数值的大小 确定独热编码中1的位置

# RNN 结构
# 多输入单输出 ：情感识别   单输入多输出 ： 序列数据生成器 文章生成  音乐生成
# 多输入多输出：语言翻译
# 当前采用的语义系统属于 单输入多输出  一个检索值
# 普通RNN缺点  前部信息传递到后部时，信息权重下降,导致信息丢失

# 提高前部特定信息权重的改善   长短期记忆网络 LSTM
# 增加一个项 记忆细胞  用于传递前部信息
# 采用优点   网络结构深时，也可保留重要信息


# 双向循环神经网络 （BRNN）
# 做判断时，会将后部序列信息也考虑
# 多包含一个从后向前的部分


# 深度循环神经网络 (DRNN)
# 将单层RNN叠加 或者 输出前与普通mlp 结构结合使用

import numpy as np
# 提取序列
def extract_data(data,slide):   # slide 数据分成几分
    x = []
    y = []
    for i in range(len(data) - slide):
        x.append([a for a in data[i:i+slide]])
        y.append(data[i+slide])
    x = np.array(x)
    x = x.reshape(x.shape[0],x.shape[1],1)
    return x,y


from keras.models import Sequential
from keras.layers import Dense,SimpleRNN
model = Sequential()
# 增加一个RNN层
model.add(SimpleRNN(units=5,  # 输出
                    input_shape=(X.shaple[1],X.shape[2]), # 格式
                    activation='relu')) # 激活函数
# input_shape  = (samples,time_steps,features)  样本数量 ，序列长度，样本的特征维数  [0,0,1]  对应3
# 增加输出层
model.add(Dense(units=1,activation='linear'))
model.compile(optimizer='adam',loss='mean_squared_error')  # 配置   优化器/损失函数








