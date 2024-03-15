from typing import List

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from common import parse_arguments, AdvText, tools, SubstituteUnit, HuggingFaceWrapper
from config import DEVICES, MAPPING, Pattern
from dataset import load_data
from segmentation import Separator, SeparatorType
from validation import Validator
from perturbation_search import Greedy
from substitution import Substituter


if __name__ == '__main__':
    args = parse_arguments()

    # 初始化 被攻击的模型
    victim_path = MAPPING[args.style].victim
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
    separator = Separator(SeparatorType.LTP)
    

    args_style = args.style
    origin_examples = load_data(args_style)
    for index, example in enumerate(origin_examples):
        tools.show_log(f'origin_examples: {index} Round')
        label, text = tools.filter_example(example, args_style)
        adv_text = validator.generate_example_wrapper(label, text)
        if not adv_text:
            tools.show_log(f'origin_examples: {index} Round, continue')
            tools.show_log(f'             ----------------------------------------------------')
            continue
        
        # 分词
        substitute_units: List[SubstituteUnit] = separator.splitByLTP(adv_text)
        # 扰动贪心查找
        success = greedy.search(substitute_units, adv_text)
        # 计算评价指标
        tools.show_log(f'             -----------------------------------------------------')
        tools.show_log(f'adversary_info = {adv_text.adversary_info}')
        tools.show_log(f'------------------------------------------------------------------------------------')