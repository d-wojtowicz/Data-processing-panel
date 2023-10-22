import pandas as pd
from typing import Union
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *
from source.df_seaborn_reader import DataSeabornReader
from source.df_sklearn_reader import DataSklearnReader
from source.df_individual_reader import DataIndividualReader
 
class DataReader(object):
    def __init__(self, df_name: str, df_source: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True):
        """ 'by_gen' parameter concerns only to the 'row_reader' & 'tuple_reader' & 'chunk_reader"""
        self.dataset: Union[pd.DataFrame, GeneratorType] = None

        self.df_name: str = df_name
        self.df_source: str = df_source

        self.location_method: Enum = location_method
        self.structure_method: Enum = structure_method
        self.limit: int = limit
        self.by_gen: bool = by_gen

    def read_data(self) -> None:
        try:
            if self.df_source in ["sns", "seaborn"]:
                if self.df_name in seaborn_libraries:
                    self.dataset = DataSeabornReader(self.df_name, self.location_method, self.structure_method, self.limit, self.by_gen).dataset
            elif self.df_source in ["sklearn", "scikit-learn"]:
                if self.df_name in sklearn_libraries:
                    self.dataset = DataSklearnReader(self.df_name, self.location_method, self.structure_method, self.limit, self.by_gen).dataset
            elif self.df_source.endswith((".txt", ".csv", ".xlsx", ".json")):
                self.dataset = DataIndividualReader(self.df_source, self.location_method, by_gen=self.by_gen).dataset # Full data are readed
        except:
            raise Exception("The dataset could NOT be readed!")