import tkinter as tk
from tkinter import messagebox

class ChestGUI:
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        #label
        self.label = tk.Label(self.win, text="Chest", font=("Arial", 24))
        self.label.pack()
        
        #--------------------------------------------------------------------------------------------------------------
        
        #bench press button
        self.bench_press_button = tk.Button(self.win, text="Bench Press", font=("Arial", 18), command=self.not_implemented)
        self.bench_press_button.pack(pady=10)
        
        #dumbbell press button
        self.dumbbell_press_button = tk.Button(self.win, text="Dumbbell Press", font=("Arial", 18), command=self.not_implemented)
        self.dumbbell_press_button.pack(pady=10)
        
        #pec-fly button
        self.pec_fly_button = tk.Button(self.win, text="Fly", font=("Arial", 18), command=self.not_implemented)
        self.pec_fly_button.pack(pady=10)
        
        #--------------------------------------------------------------------------------------------------------------
        
        #back button
        self.back_button = tk.Button(self.win, text="Back", font=("Arial", 18), command=self.open_menu)
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
    ChestGUI()