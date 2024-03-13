from typing import List
import OpenHowNet
from common import tools

class LANGUAGE:
    ZH = 'zh'
    EN = 'en'

class HownetBuilder:

    def __init__(self) -> None:
        self.__hownet_dict_advanced = OpenHowNet.HowNetDict()
        # self.__hownet_dict_advanced.initialize_babelnet_dict()


    def synonyms(self, word:str, pos:str):
        synonym_list = self.__synonyms(word, pos)
        tools.show_log(f'synonym_list = {synonym_list}')
        return synonym_list

    
    
    '''
        pos: Can be set to a/v/n/r
        使用单词原型,否则babelnet无法识别
    '''
    def __synonyms(self, lemma:str, word_pos:str):
        syn_list = []
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms = self.__hownet_dict_advanced.get_synset(lemma, pos = word_pos, language = LANGUAGE.ZH)
            tools.show_log(f'synonyms = {synonyms}')
            for syn in synonyms:
                syn_list.extend(syn.zh_synonyms)
        return list(set(syn_list))