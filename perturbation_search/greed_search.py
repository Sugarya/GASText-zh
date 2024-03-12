from typing import List
from common import SubstituteUnit, AdvText, tools, SubstituteState
from validation import Validator
from substitution import Substituter

'''
    贪心搜索
'''
class Greedy:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        self.__validator = validator
        self.__substituter = substituter
        


    def __sort_by_fragile_score(self, substitute_units: List[SubstituteUnit], adv_text: AdvText) -> List[SubstituteUnit]:
        # 1. 计算
        # 2.sort排序
        # //TODO 验证：是否要取前 Top k个，是否要过滤掉负值
        for index, substitute in enumerate(substitute_units):
            substitute.state = SubstituteState.WORD_REPLACING
            substitute.exchange_word = ''
            substitute.fragile_score = self.__validator.compute_delete_score(adv_text)
            substitute.exchange_word = substitute.origin_word
            substitute.state = SubstituteState.WORD_INITIAL
            
        substitute_units = list(filter(lambda t : t.fragile_score > 0, sorted(substitute_units, key = lambda t : t.fragile_score, reverse = True)))
        return substitute_units
    
    def search(self, substitute_units: List[SubstituteUnit], adv_text: AdvText):
        travel_substitutes: List[SubstituteUnit] = self.__sort_by_fragile_score(substitute_units, adv_text)
        for substitue_unit in travel_substitutes:
            tools.show_log(f'{substitue_unit.fragile_score} | replace {substitue_unit.origin_word} in {substitue_unit.pos_in_text}')

        
        
        pass