import json
import numpy as np
import math
from PIL import Image
import argparse
import os


heatmaps_folder_name = "heatmaps" 
if not os.path.exists(heatmaps_folder_name):
    os.makedirs(heatmaps_folder_name)
size=328    
merge=np.zeros((328,328)) 

for i in range(1,22):    
    img=Image.open("heatmaps/0001_"+str(i)+".png")
    mat=img.load()   
    for r in range(0,size):
        for c in range(0,size):
            merge[r,c]=mat[r,c]+merge[r,c]            			
			
greyscale = Image.fromarray(merge * 255).convert("L")
greyscale.show()		

    

