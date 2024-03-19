
from typing import List
from common import SubstituteUnit, AdvText, tools, SubstituteState, AdversaryInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, AlgoType
from .cwordattacker_search import WordAttackerGreedy
from .swordfooler_search import WordFoolerGreedy

class Searcher:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        if Pattern.Algorithm == AlgoType.CWordAttacker:
            self.__greedy = WordAttackerGreedy(validator, substituter)
        elif Pattern.Algorithm == AlgoType.SWordFooler:
            self.__greedy = WordFoolerGreedy(validator, substituter)
        else:
            self.__greedy = WordFoolerGreedy(validator, substituter)
        
    
    def perform(self, substitute_units: List[SubstituteUnit], adv_text: AdvText) -> bool:
        return self.__greedy.search(substitute_units, adv_text)