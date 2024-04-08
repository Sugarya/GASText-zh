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

    Default = DEBUG_BERT_Shopping

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

class ArgPostfix:
    NAME = '--postfix'

    Long = 'long'
    Short = 'short'
    Target = 'target'

    Default = None

class ArgSubstituteAddition:
    NAME = '--subproperty'
    Deletion = 'delete' # 增加删除原始词扰动

    Default = None
class ArgSubstituteSize:
    NAME = '--subsize'

    Default = None

class ArgSubstituteType:
    NAME = '--subtype'

    CWord = 'cword'
    HowNet = 'hownet'
    MLM = 'mlm'
    Hybrid = 'hybrid'


    Default = None


class ArgSpaceSize:
    NAME = '--spacesize'

    Default = None

class ArgSpaceStyle:
    NAME = '--spacestyle'

    Single = 'single'
    Capital = 'capital'
    Alternate = 'alternate'
    Full = 'full'

    Default = None


class ArgFragileMethod:
    NAME = '--fragtype'

    DS = 'ds'
    ADS = 'ads'
    ADAS = 'adas'

    Default = None

class ArgHownetSimThreshold:
    NAME = '--hsimthreshold'

    Default = None

class ArgMaskedSimThreshold:
    NAME = '--msimthreshold'

    Default = None 


'''
运行模式和元信息
'''
class Pattern:

    Algorithm:AlgoType = None
    IsTargetAttack = False
    Target_Label:int = None

    Substitute_Volume:int = 35
    Substitute_Type:str = None
    substitute_addition_property:str = None
    Fragile_Type:str = None

    # 领域宽度
    Space_Width = 2
    # 领域深度
    Space_Depth = Substitute_Volume
    Space_Style:str = None
    
    # Hownet词的相似性下界
    Hownet_Similarity_Threshold  = 0.6
    # MLM词的相似性下界
    Masked_Similarity_Threshold  = 0.2

    Postfix:str = None
   
    IsDebug = True #是否调试
    Masked_Bert = 'google-bert/bert-base-chinese'
    SentenceSimilarityModel = 'shibing624/text2vec-base-chinese-sentence'
    # CWordAttacker算法扰动比例上限
    CWordAttacker_Perturbation_Threshold = 0.2


