
import csv
from config import DATASETS
from common import show_log


def load_data(dataset_name):
    file_path = "./dataset/src/%s" % DATASETS[dataset_name]
    show_log('file_path = {}'.format(file_path))

    if dataset_name == "shopping":
        examples = __read_corpus_of_online_shopping(file_path)
    elif dataset_name == "chinanews":
        examples = __read_corpus_of_chinanews(file_path)
    else:
        examples = __read_corpus(file_path)
    return examples # 返回列表[]

'''
    读取数据文件
    @path: 文件路径
    @return：列表
'''
def __read_corpus_of_online_shopping(path):
    with open(path, encoding='utf8') as f:
        examples = list(csv.reader(f, delimiter = ',', quotechar = None))[1:]
        for i in range(len(examples)):
            examples[i] = examples[i][1:]
    return examples

def __read_corpus_of_chinanews(path):
    with open(path, encoding='utf8') as f:
        examples = list(csv.reader(f, delimiter = ',', quotechar = '"'))[1:]
    return examples

def __read_corpus(path):
    with open(path, encoding='utf8') as f:
        examples = list(csv.reader(f, delimiter = ',', quotechar = None))[1:]
        for i in range(len(examples)):
            examples[i][0] = int(examples[i][0])
            if len(examples[i]) == 2:
                examples[i].append(None)
    return examples
