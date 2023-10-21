# TODO: INDIVIDUALS (OTHER BRANCH)

import csv

import seaborn as sns
import pandas as pd
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *

def read_df_from_input(file_path: str, limit: int = 1000, by_gen: bool = True) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match file_path:
        case ext if ext.endswith((".txt", ".csv")):
            if by_gen:
                result_df = read_from_csv_by_gen(file_path)
            else:
                result_df = read_from_csv(file_path)
        case ext if ext.endswith(".xlsx"):
            if by_gen:
                result_df = read_from_xlsx_by_gen(file_path)
            else:
                result_df = read_from_xlsx(file_path)
        case ext if ext.endswith(".json"):
            if by_gen:
                result_df = read_from_json_by_gen(file_path)
            else:
                result_df = read_from_json(file_path)
        case _:
            raise Exception("The program does not support to import files from selected format.")
        
    return result_df

def read_from_csv_by_gen(file_path: str, ADJUSTABLE_CHUNK_SIZE: int = 1000) -> GeneratorType:
    for chunk in pd.read_csv(file_path, chunksize=ADJUSTABLE_CHUNK_SIZE):
        yield chunk

def read_from_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def read_from_xlsx_by_gen(file_path: str, ADJUSTABLE_CHUNK_SIZE: int = 1000) -> GeneratorType:
    for chunk in pd.read_excel(file_path, chunksize=ADJUSTABLE_CHUNK_SIZE):
        yield chunk

def read_from_xlsx(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def read_from_json_by_gen(file_path: str, ADJUSTABLE_CHUNK_SIZE: int = 1000) -> GeneratorType:
    for chunk in pd.read_json(file_path, chunksize=ADJUSTABLE_CHUNK_SIZE):
        yield chunk

def read_from_json(file_path: str):
    return pd.read_json(file_path)
