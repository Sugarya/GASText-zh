import os
import csv
from config import ArgStyle, Pattern
from common import tools

class DataLoader():

    def generate_examples(self, style_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_file_name = f'{ArgStyle.Dataset_File_Name[style_name]}'
        if Pattern.Postfix:
            data_file_name = f'{data_file_name}{Pattern.Postfix}'
        file_path = f'{current_dir}/src/{data_file_name}.csv'
        tools.show_log(f'Postfix = {Pattern.Postfix} | file_path = {file_path}')

        if ArgStyle.Shopping in style_name:
            examples = self.__read_corpus_of_online_shopping(file_path)
        elif ArgStyle.Chinanews in style_name:
            examples = self.__read_corpus_of_chinanews(file_path)
        else:
            examples = self.__read_corpus(file_path)
        return examples # 返回列表[]

    '''
        读取数据文件
        @path: 文件路径
        @return：列表
    '''
    def __read_corpus_of_online_shopping(self, path):
        with open(path, encoding='utf-8') as f:
            examples = list(csv.reader(f, delimiter = ',', quotechar = None))[1:]
            for i in range(len(examples)):
                examples[i] = examples[i][1:]
        return examples

    def __read_corpus_of_chinanews(self, path):
        with open(path, encoding='utf-8') as f:
            examples = list(csv.reader(f, delimiter = ',', quotechar = '"'))[1:]
        return examples

    def __read_corpus(self, path):
        with open(path, encoding='utf-8') as f:
            examples = list(csv.reader(f, delimiter = ',', quotechar = None))[1:]
            for i in range(len(examples)):
                examples[i][0] = int(examples[i][0])
                if len(examples[i]) == 2:
                    examples[i].append(None)
        return examples
