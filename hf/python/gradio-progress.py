import gradio as gr

def show_text(x):
    return x

demo = gr.Blocks()

with demo:
    gr.Markdown(
    """
    # Show text!
    Start typing below to see the output.
    """
    )
    input = gr.Textbox(placeholder="Flip this text")
    output = gr.Textbox()

    input.change(fn=show_text, inputs=input, outputs=output, show_progress = True)

demo.launch()