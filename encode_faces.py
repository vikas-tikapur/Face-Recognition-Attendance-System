import face_recognition
import cv2
import os
import numpy as np
import pickle

path = 'face_data'
images = []
classNames = []

for filename in os.listdir(path):
    img = cv2.imread(f"face_data/vikas.jpg")
    images.append(img)
    classNames.append(os.path.splitext(filename)[0])

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
with open('encodings.p', 'wb') as f:
    pickle.dump((encodeListKnown, classNames), f)

print("Encoding Complete")