from typing import List
import OpenHowNet
from common import tools
from config import Pattern

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
        pos(`str`): limitation on the result. Can be set to a(形容词)/v（动词）/n（名词）/r（副词）.
        使用单词原型,否则babelnet无法识别
        TODO 需要性能优化
    '''
    def __synonyms(self, lemma:str, word_pos:str=None):
        candidates = set([lemma, ''])
        word_pos = tools.ltp_to_babelnet_pos(word_pos)
        # word_pos = None
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for synonyms in synonyms_list:
                candidates.update(synonyms.zh_synonyms)
        candidate_list = list(candidates)
        tools.show_log(f'BabelNetBuilder ｜ candidate_list of {lemma}-{word_pos} = {candidate_list}')      
        return candidate_list
    