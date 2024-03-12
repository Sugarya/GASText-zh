
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


def similary_words(word1: str, word2: str) -> float:

    pass

def similary_sentences(sentence1: str, sentence2: str) -> float:
    
    pass