import seaborn as sns
import pandas as pd

from utils.data_generator import *
from utils.data_stats_calculator import *
from utils.data_exporter import *
from utils.pandas_extension import *

# TESTING GENERATOR FUNCTIONS
genMakingMeasure = calc.fullMeasure(generate_dataframe)
dfMakingMeasure = calc.fullMeasure(gen_to_df)
exportMeasure = calc.fullMeasure(export_to_txt) 

gen_of_small_df = genMakingMeasure(100, 500)       # e.g. Generator creating objects (based on the specified pattern)
#gen_of_medium_df = genMakingMeasure(10, 500)
#gen_of_big_df = genMakingMeasure(15, 5000)
#gen_of_large = genMakingMeasure(20, 25000)

df_small = dfMakingMeasure(gen_of_small_df)
#df_medium = dfMakingMeasure(gen_of_medium_df)
#df_big = dfMakingMeasure(gen_of_big_df)
#df_large = dfMakingMeasure(gen_of_large_df)

exportMeasure(df_small, "as_df")
small_df_in_generator =  df_to_gen(df_small)    # e.g. Generator storing object (compressing the storage)
exportMeasure(small_df_in_generator, "as_gen")