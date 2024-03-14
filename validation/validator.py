import numpy as np
from common import tools, AdvText, TokenStyle, SubstituteState, HuggingFaceWrapper
from .similarity_measure import SimMeasurer
from typing import List, Tuple

class Validator:

    def __init__(self, victim_model: HuggingFaceWrapper) -> None:
        self.__victim_model = victim_model
        self.__sim_measurer = SimMeasurer()


    '''
        计算两个句子的cosin的语义相似值
    '''
    def cosine_similarity(self, origin_text:str, adversary_candidate_text:str):
        sim_score = self.__sim_measurer.compute_cos_similarity(origin_text, adversary_candidate_text)
        return sim_score

    def model_output(self, candidate_text:str) -> Tuple[List[float], int]:
        probs = self.__victim_model.output_probs(candidate_text)
        prob_label = np.argmax(probs)
        return probs, prob_label

    # 数据检查通过后，再生成AdvText实例
    def generate_example_wrapper(self, label:int, text:str) -> AdvText:
        probs = self.__victim_model.output_probs(text)
        prob_label = np.argmax(probs)
        if label != prob_label: 
            tools.show_log(f'********************** skip example of {label}:{text}')
            return None
        return AdvText(label, text, probs)


    '''
        DS策略，计算分数
    '''
    def compute_delete_score(self, adv_text: AdvText) -> float:
        origin_label, origin_probs = adv_text.origin_label, adv_text.origin_probs
        updated_text = tools.generate_latest_text(adv_text)
        probs = self.__victim_model.output_probs(updated_text)
        probs_difference = origin_probs[origin_label] - probs[origin_label]
        # tools.show_log(f'{probs_difference} | {origin_label} -- origin_probs = {origin_probs}, probs = {probs}')
        return probs_difference

    