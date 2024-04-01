from typing import List, Tuple
import math, heapq
import numpy as np
from common.utils import tools
from common.entity import SpaceUnit, AdvText, SememicUnit, AdversaryInfo, SememicState, DecisionInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, AlgoType


class MaskedBeamSearch:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        self.__validator = validator
        self.__substituter = substituter

        self.Colunm_Size = Pattern.Space_Column_Size
        self.Beam_Width = Pattern.Beam_Width
        self.Substitute_Volume = Pattern.Substitute_Volume
        
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

    def __generate_spaceinfo_list(self, substitute_units: List[SememicUnit], adv_text: AdvText) -> List[SpaceUnit]:
        space_info_list = []

        temp_substitute_container = []
        substitute_units_size = len(substitute_units)
        for index, substitute_unit in enumerate(substitute_units):
            tools.show_log(f'*****substitute- {index} -Round')

            # 1）生成替代词
            origin_word, origin_pos = substitute_unit.origin_word, substitute_unit.origin_pos
            tools.show_log(f'***** origin_word = {origin_word} -> pos = {origin_pos}')
            substitute_unit.candicates = self.__substituter.generate_hybrid_candidates(substitute_unit, adv_text)
            
            # 2) 没有同义词集，跳过
            isLast = (index == substitute_units_size - 1)
            if len(substitute_unit.candicates) <= 1:
                tools.show_log(f'*****跳过{substitute_unit.origin_word}，其同义词为空')
                container_len = len(temp_substitute_container)
                if isLast and container_len > 0: # 最后一个，把剩余的装入
                    space_info_list.append(SpaceUnit(temp_substitute_container, container_len, self.Beam_Width))
                continue
            
            # 3）添加领域
            temp_substitute_container.append(substitute_unit)
            container_len = len(temp_substitute_container)
            if container_len == self.Colunm_Size:
                space_info_list.append(SpaceUnit(temp_substitute_container, container_len, self.Beam_Width))
                temp_substitute_container.clear()
            else:
                if isLast: # 最后一个则把剩余的装入
                    space_info_list.append(SpaceUnit(temp_substitute_container, container_len, self.Beam_Width))


        tools.show_log(f'space_info_list = {space_info_list}')
        return space_info_list
    
    def __travel_spaceinfos(self, space_unit_list: List[SpaceUnit], adv_text: AdvText):
        for index, space_unit in enumerate(space_unit_list):
            tools.show_log(f'*****space_info - {index} - Round')

            if len(adv_text.decision_queue[0][1]) > 0:
                tools.show_log(f'*****decision_queue tuple | {len(adv_text.decision_queue[0][1])} > 0')
                space_unit.initial_decision_queue = adv_text.decision_queue

            if not space_unit.initial_decision_queue:
                self.__operate_space_unit(space_unit, adv_text)
                continue

            tools.show_log(f'*****loop in initial_decision_queue')
            for (decision_score, initial_decision_info_list) in space_unit.initial_decision_queue:
                # 初始化，更新语义词状态，为领域遍历时生成所需的最新文本
                for initial_decision_info in initial_decision_info_list:
                    for (sememe, initial_state, word) in zip(initial_decision_info.columns, initial_decision_info.decision_states, initial_decision_info.decision_words):
                        sememe.state = initial_state
                        if initial_state == SememicState.WORD_REPLACED:
                            sememe.exchange_max_decision_word = word
                        elif initial_state == SememicState.WORD_REPLACING:
                            sememe.exchange_word = word
                self.__operate_space_unit(space_unit, adv_text, initial_decision_info_list)



    def __operate_space_unit(self, space_unit: SpaceUnit, adv_text: AdvText, initial_decision_list:List[DecisionInfo] = None) -> bool:
        cur_column_size = len(space_unit.columns)
        space_capacity = int(math.pow(self.Substitute_Volume, cur_column_size))
        # 1 遍历领域，逐一计算组合决策值
        for num in range(space_capacity):
            cur_indexs = list(np.base_repr(num, base=self.Substitute_Volume))
            tools.show_log(f'*****{num} in space_capacity = {space_capacity}, cur space column_size = {cur_column_size}')
            
            diff_len = cur_column_size - len(cur_indexs)
            if diff_len >= 1:
                for i in range(diff_len):
                    cur_indexs.append(0)
            cur_indexs = list(map(lambda t:int(t), cur_indexs)) 
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
            tools.show_log(f'*****decision_words = {decision_words}')

            # 获得该领域下当前组合的文本
            lastest_text = tools.generate_latest_text(adv_text)
            tools.show_log(f'*****lastest_text = {lastest_text}')
            probs, prob_label = self.__validator.model_output(lastest_text)
            decision_score = self.__get_decision_score(probs, adv_text)
            tools.show_log(f'*****decision_score = {decision_score}')
            
            # 判断当前组合是否是领域最佳的，优先级队列按默认生序来
            if space_unit.initial_decision_queue:
                if decision_score <= space_unit.initial_decision_queue[0][0]:
                    tools.show_log(f'*****continue | decision_score{decision_score } < {space_unit.initial_decision_queue[0][0]}initial_decision_queue_min_score')
                    continue
            if space_unit.exchange_max_decision_queue:
                if decision_score <= space_unit.exchange_max_decision_queue[0][0]:
                    tools.show_log(f'*****continue | decision_score{decision_score} < {space_unit.exchange_max_decision_queue[0][0]}exchange_max_decision_queue_min_score')
                    continue

            # 得到最佳组合，更新当前为最佳组合
            decision_info = DecisionInfo()
            decision_info.columns = space_unit.columns
            decision_info.combination_indexs = cur_indexs
            decision_info.decision_words = decision_words
            decision_info.decision_states = [column.state for column in space_unit.columns]

            decision_info.candidate_sample = lastest_text
            decision_info.prob_label = prob_label
            decision_info.prob = probs[prob_label]
            tools.show_log(f'-------come up a current best combination：decision_info decision_states = {decision_info.decision_states}')

            heapq.heapreplace(space_unit.exchange_max_decision_queue, (decision_score, decision_info))
            
            tools.show_log(f'*****prob_label={decision_info.prob_label} -- {adv_text.origin_label}adv_text.origin_label')
            # 是否对抗成功，成功break
            if prob_label != adv_text.origin_label:
                break

        # 2.1 判断当前最佳组合是否有效，即是否存在大于全局决策值
        if space_unit.exchange_max_decision_queue[(self.Beam_Width - 1)][0] <= adv_text.decision_queue[0][0]:
            # 无效的最佳组合更新到全局
            tools.show_log(f'*****continue | exchange_max_decision score{space_unit.exchange_max_decision_queue[(self.Beam_Width - 1)][0]} <= {adv_text.decision_queue[0][0]}adv_text.decision_queue score')
            self.__update_to_global(SememicState.WORD_INITIAL, space_unit.exchange_max_decision_queue, adv_text.decision_queue, initial_decision_list)
            return False
        # 2.2 判断是否满足约束
        if self.__disable_candidate_sample(adv_text):
            tools.show_log(f'*****continue | disable_candidate_sample')
            self.__update_to_global(SememicState.WORD_INITIAL, space_unit.exchange_max_decision_queue, adv_text.decision_queue, initial_decision_list)
            return False

        # 3 存在有效的最佳组合，把其更新到全局
        tools.show_log(f'------exsit an effective and best combiantation, update to global...')
        self.__update_to_global(SememicState.WORD_REPLACED, space_unit.exchange_max_decision_queue, adv_text.decision_queue, initial_decision_list)

        # 5 计算评价指标数据-part1
        self.__validator.collect_MBF_common_adversary(decision_info, adv_text)

        # 4 判断是否对抗成功
        for (desicion_score, decision_info) in reversed(space_unit.exchange_max_decision_queue):
            if decision_info.prob_label != adv_text.origin_label:
                # 计算评价指标数据-part2
                self.__validator.collect_MBF_adversary_when_attack_success(decision_info, adv_text)
                tools.show_log(f'**************ATTACK SUCCESS**************')
                return True
        
        # 计算评价指标数据-part3
        self.__validator.collect_MBF_adversary_when_attack_failure(decision_info, adv_text)
        return False
    

    def __update_to_global(self, type:SememicState, 
                           exchange_max_decision_queue:List[Tuple[int, DecisionInfo]], 
                           decision_queue:List[Tuple[int, List[DecisionInfo]]],
                           initial_decision_infos:List[DecisionInfo]):
        # 语义词状态更新, 加入历史决策
        for (score, decision_info) in reversed(exchange_max_decision_queue):
            if score > decision_queue[0][0]:
                if type == SememicState.WORD_INITIAL:
                    decision_info.decision_states = [SememicState.WORD_INITIAL, SememicState.WORD_INITIAL, SememicState.WORD_INITIAL]
                elif type == SememicState.WORD_REPLACED:
                    for index, combination_index in enumerate(decision_info.combination_indexs):
                        if combination_index == 0:
                            decision_info.decision_states[index] = SememicState.WORD_INITIAL
                        else:
                            decision_info.decision_states[index] = SememicState.WORD_REPLACED 
                
                if initial_decision_infos != None:
                    initial_decision_infos.append(decision_info)
                    heapq.heapreplace(decision_queue, (score, initial_decision_infos))
                else:
                    heapq.heapreplace(decision_queue, (score, [decision_info]))


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
    
    
    def __disable_candidate_sample(self,adv_text: AdvText) -> bool:         
        return False

    
    