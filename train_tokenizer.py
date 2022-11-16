# pip install git+https://github.com/huggingface/transformers

d = "/home/jp/Workspace/nlp/notebooks"

from pathlib import Path

from tokenizers import ByteLevelBPETokenizer

paths = [str(x) for x in Path(d).glob("**/*.txt")]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=paths, vocab_size=30_000, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

tokenizer.save_model(d)