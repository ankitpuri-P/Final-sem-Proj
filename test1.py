import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
import cvzone

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

model = YOLO('yolov8s.pt')

cap = cv2.VideoCapture('parking1.mp4')
video_width, video_height = 800, 512  # Video frame resolution

drawing = False
area_names = []

try:
    with open("Parking_save", "rb") as f:
        data = pickle.load(f)
        polylines, area_names = data['polylines'], data['area_names']
except:
    polylines = []

points = []
current_name = ""
current_index = 1  # Initialize index for sequential numbering

def draw(event, x, y, flags, param):
    global points, drawing, current_index
    # Scale coordinates to match the video frame resolution
    x = int(x * (1020 / video_width))
    y = int(y * (500 / video_height))

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        area_names.append(f'{current_index}')  # Generate sequential area name
        current_index += 1  # Increment index for the next area
        # Scale points to match the video frame resolution
        scaled_points = [(int(pt[0] * (video_width / 1020)), int(pt[1] * (video_height / 500))) for pt in points]
        polylines.append(np.array(scaled_points, np.int32))

count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    frame = cv2.resize(frame, (video_width, video_height))  # Resize to match video frame resolution

    count += 1
    if count % 3 != 0:
        continue

    frame_copy = frame.copy()
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    list1 = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])

        c = class_list[d]
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        if 'car' in c:
            list1.append([cx, cy])

    counter1 = []
    list2 = []

    for i, polyline in enumerate(polylines):
        list2.append(i)
        cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
        cvzone.putTextRect(frame, f'{area_names[i]}', tuple(polyline[0]), 1, 1)
        for i1 in list1:
            cx1 = i1[0]
            cy1 = i1[1]
            res = cv2.pointPolygonTest(polyline, ((cx1, cy1)), False)
            if res >= 0:
                cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)
                cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
                counter1.append(cx1)

    car_count = len(counter1)
    free_space = len(list2) - car_count
    cvzone.putTextRect(frame, f'CAR_COUNTER :{car_count}', (50, 60), 2, 2)
    cvzone.putTextRect(frame, f'FREE_SPACE :{free_space}', (50, 100), 2, 2)

    cv2.imshow('FRAME', frame)
    cv2.setMouseCallback('FRAME', draw)
    Key = cv2.waitKey(500) & 0xFF
    if Key == 27:  # Check if the 'esc' key is pressed
        break
    if Key == ord('s'):
        with open("Parking_save", "wb") as f:
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)

cap.release()
cv2.destroyAllWindows()
