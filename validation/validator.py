import numpy as np
from common import tools, AdvText, TokenStyle, SubstituteState, HuggingFaceWrapper

class Validator:

    def __init__(self, victim_model: HuggingFaceWrapper) -> None:
        self.__victim_model = victim_model

    # 当数据合理时，生成AdvText实例
    def generate_example_wrapper(self, label, text) -> AdvText:
        probability = self.__victim_model.output_probability(text)
        prob_label = np.argmax(probability)
        if label != prob_label: 
            tools.show_log(f'********************** skip example of {label}:{text}')
            return None
        return AdvText(label, text, probability)


    '''
        DS策略，计算分数
    '''
    def compute_delete_score(self, adv_text: AdvText) -> float:
        origin_label, origin_probs = adv_text.origin_label, adv_text.origin_probs
        updated_text = tools.generate_latest_text(adv_text)
        probs = self.__victim_model.output_probability(updated_text)
        probs_difference = origin_probs[origin_label] - probs[origin_label]
        # tools.show_log(f'{probs_difference} | {origin_label} -- origin_probs = {origin_probs}, probs = {probs}')
        return probs_difference

    
