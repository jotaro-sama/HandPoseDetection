import json
import numpy as np
import math
import PIL
from PIL import Image
import argparse
import os
import matplotlib.pyplot as plt

def onclick(event):
    if event.xdata != None and event.ydata != None:
       global click_x
       global click_y	
       click_x=event.xdata
       click_y=event.ydata
       global pause
       pause = not pause
parser = argparse.ArgumentParser(description="Resizes dataset and generates heatmaps")
parser.add_argument("dir", help="dataset folder containing two subfolders, one for images and one for jsons")
parser.add_argument("sizeX", help="new X size")
parser.add_argument("sizeY", help="new Y size")
parser.add_argument("variance", help="variance for gaussians")
parser.add_argument("resume", help="last image done e.g. i have done 54 images until now, so put 54 here")

args = parser.parse_args()

resized_images_folder_name = "resized"
if not os.path.exists(resized_images_folder_name):
    os.makedirs(resized_images_folder_name)

heatmaps_folder_name = "heatmaps" 
if not os.path.exists(heatmaps_folder_name):
    os.makedirs(heatmaps_folder_name)

NET_IMAGE_SIZE = (int(args.sizeX), int(args.sizeY))

hands_folder = args.dir+'/hands'
#jsons_folder = args.dir+'/jsons'
count = int(args.resume)

list_dir = sorted(os.listdir(hands_folder))

for file in list_dir:
    filename = os.fsdecode(file)
    count = count + 1 
    print(count)

    if filename.endswith(".jpg") and not(filename.startswith("done")):
        #print(filename)
        with Image.open(hands_folder+"/"+file) as img:
            old_size = img.size
            #print(old_size)
                
            if old_size != NET_IMAGE_SIZE:
                img = img.resize(size=NET_IMAGE_SIZE, resample=PIL.Image.BICUBIC)
                
            #img = img.save(resized_images_folder_name+'/'+ str(count)+'.jpg')
            img.save(resized_images_folder_name+'/'+ str(count)+'.jpg')
            os.rename(hands_folder+"/"+file, hands_folder+"/"+'done'+str(count)+'.jpg')
            
        im = plt.imread(resized_images_folder_name+'/'+ str(count)+'.jpg')
        ax = plt.gca()
        fig = plt.gcf()
        implot = ax.imshow(im)
        pause=False
        click_x=0
        click_y=0
        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        plt.ion()
        plt.show()
        it=0
        while it<5:
              if pause:
                  it=it+1
                  pause=not pause
                  print('x coordinate='+str(click_x))
                  print('y coordinate'+str(click_y))
                  image = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))
                  visited = np.zeros((NET_IMAGE_SIZE[0], NET_IMAGE_SIZE[1]))
                  var = float(args.variance)
                  for i, row in enumerate(image):
                      for j, pixel in enumerate(row):
                          image[i][j] = math.exp((- (((i-(click_y))**2/var) + ((j-(click_x))**2/var))))
                  
                  greyscale = Image.fromarray(image * 255).convert("L")
                  #print(heatmap_num)
                  heatmap_filename = "heatmaps/" + str(count) + "_" + str(it) + ".png"
                  #print(heatmap_filename)
                  greyscale = greyscale.save(heatmap_filename)
              plt.pause(0.001)
        plt.cla()
        plt.clf()

