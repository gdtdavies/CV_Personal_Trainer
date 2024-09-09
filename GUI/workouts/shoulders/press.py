import os
import sys
import tkinter as tk
import uuid
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from GUI.colour_palette import colours as cp
from src.workouts.shoulders.press import ShoulderPressApp
from GUI.fonts import Fonts
import GUI.workouts.utils as utils


class ShoulderPressGUI(tk.Tk):
    is_resting = False
    set_weights = []
    set_reps = []
    max_weight = 0
    volume = 0

    def __init__(self):
        super().__init__()
        self.geometry("1280x480")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        self.workout_token = utils.start_workout("Shoulder Press")
        self.set_token = None

        # -Variables----------------------------------------------------------------------------------------------------
        self.border = 3

        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)
        self.weight = tk.IntVar(value=0)
        self.rest_time = tk.IntVar(value=0)

        # APPLICATION --------------------------------------------------------------------------------------------------
        self.app_frame = tk.Frame(self, bg=cp['inactive'], width=640, height=480)
        self.app_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # initialise the ShoulderPressApp here because it is referenced by side buttons, packed later
        self.app = ShoulderPressApp(self.app_frame, (self.left_var, self.right_var))
        self.app.config(height=40, width=40)

        info_frame = tk.Frame(self.app_frame, bg=cp['bg'], height=80, relief=tk.RAISED, border=self.border)
        info_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # -Stage frame--------------------------------------------------------------------------------------------------
        stage_frame = tk.Frame(info_frame, bg=cp['bg'])
        stage_frame.pack(side=tk.LEFT, anchor=tk.W, fill=tk.BOTH, expand=True)

        stage_label = tk.Label(stage_frame, text="Stage: ", font=f['regular'], bg=cp['bg'])
        stage_label.pack(side=tk.LEFT)

        stage_label_frame = tk.Frame(stage_frame, bg=cp['bg'])
        stage_label_frame.pack(side=tk.LEFT)

        stage_label_l = tk.Label(stage_label_frame, text="L: ", font=f['regular'], bg=cp['bg'])
        stage_label_r = tk.Label(stage_label_frame, text="R: ", font=f['regular'], bg=cp['bg'])
        stage_label_l.pack(side=tk.TOP)
        stage_label_r.pack(side=tk.TOP)

        stage_val_frame = tk.Frame(stage_frame, bg=cp['bg'])
        stage_val_frame.pack(side=tk.LEFT)

        self.stage_value_l = tk.Label(stage_val_frame, text="Down", font=f['regular'], bg=cp['bg'])
        self.stage_value_r = tk.Label(stage_val_frame, text="Down", font=f['regular'], bg=cp['bg'])
        self.stage_value_l.pack(side=tk.TOP)
        self.stage_value_r.pack(side=tk.TOP)

        # -Side frame---------------------------------------------------------------------------------------------------
        side_frame = tk.Frame(info_frame, bg=cp['bg'])
        side_frame.pack(side=tk.LEFT)

        self.lr_var = tk.StringVar(value="both")

        side_label = tk.Label(side_frame, text="Side ", font=f['regular'], bg=cp['bg'])
        side_label.pack(side=tk.TOP)

        self.left_button = tk.Radiobutton(
            side_frame, text="Left", font=f['radio'], variable=self.lr_var, value="left",
            command=self.app.left_side, bg=cp['button'])
        self.right_button = tk.Radiobutton(
            side_frame, text="Right", font=f['radio'], variable=self.lr_var, value="right",
            command=self.app.right_side, bg=cp['button'])
        self.both_button = tk.Radiobutton(
            side_frame, text="Both", font=f['radio'], variable=self.lr_var, value="both",
            command=self.app.both_sides, bg=cp['button'])

        self.left_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.both_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # -Reps frame---------------------------------------------------------------------------------------------------
        reps_frame = tk.Frame(info_frame, bg=cp['bg'])
        reps_frame.pack(side=tk.LEFT, anchor=tk.E, expand=True)

        reps_label_frame = tk.Frame(reps_frame, bg=cp['bg'])
        reps_label = tk.Label(reps_label_frame, text="Rep count: ", font=f['regular'], bg=cp['bg'])
        reps_label.pack(anchor=tk.CENTER)
        reps_label_frame.pack(side=tk.LEFT)

        reps_count_frame = tk.Frame(reps_frame, bg=cp['bg'])
        left_frame = tk.Frame(reps_count_frame, bg=cp['bg'])
        right_frame = tk.Frame(reps_count_frame, bg=cp['bg'])

        self.left_label = tk.Label(left_frame, text="L: ", font=f['regular'], bg=cp['bg'])
        self.rep_count_l = tk.Label(left_frame, textvariable=self.left_var, font=f['regular'], bg=cp['bg'])
        self.left_label.pack(side=tk.LEFT)
        self.rep_count_l.pack(side=tk.LEFT)

        self.right_label = tk.Label(right_frame, text="R: ", font=f['regular'], bg=cp['bg'])
        self.rep_count_r = tk.Label(right_frame, textvariable=self.right_var, font=f['regular'], bg=cp['bg'])
        self.right_label.pack(side=tk.LEFT)
        self.rep_count_r.pack(side=tk.LEFT)

        left_frame.pack()
        right_frame.pack()
        reps_count_frame.pack(side=tk.LEFT)

        # packing the app from earlier
        self.app.pack(side=tk.TOP)

        # -GUI----------------------------------------------------------------------------------------------------------
        gui_frame = tk.Frame(self, bg=cp['bg'], width=640, height=480)
        gui_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title frame --------------------------------------------------------------------------------------------------
        title_label = tk.Label(gui_frame, text="Shoulder Press", font=f['title'], bg=cp['label'])
        title_label.pack(fill=tk.BOTH)

        # Main frame ---------------------------------------------------------------------------------------------------
        main_frame = tk.Frame(gui_frame, border=self.border, relief=tk.RAISED, bg=cp['bg'], height=380)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # COLUMN LAYOUT ------------------------------------------------------------------------------------------------

        # -Left column--------------------------------------------------------------------------------------------------
        left_column = tk.Frame(main_frame, border=self.border, relief=tk.RAISED, bg=cp['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        left_top = tk.Frame(left_column, border=self.border, relief=tk.FLAT, bg=cp['bg'])
        left_bottom = tk.Frame(left_column, border=self.border, relief=tk.FLAT, bg=cp['bg'])
        left_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        left_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # -Right column-------------------------------------------------------------------------------------------------
        right_column = tk.Frame(main_frame, border=self.border, relief=tk.RAISED, bg=cp['bg'])
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_top = tk.Frame(right_column, border=self.border, relief=tk.FLAT, bg=cp['bg'])
        right_bottom = tk.Frame(right_column, border=self.border, relief=tk.FLAT, bg=cp['bg'])
        right_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        right_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # LEFT COLUMN FRAMES -------------------------------------------------------------------------------------------
        left_column.grid_columnconfigure(0, minsize=340)
        # -Message frame------------------------------------------------------------------------------------------------
        message_frame = tk.Frame(left_top, bg=cp['bg'], width=300, height=200)
        message_frame.pack_propagate(False)  # Prevent the frame from resizing
        message_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(message_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget
        self.chat_text = tk.Text(message_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, font=f['radio'],
                                 bg=cp['bg'])
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chat_text.config(state=tk.DISABLED)

        # Configure scrollbar
        scrollbar.config(command=self.chat_text.yview)

        # -Parameters frame---------------------------------------------------------------------------------------------
        workout_frame = tk.Frame(left_bottom, bg=cp['bg'])
        workout_frame.pack(anchor=tk.CENTER, expand=True)
        weight_frame = tk.Frame(workout_frame, bg=cp['bg'])
        rest_frame = tk.Frame(workout_frame, bg=cp['bg'])
        weight_frame.pack(anchor=tk.CENTER)
        rest_frame.pack(anchor=tk.CENTER)

        weight_label = tk.Label(weight_frame, text="Weight(kg): ", font=f['regular'], bg=cp['bg'])
        self.weight_entry = tk.Entry(weight_frame, font=f['regular'], width=5)
        weight_label.pack(side=tk.LEFT)
        self.weight_entry.pack(side=tk.LEFT)

        rest_label = tk.Label(rest_frame, text="Rest(sec):  ", font=f['regular'], bg=cp['bg'])
        self.rest_entry = tk.Entry(rest_frame, font=f['regular'], width=5)
        rest_label.pack(side=tk.LEFT)
        self.rest_entry.pack(side=tk.LEFT)

        save_params = tk.Button(workout_frame, text='Save', font=f['regular'], bg=cp['button'],
                                command=self.save_params)
        save_params.pack(anchor=tk.CENTER, pady=5)

        # RIGHT COLUMN FRAMES ------------------------------------------------------------------------------------------
        right_column.grid_columnconfigure(0, minsize=300)
        # -Instructions frame-------------------------------------------------------------------------------------------
        instructions_frame = tk.Frame(right_top, relief=tk.RAISED, border=self.border, bg=cp['bg'])
        instructions_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(instructions_frame, bg=cp['bg'])
        self.image_label.pack(anchor=tk.CENTER)

        image_path = os.path.join(os.path.dirname(__file__), './assets/shoulder_press.png')
        utils.load_image(self, image_path)

        # -Start/Stop Set frame-----------------------------------------------------------------------------------------
        start_stop_frame = tk.Frame(right_bottom, bg=cp['bg'])
        start_stop_frame.pack(anchor=tk.CENTER, padx=10, pady=20, fill=tk.BOTH, expand=True)

        start_button = tk.Button(start_stop_frame, text="Start Set", font=f['regular'], bg=cp['button'],
                                 command=self.start_set)
        end_button = tk.Button(start_stop_frame, text="End Set", font=f['regular'], bg=cp['button'],
                               command=self.end_set)

        start_button.pack(side=tk.LEFT, anchor=tk.CENTER, fill=tk.BOTH, expand=True, padx=2)
        end_button.pack(side=tk.LEFT, anchor=tk.CENTER, fill=tk.BOTH, expand=True, padx=2)

        # Footer frame -------------------------------------------------------------------------------------------------
        footer_frame = tk.Frame(gui_frame, height=80, bg=cp['label'], relief=tk.SUNKEN, border=self.border)
        footer_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

        buttons_frame = tk.Frame(footer_frame, bg=cp['bg'], border=3, relief=tk.RAISED, padx=10, pady=10)
        buttons_frame.pack(anchor=tk.CENTER, expand=True)

        back_button = tk.Button(buttons_frame, text="Return", font=f['regular'], bg=cp['button'],
                                command=self.open_menu)
        back_button.pack(side=tk.LEFT, padx=10)

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'], command=self.on_closing)
        exit_button.pack(side=tk.RIGHT, padx=10)

        self.add_message("Welcome to the Shoulder Press workout. Please set the weight and rest time before starting a "
                         "set. When the set is active, the background will turn green. You can start and end a set "
                         "using the buttons below. The rep stage and count will be displayed above the camera feed "
                         "as well as the side selector. The side can be set to left, right, or both. The stage of the "
                         "rep is displayed on the top right. The image on the right shows the correct form for the "
                         "exercise.")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def add_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.insert(tk.END, "-------------------------------\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.yview(tk.END)

    def start_set(self):
        w = self.weight.get()
        r = self.rest_time.get()

        if w == 0 or r == 0:
            self.add_message("Please set weight and rest time before starting a set.")
            return
        if self.set_token:
            self.add_message("Set already active")
            return
        if self.is_resting:
            self.add_message("Rest timer is active, please wait.")
            return

        self.add_message(f"Starting set with weight: {str(w)}kg")
        self.app.toggle_active()
        self.app_frame.config(bg=cp['active'])

        from src.db.db_connection import DBConnection
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        self.set_token = str(uuid.uuid4())
        query = "SELECT * FROM cv_pt.public.start_set(%s, %s)"
        cursor.execute(query, (self.set_token, self.workout_token))
        conn.commit()

        db.close()

    def end_set(self):
        if not self.set_token:
            self.add_message("no set active")
            return
        self.add_message("Ending set")
        self.app.toggle_active()
        self.app_frame.config(bg=cp['inactive'])

        from src.db.db_connection import DBConnection
        db = DBConnection()
        conn = db.connect()
        cursor = conn.cursor()

        reps = self.left_var.get() if self.left_var.get() > self.right_var.get() else self.right_var.get()

        query = "SELECT * FROM cv_pt.public.end_set(%s, %s, %s)"
        cursor.execute(query, (self.set_token, reps, self.weight.get()))
        conn.commit()

        self.set_token = None

        db.close()

        self.rest_timer(self.rest_time.get())


    def save_params(self):
        print("Save params")
        w = self.weight_entry.get()
        r = self.rest_entry.get()

        if not w or not r:
            self.add_message("Please enter a weight and rest time.")
            return

        self.weight.set(int(w))
        self.rest_time.set(int(r))
        self.weight_entry.delete(0, tk.END)
        self.rest_entry.delete(0, tk.END)

        self.add_message(f"Set weight to {self.weight.get()}kg and rest time to {self.rest_time.get()}s.")


    def rest_timer(self, time_left):
        self.is_resting = True
        if time_left > 0:
            self.add_message(f"Rest time left: {time_left} seconds")
            self.after(1000, self.rest_timer, time_left - 1)
        else:
            self.add_message("Rest time over")
            self.is_resting = False


    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            utils.save_set(self)  # Save the last set
            utils.end_workout(self.workout_token, self.set_reps, self.set_weights)
            from src.db.login_session import logout
            logout()

            self.destroy()

    def open_menu(self):
        if messagebox.askyesno("Return", "Do you want to finish this workout?"):
            self.app.close()
            self.destroy()
            utils.save_set(self)  # save the last set
            utils.end_workout(self.workout_token, self.set_reps, self.set_weights)
            from GUI.workouts.arms.armsGUI import ArmsGUI
            ArmsGUI()


if __name__ == "__main__":
    ShoulderPressGUI()
