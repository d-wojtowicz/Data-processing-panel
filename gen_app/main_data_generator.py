import seaborn as sns
import pandas as pd

from utils.not_generators.data_generator_by_obj import DataGeneratorObj
from utils.data_generator_by_gen import DataGenerator

from utils.data_stats_calculator import *
from utils.data_exporter import DataExporter
from utils.pandas_extension import DataManager, gen_to_df, df_to_gen

from main_performance import full_export_tester

if __name__ == "__main__":
    dfMakingMeasure = calc.fullMeasure(gen_to_df) # Turned on time & storage measurement of Parsing types from Gen to Df

    # TESTING CREATOR (FROM GEN) FUNCTIONS
    gen_small = DataGenerator(10, 25)
    dataMakingByGenMeasure = calc.fullMeasure(gen_small.generate_dataframe_by_gen) # Turned on time & storage measurement of Generating Dataframe by generator

    # Creating Generators 
    gen_small_created = dataMakingByGenMeasure() # e.g. Generator creating objects (based on the specified pattern)

    # Transforming from GEN to OBJ of Dataframe (From prepared generators)
    df_small_obj = dfMakingMeasure(gen_small_created)

    # Transforming from OBJ of Dataframe to GEN (Reverse from prepared objects based on prepared generators) 
    df_small_gen = df_to_gen(df_small_obj)    # e.g. Generator storing object (compressing the storage)

    print("DATAFRAME MADE FROM GENERATOR:\n", df_small_obj)
    

    
    # TESTING CREATOR (FROM OBJ) FUNCTIONS
    gen_small = DataGeneratorObj(10, 25)
    dataMakingByObjMeasure = calc.fullMeasure(gen_small.generate_dataframe_by_obj) # Turned on time & storage measurement of Generating Dataframe by objects

    # Creating by Objects (using str, int, pd.Series & pd.DataFrame)
    df_small_obj2 = dataMakingByObjMeasure()

    print("DATAFRAME MADE FROM OBJECTS:\n", df_small_obj2)


    # TESTING EXPORTS
    export_gens_to_format = "json"
    full_export_tester(df_small_obj, "as_df")
    full_export_tester(df_small_gen, "as_gen", export_gens_to_format)