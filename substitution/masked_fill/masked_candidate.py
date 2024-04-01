
from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from config import Pattern
from common import tools, SememicUnit, AdvText, BertMaskedModelWrapper, SememicState
from typing import List
from OpenHowNet import HowNetDict

class MaskedCandidateBuilder:

    def __init__(self, hownet_dict_advanced:HowNetDict) -> None:
        self.__bert_masked_moder = BertMaskedModelWrapper()
        self.__hownet_dict_advanced = hownet_dict_advanced
        

    def candidates(self, substitute_unit: SememicUnit, adv_text: AdvText) -> List[str]:
        substitute_unit.exchange_word = BertMaskedModelWrapper.MASK_TOKEN
        substitute_unit.state = SememicState.WORD_REPLACING
        masked_text = tools.generate_text(adv_text)
        substitute_unit.exchange_word = substitute_unit.origin_word
        substitute_unit.state = SememicState.WORD_INITIAL
        
        candidate_list = []
        candidate_list.extend(self.__bert_masked_moder.output(masked_text))
        tools.show_log(f"masked word: {substitute_unit.origin_word}, its output : {candidate_list}")
        return candidate_list
    

    def candidates_sortedby_sim_score(self, substitute_unit: SememicUnit, adv_text: AdvText) -> List[str]:
        substitute_unit.exchange_word = BertMaskedModelWrapper.MASK_TOKEN
        substitute_unit.state = SememicState.WORD_REPLACING
        masked_text = tools.generate_text(adv_text)
        substitute_unit.exchange_word = substitute_unit.origin_word
        substitute_unit.state = SememicState.WORD_INITIAL
        masked_list = self.__bert_masked_moder.output(masked_text)
        tools.show_log(f'masked_list = {masked_list}')

        masked_tuple_list = map(lambda t:(self.__word_similarity(substitute_unit.origin_word,t), t), masked_list)
        masked_tuple_list = filter(lambda x:x[0]>Pattern.Word_Similarity_Threshold, masked_tuple_list)
        sorted_tuple_list = sorted(masked_tuple_list, key=lambda t:t[0], reverse=True)
        tools.show_log(f'sorted_tuple_list = {sorted_tuple_list}')
        
        candidate_list = list(map(lambda t:t[1], sorted_tuple_list))
        tools.show_log(f"masked word: {substitute_unit.origin_word}, its output : {candidate_list}")
        return candidate_list


    def __word_similarity(self, word:str, word2:str):
        word_sim = self.__hownet_dict_advanced.calculate_word_similarity(word, word2)
        return word_sim

            
