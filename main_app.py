# 1.
#TODO: Fix tuples column names & chunk reader
#TODO: Add GeneratedDF operations
#TODO: Add IndividualDF operations (input file, read)
#TODO: Check all methods of data reading for bug hunting

# 2.
#TODO: Update result_box by three buttons displaying: Table, Statistical Analysis, Log
# Table: Interactive DataFrame with checking datatypes before applying changes
# Statistical Analysis: std, med, avg etc.
# Log: Measurements of all steps while data processing (save to file & output it)

# 3.
#TODO: Theme CSS
#TODO: Value_handler refactor

# 4.
#TODO: Overall refactor

import gradio as gr
import pandas as pd

from source.data_reader import DataReader
from variables.enumerators import read_by, read_from, reader_tester
from variables.lists import seaborn_libraries, sklearn_libraries

def value_handler(source_name: str, df_name: str, location_method: str, structure_method: str, row_count: int):
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
    dataReader = DataReader(df_name, source_name, location_method, structure_method, row_count)
    result_df = dataReader.read_data()
    return pd.DataFrame(result_df)
css = """
    .gradio-container {background-color: rgb(11,15,25)}
"""

if __name__ == "__main__":
    with gr.Blocks() as my_app: #css=css
        error_box = gr.Textbox(label="Error", visible=False)
        
        source_box = gr.Dropdown(label="Please select the dataset source (library): ", value="Seaborn", choices=reader_tester.list())
        submit_source_btn = gr.Button("Submit source")

        dataset_box = gr.Radio(label="Enter the dataset name: ", visible=False)
        with gr.Column(visible=False) as output_conf_col:
            location_method_box = gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list())
            structure_method_box = gr.Radio(label="Please select the method of structure build while data reading: ", value="Normal", choices=read_by.list())
            limit_box = gr.Slider(label="Please select number of records: ", minimum=1, maximum=1000, value=5, step=5)
            submit_conf_btn = gr.Button("Submit configurations")
            
        with gr.Column(visible=False) as output_result_col:
            result_box = gr.DataFrame(label="Result: ", interactive=1)

        def submit_source(source_name: str):
            match source_name:
                case "Seaborn":
                    return {
                        dataset_box: gr.Radio(label="Enter the dataset name: ", value=seaborn_libraries[0], choices=seaborn_libraries, visible=True),
                        output_conf_col: gr.Column(visible=True)
                    }
                case "Sklearn":
                    return {
                        dataset_box: gr.Radio(label="Enter the dataset name: ", value=sklearn_libraries[0], choices=sklearn_libraries, visible=True),
                        output_conf_col: gr.Column(visible=True)
                    }
                case "Individual":
                    return {}
                case _:
                    return {error_box: gr.Textbox(value="Wrong data source selected!", visible=True)}
                
        def submit_conf(source_name: str, df_name: str, location_method: str, structure_method: str, limit: str):
            df = value_handler(source_name, df_name, location_method, structure_method, limit)
            return {
                output_result_col: gr.Column(visible=True),
                result_box: gr.DataFrame(label="Result: ", value=df, interactive=1)
            }
            

        submit_source_btn.click(
            submit_source,
            [source_box],
            [error_box, dataset_box, output_conf_col]
        )

        submit_conf_btn.click(
            submit_conf,
            [source_box, dataset_box, location_method_box, structure_method_box, limit_box],
            [error_box, output_result_col, result_box]
        )

    my_app.launch()
