import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description="Resizes dataset and generates heatmaps")
parser.add_argument("dir", help="images to be renamed")
parser.add_argument("start", help="start from")
args = parser.parse_args()

hands_folder = args.dir+'/hands'
heatmaps_folder = args.dir+'/heatmaps'
count = int(args.start)

list_dir = sorted(os.listdir(hands_folder))

for file in list_dir:
    filename = os.fsdecode(file)
    num = filename.split('.')[0]

    i = 1
    for i in range(1,6):
        os.rename(heatmaps_folder+'/'+ num +"_"+str(i)+".png", heatmaps_folder+'/' + str(count) +"_"+str(i)+".png")
    
    os.rename(hands_folder +'/'+ filename, hands_folder +'/'+str(count)+'.jpg')
    count = count +1
