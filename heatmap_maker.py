import json
import numpy as np
import math
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description="Take the filename of the json file for which to generate the heatmaps")
parser.add_argument("file", help="Properly formatted json file with the coordinates of the hand joints.")
args = parser.parse_args()

heatmaps_folder_name = "heatmaps" 
if not os.path.exists(heatmaps_folder_name):
    os.makedirs(heatmaps_folder_name)

with open(args.file) as file:
    image_1_data = json.load(file)
    for heatmap_num in range(21):
        coordinates_1 = image_1_data["hand_pts"][heatmap_num]
        #print(coordinates_1)

        size = 328
        image = np.zeros((size, size))
        visited = np.zeros((size, size))

        x0 = coordinates_1[0]
        y0 = coordinates_1[1]
        # image[x0][y0] = 1

        varx, vary = 50, 50

        for i, row in enumerate(image):
            for j, pixel in enumerate(row):
                image[i][j] = math.exp((- (((i-x0)**2/varx) + ((j-y0)**2/vary))))

        

        greyscale = Image.fromarray(image * 255).convert("L")
        #greyscale.show()
        print(heatmap_num)
        heatmap_filename = "heatmaps/" + args.file.split("/")[1].split(".")[0] + "_" + str(heatmap_num).zfill(4) + ".png"
        print(heatmap_filename)
        greyscale = greyscale.save(heatmap_filename)