import seaborn as sns
import pandas as pd

from utils.data_generator import *
from utils.data_stats_calculator import *
from utils.data_exporter import *
from utils.pandas_extension import *

# TESTING GENERATOR FUNCTIONS
genMakingMeasure = calc.fullMeasure(generate_dataframe) # Turned on time & storage measurement of Generating Dataframe
dfMakingMeasure = calc.fullMeasure(gen_to_df)           # Turned on time & storage measurement of Parsing types from Gen to Df

gen_of_small_df = genMakingMeasure(10, 25)       # e.g. Generator creating objects (based on the specified pattern)
#gen_of_medium_df = genMakingMeasure(10, 500)
#gen_of_big_df = genMakingMeasure(15, 5000)
#gen_of_large = genMakingMeasure(20, 25000)

df_small = dfMakingMeasure(gen_of_small_df)
#df_medium = dfMakingMeasure(gen_of_medium_df)
#df_big = dfMakingMeasure(gen_of_big_df)
#df_large = dfMakingMeasure(gen_of_large_df)

small_df_in_generator = df_to_gen(df_small)    # e.g. Generator storing object (compressing the storage)
#medium_df_in_generator = df_to_gen(df_medium)
#big_df_in_generator = df_to_gen(df_big)
#large_df_in_generator = df_to_gen(df_large)



# TESTING EXPORTS
txtExportMeasure = calc.fullMeasure(export_to_txt) 
jsonExportMeasure = calc.fullMeasure(export_to_json)
csvExportMeasure = calc.fullMeasure(export_to_csv)
xlsxExportMeasure = calc.fullMeasure(export_to_xlsx)
pdfExportMeasure = calc.fullMeasure(export_to_pdf)

#txtExportMeasure(df_small, "as_df")
#txtExportMeasure(small_df_in_generator, "as_gen")
#jsonExportMeasure(df_small, "as_df")
#jsonExportMeasure(small_df_in_generator, "as_gen")
#csvExportMeasure(df_small, "as_df")
#csvExportMeasure(small_df_in_generator, "as_gen")
#xlsxExportMeasure(df_small, "as_df")
#xlsxExportMeasure(small_df_in_generator, "as_gen")
#pdfExportMeasure(df_small, "as_df")
#pdfExportMeasure(small_df_in_generator, "as_gen")