from PIL import Image
import pytesseract
import argparse
import cv2
import time
from Models.audio import say

import os
tessdata_dir_config = '--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

cam = cv2.VideoCapture(0)

ct=0
while(1):
        _,img=cam.read()
        cv2.imshow('live',img)
        ct+=1

        if(cv2.waitKey(1) & 0xFF ==27):
                cv2.imwrite('Samples/live.png',img)
                break
        elif(ct>=500):
                cv2.imwrite('Samples/live.png',img)
                break
        

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False,default="Samples/live.png",
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="blur",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Preprocessing
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# checking to see if median blurring should be done to remove noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

mytext = pytesseract.image_to_string(Image.open(filename),config=tessdata_dir_config)
os.remove(filename)
print(mytext)
say(mytext)

cv2.destroyAllWindows()

