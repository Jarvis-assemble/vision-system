''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2,,                       
	==> LBPH computed model (trained faces) should be on trainer/ dir

'''

import cv2
from Models.audio import say

import os
from os import listdir

say("Facial Recognition is running now")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Models/trainer.yml')
cascadePath = "Models/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#indicate id counter
id = 0

# get the path/directory
folder_dir = "D:\Final yr project demo\Face_Dataset"
NameList=['None']
imagePaths = [os.path.join(folder_dir,f) for f in os.listdir(folder_dir)]   
#print(imagePaths)
for imagePath in imagePaths:
    name = os.path.split(imagePath)[-1].split(".")[3]
    if name not in NameList:
        NameList.append(name)
#print(NameList)

# names related to ids: example ==> name: id=1,  etc
names = ['None', 'id1', 'id2'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

img_text = ''
found = set()

while True:

    ret, img =cam.read()
    img = cv2.flip(img, 1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        conf=round(100 - confidence)

        if (conf > 40):
            img_text = NameList[id]
            confidence = "  {0}%".format(conf)
            
            if str(img_text) not in found :
                say(str(img_text))
                found.add(str(img_text))
        else:
           
            img_text = 'unknown'
            found.clear()
            confidence = "  {0}%".format(conf)
            #say(str(img_text))
        
        cv2.putText(img, str(img_text), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(1) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

#cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
