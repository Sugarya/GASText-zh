import torch

'''
运行模式
'''
class Pattern:
    isDebug = True #是否调试

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2


DATASETS = {
    'shopping': 'partly_online_shopping_cats.csv',
    'chinanews': 'partly_chinanews.csv',
}


VICTIMS = {
    'bert-base-chinese': 'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
}