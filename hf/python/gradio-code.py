import gradio as gr

code = '''def cal_average(numbers):
    sum_number = 0
    for t in numbers:
        sum_number = sum_number + t           

    average = sum_number / len(numbers)
    return average'''

with gr.Blocks() as demo:
    gr.Textbox(code)
    
demo.launch()