from .base_entity import BaseEntity 
from config import Pattern

'''
    评价指标的统计结果
'''
class EvaluationInfo(BaseEntity):

    def __init__(self) -> None:
        # 原始样本的数量
        self.validated_example_count:int = None

        # 模型准确率
        self.ave_origin_accurary:float = None
        self.ave_adversary_accurary:float = None
        self.ave_accurary_reduction:float = None

        # 攻击效果
        self.target_attack:bool = None
        self.target_label:int = None
        self.attack_success_sum:int = None
        self.attack_success_rate:float = None
        
        # 扰动数量和比率
        self.ave_perturbated_count:int = None
        self.ave_perturbated_rate:float = None

        # 对抗样本和原始样本的平均相似程度
        self.ave_sim_score:float = None
        # 查询模型的次数
        self.ave_query_times:int = None

        self.memo:str = f'S{Pattern.Substitute_Volume}C{Pattern.Space_Width}'
        
    def to_dict(self, obj):
        return {
            'target_attack':self.target_attack,
            'target_label':self.target_label,
            'validated_example_count':self.validated_example_count,
            'attack_success_sum':self.attack_success_sum,
            'attack_success_rate':self.attack_success_rate,
            'ave_sim_score':self.ave_sim_score,
            'ave_origin_accurary':self.ave_origin_accurary,
            'ave_adversary_accurary':self.ave_adversary_accurary,
            'ave_accurary_reduction':self.ave_accurary_reduction,
            'ave_perturbated_count':self.ave_perturbated_count,
            'ave_perturbated_rate':self.ave_perturbated_rate,
            'ave_query_times':self.ave_query_times,
            'memo':self.memo
        }
