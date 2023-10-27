import sys, os

import seaborn as sns
import pandas as pd
from typing import Union
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variables.enumerators import *
from variables.lists import *

class DataSeabornReader(object):
    def __init__(self, df_name: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True):
        """ 'by_gen' parameter concerns only to the 'row_reader' & 'tuple_reader' & 'chunk_reader"""
        self.dataset: Union[pd.DataFrame, GeneratorType] = None

        self.df_name: str = df_name

        self.location_method: Enum = location_method
        self.structure_method: Enum = structure_method
        self.limit: int = limit
        self.by_gen: bool = by_gen
        self.ADJUSTABLE_CHUNK_SIZE = 1000

    # Main functions - methods to read data
    def read_df_from_seaborn(self) -> None:
        if self.df_name is not None:
            if self.df_name in seaborn_libraries:
                match self.structure_method:
                    case read_by.NORMAL:
                        self.dataset = self.normal_reader()   # NON-GEN
                    case read_by.COLUMNS:
                        self.dataset = self.column_reader()   # NON-GEN
                    case read_by.ROWS:
                        if self.by_gen:
                            self.dataset = self.rows_reader_by_gen()      # GEN
                        else:
                            self.dataset = self.rows_reader()             # NON-GEN
                    case read_by.TUPLES:
                        if self.by_gen:
                            self.dataset = self.tuples_reader_by_gen()    # GEN
                        else:
                            self.dataset = self.tuples_reader()           # NON-GEN 
                    case read_by.CHUNKS:
                        if self.by_gen:
                            self.dataset = self.chunks_reader_by_gen()    # GEN
                        else:
                            self.dataset = self.chunks_reader()           # NON-GEN
                    case _:
                        raise Exception("You chose the wrong enumerator!")
            else:
                raise Exception("There is no dataframe in the Seaborn package with this self.df_name!")
        else:
            raise Exception("Your dataframe name is wrong!")


    # Structured smaller functions - to support major functionalities
    def normal_reader(self) -> pd.DataFrame:
        match self.location_method:
            case read_from.TOP:
                return sns.load_dataset(self.df_name).head(self.limit)      
            case read_from.BOTTOM:
                return sns.load_dataset(self.df_name).tail(self.limit) 
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    return sns.load_dataset(self.df_name).sample(self.limit) 
                else:
                    return sns.load_dataset(self.df_name).sample()
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

    def column_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()
        match self.location_method:
            case read_from.TOP:
                for col_name, data in sns.load_dataset(self.df_name).head(self.limit).items():
                    result_df[col_name] = data
            case read_from.BOTTOM:
                for col_name, data in sns.load_dataset(self.df_name).tail(self.limit).items():
                    result_df[col_name] = data
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    for col_name, data in sns.load_dataset(self.df_name).sample(self.limit).items():
                        result_df[col_name] = data
                else:
                    for col_name, data in sns.load_dataset(self.df_name).sample().items():
                        result_df[col_name] = data
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
        return result_df

    def rows_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP:
                for _, row in sns.load_dataset(self.df_name).head(self.limit).iterrows():
                    yield row
            case read_from.BOTTOM:
                for _, row in sns.load_dataset(self.df_name).tail(self.limit).iterrows():
                    yield row
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    for _, row in sns.load_dataset(self.df_name).sample(self.limit).iterrows():
                        yield row
                else:
                    for _, row in sns.load_dataset(self.df_name).sample().iterrows():
                        yield row
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
    def rows_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()
        
        match self.location_method:
            case read_from.TOP:
                for row_index, row in sns.load_dataset(self.df_name).head(self.limit).iterrows():
                    result_df[row_index] = row
            case read_from.BOTTOM:
                for row_index, row in sns.load_dataset(self.df_name).tail(self.limit).iterrows():
                    result_df[row_index] = row
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    for row_index, row in sns.load_dataset(self.df_name).sample(self.limit).iterrows():
                        result_df[row_index] = row
                else:
                    for row_index, row in sns.load_dataset(self.df_name).sample().iterrows():
                        result_df[row_index] = row
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
        result_df = result_df.transpose() 
        return result_df  
        
    def tuples_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP:
                yield tuple(sns.load_dataset(self.df_name).columns)
                for single_tuple in sns.load_dataset(self.df_name).head(self.limit).itertuples(index=False):
                    yield single_tuple
            case read_from.BOTTOM:
                yield tuple(sns.load_dataset(self.df_name).columns)
                for single_tuple in sns.load_dataset(self.df_name).tail(self.limit).itertuples(index=False):
                    yield single_tuple
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    yield tuple(sns.load_dataset(self.df_name).columns)
                    for single_tuple in sns.load_dataset(self.df_name).sample(self.limit).itertuples(index=False):
                        yield single_tuple
                else:
                    yield tuple(sns.load_dataset(self.df_name).columns)
                    for single_tuple in sns.load_dataset(self.df_name).sample().itertuples(index=False):
                        yield single_tuple
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")

    def tuples_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()

        match self.location_method:
            case read_from.TOP:
                result_df  = sns.load_dataset(self.df_name).head(self.limit).itertuples(index=False)
            case read_from.BOTTOM:
                result_df = sns.load_dataset(self.df_name).tail(self.limit).itertuples(index=False)
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    result_df = sns.load_dataset(self.df_name).sample(self.limit).itertuples(index=False)
                else:
                    result_df = sns.load_dataset(self.df_name).sample().itertuples(index=False)
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
                
        return pd.DataFrame(result_df)

    def chunks_reader_by_gen(self) -> GeneratorType:
        match self.location_method:
            case read_from.TOP:
                for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).head(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    yield partial_result_df
            case read_from.BOTTOM:
                for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).tail(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    yield partial_result_df
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).sample(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                        yield partial_result_df
                else:
                    for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).sample(), self.ADJUSTABLE_CHUNK_SIZE):
                        yield partial_result_df
            case _:
                raise Exception("You did not specified correct 'read_from' enumerator value!")
            
    def chunks_reader(self) -> pd.DataFrame:
        result_df = pd.DataFrame()
        
        match self.location_method:
            case read_from.TOP:
                for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).head(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
            case read_from.BOTTOM:
                for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).tail(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                    result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
            case read_from.RANDOM:
                if self.limit < len(sns.load_dataset(self.df_name)):
                    for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).sample(self.limit), self.ADJUSTABLE_CHUNK_SIZE):
                        result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
                else:
                    for partial_result_df in self.dataframe_chunk_generator(sns.load_dataset(self.df_name).sample(), self.ADJUSTABLE_CHUNK_SIZE):
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
