# TODO: Apply changes due to the OOP refactor of !DataReader and *DataManager

import seaborn as sns
import pandas as pd

from utils.not_generators.data_generator_by_obj import DataGenerator
from utils.data_generator_by_gen import DataGenerator

from utils.data_stats_calculator import *
from utils.data_exporter import DataExporter
from utils.pandas_extension import DataManager, gen_to_df, df_to_gen


if __name__ == "__main__":
    # If necessary, uncomment on what is needed

    dfMakingMeasure = calc.fullMeasure(gen_to_df) # Turned on time & storage measurement of Parsing types from Gen to Df

    # TESTING CREATOR (FROM GEN) FUNCTIONS
    gen_small = DataGenerator(10, 25)
    #gen_medium = DataGenerator(10, 500)
    #gen_big = DataGenerator(15, 5000)
    #gen_large = DataGenerator(20, 25000)
    dataMakingByGenMeasure = calc.fullMeasure(gen_small.generate_dataframe_by_gen) # Turned on time & storage measurement of Generating Dataframe by generator

    # Creating Generators 
    gen_small = dataMakingByGenMeasure(10, 25)       # e.g. Generator creating objects (based on the specified pattern)
    #gen_medium = dataMakingByGenMeasure(10, 500)
    #gen_big = dataMakingByGenMeasure(15, 5000)
    #gen_large = dataMakingByGenMeasure(20, 25000)

    # Transforming from GEN to OBJ of Dataframe (From prepared generators)
    df_small_obj = dfMakingMeasure(gen_small)
    #df_medium_obj = dfMakingMeasure(gen_medium)
    #df_big_obj = dfMakingMeasure(gen_big)
    #df_large_obj = dfMakingMeasure(gen_large)

    # Transforming from OBJ of Dataframe to GEN (Reverse from prepared objects based on prepared generators) 
    df_small_gen = df_to_gen(df_small_obj)    # e.g. Generator storing object (compressing the storage)
    #df_medium_gen = df_to_gen(df_medium_obj)
    #df_big_gen = df_to_gen(df_big_obj)
    #df_large_gen = df_to_gen(df_large_obj)

    print("DATAFRAME MADE FROM GENERATOR:\n", df_small_obj)
    

    
    # TESTING CREATOR (FROM OBJ) FUNCTIONS
    dataMakingByObjMeasure = calc.fullMeasure(generate_dataframe_by_obj) # Turned on time & storage measurement of Generating Dataframe by objects

    # Creating by Objects (using str, int, pd.Series & pd.DataFrame)
    df_small_obj2 = dataMakingByObjMeasure(5, 25)
    #df_medium_obj2 = dataMakingByObjMeasure(10, 500)
    #df_big_obj2 = dataMakingByObjMeasure(15, 5000)
    #df_large_obj2 = dataMakingByObjMeasure(20, 25000)

    print("DATAFRAME MADE FROM OBJECTS:\n", df_small_obj2)



    # TESTING EXPORTS
    txtExportMeasure = calc.fullMeasure(export_to_txt) 
    jsonExportMeasure = calc.fullMeasure(export_to_json)
    csvExportMeasure = calc.fullMeasure(export_to_csv)
    xlsxExportMeasure = calc.fullMeasure(export_to_xlsx)
    pdfExportMeasure = calc.fullMeasure(export_to_pdf)

    #txtExportMeasure(df_small_obj, "as_df")
    #txtExportMeasure(df_small_gen, "as_gen")
    #jsonExportMeasure(df_small_obj, "as_df")
    #jsonExportMeasure(df_small_gen, "as_gen")
    #csvExportMeasure(df_small_obj, "as_df")
    #csvExportMeasure(df_small_gen, "as_gen")
    #xlsxExportMeasure(df_small_obj, "as_df")
    #xlsxExportMeasure(df_small_gen, "as_gen")
    #pdfExportMeasure(df_small_obj, "as_df")
    #pdfExportMeasure(df_small_gen, "as_gen")