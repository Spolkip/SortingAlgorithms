import tkinter as tk
from visualizer import SortingVisualizer

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()