import pandas as pd

from utils.pandas_extension import DataManager
from utils.data_stats_calculator import *
from utils.data_exporter import *

from source.data_reader import DataReader
from variables.enumerators import read_from, read_by, reader_tester


if __name__ == "__main__":
    # Select the Reader tester performance (SEABORN | SKLEARN | INDIVIDUAL)
    SELECTED_TESTS = reader_tester.SKLEARN

    match SELECTED_TESTS:
        case reader_tester.SEABORN:
            DataSeabornReader = DataReader("diamonds", "seaborn", read_from.TOP, read_by.NORMAL, 100)
            DataSeabornReader.read_data()
            readed_df = DataSeabornReader.dataset

            DatasetManagerSeaborn = DataManager(readed_df)
            queried_df = DatasetManagerSeaborn.get_df_by_numeric('depth', 64.5, '>=')
            category_queried_df = DatasetManagerSeaborn.get_df_by_category('cut', ['Good', 'Fair'])

            print("SEABORN TESTS: ")
            print(readed_df)
            print("\n")
            print(queried_df)
            print("\n")
            print(category_queried_df)
            
        case reader_tester.SKLEARN:
            DataSklearnReader = DataReader("diabetes", "sklearn", read_from.BOTTOM, read_by.COLUMNS, 40)
            DataSklearnReader.read_data()
            readed_df2 = DataSklearnReader.dataset

            DatasetManagerSklearn = DataManager(readed_df2)
            queried_df2 = DatasetManagerSklearn.get_df_by_numeric('sex', 0, '>=')

            print("SKLEARN TESTS: ")
            print(readed_df2)
            print("\n")
            print(queried_df2)
    
        case reader_tester.INDIVIDUAL:
                """"""

        case _:
            raise Exception("You selected wrong tester enumerator (Variable 'SELECTED_TESTS' at the top of program).")