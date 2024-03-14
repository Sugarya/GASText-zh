from typing import List
import numpy as np
import torch
from common import tools
from .base_model_wrapper import *


class HuggingFaceWrapper(BaseModel):

    def __init__(self, model, tokenizer):
        super(HuggingFaceWrapper, self).__init__()

        self._model = model
        self._tokenizer = tokenizer

        self.unk_token = self._tokenizer.unk_token
        self.sep_token = self._tokenizer.sep_token

    '''
        转为概率值
    '''
    def __softmax(self, x):
        exp_x = np.exp(x)
        return exp_x / np.sum(exp_x)

    def __output_logits(self, text_list):
        text = []
        if isinstance(text_list, str):
            text.append(text_list)
        elif isinstance(text_list, list):
            text = [*text_list]
        else:
            text = text_list
        # tools.show_log(f"HuggingFaceWrapper text = {text}")

        inputs = self._tokenizer(
            text_list,
            padding = True,
            truncation = True,
            return_tensors = 'pt',
        )
        inputs.to(next(self._model.parameters()).device)

        with torch.no_grad():    
            outputs = self._model(**inputs)
        logits =  np.concatenate(outputs.logits.cpu().numpy(), axis = 0)
        self.plus_one_query_time()
        # tools.show_log(f'HuggingFaceWrapper logits = {logits}')
        return logits

    def output_probs(self, texts) -> List[str]:
        probs = self.__softmax(self.__output_logits(texts))
        # tools.show_log(f'HuggingFaceWrapper probs = {probs}')
        return probs

