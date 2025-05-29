import os
from datetime import datetime

def mark_attendance(name):
    filename = 'Attendance/attendance.csv'
    if not os.path.exists('Attendance'):
        os.makedirs('Attendance')

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Name,Time,Date\n')

    with open(filename, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            timeStr = now.strftime('%H:%M:%S')
            dateStr = now.strftime('%Y-%m-%d')
            f.writelines(f'{name},{timeStr},{dateStr}\n')