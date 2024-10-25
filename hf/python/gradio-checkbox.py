import gradio as gr

def crearFrase(tipo, listaActividades):
    return f"""Se agradece un café {"cargado" if tipo else "suave"} acompañado de {" y ".join(listaActividades)}"""

demo = gr.Interface(
    crearFrase,
    [
        gr.Checkbox(label="Cargado"),
        gr.CheckboxGroup(label="Café con...", choices=["tostadas", "galletas", "magdalenas", "las noticias"]),
    ],
    "text")

demo.launch()