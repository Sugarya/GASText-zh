
from typing import List
import os
import json
import time, math
from common.entity import AdversaryInfo, EvaluationResult, AdversaryInfoArrayJSONEncoder
from common.utils import tools
from config import Pattern

'''
    实验指标汇总计算
'''
class Evaluator():

    def __init__(self) -> None:
        # 本次命令运行的结果，对其打印和持久化
        self.__evaluation_result = EvaluationResult()

        # 收集到的评价指标信息
        self.__adversary_infos:List[AdversaryInfo] = []


    def set_origin_example_count(self, count:int):
        self.__evaluation_result.origin_example_count = count

    def add(self, adversary_info:AdversaryInfo):
        self.__adversary_infos.append(adversary_info)



    def __persist_to_file(self):
        dir_file_path = f'{os.getcwd()}/output_result/'
        exist = os.path.exists(dir_file_path)
        if not exist:
            os.mkdir(dir_file_path)
        
        file_path=f'{dir_file_path}{Pattern.Algorithm.name}_{math.floor(time.time())}.json'
        tools.show_log(f'The file path of experiment result is {file_path}')
        with open(file_path, 'w', encoding='utf-8', errors='replace') as f:
            # f.writelines(lines)
            json.dump(self.__evaluation_result, f, ensure_ascii=False, default=self.__evaluation_result.to_dict)
            f.write('\n\n\n')
            json.dump(self.__adversary_infos, f, ensure_ascii=False, cls=AdversaryInfoArrayJSONEncoder)
            



    def compute(self):
        origin_accurary_sum = 0
        adversary_accurary_sum = 0
        attack_success_count = 0

        text_token_sum = 0
        perturbed_token_sum = 0

        similarity_score_sum = 0
        query_times_sum = 0
        
        for index, adversary_info in enumerate(self.__adversary_infos):
            origin_accurary_sum += adversary_info.origin_accurary
            adversary_accurary_sum += adversary_info.adversary_accurary

            if adversary_info.attack_success:
                attack_success_count += 1
            
            perturbed_token_sum += adversary_info.perturbated_token_count
            text_token_sum += adversary_info.text_token_count

            similarity_score_sum += adversary_info.similarity
            query_times_sum += adversary_info.query_times
        
        origin_example_count = self.__evaluation_result.origin_example_count
        self.__evaluation_result.ave_origin_accurary = origin_accurary_sum / origin_example_count
        self.__evaluation_result.ave_adversary_accurary = adversary_accurary_sum / origin_example_count
        self.__evaluation_result.ave_accurary_reduction = (origin_accurary_sum - adversary_accurary_sum) / origin_example_count

        self.__evaluation_result.attack_rate = attack_success_count / origin_example_count
        self.__evaluation_result.ave_perturbated_rate = perturbed_token_sum / text_token_sum

        self.__evaluation_result.ave_sim_score = similarity_score_sum / origin_example_count
        self.__evaluation_result.ave_query_times = query_times_sum / origin_example_count

        self.__persist_to_file()

        
 


    