from diffusers import DiffusionPipeline
import torch

pipeline = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
# pipeline.to("cuda")
pipeline("Una imagen de una ardilla al estilo Picasso").images[0].save("hola-hf.png")