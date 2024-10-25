import gradio as gr
from transformers import pipeline

def sentimiento(frase):
    pipe = pipeline("text-classification")
    return pipe(frase)

demo = gr.Interface(fn=sentimiento, inputs="text", outputs="json")
demo.launch(share=True)