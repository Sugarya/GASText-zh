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
        candidate_list = self.__synonyms(word, pos)
        if Pattern.Ablation_Type != ArgAblation.Deletion:
            candidate_list.append('')

        if Pattern.Substitute_Volume and len(candidate_list) > Pattern.Substitute_Volume:
            candidate_list = candidate_list[:Pattern.Substitute_Volume]

        tools.show_log(f'Pattern.Ablation_Type = {Pattern.Ablation_Type}, Substitute_Size = {Pattern.Substitute_Volume} ｜ candidate_list of {word}-{pos} = {candidate_list}')    
        return candidate_list

    '''
        pos(`str`): limitation on the result. Can be set to a(形容词)/v（动词）/n（名词）/r（副词）.
        使用单词原型,否则babelnet无法识别
        TODO 需要性能优化
    '''
    def __synonyms(self, lemma:str, word_pos:str=None):
        candidates = set()        
        word_pos = tools.ltp_to_babelnet_pos(word_pos)
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for index, synonyms in enumerate(synonyms_list):
                tools.show_log(f'--{index}--, synonyms.zh_synonyms = {synonyms.zh_synonyms}')
                candidates.update(synonyms.zh_synonyms) 
        return list(candidates)
    



    def synonyms_sortedby_sim_score(self, lemma:str, word_pos:str=None) -> List[str]:
        # 1）从babelnet中获得同义词集
        syn_set = set()
        word_pos = tools.ltp_to_babelnet_pos(word_pos)
        if self.__hownet_dict_advanced.has(lemma, LANGUAGE.ZH):
            synonyms_list = self.__hownet_dict_advanced.get_synset(lemma, language = LANGUAGE.ZH, pos=word_pos)
            for index, synonyms in enumerate(synonyms_list):
                for zh_synonym in synonyms.zh_synonyms:
                    if '\\u' in zh_synonym:
                        continue
                    
                    if tools.is_only_alphabets(zh_synonym):
                        continue

                    if '+' in zh_synonym:
                        zh_synonym = zh_synonym.replace('+','')
                    syn_set.add(zh_synonym)

        tools.show_log(f'all zh_synonyms = {syn_set}')

        # 2）词级相似性排序 + 优先级规则排序
        syn_list_set = list(map(lambda t:[self.__word_similarity(lemma, t), t], syn_set))
        tools.show_log(f'syn_list_set = {syn_list_set}')
        candidate_lists = list(filter(lambda t:t[0]>Pattern.Word_Similarity_Threshold, syn_list_set))
        # tools.show_log(f'candidate_lists = {candidate_lists}')
        self.__plus_rule_score(candidate_lists, lemma)
        tools.show_log(f'plus_rule_score, then candidate_lists = {candidate_lists}')
        sorted_candidate_lists = list(sorted(candidate_lists, key=lambda t:t[0], reverse=True))

        # 3）截短并输出同义词集
        if Pattern.Substitute_Volume and len(sorted_candidate_lists) > Pattern.Substitute_Volume:
            sorted_candidate_lists = sorted_candidate_lists[:Pattern.Substitute_Volume]
        tools.show_log(f'sorted_candidate_lists of {lemma}-{word_pos} = {sorted_candidate_lists}')
        sorted_candidate_list = list(map(lambda t:t[1], sorted_candidate_lists))
        tools.show_log(f'Substitute_Size = {Pattern.Substitute_Volume}｜sorted candidate_list of {lemma}-{word_pos} = {sorted_candidate_list}')
        return sorted_candidate_list
    
    def __word_similarity(self, word:str, word2:str) -> float:
        word_sim = self.__hownet_dict_advanced.calculate_word_similarity(word, word2)
        if word_sim <= -1:
            word_sim = (Pattern.Word_Similarity_Threshold + 0.01)
        return word_sim
    
    # 通过添加规则分数区分相同相似性分数下的不同词
    def __plus_rule_score(self, candidate_list_set: set, lema:str):
        SUnit = 0.001
        DUnit = 0.002
        for candidate in candidate_list_set:
            sim_score, syn_word = candidate[0], candidate[1]
            s1 = set([c for c in syn_word])
            s2 = set([c for c in lema])
            # tools.show_log(f'{sim_score} | {syn_word} = {s1}, {lema} = {s2}')
            lema_size = len(s2)
            isSizeSame = (len(s1) == lema_size)
            if s1.isdisjoint(s2): # 两个词没有相同的字
                if isSizeSame:
                    candidate[0] = sim_score + SUnit
            else: # 两个词有相同的字
                intersect_len = len(s1.intersection(s2))
                if isSizeSame:
                    candidate[0] = sim_score + (intersect_len + lema_size) * DUnit
                else:
                    candidate[0] = sim_score + intersect_len * DUnit
            # tools.show_log(f'plus rule score = {candidate[0]}')