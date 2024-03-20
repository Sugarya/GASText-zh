from typing import List
import OpenHowNet
from common import tools

class LANGUAGE:
    ZH = 'zh'
    EN = 'en'

class SememeBuilder:

    Nearest_Word_Count = 6

    def __init__(self):
        self.__hownet_dict_advanced = OpenHowNet.HowNetDict(init_sim=True)

    def sememes(self, word:str) -> List[str]:
        sememe_list = self.__sememes(word)
        return sememe_list

    def __sememes(self, lemma:str) -> List[str]:
        sememe_candidates = [lemma, '']
        tools.show_log(f'***** SememeBuilder __sememes() lemma = {lemma}')
        nearest_words = self.__hownet_dict_advanced.get_nearest_words(lemma, 
                                                      merge=True, 
                                                      K=self.Nearest_Word_Count, 
                                                      language = LANGUAGE.ZH, 
                                                      strict=False)
        sememe_candidates.extend(nearest_words)
        tools.show_log(f'sememe_candidates = {sememe_candidates}')
        return sememe_candidates