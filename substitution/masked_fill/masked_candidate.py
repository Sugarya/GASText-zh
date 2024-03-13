
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from config import *
from common import tools, SubstituteUnit, AdvText, BertMaskedModelWrapper, SubstituteState
from typing import List

class MaskedCandidateBuilder:

    def __init__(self) -> None:
        self.__bert_masked_moder = BertMaskedModelWrapper()
        

    def candidates(self, substitute_unit: SubstituteUnit, adv_text: AdvText) -> List[str]:
        substitute_unit.exchange_word = BertMaskedModelWrapper.MASK_TOKEN
        substitute_unit.state = SubstituteState.WORD_REPLACING
        masked_text = tools.generate_text(adv_text)
        substitute_unit.exchange_word = substitute_unit.origin_word
        substitute_unit.state = SubstituteState.WORD_INITIAL
        
        tools.show_log(f'masked_text = {masked_text}')
        candidate_list = self.__bert_masked_moder.output(masked_text)
        tools.show_log(f"masked word: {substitute_unit.origin_word}, its output : {candidate_list}")
        return candidate_list





            
