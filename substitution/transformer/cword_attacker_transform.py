from typing import List
from pypinyin import lazy_pinyin
import opencc
import math
import random
from common import tools

'''
    CWordAttacker算法的替代
    论文：面向中文文本分类的词级对抗样本生成方法
'''
class CWordAttackerTransformer:

    def __init__(self) -> None:
        self.__converter = opencc.OpenCC('s2t.json')

    def candidate(self, word:str) -> str:
        num = random.randint(0,3)
        candidate = word
        if num == 0:
            candidate = self.__to_pinyin(word)
        elif num == 1:
            candidate = self.__to_traditional(word)
        elif num == 2:
            candidate = self.__reverse(word)
        else:
            candidate = self.__scatter_punctuation(word)
        tools.show_log(f'**** random = {num} | {word} --> {candidate}')
        return candidate  
    

    def __to_pinyin(self, word:str) -> str:
        result = ''.join(lazy_pinyin(word))
        return result


    def __to_traditional(self, word:str) -> str:
        result = self.__converter.convert(word)
        return result

    def __reverse(self, word:str) -> str:
        char_list = list(word)
        size = len(char_list)
        if size <= 1:
            return word
        elif size <= 2:
            char_list.reverse()
            result = ''.join(char_list)
            return result
        else:
            char_list_part1 = char_list[0:2]
            char_list_part2 = char_list[2:size]
            char_list_part1.reverse()
            result1 = ''.join(char_list_part1)
            result2 = ''.join(char_list_part2)
            return f'{result1}{result2}'

    def __scatter_punctuation(self, word:str) -> str:
        char_list = list(word)
        insert_index = math.floor(len(char_list) / 2)
        char_list.insert(insert_index, '。')
        result = ''.join(char_list)
        return result
        