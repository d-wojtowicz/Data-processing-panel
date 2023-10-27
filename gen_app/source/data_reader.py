import sys, os

import pandas as pd
from typing import Union
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variables.enumerators import *
from variables.lists import *
from source.df_seaborn_reader import DataSeabornReader
from source.df_sklearn_reader import DataSklearnReader
from source.df_individual_reader import DataIndividualReader
 
class DataReader(object):
    def __init__(self, df_name: str, df_source: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True, dataset_for_generated: Union[pd.DataFrame, GeneratorType] = None):
        """ 'by_gen' parameter concerns only to the 'row_reader' & 'tuple_reader' & 'chunk_reader"""
        self.dataset: Union[pd.DataFrame, GeneratorType] = dataset_for_generated

        self.df_name: str = df_name.lower()
        self.df_source: str = df_source.lower()

        self.location_method: Enum = location_method
        self.structure_method: Enum = structure_method
        self.limit: int = limit
        self.by_gen: bool = by_gen

    def read_data(self) -> Union[pd.DataFrame, GeneratorType]:
        result = pd.DataFrame()
        try:
            if self.df_source in ["seaborn"]:
                if self.df_name in seaborn_libraries:
                    DataReaderMethod = DataSeabornReader(self.df_name, self.location_method, self.structure_method, self.limit, self.by_gen)
                    DataReaderMethod.read_df_from_seaborn()
                    self.dataset = DataReaderMethod.dataset
                    result = DataReaderMethod.dataset
            elif self.df_source in ["sklearn"]:
                if self.df_name in sklearn_libraries:
                    DataReaderMethod = DataSklearnReader(self.df_name, self.location_method, self.structure_method, self.limit, self.by_gen)
                    DataReaderMethod.read_df_from_sklearn()
                    self.dataset = DataReaderMethod.dataset
                    result = DataReaderMethod.dataset
            elif self.df_source.endswith((".txt", ".csv", ".xlsx", ".json")) or self.df_source in ["generated"]:
                DataReaderMethod = DataIndividualReader(self.df_source, self.location_method, by_gen=self.by_gen, dataset_input=self.dataset) # Full data are readed
                DataReaderMethod.read_df_from_input()
                self.dataset = DataReaderMethod.dataset
                result = DataReaderMethod.dataset
        except:
            raise Exception("The dataset could NOT be readed!")

        return result