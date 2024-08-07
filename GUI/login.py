import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


class LoginGUI(tk.Tk):

    entry_width = 15
    session_token = os.path.join(os.path.dirname(__file__), '../src/db/session_token.txt')

    def __init__(self):
        super().__init__()
        self.geometry("440x400")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        from GUI.colour_palette import colours as cp
        from GUI.fonts import Fonts

        f = Fonts().get_fonts()

        # Header
        title_frame = tk.Frame(self)
        self.title_label = tk.Label(title_frame, text="LOGIN", font=f['title'], bg=cp['label'], border=3,
                                    relief=tk.SUNKEN)
        self.title_label.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame ---------------------------------------------------------------------------------------------------
        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        login_frame = tk.Frame(main_frame, bg=cp['label'])
        login_frame.pack(anchor=tk.CENTER, expand=True, ipady=30, ipadx=30)

        # Username
        username_frame = tk.Frame(login_frame, bg=cp['label'])
        username_frame.pack(side=tk.TOP, expand=True)

        self.username_label = tk.Label(username_frame, text="Username ", font=f['regular'], bg=cp['label'])
        self.username_entry = tk.Entry(username_frame, font=f['regular'], width=self.entry_width)
        self.username_label.pack(side=tk.LEFT, pady=5)
        self.username_entry.pack(side=tk.LEFT, pady=5)

        # Password
        password_frame = tk.Frame(login_frame, bg=cp['label'])
        password_frame.pack(side=tk.TOP, expand=True)

        self.password_label = tk.Label(password_frame, text="Password ", font=f['regular'], bg=cp['label'])
        self.password_entry = tk.Entry(password_frame, font=f['regular'], show="*", width=self.entry_width)
        self.password_label.pack(side=tk.LEFT, pady=5)
        self.password_entry.pack(side=tk.LEFT, pady=5)

        # Login Button
        login_button = tk.Button(login_frame, text="Login", font=f['regular'], bg=cp['button'], command=self.login)
        login_button.pack(side=tk.TOP, pady=10)

        # Footer frame -------------------------------------------------------------------------------------------------
        footer_frame = tk.Frame(self, bg=cp['label'])
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Return", font=f['regular'], bg=cp['button'],
                                command=self.open_home)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def login(self):
        from GUI.workouts.utils import login, get_mood
        username = self.username_entry.get()
        password = self.password_entry.get()

        mood = get_mood()
        self.destroy()
        login(username, password, mood)

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

    def open_home(self):
        self.destroy()
        import home
        home.HomeGUI()


if __name__ == "__main__":
    LoginGUI()
