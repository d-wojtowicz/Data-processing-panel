import sys, os
import pandas as pd

from typing import Union
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variables.lists import numeric_types, conditions_list, dtypes_list
from variables.enumerators import *

def df_to_gen(df: pd.DataFrame) -> GeneratorType: 
    for _, row in df.iterrows():
        yield row

def gen_to_df(gen) -> pd.DataFrame:
    return pd.concat(gen, ignore_index=True)


class DataManager(object):
    def __init__(self, dataset: Union[pd.DataFrame, GeneratorType]):
        self.dataset: pd.DataFrame = pd.DataFrame(dataset)

    def get_columns(self) -> list:
        return self.dataset.columns.to_list()

    def get_column_types(self) -> list:
        return self.dataset.dtypes.to_list()

    def get_df_by_limit(self, limit: int, location_method: Enum = read_from.TOP) -> pd.DataFrame:
        result_df = pd.DataFrame()
        match location_method.value:
            case read_from.TOP.value:
                result_df = self.dataset.head(limit)     
            case read_from.BOTTOM.value:
                result_df = self.dataset.tail(limit)
            case read_from.RANDOM.value:
                if limit < len(self.dataset):
                    result_df = self.dataset.sample(limit)
                else:
                    result_df = self.dataset.sample()
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")      

        return result_df
    
    def get_df_by_numeric(self, field_title: str, field_value: Union[int, float], condition: str) -> pd.DataFrame:
        result_df = pd.DataFrame()
        NAME_VALIDATION, VALUE_VALIDATION, TYPE_VALIDATION, CONDITION_VALIDATION = False, False, False, False

        if field_title in self.get_columns():
            NAME_VALIDATION = True
        
        if type(field_value).__name__ in numeric_types:
            VALUE_VALIDATION = True
            if type(field_value).__name__ == "list":
                for single_value in field_value:
                    if type(single_value).__name__ not in numeric_types:
                        VALUE_VALIDATION = False
                    
        if self.dataset[field_title].dtypes in numeric_types:
            TYPE_VALIDATION = True

        if condition in conditions_list:
            CONDITION_VALIDATION = True
        
        MAX_VALUE = max(field_value)
        MIN_VALUE = min(field_value)
        
        if NAME_VALIDATION and VALUE_VALIDATION and TYPE_VALIDATION and CONDITION_VALIDATION:
            match condition:
                case "less than" | "<":
                    result_df = self.dataset.loc[self.dataset[field_title] < MAX_VALUE]
                case "less than or equal" | "<=":
                    result_df = self.dataset.loc[self.dataset[field_title] <= MAX_VALUE]
                case "equal" | "==":
                    for value in list(set(field_value)):
                        tmp_df = self.dataset.loc[self.dataset[field_title] == value]
                        result_df = pd.concat([result_df, tmp_df])
                case "greater than" | ">":
                    result_df = self.dataset.loc[self.dataset[field_title] > MIN_VALUE]
                case "greater than or equal" | ">=":
                    result_df = self.dataset.loc[self.dataset[field_title] >= MIN_VALUE]
                case _:
                    raise Exception("You specified a wrong condition!")
        else:
            raise Exception("Program did not pass the query validation!")
        
        return result_df
        
    def get_df_by_category(self, field_title: str, field_values: set[str]) -> pd.DataFrame:
        result_df = pd.DataFrame()
        NAME_VALIDATION, VALUE_VALIDATION, TYPE_VALIDATION = False, False, False

        if field_title in self.get_columns():
            NAME_VALIDATION = True
        
        if len([single_field_value for single_field_value in field_values if type(single_field_value).__name__ in ['str']]) == len(field_values):
            VALUE_VALIDATION = True

        if self.dataset[field_title].dtypes in dtypes_list:
            TYPE_VALIDATION = True

        if NAME_VALIDATION and VALUE_VALIDATION and TYPE_VALIDATION:
            result_df = self.dataset[self.dataset[field_title].isin(field_values)]
        else:
            raise Exception("Program did not pass the category query validation!")
        
        return result_df

