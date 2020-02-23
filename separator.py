import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os
import shutil

parser = argparse.ArgumentParser(description="Takes the original dataset folder containing synth folders and separates images from jsons")
parser.add_argument("dir", help="synth dataset outmost folder")

args = parser.parse_args()

hands = "hands"
if not os.path.exists(hands):
    os.makedirs(hands)


jsons = "jsons"
if not os.path.exists(jsons):
    os.makedirs(jsons)

synth_folder = args.dir+'/synth'+'{}'
for idx in range(1, 5): #range should go to 1 to 4 included, since synth# folders are 4
    folder = synth_folder.format(idx)
    #print(folder)
    #print(os.listdir(folder))
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        if filename.endswith(".jpg"):
          print(filename)
          shutil.copy(folder+"/"+filename, hands+"/")
        
        if filename.endswith(".json"):
          print(filename)
          shutil.copy(folder+"/"+filename, jsons+"/")