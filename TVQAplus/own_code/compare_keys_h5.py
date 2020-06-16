#import libs
import h5py
import argparse
import numpy as np
from pathlib import Path
from tqdm import tqdm

#required arguments
parser = argparse.ArgumentParser(description='Compare extracted features to check if no keys are missing')

parser.add_argument("--input_path", required=True, type=str, help="Input path for extracted features.")
parser.add_argument("--output_path", required=True, type=str, help="Output path for extracted features.")

args = parser.parse_args()

#make path competible on every OS
args.input_path = Path(args.input_path)
args.output_path = Path(args.output_path)


#Open h5py files
print('open h5py files')
own = h5py.File(str(args.input_path), 'r')
target = h5py.File(str(args.output_path), 'r')

#Load keys
print('loading keys')
list_own = list(own.keys())
list_target = list(target.keys())

#compare keys
print('comparing keys')
difference = (set(list_target).difference(list_own))

total_keys = []
print('comparing shapes')
for i in tqdm(list_own):
    own_shape = own[i].shape
    target_shape = target[i].shape
    own_dtype = own[i].dtype
    target_dtype = target[i].dtype
     
    if not own_shape == target_shape:
        total_keys.append(i)
        print(i)
        print(own_shape)
        print(target_shape)
        print(" ")
  
    if not own_dtype == target_dtype:
        total_keys.append(i)
        print(i)
        print(own_dtype)
        print(target_dtype)
        print(" ")

    if np.any(np.isnan(own[i])):
        print("This key has nan:", i)

    if np.any(np.isnan(target[i])):
        print("This key has nan:", i)

    if np.any(np.isinf(own[i])):
        print("This key has inf:", i)

    if np.any(np.isinf(target[i])):
        print("This key has inf:", i)

print("amount of datasets with different shape:", len(total_keys))
#print amount of different keys (0 is good)
print("one file has the following amount of extra datasets:", len(difference))
print("differences:", difference)
