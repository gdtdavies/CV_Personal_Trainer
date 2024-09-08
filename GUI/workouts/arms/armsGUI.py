import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts
from GUI.workouts import utils


class ArmsGUI(tk.Tk):

    img_loc = os.path.join(os.path.dirname(__file__), 'assets/')
    session_token = os.path.join(os.path.dirname(__file__), '../../../src/db/session_token.txt')

    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        # Title frame --------------------------------------------------------------------------------------------------
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="ARMS", font=f['title'], bg=cp['label'], border=3,
                                    relief=tk.SUNKEN)
        self.title_label.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame --------------------------------------------------------------------------------------------------
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Workout frame ------------------------------------------------------------------------------------------------
        workout_frame = tk.Frame(main_frame, bg=cp['bg'], border=3, relief=tk.RAISED)
        workout_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Workout column
        workout_column = tk.Frame(workout_frame, bg=cp['label'], padx=10, pady=10)
        workout_column.pack(anchor=tk.CENTER, expand=True)

        # Labels
        bicep_label = tk.Label(workout_column, text="Bicep Curls", font=f['regular'], bg=cp['label'])
        tricep_label = tk.Label(workout_column, text="Tricep Pushdown", font=f['regular'], bg=cp['label'])

        # Images
        bicep_image = Image.open(self.img_loc + "bicep_curl.png")
        bicep_image = bicep_image.resize((107, 94))
        bicep_image = ImageTk.PhotoImage(bicep_image)
        bicep_image_label = tk.Label(workout_column, image=bicep_image, bg=cp['label'])
        bicep_image_label.image = bicep_image

        tricep_image = Image.open(self.img_loc + "tricep_pushdown.png")
        tricep_image = tricep_image.resize((107, 94))
        tricep_image = ImageTk.PhotoImage(tricep_image)
        tricep_image_label = tk.Label(workout_column, image=tricep_image, bg=cp['label'])
        tricep_image_label.image = tricep_image

        # Buttons
        bicep_button = tk.Button(workout_column, text="Bicep Curls", font=f['regular'], bg=cp['button'],
                                 command=self.open_curls)
        tricep_button = tk.Button(workout_column, text="Tricep Pushdown", font=f['regular'], bg=cp['button'],
                                  command=self.open_tricep)

        # Grid layout
        bicep_label.grid(row=0, column=0, padx=5, pady=5)
        tricep_label.grid(row=1, column=0, padx=5, pady=5)
        bicep_image_label.grid(row=0, column=1, padx=5, pady=5)
        tricep_image_label.grid(row=1, column=1, padx=5, pady=5)
        bicep_button.grid(row=0, column=2, padx=5, pady=5)
        tricep_button.grid(row=1, column=2, padx=5, pady=5)

        # Buttons frame ------------------------------------------------------------------------------------------------
        buttons_frame = tk.Frame(main_frame, bg=cp['label'])
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button column
        button_column = tk.Frame(buttons_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        button_column.pack(anchor=tk.CENTER, expand=True)

        # Back button
        back_button = tk.Button(button_column, text="Return", font=f['regular'], bg=cp['button'],
                                command=self.open_menu)
        back_button.pack(side=tk.TOP, padx=10, pady=10)

        # Exit button
        exit_button = tk.Button(button_column, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            from src.db.login_session import logout
            logout()
            self.destroy()

    def open_curls(self):
        self.destroy()
        from GUI.workouts.arms.bicep_curls import BicepCurlsGUI
        BicepCurlsGUI()

    def open_tricep(self):
        self.destroy()
        from GUI.workouts.arms.tricep_pushdown import TricepPushdownGUI
        TricepPushdownGUI()

    def open_menu(self):
        self.destroy()
        from GUI.menu import MenuGUI
        MenuGUI()


if __name__ == "__main__":
    ArmsGUI()
