import torch

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2


class ConfigConstant:
    def __init__(self, dataset, victim):
        self.dataset = dataset
        self.victim = victim

class KEY:
    Shopping = 'bert-shopping'
    Chinanews = 'roberta-chinanews'
    Bert = 'bert'

MAPPING = {
    KEY.Shopping: ConfigConstant('partly_online_shopping_cats.csv','Raychanan/bert-base-chinese-FineTuned-Binary-Best'),
    KEY.Chinanews: ConfigConstant('partly_chinanews.csv', 'uer/roberta-base-finetuned-chinanews-chinese'),
}

MASK_MODEL = {
    KEY.Bert: 'google-bert/bert-base-chinese'
}


'''
运行模式
'''
class Pattern:
    isDebug = True #是否调试

