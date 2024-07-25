import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList

from tkinter import ttk
from PIL import Image, ImageTk


class BicepCurlsApp(ttk.Frame):

    def __init__(self, parent, rep_vars):
        super().__init__(parent)

        self.side = 'left'
        self.rep_count_l = rep_vars[0]
        self.rep_count_r = rep_vars[1]
        self.rep_stage = 'down'

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.8, min_tracking_confidence=0.5)

        self.cap = cv2.VideoCapture(0)
        self.image_label = ttk.Label(self)
        self.image_label.pack()

        self.run()

    @staticmethod
    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return round(angle, 2)

    def make_detections(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.flip(img, 1)
        img.flags.writeable = False
        results = self.pose.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        return results, img

    @staticmethod
    def display_text(img, text, position):
        cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                    1, (255, 100, 50), 6, cv2.LINE_AA)

    def display_skeleton(self, img, results):
        try:
            landmarks = results.pose_landmarks.landmark

            if self.side == "right":
                shoulder = [landmarks[11].x, landmarks[11].y]
                elbow = [landmarks[13].x, landmarks[13].y]
                wrist = [landmarks[15].x, landmarks[15].y]
            elif self.side == 'left':
                shoulder = [landmarks[12].x, landmarks[12].y]
                elbow = [landmarks[14].x, landmarks[14].y]
                wrist = [landmarks[16].x, landmarks[16].y]
            else:
                raise ValueError("Side must be 'left' or 'right'")

            # Create a list of landmarks for the elbow angle calculation
            landmark_list = NormalizedLandmarkList()
            landmark_list.landmark.add(x=shoulder[0], y=shoulder[1], z=0.0)
            landmark_list.landmark.add(x=elbow[0], y=elbow[1], z=0.0)
            landmark_list.landmark.add(x=wrist[0], y=wrist[1], z=0.0)

            # Calculate the angles between the landmarks
            a_elbow = self.calculate_angle(shoulder, elbow, wrist)

            # Display the angles (in degrees) on the screen
            self.display_text(img, str(a_elbow), tuple(np.multiply(elbow, [640, 480]).astype(int)))

            # count reps
            self.rep_counter(a_elbow)

            # Render detections
            self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 1), (1, 2)])
        except AttributeError:
            # no landmarks detected
            pass

    def rep_counter(self, angle):
        if self.side != "left" and self.side != "right":
            raise ValueError("Side must be 'left' or 'right'")

        # Get the current count
        count = self.rep_count_l.get() if self.side == "left" else self.rep_count_r.get()

        if angle > 160 and self.rep_stage == "up":
            self.rep_stage = "down"
            print(f'down {count}')
        elif angle < 30 and self.rep_stage == "down":
            self.rep_stage = "up"
            count += 1  # Increment the count
            print(f'up {count}')

        # Update the IntVar with the new count
        if self.side == "left":
            self.rep_count_l.set(count)
        else:
            self.rep_count_r.set(count)

    def left_side(self):
        self.side = "left"
        self.rep_stage = "down"

    def right_side(self):
        self.side = "right"
        self.rep_stage = "down"

    def run(self):
        # while self.cap.isOpened():
        ret, frame = self.cap.read()

        if ret:
            results, img = self.make_detections(frame)
            self.display_skeleton(img, results)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            self.image_label.imgtk = img_tk
            self.image_label.configure(image=img_tk)
        self.after(10, self.run)
