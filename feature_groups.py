from abc import ABC,abstractmethod
from pandas import DataFrame
from .data import ShortAnswerInstance
from typing import List

class FeatureGroupExtractor(ABC):
    @abstractmethod
    def extract(self, instances: List[ShortAnswerInstance]) -> DataFrame:
        return DataFrame()
