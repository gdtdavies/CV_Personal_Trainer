import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts


class ShouldersGUI(tk.Tk):
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
        self.title_label = tk.Label(title_frame, text="Shoulders", font=f['title'], bg=cp['label'], border=3,
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
        facepull_label = tk.Label(workout_column, text="Face Pull", font=f['regular'], bg=cp['label'])
        frontraise_label = tk.Label(workout_column, text="Front Raise", font=f['regular'], bg=cp['label'])
        latraise_label = tk.Label(workout_column, text="Lateral Raise", font=f['regular'], bg=cp['label'])
        press_label = tk.Label(workout_column, text="Shoulder Press", font=f['regular'], bg=cp['label'])


        # Images
        facepull_img_label = self.load_image("facepull.png", workout_column)
        frontraise_img_label = self.load_image("frontraise.png", workout_column)
        latraise_img_label = self.load_image("latraise.png", workout_column)
        press_img_label = self.load_image("press.png", workout_column)

        # Buttons
        facepull_button = tk.Button(workout_column, text="Face Pull", font=f['regular'], bg=cp['button'],
                                 command=self.not_implemented)
        frontraise_button = tk.Button(workout_column, text="Front Raise", font=f['regular'], bg=cp['button'],
                                    command=self.not_implemented)
        latraise_button = tk.Button(workout_column, text="Lateral Raise", font=f['regular'], bg=cp['button'],
                                    command=self.not_implemented)
        press_button = tk.Button(workout_column, text="Shoulder Press", font=f['regular'], bg=cp['button'],
                                    command=self.open_press)

        # Grid layout
        facepull_label.grid(row=0, column=0, padx=5, pady=5)
        frontraise_label.grid(row=1, column=0, padx=5, pady=5)
        latraise_label.grid(row=2, column=0, padx=5, pady=5)
        press_label.grid(row=3, column=0, padx=5, pady=5)

        facepull_img_label.grid(row=0, column=1, padx=5, pady=5)
        frontraise_img_label.grid(row=1, column=1, padx=5, pady=5)
        latraise_img_label.grid(row=2, column=1, padx=5, pady=5)
        press_img_label.grid(row=3, column=1, padx=5, pady=5)

        facepull_button.grid(row=0, column=2, padx=5, pady=5)
        frontraise_button.grid(row=1, column=2, padx=5, pady=5)
        latraise_button.grid(row=2, column=2, padx=5, pady=5)
        press_button.grid(row=3, column=2, padx=5, pady=5)

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

    def load_image(self, img_file, frame):
        img = Image.open(self.img_loc + img_file)
        img = img.resize((107, 94))
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(frame, image=img, bg=cp['label'])
        img_label.image = img
        return img_label

    def open_press(self):
        self.destroy()
        from GUI.workouts.shoulders.press import ShoulderPressGUI
        ShoulderPressGUI()
        
    def not_implemented(self):
        messagebox.showinfo("Not Implemented", "This feature is not implemented yet.")
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()
            
    def open_menu(self):
        self.destroy()
        from GUI.menu import MenuGUI
        MenuGUI()


if __name__ == "__main__":
    ShouldersGUI()
