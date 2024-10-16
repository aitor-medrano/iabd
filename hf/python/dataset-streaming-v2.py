from datasets import load_dataset

dataset = load_dataset('oscar-corpus/OSCAR-2201', 'en', split='train', streaming=True)
print(dataset)