
from config import Pattern, ArgStyle, ArgAlgorithm, AlgoType
from common import AdvText, TokenStyle, SubstituteState
from typing import List, Tuple, Union


def show_log(content):
    if Pattern.IsDebug:
        print(content)

'''
    @example：数据集文件的一行内容
    @return：(int , str)
'''
def format_example(example, style) -> Tuple[int, str]:
    label, text = None, None
    if ArgStyle.Chinanews in style:
        label, text = int(example[0]) - 1, f'{example[1]}{example[2]}'
    else:
        label, text = int(example[0]), f'{example[1]}'
    return (label, text)

'''
    生成当前最新的文本
'''
def generate_latest_text(adv_text: AdvText) -> str:
    display_list = [None] * adv_text.token_count
    for index, token_unit in enumerate(adv_text.token_units):                
        if token_unit.style == TokenStyle.WORD_SUBSTITUTE:
            if token_unit.substitute_unit.state == SubstituteState.WORD_REPLACING:
                display_list[index] = token_unit.substitute_unit.exchange_word
            elif token_unit.substitute_unit.state == SubstituteState.WORD_REPLACED:
                display_list[index] = token_unit.substitute_unit.exchange_max_decision_word
            else:
                display_list[index] = token_unit.origin_token 
        else:
            display_list[index] = token_unit.origin_token
    text = ''.join(display_list)
    return text

'''
    生成一个词元变动的文本，比如Masked场景
'''
def generate_text(adv_text: AdvText) -> str:
    display_list = [None] * len(adv_text.token_units)
    for index, token_unit in enumerate(adv_text.token_units):                
        if token_unit.style == TokenStyle.WORD_SUBSTITUTE:
            if token_unit.substitute_unit.state == SubstituteState.WORD_REPLACING:
                display_list[index] = token_unit.substitute_unit.exchange_word
            else:
                display_list[index] = token_unit.origin_token   
        else:
            display_list[index] = token_unit.origin_token
    text = ''.join(display_list)
    return text

'''
    babelnet Can only be set to a(形容词)/v（动词）/n（名词）/r（副词）.
'''
def ltp_to_babelnet_pos(ltp_pos:str) -> Union[str, None]:
    ltp_pos = ltp_pos.lower()
    if ltp_pos.startswith('n') or ltp_pos == 'r':
        return 'n'
    elif ltp_pos == 'v':
        return 'v'
    elif ltp_pos == 'a':
        return 'a'
    elif ltp_pos == 'd':
        return 'r'
    else:
        return None
    


def __to_algorithm_type(type:str) -> AlgoType:
    if type == ArgAlgorithm.KEY_CWordAttacker:
        return AlgoType.CWordAttacker

    elif type == ArgAlgorithm.KEY_SWordFooler:
        return AlgoType.SWordFooler
    
    else:
        return AlgoType.BeamWordFooler

def setup_from_args(args):
    if args.label:
        Pattern.IsTargetAttack = True
        Pattern.Target_Label = args.label
        show_log(f'setup_from_args | IsTargetAttack{Pattern.IsTargetAttack} --> {Pattern.Target_Label}')

    if args.algo:
        Pattern.Algorithm = __to_algorithm_type(args.algo)
        show_log(f'setup_from_args | {Pattern.Algorithm}')


