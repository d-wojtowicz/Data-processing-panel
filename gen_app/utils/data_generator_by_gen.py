import sys, os
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from random import randint, choice
from variables.lists import data_types, letters

class DataGenerator(object):
    def __init__(self, number_of_cols: int, number_of_records: int):
        self.number_of_cols: int = number_of_cols
        self.number_of_records: int = number_of_records

    def generate_dataframe_by_gen(self):
        def generate_dataframe_generator() -> pd.DataFrame:
            col_names = ["Column" + str(i+1) for i in range(self.number_of_cols)]
            col_types = [choice(data_types) for _ in range(self.number_of_cols)]
            col_dict = dict(zip(col_names, col_types))

            for _ in range(self.number_of_records):
                row_data = {col_name: next(self.generate_column(1, col_type)) for col_name, col_type in col_dict.items()}
                yield pd.DataFrame(row_data, index=[0])

        return generate_dataframe_generator()

    def generate_column(self, number_of_records: int, data_type: str):
        if data_type == "number":
            yield from self.generate_number_column(1, 100, number_of_records)
        elif data_type == "text":
            yield from self.generate_text_column(5, 10, number_of_records)
        elif data_type == "char":
            yield from self.generate_char_column(number_of_records)


    def generate_number_column(self, min_value: int, max_value: int, number_of_records: int):
        for _ in range(number_of_records):
            yield randint(min_value, max_value)

    def generate_text_column(self, min_length: int, max_length: int, number_of_records: int):
        for _ in range(number_of_records):
            yield "".join(self.generate_text_to_single_record(min_length,max_length))

    def generate_char_column(self, number_of_records: int):
        for _ in range(number_of_records):
            yield chr(randint(65,90))


    def generate_text_to_single_record(self, min_length: int, max_length: int):
        for _ in range(randint(min_length, max_length)):
            yield choice(letters)