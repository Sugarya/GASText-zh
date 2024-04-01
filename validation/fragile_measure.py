import numpy as np
from common.entity import AdvText, SememicUnit, SememicState
from common.model import HuggingFaceWrapper
from common.utils import tools
from typing import List, Tuple
from config import Pattern, AlgoType


class FragileMeasurer:

    def __init__(self, victim_model: HuggingFaceWrapper) -> None:
        self.__victim_model = victim_model


    # DS策略
    def operate_ds_fragile(self, substitute:SememicUnit, adv_text: AdvText) -> float:
        substitute.state = SememicState.WORD_REPLACING
        substitute.exchange_word = ''
        updated_text = tools.generate_latest_text(adv_text)
        substitute.exchange_word = substitute.origin_word
        substitute.state = SememicState.WORD_INITIAL
        
        probs = self.__victim_model.output_probs(updated_text)
        substitute.fragile_score = self.__compute_ds_score(adv_text, probs)


    def __compute_ds_score(self, adv_text:AdvText, probs: List[float]) -> float:
        origin_probs = adv_text.origin_probs
        result_score = 0
        if Pattern.IsTargetAttack:
            target_label = Pattern.Target_Label
            result_score = probs[target_label] - origin_probs[target_label]
        else:
            origin_label = adv_text.origin_label
            result_score = origin_probs[origin_label] - probs[origin_label]
        return result_score
    
    # ADS策略: amplitude delete score
    def operate_ads_fragile(self, substitute:SememicUnit, adv_text: AdvText):
        substitute.state = SememicState.WORD_REPLACING
        substitute.exchange_word = ''
        updated_text = tools.generate_latest_text(adv_text)
        substitute.exchange_word = substitute.origin_word
        substitute.state = SememicState.WORD_INITIAL

        probs = self.__victim_model.output_probs(updated_text)
        substitute.fragile_score = self.__compute_ads_score(adv_text.origin_probs, probs)
        

    # 脆弱性代表偏离原位置的幅度，所以只关注幅度，不关注方向
    def __compute_ads_score(self, origin_probs: List[float], probs: List[float]) -> float:
        result_score = 0
        if Pattern.IsTargetAttack:
            target_label = Pattern.Target_Label
            result_score = abs(probs[target_label] - origin_probs[target_label]) + abs(probs[target_label] - origin_probs[target_label])
        else:
            result_score = np.sum(np.abs(probs - origin_probs))
        return result_score
    

    # ADAS策略: amplitude delete and addtion score
    def operate_adas_fragile(self, substitute:SememicUnit, adv_text: AdvText):
        self.operate_ads_fragile(substitute, adv_text)

        substitute.state = SememicState.WORD_REPLACING
        incomplete_text = tools.generate_incomplete_text(adv_text)
        substitute.state = SememicState.WORD_INITIAL
        probs = self.__victim_model.output_probs(incomplete_text)
        ads_score = self.__compute_ads_score(adv_text.incomplete_initial_probs, probs)
        tools.show_log(f'adas part1 score = {substitute.fragile_score}, part2 score = {ads_score}')
    
        C2 = 1 / adv_text.substitute_count
        C1 = 1 - C2
        substitute.fragile_score = C1*substitute.fragile_score + C2*ads_score
