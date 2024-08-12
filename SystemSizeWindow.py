import tkinter as tk

from PointsNumberWindow import PointsNumberWindow


class SystemSizeWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Розмір системи")
        self.root.geometry(f"500x225")

        # Add a label for system size parameters
        labels_info = [
            (150, 25, 'Задайте параметри системи рівнянь'),
            (150, 50, 'da/dτ = X0(τ, a) + εX1(τ, a, φ),'),
            (150, 75, 'dφ/dτ = ω(τ, a)/ε + εY1(τ, a, φ).'),
            (150, 110, 'Кількість змінних a - '),
            (150, 135, 'Кількість змінних φ - '),
            (150, 160, 'Інтервал [L1,L2] - '),
        ]

        for x, y, text in labels_info:
            label = tk.Label(self.root, text=text, borderwidth=0, relief="solid")
            label.place(x=x, y=y)

        # Add the first input field with default value 2
        self.input_size_n = tk.Entry(self.root, width=10)
        self.input_size_n.insert(0, "2")
        self.input_size_n.place(x=280, y=110)

        # Add a label for 'm'
        self.input_size_m = tk.Entry(self.root, width=10)
        self.input_size_m.insert(0, "2")
        self.input_size_m.place(x=280, y=135)

        self.input_L1 = tk.Entry(self.root, width=10)
        self.input_L1.insert(0, "0")
        self.input_L1.place(x=280, y=160)

        self.input_L2 = tk.Entry(self.root, width=10)
        self.input_L2.insert(0, "1")
        self.input_L2.place(x=350, y=160)

        # Add a button that opens the new window
        self.button = tk.Button(self.root, text="Задати параметри", command=self.open_new_window)
        self.button.place(x=200, y=190)

    def open_new_window(self):
        n_size = int(self.input_size_n.get())
        m_size = int(self.input_size_m.get())
        l1 = int(self.input_L1.get())
        l2 = int(self.input_L2.get())

        self.root.destroy()
        new_root = tk.Tk()
        PointsNumberWindow(new_root, n_size, m_size, l1, l2)
