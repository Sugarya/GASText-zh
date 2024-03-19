from typing import List
from enum import Enum
from .hownet import BabelNetBuilder, SememeBuilder
from .masked_fill import MaskedCandidateBuilder
from .transformer import CWordAttackerTransformer
from common import tools, SubstituteUnit, AdvText, BertMaskedModelWrapper, SubstituteState
from config import AlgoType


'''
    使用不同的方式生成替代词，如同义词，语言淹码模型，拼音，繁体字等
'''
class Substituter:

    def __init__(self, type:AlgoType):
        self.__type = type
        if self.__type == AlgoType.SWordFooler:
            self.__babelnet_builder = BabelNetBuilder()
            # self.__sememe_builder = SememeBuilder()
        elif type == AlgoType.CWordAttacker:
            self.__transformer = CWordAttackerTransformer()
        elif type == AlgoType.SWordMasked:
            self.__masked_builder = MaskedCandidateBuilder()


    def generate(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        result = []
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        tools.show_log(f'Substituter origin word = {origin_word}, pos = {origin_pos}')
        if self.__type == AlgoType.CWordAttacker:
            result = self.generate_cwordattacker_candidate(origin_word)
        elif self.__type == AlgoType.SWordFooler:
            result = self.generate_synonyms(origin_word, origin_pos)
        elif self.__type == AlgoType.SWordMasked:
            result = self.generate_masked_candidates(substitute_unit, adv_text)
        return result

    
    
    def generate_cwordattacker_candidate(self, word:str) -> List[str]:
        candidate = self.__transformer.candidate(word)
        return [candidate]

    def generate_synonyms(self, word:str, pos:str) -> List[str]:
        return self.__babelnet_builder.synonyms(word, pos)
        
    def _generate_sememes(self, word:str) -> List[str]:
        return self.__sememe_builder.sememes(word) 

    def generate_masked_candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        candidate_list = self.__masked_builder.candidates(substitute_unit, adv_text)
        return candidate_list

        
