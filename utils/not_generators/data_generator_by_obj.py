import pandas as pd

from random import randint, choice
from variables.lists import data_types, letters

def generate_dataframe_by_obj(number_of_cols: int, number_of_records: int) -> pd.DataFrame:
    col_names = ("Column" + str(i+1) for i in range(number_of_cols))

    generated_df = pd.DataFrame(columns=list(col_names))
    for col_name in generated_df.columns:
        generated_df[col_name] = generate_column(number_of_records, choice(data_types))

    return generated_df

def generate_column(number_of_records: int, data_type: str) -> list:
    if data_type == "number":
        generated_col = generate_number_column(1, 100, number_of_records)
    elif data_type == "text":
        generated_col = generate_text_column(5, 10, number_of_records)
    elif data_type == "char":
        generated_col = generate_char_column(number_of_records)

    return list(generated_col)

def generate_number_column(min_value: int, max_value: int, number_of_records: int) -> pd.Series:
    return (randint(min_value, max_value) for i in range(number_of_records))

def generate_text_column(min_length: int, max_length: int, number_of_records: int) -> pd.Series:
    return (generate_text_to_single_record(min_length,max_length) for i in range(number_of_records))

def generate_char_column(number_of_records: int) -> pd.Series:
    return (chr(randint(65,90)) for i in range(number_of_records))


def generate_text_to_single_record(min_length: int, max_length: int) -> str:
    text_generator = (choice(letters) for i in range(randint(min_length,max_length)))
    generated_record = "".join(text_generator)

    return generated_record