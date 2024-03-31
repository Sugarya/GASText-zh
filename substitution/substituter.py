from typing import List
import OpenHowNet
from .hownet import BabelNetBuilder
from .masked_fill import MaskedCandidateBuilder
from .transformer import CWordAttackerTransformer
from common import tools, SubstituteUnit, AdvText
from config import AlgoType, Pattern

'''
    使用不同的方式生成替换词集
'''
class Substituter:


    def __init__(self, type:AlgoType):
        self.__type = type
        if type == AlgoType.CWordAttacker:
            self.__transformer = CWordAttackerTransformer()
        elif self.__type == AlgoType.SWordFooler:
            self.__babelnet_builder = BabelNetBuilder(OpenHowNet.HowNetDict(True, True))
            self.__transformer = CWordAttackerTransformer()
        else:
            hownet_dict_advanced =  OpenHowNet.HowNetDict(True, True)
            self.__babelnet_builder = BabelNetBuilder(hownet_dict_advanced)
            self.__masked_builder = MaskedCandidateBuilder(hownet_dict_advanced)

    def __generate(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        result = []
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        tools.show_log(f'Substituter origin word = {origin_word}, pos = {origin_pos}')
        if self.__type == AlgoType.CWordAttacker:
            result = self.generate_cwordattacker_candidate(origin_word)
        elif self.__type == AlgoType.SWordFooler:
            result = self.generate_hownet_synonyms(origin_word, origin_pos)
        elif self.__type == AlgoType.MaskedBeamFooler:
            result = self.generate_hybrid_candidates(substitute_unit, adv_text)
        return result
    
    
    def generate_cwordattacker_candidate(self, word:str) -> List[str]:
        candidate_word = self.__transformer.candidate(word)
        return [candidate_word]

    def generate_hownet_synonyms(self, word:str, pos:str) -> List[str]:
        return self.__babelnet_builder.synonyms(word, pos)

    def generate_masked_candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        candidate_list = self.__masked_builder.candidates(substitute_unit, adv_text)
        return candidate_list

    """
        混合hownet和masked生成的同义词集。混合规则：
        1)masked候选集最高优 2)剩余按相似分数排序 
        3）相似分数相同的，按同义词带有原始词的字且和原始词相同字数的优先 > 同义词带有原始词的字 > 和原始词相同字数
    """
    def generate_hybrid_candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        sorted_masked_candidates = self.__masked_builder.candidates_sortedby_sim_score(substitute_unit, adv_text)
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        sorted_babel_candidates = self.__babelnet_builder.synonyms_sortedby_sim_score(origin_word, origin_pos)

        for babel_candidate in sorted_babel_candidates:
            if not babel_candidate in sorted_masked_candidates:
                sorted_masked_candidates.append(babel_candidate)

        if Pattern.Substitute_Volume and len(sorted_masked_candidates) > Pattern.Substitute_Volume:
            sorted_masked_candidates = sorted_masked_candidates[:Pattern.Substitute_Volume]

        tools.show_log(f'hybrid_candidates = {sorted_masked_candidates}')
        return sorted_masked_candidates
