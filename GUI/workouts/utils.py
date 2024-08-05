import os
import sys
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))


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


def login(username, password, mood_rating):
    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    # Hash the entered password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Retrieve the stored hashed password
    query = "SELECT password FROM cv_pt.public.users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result and result[0] == hashed_password:
        # Generate session token
        session_token = str(uuid.uuid4())
        query = "SELECT * FROM cv_pt.public.start_session(%s, %s, %s)"
        cursor.execute(query, (session_token, username, mood_rating))
        conn.commit()

        # Store session token
        session_token_path = os.path.join(os.path.dirname(__file__), '../../src/db/session_token.txt')
        with open(session_token_path, "w") as f:
            f.write(session_token)
        db.close()

        # open menu window
        from GUI.menu import MenuGUI
        MenuGUI()
    else:
        messagebox.showerror("Error", "Invalid username or password")
        db.close()


def get_mood():
    popup_root = tk.Tk()
    popup_root.withdraw()  # Hide the root window

    popup = tk.Toplevel(popup_root)
    popup.title("Mood Rating")

    popup.geometry("300x150")

    label = tk.Label(popup, text="Rate your mood on a scale of 1 to 10:")
    label.pack(pady=10)

    scale = tk.Scale(popup, from_=1, to=10, orient=tk.HORIZONTAL)
    scale.pack(pady=10)

    mood_rating = tk.IntVar()

    def submit_mood():
        mood_rating.set(scale.get())
        popup.destroy()

    button = tk.Button(popup, text="Submit", command=submit_mood)
    button.pack(pady=10)

    popup.wait_window()
    popup_root.destroy()

    return mood_rating.get()



