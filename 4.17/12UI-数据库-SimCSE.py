# 1. 导入库
import PySimpleGUI as sg
from model1 import get_res
from model1 import get_file
# from sort import getRes
# print(sg.theme_list())  # 主题名称

sg.theme('Dark2') # 不填主题名称时为随机主题
# text1 = '''结果显示区域'''
# 2. 定义行数，确定行数
layout = [
    [sg.Text('请输入要检索的内容'),sg.InputText('O2将为两款手机操作系统提供移动支付服务')],

    [sg.Text('结果1'),sg.ML(
                           disabled=True, # 元素禁用状态设定  True 只读模式
                           border_width=None, # 边界线条宽度设定
                           size = (50,6), # 宽度和行高设定
                           background_color=None, # 背景颜色设定
                           text_color=None,  # 文本颜色确定
                           reroute_cprint=True, # 通过cprint将内容打印到此文本框中
                           do_not_clear=True, # 窗口读取一次，内容自动清除
                           key='text1')], # 元素的唯一标识符
    [sg.Text('结果2'),sg.ML(
                           disabled=True,
                           border_width=None,
                           size = (50,6),
                           background_color=None,
                           text_color=None,
                           reroute_cprint=True,
                           do_not_clear=True,
                           key='text2')],
    [sg.Text('结果3'),sg.ML(
                           disabled=True,
                           border_width=None,
                           size = (50,6),
                           background_color=None,
                           text_color=None,
                           reroute_cprint=True,
                           do_not_clear=True,
                           key='text3')],
    [sg.Button('确认')]
]
# 3. 创建窗口
window = sg.Window('语义检索系统', layout)
# 4. 事件循环
while True:
    event,values = window.read() # 窗口的读取，俩个返回值（事件，值）

    if event=='确认':
        # sg.Popup('点击了确认') # 弹窗
        # print(values) # values 包含了所有文本框的变量
        # 可以通过索引获取单个  values[0]
        # print(values[0])
        searchValue = values[0] # 保存检索值
        res = get_res(searchValue)
        # 当前获取的res只是文件名需要根据文件名打开文件，放入结果

        # res1,res2,res3 = getRes(searchValue)
        # return searchValue
        # sg.cprint(searchValue) # 打印到对应文本框
        window['text1'].update(  # 输出文本框元素更新(相当于打印)
            value=get_file('./科技分库',res[0]),  # 输出值
            disabled=True,  # 元素禁用

        )
        window['text2'].update(
            value=get_file('./科技分库',res[1]),
            disabled=True,
        )
        window['text3'].update(
            value=get_file('./科技分库',res[2]),
            disabled=True,
        )

    if event==None: # 窗口关闭事件
        break
    # if event==sg.WIN_CLOSED: # 窗口关闭事件
    #     break

# 关闭窗口
window.close()


