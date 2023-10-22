from typing import Union
from types import GeneratorType

import pandas as pd

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
        match location_method:
            case read_from.TOP:
                result_df = self.dataset.head(limit)     
            case read_from.BOTTOM:
                result_df = self.dataset.tail(limit)
            case read_from.RANDOM:
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

        if self.dataset[field_title].dtypes in numeric_types:
            TYPE_VALIDATION = True

        if condition in conditions_list:
            CONDITION_VALIDATION = True
            
        if NAME_VALIDATION and VALUE_VALIDATION and TYPE_VALIDATION and CONDITION_VALIDATION:
            match condition:
                case "less" | "<":
                    result_df = self.dataset.loc[self.dataset[field_title] < field_value]
                case "less than or equal" | "<=":
                    result_df = self.dataset.loc[self.dataset[field_title] <= field_value]
                case "equal" | "==":
                    result_df = self.dataset.loc[self.dataset[field_title] == field_value]
                case "greater" | ">":
                    result_df = self.dataset.loc[self.dataset[field_title] > field_value]
                case "greater than or equal" | ">=":
                    result_df = self.dataset.loc[self.dataset[field_title] >= field_value]
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

