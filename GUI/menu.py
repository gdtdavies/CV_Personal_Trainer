import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from GUI.colour_palette import colours as cp
from GUI.fonts import Fonts
from GUI.workouts import utils


class MenuGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("440x300")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        # Header
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="MENU", font=f['title'], bg=cp['label'], border=3,
                                    relief=tk.SUNKEN)
        self.title_label.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame ---------------------------------------------------------------------------------------------------
        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Menu frame ---------------------------------------------------------------------------------------------------
        menu_frame = tk.Frame(main_frame, bg=cp['bg'])
        menu_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True, pady=15, padx=15)
        menu_frame.grid_rowconfigure(0, weight=1)
        menu_frame.grid_rowconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(0, weight=1)
        menu_frame.grid_columnconfigure(1, weight=1)
        menu_frame.grid_columnconfigure(2, weight=1)

        # Buttons
        buttons = {
            "Arms": self.open_arms,
            "Back": self.open_back,
            "Cardio": self.open_cardio,
            "Chest": self.open_chest,
            "Legs": self.open_legs,
            "Shoulders": self.open_shoulders
        }

        row, col = 0, 0
        for text, command in buttons.items():
            button = tk.Button(menu_frame, text=text, font=f['regular'], bg=cp['button'], command=command)
            button.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            col += 1
            if col > 2:
                col = 0
                row += 1

        # Footer frame -------------------------------------------------------------------------------------------------
        footer_frame = tk.Frame(self, bg=cp['label'])
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        if os.path.exists(os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')):
            history_button = tk.Button(buttons_frame, text="History", font=f['regular'], bg=cp['button'],
                                          command=self.open_history)
            history_button.pack(side=tk.LEFT, padx=10)

        back_button = tk.Button(buttons_frame, text="Logout", font=f['regular'], bg=cp['button'],
                                command=self.open_home)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            from src.db.login_session import logout
            logout()
            self.destroy()

    def open_home(self):
        from GUI.home import HomeGUI
        if os.path.exists(os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')):
            if messagebox.askyesno("Quit", "Do you want to logout?"):
                from src.db.login_session import logout
                logout()
        self.destroy()
        HomeGUI()

    def open_history(self):
        self.destroy()
        from GUI.history import HistoryGUI
        HistoryGUI()

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
