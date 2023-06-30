import numpy as np
import cv2 as cv

"""
Takes in a Map where Roads are White and Everything else is Black / not white.
@Returns JPG's of B/W Map and Node B/W Map
@Returns .cvs of Nodes For map 
"""

DENOICE = 2
DENOICE_SENSITIVITY = 0
GRID_AVG_PERCENT = .3
NODE_GRID = 3

# get Maps From File system  files ending **.jpg)

imageName = 'GrimsbyMap.jpg'

img = cv.imread(imageName)


# Map Img Exists
assert img is not None, "file could not be read, check with os.path.exists()"

# Make Img Black and White
(thresh, img_thresh) = cv.threshold(img, 185, 255, cv.THRESH_BINARY)
hsv = cv.cvtColor(img_thresh, cv.COLOR_BGR2HSV)
greyIMG = cv.cvtColor(img_thresh, cv.COLOR_BGR2GRAY)
secondIMG = cv.cvtColor(img_thresh, cv.COLOR_BGR2GRAY)

# Looping over pixels Removing 'Stray' Pixels

height, width = greyIMG.shape

for x in range(DENOICE):
    for i in range(height):
        for j in range(width):
            secondIMG[i, j] = 0
            count = 0
            pixel = greyIMG[i, j]
            if pixel == 255:
                if i != height - 1 and i != 0:
                    if greyIMG[i + 1, j] != 0:
                        count += 1
                    if greyIMG[i - 1, j] != 0:
                        count += 1
                    
                if j != width - 1 and j != 0:
                    if greyIMG[i, j+1] != 0:
                        count += 1
                    if greyIMG[i, j-1] != 0:
                        count +=1
                
                if count <= DENOICE_SENSITIVITY:
                    greyIMG[i, j] = 0;
                    #print(f'Removed pixel ({i}, {j})')

NodeArray = []

for i in range(int(height/NODE_GRID)):
    for j in range(int(width/NODE_GRID)):
        
        x = NODE_GRID * i
        y = NODE_GRID * j
        
        
        
        # cv.line(greyIMG, (x, 0), (x, height), (30,30,30), 1)
        # cv.line(greyIMG, (0, y), (width, y), (30,30,30), 1)
        
        #Check 5 pixels in area
        pixelArray = [greyIMG[x, y],
                      greyIMG[x - int(NODE_GRID/2), y],
                      greyIMG[x, y- int(NODE_GRID/2)],
                      greyIMG[x- int(NODE_GRID/2), y- int(NODE_GRID/2)]]
        
                
        # secondIMG[x, y] = 20
        # secondIMG[x - int(NODE_GRID/2), y] = 20
        # secondIMG[x, y- int(NODE_GRID/2)] = 20
        # secondIMG[x- int(NODE_GRID/2), y- int(NODE_GRID/2)] = 20
        
        if(sum(pixelArray)/4 > (255*(GRID_AVG_PERCENT))):
            secondIMG[x,y] = 255
            NodeArray.append([x,y])

        # greyIMG[x, y] = 50
        # greyIMG[x - int(NODE_GRID/2), y] = 50
        # greyIMG[x, y- int(NODE_GRID/2)] = 50
        # greyIMG[x- int(NODE_GRID/2), y- int(NODE_GRID/2)] = 50

        
        #print(f"{pixelArray} : Is AVG: {'True' if (sum(pixelArray)/4) > (255*(GRID_AVG_PERCENT)) else 'False'}")

#print(NodeArray)

f = open(f"NodeArray-{imageName}.csv", "a")
f.write(','.join(str(x) for x in NodeArray))
f.close()

# show image
#cv.imshow('Original Image',img)
#cv.imshow('hsv',hsv)
cv.imwrite(f"{imageName}-greyDenoised.jpg", greyIMG)
#cv.imshow('Tile', tile)
cv.imwrite(f"{imageName}-NodeMap.jpg", secondIMG)

cv.waitKey(0)
cv.destroyAllWindows()
