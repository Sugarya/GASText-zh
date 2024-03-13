from typing import List
from .hownet import BabelNetBuilder, SememeBuilder
from .masked_fill import MaskedCandidateBuilder
from .transformer import CWordAttackerTransformer
from common import tools, SubstituteUnit, AdvText, BertMaskedModelWrapper, SubstituteState
from enum import Enum

class SubstituteType(Enum):

    SYNONYM = 1
    SEMEME = 2
    CWORDATTACKER = 3
    MASKED = 4

'''
    使用不同的方式生成替代词，如同义词，语言淹码模型，拼音，繁体字等
'''
class Substituter:

    def __init__(self, type:SubstituteType):
        self.__type = type
        if type == SubstituteType.SYNONYM:
            self.__babelnet_builder = BabelNetBuilder()
        elif type == SubstituteType.SEMEME:
            self.__sememe_builder = SememeBuilder()
        elif type == SubstituteType.CWORDATTACKER:
            self.__transformer = CWordAttackerTransformer()
        elif type == SubstituteType.MASKED:
            self.__masked_builder = MaskedCandidateBuilder()


    def generate(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        result = []
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        tools.show_log(f'Substituter origin word,pos =  {origin_word} {origin_pos}')
        if self.__type == SubstituteType.SYNONYM:
            result = self._generate_synonyms(origin_word, origin_pos)
        elif self.__type == SubstituteType.SEMEME:
            result = self._generate_sememes(origin_word)
        elif self.__type == SubstituteType.CWORDATTACKER:
            result = self._generate_cwordattacker_candidate(origin_word)
        elif self.__type == SubstituteType.MASKED:
            result = self._generate_masked_candidates(substitute_unit, adv_text)
        return result
    


    def _generate_synonyms(self, word:str, pos:str) -> List[str]:
        return self.__babelnet_builder.synonyms(word, pos)
        
    def _generate_sememes(self, word:str) -> List[str]:
        return self.__sememe_builder.sememes(word)    

    def _generate_cwordattacker_candidate(self, word:str) -> List[str]:
        candidate = self.__transformer.candidate(word)
        return [candidate]
    
    def _generate_masked_candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        candidate_list = self.__masked_builder.candidates(substitute_unit, adv_text)
        return candidate_list

        
