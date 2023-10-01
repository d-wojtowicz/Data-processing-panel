import csv

import seaborn as sns
import pandas as pd

from variables.enumerators import *
from variables.lists import *

# Main functions - methods to read data
def read_df_from_seaborn(dfName: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000) -> pd.DataFrame:
    result_df = pd.DataFrame()
    
    if dfName is not None:
        if dfName in seaborn_libraries:
            match structure_method:
                case read_by.NORMAL:
                    result_df = normal_reader(dfName, location_method, limit)
                case read_by.COLUMNS:
                    result_df = column_reader(dfName, location_method, limit)
                case read_by.ROWS:
                    result_df = rows_reader(dfName, location_method, limit)
                case read_by.TUPLES:
                    result_df = tuples_reader(dfName, location_method, limit)
                case read_by.CHUNKS:
                    result_df = chunks_reader(dfName, location_method, limit, ADJUSTABLE_CHUNK_SIZE=1000)
                case _:
                    raise Exception("You chose the wrong enumerator!")
        else:
            raise Exception("There is no dataframe in the Seaborn package with this dfName!")
    else:
        raise Exception("Your dataframe name is wrong!")

    return result_df

def read_from_csv(file_name: str, number_of_rows: int) -> pd.DataFrame:
    for chunk in pd.read_csv(file_name, chunksize=number_of_rows):
        yield chunk



# Structured smaller functions - to support major functionalities
def normal_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            result_df = sns.load_dataset(dfName).head(limit)      
        case read_from.BOTTOM:
            result_df = sns.load_dataset(dfName).tail(limit) 
        case read_from.RANDOM:
            result_df = sns.load_dataset(dfName).sample(limit) 
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

    return result_df

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

def rows_reader(dfName: str, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            for row_index, data in sns.load_dataset(dfName).head(limit).iterrows():
                result_df[row_index] = data
        case read_from.BOTTOM:
            for row_index, data in sns.load_dataset(dfName).tail(limit).iterrows():
                result_df[row_index] = data
        case read_from.RANDOM:
            for row_index, data in sns.load_dataset(dfName).sample(limit).iterrows():
                result_df[row_index] = data
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

    result_df = result_df.transpose() 
    return result_df
            
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