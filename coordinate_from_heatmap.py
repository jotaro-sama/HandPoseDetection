import json
import numpy as np
import math
from PIL import Image
import argparse
import os

heatmaps_folder_name = "heatmaps" 
size=328
x_mean=0
y_mean=0
tot_sum=0
for i in range(1,22):    
    img=Image.open("heatmaps/0001_"+str(i)+".png")
    mat=img.load()   
    for r in range(0,size):
        for c in range(0,size):
            tot_sum=tot_sum+mat[r,c]
            x_mean=x_mean+c*mat[r,c]
            y_mean=y_mean+r*mat[r,c]
    if tot_sum!=0:        
       print(x_mean/tot_sum)
       print(y_mean/tot_sum) 
    tot_sum=0
    x_mean=0
    y_mean=0           
            
