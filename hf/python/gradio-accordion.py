import gradio as gr

with gr.Blocks() as demo:
    with gr.Accordion("Muestra detalles", open=False):
        gr.Markdown("IABD - *Aitor Medrano*")

demo.launch()