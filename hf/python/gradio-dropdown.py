import gradio as gr
import time

def crearFrase(fecha, cantidad, tipo, listaActividades, media):
    return f"A las {cantidad} me {"tomé" if fecha < time.time() else "tomaré"} un café {"cargado" if tipo else "suave"} acompañado de {" y ".join(listaActividades)} o ver {media}"

demo = gr.Interface(
    crearFrase,
    [
        gr.DateTime(label="Fecha...", value="now", include_time=False),
        gr.Slider(label="Hora...", minimum=2, maximum=24, value=8, step=2),
        gr.Checkbox(label="Cargado"),
        gr.CheckboxGroup(label="Café con...", choices=["tostadas", "galletas", "magdalenas", "las noticias"]),
        gr.Dropdown(["una serie", "una película", "un documental", "un concierto"])
    ],
    "text")

demo.launch()