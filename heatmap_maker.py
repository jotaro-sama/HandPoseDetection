import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description="Resizes dataset and generates heatmaps")
parser.add_argument("dir", help="dataset folder containing two subfolders, one for images and one for jsons")
parser.add_argument("sizeX", help="new X size")
parser.add_argument("sizeY", help="new Y size")
parser.add_argument("variance", help="variance for gaussians")

args = parser.parse_args()

resized_images_folder_name = "resized"
if not os.path.exists(resized_images_folder_name):
    os.makedirs(resized_images_folder_name)

heatmaps_folder_name = "heatmaps" 
if not os.path.exists(heatmaps_folder_name):
    os.makedirs(heatmaps_folder_name)

NET_IMAGE_SIZE = (int(args.sizeX), int(args.sizeY))

hands_folder = args.dir+'/hands'
jsons_folder = args.dir+'/jsons'
count = 1

list_dir = sorted(os.listdir(hands_folder))

for file in list_dir:
    filename = os.fsdecode(file)

    if filename.endswith(".jpg"):
        #print(filename)
        with Image.open(hands_folder+"/"+file) as img:
            old_size = img.size
            #print(old_size)
                
            if old_size != NET_IMAGE_SIZE:
                img = img.resize(size=NET_IMAGE_SIZE, resample=PIL.Image.BILINEAR)
                
            img = img.save(resized_images_folder_name+'/'+ str(count)+'.jpg')

            with open(jsons_folder+"/"+filename.split('.')[0]+'.json') as json_file:
                heatmap_data_json = json.load(json_file)

                for heatmap_num in range(21):
                    coordinates = heatmap_data_json["hand_pts"][heatmap_num]
                    #print(coordinates)

                    image = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))
                    visited = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))

                    z0 = coordinates[2]
                    if z0 != 0:
                        x0 = coordinates[0]
                        y0 = coordinates[1]
                    
                        var = float(args.variance)

                        #since we resized the input image, we need to scale coordinates
                        ratioX = NET_IMAGE_SIZE[0]/old_size[0]
                        ratioY = NET_IMAGE_SIZE[1]/old_size[1]

                        for i, row in enumerate(image):
                            for j, pixel in enumerate(row):
                                image[i][j] = math.exp((- (((i-(x0*ratioX))**2/var) + ((j-(y0*ratioY))**2/var))))
                    
                    greyscale = Image.fromarray(image * 255).convert("L")
                    #print(heatmap_num)
                    heatmap_filename = "heatmaps/" + str(count) + "_" + str(heatmap_num+1) + ".png"
                    #print(heatmap_filename)
                    greyscale = greyscale.save(heatmap_filename)
                        
                print(count)
                count += 1
