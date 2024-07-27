from tkinter import font


class Fonts:
    def __init__(self):
        self.fonts = {
            "title": font.Font(family="Arial", size=48),
            "regular": font.Font(family="Arial", size=15),
            "radio": font.Font(family="Arial", size=12)
        }

    def get_fonts(self):
        return self.fonts
