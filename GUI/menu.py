import tkinter as tk
from tkinter import messagebox


class MenuGUI:
    def __init__(self):
        self.win = tk.Tk()

        self.win.geometry("1280x960")
        self.win.title("Computer Vision Personal Trainer")

        label = tk.Label(self.win, text="Computer Vision Personal Trainer", font=("Arial", 24))
        label.pack()

        buttonframe = tk.Frame(self.win)
        buttonframe.columnconfigure(0, weight=1)
        buttonframe.columnconfigure(1, weight=1)
        buttonframe.columnconfigure(2, weight=1)

        btn1 = tk.Button(buttonframe, text="Arms", font=("Arial", 18), command=self.open_arms)
        btn1.grid(row=0, column=0, sticky="ew")
        btn2 = tk.Button(buttonframe, text="Back", font=("Arial", 18), command=self.open_back)
        btn2.grid(row=0, column=1, sticky="ew")
        btn3 = tk.Button(buttonframe, text="Cardio", font=("Arial", 18), command=self.open_cardio)
        btn3.grid(row=0, column=2, sticky="ew")

        btn4 = tk.Button(buttonframe, text="Chest", font=("Arial", 18), command=self.open_chest)
        btn4.grid(row=1, column=0, sticky="ew")
        btn5 = tk.Button(buttonframe, text="Legs", font=("Arial", 18), command=self.open_legs)
        btn5.grid(row=1, column=1, sticky="ew")
        btn6 = tk.Button(buttonframe, text="Shoulders", font=("Arial", 18), command=self.open_shoulders)
        btn6.grid(row=1, column=2, sticky="ew")
        
        buttonframe.pack(fill='x')
        
        # back button
        back_button = tk.Button(self.win, text="Back", font=("Arial", 18), command=self.open_home)
        back_button.pack(pady=10)
        
        # Exit button
        exit_button = tk.Button(self.win, text="Exit", font=("Arial", 18), command=self.on_closing)
        exit_button.pack(pady=10)
                
        # Run the main loop
        self.win.mainloop()
        
    def on_closing(self):
        if messagebox.askyesno("Quit", "Do you want to quit?"):
            self.win.destroy()
            
    def open_home(self):
        self.win.destroy()
        import home
        home.HomeGUI()
        
    def open_arms(self):
        self.win.destroy()
        from workouts.arms.armsGUI import ArmsGUI
        ArmsGUI()
        
    def open_back(self):
        self.win.destroy()
        from workouts.back.backGUI import BackGUI
        BackGUI()
        
    def open_cardio(self):
        self.win.destroy()
        from workouts.cardio.cardioGUI import CardioGUI
        CardioGUI()
        
    def open_chest(self):
        self.win.destroy()
        from workouts.chest.chestGUI import ChestGUI
        ChestGUI()
        
    def open_legs(self):
        self.win.destroy()
        from workouts.legs.legsGUI import LegsGUI
        LegsGUI()
        
    def open_shoulders(self):
        self.win.destroy()
        from workouts.shoulders.shouldersGUI import ShouldersGUI
        ShouldersGUI()


if __name__ == "__main__":
    MenuGUI()
    