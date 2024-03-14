from typing import List
import OpenHowNet
from common import tools

class LANGUAGE:
    ZH = 'zh'
    EN = 'en'

'''
    BabelNet同义词集
'''
class BabelNetBuilder:

    def __init__(self) -> None:
        self.__hownet_dict_advanced = OpenHowNet.HowNetDict()
        self.__hownet_dict_advanced.initialize_babelnet_dict()


    def synonyms(self, word:str, pos:str):
        synonym_list = self.__synonyms(word, pos)
        return synonym_list

    
    '''
        pos: Can be set to a/v/n/r
        使用单词原型,否则babelnet无法识别
        TODO 需要性能优化
    '''
    def __synonyms(self, lemma:str, word_pos:str):
        candidate_list = []
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH)
            tools.show_log(f'synonyms_list = {synonyms_list}')
            for synonyms in synonyms_list:
                if synonyms.pos == word_pos:
                    for syn_zh in synonyms.zh_synonyms:
                        if syn_zh not in candidate_list:
                            candidate_list.append(syn_zh)
         
        tools.show_log(f'BabelNetBuilder ｜ candidate_list of {word_pos} = {candidate_list}')      
        return candidate_list
    