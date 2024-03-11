from transformers import AutoTokenizer, AutoModelForSequenceClassification

from victim_model import HuggingFaceWrapper
from common import parse_arguments, AdvText
from config import DEVICES, MAPPING
from dataset import load_data
from common import tools


if __name__ == '__main__':
    args = parse_arguments()

    # 初始化 被攻击的模型
    victim_path = MAPPING[args.style].victim
    classifier = AutoModelForSequenceClassification.from_pretrained(victim_path).to(DEVICES[1])
    tokenizer = AutoTokenizer.from_pretrained(victim_path, use_fast = True)
    victim_model = HuggingFaceWrapper(classifier, tokenizer)

    args_style = args.style
    origin_examples = load_data(args_style)
    for index, example in enumerate(origin_examples):
        label, text = tools.filter_example(example, args_style)
        probs, prob_label = victim_model.output_probability(text)
        if label != prob_label: 
            tools.show_log(f'skip example of {label}:{text}')
            continue

        adv_text = AdvText(label, text, probs)
        # tools.show_log(f'{adv_text}')


