import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(description="Find the variance needed to generates standard heatmaps for every image in the dataset")
parser.add_argument("dir", help="dataset folder containing two subfolders, one for images and one for jsons")

args = parser.parse_args()

hands_folder = args.dir+'/hands'
jsons_folder = args.dir+'/jsons'
count = 1
min_variance = []

list_dir = sorted(os.listdir(hands_folder))

#print(list_dir)

for file in list_dir:
    filename = os.fsdecode(file)

    with open(jsons_folder+"/"+filename.split('.')[0]+'.json') as json_file:
        heatmap_data_json = json.load(json_file)

        center_x = 0
        center_y = 0
        number_of_point = 0
        for heatmap_num in range(21):
            coordinates = heatmap_data_json["hand_pts"][heatmap_num]

            z0 = coordinates[2]
            if z0 != 0:
                x0 = coordinates[0]
                y0 = coordinates[1]
                center_x=center_x+x0
                center_y=center_y+y0
                number_of_point=number_of_point+1
        const = 1.0
        center_x=(center_x/number_of_point)*const
        center_y=(center_y/number_of_point)*const
                    
        varx=0
        vary=0

        for heatmap_num in range(21):
            coordinates = heatmap_data_json["hand_pts"][heatmap_num]

            z0 = coordinates[2]
            if z0 != 0:
                x0 = coordinates[0]
                y0 = coordinates[1]
                varx=math.pow(center_x-x0, 2) + varx
                vary= math.pow(center_y-y0, 2) + vary
                number_of_point=number_of_point+1
        const = 0.1
        varx=(varx/number_of_point)*const
        vary=(vary/number_of_point)*const
        var = (varx + vary)/2
                
        if len(min_variance) == 0:
            min_variance.append(var)
                
        elif var < min_variance[0]:
            min_variance.pop()
            min_variance.append(var)
                       
        print(count)
        count += 1
print(min_variance[0]) 

