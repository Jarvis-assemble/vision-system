''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2,,,                      
'''

import cv2
import os
import time
from Models.audio import say
import stotext
import os


say("Dataset Capture")
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

face_detector = cv2.CascadeClassifier('Models/haarcascade_frontalface_default.xml')

# For each person, enter one numeric face id
face_id = int(input('\n Enter user id and press <enter> ==>  '))
face_name = stotext.speechtotext()
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0

folder_dir = "D:\Final yr project demo\Face_Dataset"
imagePaths = [os.path.join(folder_dir,f) for f in os.listdir(folder_dir)]   

if imagePaths!=[]:
  for imagePath in imagePaths:
     id = int(os.path.split(imagePath)[-1].split(".")[1])
     if id==face_id:
        os.remove(imagePath)

while(True):

    ret, img = cam.read()
    img = cv2.flip(img, 1) # flip video image vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.2, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1

        # Save the captured image into the datasets folder
        cv2.imwrite("Face_Dataset/user." + str(face_id) + '.' + str(count) + '.'+str(face_name)+".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('image', img)
    
    k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 20: # Take 20 face sample and stop video
        print("\n [INFO] Image Captured.....Thank you for your Patience")
        time.sleep(0.2)
        cam.release()
        cv2.destroyAllWindows()
        print("\n [INFO] Please wait for while until training complete's")
        os.system('python 02_face_training.py')
        
        break

#cleanup
print("\n [INFO] Capturing and Training.....Thank you for your Patience")
time.sleep(1)

