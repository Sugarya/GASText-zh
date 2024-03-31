
from .adversary_info import AdversaryInfo
from .base_entity import BaseEntity
from .token_unit import TokenUnit, SubstituteUnit
from typing import List

'''
    文本对象
'''
class AdvText(BaseEntity):

    def __init__(self, origin_label:int, origin_text:str, origin_probs:List[float]):
        self.origin_label:int = origin_label
        self.origin_text:str = origin_text
        self.origin_probs:List[float] = origin_probs
        self.incomplete_initial_probs:List[float] = None

        # 贪心选择的依据，决策分数值累计增大
        self.decision_score:float = 0
        # 实时计算中，存储评价指标相关的信息
        self.adversary_info:AdversaryInfo = AdversaryInfo(origin_text, origin_label, origin_probs[origin_label])
        # 原始文本的每个token单元构成的列表
        self.token_units: List[TokenUnit] = None
        # token_units的元素数量
        self.token_count:int = None
        
        # MaskedBeamFooler方法内使用
        self.substitute_count:int = None # 分词得到的语义词的数量
        self.decision_queue = []
        self.decision_substitute_list:List[SubstituteUnit] = []
 