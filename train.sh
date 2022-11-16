echo conda ENV: $CONDA_DEFAULT_ENV

python run_mlm.py \
    --model_type roberta \
    --config_name '/home/jp/Workspace/nlp/notebooks/roberta-from-scratch/config.json' \
    --train_file '/home/jp/Downloads/data/OSCAR/oscar.eo.txt' \
    --tokenizer_name '/home/jp/Workspace/nlp/notebooks/roberta-from-scratch' \
    --output_dir '/home/jp/Workspace/nlp/notebooks/roberta-from-scratch/out' \
    --per_device_train_batch_size 32 \
    --do_train \
    --max_seq_length 128 \
    --save_total_limit 1 \
    --ignore_data_skip
    # --fp16 \
    # --max_steps 100
    # --num_train_epochs 1 \
    # --overwrite_output_dir
