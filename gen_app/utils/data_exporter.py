# TODO: TEST ALL EXPORTS FROM ALL FORMATS & REPAIR THEM (BUT FIRSTLY REFACTOR DATA READER TO USE OF GENERATORS)
# TODO: REFACTOR ALL GENERATED_FROM WHERE I NEED
import sys, os
import pandas as pd

import csv
import json
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, PageBreak

from datetime import date, datetime
from typing import Union, Any
from types import GeneratorType

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from variables.lists import value_separator, row_separator, PAGE_SIZE, PAGE_WIDTH, MARGIN
from utils.pandas_extension import gen_to_df

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_path = "files"
files_path = os.path.join(os.path.dirname(project_path), relative_path)

class DataExporter(object):
    def __init__(self, dataset: Union[pd.DataFrame, GeneratorType], file_name: str):
        self.dataset: Union[pd.DataFrame, GeneratorType] = dataset
        self.file_name: str = file_name

    def export_to_txt(self) -> None:
        full_path = self.filepath_creator("txt")

        with open(full_path, "w") as Txt:
            if type(self.dataset) == pd.DataFrame:
                Txt.write(value_separator.join(map(str, self.dataset.columns)) + row_separator + "\n")
                for _, row in self.dataset.iterrows():
                    row_str = value_separator.join(map(str, row))
                    Txt.write(row_str + row_separator + "\n")
            elif type(self.dataset) == GeneratorType:
                checked_the_generator = False
                columns_displayed = False
                for row in self.dataset:
                    if not checked_the_generator:
                        GENERATED_FROM = self.generator_checker(row)
                        checked_the_generator = True

                    if not columns_displayed:
                        match GENERATED_FROM:
                            case "TUPLE_GENERATOR":
                                column_names = row
                            case "CHUNK_GENERATOR":
                                column_names = row.columns
                            case "OTHER_GENERATOR":
                                column_names = row.keys()
                            case _:
                                raise Exception("The dataset could NOT be exported!")
                            
                        column_str = value_separator.join(map(str, column_names))
                        Txt.write(column_str + row_separator + "\n")
                        columns_displayed = True
                        if GENERATED_FROM == "TUPLE_GENERATOR": 
                            continue

                    if GENERATED_FROM == "CHUNK_GENERATOR":
                        for _, single_row in row.iterrows():
                            row_str = value_separator.join(map(str, single_row))
                            Txt.write(row_str + row_separator + "\n")
                    else:
                        row_str = value_separator.join(map(str, row))
                        Txt.write(row_str + row_separator + "\n")
            else:
                raise Exception("Unwanted input data types.")
        
    def export_to_json(self) -> None:
        full_path = self.filepath_creator("json")
        
        with open(full_path, "w") as Json:
            if type(self.dataset) == pd.DataFrame:
                df = self.dataset.to_json(orient="records", lines=True)
                Json.write(df)
            elif type(self.dataset) == GeneratorType:
                checked_the_generator = False
                checked_the_column_names = False
                for row in self.dataset:
                    if not checked_the_generator:
                        GENERATED_FROM = self.generator_checker(row)
                        checked_the_generator = True

                    match GENERATED_FROM:
                        case "TUPLE_GENERATOR":
                            if not checked_the_column_names:
                                column_names = list(row)
                                checked_the_column_names = True
                                continue
                            row_to_save = pd.DataFrame([row], columns=column_names).to_json(orient="records", lines=True)
                        case "CHUNK_GENERATOR":
                            row_to_save = row.to_json(orient="records", lines=True)
                        case "OTHER_GENERATOR":
                            row_to_save = json.dumps(row.to_dict()) + "\n"
                        case _:
                            raise Exception("The dataset could NOT be exported!")
                        
                    Json.write(row_to_save)
            else:
                raise Exception("Unwanted input data types.")
            
    def export_to_csv(self) -> None:
        full_path = self.filepath_creator("csv")
        
        with open(full_path, "w", newline="") as Csv:
            if type(self.dataset) == pd.DataFrame:
                self.dataset.to_csv(Csv, index=False, sep=value_separator, header=True)
            elif type(self.dataset) == GeneratorType:
                checked_the_generator = False
                checked_the_column_names = False

                csv_writer = csv.writer(Csv, delimiter=value_separator)
                for row in self.dataset:
                    if not checked_the_generator:
                        GENERATED_FROM = self.generator_checker(row)
                        checked_the_generator = True

                    match GENERATED_FROM:
                        case "TUPLE_GENERATOR":
                            if not checked_the_column_names:
                                csv_writer.writerow(list(row))
                                checked_the_column_names = True
                                continue
                        case "CHUNK_GENERATOR":
                            if not checked_the_column_names:
                                csv_writer.writerow(list(row.columns))
                                checked_the_column_names = True
                        case "OTHER_GENERATOR":
                            if not checked_the_column_names:
                                csv_writer.writerow(row.keys())
                                checked_the_column_names = True
                        case _:
                            raise Exception("The dataset could NOT be exported!")
                        
                    if GENERATED_FROM == "CHUNK_GENERATOR":
                        for _, single_row in row.iterrows():
                            csv_writer.writerow(single_row)
                    else:
                        csv_writer.writerow(row)
            else:
                raise Exception("Unwanted input data types.")

    def export_to_xlsx(self) -> None:
        full_path = self.filepath_creator("xlsx")

        if type(self.dataset) == pd.DataFrame:
            self.dataset.to_excel(full_path, index=False, header=True)
        elif type(self.dataset) == GeneratorType:
            checked_the_generator = False
            checked_the_column_names = False

            excelFile = openpyxl.Workbook()
            excelSheet = excelFile.active
            for row in self.dataset:
                if not checked_the_generator:
                    GENERATED_FROM = self.generator_checker(row)
                    checked_the_generator = True

                match GENERATED_FROM:
                    case "TUPLE_GENERATOR":
                        if not checked_the_column_names:
                            excelSheet.append(list(row))
                            checked_the_column_names = True
                            continue
                        row_to_save = row
                    case "CHUNK_GENERATOR":
                        if not checked_the_column_names:
                            excelSheet.append(list(row.columns))
                            checked_the_column_names = True
                        rows_to_save = row
                    case "OTHER_GENERATOR":
                        if not checked_the_column_names:
                            excelSheet.append(row.keys().tolist())
                            checked_the_column_names = True
                        row_to_save = row.tolist()
                    case _:
                        raise Exception("The dataset could NOT be exported!")
                    
                if GENERATED_FROM == "CHUNK_GENERATOR":
                    for _, single_row in rows_to_save.iterrows():
                        excelSheet.append(list(single_row))
                else:
                    excelSheet.append(row_to_save)

            excelFile.save(full_path)
        else:
            raise Exception("Unwanted input data types.")
            
    def export_to_pdf(self) -> None: # Without generator :(
        full_path = self.filepath_creator("pdf")
        pdfFile = SimpleDocTemplate(full_path, pagesize=PAGE_SIZE)
        if type(self.dataset) == GeneratorType:
            row = next(self.dataset)
            GENERATED_FROM = self.generator_checker(row)
            match GENERATED_FROM:
                case "TUPLE_GENERATOR":
                    self.dataset = pd.DataFrame(pd.DataFrame(self.dataset), columns=row)
                case "CHUNK_GENERATOR":
                    self.dataset = pd.concat([row, gen_to_df(self.dataset)])
                case "OTHER_GENERATOR": # Works for row
                    self.dataset = pd.concat([pd.DataFrame([row]), pd.DataFrame(self.dataset)])

        if type(self.dataset) == pd.DataFrame:
            max_column_width = (PAGE_WIDTH - 2*MARGIN)

            pages = []
            elements = []
            current_page_data = []
            current_page_width = 0

            for col in self.dataset.columns:
                col_width = max(self.dataset[col].astype(str).apply(len))+15
                if current_page_width + col_width <= max_column_width:
                    current_page_data.append(self.dataset[col])
                    current_page_width += col_width
                else: 
                    pages.append(current_page_data)
                    current_page_data = [self.dataset[col]]
                    current_page_width = col_width
            
            pages.append(current_page_data)

            for page in pages:
                df = pd.concat(page, axis=1)
                table = Table([df.columns.tolist()] + df.values.tolist())

                if page != pages[-1]:
                    elements.append(table)
                    elements.append(PageBreak())
                else:
                    elements.append(table)
                
            pdfFile.build(elements)
        else:
            raise Exception("Unwanted input data types.")

    def filepath_creator(self, extension: str) -> str:
        todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
        file_name = todays_date + "_" + self.file_name + "." + extension
        full_path = os.path.join(files_path, file_name)

        return full_path

    def generator_checker(self, row: Union[tuple, pd.DataFrame, Any]) -> str:
        GENERATED_FROM = "OTHER_GENERATOR"
        if type(row) == tuple: # If first row is tuple then it is Tuple GEN
            GENERATED_FROM = "TUPLE_GENERATOR"
        elif type(row) == pd.DataFrame: # If first "row" is dataframe then it is Chunk GEN
            GENERATED_FROM = "CHUNK_GENERATOR"
        return GENERATED_FROM