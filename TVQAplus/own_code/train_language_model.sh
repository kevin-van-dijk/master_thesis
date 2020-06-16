#!/usr/bin/env bash
# Usage: bash own_code/train_language_model.sh OUTPUT_DIR MODEL_TYPE MODEL_NAME_OR_PATH EPOCHS
output_dir=$1 #dir name e.g. bert-base-uncased_epoch-3_no-gradient
output_path="/home/kevin/transformer_features_tvqa/${output_dir}"
train_data_file="/home/kevin/TVQAplus/converted_text_data/data_for_finetuning.txt"
model_type=$2 #e.g. bert
model_name_or_path=$3 #e.g. bert-base-uncased
epochs=$4 #e.g. 3

python run_language_modeling.py \
--train_data_file ${train_data_file} \
--output_dir ${output_path} \
--model_type ${model_type} \
--line_by_line \
--model_name_or_path ${model_name_or_path} \
--block_size 512 \
--do_train \
--gradient_accumulation_steps 4 \
--learning_rate 5e-5 \
--num_train_epochs ${epochs} \
--save_total_limit 3 \
--overwrite_output_dir \
--overwrite_cache \
${@:5}
