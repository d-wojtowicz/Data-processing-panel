import csv

from sklearn.datasets import load_iris, load_digits, load_wine, load_diabetes, load_breast_cancer
import pandas as pd
from types import GeneratorType

from variables.enumerators import *
from variables.lists import *

# Main functions - methods to read data
def read_df_from_sklearn(dfName: str, location_method: Enum = read_from.TOP, structure_method: Enum = read_by.NORMAL, limit: int = 1000, by_gen: bool = True) -> pd.DataFrame:
    result_df = pd.DataFrame()
    
    if dfName is not None:
        if dfName in sklearn_libraries:
            sklearn_df = read_full_df_by_name(dfName)
            match structure_method:
                case read_by.NORMAL:
                    result_df = normal_reader(sklearn_df, location_method, limit)
                case read_by.COLUMNS:
                    result_df = column_reader(sklearn_df, location_method, limit)
                case read_by.ROWS:
                    if by_gen:
                        result_df = rows_reader_by_gen(sklearn_df, location_method, limit)
                    else:
                        result_df = rows_reader(sklearn_df, location_method, limit)
                case read_by.TUPLES:
                    if by_gen:
                        result_df = tuples_reader_by_gen(sklearn_df, location_method, limit)
                    else:
                        result_df = tuples_reader(sklearn_df, location_method, limit)
                case read_by.CHUNKS:
                    if by_gen:
                        result_df = chunks_reader_by_gen(sklearn_df, location_method, limit, ADJUSTABLE_CHUNK_SIZE=1000)
                    else:
                        result_df = chunks_reader(sklearn_df, location_method, limit, ADJUSTABLE_CHUNK_SIZE=1000)
                case _:
                    raise Exception("You chose the wrong enumerator!")
        else:
            raise Exception("There is no dataframe in the Sklearn package with this dfName!")
    else:
        raise Exception("Your dataframe name is wrong!")

    return result_df


# Structured smaller functions - to support major functionalities
def read_full_df_by_name(dfName: str) -> pd.DataFrame:
    match dfName:
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
            raise Exception("There is no dataframe in the Sklearn package with this dfName!")
    
    result_df = pd.DataFrame(data=sklearn_df.data, columns=sklearn_df.feature_names)
    return result_df

def normal_reader(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            result_df = sklearn_df.head(limit)      
        case read_from.BOTTOM:
            result_df = sklearn_df.tail(limit) 
        case read_from.RANDOM:
            result_df = sklearn_df.sample(limit) 
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

    return result_df

def column_reader(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            for col_name, data in sklearn_df.head(limit).items():
                result_df[col_name] = data
        case read_from.BOTTOM:
            for col_name, data in sklearn_df.tail(limit).items():
                result_df[col_name] = data
        case read_from.RANDOM:
            for col_name, data in sklearn_df.sample(limit).items():
                result_df[col_name] = data
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
    return result_df

def rows_reader_by_gen(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            for _, row in sklearn_df.head(limit).iterrows():
                yield row
        case read_from.BOTTOM:
            for _, row in sklearn_df.tail(limit).iterrows():
                yield row
        case read_from.RANDOM:
            for _, row in sklearn_df.sample(limit).iterrows():
                yield row
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

def rows_reader(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            for row_index, row in sklearn_df.head(limit).iterrows():
                result_df[row_index] = row
        case read_from.BOTTOM:
            for row_index, row in sklearn_df.tail(limit).iterrows():
                result_df[row_index] = row
        case read_from.RANDOM:
            for row_index, row in sklearn_df.sample(limit).iterrows():
                result_df[row_index] = row
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")

    result_df = result_df.transpose() 
    return result_df

def tuples_reader_by_gen(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            yield tuple(sklearn_df.columns)
            for single_tuple in sklearn_df.head(limit).itertuples(index=False):
                yield single_tuple
        case read_from.BOTTOM:
            yield tuple(sklearn_df.columns)
            for single_tuple in sklearn_df.tail(limit).itertuples(index=False):
                yield single_tuple
        case read_from.RANDOM:
            yield tuple(sklearn_df.columns)
            for single_tuple in sklearn_df.sample(limit).itertuples(index=False):
                yield single_tuple
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
     
def tuples_reader(sklearn_df: pd.DataFrame, location_method: Enum, limit: int) -> pd.DataFrame:
    result_df = pd.DataFrame()

    match location_method:
        case read_from.TOP:
            result_df  = sklearn_df.head(limit).itertuples(index=False)
        case read_from.BOTTOM:
            result_df = sklearn_df.tail(limit).itertuples(index=False)
        case read_from.RANDOM:
            result_df = sklearn_df.sample(limit).itertuples(index=False)
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
            
    return pd.DataFrame(result_df)

def chunks_reader_by_gen(sklearn_df: pd.DataFrame, location_method: Enum, limit: int, ADJUSTABLE_CHUNK_SIZE: int) -> GeneratorType:
    match location_method:
        case read_from.TOP:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.head(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case read_from.BOTTOM:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.tail(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case read_from.RANDOM:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.sample(limit), ADJUSTABLE_CHUNK_SIZE):
                yield partial_result_df
        case _:
            raise Exception("You did not specified correct 'read_from' enumerator value!")
        
def chunks_reader(sklearn_df: pd.DataFrame, location_method: Enum, limit: int, ADJUSTABLE_CHUNK_SIZE: int) -> pd.DataFrame:
    result_df = pd.DataFrame()
    
    match location_method:
        case read_from.TOP:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.head(limit), ADJUSTABLE_CHUNK_SIZE):
                result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
        case read_from.BOTTOM:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.tail(limit), ADJUSTABLE_CHUNK_SIZE):
                result_df = pd.concat([result_df, partial_result_df], ignore_index=True)
        case read_from.RANDOM:
            for partial_result_df in dataframe_chunk_generator(sklearn_df.sample(limit), ADJUSTABLE_CHUNK_SIZE):
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