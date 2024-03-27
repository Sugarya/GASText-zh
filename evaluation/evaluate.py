
from typing import List
import os, json
import math, time
from common.entity import AdversaryInfo, EvaluationInfo, AdversaryInfoArrayJSONEncoder
from common.utils import tools
from config import Pattern
from arguement import ArgumentDict

'''
    实验指标汇总计算
'''
class Evaluator():

    def __init__(self) -> None:
        # 本次命令运行的结果，对其打印和持久化
        self.__evaluation_result = EvaluationInfo()

        # 收集到的评价指标信息
        self.__adversary_infos:List[AdversaryInfo] = []


    def set_origin_example_count(self, count:int):
        self.__evaluation_result.validated_example_count = count

    def add(self, adversary_info:AdversaryInfo):
        self.__adversary_infos.append(adversary_info)



    def __persist_to_file(self):
        current_parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
        dir_file_path = f'{current_parent_dir}/output_result/{Pattern.Algorithm.name}'
        exist = os.path.exists(dir_file_path)
        if not exist:
            os.makedirs(dir_file_path)
        
        arg_style = ArgumentDict['style']
        localtime = time.localtime(time.time())
        date_time = f'{localtime[1]}{localtime[2]}_{localtime[3]}{localtime[4]}_{localtime[5]}'
        file_path = f'{dir_file_path}/{arg_style}_{date_time}.json'
        tools.show_log(f'The file path of experiment result is {file_path}')
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            # f.writelines(lines)
            json.dump(self.__evaluation_result, f, ensure_ascii=False, default=self.__evaluation_result.to_dict)
            f.write('\n\n\n')
            json.dump(self.__adversary_infos, f, ensure_ascii=False, cls=AdversaryInfoArrayJSONEncoder)
            


    def compute(self):
        origin_accurary_sum = 0
        adversary_accurary_sum = 0
        attack_success_sum = 0

        text_token_sum = 0
        perturbed_token_sum = 0

        sim_score_sum = 0
        # success_similarity_score_sum = 0
        query_times_sum = 0
        
        for index, adversary_info in enumerate(self.__adversary_infos):
            if adversary_info.attack_success:
                origin_accurary_sum += adversary_info.origin_accurary
                adversary_accurary_sum += adversary_info.adversary_accurary
                
                attack_success_sum += 1
                sim_score_sum += adversary_info.similarity
                perturbed_token_sum += adversary_info.perturbated_token_count
                text_token_sum += adversary_info.text_token_count
                query_times_sum += adversary_info.query_times
        
        self.__evaluation_result.attack_success_sum = attack_success_sum
        if attack_success_sum != 0:
            self.__evaluation_result.ave_origin_accurary = origin_accurary_sum / attack_success_sum
            self.__evaluation_result.ave_adversary_accurary = adversary_accurary_sum / attack_success_sum
            self.__evaluation_result.ave_accurary_reduction = (origin_accurary_sum - adversary_accurary_sum) / attack_success_sum

            self.__evaluation_result.ave_sim_score = sim_score_sum / attack_success_sum
            self.__evaluation_result.ave_perturbated_count = perturbed_token_sum / attack_success_sum
            self.__evaluation_result.ave_query_times = query_times_sum / attack_success_sum

        validated_example_count = self.__evaluation_result.validated_example_count
        if validated_example_count != 0:
            self.__evaluation_result.attack_success_rate = attack_success_sum / validated_example_count
        if text_token_sum != 0:
            self.__evaluation_result.ave_perturbated_rate = perturbed_token_sum / text_token_sum

        self.__evaluation_result.target_attack = Pattern.IsTargetAttack
        self.__evaluation_result.target_label = Pattern.Target_Label

        self.__persist_to_file()

        
 


    