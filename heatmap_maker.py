import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description="Take the filename of the json file for which to generate the heatmaps")
parser.add_argument("dir", help="synth dataset outmost folder")
parser.add_argument("sizeX", help="new X size")
parser.add_argument("sizeY", help="new Y size")

args = parser.parse_args()

resized_images_folder_name = "resized"
if not os.path.exists(resized_images_folder_name):
    os.makedirs(resized_images_folder_name)

heatmaps_folder_name = "heatmaps" 
if not os.path.exists(heatmaps_folder_name):
    os.makedirs(heatmaps_folder_name)

NET_IMAGE_SIZE = (int(args.sizeX), int(args.sizeY))

synth_folder = args.dir+'/synth'+'{}'
#synth_json_folder = args.dir+'/synth'+'{}'+'json'
for idx in range(1, 5): #range should go to 1 to 4 included, since synth# folders are 4
    folder = synth_folder.format(idx)
    print(folder)
    for file in os.listdir(folder):
        filename = os.fsdecode(file)

        if filename.endswith(".jpg"):
            print(filename)
            with Image.open(folder+"/"+file) as img:
                old_size = img.size
                print(old_size)
                
                if old_size != NET_IMAGE_SIZE:
                    img = img.resize(size=NET_IMAGE_SIZE, resample=PIL.Image.BICUBIC)
                
                img = img.save(resized_images_folder_name+'/'+filename)

                with open(folder+"/"+filename.split('.')[0]+'.json') as json_file:
                    heatmap_data_json = json.load(json_file)
                    for heatmap_num in range(21):
                        coordinates = heatmap_data_json["hand_pts"][heatmap_num]
                        print(coordinates)

                        image = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))
                        visited = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))

                        z0 = coordinates[2]
                        if z0 != 0:
                            x0 = coordinates[0]
                            y0 = coordinates[1]
                    
                            varx, vary = 3, 3

                            #since we resized the input image, we need to scale coordinates
                            ratioX = NET_IMAGE_SIZE[0]/old_size[0]
                            ratioY = NET_IMAGE_SIZE[1]/old_size[1]

                            for i, row in enumerate(image):
                                for j, pixel in enumerate(row):
                                    image[i][j] = math.exp((- (((i-(x0*ratioX))**2/varx) + ((j-(y0*ratioY))**2/vary))))
                    
                        greyscale = Image.fromarray(image * 255).convert("L")
                        #greyscale.show()
                        print(heatmap_num)
                        heatmap_filename = "heatmaps/" + filename.split(".")[0] + "_" + str(heatmap_num+1) + ".png"
                        print(heatmap_filename)
                        greyscale = greyscale.save(heatmap_filename)

