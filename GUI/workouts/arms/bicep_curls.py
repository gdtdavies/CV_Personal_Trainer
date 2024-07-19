import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from src.workouts.arms.bicep_curls import BicepCurler


class BicepCurlsApp:
    def __init__(self):
        self.win = tk.Tk()
        self.win.geometry("1280x960")
        self.win.title("Bicep Curls")

        self.bicep_curler = BicepCurler()

        self.label = tk.Label(self.win, text="Bicep Curls", font=("Arial", 24))
        self.label.pack()

        self.start_button = tk.Button(self.win, text="Start", font=("Arial", 18), command=self.start)
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(self.win, text="Back", font=("Arial", 18), command=self.open_menu)
        self.back_button.pack(pady=10)

        exit_button = tk.Button(self.win, text="Exit", font=("Arial", 18), command=self.on_closing)
        exit_button.pack(pady=10)

        self.win.mainloop()

    def start(self):
        self.bicep_curler.run()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.win.destroy()

    def open_menu(self):
        self.win.destroy()
        from armsGUI import ArmsGUI
        ArmsGUI()


if __name__ == "__main__":
    BicepCurlsApp()
