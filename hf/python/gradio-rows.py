import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        gr.Text(placeholder="Uno")
        gr.Text(placeholder="Dos")
        gr.Text(placeholder="Tres")
    
demo.launch()