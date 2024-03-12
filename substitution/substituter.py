from typing import List
from .synonym import HownetBuilder

'''
    使用不同的方式生成替代词，如同义词，语言淹码模型，拼音，繁体字等
'''
class Substituter:

    def __init__(self) -> None:
        self.__hownet_builder = HownetBuilder()
        

    def generate_synonyms(self, word:str, pos:str):
        return self.__hownet_builder.generate_synonyms(word, pos)
        
