#import libs
import argparse
import json
import os
import re
from tqdm import tqdm
from pathlib import Path

#add arguments to script
parser = argparse.ArgumentParser(description='Convert TVQA dataset to new json format with video names as key and sub as value.')
parser.add_argument('--input_path_train', type=str, help='Input file for train annotations')
parser.add_argument('--input_path_val', type=str, help='Input file for valid annotations')
parser.add_argument('--input_path_test', type=str, help='Input file for test annotations')
parser.add_argument('--input_path_sub', type=str, required=True, help='Input file for sub data')
parser.add_argument('--output_path', type=str, required=True, help='Output file location')
parser.add_argument('--overwrite_output', action='store_true', help='Overwrite the output')
args = parser.parse_args()

#for convenience sake
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

def create_dict(tvqa_input_path, input_path_sub, tvqa_output_path):
    tvqa_sub = load_json(input_path_sub)
    with open(tvqa_output_path, "a+") as tvqa_new:
        for d in tqdm(load_json(tvqa_input_path), desc="Loading and writing data"):
            vid_name = d.get('vid_name')
            
            subtitles = tvqa_sub[vid_name]['sub_text']
            subtitles = subtitles.replace(' <eos> ', ' ')
            subtitles = subtitles.replace("(", " ")
            subtitles = subtitles.replace(")", " ")
            subtitles = subtitles.replace(":", " : ")
            subtitles = re.sub(r"\s{2,}", " ", subtitles)
            
            question = d.get('q')
            answer_num = d.get('answer_idx')
            correct_answer = 'a{}'.format(answer_num)
            correct_answer = d.get(correct_answer)
    
            tvqa_new.write(str(subtitles))
            tvqa_new.write(str('\n\n'))
            tvqa_new.write(str(question))
            tvqa_new.write(str('\n'))
            tvqa_new.write(str(correct_answer))
            tvqa_new.write(str('\n\n\n\n'))

#OS compatability
output_path = Path(args.output_path)
sub_path = Path(args.input_path_sub)

#Sanity check on output
if (os.path.exists(args.output_path) and not args.overwrite_output):
    raise ValueError(
        "Output directory ({}) already exists and is not empty. Use --overwrite_output_dir to overcome.".format(args.output_dir))    

if (os.path.exists(args.output_path) and args.overwrite_output):
    os.remove(args.output_path)

#Create and save output
if args.input_path_train is not None:
    input_path_train = Path(args.input_path_train)
    create_dict(input_path_train, sub_path, output_path)

if args.input_path_val is not None:
    input_path_val = Path(args.input_path_val)
    create_dict(input_path_val, sub_path, output_path)

if args.input_path_test is not None:
    input_path_test = Path(args.input_path_test)
    create_dict(input_path_test, sub_path, output_path)
