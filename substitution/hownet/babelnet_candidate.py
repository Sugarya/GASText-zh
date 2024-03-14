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
    '''
    def __synonyms(self, lemma:str, word_pos:str):
        syn_list = []
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH)
            tools.show_log(f'synonyms = {synonyms}')
            for syn in synonyms:
                if syn.pos == word_pos:
                    syn_list.extend(syn.zh_synonyms)
        syn_list = list(set(syn_list))            
        tools.show_log(f'syn_list of {word_pos} = {syn_list}')      
        return syn_list
    