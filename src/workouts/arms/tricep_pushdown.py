import os
import sys
import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from src.workouts.utils import display_text, calculate_angle, make_detections, rep_counter


class TricepPushdownApp(ttk.Frame):

    def __init__(self, parent, rep_vars):
        super().__init__(parent)

        self.side = 'both'
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

    def display_skeleton(self, img, results):
        try:
            landmarks = results.pose_landmarks.landmark

            r_shoulder = [landmarks[11].x, landmarks[11].y]
            l_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[13].x, landmarks[13].y]
            l_elbow = [landmarks[14].x, landmarks[14].y]
            r_wrist = [landmarks[15].x, landmarks[15].y]
            l_wrist = [landmarks[16].x, landmarks[16].y]

            # Create a list of landmarks for the elbow angle calculation
            landmark_list = NormalizedLandmarkList()
            landmark_list.landmark.add(x=r_shoulder[0], y=r_shoulder[1], z=0.0)
            landmark_list.landmark.add(x=r_elbow[0], y=r_elbow[1], z=0.0)
            landmark_list.landmark.add(x=r_wrist[0], y=r_wrist[1], z=0.0)
            landmark_list.landmark.add(x=l_shoulder[0], y=l_shoulder[1], z=0.0)
            landmark_list.landmark.add(x=l_elbow[0], y=l_elbow[1], z=0.0)
            landmark_list.landmark.add(x=l_wrist[0], y=l_wrist[1], z=0.0)

            # Calculate the angles between the landmarks
            r_a_elbow = calculate_angle(r_shoulder, r_elbow, r_wrist)
            l_a_elbow = calculate_angle(l_shoulder, l_elbow, l_wrist)

            # Display the angles (in degrees) on the screen
            display_text(img, str(r_a_elbow), tuple(np.multiply(r_elbow, [640, 480]).astype(int)))
            display_text(img, str(l_a_elbow), tuple(np.multiply(l_elbow, [640, 480]).astype(int)))

            min_angle = 40
            max_angle = 165
            # count reps
            rep_counter(self, r_a_elbow, 'right', min_angle, max_angle, tension_stage="down")
            rep_counter(self, l_a_elbow, 'left', min_angle, max_angle, tension_stage="down")

            # Render detections
            self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2), (3, 4), (4, 5)])
        except AttributeError:
            # no landmarks detected
            # print("No landmarks detected")
            pass

    def save_workout(self):
        print("Workout saved")
        pass

    def run(self):
        ret, frame = self.cap.read()

        if ret:
            results, img = make_detections(self, frame)
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


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Bicep Curls")
    app = TricepPushdownApp(root)
    app.pack()
    root.mainloop()
