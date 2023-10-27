# REPAIR STRUCTURE TEMPLATE PATHS!!!

# 0.
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
#TODO: Value_handler refactor

# 4.
#TODO: Requirements UPDATE!!!
#TODO: Overall refactor
#TODO: Facade, response boilerplate & GUI & backend separately

#BUG: Random, w momencie jak limit > ilosc rekordow to wyswietla 1

import sys, os

from types import GeneratorType
import gradio as gr
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_app.source.data_reader import DataReader
from gen_app.utils.data_generator_by_gen import DataGenerator
from gen_app.utils.pandas_extension import gen_to_df, df_to_gen

from gen_app.variables.enumerators import read_by, read_from, reader_tester
from gen_app.variables.lists import seaborn_libraries, sklearn_libraries

generated_dataset = None

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
    return location_method, structure_method

def value_handler(source_name: str, df_name: str, location_method: str, structure_method: str, row_count: int):
    location_method, structure_method = enum_handler(location_method, structure_method)

    dataset = None
    by_gen = True
    if source_name == "Generated":
        by_gen = False
        global generated_dataset
        dataset = pd.DataFrame(gen_to_df(generated_dataset))
    
    dataReader = DataReader(df_name, source_name, location_method, structure_method, row_count, by_gen=by_gen, dataset_for_generated=dataset)
    result_df = dataReader.read_data()
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
        return {
            error_box: gr.Textbox(value=str(e), visible=True)
        }

def submit_file(file_reader):
    if file_reader.value is not None:
        file_content = file_reader.value.read()
        print(file_content)
        #TODO: Continue here
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

css = """body {background-color: rgb(11,15,25)}"""
if __name__ == "__main__":
    with gr.Blocks(css=css) as my_app:
        error_box = gr.Textbox(label="Error", visible=False)
        
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
            
        with gr.Column(visible=False) as output_result_col:
            result_box = gr.DataFrame(label="Result: ", interactive=1)

        
        ### On-click section ###
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

    my_app.launch()
