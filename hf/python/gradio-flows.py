import gradio as gr

def saludar(nombre, hora):
    texto_hora = "¡Buenos días!" if int(hora) <= 12 else "¡Buenas tardes!" 
    return f"{texto_hora} ¡Bienvenido a Gradio, {nombre}!"

def despedir(nombre, hora):
    texto_hora = "¡A disfrutar!" if int(hora) <= 12 else "¡Mañana más!"
    return f"{texto_hora} ¡Hasta la próxima con Gradio, {nombre}!"


with gr.Blocks() as demo:
    nombre = gr.Textbox(placeholder="¿Cómo te llamas?", label="Nombre")
    hora = gr.Number(label="Hora", value="8")
    out = gr.Textbox(label="Salida")

    btnSaluda = gr.Button("Saludar")
    btnSaluda.click(fn=saludar, inputs=[nombre, hora], outputs=out)

    btnDespide = gr.Button("Despedir")
    btnDespide.click(fn=despedir, inputs=[nombre, hora], outputs=out)

demo.launch()