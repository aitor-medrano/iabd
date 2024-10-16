import gradio as gr
from transformers import pipeline

input_text="I like to play basketball and being a geek"

try:
    model = f"Helsinki-NLP/opus-mt-en-es"
    pipe = pipeline("translation", model=model)
    translation = pipe(input_text)
    print(translation[0]['translation_text'])
except KeyError:
    print(f"Error: No se ha podido traducir {input_text}")

# pip install gradio, transformers, torch, sentencepiece, sacremoses
