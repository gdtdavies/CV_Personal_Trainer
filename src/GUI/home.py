import tkinter as tk
from tkinter import messagebox

class HomeGUI:
    
    def __init__(self):
        self.win = tk.Tk()
        
        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")
        
        #login button
        self.login_button = tk.Button(self.win, text="Login", font=("Arial", 18))
        self.login_button.pack(pady=10)
        
        #register button
        self.register_button = tk.Button(self.win, text="Register", font=("Arial", 18))
        self.register_button.pack(pady=10)
        
        #login as guest button (open menu.py)
        self.guest_button = tk.Button(self.win, text="Login as Guest", font=("Arial", 18), command=self.open_menu)
        self.guest_button.pack(pady=10)      
                
        #exit button
        self.exit_button = tk.Button(self.win, text="Exit", font=("Arial", 18), command=self.on_closing)
        self.exit_button.pack(pady=10)
        
        self.win.protocol("WM_DELETE_WINDOW", self.on_closing)      
        self.win.mainloop()
        
    def open_menu(self):
        self.win.destroy()
        import menu
        menu.MenuGUI()
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.win.destroy()
        
        
if __name__ == "__main__":
    HomeGUI()