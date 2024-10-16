import torch
from transformers import pipeline
import numpy as np

pipe = pipeline(
    "automatic-speech-recognition", model="openai/whisper-base"
)

def transcribe(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    return pipe({"sampling_rate": sr, "raw": y})["text"]

import gradio as gr

demo = gr.Interface(
    transcribe,
    gr.Audio(),
    "text",
)

demo.launch()
