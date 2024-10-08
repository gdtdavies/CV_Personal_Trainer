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

    def __init__(self, parent, rep_vars, stage_vars):
        super().__init__(parent, relief=tk.RIDGE, border=10)

        self.active = False

        self.side = 'both'
        self.rep_count_l = rep_vars[0]
        self.rep_count_r = rep_vars[1]
        self.rep_stage_l = stage_vars[0]
        self.rep_stage_r = stage_vars[1]

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.5)

        self.cap = cv2.VideoCapture(0)
        self.image_label = ttk.Label(self)
        self.image_label.pack()

        self.run()

    def display_skeleton(self, img, results):
        min_angle = 40
        max_angle = 165
        try:
            landmarks = results.pose_landmarks.landmark
            if self.side != "both":
                if self.side == "right":
                    shoulder = [landmarks[11].x, landmarks[11].y]
                    elbow = [landmarks[13].x, landmarks[13].y]
                    hip = [landmarks[23].x, landmarks[23].y]
                elif self.side == 'left':
                    shoulder = [landmarks[12].x, landmarks[12].y]
                    elbow = [landmarks[14].x, landmarks[14].y]
                    hip = [landmarks[24].x, landmarks[24].y]
                else:
                    raise ValueError("Side must be 'left' or 'right'")

                # Create a list of landmarks for the elbow angle calculation
                landmark_list = NormalizedLandmarkList()
                landmark_list.landmark.add(x=elbow[0], y=elbow[1], z=0.0)
                landmark_list.landmark.add(x=shoulder[0], y=shoulder[1], z=0.0)
                landmark_list.landmark.add(x=hip[0], y=hip[1], z=0.0)

                # Calculate the angles between the landmarks
                a_shoulder = calculate_angle(elbow, shoulder, hip)

                # Display the angles (in degrees) on the screen
                display_text(img, str(a_shoulder), tuple(np.multiply(elbow, [640, 480]).astype(int)))

                # count reps
                rep_counter(self, a_shoulder, self.side, min_angle, max_angle, tension_angle='high')

                # Render detections
                self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2)])
            else:
                r_shoulder = [landmarks[11].x, landmarks[11].y]
                l_shoulder = [landmarks[12].x, landmarks[12].y]
                r_elbow = [landmarks[13].x, landmarks[13].y]
                l_elbow = [landmarks[14].x, landmarks[14].y]
                r_hip = [landmarks[23].x, landmarks[23].y]
                l_hip = [landmarks[24].x, landmarks[24].y]

                # Create a list of landmarks for the elbow angle calculation
                landmark_list = NormalizedLandmarkList()
                landmark_list.landmark.add(x=r_elbow[0], y=r_elbow[1], z=0.0)
                landmark_list.landmark.add(x=r_shoulder[0], y=r_shoulder[1], z=0.0)
                landmark_list.landmark.add(x=r_hip[0], y=r_hip[1], z=0.0)
                landmark_list.landmark.add(x=l_elbow[0], y=l_elbow[1], z=0.0)
                landmark_list.landmark.add(x=l_shoulder[0], y=l_shoulder[1], z=0.0)
                landmark_list.landmark.add(x=l_hip[0], y=l_hip[1], z=0.0)

                # Calculate the angles between the landmarks
                r_a_shoulder = calculate_angle(r_elbow, r_shoulder, r_hip)
                l_a_shoulder = calculate_angle(l_elbow, l_shoulder, l_hip)

                # Display the angles (in degrees) on the screen
                display_text(img, str(r_a_shoulder), tuple(np.multiply(r_elbow, [640, 480]).astype(int)))
                display_text(img, str(l_a_shoulder), tuple(np.multiply(l_elbow, [640, 480]).astype(int)))

                # count reps
                rep_counter(self, r_a_shoulder, 'right', min_angle, max_angle, tension_angle='high')
                rep_counter(self, l_a_shoulder, 'left', min_angle, max_angle, tension_angle='high')

                # Render detections
                self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2), (3, 4), (4, 5)])
        except AttributeError:
            # no landmarks detected
            pass

    def left_side(self):
        self.side = "left"
        self.rep_stage_l.set('down')

    def right_side(self):
        self.side = "right"
        self.rep_stage_r.set('down')

    def both_sides(self):
        self.side = "both"
        self.rep_stage_l.set('down')
        self.rep_stage_r.set('down')

    def toggle_active(self):
        self.active = not self.active

    def run(self):
        # while self.cap.isOpened():
        ret, frame = self.cap.read()

        if ret:
            results, img = make_detections(self, frame)
            if self.active:
                self.display_skeleton(img, results)

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
