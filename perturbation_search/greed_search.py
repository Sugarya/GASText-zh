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
        # 1）按脆弱值排序
        origin_text = adv_text.origin_text
        travel_substitutes: List[SubstituteUnit] = self.__sort_by_fragile_score(substitute_units, adv_text)

        for index in range(len(travel_substitutes)):
            if index >= 2: break
            
            substitute_unit = travel_substitutes[index]
            origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
            # tools.show_log(f'{substitue_unit.fragile_score} | replace {substitue_unit.origin_word} in {substitue_unit.pos_in_text}')
            
            # 2）TODO 确定一种替代方式，如使用CWorkAttacker生成替代词
            substitute_unit.candicates = self.__substituter.generate(substitute_unit, adv_text)
            # 
            # substitue_unit.candicates = self.__substituter.generate_masked_candidates(substitue_unit, adv_text)
            if not substitute_unit.candicates:
                # 没有同义词集，从列表中删去
                tools.show_log(f'****{substitute_unit.origin_word} 没有hownet同义词')
                travel_substitutes.remove(substitute_unit)
                continue
            
            # 3）替换--遍历同义词集，把让模型概率差值最大的词去替代原始文本相同位置的词


        pass