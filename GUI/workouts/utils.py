import os
import sys
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))


def load_image(gui, image_path):
    img = Image.open(image_path)
    img = img.resize((200, 175))
    img_tk = ImageTk.PhotoImage(img)
    gui.image_label.imgtk = img_tk
    gui.image_label.configure(image=img_tk)


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


def end_workout(workout_token):
    session_token_path = os.path.join(os.path.dirname(__file__), '../../src/db/session_token.txt')
    if not os.path.exists(session_token_path):
        print("Session token not found")
        return None
    print("Ending workout")
    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    cursor.execute('SELECT weight FROM cv_pt.public.sets WHERE workout_id = %s', (workout_token,))
    set_weights = cursor.fetchall()
    set_weights = [int(row[0]) for row in set_weights]

    cursor.execute('SELECT reps FROM cv_pt.public.sets WHERE workout_id = %s', (workout_token,))
    set_reps = cursor.fetchall()
    set_reps = [int(row[0]) for row in set_reps]

    max_weight = max(set_weights) if set_weights else 0
    reps = sum(set_reps) if set_reps else 0

    volume = 0
    for w, r in zip(set_weights, set_reps):
        volume += r * w

    query = "SELECT * FROM cv_pt.public.end_workout(%s, %s, %s, %s)"
    cursor.execute(query, (workout_token, reps, max_weight, volume))
    conn.commit()


def login(username, password):
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
        mood_rating = get_mood()

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
        return True
    else:
        # messagebox.showerror("Error", "Invalid username or password")
        db.close()
        return False


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


def add_message(gui, message):
    gui.chat_text.config(state=tk.NORMAL)
    gui.chat_text.insert(tk.END, message + "\n")
    gui.chat_text.insert(tk.END, "-------------------------------\n")
    gui.chat_text.config(state=tk.DISABLED)
    gui.chat_text.yview(tk.END)


def start_set(gui):

    w = gui.weight.get()
    r = gui.rest_time.get()

    if w == 0 or r == 0:
        add_message(gui, "Please set weight and rest time before starting a set.")
        return
    if gui.set_token:
        add_message(gui, "Set already active")
        return
    if gui.is_resting:
        add_message(gui, "Rest timer is active, please wait.")
        return

    add_message(gui, f"Starting set with weight: {str(w)}kg")
    gui.app.toggle_active()

    from GUI.colour_palette import colours as cp
    gui.app_frame.config(bg=cp['active'])
    gui.set_token = str(uuid.uuid4())

    if not os.path.exists(os.path.join(os.path.dirname(__file__), '../../src/db/session_token.txt')):
        print("set will not be saved as user is not logged in")
        return

    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    query = "SELECT * FROM cv_pt.public.start_set(%s, %s)"
    cursor.execute(query, (gui.set_token, gui.workout_token))
    conn.commit()

    db.close()

def end_set(gui):
    if not gui.set_token:
        add_message(gui, "no set active")
        return

    reps = gui.left_var.get() if gui.left_var.get() > gui.right_var.get() else gui.right_var.get()
    gui.left_var.set(0)
    gui.right_var.set(0)

    add_message(gui, f"Ending set with {reps} reps at {gui.weight.get()}kg")
    gui.app.toggle_active()
    from GUI.colour_palette import colours as cp
    gui.app_frame.config(bg=cp['inactive'])

    from src.db.db_connection import DBConnection
    db = DBConnection()
    conn = db.connect()
    cursor = conn.cursor()

    query = "SELECT * FROM cv_pt.public.end_set(%s, %s, %s)"
    cursor.execute(query, (gui.set_token, reps, gui.weight.get()))
    conn.commit()

    gui.set_token = None

    db.close()

    rest_timer(gui, gui.rest_time.get())


def save_params(gui):
    print("Save params")
    w = gui.weight_entry.get()
    r = gui.rest_entry.get()

    if not w or not r:
        add_message(gui, "Please enter a weight and rest time.")
        return

    gui.weight.set(int(w))
    gui.rest_time.set(int(r))
    gui.weight_entry.delete(0, tk.END)
    gui.rest_entry.delete(0, tk.END)

    add_message(gui, f"Set weight to {gui.weight.get()}kg and rest time to {gui.rest_time.get()}s.")


def rest_timer(gui, time_left):
    gui.is_resting = True
    if time_left > 0:
        add_message(gui, f"Rest time left: {time_left} seconds")
        gui.after(1000, rest_timer, gui, time_left - 1)
    else:
        add_message(gui, "Rest time over")
        gui.is_resting = False

def on_closing(gui):
    if messagebox.askyesno("Quit", "Do you want to quit?"):
        end_set(gui)  # Save the last set
        end_workout(gui.workout_token)
        from src.db.login_session import logout
        logout()

        gui.destroy()
