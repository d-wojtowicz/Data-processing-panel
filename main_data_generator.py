import seaborn as sns
import pandas as pd

from utils.data_generator_by_gen import *
from utils.not_generators.data_generator_by_obj import *

from utils.data_stats_calculator import *
from utils.data_exporter import *
from utils.pandas_extension import *

dataMakingByGenMeasure = calc.fullMeasure(generate_dataframe_by_gen)
dataMakingByObjMeasure = calc.fullMeasure(generate_dataframe_by_obj)
dfTransformingMeasure = calc.fullMeasure(gen_to_df)

# Creating by Generator
gen_small = dataMakingByGenMeasure(5, 25)
#gen_medium = dataMakingByGenMeasure(10, 500)
#gen_big = dataMakingByGenMeasure(15, 5000)
#gen_large = dataMakingByGenMeasure(20, 25000)

# Creating by Objects (using str, int, pd.Series & pd.DataFrame)
df_small = dataMakingByObjMeasure(5, 25)
#df_medium = dataMakingByObjMeasure(10, 500)
#df_big = dataMakingByObjMeasure(15, 5000)
#df_large = dataMakingByObjMeasure(20, 25000)

# Transforming from GEN to OBJ of Dataframe
gen_to_df_small = dfTransformingMeasure(gen_small)
#gen_to_df_medium =dfTransformingMeasure(gen_medium)
#gen_to_df_big = dfTransformingMeasure(gen_big)
#gen_to_df_large = dfTransformingMeasure(gen_large)

print(gen_to_df_small)
print(df_small)