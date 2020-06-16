#!/usr/bin/env bash
# Usage: bash own_code/train_language_model.sh OUTPUT_FILE EXTRACT_MODE MODEL_TYPE MODEL_NAME_OR_PATH
output_file=$1 #file name e.g. bert_sub.h5
extract_mode=$2 #[sub, qa] weither to extract sub or qa
model_type=$3 #e.g. bert
model_name_or_path=$4 #e.g. bert-base-uncased_epoch-3_no-gradient
root_path="/home/kevin/transformer_features_tvqa"
#output_path="${root_path}/${model_name_or_path}/${output_file}"
output_path="${root_path}/${model_name_or_path}_epoch-0_4-gradient/${output_file}"


if [[ ${extract_mode} == sub ]]; then
    extract_data_file="/home/kevin/TVQAplus/converted_text_data/sub_data_for_feature_extraction.json"
    max_length=512
elif [[ ${extract_mode} == qa ]]; then
    extract_data_file="/home/kevin/TVQAplus/converted_text_data/qa_data_for_feature_extraction.json"
    max_length=64 #max sentence length is <64
fi

python run_language_modeling.py \
--extracted_data_file ${extract_data_file} \
--extracted_output_file ${output_path} \
--line_by_line \
--model_type ${model_type} \
--model_name_or_path ${model_name_or_path} \
--block_size ${max_length} \
--do_extract \
--overwrite_output_dir \
--overwrite_cache \
${@:5} 

#--model_name_or_path "${root_path}/${model_name_or_path}" \

