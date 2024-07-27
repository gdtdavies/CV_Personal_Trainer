import os
import sys
import tkinter as tk
from tkinter import messagebox


class RegisterGUI(tk.Tk):

    entry_width = 15

    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Computer Vision Personal Trainer")

        sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
        from GUI.colour_palette import colours as cp
        from GUI.fonts import Fonts

        f = Fonts().get_fonts()

        title_frame = tk.Frame(self)
        title_frame.pack(side=tk.TOP, fill=tk.BOTH)

        label = tk.Label(title_frame, text="Register", font=f['title'], bg=cp['label'], border=3, relief=tk.SUNKEN)
        label.pack(fill=tk.X)

        main_frame = tk.Frame(self, bg=cp['bg'])
        main_frame.pack(side=tk.TOP, expand=True, ipady=30, ipadx=30)

        register_frame = tk.Frame(main_frame, bg=cp['bg'])
        register_frame.pack(anchor=tk.CENTER, expand=True)

        username_frame = tk.Frame(register_frame, bg=cp['bg'])
        username_frame.pack(side=tk.TOP, expand=True)

        self.username_label = tk.Label(username_frame, text="Username", font=f['regular'], bg=cp['label'])
        self.username_entry = tk.Entry(username_frame, font=f['regular'], width=self.entry_width)
        self.username_label.pack(side=tk.LEFT, pady=10)
        self.username_entry.pack(side=tk.LEFT, pady=10)

        password_frame = tk.Frame(register_frame, bg=cp['bg'])
        password_frame.pack(side=tk.TOP, expand=True)

        self.password_label = tk.Label(password_frame, text="Password", font=f['regular'], bg=cp['label'])
        self.password_entry = tk.Entry(password_frame, font=f['regular'], show="*", width=self.entry_width)
        self.password_label.pack(side=tk.LEFT, pady=10)
        self.password_entry.pack(side=tk.LEFT, pady=10)

        confirm_password_frame = tk.Frame(register_frame, bg=cp['bg'])
        confirm_password_frame.pack(side=tk.TOP, expand=True)

        self.confirm_password_label = tk.Label(confirm_password_frame, text="Confirm Password", font=f['regular'],
                                               bg=cp['label'])
        self.confirm_password_entry = tk.Entry(confirm_password_frame, font=f['regular'], show="*",
                                               width=self.entry_width)
        self.confirm_password_label.pack(side=tk.LEFT, pady=10)
        self.confirm_password_entry.pack(side=tk.LEFT, pady=10)

        register_button = tk.Button(register_frame, text="Register", font=f['regular'], bg=cp['button'],
                                    command=self.register_user)
        register_button.pack(side=tk.TOP, pady=10)

        footer_frame = tk.Frame(self, bg=cp['label'], border=3, relief=tk.SUNKEN)
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['label'])
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Back", font=f['regular'], bg=cp['button'], command=self.open_home)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.mainloop()

    def register_user(self):
        if self.password_entry.get() == self.confirm_password_entry.get():
            # TODO: Implement user registration (e.g. save to a database and log the user in)
            pass
        else:
            messagebox.showerror("Error", "Passwords do not match")

    def open_home(self):
        self.destroy()
        import home
        home.HomeGUI()

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == "__main__":
    RegisterGUI()
