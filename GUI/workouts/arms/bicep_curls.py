import os
import sys
import tkinter as tk
from tkinter import messagebox


sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from src.workouts.arms.bicep_curls import BicepCurlsApp


class BicepCurlsGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x960")
        self.title("Bicep Curls")

        app = BicepCurlsApp(self)
        app.pack()

        self.label = tk.Label(self, text="Bicep Curls", font=("Arial", 24))
        self.label.pack()

        self.back_button = tk.Button(self, text="Back", font=("Arial", 18), command=self.open_menu)
        self.back_button.pack(pady=10)

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
