import json
import numpy as np
import math
from PIL import Image

with open("test_data/0001.json") as file:
    image_1_data = json.load(file)
    coordinates_1 = image_1_data["hand_pts"][0]
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
    greyscale.show()
    greyscale = greyscale.save("0001-heatmap.png")