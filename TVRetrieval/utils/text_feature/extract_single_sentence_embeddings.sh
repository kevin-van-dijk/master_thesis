#!/usr/bin/env bash
# Usage:
# bash utils/text_feature/extract_single_sentence_embeddings.sh \
# OUTPUT_ROOT FINETUNE_MODE EXTRACTION_MODE SAVE_FILEPATH
# Examples:
# bash utils/text_feature/extract_single_sentence_embeddings.sh ${output_root} sub_query sub tvr_sub_pretrained_w_sub_query.h5 MODEL_TYPE MODEL_NAME_OR_PATH --debug
# bash utils/text_feature/extract_single_sentence_embeddings.sh ${output_root} sub_query query tvr_query_pretrained_w_sub_query.h5 MODEL_TYPE MODEL_NAME_OR_PATH--debug
output_dir=$1
extraction_mode=$2  # sub or query
extracted_file_name=$3  # tvr_query_pretrained_w_sub_query.h5, will be saved at output_dir

data_root="data"
train_data_file="${data_root}/tvr_train_release.jsonl"
val_data_file="${data_root}/tvr_val_release.jsonl"
test_data_file1="${data_root}/tvr_test_public_release.jsonl"
sub_data_file="${data_root}/tvqa_preprocessed_subtitles.jsonl"

#="/net/bvisionserver14/playpen-ssd/jielei/data/tvr/bert_feature"
model_type=$4
model_name_or_path="${output_dir}/$5"
#model_name_or_path=$5

if [[ ${extraction_mode} == query ]]; then
    max_length=30
    extra_args=(--train_data_file)
    extra_args+=(${train_data_file})
    extra_args+=(${val_data_file})
    extra_args+=(${test_data_file1})
elif [[ ${extraction_mode} == sub ]]; then
    max_length=256
    extra_args=(--use_sub)
    extra_args+=(--sub_data_file)
    extra_args+=(${sub_data_file})
fi

python utils/text_feature/lm_finetuning_on_single_sentences.py \
--output_dir ${output_dir} \
--model_type ${model_type} \
--model_name_or_path ${model_name_or_path} \
--do_extract \
--extracted_file_name ${extracted_file_name} \
--block_size ${max_length} \
${extra_args[@]} \
${@:6}
