import gradio as gr
from transformers import pipeline

def perrogato(imagen):
    pipe = pipeline(model="aitor-medrano/iabd_model")
    return pipe(imagen)

demo = gr.Interface(fn=perrogato, inputs="image", outputs="label")
demo.launch(share=True)