import os
import sys
import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

from tkinter import ttk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
import src.workouts.utils as utils


class LegExtensionApp(ttk.Frame):

    def __init__(self, parent, rep_vars, stage_vars):
        super().__init__(parent)

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

        utils.run(self)

    def display_skeleton(self, img, results):
        min_angle = 90
        max_angle = 165
        try:
            landmarks = results.pose_landmarks.landmark
            if self.side != "both":
                if self.side == "right":
                    hip = [landmarks[23].x, landmarks[23].y]
                    knee = [landmarks[25].x, landmarks[25].y]
                    ankle = [landmarks[27].x, landmarks[27].y]
                elif self.side == 'left':
                    hip = [landmarks[24].x, landmarks[24].y]
                    knee = [landmarks[26].x, landmarks[26].y]
                    ankle = [landmarks[28].x, landmarks[28].y]
                else:
                    raise ValueError("Side must be 'left' or 'right'")

                # Create a list of landmarks for the knee angle calculation
                landmark_list = NormalizedLandmarkList()
                landmark_list.landmark.add(x=hip[0], y=hip[1], z=0.0)
                landmark_list.landmark.add(x=knee[0], y=knee[1], z=0.0)
                landmark_list.landmark.add(x=ankle[0], y=ankle[1], z=0.0)

                # Calculate the angles between the landmarks
                a_knee = utils.calculate_angle(hip, knee, ankle)

                # Display the angles (in degrees) on the screen
                utils.display_text(img, str(a_knee), tuple(np.multiply(knee, [640, 480]).astype(int)))

                # count reps
                utils.rep_counter(self, a_knee, self.side, min_angle, max_angle, tension_angle='high')

                # Render detections
                self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2)])
            else:
                r_hip = [landmarks[23].x, landmarks[23].y]
                l_hip = [landmarks[24].x, landmarks[24].y]
                r_knee = [landmarks[25].x, landmarks[25].y]
                l_knee = [landmarks[26].x, landmarks[26].y]
                r_ankle = [landmarks[27].x, landmarks[27].y]
                l_ankle = [landmarks[28].x, landmarks[28].y]

                # Create a list of landmarks for the knee angle calculation
                landmark_list = NormalizedLandmarkList()
                landmark_list.landmark.add(x=r_hip[0], y=r_hip[1], z=0.0)
                landmark_list.landmark.add(x=r_knee[0], y=r_knee[1], z=0.0)
                landmark_list.landmark.add(x=r_ankle[0], y=r_ankle[1], z=0.0)
                landmark_list.landmark.add(x=l_hip[0], y=l_hip[1], z=0.0)
                landmark_list.landmark.add(x=l_knee[0], y=l_knee[1], z=0.0)
                landmark_list.landmark.add(x=l_ankle[0], y=l_ankle[1], z=0.0)

                # Calculate the angles between the landmarks
                r_a_knee = utils.calculate_angle(r_hip, r_knee, r_ankle)
                l_a_knee = utils.calculate_angle(l_hip, l_knee, l_ankle)

                # Display the angles (in degrees) on the screen
                utils.display_text(img, str(r_a_knee), tuple(np.multiply(r_knee, [640, 480]).astype(int)))
                utils.display_text(img, str(l_a_knee), tuple(np.multiply(l_knee, [640, 480]).astype(int)))

                # count reps
                utils.rep_counter(self, r_a_knee, 'right', min_angle, max_angle, tension_angle='high')
                utils.rep_counter(self, l_a_knee, 'left', min_angle, max_angle, tension_angle='high')

                # Render detections
                self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2), (3, 4), (4, 5)])
        except AttributeError:
            # no landmarks detected
            pass

    def left_side(self):
        self.side = "left"
        self.rep_stage_l.set("down")

    def right_side(self):
        self.side = "right"
        self.rep_stage_r.set("down")

    def both_sides(self):
        self.side = "both"
        self.rep_stage_l.set("down")
        self.rep_stage_r.set("down")

    def toggle_active(self):
        self.active = not self.active

    def close(self):
        self.cap.release()
        self.destroy()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    root.title("Leg Extension")
    rep_count_l = tk.IntVar()
    rep_count_r = tk.IntVar()
    rep_stage_l = tk.StringVar(value="down")
    rep_stage_r = tk.StringVar(value="down")
    app = LegExtensionApp(root, [rep_count_l, rep_count_r], [rep_stage_l, rep_stage_r])
    app.pack()
    root.mainloop()
