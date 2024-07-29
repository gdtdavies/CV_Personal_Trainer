import os
import sys
import uuid
import tkinter as tk
from tkinter import messagebox


class RegisterGUI(tk.Tk):

    entry_width = 15

    def __init__(self):
        super().__init__()
        self.geometry("440x400")
        self.title("Computer Vision Personal Trainer")

        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
        from GUI.colour_palette import colours as cp
        from GUI.fonts import Fonts

        f = Fonts().get_fonts()

        # --------------------------------------------------------------------------------------------------------------
        # HEADER--------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        title_frame = tk.Frame(self)
        self.title = tk.Label(title_frame, text="REGISTER", font=f['title'], bg=cp['label'], border=3, relief=tk.SUNKEN)
        self.title.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # --------------------------------------------------------------------------------------------------------------
        # REGISTER LAYOUT-----------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        main_frame = tk.Frame(self, bg=cp['bg'], border=3, relief=tk.RAISED)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        register_frame = tk.Frame(main_frame, bg=cp['label'])
        register_frame.pack(anchor=tk.CENTER, expand=True, ipady=30, ipadx=30)

        # -Username-----------------------------------------------------------------------------------------------------
        username_frame = tk.Frame(register_frame, bg=cp['label'])
        username_frame.pack(side=tk.TOP, expand=True)

        self.username_label = tk.Label(username_frame, text="    Username     ", font=f['regular'], bg=cp['label'])
        self.username_entry = tk.Entry(username_frame, font=f['regular'], width=self.entry_width)
        self.username_label.pack(side=tk.LEFT, pady=5)
        self.username_entry.pack(side=tk.LEFT, pady=5)

        # -Password-----------------------------------------------------------------------------------------------------
        password_frame = tk.Frame(register_frame, bg=cp['label'])
        password_frame.pack(side=tk.TOP, expand=True)

        self.password_label = tk.Label(password_frame, text="    Password     ", font=f['regular'], bg=cp['label'])
        self.password_entry = tk.Entry(password_frame, font=f['regular'], show="*", width=self.entry_width)
        self.password_label.pack(side=tk.LEFT, pady=5)
        self.password_entry.pack(side=tk.LEFT, pady=5)

        # -Confirm Password---------------------------------------------------------------------------------------------
        c_password_frame = tk.Frame(register_frame, bg=cp['label'])
        c_password_frame.pack(side=tk.TOP, expand=True)

        self.c_password_label = tk.Label(c_password_frame, text="Confirm Password ", font=f['regular'], bg=cp['label'])
        self.c_password_entry = tk.Entry(c_password_frame, font=f['regular'], show="*", width=self.entry_width)
        self.c_password_label.pack(side=tk.LEFT, pady=5)
        self.c_password_entry.pack(side=tk.LEFT, pady=5)

        # -Register button----------------------------------------------------------------------------------------------
        register_button = tk.Button(register_frame, text="Register", font=f['regular'], bg=cp['button'],
                                    command=self.register_user)
        register_button.pack(side=tk.TOP, pady=10)

        # --------------------------------------------------------------------------------------------------------------
        # FOOTER--------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        footer_frame = tk.Frame(self, bg=cp['label'])
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Back", font=f['regular'], bg=cp['button'], command=self.open_home)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def register_user(self):
        if self.password_entry.get() == self.c_password_entry.get():
            from src.db.db_connection import DBConnection
            db = DBConnection()
            conn = db.connect()
            cursor = conn.cursor()

            username = self.username_entry.get()
            password = self.password_entry.get()

            # check if username already exists
            query = "SELECT * from cv_pt.public.check_user(%s)"
            cursor.execute(query, (username,))
            if cursor.fetchone()[0]:
                messagebox.showerror("Error", "Username already exists")
                db.close()
                return

            user_id = str(uuid.uuid4())
            query = "SELECT * from cv_pt.public.create_user(%s, %s, %s)"
            cursor.execute(query, (user_id, username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully")
            db.close()

            # open menu window
            self.destroy()
            from GUI.menu import MenuGUI
            MenuGUI()
        else:
            messagebox.showerror("Error", "Passwords do not match")

    def open_home(self):
        self.destroy()
        import home
        home.HomeGUI()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

            from src.db.login_session import delete_session
            delete_session()


if __name__ == "__main__":
    RegisterGUI()
