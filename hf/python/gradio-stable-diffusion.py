import gradio as gr
from diffusers import DiffusionPipeline
import torch


def stable(prompt):
    pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
    # pipeline.to("cuda")
    return pipeline(prompt).images[0]

demo = gr.Interface(fn=stable, inputs="text", outputs="image")
demo.launch()