# TODO: Test sklearn processing of dataframe
# Requirements: firstly complete the df_sklearn_reader.py methods

import pandas as pd

from utils.pandas_extension import *
from utils.data_stats_calculator import *
from utils.data_exporter import *

from source.data_reader import *


# Seaborn processing
df_seaborn_reader = DataReader("diamonds", "seaborn", read_from.TOP, read_by.NORMAL, 10)
readed_df = df_seaborn_reader.read_data()

queried_df = get_df_by_query(readed_df, 'depth', 64.5, '>=')
category_queried_df = get_df_by_category(readed_df, 'cut', ['Good', 'Fair'])

print("SEABORN TESTS: ")
print(readed_df)
print("\n")
print(queried_df)
print("\n")
print(category_queried_df)


# Sklearn processing
df_sklearn_reader = DataReader("diabetes", "sklearn", read_from.BOTTOM, read_by.COLUMNS, 40)
readed_df2 = df_sklearn_reader.read_data()

queried_df2 = get_df_by_query(readed_df2, 'sex', 0, '>=')

print("SKLEARN TESTS: ")
print(readed_df2)
print("\n")
print(queried_df2)
