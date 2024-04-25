import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import numpy as np
import pickle
import pandas as pd
from ultralytics import YOLO
import torch

class ParkingApp:
    def __init__(self, master, class_list):
        self.master = master
        self.master.title("Parking Slot Detector")
        
        self.master.configure(bg='black')  # Set background color to black
        self.class_list = class_list
        
        # Create a frame for the video with desired width and height
        self.video_frame = tk.Frame(master, width=800, height=512, padx=15, pady=20, bg='black')  # Set background color to black
        self.video_frame.pack(side=tk.LEFT)

        self.text_frame = tk.Frame(master, width=400, height=512, padx=30, pady=20, bg='black')  # Set background color to black
        self.text_frame.pack(side=tk.RIGHT)

        self.video_label = tk.Label(self.video_frame, bg='black')  # Set background color to black
        self.video_label.pack()

        self.car_counter_label = ttk.Label(self.text_frame, text="Car Counter:", foreground="white", background="black", font=('Helvetica', 12))
        self.car_counter_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.car_counter_value = tk.StringVar()
        self.car_counter_text = ttk.Label(self.text_frame, textvariable=self.car_counter_value, foreground="white", background="black", font=('Helvetica', 12))
        self.car_counter_text.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Create a frame for the parking boxes
        self.parking_frame = tk.Frame(self.text_frame, width=380, height=400, padx=20, pady=20, bg='black')  # Set background color to black
        self.parking_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Create parking boxes
        self.parking_boxes = []
        self.create_parking_boxes()

        self.cap = cv2.VideoCapture('parking1.mp4')
        self.model = YOLO('yolov8s.pt')
        
        self.drawing = False
        self.area_names = []
        self.polylines = []
        self.points = []
        self.current_name = ""
        self.current_index = 1  # Initialize index for sequential numbering

        self.load_saved_data()

        self.update_video()

        self.master.bind('<Escape>', self.exit_app)
        self.master.bind('s', self.save_data)

    def update_video(self):
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return
        # Resize the frame to a smaller size
        frame = cv2.resize(frame, (800, 512))
        black_bg = np.zeros_like(frame)
        frame_copy = black_bg.copy()
        frame_copy = frame.copy()
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB) 
        frame_copy = np.transpose(frame_copy, (2, 0, 1)) 
        frame_tensor = torch.from_numpy(frame_copy).unsqueeze(0).float() 
        results = self.model.predict(frame_tensor)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")

        list1 = []

        for index, row in px.iterrows():
            x1, y1, x2, y2, _, d = map(int, row)
            c = self.class_list[d]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            if 'car' in c:
                list1.append([cx, cy])

        counter1 = []

        for i, polyline in enumerate(self.polylines):
            cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
            for i1 in list1:
                cx1, cy1 = i1
                res = cv2.pointPolygonTest(polyline, ((cx1, cy1)), False)
                if res >= 0:
                    cv2.circle(frame, (cx1, cy1), 5, (255, 0, 0), -1)
                    cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
                    counter1.append(cx1)

        car_count = len(counter1)
        free_space = len(self.polylines) - car_count

        # Convert the frame to Tkinter compatible image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)

        # Update the video label with the new frame
        self.video_label.img = img
        self.video_label.config(image=img)
        
        # Update car counter label
        self.car_counter_value.set(car_count)

        # Update parking box colors
        self.update_parking_boxes(len(counter1))

        self.video_label.after(1, self.update_video)

    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points = [(x, y)]
        elif event == cv2.EVENT_MOUSEMOVE:
            self.points.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.area_names.append(f'{self.current_index}')  # Generate sequential area name
            self.current_index += 1  # Increment index for the next area
            self.polylines.append(np.array(self.points, np.int32))

    def load_saved_data(self):
        try:
            with open("Parking_save", "rb") as f:
                data = pickle.load(f)
                self.polylines, self.area_names = data['polylines'], data['area_names']
                # Set current_index to the next number after the last saved area name
                if self.area_names:
                    self.current_index = int(self.area_names[-1]) + 1
        except:
            pass

    def save_data(self, event=None):
        with open("Parking_save", "wb") as f:
            data = {'polylines': self.polylines, 'area_names': self.area_names}
            pickle.dump(data, f)

    def exit_app(self, event=None):
        self.cap.release()
        cv2.destroyAllWindows()
        self.master.quit()

    def create_parking_boxes(self):
        for i in range(20):  # Assuming there are 20 parking spots
            box = tk.Label(self.parking_frame, text=str(i+1), bg='green', foreground="white", font=('Helvetica', 12), width=5, height=2)
            box.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="nsew")
            self.parking_boxes.append(box)

    def update_parking_boxes(self, car_count):
        for i, box in enumerate(self.parking_boxes):
            if i < car_count:
                box.config(bg='red')
            else:
                box.config(bg='green')

def main():
    # Load class_list
    my_file = open("coco.txt", "r")
    data = my_file.read()
    class_list = data.split("\n")
    
    root = tk.Tk()
    app = ParkingApp(root, class_list)
    root.mainloop()

if __name__ == "__main__":
    main()
