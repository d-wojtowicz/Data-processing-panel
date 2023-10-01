from typing import Union

import pandas as pd

from variables.lists import numeric_types, conditions_list, dtypes_list

def get_columns(df: pd.DataFrame) -> list:
    return df.columns.to_list()

def get_column_types(df: pd.DataFrame) -> list:
    return df.dtypes.to_list()

def get_df_by_query(df: pd.DataFrame, field_title: str, field_value: Union[int, float], condition: str) -> pd.DataFrame:
    NAME_VALIDATION, VALUE_VALIDATION, TYPE_VALIDATION, CONDITION_VALIDATION = False, False, False, False

    if field_title in get_columns(df):
        NAME_VALIDATION = True
    
    if type(field_value).__name__ in numeric_types:
        VALUE_VALIDATION = True

    if df[field_title].dtypes in numeric_types:
        TYPE_VALIDATION = True

    if condition in conditions_list:
        CONDITION_VALIDATION = True
        
    if NAME_VALIDATION and VALUE_VALIDATION and TYPE_VALIDATION and CONDITION_VALIDATION:
        match condition:
            case "less" | "<":
                df = df.loc[df[field_title] < field_value]
            case "less than or equal" | "<=":
                df = df.loc[df[field_title] <= field_value]
            case "equal" | "==":
                df = df.loc[df[field_title] == field_value]
            case "greater" | ">":
                df = df.loc[df[field_title] > field_value]
            case "greater than or equal" | ">=":
                df = df.loc[df[field_title] >= field_value]
            case _:
                raise Exception("You specified a wrong condition!")
    else:
        raise Exception("Program did not pass the query validation!")
    
    return df

def get_df_by_category(df: pd.DataFrame, field_title: str, field_values: set[str]) -> pd.DataFrame:
    NAME_VALIDATION, VALUE_VALIDATION, TYPE_VALIDATION = False, False, False

    if field_title in get_columns(df):
        NAME_VALIDATION = True
    
    if len([single_field_value for single_field_value in field_values if type(single_field_value).__name__ in ['str']]) == len(field_values):
        VALUE_VALIDATION = True

    if df[field_title].dtypes in dtypes_list:
        TYPE_VALIDATION = True

    if NAME_VALIDATION and VALUE_VALIDATION and TYPE_VALIDATION:
        df = df[df[field_title].isin(field_values)]
    else:
        raise Exception("Program did not pass the category query validation!")
    
    return df

