import gradio as gr

with gr.Blocks() as demo:
    gr.DateTime()
    gr.DateTime(label="Solo fecha", include_time=False)
    
demo.launch()