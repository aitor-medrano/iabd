from datasets import load_dataset
from huggingface_hub import login

# Hacemos login en HF
# login()

streaming_dataset = load_dataset("bigcode/the-stack-v2", "Dockerfile", split="train", streaming=True)
print(streaming_dataset)

def mayusLicencias(registro):
    registro["license_type"] = registro["license_type"].upper()
    return registro

mapped_dataset = streaming_dataset.map(mayusLicencias)

print(next(iter(mapped_dataset)))
