from typing import List,Tuple
from queue import PriorityQueue
from .base_entity import BaseEntity
from .token_unit import SubstituteUnit

class SpaceInfo(BaseEntity):

    def __init__(self, columns: List[SubstituteUnit], column_size = 3, beam_width = 2) -> None:
        super().__init__()

        self.columns:List[SubstituteUnit] = [column for column in columns]

        self.initial_decision_queue:List[Tuple] = [None] * beam_width

        self.exchange_word_indexs:List[int] = [None] * column_size
        self.exchange_max_decision_queue:List[Tuple] = [None] * beam_width


# 确定领域最佳决策后，得到的各种信息存放于此
class DecisionInfo(BaseEntity):

    def __init__(self) -> None:
        super().__init__()
        self.candidiate_sample:str = None
        self.probs:List[float] = None
        self.prob_label:int = None
        self.word_indexs = None



