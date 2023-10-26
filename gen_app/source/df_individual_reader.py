import pandas as pd
from typing import Union
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *

class DataIndividualReader(object):
    def __init__(self, file_path: str, location_method: Enum = read_from.TOP, by_gen: bool = True):
        self.dataset: Union[pd.DataFrame, GeneratorType] = None

        self.file_path: str = file_path

        self.location_method: Enum = location_method
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
                if self.by_gen:
                    self.dataset = self.read_from_xlsx_by_gen()
                else:
                    self.dataset = self.read_from_xlsx()
            case ext if ext.endswith(".json"):
                if self.by_gen:
                    self.dataset = self.read_from_json_by_gen()
                else:
                    self.dataset = self.read_from_json()
            case _:
                raise Exception("The program does not support to import files from selected format.")

    def read_from_csv_by_gen(self) -> GeneratorType:
        for chunk in pd.read_csv(self.file_path, chunksize=self.ADJUSTABLE_CHUNK_SIZE):
            yield chunk

    def read_from_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

    def read_from_xlsx_by_gen(self) -> GeneratorType:
        for chunk in pd.read_excel(self.file_path, chunksize=self.ADJUSTABLE_CHUNK_SIZE):
            yield chunk

    def read_from_xlsx(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)

    def read_from_json_by_gen(self) -> GeneratorType:
        for chunk in pd.read_json(self.file_path, chunksize=self.ADJUSTABLE_CHUNK_SIZE):
            yield chunk

    def read_from_json(self) -> pd.DataFrame:
        return pd.read_json(self.file_path)
