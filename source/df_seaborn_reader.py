# TODO: TEST LIMITS IN THE READING (e.g. limit=1000 & number of records in df=999) AND REFACTOR
# TODO: WRITE SKLEARN READER LIKE THIS ONE
# TODO: WRITE CHUNK_READER & CHUNK_READER_BY_GEN

import csv

import seaborn as sns
import pandas as pd
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *

# Main functions - methods to read data
def read_df_from_seaborn(dfName: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True) -> pd.DataFrame:
    result_df = pd.DataFrame()
    if dfName is not None:
        if dfName in seaborn_libraries:
            match structure_method:
                case read_by.NORMAL:
                    result_df = normal_reader(dfName, location_method, limit)   # NON-GEN
                case read_by.COLUMNS:
                    result_df = column_reader(dfName, location_method, limit)   # NON-GEN
                case read_by.ROWS:
                    if by_gen:
                        result_df = rows_reader_by_gen(dfName, location_method, limit)      # GEN
                    else:
                        result_df = rows_reader(dfName, location_method, limit)             # NON-GEN
                case read_by.TUPLES:
                    if by_gen:
                        result_df = tuples_reader_by_gen(dfName, location_method, limit)    # GEN
                    else:
                        result_df = tuples_reader(dfName, location_method, limit)           # NON-GEN 
                case read_by.CHUNKS:
                    if by_gen:
                        result_df = chunks_reader_by_gen(dfName, location_method, limit, ADJUSTABLE_CHUNK_SIZE=10)   # GEN
                    else:
                        result_df = chunks_reader(dfName, location_method, limit, ADJUSTABLE_CHUNK_SIZE=10)   # NON-GEN
                case _:
                    raise Exception("You chose the wrong enumerator!")
        else:
            raise Exception("There is no dataframe in the Seaborn package with this dfName!")
    else:
        raise Exception("Your dataframe name is wrong!")
    
    return result_df


# Structured smaller functions - to support major functionalities
def normal_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    match location_method:
        case read_from.TOP:
            return sns.load_dataset(dfName).head(limit)      
        case read_from.BOTTOM:
            return sns.load_dataset(dfName).tail(limit) 
        case read_from.RANDOM:
            return sns.load_dataset(dfName).sample(limit) 
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

def column_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()
    match location_method:
        case read_from.TOP:
            for col_name, data in sns.load_dataset(dfName).head(limit).items():
                result_df[col_name] = data
        case read_from.BOTTOM:
            for col_name, data in sns.load_dataset(dfName).tail(limit).items():
                result_df[col_name] = data
        case read_from.RANDOM:
            for col_name, data in sns.load_dataset(dfName).sample(limit).items():
                result_df[col_name] = data
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
    return result_df

def rows_reader_by_gen(dfName: str, location_method: Enum, limit: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            for _, row in sns.load_dataset(dfName).head(limit).iterrows():
                yield row
        case read_from.BOTTOM:
            for _, row in sns.load_dataset(dfName).tail(limit).iterrows():
                yield row
        case read_from.RANDOM:
            for _, row in sns.load_dataset(dfName).sample(limit).iterrows():
                yield row
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
def rows_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()
    
    match location_method:
        case read_from.TOP:
            for row_index, row in sns.load_dataset(dfName).head(limit).iterrows():
                result_df[row_index] = row
        case read_from.BOTTOM:
            for row_index, row in sns.load_dataset(dfName).tail(limit).iterrows():
                result_df[row_index] = row
        case read_from.RANDOM:
            for row_index, row in sns.load_dataset(dfName).sample(limit).iterrows():
                result_df[row_index] = row
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
    result_df = result_df.transpose() 
    return result_df  
    
def tuples_reader_by_gen(dfName: str, location_method: Enum, limit: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            yield tuple(sns.load_dataset(dfName).columns)
            for single_tuple in sns.load_dataset(dfName).head(limit).itertuples(index=False):
                yield single_tuple
        case read_from.BOTTOM:
            yield tuple(sns.load_dataset(dfName).columns)
            for single_tuple in sns.load_dataset(dfName).tail(limit).itertuples(index=False):
                yield single_tuple
        case read_from.RANDOM:
            yield tuple(sns.load_dataset(dfName).columns)
            for single_tuple in sns.load_dataset(dfName).sample(limit).itertuples(index=False):
                yield single_tuple
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

def tuples_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            result_df  = sns.load_dataset(dfName).head(limit).itertuples(index=False)
        case read_from.BOTTOM:
            result_df = sns.load_dataset(dfName).tail(limit).itertuples(index=False)
        case read_from.RANDOM:
            result_df = sns.load_dataset(dfName).sample(limit).itertuples(index=False)
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
            
    return pd.DataFrame(result_df)

def chunks_reader_by_gen(dfName: str, location_method: Enum, limit: int, ADJUSTABLE_CHUNK_SIZE: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).head(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case read_from.BOTTOM:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).tail(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case read_from.RANDOM:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).sample(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
def chunks_reader(dfName: str, location_method: Enum, limit: int, ADJUSTABLE_CHUNK_SIZE: int) -> pd.DataFrame:
    result_df = pd.DataFrame()
    
    match location_method:
        case read_from.TOP:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).head(limit), ADJUSTABLE_CHUNK_SIZE):
                result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
        case read_from.BOTTOM:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).tail(limit), ADJUSTABLE_CHUNK_SIZE):
                result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
        case read_from.RANDOM:
            for partial_result_df in dataframe_chunk_generator(sns.load_dataset(dfName).sample(limit), ADJUSTABLE_CHUNK_SIZE):
                result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

    return result_df

def dataframe_chunk_generator(df: pd.DataFrame, chunk_size: int) -> pd.DataFrame:
    num_of_chunks = len(df) // chunk_size + 1
    for chunk_id in range(num_of_chunks):
        from_id = chunk_id * chunk_size
        to_id = (chunk_id + 1) * chunk_size
        chunk_value = df[from_id:to_id]
        if not chunk_value.empty:
            yield chunk_value