#import libs
import  argparse
import json
from tqdm import tqdm
from pathlib import Path
import numpy as np
import re
import os

#add arguments to script
parser = argparse.ArgumentParser(description='Convert TVQA dataset to new json format with video names as key and sub as value.')
parser.add_argument('--input_path', type=str, required=True, help='Input file for subs')
parser.add_argument('--output_path', type=str, required=True, help='output file for json of video and sub')
parser.add_argument('--overwrite_output', action='store_true', help='Overwrite the output')
args = parser.parse_args()

#make path competible on every OS
args.input_path = Path(args.input_path)
args.output_path = Path(args.output_path)

#load data from sub file
with open(str(args.input_path),"r") as tvqa_sub:
    tvqa_sub = json.load(tvqa_sub)

#initialize variables
s = 1 #initialize season
e = 1 #initialize episode
seg = 1 #initialize segment
clip = 0 #initialize clip
vid_name = "s{0:0=2d}".format(s) + "e{0:0=2d}".format(e) + "_" + "seg{0:0=2d}".format(seg) + "_" + "clip_{0:0=2d}".format(clip)
dict_vid_and_sub = {}

#start collecting all subs and vidoes in dict
while s < 11:

    try:
        if tvqa_sub[vid_name]:
            
            #get subtitles relevant to video
            tvqa_sub_text = tvqa_sub[vid_name]["sub_text"]
            
            #formating of subtitles
            tvqa_sub_text = tvqa_sub_text.split(" <eos> ")
            tvqa_sub_text = (" ".join(tvqa_sub_text))
            tvqa_sub_text = tvqa_sub_text.replace("\n", " ")
            tvqa_sub_text = tvqa_sub_text.replace(")", " ")
            tvqa_sub_text = tvqa_sub_text.replace("(", " ")
            tvqa_sub_text = tvqa_sub_text.replace(":", " : ")
            tvqa_sub_text = re.sub(r"\s{2,}", " ", tvqa_sub_text)
           
            #add subtitles to final list
            vid_name = str(vid_name)
            dict_vid_and_sub[vid_name] = tvqa_sub_text
            
            if clip <= 30:
                clip = clip + 1
                
                if clip >= 30:
                    clip = 0
                    seg = seg + 1

                    if seg >= 5:
                        clip = 00
                        seg = 00
                        e = e + 1

                        if e >= 30:
                            clip = 00
                            seg = 00
                            e = 00
                            s = s + 1
            vid_name = "s{0:0=2d}".format(s) + "e{0:0=2d}".format(e) + "_" + "seg{0:0=2d}".format(seg) + "_" + "clip_{0:0=2d}".format(clip)
    except:   

        if clip <= 30:
            clip = clip + 1
                
            if clip >= 30:
                clip = 0
                seg = seg + 1

                if seg >= 5:
                    clip = 00
                    seg = 00
                    e = e + 1

                    if e >= 30:
                        clip = 00
                        seg = 00
                        e = 00
                        s = s + 1
        vid_name = "s{0:0=2d}".format(s) + "e{0:0=2d}".format(e) + "_" + "seg{0:0=2d}".format(seg) + "_" + "clip_{0:0=2d}".format(clip)

#Sanity check on output
if (os.path.exists(args.output_path) and not args.overwrite_output):
    raise ValueError(
        "Output directory ({}) already exists and is not empty. Use --overwrite_output to overcome.".format(args.output_dir))

if (os.path.exists(args.output_path) and args.overwrite_output):
    os.remove(args.output_path)

#write dict to json file
with open(str(args.output_path), 'w', newline='') as vid_and_sub:
    json.dump(dict_vid_and_sub, vid_and_sub)
print("Finished")
