from transformers import pipeline
import numpy as np
import gradio as gr

pipe = pipeline(
    "automatic-speech-recognition", model="openai/whisper-base"
)

def transcribe(stream, new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
    return stream, pipe({"sampling_rate": sr, "raw": stream})["text"]

demo = gr.Interface(
    transcribe,
    ["state", gr.Audio(sources=["microphone"], streaming=True)],
    ["state", "text"],
    live=True,
)

demo.launch()