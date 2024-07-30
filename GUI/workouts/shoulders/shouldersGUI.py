import tkinter as tk
from tkinter import messagebox


class ShouldersGUI:
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        # label
        self.label = tk.Label(self.win, text="Shoulders", font=("Arial", 24))
        self.label.pack()

        # shoulder press button
        self.shoulder_press_button = tk.Button(self.win, text="Shoulder Press", font=("Arial", 18), command=self.not_implemented)
        self.shoulder_press_button.pack(pady=10)
        
        # lateral raise button
        self.lateral_raise_button = tk.Button(self.win, text="Lateral Raise", font=("Arial", 18), command=self.not_implemented)
        self.lateral_raise_button.pack(pady=10)
        
        # front raise button
        self.front_raise_button = tk.Button(self.win, text="Front Raise", font=("Arial", 18), command=self.not_implemented)
        self.front_raise_button.pack(pady=10)
        
        # face pull button
        self.face_pull_button = tk.Button(self.win, text="Face Pull", font=("Arial", 18), command=self.not_implemented)
        self.face_pull_button.pack(pady=10)

        # back button
        self.back_button = tk.Button(self.win, text="Return", font=("Arial", 18), command=self.open_menu)
        self.back_button.pack(pady=10)
        
        # Exit button
        exit_button = tk.Button(self.win, text="Exit", font=("Arial", 18), command=self.on_closing)
        exit_button.pack(pady=10)
        
        self.win.mainloop()
        
    def not_implemented(self):
        messagebox.showinfo("Not Implemented", "This feature is not implemented yet.")
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.win.destroy()
            
    def open_menu(self):
        self.win.destroy()
        import menu
        menu.MenuGUI()


if __name__ == "__main__":
    ShouldersGUI()
