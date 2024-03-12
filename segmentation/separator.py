import torch
from ltp import LTP
import jieba
import jieba.posseg as pseg
import jieba.analyse
from common import tools, AdvText
from enum import Enum


class SeparatorType(Enum):
    LTP = 1 #使用ltp分词库
    JIE_BA = 2 #使用jieba分词库
    ALL = 3 #都使用

'''
    中文划分器
'''
class Separator:

    def __init__(self, type: SeparatorType) -> None:
        if type == SeparatorType.LTP:
            self.__initial_ltp()
        elif type == SeparatorType.JIE_BA:
            self.__initial_jieba()
        else:
            self.__initial_ltp()
            self.__initial_jieba()
        

    def __initial_ltp(self):
        self.ltp = LTP("LTP/small") 
        # 将模型移动到 GPU 上
        if torch.cuda.is_available():
            self.ltp.to("cuda")
    
    def __initial_jieba(self):

        pass

    '''
        "他叫汤姆去拿外衣。"，["cws", "pos", "ner"]分词后所得：
        cws=['他', '叫', '汤姆', '去', '拿', '外衣', '。'], 
        pos=['r', 'v', 'nh', 'v', 'v', 'n', 'wp'], 
        ner=[('Nh', '汤姆')]
    '''
    def splitByLTP(self, adv_text: AdvText):
        text_line = adv_text.origin_text
        output = self.ltp.pipeline(text_line, tasks=["cws", "pos", "ner"])
        for index, token in enumerate(output.cws):
            tools.show_log(f'{index}; {token} {output.pos[index]}')
            


    def splitByJieba(self, adv_text: AdvText):
        # seg_list = jieba.analyse.textrank(adv_text.origin_text, topK=8, withWeight=True, allowPOS=('a', 'n', 'vn', 'v','ad','vd','d'))
        # for seg in seg_list:
        #     tools.show_log(f'{seg}  {len(seg)}')

        # for seg in jieba.analyse.extract_tags(adv_text.origin_text, topK=8, withWeight=True, allowPOS=('a', 'n', 'vn', 'v','ad','vd','d')):
        #     tools.show_log(f'{seg}  {len(seg)}')
        
        seg_list = pseg.cut(adv_text.origin_text) #jieba 默认精确模式
        for index, (token, pos) in enumerate(seg_list):
            tools.show_log(f'{index}; {token}  {pos}')


        