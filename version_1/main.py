import random
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DifferentialEquationSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Differential Equation Solver")

        # Load and display image
        image = Image.open("image.jpg")  # Replace "image.jpg" with your image file
        photo = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(root, image=photo)
        self.image_label.image = photo  # To prevent image from being garbage collected
        self.image_label.grid(row=0, column=0, columnspan=2)

        # Create input fields and labels in three rows
        inputs = [
            ("Alpha 1:", "Beta 1:"),
            ("Alpha 2:", "Beta 2:"),
            ("D 1:", "D 2:"),
        ]

        self.entries = []
        for i, (label1, label2) in enumerate(inputs):
            tk.Label(root, text=label1).grid(row=i + 1, column=0, sticky=tk.E)
            entry1 = tk.Entry(root)
            entry1.insert(0, "0")
            entry1.grid(row=i + 1, column=1)
            self.entries.append(entry1)

            tk.Label(root, text=label2).grid(row=i + 5, column=0, sticky=tk.E)
            entry2 = tk.Entry(root)
            entry2.insert(0, "0")
            entry2.grid(row=i + 5, column=1)
            self.entries.append(entry2)

        for i in range(1, 7):
            tk.Label(root, text=f"Tau {i}:").grid(row=i + 10, column=0, sticky=tk.E)
            entry = tk.Entry(root)
            entry.insert(0, str(random.randint(1, 11)))
            entry.grid(row=i + 10, column=1)
            self.entries.append(entry)

        # Additional inputs
        tk.Label(root, text="Beta 3:").grid(row=8, column=0, sticky=tk.E)
        self.b3_entry = tk.Entry(root)
        self.b3_entry.insert(0, "-3")
        self.b3_entry.grid(row=8, column=1)

        tk.Label(root, text="Beta 4:").grid(row=9, column=0, sticky=tk.E)
        self.b4_entry = tk.Entry(root)
        self.b4_entry.insert(0, "2")
        self.b4_entry.grid(row=9, column=1)

        tk.Label(root, text="D 3:").grid(row=10, column=0, sticky=tk.E)
        self.d3_entry = tk.Entry(root)
        self.d3_entry.insert(0, "0")
        self.d3_entry.grid(row=10, column=1)

        # Create buttons
        self.solve_button = tk.Button(root, text="Solve", command=self.solve_equation)
        self.solve_button.grid(row=18, column=0, columnspan=2)

        self.show_points_button = tk.Button(root, text="Show Points", command=self.show_points)
        self.show_points_button.grid(row=19, column=0, columnspan=2)

        # Create plot canvas
        self.figure, self.ax = plt.subplots(3, 1, figsize=(8, 7))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=18, padx=5, pady=5)

        # Create epsilon label
        self.epsilon_label = tk.Label(root, text="")
        self.epsilon_label.grid(row=20, column=0, columnspan=2)

    def solve_second_equation(self, a):
        # Get input values
        values = [float(entry.get()) for entry in self.entries]
        beta1 = values[1]
        beta2 = values[3]
        d2 = values[5]

        # Parameters for the differential equation
        e = np.e

        # Solve the differential equation du/dt = 1/e
        t = np.linspace(0, 10, 100)
        u = (1 / e) * t  # General solution to the differential equation

        # Use the condition beta1*u(t1) +beta2*u(t2) = d2 to find C
        t1 = values[8]  # Example value for t1
        t2 = values[9]  # Example value for t2
        C = (d2 - beta1 * ((2 * t1 + 2 * t1 * t1) / e) * - beta2 * ((2 * t2 + 2 * t2 * t2) / e) / (beta1 + beta2))

        # Update the solution u(t) with the constant C
        u = (1 / e) * t + a + C
        return u

    def solve_first_equation(self):
        # Get input values
        values = [float(entry.get()) for entry in self.entries]
        alpha1 = values[0]
        alpha2 = values[2]
        d1 = values[4]

        # Parameters for the differential equation
        e = np.e

        # Solve the differential equation da/dt = -a
        # The general solution to this equation is u(t) = Ce^(-t)

        # Use the condition alpha1*u(t1) + alpha2*u(t2) = d1 to find C
        t1 = values[6]  # Example value for t1
        t2 = values[7]  # Example value for t2

        # Formulate the system of equations to solve for C
        # alpha1 * C * e^(-t1) + alpha2 * C * e^(-t2) = d1
        A = np.array([[alpha1 * np.exp(-t1), alpha2 * np.exp(-t2)]])
        B = np.array([d1])

        # Solve for C
        C = np.linalg.lstsq(A, B, rcond=None)[0][0]

        # Calculate u(t) using the found C
        t = np.linspace(0, 10, 100)
        a = C * np.exp(-t)
        return a

    def solve_third_equation(self, a):
        # Get input values
        values = [float(entry.get()) for entry in self.entries]
        beta3 = float(self.b3_entry.get())
        beta4 = float(self.b4_entry.get())
        d3 = float(self.d3_entry.get())

        # Parameters for the differential equation
        e = np.e

        # Solve the differential equation da/dt = -a
        # The general solution to this equation is u(t) = Ce^(-t)

        # Use the condition alpha1*u(t1) + alpha2*u(t2) = d1 to find C
        t1 = values[10]  # Example value for t1
        t2 = values[11]  # Example value for t2

        # Formulate the system of equations to solve for C
        # alpha1 * C * e^(-t1) + alpha2 * C * e^(-t2) = d1
        A = np.array([[beta3, beta4]])
        B = np.array([d3 - beta3 * ((t1 + 2 * t1 * t1) / e) - beta4 * ((t2 + 2 * t2 * t2) / e)])

        # Solve for C
        C = np.linalg.lstsq(A, B, rcond=None)[0][0]

        # Calculate u(t) using the found C
        t = np.linspace(0, 10, 100)
        u = -3 * t ** 2 / (2 * e) + C + a
        return u

    def solve_equation(self):
        # Get input values
        values = [float(entry.get()) for entry in self.entries]
        beta3 = float(self.b3_entry.get())
        beta4 = float(self.b4_entry.get())

        # Solve the differential equation system
        t = np.linspace(0, 10, 100)
        y1 = self.solve_first_equation()
        y2 = self.solve_second_equation(y1)
        y3 = self.solve_third_equation(y1)
        y4 = y1 + np.cos(y2 - 2 * y3)
        y5 = self.solve_second_equation(y4)
        y6 = self.solve_third_equation(y4)

        # Plot the results
        self.ax[0].plot(t, y1)
        self.ax[0].plot(t, y4, ".")
        #self.ax[0].set_title('Plot of a and a\'')
        self.ax[0].set_xlabel('Time tau')
        self.ax[0].set_ylabel('a and a\'')

        self.ax[1].plot(t, y2)
        self.ax[1].plot(t, y5, ".")
        #self.ax[1].set_title('Plot of phi1 and phi1\'')
        self.ax[1].set_xlabel('Time tau')
        self.ax[1].set_ylabel('phi1 and phi1\'')

        self.ax[2].plot(t, y3)
        self.ax[2].plot(t, y6, ".")
        #self.ax[2].set_title('Plot of phi2 and phi2\'')
        self.ax[2].set_xlabel('Time tau')
        self.ax[2].set_ylabel('phi2 and phi2\'')
        self.canvas.draw()

        # Calculate epsilon
        epsilon = np.abs(y1 - y2).max()
        self.epsilon_label.config(text=f"Epsilon is {epsilon:.4f}")

    def show_points(self):
        # Get input values
        values = [float(entry.get()) for entry in self.entries]
        beta3 = float(self.b3_entry.get())
        beta4 = float(self.b4_entry.get())

        # Calculate points
        t = np.linspace(0, 10, 100)
        y1 = values[0] * np.exp(values[1] * t) + values[2]
        y2 = values[3] * np.exp(values[4] * t) + values[5]
        y3 = y1 + y2
        # Show points in a message box
        points = "\n".join(
            f"t={t_i:.2f}, y1={y1_i:.4f}, y2={y2_i:.4f}, y3={y3_i:.4f}" for t_i, y1_i, y2_i, y3_i in zip(t, y1, y2, y3))
        messagebox.showinfo("Points", points)


if __name__ == '__main__':
    root = tk.Tk()
    app = DifferentialEquationSolver(root)
    root.mainloop()
