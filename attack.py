from transformers import AutoTokenizer, AutoModelForSequenceClassification

from victim_model import HuggingFaceWrapper
from common import parse_arguments
from config import *
from dataset import load_data
from common import tools


if __name__ == '__main__':
    args = parse_arguments()
    dataset_name, victim_path = args.dataset, VICTIMS[args.victim]

    # 初始化 被攻击的模型
    classifier = AutoModelForSequenceClassification.from_pretrained(victim_path).to(DEVICES[1])
    tokenizer = AutoTokenizer.from_pretrained(victim_path, use_fast = True)
    victim_model = HuggingFaceWrapper(classifier, tokenizer)

    origin_examples = load_data(dataset_name)
    for index, example in enumerate(origin_examples):
        label, text = tools.filter_example(example)
        probability, prob_label = victim_model.output_probability(text)
        if label != prob_label: continue

        # TODO 
