import numpy as np
from typing import List, Tuple
from config import Pattern, AlgoType, ArgFragileMethod

from common.model import HuggingFaceWrapper
from common.entity import SememicUnit, SememicState, TokenStyle, AdvText, DecisionInfo
from common.utils import tools

from .similarity_measure import SimMeasurer
from .fragile_measure import FragileMeasurer

class Validator:

    def __init__(self, victim_model: HuggingFaceWrapper) -> None:
        self.__victim_model = victim_model
        self.__fragile_measurer = FragileMeasurer(victim_model)
        self.__sim_measurer = SimMeasurer()

    # 数据检查通过后，生成AdvText实例列表
    def generate_adv_texts(self, origin_examples, args_style) -> List[AdvText]:
        tools.show_log(f'Now, Its generating plenty of adv_text objects...')
        result_list = []
        for index, example in enumerate(origin_examples):
            origin_label, text = tools.format_example(example, args_style)
            if Pattern.IsTargetAttack:
                if Pattern.Target_Label == origin_label:
                    continue
            probs = self.__victim_model.output_probs(text)
            probs_label = int(np.argmax(probs))

            if probs_label == origin_label:
                result_list.append(AdvText(origin_label, text, probs))
            else:
                tools.show_log(f'第{index}个数据样本无效｜probs_label{probs_label}!={origin_label}origin_label')    
        return result_list

    def model_output(self, candidate_text:str) -> Tuple[List[float], int]:
        probs = self.__victim_model.output_probs(candidate_text)
        prob_label = np.argmax(probs)
        return probs, prob_label

    '''
        计算两个句子的cosin的语义相似值
    '''
    def cosine_similarity(self, origin_text:str, adversary_candidate_text:str) -> float:
        sim_score = self.__sim_measurer.compute_cos_similarity(origin_text, adversary_candidate_text)
        return sim_score

    '''
        按不同的策略
    '''
    def operate_fragile(self, substitute: SememicUnit, adv_text: AdvText):
        if Pattern.Fragile_Type:
            if Pattern.Fragile_Type == ArgFragileMethod.DS:
                tools.show_log(f'Now its computing via {Pattern.Fragile_Type}')
                self.__fragile_measurer.operate_ds_fragile(substitute, adv_text)
            elif Pattern.Fragile_Type == ArgFragileMethod.ADS:
                tools.show_log(f'Now its computing via {Pattern.Fragile_Type}')
                self.__fragile_measurer.operate_ads_fragile(substitute, adv_text)
            elif Pattern.Fragile_Type == ArgFragileMethod.ADAS:
                tools.show_log(f'Now its computing via {Pattern.Fragile_Type}')
                self.__fragile_measurer.operate_adas_fragile(substitute, adv_text)
            return

        if Pattern.Algorithm == AlgoType.CWordAttacker:
            self.__fragile_measurer.operate_ds_fragile(substitute, adv_text)
        elif Pattern.Algorithm == AlgoType.SWordFooler:                
            self.__fragile_measurer.operate_ads_fragile(substitute, adv_text)
            tools.show_log(f'compute ADS fragile, fragile_score = {substitute.fragile_score}')
        else:
            self.__fragile_measurer.operate_adas_fragile(substitute, adv_text)
            tools.show_log(f'compute ADAS fragile, fragile_score = {substitute.fragile_score}')


    # 当搜索结束时（对抗攻击可能成功，可能失败），收集评价指标信息
    def collect_adversary_info(self, adv_text: AdvText):
        # 1 收集替换词数量，perturbed_number
        adversary_info = adv_text.adversary_info
        adversary_info.perturbated_token_count = len(list(filter(lambda token_unit: 
                token_unit.style == TokenStyle.WORD_SUBSTITUTE and token_unit.substitute_unit.state == SememicState.WORD_REPLACED
                        ,adv_text.token_units)))
        
        # 2 收集替换词的总数
        adversary_info.text_token_count = adv_text.token_count

        # 3 收集对抗样本和原始文本的相似度
        adversary_info.similarity = self.cosine_similarity(adversary_info.origin_text, adversary_info.adversary_text)

        # 3 收集查询次数
        adversary_info.query_times = self.__victim_model.get_query_times()
        self.__victim_model.initial_query_time()

    # 为MaskedBeamFooler算法收集算法指标信息
    def collect_MBF_common_adversary(self, decision_info: DecisionInfo, adv_text: AdvText):
        adversary_info = adv_text.adversary_info
        adversary_info.adversary_accurary = decision_info.prob
        adversary_info.adversary_text = decision_info.candidate_sample
        adversary_info.adversary_label = decision_info.prob_label

    def collect_MBF_adversary_when_ending(self,adv_text: AdvText):
        adversary_info = adv_text.adversary_info
        adversary_info.similarity = self.cosine_similarity(adversary_info.origin_text, adversary_info.adversary_text)
        adversary_info.text_token_count = adv_text.token_count
        adversary_info.query_times = self.__victim_model.get_query_times()
        self.__victim_model.initial_query_time()
        adversary_info.perturbated_token_count = len(list(filter(lambda token_unit: 
                token_unit.style == TokenStyle.WORD_SUBSTITUTE and token_unit.substitute_unit.state == SememicState.WORD_REPLACED
                        ,adv_text.token_units)))


    def generate_incomplete_initial_probs(self, adv_text: AdvText) -> List[float]:
        incomplete_initial_text = tools.generate_incomplete_text(adv_text)
        probs = self.__victim_model.output_probs(incomplete_initial_text)
        return probs