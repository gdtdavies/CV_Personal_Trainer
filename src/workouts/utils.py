import cv2
import numpy as np
from PIL import Image, ImageTk


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


def rep_counter(app, angle, side, min_angle, max_angle, tension_angle='low'):
    if side != "left" and side != "right":
        raise ValueError("Side must be 'left' or 'right'")

    # Get the current count
    count = app.rep_count_l.get() if side == "left" else app.rep_count_r.get()
    rep_stage = app.rep_stage_l.get() if side == "left" else app.rep_stage_r.get()

    if tension_angle == 'low': # e.g. bicep curls
        if angle > max_angle and rep_stage == "up":
            rep_stage = "down"
        elif angle < min_angle and rep_stage == "down":
            rep_stage = "up"
            count += 1
    elif tension_angle == 'high': # e.g. shoulder press
        if angle > max_angle and rep_stage == "down":
            rep_stage = "up"
            count += 1
        elif angle < min_angle and rep_stage == "up":
            rep_stage = "down"

    # Update the IntVar with the new count
    if side == "left":
        app.rep_count_l.set(count)
        app.rep_stage_l.set(rep_stage)
    else:
        app.rep_count_r.set(count)
        app.rep_stage_r.set(rep_stage)


def run(app):
    ret, frame = app.cap.read()

    if ret:
        results, img = make_detections(app, frame)
        if app.active:
            app.display_skeleton(img, results)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        app.image_label.imgtk = img_tk
        app.image_label.configure(image=img_tk)
    app.after(10, lambda: run(app))
