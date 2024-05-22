import mediapipe as mp
import cv2
import numpy as np


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return round(angle, 2)

def calulate_distance_ratio(a, b, c, d):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  
    d = np.array(d)  
    
    dist1 = np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    dist2 = np.sqrt((c[0] - d[0])**2 + (c[1] - d[1])**2)
    
    return round(dist1/dist2, 3)
    

def display_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 100, 50), 6, cv2.LINE_AA)

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
            
            try:
                landmarks = results.pose_landmarks.landmark
                
                r_shoulder = [landmarks[11].x, landmarks[11].y]
                l_shoulder = [landmarks[12].x, landmarks[12].y]
                r_elbow = [landmarks[13].x, landmarks[13].y]
                l_elbow = [landmarks[14].x, landmarks[14].y]
                r_wrist = [landmarks[15].x, landmarks[15].y]
                l_wrist = [landmarks[16].x, landmarks[16].y]
                
                r_hip = [landmarks[23].x, landmarks[23].y]
                l_hip = [landmarks[24].x, landmarks[24].y]
                r_knee = [landmarks[25].x, landmarks[25].y]
                l_knee = [landmarks[26].x, landmarks[26].y]
                r_ankle = [landmarks[27].x, landmarks[27].y]
                l_ankle = [landmarks[28].x, landmarks[28].y]
                
                # for bicep curls and pushups
                a_l_elbow = calculate_angle(l_shoulder, l_elbow, l_wrist)
                a_r_elbow = calculate_angle(r_shoulder, r_elbow, r_wrist)
                
                # for squats
                a_l_knee = calculate_angle(l_hip, l_knee, l_ankle)
                a_r_knee = calculate_angle(r_hip, r_knee, r_ankle)
                
                # shoulder press and form check
                a_l_shoulder = calculate_angle(l_elbow, l_shoulder, l_hip)
                a_r_shoulder = calculate_angle(r_elbow, r_shoulder, r_hip)
                
                stance_ratio = calulate_distance_ratio(l_hip, r_hip, l_knee, r_knee)
                
                display_text(img, str(a_l_elbow), tuple(np.multiply(l_elbow, [640, 480]).astype(int)))
                display_text(img, str(a_r_elbow), tuple(np.multiply(r_elbow, [640, 480]).astype(int)))
                display_text(img, str(a_l_shoulder), tuple(np.multiply(l_shoulder, [640, 480]).astype(int)))
                display_text(img, str(a_r_shoulder), tuple(np.multiply(r_shoulder, [640, 480]).astype(int)))
                display_text(img, str(a_l_knee), tuple(np.multiply(l_knee, [640, 480]).astype(int)))
                display_text(img, str(a_r_knee), tuple(np.multiply(r_knee, [640, 480]).astype(int)))
                
                display_text(img, str(stance_ratio), tuple(np.multiply(l_hip, [640, 480]).astype(int)))
                
                mp_drawing.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            except:
                pass
            
            # Increase window size
            cv2.namedWindow('MediaPipe Pose', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('MediaPipe Pose', 1280, 960)
            cv2.imshow('MediaPipe Pose', img)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
