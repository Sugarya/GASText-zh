import torch
from enum import Enum

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2


class MappingConstant:
    def __init__(self, dataset, victim):
        self.dataset = dataset
        self.victim = victim

class KEY:
    Shopping = 'bert-shopping'
    Chinanews = 'roberta-chinanews'
    Masked_Bert = 'bert'
    SentenceSimilarity = 'text2vec'

MAPPING = {
    KEY.Shopping: MappingConstant('partly_online_shopping_cats.csv','Raychanan/bert-base-chinese-FineTuned-Binary-Best'),
    KEY.Chinanews: MappingConstant('partly_chinanews.csv', 'uer/roberta-base-finetuned-chinanews-chinese'),
}

MODEL_POOL = {
    KEY.Masked_Bert: 'google-bert/bert-base-chinese',
    KEY.SentenceSimilarity: 'shibing624/text2vec-base-chinese-sentence'
}

class AlgoType(Enum):

    CWordAttacker = 1

    SWordFooler = 2

    SWordMasked = 3

'''
运行模式
'''
class Pattern:
    IsDebug = True #是否调试

    Algorithm = AlgoType.SWordFooler

    # 句子相似性
    SENTENCE_SIMILARITY_THRESHOLD = 0.80


