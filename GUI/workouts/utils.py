import os
import uuid

from PIL import Image, ImageTk


def load_image(gui, image_path):
    img = Image.open(image_path)
    img = img.resize((214, 188))
    img_tk = ImageTk.PhotoImage(img)
    gui.image_label.imgtk = img_tk
    gui.image_label.configure(image=img_tk)


def save_set(gui):
    gui.set_weights.append(gui.weight.get())
    gui.set_reps.append((gui.left_var.get(), gui.right_var.get()))
    gui.left_var.set(0)
    gui.right_var.set(0)


def start_workout(workout_name):
    workout_token = str(uuid.uuid4())
    session_token_path = os.path.join(os.path.dirname(__file__), '../../src/db/session_token.txt')
    if not os.path.exists(session_token_path):
        print("Session token not found")
        return None
    print("Starting workout")
    try:
        with open(session_token_path, "r") as f:
            session_token = f.read().strip()
    except FileNotFoundError:
        return None

    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    query = "SELECT * FROM cv_pt.public.start_workout(%s, %s, %s)"
    cursor.execute(query, (workout_token, session_token, workout_name))
    conn.commit()

    return workout_token


def end_workout(workout_token, set_reps, set_weights):
    session_token_path = os.path.join(os.path.dirname(__file__), '../../src/db/session_token.txt')
    if not os.path.exists(session_token_path):
        print("Session token not found")
        return None
    print("Ending workout")
    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    if set_weights:
        weight = max(set_weights)
    else:
        weight = 0
    reps = 0
    for r in set_reps:
        reps += r[0] if r[0] > r[1] else r[1]
    volume = 0
    for w, r in zip(set_weights, set_reps):
        rep_count = r[0] if r[0] > r[1] else r[1]
        volume += rep_count * w

    query = "SELECT * FROM cv_pt.public.end_workout(%s, %s, %s, %s)"
    cursor.execute(query, (workout_token, reps, weight, volume))
    conn.commit()
