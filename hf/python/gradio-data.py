import gradio as gr

def mostrarDatos(datos):
    return datos

demo = gr.Interface(mostrarDatos, gr.Dataframe(), "dataframe")
demo.launch()