# !TODO: Rewrite all input reads and result returns to operate on the generators from the dataframe rather than the dataframe!!!
# Details: At the most detailed moments, such as reading by columns or chunks or tuples (etc.),
# I should read not from the finished dataframe object but from the object passed through df_to_gen
# (i.e. read from the generator, not the dataframe)

# TODO: Reading datasets individually (e.g. via input files)

import csv

import seaborn as sns
import pandas as pd

from variables.enumerators import *
from variables.lists import *
from source.df_seaborn_reader import read_df_from_seaborn
from source.df_sklearn_reader import read_df_from_sklearn

class DataReader(object):
    def __init__(self, df_name: str, df_source: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000):
        self.df_name = df_name
        self.df_source = df_source

        self.location_method = location_method
        self.structure_method = structure_method
        self.limit = limit

    def read_data(self) -> pd.DataFrame:
        df = pd.DataFrame()

        try:
            if self.df_source in ["sns", "seaborn"]:
                if self.df_name in seaborn_libraries:
                    df = read_df_from_seaborn(self.df_name, self.location_method, self.structure_method, self.limit)
            elif self.df_source in ["sklearn", "scikit-learn"]:
                if self.df_name in sklearn_libraries:
                    df = read_df_from_sklearn(self.df_name, self.location_method, self.structure_method, self.limit)
            elif self.df_source in ["individual"]:
                """ TODO """
        except:
            raise Exception("The dataset could NOT be readed!")

        return df