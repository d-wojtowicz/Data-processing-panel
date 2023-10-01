import seaborn as sns
import pandas as pd

from utils.data_generator import *
from utils.data_stats_calculator import *
from utils.data_exporter import *
from utils.pandas_extension import *

genMakingMeasure = calc.fullMeasure(generate_dataframe)
dfMakingMeasure = calc.fullMeasure(gen_to_df)

gen_small = genMakingMeasure(5, 25)
gen_medium = genMakingMeasure(10, 500)
gen_big = genMakingMeasure(15, 5000)
#gen_large = genMakingMeasure(20, 25000)

df_small = dfMakingMeasure(gen_small)
df_medium = dfMakingMeasure(gen_medium)
df_big = dfMakingMeasure(gen_big)
#df_large = dfMakingMeasure(gen_large)

print(df_small)