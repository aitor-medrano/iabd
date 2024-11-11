from transformers import pipeline
import gradio as gr
import numpy as np
from datetime import datetime

import librosa

# Con el parámetro device=0, carga el modelo en GPU
pipe_aspanias_mujeres = pipeline("automatic-speech-recognition", model="/home/iabd/Gradio/models/Aspanias/Mujeres")
pipe_g = pipeline("automatic-speech-recognition", model="/home/iabd/Gradio/models/Gertrudis")
pipe_aspanias_completo = pipeline("automatic-speech-recognition", model="/home/iabd/Gradio/models/Aspanias/Completo")
pipe_asfeme = pipeline("automatic-speech-recognition", model="/home/iabd/Gradio/models/Asfeme")

contador = 0

def transcribe(audio, modelo="3"):

    global contador

    sr, y = audio
    y = y.astype(np.float32)

    print("Recibido:", audio, modelo, y.shape)

    y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)

    # Si tiene 2 canales, me quedo sólo con uno
    if y_resampled.ndim == 2:
        y_resampled = y_resampled[1]

    y /= np.max(np.abs(y_resampled))

    if modelo is None:
        modelo = "1"
    elif modelo.startswith("Modelo"):
        modelo = modelo[-1] # Nos quedamos con el dígito

    print(modelo)

    if modelo == "base" or modelo == "1":
        pipe = pipe_aspanias_mujeres
    elif modelo == "2":
        pipe = pipe_g
    elif modelo == "3":
        pipe = pipe_aspanias_completo
    else:    
        modelo = "4"
        pipe = pipe_asfeme

    resultado = pipe({"sampling_rate": sr, "raw": y})["text"]
    
    contador += 1

    print(contador, modelo, datetime.now(), resultado)

    return resultado

descripcion = """
<figure style="float: right;"><img src="https://piafplara.es/wp-content/uploads/2022/12/logoLaraFinalGrande.png" width="200" /></figure>
El proyecto <a href="https://piafplara.es">PIAFP Lara</a> se traduce en un modelo de IA para facilitar la autonomía comunicativa de las personas con trastornos en el habla.<br />

Este modelo se ha reentrenado sobre el modelo Whisper de OpenAI, y a partir de un audio, genera un texto.
"""

article = """
El proyecto Lara es un proyecto educativo cuyo objetivo es dotar de autonomía comunicativa a las personas que padecen un trastorno en el habla.
"""

demo = gr.Interface(
    transcribe,
    inputs=[
        gr.Audio(label="Grabar"),
        gr.Dropdown(
            ["Modelo 1", "Modelo 2", "Modelo 3", "Modelo 4"], label="Modelo", info="Modelos de Lara entrenados"
        )
    ],
    outputs=["text"],
    theme="soft",
    title="PIAFP Lara",
    description=descripcion,
    article=article,
    allow_flagging="auto"
#    theme="gradio/monochrome"
)

# , auth=("lara","lara"),

demo.launch(share=False, server_name="0.0.0.0", server_port=8080, ssl_verify=False, ssl_certfile="cert.pem", ssl_keyfile="key.pem",)