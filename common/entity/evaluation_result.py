from .base_entity import BaseEntity 

'''
    评价指标的统计结果
'''
class EvaluationResult(BaseEntity):

    def __init__(self) -> None:
        # 原始样本的数量
        self.origin_example_count:int = None

        # 模型准确率
        self.ave_origin_accurary:float = None
        self.ave_adversary_accurary:float = None
        self.ave_accurary_reduction:float = None

        self.attack_rate:float = None
        
        # 扰动率
        self.ave_perturbated_rate:float = None

        self.ave_sim_score:float = None

        self.ave_query_times:int = None
        
    def to_dict(self, obj):
        return {
            'ave_origin_accurary': self.ave_origin_accurary,
            'ave_adversary_accurary': self.ave_adversary_accurary,
            'ave_accurary_reduction':self.ave_accurary_reduction,
            'attack_rate':self.attack_rate,
            'ave_perturbated_rate':self.ave_perturbated_rate,
            'ave_sim_score':self.ave_sim_score,
            'ave_query_times':self.ave_query_times
        }
