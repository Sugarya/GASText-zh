import torch
from enum import Enum

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2

class AlgoType(Enum):
    CWordAttacker = 1
    SWordFooler = 2
    SWordMasked = 3

class ArgStyle:
    NAME = '--style'
    KEY_Shopping = 'bert-shopping'
    KEY_Chinanews = 'roberta-chinanews'

    Default = KEY_Chinanews

    DatasetFile = {
        KEY_Shopping:'partly_online_shopping_cats.csv',
        KEY_Chinanews:'partly_chinanews.csv',
    }

    Victim_Model = {
        KEY_Shopping:'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
        KEY_Chinanews:'uer/roberta-base-finetuned-chinanews-chinese'
    }

class ArgSpliter:
    NAME = '--split'
    KEY_LTP = 'ltp'
    KEY_JIEBA = 'jieba'

    Default = KEY_LTP

'''
运行模式
'''
class Pattern:
    Algorithm = AlgoType.SWordFooler
    IsTargetAttack = False
    Target_Label = None

    IsDebug = True #是否调试
    Masked_Bert = 'google-bert/bert-base-chinese'
    SentenceSimilarityModel = 'shibing624/text2vec-base-chinese-sentence'
    # 句子相似性
    SENTENCE_SIMILARITY_THRESHOLD = 0.80
    # CWordAttacker算法扰动比例上限
    CWordAttacker_Perturbation_Threshold = 0.2


