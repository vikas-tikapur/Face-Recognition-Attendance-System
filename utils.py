import os
from datetime import datetime

def mark_attendance(name):
    filename = 'attendance.csv'
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time\n')

    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        name_list = [line.split(',')[0] for line in myDataList]
        if name not in name_list:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.write(f'{name},{dtString}\n')
            print(f'[INFO] Attendance marked for {name} at {dtString}')
