import tkinter as tk
import random

from DifferentialEquationSystemWindow import DifferentialEquationSolver


class PointsNumberWindow:
    def __init__(self, root, n, m, l1, l2):
        self.root = root

        size_down = max(250, (n + m + 2) * 25 + 125)
        self.root.title("Розмір системи")
        self.root.geometry(f"500x{size_down}")
        self.n_size = n
        self.m_size = m
        self.L1 = l1
        self.L2 = l2

        # Add a label for system size parameters
        labels_info = [
            (50, 25, 'Задайте кількість точок для багаточкової умови кожного з рівнянь'),
            (50, 50, 'Σ α_i a(τ_i) = d1,'),
            (50, 75, 'Σ β_i φ(τ_i) = d2'),
        ]

        start_y = 125
        self.a_points_inputs = []
        for i in range(0, n):
            labels_info.append((50, start_y, f'Кількість точок в багаточоковій умові для визначення a{i + 1} - '))
            input_size_points_n = tk.Entry(self.root, width=10)
            input_size_points_n.insert(0, f"{random.randint(1, 4)}")
            input_size_points_n.place(x=380, y=start_y)
            self.a_points_inputs.append(input_size_points_n)
            start_y = start_y + 25

        self.phi_points_inputs = []
        for i in range(0, m):
            labels_info.append((50, start_y, f'Кількість точок в багаточоковій умові для визначення  φ{i + 1} - '))
            input_size_points_n = tk.Entry(self.root, width=10)
            input_size_points_n.insert(0, f"{random.randint(1, 4)}")
            input_size_points_n.place(x=380, y=start_y)
            self.phi_points_inputs.append(input_size_points_n)
            start_y = start_y + 25

        for x, y, text in labels_info:
            label = tk.Label(self.root, text=text, borderwidth=0, relief="solid")
            label.place(x=x, y=y)

        # Add a button that opens the new window
        self.button = tk.Button(self.root, text="Задати кількість точок", command=self.open_new_window)
        self.button.place(x=190, y=start_y)

    def open_new_window(self):
        a_points_size = []
        for entry in self.a_points_inputs:
            a_points_size.append(int(entry.get()))

        phi_points_size = []
        for entry in self.phi_points_inputs:
            phi_points_size.append(int(entry.get()))

        self.root.destroy()
        new_root = tk.Tk()
        DifferentialEquationSolver(new_root, self.n_size, a_points_size, self.m_size, phi_points_size, self.L1, self.L2)
