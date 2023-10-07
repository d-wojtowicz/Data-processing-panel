import seaborn as sns
import string

# Data generator
data_types = ["number", "text", "char"]
letters = string.ascii_lowercase

# Data reader
seaborn_libraries = sns.get_dataset_names()
sklearn_libraries = ["iris", "digits", "wine", "diabetes", "breast_cancer"]

# Pandas extension
numeric_types = ['int', 'int64', 'float', 'float64']
conditions_list = ['less', 'less than or equal', 'equal', 'greater than or equal', 'greater', '<', '<=', '==', '>=', '>']
dtypes_list = ['category', 'object']

# Data exporter
value_separator = ","
row_separator = ";"