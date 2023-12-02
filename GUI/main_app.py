#TODO: Column deleting, Including sorting to be remembered during export

"""
NOTES:
Seaborn, Sklearn & Generated are designed to show the efficiency of generators.

IMPORT:
ACTION: Using generators, we move the moment of writing data to memory from the very beginning to just before the display 
(To show the data on the page, we need the dataframe format).
The generator is converted to a dataframe not until a parameter with itself is passed to the result_box.
PURPOSE: We transfer the data in the generator format until it is written before displaying.
EFFECT: We do not move a previously saved object in memory several times (memory-saving).

PROCESSING:
The dataframe in the Dataset panel on the right is shown for visual purposes and to demonstrate operation only. 
It causes a drop in performance by forcing data from the generators to be written to the Dataframe.
My aim was to create an efficient and user-friendly application, not just an efficient one. 
It would be good if the user could see what they wanted to process and where to get the data from.
If the data were not displayed, it would be possible to keep the format of the generators, and then in the filtering panel,
check through iterations of a loop each item generated on the fly to see if it meets the filtering conditions 
(This would be less efficient than using the already optimised pandas library, so I decided to balance and partially implement the solution).
"""
import sys, os
import io, base64

from datetime import datetime
from types import GeneratorType
from typing import Union
from enum import Enum
import math
import matplotlib.pyplot as plt
import gradio as gr
import pandas as pd
import seaborn as sns

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gen_app.source.data_reader import DataReader
from gen_app.utils.data_generator_by_gen import DataGenerator
from gen_app.utils.data_exporter import DataExporter
from gen_app.utils.pandas_extension import DataManager, gen_to_df, df_to_gen

from gen_app.variables.enumerators import read_by, read_from, reader_tester
from gen_app.variables.lists import seaborn_libraries, sklearn_libraries, comparision_marks, gen_exports, exports, read_with_gen

generated_dataset = None
individual_dataset_path = None
dataManager = DataManager(pd.DataFrame())

def is_text(value):
    return isinstance(value, str) and any(char.isalpha() for char in value)

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

def value_handler(source_name: str, df_name: str, read_with_gen: bool = True, location_method: str = read_from.TOP, structure_method: str = read_by.NORMAL, row_count: int = 1000):
    location_method, structure_method = enum_handler(location_method, structure_method)

    dataset = None
    if source_name == "Generated":
        global generated_dataset
        dataset = generated_dataset
    elif source_name == "Individual":
        global individual_dataset_path
        source_name = individual_dataset_path
        df_name = "Individual"
    
    dataReader = DataReader(df_name, source_name, location_method, structure_method, row_count, by_gen=read_with_gen, dataset_for_generated=dataset)
    result_ds = dataReader.read_data()

    if source_name in ["Seaborn", "Sklearn"]:
        if structure_method == read_by.CHUNKS and read_with_gen == True:
            return gen_to_df(result_ds)

    if df_name == "Individual":
        if type(result_ds) == GeneratorType:
            if source_name.endswith((".txt", ".csv", ".json")):
                return gen_to_df(result_ds)

    return result_ds

def reformat_reader_data_to_log(log_records: str, source_name: str, df_name: str, read_with_gen: bool = True, location_method: str = read_from.TOP, structure_method: str = read_by.ROWS, limit: int = 1, col_number: int=1) -> str:
    elem_content = "<h3>DATASET READER - " + datetime.now().strftime("[%Y-%m-%d, %H:%M:%S], ")
    if source_name in ["Seaborn", "Sklearn"]:
        elem_content += (
            "(" + source_name           + ", " + df_name        + "):</h3>" +
            "<ul><li>READ_BY_GEN: "     + str(read_with_gen)    + "</li>" +
            "<li>READ_FROM: "           + location_method       + "</li>" +
            "<li>READ_BY: "             + structure_method      + "</li>" +
            "<li>NUM_OF_ROWS: "         + str(limit)            + "</li>" +
            "<li>TIME: "                + "0s"                  + "</li></ul>"
        )   
    elif source_name == "Generated":
        elem_content += (
            "(" + source_name                           + "):</h3>" +
            "<ul><li>NUM_OF_COLS: " + str(col_number)   + "</li>" + 
            "<li>NUM_OF_ROWS: "     + str(limit)        + "</li>" +
            "<li>TIME: "            + "0s"              + "</li></ul>"
        )
    elif source_name == "Individual":
        global individual_dataset_path
        df_name = os.path.basename(individual_dataset_path)
        elem_content += (
            "(" + source_name       + ", " + df_name        + "):</h3>" +
            "<ul><li>READ_BY_GEN: " + str(read_with_gen)    + "</li>" +
            "<li>TIME: "            + "0s"                  + "</li></ul>"
        )
    else:
        raise Exception("Wrong source!")
    
    new_elem = "<tr><td>" + elem_content + "</td></tr>"

    table_content_start_index = log_records.find(">")+1
    start_of_table = log_records[:table_content_start_index]
    end_of_table = log_records[table_content_start_index:]

    return start_of_table + new_elem + end_of_table
        


def submit_gen(col_number: int, row_number: int, log_record: str):
    try:
        dataGen = DataGenerator(int(col_number), int(row_number))

        global generated_dataset
        generated_dataset = dataGen.generate_dataframe_by_gen()
        generated_dataset_to_df = value_handler(source_name="Generated", df_name="Generated", read_with_gen=True)
        log_info = reformat_reader_data_to_log(log_record, source_name="Generated", df_name="Generated", limit=row_number, col_number=col_number)
        return {
            dataset_box: gr.Radio(label="Enter the dataset name: ", visible=False),
            gen_info_text: gr.Text("The dataset was successfully generated!", visible=True),
            output_conf_col: gr.Column(visible=False),
            output_result_col: gr.Column(visible=True),
            individual_dataset_col: gr.Column(visible=False),
            result_box: gr.DataFrame(label="Result: ", value=pd.DataFrame(gen_to_df(generated_dataset_to_df)), interactive=1),
            log_records: gr.HTML(log_info)
        }
    except Exception as e:
        return {error_box: gr.Textbox(value=str(e), visible=True)}

def submit_file(file_reader):
    if file_reader is not None:
        global individual_dataset_path
        individual_dataset_path = file_reader.name
        if individual_dataset_path.endswith((".txt", ".csv", ".json")):
            read_method_box_choices = read_with_gen
            read_method_box_value = None
        elif individual_dataset_path.endswith(".xlsx"):
            read_method_box_choices = [False]
            read_method_box_value = False
        else:
            return {error_box: gr.Textbox(value="Acceptable file formats are only .txt, .csv, .json and .xlsx!", visible=True)}
        return {
            dataset_box: gr.Radio(label="Enter the dataset name: ", visible=False),
            output_conf_col: gr.Column(visible=True),
            generated_dataset_col: gr.Column(visible=False),
            output_result_col: gr.Column(visible=False),
            read_method_box: gr.Radio(label="Do you want to read the data with a generator?", value=read_method_box_value, choices=read_method_box_choices)
        }
    else:
        return {error_box: gr.Textbox(value="First you have to select the file!", visible=True)}

def submit_conf(source_name: str, df_name: str, read_with_gen: bool, location_method: str, structure_method: str, limit: str, log_record: str):    
    dataset = value_handler(source_name, df_name, read_with_gen, location_method, structure_method, limit)
    log_info = reformat_reader_data_to_log(log_record, source_name, df_name, read_with_gen, location_method, structure_method, limit)
    return {
        output_result_col: gr.Column(visible=True),
        result_box: gr.DataFrame(label="Result: ", value=pd.DataFrame(dataset), interactive=1),
        log_records: gr.HTML(log_info)
    }

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

        return {
            filter_result: filtered_dataset, 
            source_selector: gr.Checkbox(label="Do you want to perform filtering on the following dataset?", visible=True),

            export_info: gr.Text("The dataset was successfully filtered. Select the file format of dataset export: ", visible=True),
            export_method: gr.Radio(label="Do you want to export the data with a generator?", value=read_with_gen[0], choices=read_with_gen, visible=True),
            export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=gen_exports[0], choices=gen_exports, visible=True),
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

def submit_export(filtered_dataset: pd.DataFrame, export_method_by_gen: bool, format: str) -> None:
    if export_method_by_gen:
        filtered_gen = df_to_gen(filtered_dataset)
        dataExporter = DataExporter(filtered_gen, "Exported_by_gen")
    else:
        dataExporter = DataExporter(filtered_dataset, "Exported_by_df")
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

def submit_analysis(filtered_dataset: pd.DataFrame):
    result = filtered_dataset.applymap(is_text)
    string_columns = result.columns[result.all()].tolist()
    numeric_columns = filtered_dataset.select_dtypes(include="number").columns.tolist()
    return {
        analysis_describe: gr.Dataframe(label="Basic descriptive statistics: ", value=filtered_dataset.describe().reset_index(), visible=True),
        analysis_panel: gr.Row(visible=True),
        analysis_numeric_fields_correlation: gr.Dropdown(label="Select fields", choices=numeric_columns, multiselect=True),
        analysis_numeric_fields_histogram: gr.Dropdown(label="Select fields", choices=numeric_columns, multiselect=True),
        analysis_numeric_fields_boxplot: gr.Dropdown(label="Select numeric variable", choices=numeric_columns, visible=False),
        analysis_string_fields_boxplot: gr.Dropdown(label="Select category group", choices=string_columns, visible=False),
    }

def submit_draw(filtered_dataset: pd.DataFrame, analysis_boxplot_choose: str, group_col: str, num_col: str):
    if analysis_boxplot_choose:
        plt.figure()
        if analysis_boxplot_choose == "For category and numeric variable" and group_col and num_col:
            sns.boxplot(x=group_col, y=num_col, data=filtered_dataset)
            plt.xlabel(f"Category - {group_col}")
        elif analysis_boxplot_choose == "For numeric variable" and num_col:
            sns.boxplot(data=filtered_dataset[num_col])
        else:
            return {analysis_boxplots: gr.Image(None, label="Boxplot", visible=False, elem_id="boxp")}
        
        plt.title(f"Boxplot - {analysis_boxplot_choose}")
        plt.ylabel(f"Numeric value - {num_col}")
        plt.tight_layout()
        plt.savefig("Boxplot_TMP.png")

        return {analysis_boxplots: gr.Image("Boxplot_TMP.png", label="Boxplot", visible=True, elem_id="boxp")}
    else:
        return {analysis_boxplots: gr.Image(None, label="Boxplot", visible=False, elem_id="boxp")}

def submit_clear_log():
    return {log_records: gr.HTML("<table style='width: 100%; border: 1px solid grey; text-align: center; padding: 10px'></table>")}

def turn_configuration(source_name: str):
    dataset_box_choices = dataset_box_visible = None

    match source_name:
        case "Seaborn":
            dataset_box_choices = seaborn_libraries
            dataset_box_value = dataset_box_choices[0]
            dataset_box_visible = True
        case "Sklearn":
            dataset_box_choices = sklearn_libraries
            dataset_box_value = dataset_box_choices[0]
            dataset_box_visible = True
        case "Generated":
            dataset_box_value = None
            dataset_box_visible = False
        case "Individual":
            dataset_box_value = None
            dataset_box_visible = False
        case _:
            return {error_box: gr.Textbox(value="Wrong data source selected!", visible=True)}
        
    return {
        dataset_box: gr.Radio(label="Enter the dataset name: ", value=dataset_box_value, choices=dataset_box_choices, visible=dataset_box_visible),
        output_conf_col: gr.Column(visible=(source_name=="Seaborn" or source_name=="Sklearn")),

        read_method_box: gr.Radio(label="Do you want to read the data with a generator?", value=None, choices=read_with_gen),
        location_method_box: gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list(), visible=False),
        structure_method_box: gr.Radio(label="Please select the method of structure build while data reading: ", value="Normal", choices=read_by.list(), visible=False),
        limit_box: gr.Slider(label="Please select number of records: ", minimum=1, maximum=10000, value=1, step=5, visible=False),
        submit_conf_btn: gr.Button("Submit configurations", visible=False),
        
        generated_dataset_col: gr.Column(visible=source_name=="Generated"),
        individual_dataset_col: gr.Column(visible=source_name=="Individual"),
        output_result_col: gr.Column(visible=False),
        gen_info_text: gr.Text(visible=False),
        result_box: gr.DataFrame(None),

        filter_fields: gr.Dropdown(label="Select Field", choices=[]),
        export_info: gr.Text("The dataset was successfully filtered. Select the file format of dataset export: ", visible=False),
        export_method: gr.Radio(label="Do you want to export the data with a generator?", value=read_with_gen[0], choices=read_with_gen, visible=False),
        export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=gen_exports[0], choices=gen_exports, visible=False),
        submit_export_btn: gr.Button("Export Filtered Dataset", visible=False)
    }

def turn_preparation(source_name: str, read_with_gen: bool):
    if read_with_gen is not None:
        match source_name:
            case "Seaborn" | "Sklearn":
                if read_with_gen:
                    structure_method_box_value = read_by.seaborn_sklearn_gen_list()[0]
                    structure_method_box_choices = read_by.seaborn_sklearn_gen_list()
                else:
                    structure_method_box_value = read_by.list()[0]
                    structure_method_box_choices = read_by.list()
            case "Individual":
                structure_method_box_value = "Normal"
                structure_method_box_choices = read_by.list()
            case _:
                raise Exception("Wrong source!")
            
        return {
            location_method_box: gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list(), visible=(source_name!="Individual")),
            structure_method_box: gr.Radio(label="Please select the method of structure build while data reading: ", value=structure_method_box_value, choices=structure_method_box_choices, visible=(source_name!="Individual")),
            limit_box: gr.Slider(label="Please select number of records: ", minimum=1, maximum=10000, value=1, step=5, visible=(source_name!="Individual")),
            submit_conf_btn: gr.Button("Submit configurations", visible=True)
        }
    return {
        location_method_box: gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list(), visible=False),
        structure_method_box: gr.Radio(label="Please select the method of structure build while data reading: ", value="Normal", choices=read_by.list(), visible=False),
        limit_box: gr.Slider(label="Please select number of records: ", minimum=1, maximum=10000, value=1, step=5, visible=False),
        submit_conf_btn: gr.Button("Submit configurations", visible=False)
    }

def turn_details(dataset: pd.DataFrame):
    IS_DATASET_NULL = (dataset.columns.tolist() == ['1','2','3'] or dataset.columns.tolist() == [1,2,3]) and dataset.shape[0] == 1 # gr.DataFrame is empty with [1,2,3] columns and one null record with index 0
    if IS_DATASET_NULL: 
        filter_fields_choices = []
        filter_fields_value = None
    else:
        filter_fields_choices = dataset.columns.tolist()
        filter_fields_value = dataset.columns[0]

    return {
        DF_status_before: gr.Column(visible=IS_DATASET_NULL),
        SA_status_before: gr.Column(visible=IS_DATASET_NULL),
        DF_status_after: gr.Column(visible=not IS_DATASET_NULL),
        SA_status_after: gr.Column(visible=not IS_DATASET_NULL),

        filter_fields: gr.Dropdown(label="Select Field", value=filter_fields_value, choices=filter_fields_choices),
        filter_dtype: gr.Radio(label="Filtering by", choices=["Str", "Int", "Float"], value="Str"),
        filter_value: gr.Textbox(label="Enter value", value=""),
        numeric_filter: gr.Radio(label="Select comparision mark (Only for numeric filter!)", value=comparision_marks[2], choices=comparision_marks, visible=False),
                                
        source_selector: gr.Checkbox(label="Do you want to perform filtering on the following dataset?", value=False, visible=False),
        extractor_position: gr.Radio(label="Extract samples from: ", value=read_from.list()[0], choices=read_from.list(), visible=False),
        extractor_quantity: gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=1000, visible=False),
        submit_sampling_btn: gr.Button("Extract slice of samples", visible=False),
        
        filter_result: gr.DataFrame(None) if IS_DATASET_NULL else gr.DataFrame(label="Result: ", value=pd.DataFrame(dataset), interactive=1),

        export_info: gr.Text(visible=False),
        export_method: gr.Radio(label="Do you want to export the data with a generator?", value=None, choices=read_with_gen, visible=False),
        export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=gen_exports[0], choices=gen_exports, visible=False),
        submit_export_btn: gr.Button("Export Filtered Dataset", visible=False)
    }

def turn_comparision(dtype: str):
    if dtype == "Str":
        instruction = """
                        <ul>
                            <h3 style='text-align: center'>Search masks examples for string (without quotes): </h3>
                            <li>'a' - Returns records containing the character/word 'a'</li>
                            <li>'aa,bb,cb' - Returns records containing the characters/words 'aa' or 'bb' or 'cc'</li>
                            <li>'a..d' - Returns records containing the words with unknown characters (number of dots = number of unknown chars inplace): e.g.: acid</li>
                            <li>'p*n' - Returns records containing the words with undefined number of unknown characters inplace of *: e.g.: python</li>
                        </ul>
                    """
    elif dtype == "Int":
        instruction = """
                        <ul>
                            <h3 style='text-align: center'>Search masks examples for int (without quotes): </h3>
                            <li>'3' - Uses records containing the number 3</li>
                            <li>'3,4,9,11' - Uses records containing the number 3 or 4 or 9 or 11</li>
                        </ul>
                    """
    elif dtype == "Float":
        instruction = """
                        <ul>
                            <h3 style='text-align: center'>Search masks examples for float (without quotes): </h3>
                            <li>'3.12' - Uses records containing the number 3.12</li>
                            <li>'3.14,1.618,2.0' - Uses records containing the number 3.14 or 1.618 or 2.0</li>
                        </ul>
                    """
    return {
        filter_info: gr.HTML(instruction),
        numeric_filter: gr.Radio(label="Select comparision mark (Only for numeric filter!)", value=comparision_marks[2], choices=comparision_marks, visible=(dtype != "Str"))
    }

def turn_extraction(filtered_dataset: pd.DataFrame, is_filtered: bool):
    return {
        extractor_position: gr.Radio(label="Extract samples from: ", value=read_from.list()[0], choices=read_from.list(), visible=is_filtered),
        extractor_quantity: gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=len(filtered_dataset), visible=is_filtered),
        submit_sampling_btn: gr.Button("Extract slice of samples", visible=is_filtered)
    }

def turn_export_preparation(export_method_by_gen: bool):
    if export_method_by_gen is not None:
        if export_method_by_gen:
            return {export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=gen_exports[0], choices=gen_exports, visible=True)}
        else:
            return {export_format: gr.Radio(label="Select export format for the filtered dataset: ", value=exports[0], choices=exports, visible=True)}
    
def turn_analysis():
    return {
        analysis_describe: gr.DataFrame(visible=False),
        analysis_panel: gr.Row(visible=False),

        analysis_numeric_fields_correlation: gr.Dropdown(label="Select fields", value=[], choices=[], multiselect=True),
        analysis_correlations: gr.DataFrame(None, visible=False),

        analysis_numeric_fields_histogram: gr.Dropdown(label="Select fields", value=[], choices=[], multiselect=True),
        analysis_histograms: gr.Image(None, label="Plot", visible=False, elem_id="hist"),

        analysis_boxplot_radio: gr.Radio(label="Select type of boxplots:", value=None, choices=["For category and numeric variable", "For numeric variable"]),
        analysis_string_fields_boxplot: gr.Dropdown(label="Select category group:", value="", choices=[""], visible=False),
        analysis_numeric_fields_boxplot: gr.Dropdown(label="Select numeric variable:", value="", choices=[""], visible=False),
        analysis_boxplots: gr.Image(None, label="Boxplot", visible=False, elem_id="boxp")
    }

def turn_correlations(filtered_dataset: pd.DataFrame, analysis_numeric_fields: list[str]):
    if analysis_numeric_fields is not None:
        if len(analysis_numeric_fields) > 1:
            return {
                analysis_correlations: gr.DataFrame(
                    label="Correlations between " + str(analysis_numeric_fields), 
                    value=filtered_dataset[analysis_numeric_fields].corr().reset_index(), 
                    visible=True
                )
            }
    
    return {analysis_correlations: gr.DataFrame(label="",value=pd.DataFrame(None), visible=False)}

def turn_histograms(filtered_dataset: pd.DataFrame, analysis_numeric_fields: list[str]):
    if analysis_numeric_fields is not None:
        if len(analysis_numeric_fields) > 0:
            plt.figure()
            hist_per_row = math.ceil(math.sqrt(len(analysis_numeric_fields)))
            hist_per_col = math.ceil(len(analysis_numeric_fields)/hist_per_row)
            
            if len(analysis_numeric_fields) > 1:
                fig, axes = plt.subplots(hist_per_col,hist_per_row)
                axes = axes.ravel()
                for title, ax in zip(analysis_numeric_fields, axes):
                    ax.hist(filtered_dataset[title])

                    ax.set_title(f"Histogram - {title}")
                    ax.set_xlabel("Value")
                    ax.set_ylabel("Frequency")
            else:
                filtered_dataset[analysis_numeric_fields].hist()
                plt.title(f"Histogram - {analysis_numeric_fields[0]}")
                plt.xlabel("Value")
                plt.ylabel("Frequency")

            plt.tight_layout(pad=2.0)
            plt.savefig("Histogram_TMP.png")

            return {analysis_histograms: gr.Image("Histogram_TMP.png", label="Plot", visible=True, elem_id="hist")}
    return {analysis_histograms: gr.Image(None, label="Plot", visible=False, elem_id="hist")}

def turn_boxplots_conf(analysis_boxplot_choose: str):
    FOR_SELECTED = False
    if analysis_boxplot_choose:
        if analysis_boxplot_choose == "For category and numeric variable":
            FOR_SELECTED = True
        elif analysis_boxplot_choose == "For numeric variable":
            FOR_SELECTED = False

    return {
        analysis_string_fields_boxplot: gr.Dropdown(visible=(analysis_boxplot_choose is not None and FOR_SELECTED)),
        analysis_numeric_fields_boxplot: gr.Dropdown(visible=(analysis_boxplot_choose is not None)),
        analysis_boxplots: gr.Image(None, label="Boxplot", visible=False, elem_id="boxp")
    }


global_css = '#hist,#boxp{display: flex; justify-content: center} #hist img,#boxp img{width: 50vw}'
if __name__ == "__main__":
    with gr.Blocks(title="Dataset Converter", css=global_css) as my_app:
        error_box = gr.Textbox(label="Error", visible=False)

        with gr.Tabs():
            with gr.TabItem("Dataset"):
                with gr.Row():
                    # Left Panel
                    with gr.Column():
                        source_box = gr.Dropdown(label="Please select the dataset source (library): ", choices=reader_tester.list())

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
                            read_method_box = gr.Radio(label="Do you want to read the data with a generator?", choices=read_with_gen)
                            location_method_box = gr.Radio(label="Please select the row sampling type: ", value="Top", choices=read_from.list(), visible=False)
                            structure_method_box = gr.Radio(label="Please select the method of structure build while data reading: ", value="Normal", choices=read_by.list(), visible=False)
                            limit_box = gr.Slider(label="Please select number of records: ", minimum=1, maximum=10000, value=1, step=5, visible=False)
                            submit_conf_btn = gr.Button("Submit configurations", visible=False)

                    # Right Panel   
                    with gr.Column():
                        with gr.Column(visible=False) as output_result_col:
                            result_box = gr.DataFrame()

            with gr.TabItem("Details & Filtering"):
                # Filtering Panel
                with gr.Row():
                    with gr.Column(visible=True) as DF_status_before:
                        message_info = gr.Label(label="Info", value="In order to operate on the selected data set, it must first be loaded in the previous tab.")
                    with gr.Column(visible=False) as DF_status_after:
                        filter_fields = gr.Dropdown(label="Select Field", choices=[])
                        filter_dtype = gr.Radio(label="Filtering by", choices=["Str", "Int", "Float"], value="Str")
                
                        filter_info = gr.HTML("""
                            <ul>
                                <h3 style='text-align: center'>Search masks examples (without quotes): </h3>
                                <li>'a' - Returns records containing the character/word 'a'</li>
                                <li>'aa,bb,cb' - Returns records containing the characters/words 'aa' and 'bb' and 'cc'</li>
                                <li>'a..d' - Returns records containing the words with unknown characters (number of dots = number of unknown chars inplace): e.g.: acid</li>
                                <li>'p*n' - Returns records containing the words with undefined number of unknown characters inplace of *: e.g.: python</li>
                            </ul>
                        """)
                        filter_value = gr.Textbox(label="Enter value")
                        numeric_filter = gr.Radio(label="Select comparision mark (Only for numeric filter!)", value=comparision_marks[2], choices=comparision_marks, visible=False)
                        source_selector = gr.Checkbox(label="Do you want to perform filtering on the following dataset?", visible=False)
                        
                        # Sampling Panel
                        extractor_position = gr.Radio(label="Extract samples from: ", value=read_from.list()[0], choices=read_from.list(), visible=False)
                        extractor_quantity = gr.Number(label="Enter number of rows: ", value=1, minimum=1, maximum=1000, visible=False)
                        submit_sampling_btn = gr.Button("Extract slice of samples", visible=False)

                        filter_result = gr.DataFrame()
                
                        # APPLY SETTINGS
                        submit_filter_ds_btn = gr.Button("Get Filtered Dataset")
                
                # Exporting Panel
                export_info = gr.Text(visible=False)
                export_method = gr.Radio(label="Do you want to export the data with a generator?", value=read_with_gen[0], choices=read_with_gen, visible=False)
                export_format = gr.Radio(label="Select export format for the filtered dataset: ", value=gen_exports[0], choices=gen_exports, visible=False)
                submit_export_btn = gr.Button("Export Filtered Dataset", visible=False)

            with gr.TabItem("Statistical analysis"):
                # Analysis panel
                with gr.Row():
                    with gr.Column(visible=True) as SA_status_before:
                        message_info = gr.Label(label="Info", value="In order to operate on the selected data set, it must first be loaded in the previous tab.")
                    with gr.Column(visible=False) as SA_status_after:
                        analysis_info = gr.Text("Analysis is based on the dataset located in the filtering panel.", label="Important")
                        start_analysis_btn = gr.Button("Start statistical analysis")

                        analysis_describe = gr.DataFrame(visible=False)
                        with gr.Row(visible=False) as analysis_panel:
                            with gr.TabItem("Correlations"):
                                analysis_numeric_fields_correlation = gr.Dropdown(label="Select fields", choices=[], multiselect=True)
                                analysis_correlations = gr.DataFrame(visible=False)
                            with gr.TabItem("Histograms"):
                                analysis_numeric_fields_histogram = gr.Dropdown(label="Select fields", choices=[], multiselect=True)
                                analysis_histograms = gr.Image(label="Plot", visible=False, elem_id="hist")
                            with gr.TabItem("Boxplots"):
                                analysis_boxplot_radio = gr.Radio(label="Select type of boxplots:", choices=["For category and numeric variable", "For numeric variable"])
                                analysis_string_fields_boxplot = gr.Dropdown(label="Select category group:", choices=[], visible=False)
                                analysis_numeric_fields_boxplot = gr.Dropdown(label="Select numeric variable:", choices=[], visible=False)
                                analysis_draw_btn = gr.Button("Generate boxplot")
                                analysis_boxplots = gr.Image(label="Boxplot", visible=False, elem_id="boxp")
        
            with gr.TabItem("Log"):
                # Log panel
                with gr.Column():
                    logs_info = gr.Text(label="Info", value="This log records information about each key operation (i.e. data loading, filtering, exports, time measurements and all parameters) into history.")
                    clear_log_btn = gr.Button("Clear log")
                    with gr.Row():
                        log_records = gr.HTML("<table style='width: 100%; border: 1px solid grey; text-align: center; padding: 10px'></table>")

        ### On-click 'Dataset' section ###
        submit_gen_btn.click(
            submit_gen,
            [col_number, row_number, log_records],
            [error_box, dataset_box, output_conf_col, gen_info_text, individual_dataset_col, output_result_col, result_box, log_records]
        )

        submit_file_btn.click(
            submit_file,
            [file_reader],
            [error_box, dataset_box, output_conf_col, generated_dataset_col, output_result_col, read_method_box]
        )

        submit_conf_btn.click(
            submit_conf,
            [source_box, dataset_box, read_method_box, location_method_box, structure_method_box, limit_box, log_records],
            [error_box, output_result_col, result_box, log_records]
        )

        ### On-click 'Details & Filtering' section ###
        submit_sampling_btn.click(
            submit_sample,
            [filter_result, extractor_position, extractor_quantity],
            [error_box, filter_result, extractor_quantity]
        )

        submit_filter_ds_btn.click(
            submit_filter,
            [result_box, filter_result, filter_fields, filter_dtype, filter_value, numeric_filter, source_selector],
            [error_box, filter_result, source_selector, 
             export_info, export_method, export_format, submit_export_btn]
        )

        submit_export_btn.click(
            submit_export,
            [filter_result, export_method, export_format]
        )

        ### On-click 'Statistical analysis' section ###
        start_analysis_btn.click(
            submit_analysis,
            [filter_result],
            [analysis_describe, analysis_panel, analysis_numeric_fields_correlation, analysis_numeric_fields_histogram, analysis_numeric_fields_boxplot, analysis_string_fields_boxplot]
        )

        analysis_draw_btn.click(
            submit_draw,
            [filter_result, analysis_boxplot_radio, analysis_string_fields_boxplot, analysis_numeric_fields_boxplot],
            [analysis_boxplots]
        )

        ### On-click 'Log' section ###
        clear_log_btn.click(
            submit_clear_log,
            [], [log_records]
        )

        ### On-change 'Dataset' section ###
        source_box.change(
            turn_configuration,
            [source_box],
            [error_box, read_method_box, location_method_box, structure_method_box, limit_box, submit_conf_btn, dataset_box, output_conf_col, filter_fields, generated_dataset_col, individual_dataset_col, output_result_col, gen_info_text, result_box, export_info, export_method, export_format, submit_export_btn]
        )
        
        read_method_box.change(
            turn_preparation,
            [source_box, read_method_box],
            [location_method_box, structure_method_box, limit_box, submit_conf_btn]
        )

        result_box.change(
            turn_details,
            [result_box],
            [error_box, DF_status_before, DF_status_after, SA_status_before, SA_status_after, filter_fields, filter_dtype, filter_value, numeric_filter, source_selector, extractor_position, extractor_quantity, submit_sampling_btn, export_info, export_method, export_format, submit_export_btn, filter_result]
        )

        ### On-change 'Details & Filtering' section ###
        filter_dtype.change(
            turn_comparision,
            [filter_dtype],
            [filter_info, numeric_filter]
        )

        source_selector.change(
            turn_extraction,
            [filter_result, source_selector],
            [extractor_position, extractor_quantity, submit_sampling_btn]
        )

        filter_result.change(
            turn_analysis,
            [], [analysis_describe, analysis_panel, analysis_boxplot_radio, analysis_numeric_fields_correlation, analysis_correlations,
             analysis_numeric_fields_histogram, analysis_histograms, 
             analysis_boxplot_radio, analysis_string_fields_boxplot, analysis_numeric_fields_boxplot, analysis_boxplots]
        )

        export_method.change(
            turn_export_preparation,
            [export_method],
            [export_format]
        )

        ### On-change 'Statistical analysis' section ###
        analysis_numeric_fields_correlation.change(
            turn_correlations,
            [filter_result, analysis_numeric_fields_correlation],
            [analysis_correlations]
        )

        analysis_numeric_fields_histogram.change(
            turn_histograms,
            [filter_result, analysis_numeric_fields_histogram],
            [analysis_histograms]
        )

        analysis_boxplot_radio.change(
            turn_boxplots_conf,
            [analysis_boxplot_radio],
            [analysis_string_fields_boxplot, analysis_numeric_fields_boxplot, analysis_boxplots]
        )

    my_app.launch()
