import gradio as gr

def updateTextbox(eleccion):
    if eleccion == "Pequeño":
        return gr.Textbox(lines=1, visible=True)
    elif eleccion == "Grande":
        return gr.Textbox(lines=6, visible=True)
    else:
        return gr.Textbox(visible=False)

demo = gr.Interface(
    updateTextbox,
    gr.Radio(
        ["Pequeño", "Grande", "Sin mensaje"], label="¿Qué tipo de mensaje quieres enviar?"
    ),
    gr.Textbox(lines=2)
)

demo.launch()