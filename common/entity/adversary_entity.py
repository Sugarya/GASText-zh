from .base_entity import BaseEntity 

'''
    收集评价指标的信息
'''
class AdversaryEntity(BaseEntity):

    def __init__(self, origin_text, origin_accurary) -> None:
        self.origin_text = origin_text
        self.origin_accurary = origin_accurary
        
        # 查询模型的次数
        self.query_times = None

        # 是否攻击成功
        self.attack_success = None

        self.adversary_text = None
        self.adversary_label = None
        self.adversary_accurary = None

        # 文本中token的总数
        self.total_token_number = None
        # 对抗攻击成功后，文本里被扰动的词语的数量
        self.perturbed_token_number = None

        # 和原始文本的相似度，范围：0～1
        self.similarity = None



    