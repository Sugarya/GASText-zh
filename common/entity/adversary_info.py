from .base_entity import BaseEntity 

'''
    收集评价指标的信息
'''
class AdversaryInfo(BaseEntity):

    def __init__(self, origin_text:str, origin_label:int, origin_accurary:float):
        # 是否攻击成功
        self.attack_success:bool = False

        self.adversary_label:int = origin_label

        self.origin_text = origin_text

        self.adversary_text:str = None

        # 原始文本的原始标签的概率值
        self.origin_accurary:float = origin_accurary

        # 对抗样本的原始标签概率值
        self.adversary_accurary:float = None

        # 文本中token的总数
        self.total_token_number:int = None

        # 对抗攻击成功后，文本里被扰动的词语的数量
        self.perturbed_token_number:int = None

        # 和原始文本的相似度，范围：0～1
        self.similarity:float = None
                
        # 查询模型的次数
        self.query_times:float = 0



    