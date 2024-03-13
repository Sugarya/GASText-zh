from typing import List
from .synonym import HownetBuilder
from .masked_fill import MaskedCandidateBuilder
from .transformer import CWordAttackerTransformer
from common import tools, SubstituteUnit, AdvText, BertMaskedModelWrapper, SubstituteState

'''
    使用不同的方式生成替代词，如同义词，语言淹码模型，拼音，繁体字等
'''
class Substituter:

    def __init__(self) -> None:
        # self.__hownet_builder = HownetBuilder()
        # self.__transformer = CWordAttackerTransformer()
        self.__masked_builder = MaskedCandidateBuilder()
        

    def generate_synonyms(self, word:str, pos:str) -> List[str]:
        return self.__hownet_builder.synonyms(word, pos)
        

    def generate_cwordattacker_candidate(self, word:str) -> List[str]:
        candidate = self.__transformer.candidate(word)
        return [candidate]
    
    def generate_masked_candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        candidate_list = self.__masked_builder.candidates(substitute_unit, adv_text)
        return candidate_list

        
