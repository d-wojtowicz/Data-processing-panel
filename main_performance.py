# TODO: Apply corrections to avoid the execution of 'eval' function and measure time and capacity correctly
# Requirements: Enhance data_stats_calculator.py functions firstly

import seaborn as sns
import pandas as pd

from utils.data_stats_calculator import *
from utils.data_exporter import *

from source.data_reader import *

if __name__ == "__main__":

    # Testing performance on the example of 'diamonds' seaborn dataframe set:
    
    column_method = 'read_df_from_seaborn("diamonds", read_from.TOP, read_by.COLUMNS, 10000)'
    row_method = 'read_df_from_seaborn("diamonds", read_from.TOP, read_by.ROWS, 10000)'
    tuple_method = 'read_df_from_seaborn("diamonds", read_from.TOP, read_by.TUPLES, 10000)'
    normal_method = 'read_df_from_seaborn("diamonds", read_from.TOP, read_by.NORMAL, 10000)'
    chunk_method = 'read_df_from_seaborn("diamonds", read_from.TOP, read_by.CHUNKS, 10000)'

    columns_read_time = calc.timeMeasure(column_method)
    columns_read_memory = calc.sizeMeasure(column_method)

    rows_read_time = calc.timeMeasure(row_method)
    rows_read_memory = calc.sizeMeasure(row_method)

    tuples_read_time = calc.timeMeasure(tuple_method)
    tuples_read_memory = calc.sizeMeasure(tuple_method)

    normal_read_time = calc.timeMeasure(normal_method)
    normal_read_memory = calc.sizeMeasure(normal_method)

    chunk_read_time = calc.timeMeasure(chunk_method)
    chunk_read_memory = calc.sizeMeasure(chunk_method)

    print(columns_read_time, rows_read_time, tuples_read_time, normal_read_time, chunk_read_time)
    print(columns_read_memory, rows_read_memory, tuples_read_memory, normal_read_memory, chunk_read_memory)

    column_method_df = eval(column_method)
    row_method_df = eval(row_method)
    tuple_method_df = eval(tuple_method)
    normal_method_df = eval(normal_method)
    chunk_method_df = eval(chunk_method)

    export_to_txt(column_method_df, "Column_DataFrame")
    export_to_txt(row_method_df, "Row_DataFrame")
    export_to_txt(tuple_method_df, "Tuple_DataFrame")
    export_to_txt(normal_method_df, "normal_DataFrame")
    export_to_txt(chunk_method_df, "Chunk_DataFrame")
