# 1- Obtengo dataset

# to do: chequear en este punto que tenga el dataset

# 2- Entrenar tokenizer

import os
import shutil
import torch
from os import path
from pathlib import Path
from tokenizers import ByteLevelBPETokenizer
from tokenizers.implementations import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
from transformers import RobertaConfig
from transformers import RobertaTokenizerFast
from transformers import RobertaForMaskedLM
from transformers import LineByLineTextDataset
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments

vocab_size = 30_522
paths = [str(x) for x in Path(".").glob("**/*.txt")]

# Initialize a tokenizer
tokenizer = ByteLevelBPETokenizer()

# Customize training
tokenizer.train(files=paths, vocab_size=vocab_size, min_frequency=2, special_tokens=[
    "<s>",
    "<pad>",
    "</s>",
    "<unk>",
    "<mask>",
])

if(os.path.isdir('UruNotiBERTo')):
    shutil.rmtree('UruNotiBERTo')

os.makedirs('UruNotiBERTo')

tokenizer.save_model("UruNotiBERTo")

tokenizer = ByteLevelBPETokenizer(
    "./UruNotiBERTo/vocab.json",
    "./UruNotiBERTo/merges.txt",
)

tokenizer._tokenizer.post_processor = BertProcessing(
    ("</s>", tokenizer.token_to_id("</s>")),
    ("<s>", tokenizer.token_to_id("<s>")),
)
tokenizer.enable_truncation(max_length=512)

#3- Entreno un modelo BERT from scratch
print(f'cuda available {torch.cuda.is_available()}')

# Parametros del modelo

config = RobertaConfig(
    vocab_size=vocab_size,
    max_position_embeddings=514,
    num_attention_heads=12,
    num_hidden_layers=6,
    type_vocab_size=1,
)

tokenizer = RobertaTokenizerFast.from_pretrained("./UruNotiBERTo", max_len=512)

# Finally let's initialize our model.
# Important:
# As we are training from scratch, we only initialize from a config, not from an existing pretrained model or checkpoint.

model = RobertaForMaskedLM(config=config)

# 4- Creo dataset con el tokenizer
# Aplico el dataset al archivo de textos.
# Por ahora solo se aplica a un archivo, tengo que ver como se hace cuando tengo mas de uno
# Here, as we only have one text file, we don't even need to customize our Dataset. We'll just use the LineByLineDataset out-of-the-box.

dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path=paths[0],
    block_size=128,
)

# Like in the run_language_modeling.py script, we need to define a data_collator. This is just a small helper that will help us batch different samples of the dataset together into an object that PyTorch knows how to perform backprop on.

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# initialize Trainer
training_args = TrainingArguments(
    output_dir="./UruNotiBERTo",
    overwrite_output_dir=True,
    num_train_epochs=1,
    per_device_train_batch_size=64,
    save_steps=10_000,
    save_total_limit=2,
    prediction_loss_only=True,
) 

trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset,
)

# Start trainig
trainer.train()

# Save final model (+ tokenizer + config) to disk
trainer.save_model("./UruNotiBERTo")

# 4. chack that the lm actually trained

from transformers import pipeline

fill_mask = pipeline(
    "fill-mask",
    model="./UruNotiBERTo",
    tokenizer="./UruNotiBERTo"
)

print('test Mujica')
print(fill_mask("Mujica <mask>."))
print('test QEPD')
print(fill_mask("Q.E.P.D. Falleció en la Paz del <mask>."))
