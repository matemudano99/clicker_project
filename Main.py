# main.py

import tkinter as tk
from GameController import GameController

if __name__ == "__main__":
    root = tk.Tk()
    app = GameController(root)
    root.mainloop()