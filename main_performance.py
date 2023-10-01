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

    column_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.COLUMNS, 100)
    row_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.ROWS, 100) # PerformanceWarning
    tuple_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.TUPLES, 100)
    normal_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.NORMAL, 100)
    chunk_method_as_df = full_measure_with_seaborn("diamonds", read_from.TOP, read_by.CHUNKS, 100)

    column_method_as_gen = size_measure_of_generator(column_method_as_df)
    row_method_as_gen = size_measure_of_generator(row_method_as_df)
    tuple_method_as_gen = size_measure_of_generator(tuple_method_as_df)
    normal_method_as_gen = size_measure_of_generator(normal_method_as_df)
    chunk_method_as_gen = size_measure_of_generator(chunk_method_as_df)

    export_to_txt(column_method_as_df, "Column_DataFrame")
    export_to_txt(row_method_as_df, "Row_DataFrame")
    export_to_txt(tuple_method_as_df, "Tuple_DataFrame")
    export_to_txt(normal_method_as_df, "Normal_DataFrame")
    export_to_txt(chunk_method_as_df, "Chunk_DataFrame") 