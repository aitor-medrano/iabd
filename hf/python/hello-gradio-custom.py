import gradio as gr

def saluda(nombre):
    return "Hola " + nombre + "!"


titulo = "Hola Gradio"
descripcion = """Con Gradio podemos crear prototipos visuales para probar nuestros <strong>modelos de IA</strong>

<br />

<figure style="display: flex; justify-content: center; align-items: center;">
    <img src="https://aitor-medrano.github.io/iabd/images/logoIABD3.png" alt=Logo IABD" width="100px">
</figure>
"""
articulo = "En este caso, sólo debes escribir tu *nombre* y pulsar sobre **enviar**"

demo = gr.Interface(fn=saluda, inputs="text", outputs="text", title=titulo, description=descripcion, article=articulo, theme="glass", submit_btn="enviar", fill_width=True)
demo.launch()