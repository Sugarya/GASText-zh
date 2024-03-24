from enum import Enum
import torch
from ltp import LTP
import jieba
import jieba.posseg as pseg
from common import tools, AdvText, TokenUnit, TokenStyle, SubstituteUnit
from typing import List
from config import SeparatorType


'''
    中文划分器
'''
class Separator:

    def __init__(self, separator_type: SeparatorType) -> None:
        self.__type = separator_type
        if separator_type == SeparatorType.LTP:
            self.__initial_ltp()

        self.POS_FILTER_BABELNET = set(['a', 'v', 'd', 'n', 'nd', 'nh','ni','nl','ns','nt'])
        self.POS_LTP_FILTER = ('a', 'v', 'd', 'n')
        

    def __initial_ltp(self):
        self.__ltp = LTP("LTP/small") 
        # 将模型移动到 GPU 上
        if torch.cuda.is_available():
            self.__ltp.to("cuda")
    

    def split(self, adv_text: AdvText) -> List[SubstituteUnit]:
        if self.__type == SeparatorType.LTP:
            tools.show_log(f'self.__type={self.__type}, split_by_ltp')
            return self.__split_by_ltp_for_babelnet(adv_text)
        else:
            tools.show_log(f'self.__type={self.__type}, split_by_jieba')
            return self.__split_by_jieba(adv_text)

    '''
        对文本分词，生成替代单元列表

        "他叫汤姆去拿外衣。"，["cws", "pos", "ner"]分词后所得：
        cws=['他', '叫', '汤姆', '去', '拿', '外衣', '。'], 
        pos=['r', 'v', 'nh', 'v', 'v', 'n', 'wp'], 
        ner=[('Nh', '汤姆')]
    '''
    def __split_by_ltp(self, adv_text: AdvText) -> List[SubstituteUnit]:
        substitute_units: List[SubstituteUnit] = []
        output = self.__ltp.pipeline(adv_text.origin_text, tasks=["cws", "pos", "ner"])
        adv_text.token_count = len(output.cws)
        adv_text.token_units = [TokenUnit] * adv_text.token_count

        for index, token in enumerate(output.cws):
            pos = output.pos[index]
            # 生成待替换的原始词序列，即语义词序列
            if pos in self.POS_LTP_FILTER and len(token) >= 2:
                cur_token_unit = TokenUnit(index, token, pos, TokenStyle.WORD_SUBSTITUTE)
                adv_text.token_units[index] = cur_token_unit
                substitute_units.append(cur_token_unit.substitute_unit)
            else:
                adv_text.token_units[index] = TokenUnit(index, token, pos, TokenStyle.SILENCE)
        return substitute_units

    '''
       分词，babelnet支持的POS
    '''
    def __split_by_ltp_for_babelnet(self, adv_text: AdvText) -> List[SubstituteUnit]:
        substitute_units: List[SubstituteUnit] = []
        output = self.__ltp.pipeline(adv_text.origin_text, tasks=["cws", "pos", "ner"])
        adv_text.token_count = len(output.cws)
        adv_text.token_units = [TokenUnit] * adv_text.token_count

        for index, token in enumerate(output.cws):
            pos = output.pos[index]
            # 生成待替换的原始词序列，即语义词序列
            if pos in self.POS_FILTER_BABELNET and len(token) >= 2:
                cur_token_unit = TokenUnit(index, token, pos, TokenStyle.WORD_SUBSTITUTE)
                adv_text.token_units[index] = cur_token_unit
                substitute_units.append(cur_token_unit.substitute_unit)
            else:
                adv_text.token_units[index] = TokenUnit(index, token, pos, TokenStyle.SILENCE)
        return substitute_units


    # 对文本分词，生成替代单元列表
    def __split_by_jieba(self, adv_text: AdvText) -> List[SubstituteUnit]:
        substitute_units: List[SubstituteUnit] = []
        adv_text.token_units = []
        # 精确分词
        seg_list = pseg.cut(adv_text.origin_text) #jieba 默认精确模式        
        count = 0
        for index, (token, pos) in enumerate(seg_list):
            count = count + 1
            tools.show_log(f'split_by_jieba |{token},{pos}')
            if pos in self.POS_LTP_FILTER:
                cur_token_unit = TokenUnit(index, token, pos, TokenStyle.WORD_SUBSTITUTE)
                adv_text.token_units.append(cur_token_unit) 
                substitute_units.append(cur_token_unit.substitute_unit)
            else:
                adv_text.token_units.append(TokenUnit(index, token, pos, TokenStyle.SILENCE)) 
        adv_text.token_count = count
        return substitute_units