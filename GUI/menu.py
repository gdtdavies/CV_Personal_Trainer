import os
import sys
import tkinter as tk
from tkinter import messagebox


class MenuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("440x300")
        self.title("Computer Vision Personal Trainer")

        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
        from GUI.colour_palette import colours as cp
        from GUI.fonts import Fonts

        f = Fonts().get_fonts()

        # --------------------------------------------------------------------------------------------------------------
        # HEADER--------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        title_frame = tk.Frame(self)
        self.title = tk.Label(title_frame, text="MENU", font=f['title'], bg=cp['label'], border=3, relief=tk.SUNKEN)
        self.title.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # --------------------------------------------------------------------------------------------------------------
        # MENU LAYOUT---------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # -Menu Frame---------------------------------------------------------------------------------------------------
        menu_frame = tk.Frame(main_frame, bg=cp['bg'])
        menu_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True, pady=15, padx=15)
        menu_frame.grid_rowconfigure(0, weight=1)
        menu_frame.grid_rowconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(2, weight=1)

        # -Buttons------------------------------------------------------------------------------------------------------
        arms_button = tk.Button(menu_frame, text="Arms", font=f['regular'], bg=cp['button'],
                                command=self.open_arms)
        back_button = tk.Button(menu_frame, text="Back", font=f['regular'], bg=cp['button'],
                                command=self.open_back)
        cardio_button = tk.Button(menu_frame, text="Cardio", font=f['regular'], bg=cp['button'],
                                  command=self.open_cardio)
        chest_button = tk.Button(menu_frame, text="Chest", font=f['regular'], bg=cp['button'],
                                 command=self.open_chest)
        legs_button = tk.Button(menu_frame, text="Legs", font=f['regular'], bg=cp['button'],
                                command=self.open_legs)
        shoulders_button = tk.Button(menu_frame, text="Shoulders", font=f['regular'], bg=cp['button'],
                                     command=self.open_shoulders)

        # -Grid---------------------------------------------------------------------------------------------------------
        arms_button.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
        back_button.grid(row=0, column=1, sticky="nsew", padx=1, pady=1)
        cardio_button.grid(row=0, column=2, sticky="nsew", padx=1, pady=1)
        chest_button.grid(row=1, column=0, sticky="nsew", padx=1, pady=1)
        legs_button.grid(row=1, column=1, sticky="nsew", padx=1, pady=1)
        shoulders_button.grid(row=1, column=2, sticky="nsew", padx=1, pady=1)

        # --------------------------------------------------------------------------------------------------------------
        # FOOTER--------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        footer_frame = tk.Frame(self, bg=cp['label'])
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Return", font=f['regular'], bg=cp['button'], command=self.open_home)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

            from src.db.login_session import logout
            logout()

    def open_home(self):
        # if session is active, ask if logout
        from GUI.home import HomeGUI
        if os.path.exists(os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')):
            if messagebox.askyesno("Quit", "Do you want to logout?"):
                from src.db.login_session import logout
                logout()
                self.destroy()
                HomeGUI()
        else:
            self.destroy()
            HomeGUI()

    def open_arms(self):
        self.destroy()
        from GUI.workouts.arms.armsGUI import ArmsGUI
        ArmsGUI()
        
    def open_back(self):
        self.destroy()
        from GUI.workouts.back.backGUI import BackGUI
        BackGUI()
        
    def open_cardio(self):
        self.destroy()
        from GUI.workouts.cardio.cardioGUI import CardioGUI
        CardioGUI()
        
    def open_chest(self):
        self.destroy()
        from GUI.workouts.chest.chestGUI import ChestGUI
        ChestGUI()
        
    def open_legs(self):
        self.destroy()
        from GUI.workouts.legs.legsGUI import LegsGUI
        LegsGUI()
        
    def open_shoulders(self):
        self.destroy()
        from GUI.workouts.shoulders.shouldersGUI import ShouldersGUI
        ShouldersGUI()


if __name__ == "__main__":
    MenuGUI()
    