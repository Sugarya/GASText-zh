from typing import List, Tuple
import math, heapq
import numpy as np
from common.utils import tools
from common.entity import SpaceUnit, AdvText, SememicUnit, AdversaryInfo, SememicState, DecisionInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, ArgSpaceStyle


class MaskedAreaSearch:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        self.__validator = validator
        self.__substituter = substituter
        
    def search(self, substitute_units: List[SememicUnit], adv_text: AdvText):
        units_size = len(substitute_units)
        adv_text.substitute_count = units_size
        tools.show_log(f'WordMaskedGreedy search, the length of substitute_units = {units_size}')
        
        # 1）计算脆弱值并降序排序
        sorted_substitutes = self.__sorted_by_fragile_score(substitute_units, adv_text)

        # 2）生成领域对象序列
        space_info_list = self.__generate_spaceinfo_list(sorted_substitutes, adv_text)

        # 3) 遍历领域对象，逐一计算领域内每个组合决策值，更新最佳组合信息
        self.__travel_spaceinfos(space_info_list, adv_text)

    '''
       计算脆弱值，并降序排序
    '''
    def __sorted_by_fragile_score(self, substitute_units: List[SememicUnit], adv_text: AdvText) -> List[SememicUnit]:
        # 1 计算语义词缺失下的初始脆弱值
        adv_text.incomplete_initial_probs = self.__validator.generate_incomplete_initial_probs(adv_text)
        
        # 2 计算每个语义词的脆弱值,/TODO 验证：是否要取前 Top k个，是否要过滤掉负值
        for index, substitute in enumerate(substitute_units):
            if substitute.state == SememicState.WORD_REPLACED:
                continue
            self.__validator.operate_fragile(substitute, adv_text)
        
        # 1 sort按脆弱值大小降序
        sorted_substitute_list = list(sorted(substitute_units, key = lambda t : t.fragile_score, reverse = True))
        sorted_words = list(map(lambda t:f'{t.pos_in_text}-{t.origin_word}',sorted_substitute_list))
        tools.show_log(f'sorted_substitute_list = {sorted_words}')
        
        return sorted_substitute_list

    '''
        生成领域序列，确定领域宽度信息
    '''
    def __generate_sequence(self, substitute_units: List[SememicUnit]) -> List[int]:
        sequence = []
        size = len(substitute_units)
        if Pattern.Space_Style:
            if Pattern.Space_Style == ArgSpaceStyle.Single:
                tools.show_log(f'Now, its runing via {Pattern.Space_Style}')
                sequence = [1 for s in range(size)]
            elif Pattern.Space_Style == ArgSpaceStyle.Capital:
                tools.show_log(f'Now, its runing via {Pattern.Space_Style}')
                sequence = [Pattern.Space_Width]
                if size >= 3:
                    sequence.extend([1 for s in range(size - 2)])
            elif Pattern.Space_Style == ArgSpaceStyle.Alternate:
                tools.show_log(f'Now, its runing via {Pattern.Space_Style}')
                sequence = [1 for s in range(size)]
                for i in range(size):
                    if i % 2 == 0:
                        sequence[i] = Pattern.Space_Width
            elif Pattern.Space_Style == ArgSpaceStyle.Full:
                tools.show_log(f'Now, its runing via {Pattern.Space_Style}')
                sequence = [Pattern.Space_Width for s in range(math.ceil(size / 2))]  
            return sequence
        
        sequence = [Pattern.Space_Width]
        if size >= 3:
            sequence.extend([1 for s in range(size - 2)])        

        return sequence

    def __generate_spaceinfo_list(self, substitute_units: List[SememicUnit], adv_text: AdvText) -> List[SpaceUnit]:
        space_info_list = []
        sequence = self.__generate_sequence(substitute_units)
        sequence_index = 0

        temp_substitute_container = []
        for index, substitute_unit in enumerate(substitute_units):
            tools.show_log(f'*****substitute- {index} -Round')

            # 1）生成替代词
            origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
            tools.show_log(f'***** origin_word = {origin_word} -> pos = {origin_pos}')
            substitute_unit.candicates = self.__substituter.generate(substitute_unit, adv_text)
            
            # 2) 没有同义词集，跳过
            if not substitute_unit.candicates or len(substitute_unit.candicates) <= 1:
                tools.show_log(f'*****跳过{substitute_unit.origin_word}，其同义词为空')
                continue
            
            # 3）添加领域
            temp_substitute_container.append(substitute_unit)
            container_len = len(temp_substitute_container)
            if container_len == sequence[sequence_index]:
                space_info_list.append(SpaceUnit(temp_substitute_container, container_len, Pattern.Space_Depth))
                sequence_index = sequence_index + 1
                temp_substitute_container.clear()

        container_len = len(temp_substitute_container)
        if container_len > 0: #把剩余的装入
            space_info_list.append(SpaceUnit(temp_substitute_container, container_len, Pattern.Space_Depth))

        # tools.show_log(f'space_info_list = {space_info_list}')
        return space_info_list
    
    def __travel_spaceinfos(self, space_unit_list: List[SpaceUnit], adv_text: AdvText) -> bool:
        for index, space_unit in enumerate(space_unit_list):
            tools.show_log(f'*****space_info - {index} - Round')
            attack_success = self.__operate_space_unit(space_unit, adv_text)
            if attack_success:
                adv_text.adversary_info.attack_success = True
                self.__validator.collect_MBF_adversary_when_ending(adv_text)
                return True
        
        # 计算评价指标数据
        self.__validator.collect_MBF_adversary_when_ending(adv_text)
        return False

    # 转为数字
    def __mapping_to_num(self, s:str) -> int:
        if s.isdigit():
            return int(s)
        else:
            return ord(s.upper()) - 55


    def __operate_space_unit(self, space_unit: SpaceUnit, adv_text: AdvText) -> bool:
        cur_column_size = len(space_unit.columns)
        space_capacity = int(math.pow(space_unit.depth, cur_column_size))
        # 1 遍历领域，逐一计算组合决策值
        for num in range(space_capacity):
            cur_indexs = list(map(self.__mapping_to_num, list(np.base_repr(num, base=space_unit.depth))))
            tools.show_log(f'*****{num} in space_capacity = {space_capacity}, cur space column_size = {cur_column_size}')
            
            diff_len = cur_column_size - len(cur_indexs)
            if diff_len >= 1:
                for i in range(diff_len):
                    cur_indexs.append(0)
            tools.show_log(f'*****complete cur_indexs = {cur_indexs}')
            
            # 替换词集存在长度不满情况，忽略这部分组合
            disable = False
            for index, (cur_index, sememic_unit) in enumerate(zip(cur_indexs, space_unit.columns)):
                if cur_index >= len(sememic_unit.candicates):
                    disable = True
                    break
            if disable:
                tools.show_log(f'*****continue | disable cur_indexs = {cur_indexs}')
                continue

            # 更新当前组合下的词状态，词信息
            tools.show_log(f'sememic_unit.candicates list = {[sememic_unit.candicates for sememic_unit in space_unit.columns]}')
            decision_words = [None] * cur_column_size
            for index, (cur_index, sememic_unit) in enumerate(zip(cur_indexs, space_unit.columns)):
                decision_words[index] = sememic_unit.candicates[cur_index]
                if cur_index == 0:
                    sememic_unit.state = SememicState.WORD_INITIAL
                else:
                    sememic_unit.state = SememicState.WORD_REPLACING
                    sememic_unit.exchange_word = sememic_unit.candicates[cur_index]

            # 获得该领域下当前组合的文本
            lastest_text = tools.generate_latest_text(adv_text)
            tools.show_log(f'*****decision_words = {decision_words}, lastest_text = {lastest_text}')
            probs, prob_label = self.__validator.model_output(lastest_text)
            cur_decision_score = self.__get_decision_score(probs, adv_text)
            tools.show_log(f'*****the decision score of lastest text = {cur_decision_score}')
            tools.show_log(f'************{num}***********PROB_LABEL{prob_label}->{adv_text.origin_label}ORIGIN_LABEL**********')

            # 判断当前组合是否是领域最佳的，优先级队列按默认升序来
            attack_success = prob_label != adv_text.origin_label
            if not attack_success and cur_decision_score <= adv_text.decision_score:
                tools.show_log(f'*****CONTNUE1.1 | decision_score{cur_decision_score } < {adv_text.decision_score}adv_text.decision_score')
                continue
            if not attack_success and cur_decision_score <= space_unit.exchange_max_decision_score:
                tools.show_log(f'*****CONTINUE1.2 | decision_score{cur_decision_score} < {space_unit.exchange_max_decision_score}exchange_max_decision_score')
                continue

            # 得到最佳组合，更新当前为最佳组合
            space_unit.exchange_max_decision_score = cur_decision_score
            decision_info = DecisionInfo()
            decision_info.columns = space_unit.columns
            decision_info.combination_indexs = cur_indexs
            decision_info.decision_words = decision_words
            decision_info.candidate_sample = lastest_text
            decision_info.prob_label = prob_label
            decision_info.prob = probs[prob_label]
            space_unit.exchange_max_decision_info = decision_info
            tools.show_log(f'-------COME UP a current best combination：decision_words = {decision_info.decision_words}')
            
            # 是否对抗成功，成功break
            if attack_success:
                tools.show_log(f'******{num}-************ATTACK SUCCESS****************- | prob_label{prob_label} != {adv_text.origin_label}origin_label')
                break

        # 2.1 判断当前最佳组合是否有效，即是否存在大于全局决策值        
        if space_unit.exchange_max_decision_score <= adv_text.decision_score:
            # 无效的最佳组合更新到全局
            tools.show_log(f'*****CONTINUE2.1 | exchange_max_decision score{space_unit.exchange_max_decision_score} <= {adv_text.decision_score}adv_text.decision_score')
            self.__setup_global_intial(space_unit.exchange_max_decision_info)
            return False
        # 2.2 判断是否满足约束
        if self.__disable_candidate_sample(adv_text):
            tools.show_log(f'*****CONTINUE2.2 | disable_candidate_sample')
            self.__setup_global_intial(space_unit.exchange_max_decision_info)
            return False

        # 3 存在有效的最佳组合，把其更新到全局
        tools.show_log(f'------EXIST an effective and best combiantation{space_unit.exchange_max_decision_info.combination_indexs}={space_unit.exchange_max_decision_info.decision_words}, update to global...')
        self.__setup_global_replaced(space_unit.exchange_max_decision_score, space_unit.exchange_max_decision_info, adv_text)
        
        # 4 计算评价指标数据
        self.__validator.collect_MBF_common_adversary(decision_info, adv_text)
        # 5 判断是否对抗成功
        if space_unit.exchange_max_decision_info.prob_label != adv_text.origin_label:
            tools.show_log(f'*************FOUND IT*****ATTACK SUCCESS*****************')
            return True
        
        return False
    
    '''
        把领域状态设置为初始化
    '''
    def __setup_global_intial(self, max_decision_info: DecisionInfo,):
        for sememe in max_decision_info.columns:
            sememe.state = SememicState.WORD_INITIAL

    '''
        把领域状态设置为已替换
    '''
    def __setup_global_replaced(self, max_score:int, max_decision_info: DecisionInfo, adv_text:AdvText):
        adv_text.decision_score = max_score

        for sememe, combination_index, decision_word in zip(max_decision_info.columns, max_decision_info.combination_indexs, max_decision_info.decision_words):
            if combination_index == 0:
                sememe.state = SememicState.WORD_INITIAL
            else:
                sememe.state = SememicState.WORD_REPLACED
                sememe.exchange_max_decision_word = decision_word


    '''
        计算决策值
    '''
    def __get_decision_score(self, candidate_probs:List[float], adv_text:AdvText) -> float:
        decision_score = 0
        origin_probs = adv_text.origin_probs
        target_label = Pattern.Target_Label
        origin_label = adv_text.origin_label

        if Pattern.IsTargetAttack:
            decision_score = (candidate_probs[target_label] - origin_probs[target_label]) + (origin_probs[origin_label] - candidate_probs[origin_label])
        else:
            decision_score = origin_probs[origin_label] - candidate_probs[origin_label]
        
        return decision_score
    
    def __disable_candidate_sample(self, adv_text: AdvText) -> bool:         
        return False
