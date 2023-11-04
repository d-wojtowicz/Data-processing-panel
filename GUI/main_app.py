# 0.
"""
                SEABORN     SKLEARN     GENERATED       INDIVIDUAL
NORMAL          OK
COLUMN          OK
ROWS            
ROWS_GEN
TUPLES
TUPLES_GEN
CHUNKS
CHUNKS_GEN



"""




#TODO: Fix tuples column names & chunk reader
#TODO: Add new filter ways
#TODO: Refactor returning of datareader to self.dataset not result
#TODO: Main_performance apply OOP changes

# 1.
#TODO: Add IndividualDF operations (input file, read)
#TODO: Check all methods of data reading for bug hunting
#TODO: DataFrame splitting by number of rows per page

# 2.
#TODO: Update result_box by three buttons displaying: Table, Statistical Analysis, Log
# Table: Interactive DataFrame with checking datatypes before applying changes
# Statistical Analysis: std, med, avg etc.
# Log: Measurements of all steps while data processing (save to file & output it)

# 3.
#TODO: Theme CSS
#TODO: Value_handler refactor!!!!!!!!

# 4.
#TODO: Requirements UPDATE!!!
#TODO: Overall refactor
#TODO: Facade, response boilerplate & GUI & backend separately

#BUG: Random, w momencie jak limit > ilosc rekordow to wyswietla 1
#TODO: Add possibility of basing on the actual filtered dataset in the filtering panel (Not one the dataset from the fetching panel)

from enum import Enum
import sys, os

from types import GeneratorType
from typing import Union
import gradio as gr
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_app.source.data_reader import DataReader
from gen_app.utils.data_generator_by_gen import DataGenerator
from gen_app.utils.data_exporter import DataExporter
from gen_app.utils.pandas_extension import DataManager, gen_to_df, df_to_gen

from gen_app.variables.enumerators import read_by, read_from, reader_tester
from gen_app.variables.lists import seaborn_libraries, sklearn_libraries, comparision_marks, exports

generated_dataset = None
individual_dataset_path = None
dataManager = DataManager(pd.DataFrame())

def enum_handler(location_method: str, structure_method: str) -> (enumerate, enumerate):
    match location_method:
        case "Top":
            location_method = read_from.TOP
        case "Bottom":
            location_method = read_from.BOTTOM
        case "Random":
            location_method = read_from.RANDOM
        case _:
            """"""
    match structure_method:
        case "Normal":
            structure_method = read_by.NORMAL
        case "Columns":
            structure_method = read_by.COLUMNS
        case "Tuples": 
            structure_method = read_by.TUPLES
        case "Rows":
            structure_method = read_by.ROWS
        case "Chunks":
            structure_method = read_by.CHUNKS
        case _:
            """"""
    
    if location_method != "" and structure_method != "":
        return location_method, structure_method
    elif location_method == "" and structure_method != "":
        return structure_method
    else:
        return location_method

def value_handler(source_name: str, df_name: str, location_method: str, structure_method: str, row_count: int):
    location_method, structure_method = enum_handler(location_method, structure_method)

    dataset = None
    by_gen = True
    if source_name == "Generated":
        by_gen = False
        global generated_dataset
        dataset = pd.DataFrame(gen_to_df(generated_dataset))
    elif source_name == "Individual":
        global individual_dataset_path
        source_name = individual_dataset_path
        df_name = "Individual"
    
    dataReader = DataReader(df_name, source_name, location_method, structure_method, row_count, by_gen=by_gen, dataset_for_generated=dataset)
    result_df = dataReader.read_data()

    # Odpowiednie przetwarzanie
    if df_name == "Individual":
        if type(result_df) == GeneratorType:
            if source_name.endswith((".txt", ".csv", ".json")):
                result_df = gen_to_df(result_df)


    return pd.DataFrame(result_df)

def submit_source(source_name: str):
    match source_name:
        case "Seaborn":
            return {
                dataset_box: gr.Radio(label="Enter the dataset name: ", value=seaborn_libraries[0], choices=seaborn_libraries, visible=True),
                output_conf_col: gr.Column(visible=True),
                generated_dataset_col: gr.Column(visible=False),
                individual_dataset_col: gr.Column(visible=False),
                output_result_col: gr.Column(visible=False)
            }
        case "Sklearn":
            return {
                dataset_box: gr.Radio(label="Enter the dataset name: ", value=sklearn_libraries[0], choices=sklearn_libraries, visible=True),
                output_conf_col: gr.Column(visible=True),
                generated_dataset_col: gr.Column(visible=False),
                individual_dataset_col: gr.Column(visible=False),
                output_result_col: gr.Column(visible=False)
            }
        case "Generated":
            return {
                dataset_box: gr.Radio(label="Enter the dataset name: ", visible=False),
                output_conf_col: gr.Column(visible=False),
                generated_dataset_col: gr.Column(visible=True),
                individual_dataset_col: gr.Column(visible=False),
                output_result_col: gr.Column(visible=False)
            }
        case "Individual":
            return {
                dataset_box: gr.Radio(label="Enter the dataset name: ", visible=False),
                output_conf_col: gr.Column(visible=False),
                generated_dataset_col: gr.Column(visible=False),
                individual_dataset_col: gr.Column(visible=True),
                output_result_col: gr.Column(visible=False)
            }
        case _:
            return {error_box: gr.Textbox(value="Wrong data source selected!", visible=True)}
                
def submit_gen(col_number: int, row_number: int):
    try:
        dataGen = DataGenerator(int(col_number), int(row_number))

        global generated_dataset
        generated_dataset = dataGen.generate_dataframe_by_gen()
        return {
            gen_info_text: gr.Text("The dataset was successfully generated!", visible=True),
            output_conf_col: gr.Column(visible=True),
            output_result_col: gr.Column(visible=False),
            individual_dataset_col: gr.Column(visible=False)
        }
    except Exception as e:
        return {error_box: gr.Textbox(value=str(e), visible=True)}

def submit_file(file_reader):
    if file_reader is not None:
        global individual_dataset_path
        individual_dataset_path = file_reader.name
        return {
            dataset_box: gr.Radio(label="Enter the dataset name: ", visible=False),
            output_conf_col: gr.Column(visible=True),
            generated_dataset_col: gr.Column(visible=False),
            output_result_col: gr.Column(visible=False)
        }
    else:
        return {error_box: gr.Textbox(value="First you have to select the file!", visible=True)}

def submit_conf(source_name: str, df_name: str, location_method: str, structure_method: str, limit: str):
    if source_name == "Generated":
        df_name = "Generated"
    
    df = value_handler(source_name, df_name, location_method, structure_method, limit)
    return {
        output_result_col: gr.Column(visible=True),
        result_box: gr.DataFrame(label="Result: ", value=df, interactive=1)
    }

def submit_fetch(dataset: pd.DataFrame):
    try:
        return {filter_fields: gr.Dropdown(label="Select Field", value=dataset.columns[0], choices=dataset.columns.tolist())}
    except Exception as e:
        return {error_box: gr.Textbox(value=str(e), visible=True)}

def submit_filter(dataset: pd.DataFrame, filtered_dataset: pd.DataFrame, col_name: str, col_dtype: str, filter_value: Union[int, str, float], numeric_comparator: str, operate_on_filtered: bool=False):
    try:
        global dataManager
        if operate_on_filtered:
            dataManager = DataManager(filtered_dataset)
        else:
            dataManager = DataManager(dataset)
        
        filtered_dataset = pd.DataFrame()
        if col_dtype == "Str":
            filtered_dataset = dataManager.get_df_by_category(col_name, filter_value.split(","))
        elif col_dtype == "Int":
            filter_value = [int(elem) for elem in filter_value.split(",")]
            filtered_dataset = dataManager.get_df_by_numeric(col_name, filter_value, numeric_comparator)
        elif col_dtype == "Float":
            filter_value = [float(elem) for elem in filter_value.split(",")]
            filtered_dataset = dataManager.get_df_by_numeric(col_name, filter_value, numeric_comparator)

        if operate_on_filtered:
            return {
                filter_result: filtered_dataset, 
                source_selector: gr.Checkbox(label="Do you want to perform filtering on the following dataset?", visible=True),

                extractor_position: gr.Radio(label="Extract samples from: ", value=read_from.list()[0], choices=read_from.list(), visible=True),
                extractor_quantity: gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=len(filtered_dataset), visible=True),
                submit_sampling_btn: gr.Button("Extract slice of samples", visible=True),

                export_info: gr.Text("The dataset was successfully filtered. Select the file format of dataset export: ", visible=True),
                export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=exports[0], choices=exports, visible=True),
                submit_export_btn: gr.Button("Export Filtered Dataset", visible=True)
            }
        else:
            return {
                filter_result: filtered_dataset, 
                source_selector: gr.Checkbox(label="Do you want to perform filtering on the following dataset?", visible=True),

                export_info: gr.Text("The dataset was successfully filtered. Select the file format of dataset export: ", visible=True),
                export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=exports[0], choices=exports, visible=True),
                submit_export_btn: gr.Button("Export Filtered Dataset", visible=True)
            }
            
    except Exception as e:
        return {error_box: gr.Textbox(value=str(e), visible=True)}

def submit_sample(dataset: pd.DataFrame, read_from: Enum, number_of_records: int) -> pd.DataFrame:
    try:
        global dataManager
        dataManager = DataManager(dataset)
        read_from = enum_handler(location_method=read_from, structure_method="")
        filtered_dataset = dataManager.get_df_by_limit(int(number_of_records), read_from)
        return {
            filter_result: filtered_dataset,
            extractor_quantity: gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=len(filtered_dataset), visible=True)
        }
    except Exception as e:
        return {error_box: gr.Textbox(value=str(e), visible=True)}

def submit_export(filtered_dataset: pd.DataFrame, format: str) -> None:
    dataExporter = DataExporter(filtered_dataset, "Exported")
    match format:
        case "TXT":
            dataExporter.export_to_txt()
        case "JSON":
            dataExporter.export_to_json()
        case "CSV":
            dataExporter.export_to_csv()
        case "XLSX":
            dataExporter.export_to_xlsx()
        case "PDF":
            dataExporter.export_to_pdf()
        case _:
            raise Exception("You selected a wrong format of the export file!")

css = """body {background-color: rgb(111,15,25)}"""
if __name__ == "__main__":
    with gr.Blocks(title="Dataset Converter") as my_app:
        error_box = gr.Textbox(label="Error", visible=False)

        with gr.Tabs():
            with gr.TabItem("Dataset"):
                with gr.Row():
                    # Left Panel
                    with gr.Column():
                        source_box = gr.Dropdown(label="Please select the dataset source (library): ", value="Seaborn", choices=reader_tester.list())
                        submit_source_btn = gr.Button("Submit source")

                        ### Seaborn & Sklearn section ###
                        dataset_box = gr.Radio(label="Enter the dataset name: ", visible=False)

                        ### Generated section ###
                        with gr.Column(visible=False) as generated_dataset_col:
                            col_number = gr.Number(label="Enter number of columns: ", value=1, minimum=1, maximum=50)
                            row_number = gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=10000)
                            submit_gen_btn = gr.Button("Generate dataset")
                            gen_info_text = gr.Text(visible=False)

                        ### Individual section ###
                        with gr.Column(visible=False) as individual_dataset_col:
                            file_reader = gr.File(label="Input file with dataset: ")
                            submit_file_btn = gr.Button("Import file")

                        ### Last configuration section ###
                        with gr.Column(visible=False) as output_conf_col:
                            location_method_box = gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list())
                            structure_method_box = gr.Radio(label="Please select the method of structure build while data reading: ", value="Normal", choices=read_by.list())
                            limit_box = gr.Slider(label="Please select number of records: ", minimum=1, maximum=1000, value=5, step=5)
                            submit_conf_btn = gr.Button("Submit configurations")

                    # Right Panel
                    with gr.Column():
                        with gr.Column(visible=False) as output_result_col:
                            result_box = gr.DataFrame()

            with gr.TabItem("Details & Filtering"):
                # Filtering Panel
                submit_fetch_fields_btn = gr.Button("Fetch Dataset Fields")
                with gr.Row():
                    with gr.Column():
                        
                        filter_info = gr.Label(label="Info", value="Please choose Fetch Dataset Fields button to fill the missing values in the field filterings dropdown.")
                        
                        filter_fields = gr.Dropdown(label="Select Field", choices=[])
                        filter_dtype = gr.Radio(label="Filtering by", choices=["Str", "Int", "Float"], value="Str")

                        filter_value = gr.Textbox(label="Enter value (e.g. 'a'; 'a,b,c'; '2,5,10'; '3.14,1.618')")
                        numeric_filter = gr.Radio(label="Select comparision mark (Only for numeric filter!)", value=comparision_marks[2], choices=comparision_marks)
                        source_selector = gr.Checkbox(label="Do you want to perform filtering on the following dataset?", visible=False)

                        filter_result = gr.DataFrame()
                
                # Sampling Panel
                extractor_position = gr.Radio(label="Extract samples from: ", value=read_from.list()[0], choices=read_from.list(), visible=False)
                extractor_quantity = gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=len(filter_result.value), visible=False)
                submit_sampling_btn = gr.Button("Extract slice of samples", visible=False)

                # APPLY SETTINGS
                submit_filter_ds_btn = gr.Button("Get Filtered Dataset")

                # Exporting Panel
                export_info = gr.Text(visible=False)
                export_format = gr.Radio(label="Select export format for the filtered dataset: ", value=exports[0], choices=exports, visible=False)
                submit_export_btn = gr.Button("Export Filtered Dataset", visible=False)
                
        ### On-click 'Dataset' section ###
        submit_source_btn.click(
            submit_source,
            [source_box],
            [error_box, dataset_box, output_conf_col, generated_dataset_col, individual_dataset_col, output_result_col]
        )

        submit_gen_btn.click(
            submit_gen,
            [col_number, row_number],
            [error_box, dataset_box, output_conf_col, gen_info_text, individual_dataset_col, output_result_col]
        )

        submit_file_btn.click(
            submit_file,
            [file_reader],
            [error_box, dataset_box, output_conf_col, generated_dataset_col, output_result_col]
        )

        submit_conf_btn.click(
            submit_conf,
            [source_box, dataset_box, location_method_box, structure_method_box, limit_box],
            [error_box, output_result_col, result_box]
        )

        ### On-click 'Details & Filtering' section ###
        submit_fetch_fields_btn.click(
            submit_fetch,
            [result_box],
            [error_box, filter_fields]
        )

        submit_sampling_btn.click(
            submit_sample,
            [filter_result, extractor_position, extractor_quantity],
            [error_box, filter_result, extractor_quantity]
        )

        submit_filter_ds_btn.click(
            submit_filter,
            [result_box, filter_result, filter_fields, filter_dtype, filter_value, numeric_filter, source_selector],
            [error_box, filter_result, source_selector, 
             extractor_position, extractor_quantity, submit_sampling_btn,
             export_info, export_format, submit_export_btn]
        )

        submit_export_btn.click(
            submit_export,
            [filter_result, export_format]
        )

    my_app.launch()
