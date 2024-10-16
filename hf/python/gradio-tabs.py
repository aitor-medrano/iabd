import gradio as gr

with gr.Blocks() as demo:
    with gr.Tab(label="Botones"):
        btn1 = gr.Button("Botón 1")
        btn2 = gr.Button("Botón 2")
    with gr.Tab(label="Cajas"):
        text1 = gr.Textbox(placeholder="Uno")
        text2 = gr.Textbox(placeholder="Dos")

demo.launch()