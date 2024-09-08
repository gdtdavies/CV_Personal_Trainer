import tkinter as tk
from tkinter import messagebox


class ShouldersGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry("640x480")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)
        
        # label
        self.label = tk.Label(self, text="Shoulders", font=("Arial", 24))
        self.label.pack()

        # shoulder press button
        self.shoulder_press_button = tk.Button(self, text="Shoulder Press", font=("Arial", 18), command=self.open_press)
        self.shoulder_press_button.pack(pady=10)
        
        # lateral raise button
        self.lateral_raise_button = tk.Button(self, text="Lateral Raise", font=("Arial", 18), command=self.not_implemented)
        self.lateral_raise_button.pack(pady=10)
        
        # front raise button
        self.front_raise_button = tk.Button(self, text="Front Raise", font=("Arial", 18), command=self.not_implemented)
        self.front_raise_button.pack(pady=10)
        
        # face pull button
        self.face_pull_button = tk.Button(self, text="Face Pull", font=("Arial", 18), command=self.not_implemented)
        self.face_pull_button.pack(pady=10)

        # back button
        self.back_button = tk.Button(self, text="Return", font=("Arial", 18), command=self.open_menu)
        self.back_button.pack(pady=10)
        
        # Exit button
        exit_button = tk.Button(self, text="Exit", font=("Arial", 18), command=self.on_closing)
        exit_button.pack(pady=10)
        
        self.mainloop()

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
