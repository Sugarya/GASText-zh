from typing import List
import OpenHowNet
from common import tools

class LANGUAGE:
    ZH = 'zh'
    EN = 'en'

class SememeBuilder:

    def __init__(self):
        self.__hownet_dict_advanced = OpenHowNet.HowNetDict()
        self.__hownet_dict_advanced.initialize_similarity_calculation()


    def sememes(self, word:str):
        sememe_list = self.__sememes(word)
        return sememe_list

    
    '''
        pos: Can be set to a/v/n/r
        使用词的原型形式，且词性POS必须为Hownet的形式,否则babelnet无法识别
    '''
    def __sememes(self, lemma:str):  
        sememe_candidates = self.__hownet_dict_advanced.get_nearest_words(lemma, merge=True, K=6, language = LANGUAGE.ZH, strict=False)
        tools.show_log(f'sememe_candidates = {sememe_candidates}')
        return sememe_candidates