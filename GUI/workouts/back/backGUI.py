import os
import sys
import tkinter as tk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts
import GUI.workouts.utils as utils


class BackGUI(tk.Tk):
    img_loc = os.path.join(os.path.dirname(__file__), 'assets/')
    session_token = os.path.join(os.path.dirname(__file__), '../../../src/db/session_token.txt')

    def __init__(self):
        super().__init__()
        self.geometry("640x600")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        # Title frame --------------------------------------------------------------------------------------------------
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="Back", font=f['title'], bg=cp['label'], border=3,
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
        deadlift_img_label = utils.load_image_label(self, "deadlift.png", workout_column)
        latpulldown_img_label = utils.load_image_label(self, "latpulldown.png", workout_column)
        pullups_img_label = utils.load_image_label(self, "pullups.png", workout_column)
        row_img_label = utils.load_image_label(self, "row.png", workout_column)

        # Buttons
        deadlift_btn = tk.Button(workout_column, text="Deadlift", font=f['regular'], bg=cp['button'],
                                    command=lambda: utils.not_implemented(self))
        latpulldown_btn = tk.Button(workout_column, text="Lateral Pulldown", font=f['regular'], bg=cp['button'],
                                      command=lambda: utils.not_implemented(self))
        pullups_btn = tk.Button(workout_column, text="Pull-ups", font=f['regular'], bg=cp['button'],
                                    command=lambda: utils.not_implemented(self))
        row_btn = tk.Button(workout_column, text="Row", font=f['regular'], bg=cp['button'],
                                 command=lambda: utils.not_implemented(self))

        deadlift_img_label.grid(row=0, column=0, padx=5, pady=5)
        latpulldown_img_label.grid(row=1, column=0, padx=5, pady=5)
        pullups_img_label.grid(row=2, column=0, padx=5, pady=5)
        row_img_label.grid(row=3, column=0, padx=5, pady=5)

        deadlift_btn.grid(row=0, column=1, padx=5, pady=5)
        latpulldown_btn.grid(row=1, column=1, padx=5, pady=5)
        pullups_btn.grid(row=2, column=1, padx=5, pady=5)
        row_btn.grid(row=3, column=1, padx=5, pady=5)

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


if __name__ == "__main__":
    BackGUI()
