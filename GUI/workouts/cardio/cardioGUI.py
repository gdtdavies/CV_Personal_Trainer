import os
import sys
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts
import GUI.workouts.utils as utils


class CardioGUI(tk.Tk):

    img_loc = os.path.join(os.path.dirname(__file__), 'assets/')
    session_token = os.path.join(os.path.dirname(__file__), '../../../src/db/session_token.txt')

    def __init__(self):
        super().__init__()
        self.geometry("640x500")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        # Title frame --------------------------------------------------------------------------------------------------
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="CARDIO", font=f['title'], bg=cp['label'], border=3,
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

        # Images
        elliptical_img_label = utils.load_image_label(self, "elliptical.png", workout_column)
        rowing_img_label = utils.load_image_label(self, "rowing.png", workout_column)
        treadmill_img_label = utils.load_image_label(self, "treadmill.png", workout_column)

        # Buttons
        elliptical_btn = tk.Button(workout_column, text="Elliptical", font=f['regular'], bg=cp['button'],
                                 command=utils.not_implemented)
        rowing_btn = tk.Button(workout_column, text="Rowing Machine", font=f['regular'], bg=cp['button'],
                                 command=utils.not_implemented)
        treadmill_btn = tk.Button(workout_column, text="Treadmill", font=f['regular'], bg=cp['button'],
                                 command=utils.not_implemented)

        # Grid layout
        elliptical_img_label.grid(row=0, column=0, padx=5, pady=5)
        rowing_img_label.grid(row=1, column=0, padx=5, pady=5)
        treadmill_img_label.grid(row=2, column=0, padx=5, pady=5)

        elliptical_btn.grid(row=0, column=1, padx=5, pady=5)
        rowing_btn.grid(row=1, column=1, padx=5, pady=5)
        treadmill_btn.grid(row=2, column=1, padx=5, pady=5)

        # Buttons frame ------------------------------------------------------------------------------------------------
        buttons_frame = tk.Frame(main_frame, bg=cp['label'])
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Button column
        button_column = tk.Frame(buttons_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        button_column.pack(anchor=tk.CENTER, expand=True)

        # Back button
        back_btn = tk.Button(button_column, text="Return", font=f['regular'], bg=cp['button'],
                                command=lambda: utils.open_menu(self))
        back_btn.pack(side=tk.TOP, padx=10, pady=10)

        # Exit button
        exit_btn = tk.Button(button_column, text="Exit", font=f['regular'], bg=cp['button'],
                                command=lambda: utils.on_closing(self))
        exit_btn.pack(side=tk.TOP, padx=10, pady=10)

        self.protocol("WM_DELETE_WINDOW", lambda: utils.on_closing(self))
        self.mainloop()

    def open_bicep(self):
        self.destroy()
        from GUI.workouts.arms.bicep_curls import BicepCurlsGUI
        BicepCurlsGUI()

    def open_tricep(self):
        self.destroy()
        from GUI.workouts.arms.tricep_extension import TricepExtensionGUI
        TricepExtensionGUI()


if __name__ == "__main__":
    CardioGUI()
