
from config import Pattern, KEY
from common import AdvText, TokenStyle, SubstituteState



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

'''
    生成当前最新的文本
'''
def generate_latest_text(adv_text: AdvText) -> str:
    display_list = [None] * len(adv_text.token_units)
    for index, token_unit in enumerate(adv_text.token_units):                
        if token_unit.style == TokenStyle.WORD_SUBSTITUTE:
            if token_unit.substitute_unit.state == SubstituteState.WORD_REPLACING:
                display_list[index] = token_unit.substitute_unit.exchange_word
            elif token_unit.substitute_unit.state == SubstituteState.WORD_REPLACED:
                display_list[index] = token_unit.substitute_unit.candidate_max_word
            else:
                display_list[index] = token_unit.origin_token 
        else:
            display_list[index] = token_unit.origin_token
    text = ''.join(display_list)
    return text

'''
    生成一个词元变动的文本，比如Masked场景
'''
def generate_text(adv_text: AdvText) -> str:
    display_list = [None] * len(adv_text.token_units)
    for index, token_unit in enumerate(adv_text.token_units):                
        if token_unit.style == TokenStyle.WORD_SUBSTITUTE:
            if token_unit.substitute_unit.state == SubstituteState.WORD_REPLACING:
                display_list[index] = token_unit.substitute_unit.exchange_word
            else:
                display_list[index] = token_unit.origin_token   
        else:
            display_list[index] = token_unit.origin_token
    text = ''.join(display_list)
    return text
    


def similary_words(word1: str, word2: str) -> float:

    pass

def similary_sentences(sentence1: str, sentence2: str) -> float:
    
    pass