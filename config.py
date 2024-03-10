import torch

DEVICES = [f'cuda:{i}' for i in range(torch.cuda.device_count())]
if len(DEVICES) == 0:
    DEVICES = ['cpu'] * 2
elif len(DEVICES) == 1:
    DEVICES = DEVICES * 2


DATASETS = {
    'chinanews': 'partly_chinanews.csv',
    'shopping': 'partly_shopping_cats.csv',
}


VICTIMS = {
    'bert-base-chinese': 'Raychanan/bert-base-chinese-FineTuned-Binary-Best',
}