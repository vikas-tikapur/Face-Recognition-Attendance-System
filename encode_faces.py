'''import face_recognition
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

print("Encoding Complete")'''


import face_recognition
import cv2
import os
import pickle

known_encodings = []
known_names = []

# ✅ सही folder का नाम
image_dir = "face_data"

for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(image_dir, filename)
        print(f"[INFO] Processing: {filename}")
        
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        boxes = face_recognition.face_locations(rgb, model="hog")
        encodings = face_recognition.face_encodings(rgb, boxes)

        name = os.path.splitext(filename)[0]  # filename से नाम लेना, e.g., Ranjan.jpg -> Ranjan

        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)
            print(f"[INFO] Detected {len(encodings)} face(s) in {filename}")

# Save encodings
data = {"encodings": known_encodings, "names": known_names}

with open("encodings.p", "wb") as f:
    pickle.dump(data, f)

print("[INFO] Encodings saved to encodings.p")
