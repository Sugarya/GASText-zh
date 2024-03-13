from enum import Enum
from .base_entity import BaseEntity 

'''
    文本自定义的Token实体类
'''
class TokenUnit(BaseEntity):

    def __init__(self, pos_in_text, origin_token, origin_pos, style) -> None:
        self.__common_init(pos_in_text, origin_token, origin_pos, style)
        self.substitute_unit: SubstituteUnit = SubstituteUnit(pos_in_text, origin_token, origin_pos)

    def initial(self, pos_in_text, origin_token, origin_pos, style):
        self.__common_init(pos_in_text, origin_token, origin_pos, style)
        # 语义单元
        self.substitute_unit.initial()

    def __common_init(self, pos_in_text, origin_token, origin_pos, style):
        self.pos_in_text = pos_in_text
        # 数据集文件里的文本的token
        self.origin_token = origin_token
        self.origin_pos = origin_pos
        # TokenUnit实例的类型
        self.style = style

        

'''
    语义单元实体类
'''
class SubstituteUnit((BaseEntity)):

    def __init__(self, pos_in_text: int, origin_word: str, origin_pos) -> None:
        self.__common_init(pos_in_text, origin_word, origin_pos)
        self.state = SubstituteState.WORD_INITIAL
        # 同义候选词集
        self.candicates = []

    def initial(self, pos_in_text: int, origin_word: str, origin_pos):
        self.__common_init(pos_in_text, origin_word, origin_pos)
        self.state = None
        self.candicates.clear()

    def __common_init(self, pos_in_text: int, origin_word: str, origin_pos):
        self.pos_in_text = pos_in_text
        self.origin_word = origin_word
        self.origin_pos = origin_pos

        # 脆弱值
        self.fragile_score = None

        # 替换前初始的概率值
        self.exchange_inital_probability = None
        # 替换过程，记录下当前最大的概率值
        self.exchange_max_probability = None
        # 替换过程，产生的当前替代词
        self.exchange_word = None
        # 替换过程，产生的最大概率值对应的替代词
        self.candidate_max_word = None
       

'''
    TokenUnit的类型
'''
class TokenStyle(Enum):
    # 文本中不被替代的词语
    SILENCE = 1
    # 文本中，用来替代的
    WORD_SUBSTITUTE = 2

class SubstituteState(Enum):
    WORD_INITIAL = 1

    # 文本中已经被替代的
    WORD_REPLACED = 2

    # 文本中正在被替代的
    WORD_REPLACING = 3