import numpy as np
from common.entity import AdvText, SubstituteUnit, SubstituteState
from common.model import HuggingFaceWrapper
from common.utils import tools
from typing import List, Tuple
from config import Pattern, AlgoType


class FragileMeasurer:

    def __init__(self, victim_model: HuggingFaceWrapper) -> None:
        self.__victim_model = victim_model

          
    # DS策略
    def operate_ds_fragile(self, substitute:SubstituteUnit, adv_text: AdvText) -> float:
        substitute.state = SubstituteState.WORD_REPLACING
        substitute.exchange_word = ''
        substitute.fragile_score = self.__compute_ds_score(adv_text)
        substitute.exchange_word = substitute.origin_word
        substitute.state = SubstituteState.WORD_INITIAL

    def __compute_ds_score(self, adv_text: AdvText) -> float:
        updated_text = tools.generate_latest_text(adv_text)
        probs = self.__victim_model.output_probs(updated_text)
        result_score = 0

        origin_probs = adv_text.origin_probs
        if Pattern.IsTargetAttack:
            target_label = Pattern.Target_Label
            result_score = probs[target_label] - origin_probs[target_label]
        else:
            origin_label = adv_text.origin_label
            result_score = origin_probs[origin_label] - probs[origin_label]
        return result_score
    
    # ADS策略: amplitude delete score
    def operate_ads_fragile(self, substitute:SubstituteUnit, adv_text: AdvText):
        substitute.state = SubstituteState.WORD_REPLACING
        substitute.exchange_word = ''
        substitute.fragile_score = self.__compute_ads_score(adv_text)
        substitute.exchange_word = substitute.origin_word
        substitute.state = SubstituteState.WORD_INITIAL

    # 脆弱性代表偏离原位置的幅度，所以只关注幅度，不关注方向
    def __compute_ads_score(self, adv_text: AdvText) -> float:
        result_score = 0
        updated_text = tools.generate_latest_text(adv_text)
        probs = self.__victim_model.output_probs(updated_text)
        origin_probs = adv_text.origin_probs
        if Pattern.IsTargetAttack:
            target_label = Pattern.Target_Label
            result_score = abs(probs[target_label] - origin_probs[target_label]) + abs(probs[target_label] - origin_probs[target_label])
        else:
            result_score = np.sum(np.abs(probs - origin_probs))
        return result_score
    

    # TODO ADAS策略: amplitude delete and addtion score
    def operate_fragile(self, substitute:SubstituteUnit, adv_text: AdvText):
        
        pass