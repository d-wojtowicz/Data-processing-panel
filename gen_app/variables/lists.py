import seaborn as sns
import string
from reportlab.lib.pagesizes import A4

# Main app GUI
comparision_marks = ['less than', 'less than or equal', 'equal', 'greater than or equal', 'greater than']
exports = ["TXT", "JSON", "CSV", "XLSX", "PDF"]
read_with_gen = [True, False]

# Data generator
data_types = ["number", "text", "char"]
letters = string.ascii_lowercase

# Data reader
seaborn_libraries = sns.get_dataset_names()
sklearn_libraries = ["iris", "digits", "wine", "diabetes", "breast_cancer"]

# Pandas extension
numeric_types = ['int', 'int64', 'float', 'float64', 'list']
conditions_list = ['less than', 'less than or equal', 'equal', 'greater than or equal', 'greater than', '<', '<=', '==', '>=', '>']
dtypes_list = ['category', 'object']

# Data exporter
value_separator = ","
row_separator = ";"
PAGE_SIZE = A4
PAGE_WIDTH = 210 # [mm] Width for A4
MARGIN = 15
