import cv2
import numpy as np


def display_text(img, text, position):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 100, 50), 3, cv2.LINE_AA)


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return round(angle, 2)


def make_detections(app, frame):
    img = cv2.resize(frame, (540, 405))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img, 1)
    img.flags.writeable = False
    results = app.pose.process(img)
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return results, img


def rep_counter(app, angle, side, min_angle, max_angle, tension_stage="up"):
    if side != "left" and side != "right":
        raise ValueError("Side must be 'left' or 'right'")

    # Get the current count
    count = app.rep_count_l.get() if side == "left" else app.rep_count_r.get()
    rep_stage = app.rep_stage_l if side == "left" else app.rep_stage_r

    if angle > max_angle and rep_stage == "up":
        rep_stage = "down"
        count += 1 if tension_stage == 'down' else 0  # Increment the count
        print(f'down {count}')
    elif angle < min_angle and rep_stage == "down":
        rep_stage = "up"
        count += 1 if tension_stage == 'up' else 0  # Increment the count
        print(f'up {count}')

    # Update the IntVar with the new count
    if side == "left":
        app.rep_count_l.set(count)
        app.rep_stage_l = rep_stage
    else:
        app.rep_count_r.set(count)
        app.rep_stage_r = rep_stage
