import tkinter as tk
from tkinter import messagebox


class LegsGUI:
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        # label
        self.label = tk.Label(self.win, text="Legs", font=("Arial", 24))
        self.label.pack()

        # squat button
        self.squat_button = tk.Button(self.win, text="Squat", font=("Arial", 18), command=self.not_implemented)
        self.squat_button.pack(pady=10)
        
        # leg press button
        self.leg_press_button = tk.Button(self.win, text="Leg Press", font=("Arial", 18), command=self.not_implemented)
        self.leg_press_button.pack(pady=10)
        
        # leg curl button
        self.leg_curl_button = tk.Button(self.win, text="Leg Curl", font=("Arial", 18), command=self.not_implemented)
        self.leg_curl_button.pack(pady=10)
        
        # leg extension button
        self.leg_extension_button = tk.Button(self.win, text="Leg Extension", font=("Arial", 18), command=self.not_implemented)
        self.leg_extension_button.pack(pady=10)
        
        # calf raise button
        self.calf_raise_button = tk.Button(self.win, text="Calf Raise", font=("Arial", 18), command=self.not_implemented)
        self.calf_raise_button.pack(pady=10)

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
    LegsGUI()
