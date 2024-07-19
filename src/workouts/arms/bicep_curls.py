import mediapipe as mp
import cv2
import numpy as np
from mediapipe.framework.formats.landmark_pb2 import NormalizedLandmarkList


class BicepCurler:

    def __init__(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.8, min_tracking_confidence=0.5)
        self.cap = cv2.VideoCapture(0)

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

            r_shoulder = [landmarks[11].x, landmarks[11].y]
            l_shoulder = [landmarks[12].x, landmarks[12].y]
            r_elbow = [landmarks[13].x, landmarks[13].y]
            l_elbow = [landmarks[14].x, landmarks[14].y]
            r_wrist = [landmarks[15].x, landmarks[15].y]
            l_wrist = [landmarks[16].x, landmarks[16].y]

            # Create a list of landmarks for the elbow angle calculation
            landmark_list = NormalizedLandmarkList()
            for landmark in landmarks[11:17]:
                landmark_list.landmark.add(x=landmark.x, y=landmark.y, z=landmark.z)

            # Calculate the angles between the landmarks
            a_l_elbow = self.calculate_angle(l_shoulder, l_elbow, l_wrist)
            a_r_elbow = self.calculate_angle(r_shoulder, r_elbow, r_wrist)

            # Display the angles (in degrees) on the screen
            self.display_text(img, str(a_l_elbow), tuple(np.multiply(l_elbow, [640, 480]).astype(int)))
            self.display_text(img, str(a_r_elbow), tuple(np.multiply(r_elbow, [640, 480]).astype(int)))

            # Render detections
            self.mp_drawing.draw_landmarks(img, landmark_list, [(0, 2), (2, 4), (1, 3), (3, 5)])
        except AttributeError:
            # print("No pose detected")
            pass

    def rep_counter(self, reps):
        pass

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if not ret:
                print("Ignoring empty camera frame.")
                continue

            results, img = self.make_detections(frame)

            self.display_skeleton(img, results)
            cv2.imshow('Mediapipe Feed', img)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    bicep_curler = BicepCurler()
    bicep_curler.run()
