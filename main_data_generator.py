import seaborn as sns
import pandas as pd

from utils.data_generator import *
from utils.data_stats_calculator import *
from utils.data_exporter import *

df_small = generate_dataframe(5, 10)
df_medium = generate_dataframe(10, 500)
df_big = generate_dataframe(15, 5000)
df_large = generate_dataframe(20, 25000)