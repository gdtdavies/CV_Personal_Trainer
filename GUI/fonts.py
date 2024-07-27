from tkinter import font


class Fonts:
    def __init__(self):
        self.fonts = {
            "title": font.Font(family="American Stencil", size=48),
            "regular": font.Font(family="Unispace", size=12),
            "radio": font.Font(family="Unispace", size=10)
        }

    def get_fonts(self):
        return self.fonts
