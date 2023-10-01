# *TODO: Extend functionality by adding the same action with the help of generators.
# TODO: Add export to .xlsx, .csv, .pdf

import os

import json
import pandas as pd
from datetime import date, datetime

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_path = "files"
files_path = os.path.join(project_path, relative_path)

def export_to_txt(df: pd.DataFrame, file_name: str) -> None:
    todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_name = todays_date + "_" + file_name + ".txt"

    full_path = os.path.join(files_path, file_name)
    with open(full_path, "a") as f:
        df_text = df.to_string(header=True, index=True)
        f.write(df_text)

def export_to_json(df: pd.DataFrame, file_name: str) -> None:
    todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_name = todays_date + "_" + file_name + ".json"

    full_path = os.path.join(files_path, file_name)
    df = df.to_json(orient="records")
    with open(full_path, "w") as f:
        json.dump(df, f)
