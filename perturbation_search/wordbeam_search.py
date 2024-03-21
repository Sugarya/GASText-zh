from typing import List
from common import SubstituteUnit, AdvText, tools, SubstituteState, AdversaryInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, AlgoType

class WordBeamSearch:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        self.__validator = validator
        self.__substituter = substituter


    def search(self, substitute_units: List[SubstituteUnit], adv_text: AdvText) -> bool:
        units_size = len(substitute_units)
        tools.show_log(f'WordMaskedGreedy search, the length of substitute_units = {units_size}')
        travel_times = units_size
        travel_substitutes = list(substitute_units)
    
        # 1）计算脆弱值
        travel_substitutes = self.__sorted_by_fragile_score(travel_substitutes, adv_text)
        # 遍历语义单元序列
        for index in range(travel_times):
            tools.show_log(f'*****substitute- {index} -Round')

            substitute_unit = travel_substitutes[index]
            # 2）生成替代词
            origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
            tools.show_log(f'***** origin_word = {origin_word} -> pos = {origin_pos}')
            substitute_unit.candicates = self.__substituter.generate_synonyms(origin_word, origin_pos)
            
            # 没有同义词集
            if len(substitute_unit.candicates) <= 2:
                tools.show_log(f'*****跳过{substitute_unit.origin_word}，其同义词为空')
                continue
            
            # 3）遍历语义单元的候选词集，逐一替换和检验
            tools.show_log(f'*****substitute- {index} -Round, greedy_score = {adv_text.decision_score}')
            attack_succees = self.__operate_substitute(substitute_unit, adv_text)

            # 4) 样本粒度约束条件检验
            # disable = self.__disable_candidate_sample(adv_text)
            # if disable:
            #     self.__validator.collect_adversary_info(adv_text)
            #     return False

            # 5) 计算实验评价数据
            if attack_succees:
                self.__validator.collect_adversary_info(adv_text)
                return True
        
        self.__validator.collect_adversary_info(adv_text)
        return False


   # TODO 提供样本粒度的条件约束
    def __disable_candidate_sample(self,adv_text: AdvText) -> bool:         
        return False


    '''
        处理单个语义单元，共有3个环节：初始化，逐一替换和检验，产生有效替代
        return: 当前substitute内，是否能找到对抗样本
    '''
    def __operate_substitute(self, substitute: SubstituteUnit, adv_text:AdvText) -> bool:
        
        # 环节1) SubstituteUnit初始化
        substitute.initial_decision_score = adv_text.decision_score
        substitute.exchange_max_decision_score = adv_text.decision_score
        substitute.exchange_max_decision_label = adv_text.origin_label
        substitute.exchange_max_decision_word = substitute.origin_word

        # 环节2）逐一遍历候选词集，尝试找到最佳替换词
        for index, candidate in enumerate(substitute.candicates):
            
            # 2.1 替换并生成替换后的候选文本
            substitute.exchange_word = candidate
            substitute.state = SubstituteState.WORD_REPLACING
            tools.show_log(f'************** {index} -round, candidate = {candidate}, substitute.state = {substitute.state}')
            latest_candidate_text = tools.generate_latest_text(adv_text)

            # 2.2 检验，输入到攻击模型；计算决策分数
            candidate_probs, prob_label = self.__validator.model_output(latest_candidate_text)
            cur_decision_score = self.__get_decision_score(candidate_probs, adv_text)
            tools.show_log(f'**************candidate={candidate}, label(origin->prob): {adv_text.origin_label}->{prob_label}, cur_greedy_score = {cur_decision_score}')
            
            # 2.3 判断当前候选词是否是最佳的
            if cur_decision_score <= substitute.initial_decision_score:
                tools.show_log(f'************** continue --> cur_decision_score{cur_decision_score} <= {substitute.initial_decision_score}initial_greedy_score')
                continue
            if cur_decision_score <= substitute.exchange_max_decision_score:
                tools.show_log(f'************** continue --> cur_decision_score{cur_decision_score} <= {substitute.exchange_max_decision_score}exchange_max_greedy_score')
                continue
            # sim_score = self.__validator.cosine_similarity(adv_text.origin_text, latest_candidate_text)
            # if sim_score < Pattern.Sentence_Similarity_Threshold:
            #     tools.show_log(f'************** sim_score{sim_score} < {Pattern.Sentence_Similarity_Threshold}')
            #     continue
            
            # 2.4 找到最佳替换词，更新语义词信息
            substitute.exchange_max_decision_score = cur_decision_score
            substitute.exchange_max_decision_word = candidate
            substitute.exchange_max_decision_label = prob_label
            substitute.exchange_max_decision_prob = candidate_probs[adv_text.origin_label]
            substitute.exchange_max_decision_text = latest_candidate_text
        
            tools.show_log(f'**************exchange_max_greedy_word = {substitute.exchange_max_decision_word}, exchange_max_greedy_label = {substitute.exchange_max_decision_label}, exchange_max_greedy_score = {substitute.exchange_max_decision_score}')
            tools.show_log(f'**************exchange_max_greedy_text = {substitute.exchange_max_decision_text}')
            
            # 2.5 如果成功，不再搜索
            if prob_label != adv_text.origin_label:
                break

        # 环节3）判断累计决策得到的最佳候选词是否有效
        # 3.1 决策累计搜索是否更新了替换词
        if substitute.exchange_max_decision_score <= substitute.initial_decision_score:
            substitute.state = SubstituteState.WORD_INITIAL
            tools.show_log(f'**************return substitute.state = {substitute.state}, exchange_max_greedy_score{substitute.exchange_max_decision_score} <= {substitute.initial_decision_score}initial_greedy_score')
            return False
        
        # # 3.2 TODO 是否满足语义词级别的相似性标准
        # sim_score = self.__validator.cosine_similarity(adv_text.origin_text, substitute.exchange_max_decision_text)
        # tools.show_log(f'**************__operate_substitute sim_score = {sim_score}')
        # if sim_score < Pattern.Sentence_Similarity_Threshold:
        #     substitute.state = SubstituteState.WORD_INITIAL
        #     tools.show_log(f'**************return sim_score = {sim_score} < {Pattern.Sentence_Similarity_Threshold}')
        #     return False
        
        # 环节4）本轮产生了的最佳且有效的替换词
        # 4.1 更新全局信息
        substitute.state = SubstituteState.WORD_REPLACED
        adv_text.decision_score = substitute.exchange_max_decision_score
        
        # 4.2 收集评价指标信息
        adv_text.adversary_info.perturbated_token_count = adv_text.adversary_info.perturbated_token_count + 1
        adv_text.adversary_info.adversary_accurary = substitute.exchange_max_decision_prob
        adv_text.adversary_info.adversary_text = substitute.exchange_max_decision_text
        adv_text.adversary_info.adversary_label = substitute.exchange_max_decision_label
        
        # 4.3 判断当前候选文本是否对抗成功
        cur_adversary_success = (substitute.exchange_max_decision_label != adv_text.origin_label)
        if cur_adversary_success:
            # 收集评价指标信息
            adv_text.adversary_info.attack_success = True
            tools.show_log(f'**************ATTACK SUCCESS**************')
            return True

        tools.show_log(f'**************return substitute.state = {substitute.state} | exchange_max_greedy_word = {substitute.exchange_max_decision_word}, exchange_max_greedy_score = {substitute.exchange_max_decision_score}')
        return False

    '''
       计算脆弱值，并降序排序
    '''
    def __sorted_by_fragile_score(self, substitute_units: List[SubstituteUnit], adv_text: AdvText) -> List[SubstituteUnit]:
        # 1 计算脆弱值
        # //TODO 验证：是否要取前 Top k个，是否要过滤掉负值
        for index, substitute in enumerate(substitute_units):
            if substitute.state == SubstituteState.WORD_REPLACED:
                continue
            self.__validator.operate_fragile(substitute, adv_text)
            tools.show_log(f'compute fragile score-{index}, fragile_score = {substitute.fragile_score}')
        
        # 2 sort按脆弱值大小降序  
        sorted_substitute_list = list(sorted(substitute_units, key = lambda t : t.fragile_score, reverse = True))
        return sorted_substitute_list

    '''
       计算脆弱值，并降序排序
    '''
    def __pick_max_fragile_substitute(self, substitute_units: List[SubstituteUnit], adv_text: AdvText) -> SubstituteUnit:
        # 1 计算脆弱值
        # //TODO 验证：是否要取前 Top k个，是否要过滤掉负值
        for index, substitute in enumerate(substitute_units):
            if substitute.state == SubstituteState.WORD_REPLACED:
                continue
            self.__validator.operate_fragile(substitute, adv_text)
            tools.show_log(f'compute fragile score-{index}, fragile_score = {substitute.fragile_score}')
        
        # 2 sort按脆弱值大小降序  
        sorted_substitute_list = list(sorted(substitute_units, key = lambda t : t.fragile_score, reverse = True))
        
        # 3 返回最大的
        max_substitute = sorted_substitute_list.pop(0)
        return max_substitute
    
    '''
        计算贪心选择的决策值
    '''
    def __get_decision_score(self, candidate_probs:List[float], adv_text:AdvText) -> float:
        decision_score = 0
        origin_probs = adv_text.origin_probs
        
        if Pattern.Algorithm == AlgoType.CWordAttacker:
            if Pattern.IsTargetAttack:
                target_label = Pattern.Target_Label
                decision_score = candidate_probs[target_label] - origin_probs[target_label]
            else:
                origin_label = adv_text.origin_label
                decision_score = origin_probs[origin_label] - candidate_probs[origin_label]
        else:
            target_label = Pattern.Target_Label
            origin_label = adv_text.origin_label
            if Pattern.IsTargetAttack:
                decision_score = (candidate_probs[target_label] - origin_probs[target_label]) + (origin_probs[origin_label] - candidate_probs[origin_label])
            else:
                decision_score = origin_probs[origin_label] - candidate_probs[origin_label]
        return decision_score