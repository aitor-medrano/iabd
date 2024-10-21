from transformers import pipeline
import numpy as np
import gradio as gr

transcriber = pipeline(
    "automatic-speech-recognition", model="openai/whisper-base"
)

tts = pipeline("text-to-speech", model="suno/bark-small")

def transcribe(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    text_generated = transcriber({"sampling_rate": sr, "raw": y})["text"]
    print(text_generated)
    audio_generated = tts(text_generated)
    print(audio_generated)

    audio_generated_y = audio_generated["audio"]
    audio_returned = audio_generated["sampling_rate"],audio_generated_y[0]

    return [text_generated, audio_returned]


demo = gr.Interface(
    transcribe,
    inputs=gr.Audio(sources=["microphone"]),
    outputs=[
        gr.Text(label="texto generado"),
        gr.Audio(label="audio generado")
    ],
    title="De audio a Whisper y TTS",
    description="Transcribe el audio y luego sintetiza el texto en audio"
)

demo.launch()
