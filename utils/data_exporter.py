# *TODO: Extend functionality by adding the same action with the help of generators.
# TODO: Add export to .xlsx, .csv, .pdf

import os

import json
import pandas as pd

from datetime import date, datetime
from typing import Union
from types import GeneratorType
from variables.lists import value_separator, row_separator

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_path = "files"
files_path = os.path.join(project_path, relative_path)

def export_to_txt(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_name = todays_date + "_" + file_name + ".txt"

    full_path = os.path.join(files_path, file_name)
    
    with open(full_path, "w") as f:
        if type(dataset) == pd.DataFrame:
            f.write(value_separator.join(map(str, dataset.columns)) + row_separator + "\n")
            for _, row in dataset.iterrows():
                row_str = value_separator.join(map(str, row))
                f.write(row_str + row_separator + "\n")
        elif type(dataset) == GeneratorType:
            columns_displayed = False
            for row in dataset:
                if not columns_displayed:
                    column_str = value_separator.join(map(str, row.keys()))
                    f.write(column_str + row_separator + "\n")
                    columns_displayed = True
                
                row_str = value_separator.join(map(str, row))
                f.write(row_str + row_separator + "\n")
        else:
            raise Exception("Unwanted input data types.")
    

def export_to_json(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_name = todays_date + "_" + file_name + ".json"

    full_path = os.path.join(files_path, file_name)

    with open(full_path, "w") as f:
        if type(dataset) == pd.DataFrame:
            df = dataset.to_json(orient="records", lines=True)
            f.write(df)
        elif type(dataset) == GeneratorType:
            for row in dataset:
                f.write(json.dumps(row.to_dict()) + "\n")

