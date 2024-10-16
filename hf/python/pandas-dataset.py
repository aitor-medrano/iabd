from huggingface_hub import hf_hub_download
import pandas as pd

REPO_ID = "aitor-medrano/iabd"
FICHERO = "cp_train.csv"

dataset = pd.read_csv(
    hf_hub_download(repo_id=REPO_ID, filename=FICHERO, repo_type="dataset")
)
print(dataset.info())