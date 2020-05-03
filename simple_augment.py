import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os

np.random.seed(473683) #put here your random seed

parser = argparse.ArgumentParser(description="augment dataset")
parser.add_argument("dir", help="images to be augmented")
parser.add_argument("num_samples", help="total numeber of images in dataset, the algorithm will double it by starting from that number + 1")
args = parser.parse_args()

hands_folder = args.dir+'/resized'
heatmaps_folder = args.dir+'/heatmaps'
count = int(args.num_samples)+1
augmented_folder = "augmented"

if not os.path.exists(args.dir + "/" + augmented_folder):
    os.makedirs(args.dir + "/" + augmented_folder)

augmented_resized = args.dir + "/" + augmented_folder+ "/resized"
augmented_heatmaps = args.dir + "/" + augmented_folder+ "/heatmaps"

if not os.path.exists(augmented_resized):
    os.makedirs(augmented_resized)

if not os.path.exists(augmented_heatmaps):
    os.makedirs(augmented_heatmaps)



list_dir = sorted(os.listdir(hands_folder))

for file in list_dir:
    filename = os.fsdecode(file)
    num = filename.split('.')[0]
    rand = np.random.rand()
    angle = 0

    if (rand <= 0.33): #rotate right once
        angle -90
    
    elif (rand > 0.33) and (rand <= 0.66): # rotate left once
        angle = 90
    
    elif rand > 0.66: # rotate right twice
        angle = -180


    with Image.open(hands_folder+"/"+file) as img:
            #rotate image
            img2 = img.rotate(angle)
            
            #save
            img2.save(augmented_resized +'/'+ str(count)+'.jpg')

    i = 1
    for i in range(1,6):
        with Image.open(heatmaps_folder+ "/" + num + "_" + str(i) +".png") as img:
            #rotate
            img2 = img.rotate(angle)

            #save
            img2.save(augmented_heatmaps+ "/" + str(count) + "_" + str(i) +".png")

    count = count +1

