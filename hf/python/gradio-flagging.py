import gradio as gr

def calcula(num1, operacion, num2):
    if operacion == "suma":
        return num1 + num2
    elif operacion == "resta":
        return num1 - num2
    elif operacion == "producto":
        return num1 * num2
    elif operacion == "división":
        return num1 / num2


demo = gr.Interface(
    calcula,
    ["number", gr.Radio(["suma", "resta", "producto", "división"]), "number"],
    "number",
    flagging_mode="manual",
    flagging_options=["signo incorrecto", "división por cero", "otro"]
)

demo.launch()