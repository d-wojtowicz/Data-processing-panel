import gradio as gr
import pandas as pd
from source.df_individual_reader import read_df_from_input

def process_file(input_file):
    return input_file.name

if __name__ == "__main__":
    file_input = gr.inputs.File()
    output_text = gr.outputs.Textbox()

    iface = gr.Interface(fn=process_file, inputs=file_input, outputs=output_text)


    selected_file = iface.launch(share=True)

    
    print(file_input.value)
    dataframe = read_df_from_input(file_input.value)
    output_text.update("AAA")