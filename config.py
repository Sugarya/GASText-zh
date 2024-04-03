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
    MaskedAreaFooler = 3

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

    Dataset_File_Name = {
        BERT_Shopping:'partly_online_shopping_cats',
        RoBERTa_Chinanews:'partly_chinanews',
        DEBUG_BERT_Shopping:'debug_online_shopping_cats',
        DEBUG_RoBERTa_Chinanews:'debug_chinanews'
    }
    Victim_Model = {
        BERT_Shopping:'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
        RoBERTa_Chinanews:'uer/roberta-base-finetuned-chinanews-chinese',
        DEBUG_BERT_Shopping:'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
        DEBUG_RoBERTa_Chinanews:'uer/roberta-base-finetuned-chinanews-chinese',
    }

class ArgAlgorithm:
    NAME = '--algo'
    CWordAttacker = 'CWordAttacker'
    SWordFooler = 'SWordFooler'
    MaskedAreaFooler = 'MaskedAreaFooler'

    Default = MaskedAreaFooler


class ArgLabel:
    NAME = '--label'

    Default = None

class ArgAblation:
    NAME = '--ablation'

    Fragile_DS = 1 # 脆弱值计算
    Deletion = 2 # 消去删除扰动
    Substitute_Via_Others = 3 # 替换动作

    Default = None

class ArgPostfix:
    NAME = '--postfix'

    Long = 'long'
    Short = 'short'
    Target = 'target'

    Default = None

class ArgSubstituteSize:
    NAME = '--subsize'

    Default = None

class ArgSpaceSize:
    NAME = '--spacesize'

    Default = None



'''
运行模式和元信息
'''
class Pattern:
    Algorithm:AlgoType = None
    IsTargetAttack = False
    Target_Label:int = None

    Ablation_Type:int = None
    Substitute_Volume:int = 18
    Postfix:str = None

    IsDebug = True #是否调试
    Masked_Bert = 'google-bert/bert-base-chinese'
    SentenceSimilarityModel = 'shibing624/text2vec-base-chinese-sentence'
    # CWordAttacker算法扰动比例上限
    CWordAttacker_Perturbation_Threshold = 0.2
    
    # 句子相似性
    Sentence_Similarity_Threshold = 0.95
    # 同义词和原始词的相似性上限
    Word_Similarity_Threshold  = 0.815
    
    # 领域大小
    Space_Column_Size = 2
   
    


