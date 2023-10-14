# TODO: INDIVIDUALS (OTHER BRANCH)

import csv

import seaborn as sns
import pandas as pd
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *

def read_from_csv(file_name: str, number_of_rows: int) -> pd.DataFrame:
    for chunk in pd.read_csv(file_name, chunksize=number_of_rows):
        yield chunk