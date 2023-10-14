# TODO: TEST ALL EXPORTS FROM ALL FORMATS & REPAIR THEM (BUT FIRSTLY REFACTOR DATA READER TO USE OF GENERATORS)
# TODO: REFACTOR ALL GENERATED_FROM WHERE I NEED

import os
import pandas as pd

import csv
import json
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, PageBreak

from datetime import date, datetime
from typing import Union
from types import GeneratorType
from variables.lists import value_separator, row_separator, PAGE_SIZE, PAGE_WIDTH, MARGIN

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
relative_path = "files"
files_path = os.path.join(project_path, relative_path)

def export_to_txt(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    full_path = filepath_creator(file_name, "txt")

    with open(full_path, "w") as Txt:
        if type(dataset) == pd.DataFrame:
            Txt.write(value_separator.join(map(str, dataset.columns)) + row_separator + "\n")
            for _, row in dataset.iterrows():
                row_str = value_separator.join(map(str, row))
                Txt.write(row_str + row_separator + "\n")
        elif type(dataset) == GeneratorType:
            columns_displayed = False
            for row in dataset:
                if not columns_displayed:
                    if type(row) == tuple: # If first row is tuple then it is Tuple GEN
                        column_names = row
                    else:
                        column_names = row.keys()
                        
                    column_str = value_separator.join(map(str, column_names))
                    Txt.write(column_str + row_separator + "\n")
                    columns_displayed = True
                    if type(row) == tuple: 
                        continue
                
                row_str = value_separator.join(map(str, row))
                Txt.write(row_str + row_separator + "\n")
        else:
            raise Exception("Unwanted input data types.")
    
def export_to_json(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    full_path = filepath_creator(file_name, "json")
    
    with open(full_path, "w") as Json:
        if type(dataset) == pd.DataFrame:
            df = dataset.to_json(orient="records", lines=True)
            Json.write(df)
        elif type(dataset) == GeneratorType:
            checked_the_generator = False
            checked_the_column_names = False
            for row in dataset:
                if not checked_the_generator:
                    GENERATED_FROM = generator_checker(row)
                    checked_the_generator = True

                match GENERATED_FROM:
                    case "TUPLE_GENERATOR":
                        if not checked_the_column_names:
                            column_names = list(row)
                            checked_the_column_names = True
                            continue
                        row_to_save = pd.DataFrame([row], columns=column_names).to_json(orient="records", lines=True)
                    case "OTHER_GENERATOR":
                        row_to_save = json.dumps(row.to_dict()) + "\n"
                    case _:
                        raise Exception("The dataset could NOT be exported!")
                    
                Json.write(row_to_save)
        else:
            raise Exception("Unwanted input data types.")
        
def export_to_csv(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    full_path = filepath_creator(file_name, "csv")
    
    with open(full_path, "w", newline="") as Csv:
        if type(dataset) == pd.DataFrame:
            dataset.to_csv(Csv, index=False, sep=value_separator, header=True)
        elif type(dataset) == GeneratorType:
            checked_the_generator = False
            checked_the_column_names = False

            csv_writer = csv.writer(Csv, delimiter=value_separator)
            for row in dataset:
                if not checked_the_generator:
                    GENERATED_FROM = generator_checker(row)
                    checked_the_generator = True

                match GENERATED_FROM:
                    case "TUPLE_GENERATOR":
                        if not checked_the_column_names:
                            csv_writer.writerow(list(row))
                            checked_the_column_names = True
                            continue
                    case "OTHER_GENERATOR":
                        if not checked_the_column_names:
                            csv_writer.writerow(row.keys())
                            checked_the_column_names = True
                    case _:
                        raise Exception("The dataset could NOT be exported!")
                    
                csv_writer.writerow(row)
        else:
            raise Exception("Unwanted input data types.")

def export_to_xlsx(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None:
    full_path = filepath_creator(file_name, "xlsx")

    if type(dataset) == pd.DataFrame:
        dataset.to_excel(full_path, index=False, header=True)
    elif type(dataset) == GeneratorType:
        checked_the_generator = False
        checked_the_column_names = False

        excelFile = openpyxl.Workbook()
        excelSheet = excelFile.active
        for row in dataset:
            if not checked_the_generator:
                GENERATED_FROM = generator_checker(row)
                checked_the_generator = True

            match GENERATED_FROM:
                case "TUPLE_GENERATOR":
                    if not checked_the_column_names:
                        excelSheet.append(list(row))
                        checked_the_column_names = True
                        continue
                    row_to_save = row
                case "OTHER_GENERATOR":
                    if not checked_the_column_names:
                        excelSheet.append(row.keys().tolist())
                        checked_the_column_names = True
                    row_to_save = row.tolist()
                case _:
                    raise Exception("The dataset could NOT be exported!")
                
            excelSheet.append(row_to_save)

        excelFile.save(full_path)
    else:
        raise Exception("Unwanted input data types.")
        
def export_to_pdf(dataset: Union[pd.DataFrame, GeneratorType], file_name: str) -> None: # Without generator :(
    full_path = filepath_creator(file_name, "pdf")
    pdfFile = SimpleDocTemplate(full_path, pagesize=PAGE_SIZE)
    if type(dataset) == GeneratorType:
        row = next(dataset)
        GENERATED_FROM = generator_checker(row)
        match GENERATED_FROM:
            case "TUPLE_GENERATOR":
                dataset = pd.DataFrame(pd.DataFrame(dataset), columns=row)
            case "OTHER_GENERATOR": # Works for row
                dataset = pd.concat([pd.DataFrame([row]), pd.DataFrame(dataset)])

    if type(dataset) == pd.DataFrame:
        max_column_width = (PAGE_WIDTH - 2*MARGIN)

        pages = []
        elements = []
        current_page_data = []
        current_page_width = 0

        for col in dataset.columns:
            col_width = max(dataset[col].astype(str).apply(len))+15
            if current_page_width + col_width <= max_column_width:
                current_page_data.append(dataset[col])
                current_page_width += col_width
            else: 
                pages.append(current_page_data)
                current_page_data = [dataset[col]]
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

def filepath_creator(file_name: str, extension: str) -> str:
    todays_date = str(datetime.now().strftime("%d%m%Y_%H%M%S"))
    file_name = todays_date + "_" + file_name + "." + extension
    full_path = os.path.join(files_path, file_name)

    return full_path

def generator_checker(row) -> str:
    GENERATED_FROM = "OTHER_GENERATOR"
    if type(row) == tuple: # If first row is tuple then it is Tuple GEN
        GENERATED_FROM = "TUPLE_GENERATOR"
    return GENERATED_FROM