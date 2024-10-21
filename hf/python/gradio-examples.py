import gradio as gr

def saluda(nombre):
    return "Hola " + nombre + "!"

demo = gr.Interface(fn=saluda, inputs="text", outputs="text", examples=["Aitor", "IABD", "¿Qué tal?"])
demo.launch()