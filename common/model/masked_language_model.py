from transformers import AutoTokenizer, AutoModelForMaskedLM, pipeline
from config import Pattern, DEVICES
from typing import List

class BertMaskedModelWrapper:

    MASK_TOKEN = '[MASK]'

    def __init__(self) -> None:
        model_name = Pattern.Masked_Bert # "bert-base-chinese"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForMaskedLM.from_pretrained(model_name).to(DEVICES[1])
        self.__unmasker = pipeline('fill-mask', model=model, tokenizer=tokenizer) 
        
    '''
        mask_text：替换成mask格式后的文本
    '''
    def output(self, masked_text:str) -> List[str]:
        output = self.__unmasker(masked_text)
        candicate_list = list(map(lambda e : e['token_str'], output))
        return candicate_list


