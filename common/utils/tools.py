
from config import Pattern, KEY
from common import AdvText, TokenStyle, SubstituteState
from nltk.corpus import wordnet as wn
from typing import List, Tuple


def show_log(content):
    if Pattern.IsDebug:
        print(content)

'''
    @example：数据集文件的一行内容
    @return：(, isValid)
'''
def filter_example(example, style) -> Tuple[int, str]:
    label, text = None, None
    if style == KEY.Chinanews:
        label, text = int(example[0]) - 1, f'{example[1]}{example[2]}'
    else:
        label, text = int(example[0]), f'{example[1] }'   
    return label, text

'''
    生成当前最新的文本
'''
def generate_latest_text(adv_text: AdvText) -> str:
    display_list = [None] * adv_text.token_count
    for index, token_unit in enumerate(adv_text.token_units):                
        if token_unit.style == TokenStyle.WORD_SUBSTITUTE:
            if token_unit.substitute_unit.state == SubstituteState.WORD_REPLACING:
                display_list[index] = token_unit.substitute_unit.exchange_word
            elif token_unit.substitute_unit.state == SubstituteState.WORD_REPLACED:
                display_list[index] = token_unit.substitute_unit.exchange_max_greedy_word
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
    
# def to_hownet_pos(pos:str):
#     upper_pos = pos.upper()
#     if upper_pos.startswith('J') or upper_pos.startswith('A'):
#         return wn.ADJ
#     elif upper_pos.startswith('V'):
#         return wn.VERB
#     elif upper_pos.startswith('N'):
#         return wn.NOUN
#     elif upper_pos.startswith('R'):
#         return wn.ADV
#     else:
#         return None

def similary_words(word1: str, word2: str) -> float:

    pass

def similary_sentences(sentence1: str, sentence2: str) -> float:
    
    pass