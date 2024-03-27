import torch
from enum import Enum

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2

class SeparatorType(Enum):
    LTP = 1
    JIE_BA = 2

class AlgoType(Enum):
    CWordAttacker = 1
    SWordFooler = 2
    BeamWordFooler = 3

class ArgStyle:
    NAME = '--style'

    Shopping = 'shopping'
    Chinanews = 'chinanews'
    BERT = 'bert'
    RoBERTa = 'roberta'
    DEBUG = 'debug'

    BERT_Shopping = f'{BERT}-{Shopping}'
    RoBERTa_Chinanews = f'{RoBERTa}-{Chinanews}'
    DEBUG_BERT_Shopping = f'{DEBUG}-{BERT}-{Shopping}'
    DEBUG_RoBERTa_Chinanews = f'{DEBUG}-{RoBERTa}-{Chinanews}'

    Default = DEBUG_RoBERTa_Chinanews

    Dataset_File = {
        BERT_Shopping:'partly_online_shopping_cats.csv',
        RoBERTa_Chinanews:'partly_chinanews3.csv',
        DEBUG_BERT_Shopping:'debug_online_shopping_cats.csv',
        DEBUG_RoBERTa_Chinanews:'debug_chinanews.csv'
    }
    Victim_Model = {
        BERT_Shopping:'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
        RoBERTa_Chinanews:'uer/roberta-base-finetuned-chinanews-chinese',
        DEBUG_BERT_Shopping:'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
        DEBUG_RoBERTa_Chinanews:'uer/roberta-base-finetuned-chinanews-chinese',
    }

class ArgAlgorithm:
    NAME = '--algo'
    KEY_CWordAttacker = 'CWordAttacker'
    KEY_SWordFooler = 'SWordFooler'
    KEY_BeamWordFooler = 'AreaBeamFooler'

    Default = KEY_SWordFooler
    # Default = None

class ArgLabel:
    NAME = '--label'

    Default = None

class ArgAblation:
    NAME = '--ablation'

    Fragile_DS = 1 # 脆弱值计算
    Deletion = 2 # 消去删除扰动
    Maintain = 3 # 保持原始词
    Substitute = 4 # 替换动作

    Default = None


'''
运行模式
'''
class Pattern:
    Algorithm:AlgoType = None
    IsTargetAttack = False
    Target_Label:int = None
    Ablation_Type:int = None

    IsDebug = True #是否调试
    Masked_Bert = 'google-bert/bert-base-chinese'
    SentenceSimilarityModel = 'shibing624/text2vec-base-chinese-sentence'
    # 句子相似性
    Sentence_Similarity_Threshold = 0.95
    # CWordAttacker算法扰动比例上限
    CWordAttacker_Perturbation_Threshold = 0.2
    # 同义词集的数量上限
    # Synonym_Upper_Bound = 8


