#!/usr/bin/env bash
# Usage: bash utils/text_feature/train_lm_finetuning_single_sentence.sh FINETUNE_MODE OUTPUT_ROOT MODEL_TYPE MODEL_NAME_OR_PATH EPOCHS OUTPUT_DIR
finetune_mode=$1  # [query_only, sub_query]
output_root=$2  # path to store the generated output
data_root="data"
train_data_file="${data_root}/tvr_train_release.jsonl"
sub_data_file="${data_root}/tvqa_preprocessed_subtitles.jsonl"
model_type=$3
model_name_or_path=$4

num_train_epochs=$5
output_dir="${output_root}/$6"

if [[ ${finetune_mode} == query_only ]]; then
    max_length=32
    gradient_accumulation_steps=1

    extra_args=()
elif [[ ${finetune_mode} == sub_query ]]; then
    max_length=256  # since sub is longer
    gradient_accumulation_steps=8

    extra_args=(--use_sub)
    extra_args+=(--sub_data_file)
    extra_args+=(${sub_data_file})
fi

python utils/text_feature/lm_finetuning_on_single_sentences.py \
--output_dir ${output_dir} \
--model_type ${model_type} \
--model_name_or_path ${model_name_or_path} \
--do_train \
--train_data_file ${train_data_file} \
--gradient_accumulation_steps ${gradient_accumulation_steps} \
--block_size ${max_length} \
--num_train_epochs ${num_train_epochs} \
${extra_args[@]} \
${@:7}
