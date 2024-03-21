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
        # self.__hownet_dict_advanced.initialize_similarity_calculation()


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
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for index, synonyms in enumerate(synonyms_list):
                tools.show_log(f'--{index}--, synonyms.zh_synonyms = {synonyms.zh_synonyms}')
                candidates.update(synonyms.zh_synonyms)
        candidate_list = list(candidates)
        tools.show_log(f'BabelNetBuilder ｜ candidate_list of {lemma}-{word_pos} = {candidate_list}')      
        return candidate_list
    
    # def __nearest_words(self, lemma:str, word_pos:str=None):
    #     candidates = set([lemma, ''])
    #     word_pos = tools.ltp_to_babelnet_pos(word_pos)
    #     if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
    #         try:
    #             synonyms_list = self.__hownet_dict_advanced.get_nearest_words(lemma, LANGUAGE.ZH, K = 6, merge=True)
    #             if len(synonyms_list) > 0:
    #                 candidates.update(synonyms_list)
    #         except (RuntimeError, TypeError):
    #             pass
    #     result_list = list(candidates)
    #     tools.show_log(f'BabelNetBuilder ｜ sememes words of {lemma}-{word_pos} = {result_list}')      
    #     return result_list
    
    def __word_similarity(self, word:str, word2:str):
        word_sim = self.__hownet_dict_advanced.calculate_word_similarity(word, word2)
        return word_sim