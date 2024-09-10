import os
import sys
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from GUI.colour_palette import colours as cp
from src.workouts.legs.curl import LegCurlsApp
from GUI.fonts import Fonts
import GUI.workouts.utils as utils


class LegCurlsGUI(tk.Tk):
    is_resting = False

    def __init__(self):
        super().__init__()
        self.geometry("1280x480")
        self.title("Computer Vision Personal Trainer")
        self.resizable(False, False)

        f = Fonts().get_fonts()

        self.workout_token = utils.start_workout("Leg Curl")
        self.set_token = None

        # -Variables----------------------------------------------------------------------------------------------------
        self.border = 3

        self.left_var = tk.IntVar(value=0)
        self.right_var = tk.IntVar(value=0)
        self.weight = tk.IntVar(value=0)
        self.rest_time = tk.IntVar(value=0)
        self.left_stage = tk.StringVar(value="down")
        self.right_stage = tk.StringVar(value="down")

        # APPLICATION --------------------------------------------------------------------------------------------------
        self.app_frame = tk.Frame(self, bg=cp['inactive'], width=640, height=480)
        self.app_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # initialise the app here because it is referenced by side buttons, packed later
        self.app = LegCurlsApp(self.app_frame, (self.left_var, self.right_var),
                                    (self.left_stage, self.right_stage))
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

        self.stage_value_l = tk.Label(stage_val_frame, textvariable=str(self.left_stage), font=f['regular'],
                                      bg=cp['bg'])
        self.stage_value_r = tk.Label(stage_val_frame, textvariable=str(self.right_stage), font=f['regular'],
                                      bg=cp['bg'])
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
        title_label = tk.Label(gui_frame, text="Leg Curl", font=f['title'], bg=cp['label'])
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
                                command=lambda: utils.save_params(self))
        save_params.pack(anchor=tk.CENTER, pady=5)

        # RIGHT COLUMN FRAMES ------------------------------------------------------------------------------------------
        right_column.grid_columnconfigure(0, minsize=300)
        # -Instructions frame-------------------------------------------------------------------------------------------
        instructions_frame = tk.Frame(right_top, relief=tk.RAISED, border=self.border, bg=cp['bg'])
        instructions_frame.pack(anchor=tk.CENTER, fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(instructions_frame, bg=cp['bg'])
        self.image_label.pack(anchor=tk.CENTER)

        image_path = os.path.join(os.path.dirname(__file__), './assets/curl.png')
        utils.load_image(self, image_path)

        # -Start/Stop Set frame-----------------------------------------------------------------------------------------
        start_stop_frame = tk.Frame(right_bottom, bg=cp['bg'])
        start_stop_frame.pack(anchor=tk.CENTER, padx=10, pady=20, fill=tk.BOTH, expand=True)

        start_button = tk.Button(start_stop_frame, text="Start Set", font=f['regular'], bg=cp['button'],
                                 command=lambda: utils.start_set(self))
        end_button = tk.Button(start_stop_frame, text="End Set", font=f['regular'], bg=cp['button'],
                               command=lambda:utils.end_set(self))

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

        exit_button = tk.Button(buttons_frame, text="Exit", font=f['regular'], bg=cp['button'],
                                command=lambda :utils.on_closing(self, True))
        exit_button.pack(side=tk.RIGHT, padx=10)

        utils.add_message(self, "Welcome to the Leg Curl workout. Please set the weight and rest time before "
                                "starting a set. When the set is active, the background will turn green. You can start "
                                "and end a set using the buttons below. The rep stage and count will be displayed "
                                "above the camera feed as well as the side selector. The side can be set to left, "
                                "right, or both. The stage of the rep is displayed on the top right. The image on the "
                                "right shows the correct form for the exercise.")

        self.protocol("WM_DELETE_WINDOW", lambda: utils.on_closing(self, True))
        self.mainloop()

    def open_menu(self):
        if self.set_token:
            messagebox.showinfo("Error", "Please end the set before quitting.")
            return

        if messagebox.askyesno("Return", "Do you want to finish this workout?"):
            self.app.close()
            self.destroy()
            utils.end_workout(self.workout_token)
            from GUI.workouts.legs.legsGUI import LegsGUI
            LegsGUI()


if __name__ == "__main__":
    LegCurlsGUI()
