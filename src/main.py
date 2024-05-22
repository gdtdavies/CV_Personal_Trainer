import mediapipe as mp
import cv2

def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    
    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                print("Ignoring empty camera frame.")
                continue
            
            # Detections
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Mediapipe needs RGB
            img = cv2.flip(img, 1)  # Flip on horizontal
            img.flags.writeable = False  # Image is no longer writeable
            results = pose.process(img)  # make detections
            img.flags.writeable = True  # Image is now writeable
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Convert back to BGR for rendering
            
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            cv2.imshow('MediaPipe Pose', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
