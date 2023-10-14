import seaborn as sns
import pandas as pd

from utils.data_stats_calculator import *
from utils.data_exporter import *
from utils.pandas_extension import *

from source.data_reader import *


if __name__ == "__main__":

    # Testing performance on the example of 'diamonds' seaborn dataframe set:
    full_measure_with_seaborn = calc.fullMeasure(read_df_from_seaborn)
    size_measure_of_generator = calc.sizeMeasure(df_to_gen)

    #column_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.COLUMNS, 100)
    #row_method_as_df1 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.ROWS, 100, by_gen=True) 
    #row_method_as_df2 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.ROWS, 100, by_gen=False) # PerformanceWarning
    #tuple_method_as_df1 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.TUPLES, 100, by_gen=True)
    #tuple_method_as_df2 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.TUPLES, 100, by_gen=False)
    #normal_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.NORMAL, 100)
    chunk_method_as_df1 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.CHUNKS, 100, by_gen=True)
    chunk_method_as_df2 = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.CHUNKS, 100, by_gen=False)

    #column_method_as_gen = size_measure_of_generator(column_method_as_df)
    #row_method_as_gen = size_measure_of_generator(row_method_as_df2)
    #tuple_method_as_gen = size_measure_of_generator(tuple_method_as_df2)
    #normal_method_as_gen = size_measure_of_generator(normal_method_as_df)
    #chunk_method_as_gen = size_measure_of_generator(chunk_method_as_df2)

    #export_to_txt(column_method_as_df, "Column_DataFrame")
    #export_to_txt(row_method_as_df1, "Row_DataFrame_Gen")
    #export_to_txt(row_method_as_df2, "Row_DataFrame")
    #export_to_txt(tuple_method_as_df1, "Tuple_DataFrame_Gen")
    #export_to_txt(tuple_method_as_df2, "Tuple_DataFrame")
    #export_to_txt(normal_method_as_df, "Normal_DataFrame")
    #export_to_txt(chunk_method_as_df1, "Chunk_DataFrame_Gen") 
    #export_to_txt(chunk_method_as_df2, "Chunk_DataFrame") 


    # TODO: 1. SEABORN - df_seaborn_reader.py
    # TODO: 1.1. WRITE CHUNK_READER & CHUNK_READER_BY_GEN (IN SEABORN)
    # TODO: 1.2. TEST PRINT OF ALL GENERATED DATAFRAMES WITH USE OF OBJECT
    # TODO: 1.3. TEST PRINT OF ALL GENERATED DATAFRAMES WITH USE OF GENERATORS
    # TODO: 1.4. TEST DF_TO_GEN, GEN_TO_DF FUNCTIONS WITH IT
    # TODO: 1.5. TEST DATA_EXPORTER AND REPAIR ALL EXPORTS FROM ALL DATAFRAMES (FROM OBJECTS EITHER FROM GENERATORS)

    # TODO: 2. SKLEAERN - df_sklearn_reader.py
    # TODO: 2.1. Apply seaborn changes to refactor & update functionalities by df generating from gen

    # TODO: 3. INDIVIDUAL - df_individual_reader.py
    # TODO: 3.1. WRITE ALL IMPORTANT FILE TYPE IMPORTS (CSV, XLSX, TXT etc.)

    # TODO: 4. TEST PRINTING OF ALL DF FROM OBJ & ALL DF FROM GEN
    # TODO: 5. TEST EXPORT OF ALL DF FROM OBJ & ALL DF FROM GEN