from typing import List
import OpenHowNet
from .hownet import BabelNetBuilder
from .masked_fill import MaskedCandidateBuilder
from .transformer import CWordAttackerTransformer
from common import tools, SememicUnit, AdvText
from config import AlgoType, Pattern, ArgSubstituteType

'''
    使用不同的方式生成替换词集
'''
class Substituter:


    def __init__(self):
        if Pattern.Algorithm == AlgoType.CWordAttacker:
            self.__attacker_transformer = CWordAttackerTransformer()
        elif Pattern.Algorithm == AlgoType.SWordFooler:
            self.__babelnet_builder = BabelNetBuilder(OpenHowNet.HowNetDict(True, True))
            self.__attacker_transformer = CWordAttackerTransformer()
        else:
            hownet_dict_advanced =  OpenHowNet.HowNetDict(True, True)
            self.__babelnet_builder = BabelNetBuilder(hownet_dict_advanced)
            self.__masked_builder = MaskedCandidateBuilder(hownet_dict_advanced)

    def generate(self, substitute_unit: SememicUnit, adv_text: AdvText) -> List[str]:
        result = []
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        tools.show_log(f'Substituter origin word = {origin_word}, pos = {origin_pos}')

        if Pattern.Substitute_Type:
            if Pattern.Substitute_Type == ArgSubstituteType.HowNet:
                tools.show_log(f'Now, its runing via {Pattern.Substitute_Type}')
                result = self.generate_hownet_synonyms(origin_word, origin_pos)
            elif Pattern.Substitute_Type == ArgSubstituteType.MLM:
                tools.show_log(f'Now, its runing via {Pattern.Substitute_Type}')
                result = self.generate_masked_candidates(substitute_unit, adv_text)
            elif Pattern.Substitute_Type == ArgSubstituteType.Hybrid:
                tools.show_log(f'Now, its runing via {Pattern.Substitute_Type}')
                result = self.generate_hybrid_candidates(substitute_unit, adv_text)
            return result

        if Pattern.Algorithm == AlgoType.CWordAttacker:
            result = self.generate_cwordattacker_candidate(origin_word)
        elif Pattern.Algorithm == AlgoType.SWordFooler:
            result = self.generate_hownet_synonyms(origin_word, origin_pos)
        elif Pattern.Algorithm == AlgoType.MaskedAreaFooler:
            result = self.generate_hybrid_candidates(substitute_unit, adv_text)
        return result
    
    
    def generate_cwordattacker_candidate(self, word:str) -> List[str]:
        candidate_word = self.__attacker_transformer.candidate(word)
        return [candidate_word]

    def generate_hownet_synonyms(self, word:str, pos:str) -> List[str]:
        return self.__babelnet_builder.synonyms(word, pos)

    def generate_masked_candidates(self, substitute_unit: SememicUnit, adv_text: AdvText) -> List[str]:
        candidate_list = self.__masked_builder.candidates(substitute_unit, adv_text)
        return candidate_list

    """
        混合hownet和masked生成的同义词集。混合规则：
        1)masked候选集最高优 2)剩余按相似分数排序 
        3）相似分数相同的，按同义词带有原始词的字且和原始词相同字数的优先 > 同义词带有原始词的字 > 和原始词相同字数
    """
    def generate_hybrid_candidates(self, substitute_unit: SememicUnit, adv_text: AdvText) -> List[str]:
        sorted_masked_candidates = self.__masked_builder.candidates_sortedby_sim_score(substitute_unit, adv_text)
        
        origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
        sorted_babel_candidates = self.__babelnet_builder.synonyms_sortedby_sim_score(origin_word, origin_pos)

        for masked_candidate in sorted_masked_candidates:
            if not masked_candidate in sorted_babel_candidates:
                sorted_babel_candidates.append(masked_candidate)

        if Pattern.Substitute_Volume and len(sorted_babel_candidates) > Pattern.Substitute_Volume:
            sorted_babel_candidates = sorted_babel_candidates[:Pattern.Substitute_Volume]

        tools.show_log(f'hybrid_candidates = {sorted_babel_candidates}')
        return sorted_babel_candidates
