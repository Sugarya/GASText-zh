from enum import Enum
from .base_entity import BaseEntity 

'''
    文本自定义的Token实体类
'''
class TokenUnit(BaseEntity):

    def __init__(self, pos_in_text, origin_token, style) -> None:
        self.__common_init(pos_in_text, origin_token, style)
        self.substitute_unit = SubstituteUnit(pos_in_text)

    def initial(self, pos_in_text, origin_token, style):
        self.__common_init(pos_in_text, origin_token, style)
        # 语义单元
        self.substitute_unit.initial()

    def __common_init(self, pos_in_text, origin_token, style):
        self.pos_in_text = pos_in_text
        # 数据集文件里的文本的token
        self.origin_token = origin_token
        # TokenUnit实例的类型
        self.style = style
        
        # 当前的token，用来恢复文本的
        self.token = origin_token
        # 若该单元处在替换中，候选同义词语赋值而来，用于恢复文本
        self.exchange_token = origin_token

'''
    语义单元实体类
'''
class SubstituteUnit((BaseEntity)):

    def __init__(self, pos_in_text) -> None:
        self.__common_init(pos_in_text)
        # 同义候选词集
        self.candicates = []

    def initial(self, pos_in_text):
        self.__common_init(pos_in_text)
        self.candicates.clear()

    def __common_init(self, pos_in_text):
        self.pos_in_text = pos_in_text
        self.fragile_score = None
        # 替换前初始值
        self.exchange_inital_score = None
        # 替换中产生的当前最大脆弱值
        self.exchange_max_score = None
        # 替换中产生的最大脆弱值对应的替代词
        self.candidate_replaced_word = None

'''
    TokenUnit的类型
'''
class TokenStyle(Enum):
    # 文本中不被替代的词语
    SILENCE = 1
    # 文本中，用来替代的
    WORD_SYNONYM = 2
    # 文本中已经被替代的
    WORD_SYNONYM_REPLACED = 3
    # 文本中正在被替代的
    WORD_SYNONYM_REPLACING = 4