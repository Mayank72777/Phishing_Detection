# src/base_window.py
import tkinter as tk

class BaseWindow:
    def __init__(self, root, title):
        if root is None:
            self.root = tk.Tk()
        else:
            self.root = root
        self.root.title(title)
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def show(self):
        self.root.deiconify()

    def hide(self):
        self.root.withdraw()

    def destroy(self):
        self.root.destroy()
