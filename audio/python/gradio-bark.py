from transformers import pipeline
import numpy as np
import gradio as gr

pipe = pipeline("text-to-speech", model="suno/bark-small")

def tts(frase):
    audio_generated = pipe(frase)

    return audio_generated["sampling_rate"],audio_generated["audio"][0]

demo = gr.Interface(
    tts,
    inputs=gr.Text(label="Teclea el texto a pronunciar"),
    outputs=
        gr.Audio(label="audio generado")
    ,
    title="De texto a voz",
)

demo.launch()
