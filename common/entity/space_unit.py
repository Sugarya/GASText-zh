from typing import List,Tuple
from queue import PriorityQueue
from .base_entity import BaseEntity
from .token_unit import SememicUnit, SememicState

'''
    领域结构实体
'''
class SpaceUnit(BaseEntity):

    def __init__(self, columns: List[SememicUnit], column_size, beam_width = 2) -> None:
        super().__init__()

        self.columns:List[SememicUnit] = [column for column in columns]

        self.initial_decision_queue:List[Tuple[int, List[DecisionInfo]]] = None

        self.exchange_word_indexs:List[int] = [None] * column_size
        self.exchange_max_decision_queue:List[Tuple[int, DecisionInfo]] = [(0, DecisionInfo())] * beam_width


# 确定领域最佳决策后，得到的各种信息存放于此
class DecisionInfo(BaseEntity):

    def __init__(self) -> None:
        super().__init__()
        
        self.columns:List[SememicUnit] = None
        self.combination_indexs = None
        self.decision_words:List[str] = None
        self.decision_states:List[SememicState] = None

        self.candidate_sample:str = None
        self.prob_label:int = None
        self.prob:float = 0
        
    def __lt__(self, other):
        return self.prob < other.prob



