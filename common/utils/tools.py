
from config import Pattern, KEY



def show_log(content):
    if Pattern.isDebug:
        print(content)


'''
    @example：数据集文件的一行内容
    @return：(, isValid)
'''
def filter_example(example, style):
    label, text = int(example[0]), example[1]
    if style == KEY.Chinanews:
        label, text = int(example[0]), f'{example[1]}{example[2]}'
    return label, text
