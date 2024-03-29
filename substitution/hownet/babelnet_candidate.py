from typing import List
from OpenHowNet import HowNetDict

from common import tools
from config import Pattern, ArgAblation


class LANGUAGE:
    ZH = 'zh'
    EN = 'en'

'''
    BabelNet同义词集
'''
class BabelNetBuilder:

    def __init__(self, hownet_dict_advanced:HowNetDict) -> None:
        self.__hownet_dict_advanced = hownet_dict_advanced


    def synonyms(self, word:str, pos:str):
        synonym_list = self.__synonyms(word, pos)
        return synonym_list

    
    '''
        pos(`str`): limitation on the result. Can be set to a(形容词)/v（动词）/n（名词）/r（副词）.
        使用单词原型,否则babelnet无法识别
        TODO 需要性能优化
    '''
    def __synonyms(self, lemma:str, word_pos:str=None):
        candidates = None
        if Pattern.Ablation_Type == ArgAblation.Deletion:
            candidates = set()
        else:
            candidates = set([''])
        tools.show_log(f'Pattern.Ablation_Type = {Pattern.Ablation_Type}')
        
        word_pos = tools.ltp_to_babelnet_pos(word_pos)
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for index, synonyms in enumerate(synonyms_list):
                tools.show_log(f'--{index}--, synonyms.zh_synonyms = {synonyms.zh_synonyms}')
                candidates.update(synonyms.zh_synonyms) 
        candidate_list = list(candidates)
        
        if Pattern.Substitute_Size and len(candidate_list) > Pattern.Substitute_Size:
            candidate_list = candidate_list[:Pattern.Substitute_Size]
        
        tools.show_log(f'Substitute_Size = {Pattern.Substitute_Size} ｜ candidate_list of {lemma}-{word_pos} = {candidate_list}')
        return candidate_list
    
    def synonyms_by_similarity_score(self, lemma:str, word_pos:str=None):
        syn_set = set()
        word_pos = tools.ltp_to_babelnet_pos(word_pos)
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for index, synonyms in enumerate(synonyms_list):
                syn_set.update(synonyms.zh_synonyms)
        tools.show_log(f'all zh_synonyms = {syn_set}')

        syn_tuple_set = map(lambda t:(self.__word_similarity(lemma, t), t), syn_set)
        candidate_tuple_set = filter(lambda t:t[0]>Pattern.Word_Similarity_Threshold, syn_tuple_set)
        candidate_tuple_list = list(sorted(candidate_tuple_set, key=lambda t:t[0], reverse=True))
        if Pattern.Ablation_Type != ArgAblation.Deletion:
            candidate_tuple_list.insert(0, (1, ''))

        if Pattern.Substitute_Size and len(candidate_tuple_list) > Pattern.Substitute_Size:
            candidate_tuple_list = candidate_tuple_list[:Pattern.Substitute_Size]
        tools.show_log(f'candidate_tuple_list of {lemma}-{word_pos} = {candidate_tuple_list}')
        
        candidate_list = list(map(lambda t:t[1], candidate_tuple_list))
        tools.show_log(f'Substitute_Size = {Pattern.Substitute_Size}｜candidate_list of {lemma}-{word_pos} = {candidate_list}')
        return candidate_list
    
    def __word_similarity(self, word:str, word2:str):
        word_sim = self.__hownet_dict_advanced.calculate_word_similarity(word, word2)
        return word_sim
    