import tkinter as tk
from tkinter import messagebox

class ArmsGUI:
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        #label
        self.label = tk.Label(self.win, text="Arms", font=("Arial", 24))
        self.label.pack()
        
        #--------------------------------------------------------------------------------------------------------------
        
        #bicep curl button
        self.bicep_button = tk.Button(self.win, text="Bicep", font=("Arial", 18), command=self.not_implemented)
        self.bicep_button.pack(pady=10)
        
        #tricep pushdown button
        self.tricep_button = tk.Button(self.win, text="Tricep", font=("Arial", 18), command=self.not_implemented)
        self.tricep_button.pack(pady=10)
        
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
    ArmsGUI()