import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from GUI.colour_palette import colours as cp
from src.workouts.arms.tricep_pushdown import TricepPushdownApp
from GUI.fonts import Fonts
import GUI.workouts.utils as utils


class TricepPushdownGUI(tk.Tk):
    is_resting = False
    set_weights = []
    set_reps = []
    max_weight = 0
    volume = 0

    def __init__(self):
        super().__init__()
        self.geometry("1280x480")
        self.title("Computer Vision Personal Trainer")

        f = Fonts().get_fonts()

        self.workout_token = utils.start_workout("Tricep Pushdown")

        # -Variables----------------------------------------------------------------------------------------------------

        self.border = 3

        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)
        self.weight = tk.IntVar(value=0)
        self.rest_time = tk.IntVar(value=0)

        # -Application--------------------------------------------------------------------------------------------------

        self.app = TricepPushdownApp(self, (self.left_var, self.right_var))
        self.app.pack(side=tk.LEFT)

        # --------------------------------------------------------------------------------------------------------------
        # MENU LAYOUT---------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # Title frame
        title_frame = tk.Frame(self)
        self.title = tk.Label(title_frame, text="Tricep Pushdown", font=f['title'], bg=cp['label'])
        self.title.pack(fill=tk.BOTH)
        title_frame.pack(fill=tk.BOTH)

        # Main frame for columns
        main_frame = tk.Frame(self, border=self.border, relief=tk.RAISED, bg=cp['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --------------------------------------------------------------------------------------------------------------
        # COLUMN LAYOUT FOR MAIN FRAME----------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # -Left column--------------------------------------------------------------------------------------------------

        left_column = tk.Frame(main_frame, border=self.border, relief=tk.RAISED, bg=cp['bg'])
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        left_middle = tk.Frame(left_column, border=self.border, relief=tk.RAISED, width=213, bg=cp['bg'])
        left_bottom = tk.Frame(left_column, border=self.border, relief=tk.FLAT, width=213, bg=cp['bg'])
        left_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        left_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # -Middle column------------------------------------------------------------------------------------------------

        middle_column = tk.Frame(main_frame, border=self.border, bg=cp['bg'])
        middle_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Split middle column into two rows
        middle_top = tk.Frame(middle_column, border=self.border, width=214, bg=cp['bg'])
        middle_bottom = tk.Frame(middle_column, border=self.border, width=214, bg=cp['bg'])
        middle_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        middle_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # -Right column-------------------------------------------------------------------------------------------------

        right_column = tk.Frame(main_frame, border=self.border, relief=tk.RAISED, bg=cp['bg'])
        right_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Split right column into two rows
        right_top = tk.Frame(right_column, border=self.border, relief=tk.FLAT, width=213, bg=cp['bg'])
        right_bottom = tk.Frame(right_column, border=self.border, relief=tk.RAISED, width=213, bg=cp['bg'])
        right_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        right_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # --------------------------------------------------------------------------------------------------------------
        # FRAMES FOR LEFT COLUMN----------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # -Parameters frame---------------------------------------------------------------------------------------------

        workout_frame = tk.Frame(left_middle, bg=cp['bg'])
        workout_frame.pack(anchor=tk.CENTER, expand=True)
        weight_frame = tk.Frame(workout_frame, bg=cp['bg'])
        rest_frame = tk.Frame(workout_frame, bg=cp['bg'])
        weight_frame.pack(anchor=tk.CENTER)
        rest_frame.pack(anchor=tk.CENTER)

        self.weight_label = tk.Label(weight_frame, text="Weight(kg): ", font=f['regular'], bg=cp['bg'])
        self.weight_entry = tk.Entry(weight_frame, font=f['regular'], width=5)
        self.weight_label.pack(side=tk.LEFT)
        self.weight_entry.pack(side=tk.LEFT)

        self.rest_label = tk.Label(rest_frame, text="Rest(sec): ", font=f['regular'], bg=cp['bg'])
        self.rest_entry = tk.Entry(rest_frame, font=f['regular'], width=5)
        self.rest_label.pack(side=tk.LEFT)
        self.rest_entry.pack(side=tk.LEFT)

        self.save_params = tk.Button(workout_frame, text='Save', font=f['regular'], bg=cp['button'],
                                     command=self.save_params)
        self.save_params.pack(anchor=tk.CENTER, pady=10)

        set_weight_frame = tk.Frame(workout_frame, bg=cp['bg'])
        set_weight_frame.pack(anchor=tk.CENTER)
        set_rest_frame = tk.Frame(workout_frame, bg=cp['bg'])
        set_rest_frame.pack(anchor=tk.CENTER)

        self.set_weight_label = tk.Label(set_weight_frame, text="Set Weight: ", font=f['regular'], bg=cp['bg'])
        self.set_weight_value = tk.Label(set_weight_frame, textvariable=self.weight, font=f['regular'], bg=cp['bg'])
        self.set_rest_label = tk.Label(set_rest_frame, text="Set Rest Time: ", font=f['regular'], bg=cp['bg'])
        self.set_rest_value = tk.Label(set_rest_frame, textvariable=self.rest_time, font=f['regular'], bg=cp['bg'])

        self.set_weight_label.pack(side=tk.LEFT)
        self.set_weight_value.pack(side=tk.LEFT)
        self.set_rest_label.pack(side=tk.LEFT)
        self.set_rest_value.pack(side=tk.LEFT)

        # -Next set frame-----------------------------------------------------------------------------------------------

        next_frame = tk.Frame(left_bottom, bg=cp['bg'])
        next_frame.pack(anchor=tk.CENTER, expand=True)
        next_set_frame = tk.Frame(next_frame, bg=cp['bg'])
        next_set_frame.pack(anchor=tk.CENTER)

        self.rest_timer_label = tk.Label(next_set_frame, text="Rest Timer: ", font=f['regular'], bg=cp['bg'])
        self.rest_timer_value = tk.Label(next_set_frame, text="", font=f['regular'], bg=cp['bg'])
        self.next_set_button = tk.Button(next_frame, text='Next Set', font=f['regular'], bg=cp['button'],
                                         command=self.next_set)

        self.rest_timer_label.pack(side=tk.LEFT)
        self.rest_timer_value.pack(side=tk.LEFT)
        self.next_set_button.pack(pady=10)

        # --------------------------------------------------------------------------------------------------------------
        # FRAMES FOR MIDDLE COLUMN--------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # -Message frame------------------------------------------------------------------------------------------------

        message_frame = tk.Frame(middle_top, bg=cp['bg'])
        message_frame.pack(anchor=tk.CENTER, expand=True)

        self.message_label = tk.Label(message_frame, text="", font=f['regular'], bg=cp['label'])
        self.message_label.pack(anchor=tk.CENTER)

        # -Image frame--------------------------------------------------------------------------------------------------

        image_frame = tk.Frame(middle_bottom, bg=cp['bg'])
        image_frame.pack(anchor=tk.S, expand=True)

        self.image_label = tk.Label(image_frame, bg=cp['bg'])
        self.image_label.pack(anchor=tk.S)

        image_path = os.path.join(os.path.dirname(__file__), './assets/tricep_pushdown.png')
        utils.load_image(self, image_path)

        # --------------------------------------------------------------------------------------------------------------
        # FRAMES FOR RIGHT COLUMN---------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        # -Reps frame---------------------------------------------------------------------------------------------------

        reps_frame = tk.Frame(right_top, bg=cp['bg'])
        reps_frame.pack(anchor=tk.CENTER, expand=True)

        left_frame = tk.Frame(reps_frame, bg=cp['bg'])
        right_frame = tk.Frame(reps_frame, bg=cp['bg'])

        self.left_label = tk.Label(left_frame, text="Left reps: ", font=f['regular'], bg=cp['bg'])
        self.rep_count_l = tk.Label(left_frame, textvariable=self.left_var, font=f['regular'], bg=cp['bg'])
        self.left_label.pack(side=tk.LEFT)
        self.rep_count_l.pack(side=tk.LEFT)

        self.right_label = tk.Label(right_frame, text="Right reps: ", font=f['regular'], bg=cp['bg'])
        self.rep_count_r = tk.Label(right_frame, textvariable=self.right_var, font=f['regular'], bg=cp['bg'])
        self.right_label.pack(side=tk.LEFT)
        self.rep_count_r.pack(side=tk.LEFT)

        left_frame.pack()
        right_frame.pack()

        # -Buttons frame------------------------------------------------------------------------------------------------

        button_frame = tk.Frame(right_bottom, bg=cp['bg'])
        button_frame.pack(anchor=tk.CENTER, expand=True)

        self.save_button = tk.Button(button_frame, text='Save', font=f['regular'], bg=cp['button'],
                                     command=self.app.save_workout)
        self.back_button = tk.Button(button_frame, text='Return', font=f['regular'], bg=cp['button'],
                                     command=self.open_menu)
        self.exit_button = tk.Button(button_frame, text='Exit', font=f['regular'], bg=cp['button'],
                                     command=self.on_closing)

        self.save_button.pack(side=tk.TOP, padx=10, pady=10)
        self.back_button.pack(side=tk.TOP, padx=10, pady=10)
        self.exit_button.pack(side=tk.TOP, padx=10, pady=10)

        # --------------------------------------------------------------------------------------------------------------
        # MAIN LOOP-----------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def next_set(self):
        print("Next set")
        if self.rest_time.get() == 0:
            print("Rest time not set")
            # TODO: show message in middle top frame
            return
        self.is_resting = True
        self.update_timer()

        self.set_weights.append(self.weight.get())
        self.set_reps.append((self.left_var.get(), self.right_var.get()))
        self.left_var.set(0)
        self.right_var.set(0)

    def save_params(self):
        print("Save params")
        self.weight.set(int(self.weight_entry.get()))
        self.rest_time.set(int(self.rest_entry.get()))
        self.set_weight_value.config(text=self.weight.get())
        self.set_rest_value.config(text=self.rest_time)
        self.weight_entry.delete(0, tk.END)
        self.rest_entry.delete(0, tk.END)

    def update_timer(self):
        print("Updating timer")
        if self.rest_time.get() > 0:
            mins, secs = divmod(self.rest_time.get(), 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.rest_timer_value.config(text=time_format)
            self.rest_time.set(self.rest_time.get() - 1)
            self.after(1000, self.update_timer)
        else:
            self.rest_timer_value.config(text="Go!")
            self.is_resting = False

    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.destroy()

            utils.save_set(self)  # save the last set
            utils.end_workout(self.workout_token, self.set_reps, self.set_weights)
            from src.db.login_session import logout
            logout()

    def open_menu(self):
        if messagebox.askyesno("Return", "Do you want to finish this workout?"):
            self.app.close()
            self.destroy()
            utils.save_set(self)  # save the last set
            utils.end_workout(self.workout_token, self.set_reps, self.set_weights)
            from GUI.workouts.arms.armsGUI import ArmsGUI
            ArmsGUI()


if __name__ == "__main__":
    TricepPushdownGUI()
