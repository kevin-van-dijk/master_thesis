#import libs
import  argparse
import json
import os
from tqdm import tqdm
from pathlib import Path

#add arguments to script
parser = argparse.ArgumentParser(description='Convert TVQA dataset to new json format with video names as key and sub as value.')
parser.add_argument('--input_path_train', type=str, help='Input file for train annotations')
parser.add_argument('--input_path_val', type=str, help='Input file for val annotations')
parser.add_argument('--input_path_test', type=str, help='Input file for test annotations')
parser.add_argument('--output_path', type=str, required=True, help='output file for json of q and a')
parser.add_argument('--overwrite_output', action='store_true', help='Overwrite the content of the output directory')
args = parser.parse_args()

#initialize variables
qa_dict = {}

#for convenience sake
def load_json(filename):
    with open(filename, "r") as f:
        return json.load(f)

#start collecting all questions and answers in dict
def create_dict(tvqa_anno_path):
    
    #initialize variables
    #qa_dict = {}
    counter = 1

    for d in tqdm(load_json(tvqa_anno_path), desc="Loading data"):

        a0 = d.get('a0')
        a1 = d.get('a1')
        a2 = d.get('a2')
        a3 = d.get('a3')
        a4 = d.get('a4')
        q = d.get('q')
        qid = d.get('qid')
        
        #loop through all answers and questions
        if counter == 1:
            qa_name = str(qid) + "_" + "a0"
            qa_dict[qa_name] = a0
            counter = counter + 1
        if counter == 2:
            qa_name = str(qid) + "_" + "a1"
            qa_dict[qa_name] = a1
            counter = counter + 1
        if counter == 3:
            qa_name = str(qid) + "_" + "a2"
            qa_dict[qa_name] = a2
            counter = counter + 1
        if counter == 4:
            qa_name = str(qid) + "_" + "a3"
            qa_dict[qa_name] = a3
            counter = counter + 1
        if counter == 5:
            qa_name = str(qid) + "_" + "a4"
            qa_dict[qa_name] = a4
            counter = counter + 1
        if counter == 6:
            qa_name = str(qid) + "_" + "q"
            qa_dict[qa_name] = q
            counter = counter + 1
        if counter == 7:
            counter = 1
    return qa_dict

#make path competible on every OS and create dict with data
if args.input_path_train is not None:
    input_path_train = Path(args.input_path_train)
    create_dict(input_path_train)

if args.input_path_val is not None:
    input_path_val = Path(args.input_path_val)
    create_dict(input_path_val)

if args.input_path_test is not None:
    input_path_test = Path(args.input_path_test)
    create_dict(input_path_test)

#OS compatability
args.output_path = Path(args.output_path)

#Sanity check on output
if (os.path.exists(args.output_path) and not args.overwrite_output):
    raise ValueError(
        "Output directory ({}) already exists and is not empty. Use --overwrite_output_dir to overcome.".format(args.output_path))

if (os.path.exists(args.output_path) and args.overwrite_output):
    os.remove(args.output_path)

#write dict to json file    
with open(str(args.output_path), 'w', newline='') as q_and_a:
    json.dump(qa_dict, q_and_a)
