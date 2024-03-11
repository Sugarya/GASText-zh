
from .adversary_entity import AdversaryEntity
from .base_entity import BaseEntity 

'''
    文本对象
'''
class AdvText(BaseEntity):

    def __init__(self, origin_label, origin_text, origin_probs):
        self.origin_label = origin_label
        self.origin_text = origin_text
        self.origin_probs = origin_probs

        # 实时计算中，存储评价指标相关的信息
        self.adversary_entity = AdversaryEntity(origin_text, origin_probs[origin_label])
        # 原始文本的每个token单元构成的列表
        self.token_units = []




 