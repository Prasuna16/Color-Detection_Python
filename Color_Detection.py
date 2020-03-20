'''
1) Run this code using Command Prompt
2) Syntax to run: python <path_to_this_file> -i <path_to_the_image>
3) Make sure you give correct path to colors.csv file in pd.read_csv(<pathToColorsFile>)

#Resources - Obtained colors.csv file from internet
'''

#OpenCV - Library employed for image processing techniques

import cv2
import pandas as pd
import argparse

#Creating argument parser to take image path from command line
ag = argparse.ArgumentParser()
ag.add_argument('-i', '--image', required = True, help = 'Path to the image')
arguments = vars(ag.parse_args())
image_path = arguments['image']

#Reading image with OpenCV
img_actual = cv2.imread(image_path)

#to resize the image
width = 700
height = 680
dim = (width, height)
img = cv2.resize(img_actual, dim, interpolation = cv2.INTER_AREA)

clicked = False
r = g = b = xpos = ypos = 0

#Giving names to each column in the csv file.
#The uploaded colors.csv file contains names for each corresponding RGB values
index = ['color', 'color_name', 'hex_value', 'R', 'G', 'B']
file = pd.read_csv('colors.csv', names=index)

#function to get the color name for given R, G, B values
#Here we calculate the minimum distance from all colors and get the most matching color
def getColorName(R, G, B):
    min_dis = 100000
    for i in range(len(file)):
        dis = abs(R-int(file.loc[i, 'R']))+abs(G-int(file.loc[i, 'G']))+abs(B-int(file.loc[i, 'B']))
        if (min_dis > dis):
            min_dis = dis
            clr_name = file.loc[i, 'color_name']
    return clr_name

#function to get x,y coordinates of mouse double click
def getCoordinates(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow ('Image')
cv2.setMouseCallback('Image', getCoordinates)

while (1):

    cv2.imshow('Image', img)
    if (clicked):

        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle (img, (10,25), (560,60), (b,g,r), -1)

        #Creating text string to display( Color name and RGB values )
        text = getColorName(r, g, b) + " R=" + str(r) + " G=" + str(g) + " B=" + str(b)

        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText (img, text, (30, 50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)

        #For very light colours we will display text in black colour
        if (r+g+b >= 600):
            cv2.putText (img, text, (50, 50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

        clicked = False

    #Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
