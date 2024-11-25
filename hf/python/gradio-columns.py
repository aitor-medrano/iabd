import gradio as gr

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=2):
            btn1 = gr.Button("Botón 1")
            btn2 = gr.Button("Botón 2")
        with gr.Column(scale=1):
            text1 = gr.Textbox(placeholder="A")
            text2 = gr.Textbox(placeholder="B")

demo.launch()