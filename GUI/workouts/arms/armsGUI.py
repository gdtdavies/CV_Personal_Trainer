import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class ArmsGUI(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Computer Vision Personal Trainer")

        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
        from GUI.colour_palette import colours as cp
        from GUI.fonts import title_font, regular_font

        # --------------------------------------------------------------------------------------------------------------
        # MENU LAYOUT---------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # Title frame
        title_frame = tk.Frame(self)
        self.title = tk.Label(title_frame, text="ARMS", font=title_font, bg=cp['label'], border=3, relief=tk.SUNKEN)
        self.title.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --------------------------------------------------------------------------------------------------------------
        # WORKOUT GRID--------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # workout frame
        workout_frame = tk.Frame(main_frame, bg=cp['bg'], border=3, relief=tk.RAISED)
        workout_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # workout column
        workout_column = tk.Frame(workout_frame, bg=cp['label'], padx=10, pady=10)
        workout_column.pack(anchor=tk.CENTER, expand=True)

        # -Labels-------------------------------------------------------------------------------------------------------
        bicep_label = tk.Label(workout_column, text="Bicep Curls", font=regular_font)
        tricep_label = tk.Label(workout_column, text="Tricep Pushdown", font=regular_font)

        # -Images-------------------------------------------------------------------------------------------------------
        bicep_image = Image.open("assets/bicep_curl.png")
        bicep_image = bicep_image.resize((107, 94))
        bicep_image = ImageTk.PhotoImage(bicep_image)
        bicep_image_label = tk.Label(workout_column, image=bicep_image)
        bicep_image_label.image = bicep_image

        tricep_image = Image.open("assets/tricep_pushdown.png")
        tricep_image = tricep_image.resize((107, 94))
        tricep_image = ImageTk.PhotoImage(tricep_image)
        tricep_image_label = tk.Label(workout_column, image=tricep_image)
        tricep_image_label.image = tricep_image

        # -Buttons------------------------------------------------------------------------------------------------------
        bicep_button = tk.Button(workout_column, text="Bicep Curls", font=regular_font, bg=cp['button'],
                                 command=self.open_curls)
        tricep_button = tk.Button(workout_column, text="Tricep Pushdown", font=regular_font, bg=cp['button'],
                                  command=self.not_implemented)

        # -Grid layout--------------------------------------------------------------------------------------------------
        bicep_label.grid(row=0, column=0)
        tricep_label.grid(row=1, column=0)
        bicep_image_label.grid(row=0, column=1)
        tricep_image_label.grid(row=1, column=1)
        bicep_button.grid(row=0, column=2)
        tricep_button.grid(row=1, column=2)

        # --------------------------------------------------------------------------------------------------------------
        # BUTTONS LAYOUT------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # buttons frame
        buttons_frame = tk.Frame(main_frame, bg=cp['label'])
        buttons_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # button column
        button_column = tk.Frame(buttons_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        button_column.pack(anchor=tk.CENTER, expand=True)

        # back button
        back_button = tk.Button(button_column, text="Back", font=regular_font, bg=cp['button'], command=self.open_menu)
        back_button.pack(side=tk.TOP, padx=10, pady=10)

        # exit button
        exit_button = tk.Button(button_column, text="Exit", font=regular_font, bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.TOP, padx=10, pady=10)

        self.mainloop()

    def not_implemented(self):
        messagebox.showinfo("Not Implemented", "This feature is not implemented yet.")

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

    def open_curls(self):
        self.destroy()
        from GUI.workouts.arms.bicep_curls import BicepCurlsGUI
        BicepCurlsGUI()

    def open_menu(self):
        self.destroy()
        from GUI.menu import MenuGUI
        MenuGUI()


if __name__ == "__main__":
    ArmsGUI()
