import tkinter as tk
from tkinter import messagebox


class BackGUI:
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        # label
        self.label = tk.Label(self.win, text="Back", font=("Arial", 24))
        self.label.pack()

        # deadlift button
        self.deadlift_button = tk.Button(self.win, text="Deadlift", font=("Arial", 18), command=self.not_implemented)
        self.deadlift_button.pack(pady=10)
        
        # pull up button
        self.pull_up_button = tk.Button(self.win, text="Pull Up", font=("Arial", 18), command=self.not_implemented)
        self.pull_up_button.pack(pady=10)
        
        # row button
        self.row_button = tk.Button(self.win, text="Row", font=("Arial", 18), command=self.not_implemented)
        self.row_button.pack(pady=10)
        
        # lat pulldown button
        self.lat_pulldown_button = tk.Button(self.win, text="Lat Pulldown", font=("Arial", 18), command=self.not_implemented)
        self.lat_pulldown_button.pack(pady=10)
        
        # straight arm pulldown button
        self.straight_arm_pulldown_button = tk.Button(self.win, text="Straight Arm Pulldown", font=("Arial", 18), command=self.not_implemented)
        self.straight_arm_pulldown_button.pack(pady=10)

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
    BackGUI()
