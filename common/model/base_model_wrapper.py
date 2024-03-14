import numpy as np
from abc import ABC

class BaseModel(ABC):

    def __init__(self) -> None:
        super().__init__()
        self.__query_times:int = 0



    def plus_one_query_time(self):
        self.__query_times = self.__query_times + 1

    def get_query_times(self) -> int:
        return self.__query_times

    def initial_query_time(self):
        self.__query_times = 0
