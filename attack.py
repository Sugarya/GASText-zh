from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from arguement import parse_args
from common import tools, SubstituteUnit, HuggingFaceWrapper
from config import DEVICES, Pattern, ArgStyle, ArgSpliter
from dataset import DataLoader
from segmentation import Separator
from validation import Validator
from perturbation_search import Greedy
from substitution import Substituter
from evaluation import Evaluator



if __name__ == '__main__':
    args = parse_args()

    # 初始化数据集加载器
    data_loader = DataLoader()

    # 初始化 被攻击的模型
    victim_path = ArgStyle.Victim_Model[args.style]
    classifier = AutoModelForSequenceClassification.from_pretrained(victim_path).to(DEVICES[1])
    tokenizer = AutoTokenizer.from_pretrained(victim_path, use_fast = True)
    victim_model = HuggingFaceWrapper(classifier, tokenizer)

    # 初始化检验器
    validator = Validator(victim_model)

    # 初始化替代器
    substituter = Substituter(Pattern.Algorithm)

    # 搜索
    greedy = Greedy(validator, substituter)

    # 初始化分词器
    separator = Separator(args.style)

    # 初始化评价器
    evaluator = Evaluator()

    args_style = args.style
    origin_examples = data_loader.generate_examples(args_style)
    adv_text_list = validator.generate_adv_texts(origin_examples, args_style)
    evaluator.set_origin_example_count(len(adv_text_list))
    for index, adv_text in enumerate(adv_text_list):
        tools.show_log(f'adv_text: {index} Round')
        # 分词
        substitute_units: List[SubstituteUnit] = separator.splitByLTP(adv_text)
        # 扰动贪心查找
        greedy.search(substitute_units, adv_text)
        # 收集评价指标信息
        evaluator.add(adv_text.adversary_info)
        tools.show_log(f'------------------------------------------------------------------------------------')

    # 计算实验指标
    evaluator.compute()