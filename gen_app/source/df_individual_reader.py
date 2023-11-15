import sys, os

import pandas as pd
from typing import Union
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pandas_extension import gen_to_df
from variables.enumerators import *
from variables.lists import *

class DataIndividualReader(object):
    def __init__(self, file_path: str, by_gen: bool = True, dataset_input: Union[pd.DataFrame, GeneratorType] = None):
        self.dataset: Union[pd.DataFrame, GeneratorType] = dataset_input

        self.file_path: str = file_path

        self.by_gen: bool = by_gen
        self.ADJUSTABLE_CHUNK_SIZE = 1000

    def read_df_from_input(self) -> None:
        match self.file_path:
            case ext if ext.endswith((".txt", ".csv")):
                if self.by_gen:
                    self.dataset = self.read_from_csv_by_gen()
                else:
                    self.dataset = self.read_from_csv()
            case ext if ext.endswith(".xlsx"):
                self.dataset = self.read_from_xlsx()
            case ext if ext.endswith(".json"):
                if self.by_gen:
                    self.dataset = self.read_from_json_by_gen()
                else:
                    self.dataset = self.read_from_json()
            case "generated":
                self.dataset = self.read_from_generated()
            case _:
                raise Exception("The program does not support to import files from selected format.")

    def read_from_csv_by_gen(self) -> GeneratorType:
        for chunk in pd.read_csv(self.file_path, chunksize=self.ADJUSTABLE_CHUNK_SIZE):
            yield chunk

    def read_from_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

    def read_from_xlsx(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)

    def read_from_json_by_gen(self) -> GeneratorType:
        for chunk in pd.read_json(self.file_path, lines=True, chunksize=self.ADJUSTABLE_CHUNK_SIZE):
            yield chunk

    def read_from_json(self) -> pd.DataFrame:
        return pd.read_json(self.file_path, lines=True)

    def read_from_generated(self) -> pd.DataFrame:
        return self.dataset