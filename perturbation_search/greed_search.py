from typing import List
from common import SubstituteUnit, AdvText, tools, SubstituteState, AdversaryInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, AlgoType

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
    
    '''
        扰动搜索
        @return：True表示找到对抗样本，False表示没有找到
    '''
    def search(self, substitute_units: List[SubstituteUnit], adv_text: AdvText):
        # 环节1）计算脆弱值，并按脆弱值从大到小排序
        travel_substitutes: List[SubstituteUnit] = self.__sort_by_fragile_score(substitute_units, adv_text)
        
        # 环节2）遍历语义单元序列，生成替代词--》替换--》检验
        for index, substitute_unit in enumerate(travel_substitutes):
            tools.show_log(f'*****substitute- {index} -Round')
            # origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
            # tools.show_log(f'{substitue_unit.fragile_score} | replace {substitue_unit.origin_word} in {substitue_unit.pos_in_text}')
            
            # 2.1）以某种方式生成替代词
            substitute_unit.candicates = self.__substituter.generate(substitute_unit, adv_text)
            # substitue_unit.candicates = self.__substituter.generate_masked_candidates(substitue_unit, adv_text)
            # 没有同义词集
            if not substitute_unit.candicates:
                tools.show_log(f'*****{substitute_unit.origin_word} 没有hownet同义词')
                continue
            
            # 2.2）遍历语义单元的候选词集，逐一替换和检验
            tools.show_log(f'*****substitute- {index} -Round, greedy_score = {adv_text.greedy_score}')
            attack_succees = self.operate_substitute(substitute_unit, adv_text)
            if attack_succees:
                self.__validator.collect_adversary_info(adv_text)
                return True
        
        self.__validator.collect_adversary_info(adv_text)
        return False

    '''
        处理单个语义单元，共有3个环节：初始化，逐一替换和检验，产生有效替代
        return: 当前substitute内，是否能找到对抗样本
    '''
    def operate_substitute(self, substitute: SubstituteUnit, adv_text:AdvText) -> bool:
        # 环节1) SubstituteUnit初始化
        substitute.initial_greedy_score = adv_text.greedy_score
        substitute.exchange_max_greedy_score = adv_text.greedy_score
        substitute.exchange_max_greedy_word = substitute.origin_word

        # 环节2）遍历候选词集，逐一操作
        for index, candidate in enumerate(substitute.candicates):
            
            # 2.1 替换动作
            substitute.exchange_word = candidate
            substitute.state = SubstituteState.WORD_REPLACING

            tools.show_log(f'************** {index} -round, candidate = {candidate}, substitute.state = {substitute.state}')
            
            # 2.2 生成替换后的候选文本
            latest_candidate_text = tools.generate_latest_text(adv_text)

            # 2.3 检验，输入到攻击模型；计算贪心分数
            candidate_probs, prob_label = self.__validator.model_output(latest_candidate_text)
            cur_greedy_score = self.__greedy_selection_score(adv_text.origin_probs, candidate_probs, adv_text.origin_label)
            tools.show_log(f'**************candidate={candidate}, label(origin->prob): {adv_text.origin_label}->{prob_label}, cur_greedy_score = {cur_greedy_score}')
            
            # 2.4 判断当前候选词有效性,如果不是对抗样本
            adversary_success = (prob_label != adv_text.origin_label)
            if not adversary_success and cur_greedy_score <= substitute.initial_greedy_score:
                tools.show_log(f'************** continue --> cur_greedy_score{cur_greedy_score} <= {substitute.initial_greedy_score}initial_greedy_score')
                continue
            if not adversary_success and cur_greedy_score <= substitute.exchange_max_greedy_score:
                tools.show_log(f'************** continue --> cur_greedy_score{cur_greedy_score} <= {substitute.exchange_max_greedy_score}exchange_max_greedy_score')
                continue

            # 2.5 更新substitute unit
            substitute.exchange_max_greedy_score = cur_greedy_score
            substitute.exchange_max_greedy_word = candidate
            substitute.exchange_max_greedy_text = latest_candidate_text
            tools.show_log(f'**************exchange_max_greedy_word = {substitute.exchange_max_greedy_word}, exchange_max_greedy_score = {substitute.exchange_max_greedy_score}')
            tools.show_log(f'**************exchange_max_greedy_text = {substitute.exchange_max_greedy_text}')
            
            # 2.6 收集评价指标信息
            adv_text.adversary_info.adversary_accurary = candidate_probs[adv_text.origin_label]
            adv_text.adversary_info.adversary_text = latest_candidate_text
            adv_text.adversary_info.adversary_label = prob_label
            
            # 2.7 如果对抗样本成功
            if adversary_success:
                substitute.state = SubstituteState.WORD_REPLACED
                # 更新全局信息
                adv_text.greedy_score = cur_greedy_score
                adv_text.adversary_info.attack_success = True
                tools.show_log(f'**************ATTACK SUCCESS**************')
                return True 

        # 环节3）判断候选词是否有效，检验约束条件，更新状态
        # 3.1 是否有出现了有效候词替代原始文本
        if substitute.exchange_max_greedy_score <= substitute.initial_greedy_score:
            substitute.state = SubstituteState.WORD_INITIAL
            tools.show_log(f'**************return substitute.state = {substitute.state}, exchange_max_greedy_score{substitute.exchange_max_greedy_score} <= {substitute.initial_greedy_score}initial_greedy_score')
            return False
        
        # 3.2 Optional 检验约束条件
        if Pattern.Algorithm == AlgoType.SWordMasked:
            sim_score = self.__validator.cosine_similarity(adv_text.origin_text, substitute.exchange_max_greedy_text) 
            tools.show_log(f'**************sim_score = {sim_score}')
            if sim_score < Pattern.SENTENCE_SIMILARITY_THRESHOLD:
                substitute.state = SubstituteState.WORD_INITIAL
                tools.show_log(f'**************return substitute.state = {substitute.state} --> sim_score < 0.8')
                return False

        # 3.3 本轮产生了有效替代，更新全局greedy_score和substitute state
        adv_text.greedy_score = substitute.exchange_max_greedy_score
        substitute.state = SubstituteState.WORD_REPLACED
        tools.show_log(f'**************return substitute.state = {substitute.state} | exchange_max_greedy_word = {substitute.exchange_max_greedy_word}, exchange_max_greedy_score = {substitute.exchange_max_greedy_score}')

        return False
    

    '''
        贪心选择的分数值
    '''
    def __greedy_selection_score(self, origin_probs: List[float], candidate_probs:List[float], label:int) -> float:
        return origin_probs[label] - candidate_probs[label]
