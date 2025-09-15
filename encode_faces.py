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


import face_recognition    # Library for face detection & encoding
import cv2                 # OpenCV library for image processing
import os                  # For file and folder operations
import pickle              # For saving/loading Python objects in binary format

# Lists to store known face encodings and corresponding names
known_encodings = []
known_names = []

# Folder containing all registered face images
image_dir = "face_data"        # Each image file should be named as person's name (e.g., vikas.jpg)


# Loop through all image files inside the face_data folder
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):    # Process only image files
        path = os.path.join(image_dir, filename)
        print(f"[INFO] Processing: {filename}")
        
        # Read the image and convert it from BGR (OpenCV format) to RGB (face_recognition format)
        image = cv2.imread(path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect face locations in the image (HOG model is faster but less accurate than CNN)
        boxes = face_recognition.face_locations(rgb, model="hog")

        # Encode the faces found in the image
        encodings = face_recognition.face_encodings(rgb, boxes)

        name = os.path.splitext(filename)[0]  # getting name from filename, e.g., Ranjan.jpg -> Ranjan

        # Store each encoding and corresponding name
        for encoding in encodings:
            known_encodings.append(encoding)
            known_names.append(name)
            print(f"[INFO] Detected {len(encodings)} face(s) in {filename}")

# Save encodings and names into a dictionary
data = {"encodings": known_encodings, "names": known_names}

# Serialize (save) the encodings to a file 'encodings.p'
with open("encodings.p", "wb") as f:
    pickle.dump(data, f)

print("[INFO] Encodings saved to encodings.p")
