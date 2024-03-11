
from config import Pattern



def show_log(content):
    if Pattern.isDebug:
        print(content)


'''
    @example：数据集文件的一行内容
    @return：(, isValid)
'''
def filter_example(example):
    label, text = int(example[0]), example[1]
    return label, text
