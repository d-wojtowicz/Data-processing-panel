import sys, os
from sklearn.datasets import load_iris, load_digits, load_wine, load_diabetes, load_breast_cancer
import pandas as pd
from typing import Union
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variables.enumerators import *
from variables.lists import *

class DataSklearnReader(object):
    def __init__(self, df_name: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True):
        """ 'by_gen' parameter concerns only to the 'row_reader' & 'tuple_reader' & 'chunk_reader"""
        self.dataset: Union[pd.DataFrame, GeneratorType] = None
        self.sklearn_df: pd.DataFrame = None

        self.df_name: str = df_name

        self.location_method: Enum = location_method.value
        self.structure_method: Enum = structure_method.value
        self.limit: int = limit
        self.by_gen: bool = by_gen
        self.ADJUSTABLE_CHUNK_SIZE = 1000

    # Main functions - methods to read data
    def read_df_from_sklearn(self) -> None:
        if self.df_name is not None:
            if self.df_name in sklearn_libraries:
                self.read_full_df_by_name()
                match self.structure_method:
                    case read_by.NORMAL.value:
                        self.dataset = self.normal_reader()
                    case read_by.COLUMNS.value:
                        self.dataset = self.column_reader()
                    case read_by.ROWS.value:
                        if self.by_gen:
                            self.dataset = self.rows_reader_by_gen()
                        else:
                            self.dataset = self.rows_reader()
                    case read_by.TUPLES.value:
                        if self.by_gen:
                            self.dataset = self.tuples_reader_by_gen()
                        else:
                            self.dataset = self.tuples_reader()
                    case read_by.CHUNKS.value:
                        if self.by_gen:
                            self.dataset = self.chunks_reader_by_gen()
                        else:
                            self.dataset = self.chunks_reader()
                    case _:
                        raise Exception("You chose the wrong enumerator!")
            else:
                raise Exception("There is no dataframe in the Sklearn package with this df_name!")
        else:
            raise Exception("Your dataframe name is wrong!")


    # Structured smaller functions - to support major functionalities
    def read_full_df_by_name(self) -> None:
        match self.df_name:
            case "iris":
                sklearn_df = load_iris()
            case "digits":
                sklearn_df = load_digits()
            case "wine":
                sklearn_df = load_wine()
            case "diabetes":
                sklearn_df = load_diabetes()
            case "breast_cancer":
                sklearn_df = load_breast_cancer()
            case _:
                raise Exception("There is no dataframe in the Sklearn package with this df_name!")
        
        self.sklearn_df = pd.DataFrame(data=sklearn_df.data, columns=sklearn_df.feature_names)

    def normal_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()

        match self.location_method:
            case read_from.TOP.value:
                result_df = self.sklearn_df.head(self.limit)      
            case read_from.BOTTOM.value:
                result_df = self.sklearn_df.tail(self.limit) 
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    result_df = self.sklearn_df.sample(self.limit) 
                else:
                    result_df = self.sklearn_df.sample() 
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

        return result_df

    def column_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()

        match self.location_method:
            case read_from.TOP.value:
                for col_name, data in self.sklearn_df.head(self.limit).items():
                    result_df[col_name] = data
            case read_from.BOTTOM.value:
                for col_name, data in self.sklearn_df.tail(self.limit).items():
                    result_df[col_name] = data
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for col_name, data in self.sklearn_df.sample(self.limit).items():
                        result_df[col_name] = data
                else:
                    for col_name, data in self.sklearn_df.sample().items():
                        result_df[col_name] = data
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
        return result_df

    def rows_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP.value:
                for _, row in self.sklearn_df.head(self.limit).iterrows():
                    yield row
            case read_from.BOTTOM.value:
                for _, row in self.sklearn_df.tail(self.limit).iterrows():
                    yield row
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for _, row in self.sklearn_df.sample(self.limit).iterrows():
                        yield row
                else:  
                    for _, row in self.sklearn_df.sample().iterrows():
                        yield row
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

    def rows_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()

        match self.location_method:
            case read_from.TOP.value:
                for row_index, row in self.sklearn_df.head(self.limit).iterrows():
                    result_df[row_index] = row
            case read_from.BOTTOM.value:
                for row_index, row in self.sklearn_df.tail(self.limit).iterrows():
                    result_df[row_index] = row
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for row_index, row in self.sklearn_df.sample(self.limit).iterrows():
                        result_df[row_index] = row
                else:
                    for row_index, row in self.sklearn_df.sample().iterrows():
                        result_df[row_index] = row
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

        result_df = result_df.transpose() 
        return result_df

    def tuples_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP.value:
                for single_tuple in self.sklearn_df.head(self.limit).itertuples(index=False):
                    yield dict(zip(self.sklearn_df.columns, single_tuple))
            case read_from.BOTTOM.value:
                for single_tuple in self.sklearn_df.tail(self.limit).itertuples(index=False):
                    yield dict(zip(self.sklearn_df.columns, single_tuple))
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for single_tuple in self.sklearn_df.sample(self.limit).itertuples(index=False):
                        yield dict(zip(self.sklearn_df.columns, single_tuple))
                else:
                    for single_tuple in self.sklearn_df.sample().itertuples(index=False):
                        yield dict(zip(self.sklearn_df.columns, single_tuple))
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
        
    def tuples_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()

        match self.location_method:
            case read_from.TOP.value:
                result_df  = self.sklearn_df.head(self.limit).itertuples(index=False)
            case read_from.BOTTOM.value:
                result_df = self.sklearn_df.tail(self.limit).itertuples(index=False)
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    result_df = self.sklearn_df.sample(self.limit).itertuples(index=False)
                else:
                    result_df = self.sklearn_df.sample().itertuples(index=False)
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
        
        result_df = pd.DataFrame(result_df)
        result_df.columns = self.sklearn_df.columns
        return result_df

    def chunks_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP.value:
                for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.head(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    yield partial_result_df
            case read_from.BOTTOM.value:
                for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.tail(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    yield partial_result_df
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.sample(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                        yield partial_result_df
                else:
                    for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.sample(), self.ADJUSTABLE_CHUNK_SIZE):
                        yield partial_result_df
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
    def chunks_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()
        
        match self.location_method:
            case read_from.TOP.value:
                for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.head(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
            case read_from.BOTTOM.value:
                for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.tail(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
            case read_from.RANDOM.value:
                if self.limit < len(self.sklearn_df):
                    for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.sample(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                        result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
                else:
                    for partial_result_df in self.dataframe_chunk_generator(self.sklearn_df.sample(), self.ADJUSTABLE_CHUNK_SIZE):
                        result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

        return result_df

    def dataframe_chunk_generator(self, df: pd.DataFrame, chunk_size: int) -> pd.DataFrame:
        num_of_chunks = len(df) // chunk_size + 1
        for chunk_id in range(num_of_chunks):
            from_id = chunk_id * chunk_size
            to_id = (chunk_id + 1) * chunk_size
            chunk_value = df[from_id:to_id]
            if not chunk_value.empty:
                yield chunk_value