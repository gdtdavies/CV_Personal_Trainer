import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from src.workouts.arms.bicep_curls import BicepCurlsApp


class BicepCurlsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x480")
        self.title("Bicep Curls")

        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)

        app = BicepCurlsApp(self, (self.left_var, self.right_var))
        app.pack(side=tk.LEFT)

        self.label = tk.Label(self, text="Bicep Curls", font=("Arial", 24))
        self.label.pack()

        # switch button between left and right bicep curls
        self.lr_var = tk.StringVar(value="left")

        # Create frames for left and right button-label pairs
        left_frame = tk.Frame(self)
        right_frame = tk.Frame(self)

        # populate left frame
        self.left_button = tk.Radiobutton(
            left_frame, text="Left", font=("Arial", 18), variable=self.lr_var, value="left", command=app.left_side)
        self.rep_count_l = tk.Label(left_frame, textvariable=self.left_var, font=("Arial", 18))
        self.left_button.pack(side=tk.LEFT)
        self.rep_count_l.pack(side=tk.LEFT)

        # populate right frame
        self.right_button = tk.Radiobutton(
            right_frame, text="Right", font=("Arial", 18), variable=self.lr_var, value="right", command=app.right_side)
        self.rep_count_r = tk.Label(right_frame, textvariable=self.right_var, font=("Arial", 18))
        self.right_button.pack(side=tk.LEFT)
        self.rep_count_r.pack(side=tk.LEFT)

        left_frame.pack()
        right_frame.pack()

        # back button
        self.back_button = tk.Button(self, text="Back", font=("Arial", 18), command=self.open_menu)
        self.back_button.pack(pady=10)

        # Exit button
        exit_button = tk.Button(self, text="Exit", font=("Arial", 18), command=self.on_closing)
        exit_button.pack(pady=10)

        self.mainloop()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

    def open_menu(self):
        self.destroy()
        from .armsGUI import ArmsGUI
        ArmsGUI()


if __name__ == "__main__":
    BicepCurlsGUI()
