#import libs
import h5py
import json
import argparse
import os
from transformers import pipeline, AutoTokenizer, AutoModel
from tqdm import tqdm
from pathlib import Path
import numpy as np
import nltk

#downlaod additional lib
nltk.download('punkt')

#required arguments
parser = argparse.ArgumentParser(description='Convert TVQA dataset to new json format with video names as key and sub as value.')

parser.add_argument("--input_path", required=True, type=str, help="Input path for feature extraction pipeline.")
parser.add_argument("--output_path", required=True, type=str, help="Output path for feature extraction pipeline.")

#optional arguments
parser.add_argument("--overwrite_output", action="store_true", default="True", help="Choose if previous output should be overwritten")
parser.add_argument("--model", default="bert-base-cased", type=str, help="The model architecture used for the feature extraction pipeline.")
parser.add_argument("--config", default="bert-base-cased", type=str, help="The config used for the feature extraction pipeline.")
parser.add_argument("--tokenizer", default="bert-base-cased", type=str, help="The tokenizer used for the feature extraction pipeline.")
parser.add_argument("--device", default=-1, type=int, help="ID to determine which device to run pipeline on. -1 is CPU and 0> is GPU.")

args = parser.parse_args()

#make path competible on every OS
args.input_path = Path(args.input_path)
args.output_path = Path(args.output_path)

#initialize model and tokenizer
tokenizer = args.tokenizer
model = args.model
tokenizer = AutoTokenizer.from_pretrained(tokenizer, add_special_tokens=False)
model = AutoModel.from_pretrained(model)
wp_tokens = []
wp_token_map = []
sen1 = []
sen2 = []
counter = 0

#initialize pipeline
nlp = pipeline('feature-extraction', model=model, config=args.config, tokenizer=tokenizer, device=args.device)

#check if output path is available and delete if requested
if (
   os.path.exists(args.output_path)
   and not args.overwrite_output
):
  raise ValueError(
    "Output path ({}) already exists. Use --overwrite_output or choose a different path.".format(
      args.output_path
    )
  )

elif (
   os.path.exists(args.output_path)
   and args.overwrite_output
):
  os.remove(args.output_path)  


#run pipeline and save output in h5py file
with open(str(args.input_path), "r") as input_data:
  input_data = json.load(input_data)

for key, value in tqdm(input_data.items()):
  '''
  if len(tokenizer.encode(value)) > 512:
    sentence_list = nltk.tokenize.sent_tokenize(value)
    value_len = int(len(sentence_list)/2)
    for s in sentence_list:
      if counter < value_len:
        sen1.append(s)
        counter = counter +1
      else:
        sen2.append(s)
        counter = counter +1
    for w in sen1:
      wp_token_map.append(len(wp_tokens))
      wp_tokens.extend(tokenizer.tokenize(w))
    wp_token_map.append(len(wp_tokens))
    sen1 = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(sen1)
    features = nlp(sen1)
    features = np.asarray(features, dtype=np.float32)
    if features.shape[1] == 1:
      features = features.reshape(1,768)
    elif features.shape[1] > 1:
      features = np.squeeze(features)
      features = [
        features[wp_token_map[i]:wp_token_map[i+1]].mean(0)
        for i in range(len(wp_token_map)-1)]
      features_1 = np.stack(features)
    wp_token_map = []
    wp_tokens = []
    sen1 = []
    
    for w in sen2:
      wp_token_map.append(len(wp_tokens))
      wp_tokens.extend(tokenizer.tokenize(w))

    wp_token_map.append(len(wp_tokens))
    sen2 = nltk.tokenize.treebank.TreebankWordDetokenizer().detokenize(sen2)
    features = nlp(sen2)
    features = np.asarray(features, dtype=np.float32)
    if features.shape[1] == 1:
      features = features.reshape(1,768)
    elif features.shape[1] > 1:
      features = np.squeeze(features)
      features = [
        features[wp_token_map[i]:wp_token_map[i+1]].mean(0)
        for i in range(len(wp_token_map)-1)]
      features_2 = np.stack(features)
    wp_token_map = []
    wp_tokens = []
    sen2 = []  

    features = np.append(features_1, features_2, axis=0)   
    h5f = h5py.File(args.output_path, 'a')
    h5f.create_dataset(key, data=features)
    h5f.close()
    counter = 0
  else:
'''
  while len(tokenizer.encode(value))> 512:
    value = value.rsplit(' ', 1)[0]
  
  sentence_list = list(value.split(" "))
  
  for w in sentence_list:
    wp_token_map.append(len(wp_tokens))
    wp_tokens.extend(tokenizer.tokenize(w))
  wp_token_map.append(len(wp_tokens))

  features = nlp(value)
  features = np.asarray(features, dtype=np.float32)
    
  if features.shape[1] == 1:
    features = features.reshape(1,768)
  elif features.shape[1] > 1:
    features = np.squeeze(features)

    features = [
      features[wp_token_map[i]:wp_token_map[i+1]].mean(0)
      for i in range(len(wp_token_map)-1)]
    features = np.stack(features)

  h5f = h5py.File(args.output_path, 'a')
  h5f.create_dataset(key, data=features)
  h5f.close()
  wp_tokens = []
  wp_token_map = []
  sentence_list = []
  counter = 0
