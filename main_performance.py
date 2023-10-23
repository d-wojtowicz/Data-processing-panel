# TODO: Apply changes due to the OOP refactor of !DataReader and *DataManager FOR SKLEARN like for SEABORN

import pandas as pd
from typing import Union
from types import GeneratorType

from utils.pandas_extension import DataManager, df_to_gen, gen_to_df
from utils.data_stats_calculator import *
from utils.data_exporter import DataExporter

from source.data_reader import DataReader
from variables.enumerators import read_from, read_by, reader_tester

def full_export_tester(dataset: Union[pd.DataFrame, GeneratorType], file_name: str, gen_format: str = "txt") -> None:
    methods = ["txt", "json", "csv", "xlsx", "pdf"]
    print("\nTESTS OF EXPORT MEASUREMENTS FROM: " + file_name)
    if type(dataset) == pd.DataFrame:
        for method in methods:
            export_tester(dataset, file_name, method)
    elif type(dataset) == GeneratorType:
        if gen_format in methods:
            export_tester(dataset, file_name, gen_format)
    else:
        raise Exception("Wrong data type of input dataset.")

def export_tester(dataset: Union[pd.DataFrame, GeneratorType], file_name: str, method: str) -> None:
    export = DataExporter(dataset, file_name)
    match method:
        case "txt":
            time_measure_of_export = calc.timeMeasure(export.export_to_txt)
        case "json":
            time_measure_of_export = calc.timeMeasure(export.export_to_json)
        case "csv":
            time_measure_of_export = calc.timeMeasure(export.export_to_csv)
        case "xlsx":
            time_measure_of_export = calc.timeMeasure(export.export_to_xlsx)
        case "pdf":
            time_measure_of_export = calc.timeMeasure(export.export_to_pdf)
        case _:
            raise Exception("Something went wrong.")
    
    time_measure_of_export()
    

if __name__ == "__main__":
    # Select the Reader tester performance (SEABORN | SKLEARN | INDIVIDUAL)
    SELECTED_TESTS = reader_tester.SEABORN
    
    match SELECTED_TESTS:
        case reader_tester.SEABORN:
            # Testing performance on the example of 'diamonds' seaborn dataframe set:
            dataset = "diamonds"
            source = "seaborn"
            read_rows = read_from.TOP

            column_seaborn_reader = DataReader(dataset, source, read_rows, read_by.COLUMNS, 100)
            row_seaborn_reader_gen = DataReader(dataset, source, read_rows, read_by.ROWS, 100)
            row_seaborn_reader = DataReader(dataset, source, read_rows, read_by.ROWS, 100, by_gen=False)
            tuple_seaborn_reader_gen = DataReader(dataset, source, read_rows, read_by.TUPLES, 100)
            tuple_seaborn_reader = DataReader(dataset, source, read_rows, read_by.TUPLES, 100, by_gen=False)
            normal_seaborn_reader = DataReader(dataset, source, read_rows, read_by.NORMAL, 100)
            chunk_seaborn_reader_gen = DataReader(dataset, source, read_rows, read_by.CHUNKS, 100)
            chunk_seaborn_reader = DataReader(dataset, source, read_rows, read_by.CHUNKS, 100, by_gen=False)

            all_seaborn_readers = [column_seaborn_reader, row_seaborn_reader_gen, row_seaborn_reader, 
                                   tuple_seaborn_reader_gen, tuple_seaborn_reader, normal_seaborn_reader,
                                   chunk_seaborn_reader_gen, chunk_seaborn_reader]
            all_seaborn_readers_names = ["Column method (by obj):", "Row method (by gen):", "Row method (by obj):",
                                         "Tuple method (by gen):", "Tuple method (by obj):", "Normal method (by obj):",
                                         "Chunk method (by gen):", "Chunk method (by obj):"]
            all_seaborn_readers_names_obj = [name for name in all_seaborn_readers_names if "(by gen)" not in name]
            all_seaborn_readers_names_gen = [name for name in all_seaborn_readers_names if "(by obj)" not in name]
            

            # Testing of ALL exports from ALL methods of df generating
            # *When generator is used, it become empty so it is possible to export it only once.
            export_gens_to_format = "json"
            for name, reader in zip(all_seaborn_readers_names, all_seaborn_readers):
                name = name.replace(" method (by obj):", "_obj")
                name = name.replace(" method (by gen):", "_gen")
                reader.read_data()
                dataset = reader.dataset
                if type(dataset) == pd.DataFrame:
                    full_export_tester(dataset, name)
                else:
                    full_export_tester(dataset, name, export_gens_to_format)


            # Testing of generating dataframes by all methods & printing their results
            print("\nREADING MEASUREMENTS (TO DFs or TO GENs):")
            readed_datasets = []
            for seaborn_reader in all_seaborn_readers:
                full_measure_with_seaborn = calc.fullMeasure(seaborn_reader.read_data)  # Time & Storage of readed df
                readed_datasets.append(full_measure_with_seaborn())
            
            print("\nREADED DFs and GENs:")
            for name, dataset in zip(all_seaborn_readers_names, readed_datasets):
                print("\n" + name)
                print(dataset)

        
            # Testing of storage measurements (of parsed df to gen) by all methods (all of them initially are NOT generators!)
            print("\nMEASURED STORAGE OF GENs PARSED FROM DFs (BY OWN METHOD):")
            size_measure_of_generator = calc.sizeMeasure(df_to_gen)  # Storage of gen made from df rows
            readed_datasets_obj = []
            readed_datasets_gen = []
            readed_df_to_gen = []
            for dataset in readed_datasets:
                if type(dataset) == pd.DataFrame:
                    size_measured_dataset = size_measure_of_generator(dataset)
                    readed_df_to_gen.append(size_measured_dataset)
                    readed_datasets_obj.append(dataset)
                elif type(dataset) == GeneratorType:
                    readed_datasets_gen.append(dataset)

            for name, dataset in zip(all_seaborn_readers_names_obj, readed_df_to_gen):
                print("\n" + name)
                print(dataset)
            

        case reader_tester.SKLEARN:
            # Testing performance on the example of 'diabetes' sklearn dataframe set:
            full_measure_with_sklearn = calc.fullMeasure(df_to_gen)  # Time & Storage of readed df
            size_measure_of_generator = calc.sizeMeasure(df_to_gen)             # Storage of gen made from df rows

            # Testing of generating dataframes by all methods & printing their results
            print("\nREADING MEASUREMENTS (TO DFs or TO GENs):")
            column_method_as_df = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.COLUMNS, 100)
            row_method_as_df1 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.ROWS, 100, by_gen=True) 
            row_method_as_df2 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.ROWS, 100, by_gen=False) # PerformanceWarning
            tuple_method_as_df1 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.TUPLES, 100, by_gen=True)
            tuple_method_as_df2 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.TUPLES, 100, by_gen=False)
            normal_method_as_df = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.NORMAL, 100)
            chunk_method_as_df1 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.CHUNKS, 100, by_gen=True)
            chunk_method_as_df2 = full_measure_with_sklearn("diabetes", read_from.TOP, read_by.CHUNKS, 100, by_gen=False)

            print("\nREADED DFs and GENs:")
            print("Column method (by obj): \n", column_method_as_df)
            print("Row method (by gen): \n", row_method_as_df1)
            print("Row method (by obj): \n", row_method_as_df2)
            print("Tuple method (by gen): \n", tuple_method_as_df1)
            print("Tuple method (by obj): \n", tuple_method_as_df2)
            print("Normal method (by obj): \n", normal_method_as_df)
            print("Chunk method (by gen): \n", chunk_method_as_df1)
            print("Chunk method (by obj): \n", chunk_method_as_df2)

            # Testing of storage measurements (of parsed df to gen) by all methods (all of them initially are NOT generators!)
            print("\nMEASURED STORAGE OF GENs PARSED FROM DFs (BY OWN METHOD):")
            column_method_as_gen = size_measure_of_generator(column_method_as_df)
            row_method_as_gen = size_measure_of_generator(row_method_as_df2)
            tuple_method_as_gen = size_measure_of_generator(tuple_method_as_df2)
            normal_method_as_gen = size_measure_of_generator(normal_method_as_df)
            chunk_method_as_gen = size_measure_of_generator(chunk_method_as_df2)

            # Testing of ALL exports from ALL methods of df generating
            # *When generator is used, it become empty so it is possible to export it only once.
            export_gens_to_format = "txt"
            full_export_tester(column_method_as_df, "column_df")
            full_export_tester(row_method_as_df1, "row_gen", export_gens_to_format)
            full_export_tester(row_method_as_df2, "row_df")
            full_export_tester(tuple_method_as_df1, "tuple_gen", export_gens_to_format)
            full_export_tester(tuple_method_as_df2, "tuple_df")
            full_export_tester(normal_method_as_df, "normal_df")
            full_export_tester(chunk_method_as_df1, "chunk_gen", export_gens_to_format)
            full_export_tester(chunk_method_as_df2, "chunk_df")

        case reader_tester.INDIVIDUAL:
            """"""
        case _:
            raise Exception("You selected wrong tester enumerator (Variable 'SELECTED_TESTS' at the top of program).")