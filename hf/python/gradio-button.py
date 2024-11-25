import gradio as gr

def combinar(a, b):
    return "¡Hola " + a + " " + b + '!\n'+ " Bienvenido a IABD"

with gr.Blocks() as demo:  
    txtIn1 = gr.Textbox(label="Nombre", lines=2)
    txtIn2 = gr.Textbox(label="Apellidos")
    txtOut = gr.Textbox(value="", label="Salida")
    btn = gr.Button(value="Enviar")

    btn.click(combinar, inputs=[txtIn1, txtIn2], outputs=[txtOut])

demo.launch()