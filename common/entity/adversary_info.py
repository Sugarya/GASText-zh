from .base_entity import BaseEntity 
from json import JSONEncoder
from typing import List



'''
    收集评价指标的信息
'''
class AdversaryInfo(BaseEntity):

    def __init__(self, origin_text:str, origin_label:int, origin_accurary:float):
        # 是否攻击成功
        self.attack_success:bool = False
        self.origin_label:int = origin_label 
        self.adversary_label:int = origin_label
        self.origin_text:str = origin_text
        
        self.adversary_text:str = None

        # 原始文本的原始标签的概率值
        self.origin_accurary:float = origin_accurary
        # 对抗样本的原始标签概率值
        self.adversary_accurary:float = None

        # 文本中token的总数
        self.text_token_count:int = None
        # 对抗攻击成功后，文本里被扰动的词语的数量
        self.perturbated_token_count:int = 0

        # 和原始文本的相似度，范围：0～1
        self.similarity:float = None
        # 查询模型的次数
        self.query_times:float = 0
    

    def to_dict(self):
        return {
            'attack_success':self.attack_success,
            'origin_label':int(self.origin_label),
            'adversary_label':int(self.adversary_label),
            'origin_text':str(self.origin_text),
            'adversary_text':str(self.adversary_text),
            'origin_accurary':float(self.origin_accurary),
            'adversary_accurary':float(self.adversary_accurary),
            'text_token_count':int(self.text_token_count),
            'perturbated_token_count':int(self.perturbated_token_count),
            'similarity':float(self.similarity),
            'query_times':int(self.query_times),
        }



class AdversaryInfoArrayJSONEncoder(JSONEncoder):

    def default(self, obj:AdversaryInfo):
        print(f'obj = {obj}')
        return obj.to_dict()
   
    

      