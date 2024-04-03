
from typing import List
from common import SememicUnit, AdvText, tools, SememicState, AdversaryInfo
from validation import Validator
from substitution import Substituter
from config import Pattern, AlgoType
from .wordattacker_search import WordAttackerGreedy
from .wordfooler_search import WordFoolerSearch
from .maskedarea_search import MaskedAreaSearch

class Searcher:

    def __init__(self, validator: Validator, substituter: Substituter) -> None:
        if Pattern.Algorithm == AlgoType.CWordAttacker:
            self.__greedy = WordAttackerGreedy(validator, substituter)
        elif Pattern.Algorithm == AlgoType.SWordFooler:
            self.__greedy = WordFoolerSearch(validator, substituter)
        else:
            self.__greedy = MaskedAreaSearch(validator, substituter)
        
    
    def perform(self, substitute_units: List[SememicUnit], adv_text: AdvText):
        self.__greedy.search(substitute_units, adv_text)