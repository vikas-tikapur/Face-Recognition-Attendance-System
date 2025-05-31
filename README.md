## Description
This project uses Python and OpenCV to build a real-time face recognition-based attendance system. When a registered face is recognized through webcam, the attendance is marked and stored in a CSV file.

## Features
- Register new faces with images
- Encode known faces
- Real-time face recognition
- Attendance stored with timestamp in CSV format

## Folder Structure
```
FaceRecognitionAttendance/
├── main.py               # Main attendance system code
├── face_data/            # Registered face images (with names)
├── Attendance/           # Attendance CSV files
├── encode_faces.py       # Encode known faces
├── utils.py              # Helper functions
├── encodings.p           # Stored face encodings
└── README.md             # Documentation
```

## Installation
```bash
pip install opencv-python
pip install face_recognition
pip install numpy
```

## Usage
1. Add clear face images to `face_data/` folder (name the image with person's name)
2. Run `encode_faces.py` to generate encodings
4. Attendance will be saved in `Attendance/attendance.csv`

## Example
![screenshot](screenshot.png)  # Optional

## Run Program/Important Command:- 
1. If you want to run a simple script — python recognize_faces.py
2. If you want a user-friendly interface with GUI —  python main.py  
3. If save file and images changes - python encode_faces.py
4. Check Registered Names:-  python check_names.py

## some other command-
1. notepad recognize_faces.py
2. python .\show_names.py