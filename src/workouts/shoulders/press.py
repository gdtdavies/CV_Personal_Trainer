import os
import sys
import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

from tkinter import ttk
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from src.workouts.utils import display_text, calculate_angle, make_detections, rep_counter
import tkinter as tk


class ShoulderPressApp(ttk.Frame):

    def __init__(self, parent, rep_vars):
        super().__init__(parent, relief=tk.RIDGE, border=10)

        self.active = False

        self.side = 'left'
        self.rep_count_l = rep_vars[0]
        self.rep_count_r = rep_vars[1]
        self.rep_stage_r = 'down'
        self.rep_stage_l = 'down'

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.5)

        self.cap = cv2.VideoCapture(0)
        self.image_label = ttk.Label(self)
        self.image_label.pack()

        self.run()

    def left_side(self):
        self.side = "left"
        self.rep_stage_l = "down"

    def right_side(self):
        self.side = "right"
        self.rep_stage_r = "down"

    def both_sides(self):
        self.side = "both"
        self.rep_stage_l = "down"
        self.rep_stage_r = "down"

    def run(self):
        # while self.cap.isOpened():
        ret, frame = self.cap.read()

        if ret:
            results, img = make_detections(self, frame)
            # self.display_skeleton(img, results)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.image_label.imgtk = img_tk
            self.image_label.configure(image=img_tk)
        self.after(10, self.run)

    def close(self):
        self.cap.release()
        self.destroy()
        cv2.destroyAllWindows()
