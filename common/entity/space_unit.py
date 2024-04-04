from typing import List,Tuple
from queue import PriorityQueue
from .base_entity import BaseEntity
from .token_unit import SememicUnit, SememicState

'''
    领域结构实体
'''
class SpaceUnit(BaseEntity):

    def __init__(self, columns: List[SememicUnit], column_size) -> None:
        super().__init__()

        self.columns:List[SememicUnit] = [column for column in columns]

        self.exchange_word_indexs:List[int] = [None] * column_size
        self.exchange_max_decision_score = -1
        self.exchange_max_decision_info = DecisionInfo()


# 确定领域最佳决策后，得到的各种信息存放于此
class DecisionInfo(BaseEntity):

    def __init__(self) -> None:
        super().__init__()
        
        self.columns:List[SememicUnit] = []
        self.combination_indexs = None
        self.decision_words:List[str] = None

        self.candidate_sample:str = None
        self.prob_label:int = None
        self.prob:float = 0
        
    def __lt__(self, other):
        return self.prob < other.prob



