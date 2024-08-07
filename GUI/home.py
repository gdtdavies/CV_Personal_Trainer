import os
import sys
import tkinter as tk
from tkinter import messagebox


class HomeGUI(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.geometry("440x400")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
        from GUI.colour_palette import colours as cp
        from GUI.fonts import Fonts

        f = Fonts().get_fonts()

        # --------------------------------------------------------------------------------------------------------------
        # HEADER--------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        title_frame = tk.Frame(self)
        self.title = tk.Label(title_frame, text="CV-PT", font=f['title'], bg=cp['label'], border=3, relief=tk.SUNKEN)
        self.title.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # --------------------------------------------------------------------------------------------------------------
        # HOME LAYOUT---------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        menu_frame = tk.Frame(main_frame, bg=cp['bg'])
        menu_frame.pack(anchor=tk.CENTER, expand=True, pady=30, padx=30)

        # -Login--------------------------------------------------------------------------------------------------------
        login_button = tk.Button(menu_frame, text="Login", font=f['regular'], bg=cp['button'],
                                 command=self.open_login)
        login_button.pack(side=tk.TOP, pady=10)

        # -Register-----------------------------------------------------------------------------------------------------
        register_button = tk.Button(menu_frame, text="Register", font=f['regular'], bg=cp['button'],
                                    command=self.open_register)
        register_button.pack(side=tk.TOP, pady=10)

        # -Guest--------------------------------------------------------------------------------------------------------
        guest_button = tk.Button(menu_frame, text="Login as Guest", font=f['regular'], bg=cp['button'],
                                 command=self.open_menu)
        guest_button.pack(side=tk.TOP, pady=10)

        # --------------------------------------------------------------------------------------------------------------
        # SIDE----------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        side_frame = tk.Frame(self, bg=cp['label'])
        side_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        exit_frame = tk.Frame(side_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        exit_frame.pack(anchor=tk.CENTER, expand=True)

        exit_button = tk.Button(exit_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.TOP, pady=10)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)      
        self.mainloop()
        
    def open_menu(self):
        self.destroy()
        from GUI.menu import MenuGUI
        MenuGUI()

    def open_login(self):
        self.destroy()
        from GUI.login import LoginGUI
        LoginGUI()
        
    def open_register(self):
        self.destroy()
        from GUI.register import RegisterGUI
        RegisterGUI()
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()
        
        
if __name__ == "__main__":
    HomeGUI()
