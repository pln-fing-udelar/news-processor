#!/bin/sh

echo conda ENV: $CONDA_DEFAULT_ENV

python src/run_mlm.py \
    --model_type roberta \
    --config_name '/clusteruy/home03/fing-pln-llm/models/modelo_notibert/tokenizer/config.json' \
    --train_file '/clusteruy/home03/fing-pln-llm/datasets/all_together.txt' \
    --tokenizer_name '/clusteruy/home03/fing-pln-llm/models/modelo_notibert/tokenizer' \
    --output_dir '/clusteruy/home03/fing-pln-llm/models/modelo_notibert/out' \
    --per_device_train_batch_size 32 \
    --do_train \
    --max_seq_length 128 \
    --save_total_limit 2 \
    --ignore_data_skip \
    --num_train_epochs 1
    # --fp16 \
    # --max_steps 100
    #  --num_train_epochs 1 \
    # --overwrite_output_dir

# para correr en batch:
# sbatch --job-name=20221116_bert_train --ntasks=1 --mem=12G --time=119:00:00 --partition=normal --qos=gpu --gres=gpu:1 --mail-type=ALL train.sh 