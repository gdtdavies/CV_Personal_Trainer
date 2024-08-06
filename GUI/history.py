import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts
from GUI.workouts import utils


class HistoryGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Computer Vision Personal Trainer")

        f = Fonts().get_fonts()
        self.selected_idx = None

        # Header
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="HISTORY", font=f['title'], bg=cp['label'], border=3,
                                    relief=tk.SUNKEN)
        self.title_label.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame ---------------------------------------------------------------------------------------------------
        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Menu frame ---------------------------------------------------------------------------------------------------
        menu_frame = tk.Frame(main_frame, bg=cp['bg'])
        menu_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True, pady=15, padx=15)

        # Sessions frame -----------------------------------------------------------------------------------------------
        sessions_canvas = tk.Canvas(menu_frame, bg=cp['bg'], width=200)
        sessions_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sessions_scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=sessions_canvas.yview)
        sessions_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        sessions_canvas.configure(yscrollcommand=sessions_scrollbar.set)
        sessions_canvas.bind('<Configure>',
                             lambda e: sessions_canvas.configure(scrollregion=sessions_canvas.bbox("all")))

        sessions_frame = tk.Frame(sessions_canvas, bg=cp['bg'])
        sessions_canvas.create_window((0, 0), window=sessions_frame, anchor="nw")

        self.fill_sessions_frame(sessions_frame)

        # Workouts frame -----------------------------------------------------------------------------------------------
        workouts_canvas = tk.Canvas(menu_frame, bg=cp['bg'], width=400)
        workouts_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        workouts_scrollbar = tk.Scrollbar(menu_frame, orient="vertical", command=workouts_canvas.yview)
        workouts_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        workouts_canvas.configure(yscrollcommand=workouts_scrollbar.set)
        workouts_canvas.bind('<Configure>',
                             lambda e: workouts_canvas.configure(scrollregion=workouts_canvas.bbox("all")))

        self.workouts_frame = tk.Frame(workouts_canvas, bg=cp['bg'])
        workouts_canvas.create_window((0, 0), window=self.workouts_frame, anchor="nw")

        # Footer frame -------------------------------------------------------------------------------------------------
        footer_frame = tk.Frame(self, bg=cp['label'])
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Menu", font=f['regular'], bg=cp['button'],
                                command=self.open_menu)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def fill_sessions_frame(self, frame):
        from src.db.db_connection import DBConnection

        session_token_path = os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')
        if not os.path.exists(session_token_path):
            print("Session token not found")
            return

        with open(session_token_path, "r") as f:
            session_token = f.read().strip()

        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        query = "SELECT username FROM cv_pt.public.sessions WHERE sessions.id = %s"
        cursor.execute(query, (session_token,))
        username = cursor.fetchone()[0]

        query = "SELECT id, created_at FROM cv_pt.public.sessions WHERE sessions.username = %s"
        cursor.execute(query, (username,))
        sessions = cursor.fetchall()

        session_ids = [session[0] for session in sessions]

        def set_selected_idx(index):
            self.selected_idx = index
            self.fill_workouts_frame(session_ids[self.selected_idx])

        for idx, session in enumerate(sessions):
            created_at = str(session[1]).split(".")[0]
            button = tk.Button(frame, text=created_at, font=Fonts().get_fonts()['radio'], bg=cp['button'],
                               command=lambda i=idx: set_selected_idx(i))
            button.pack(fill=tk.BOTH, expand=True, pady=5, padx=5)

        if self.selected_idx is not None:
            self.fill_workouts_frame(session_ids[self.selected_idx])

        db.close()

    def fill_workouts_frame(self, session_id):
        print(f"Session ID: {session_id}")
        from src.db.db_connection import DBConnection

        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        # Retrieve the workout details for the given session_token
        query = """
            SELECT name, duration, reps, max_weight, volume 
            FROM cv_pt.public.workouts 
            WHERE session_id = %s
            """
        cursor.execute(query, (session_id,))
        workouts = cursor.fetchall()

        # Process the workouts data
        processed_workouts = []
        for workout in workouts:
            name, duration, reps, max_weight, volume = workout
            duration = str(duration).split('.')[0]  # Split duration and take the first part
            processed_workouts.append((name, duration, reps, max_weight, volume))

        # Clear the frame before adding new widgets
        for widget in self.workouts_frame.winfo_children():
            widget.destroy()

        # Create table headers
        headers = ["Name", "Duration", "Reps", "Max Weight", "Volume"]
        for col, header in enumerate(headers):
            label = tk.Label(self.workouts_frame, text=header, font=Fonts().get_fonts()['small'], bg=cp['label'])
            label.grid(row=0, column=col, padx=5, pady=5)

        # Populate the table with workout data
        for row, workout in enumerate(processed_workouts, start=1):
            for col, value in enumerate(workout):
                label = tk.Label(self.workouts_frame, text=value, font=Fonts().get_fonts()['small'], bg=cp['bg'])
                label.grid(row=row, column=col, padx=5, pady=5)

        db.close()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            from src.db.login_session import logout
            session_token = os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')
            mood = utils.get_mood() if os.path.exists(session_token) else None
            logout(mood)
            self.destroy()

    def open_menu(self):
        from GUI.menu import MenuGUI
        self.destroy()
        MenuGUI()


if __name__ == "__main__":
    HistoryGUI()
