import gradio as gr
import time

def crearFrase(fecha, cantidad, tipo, listaActividades):
    return f"A las {cantidad} me {"tomé" if fecha < time.time() else "tomaré"} un café {"cargado" if tipo else "suave"} acompañado de {" y ".join(listaActividades)}"

demo = gr.Interface(
    crearFrase,
    [
        gr.DateTime(label="Fecha...", include_time=False),
        gr.Slider(label="Hora...", minimum=2, maximum=24, value=8, step=2),
        gr.Checkbox(label="Cargado"),
        gr.CheckboxGroup(label="Café con...", choices=["tostadas", "galletas", "magdalenas", "las noticias"])
    ],
    "text")

demo.launch()