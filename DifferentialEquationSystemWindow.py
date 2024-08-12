import tkinter as tk
import random

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Solver import Solver


# метод ньютона
# апроксимація в вузлах

class DifferentialEquationSolver:
    def __init__(self, root, n, points_n, m, points_m, l1, l2):
        self.root = root
        self.root.title("Differential Equation Solver")
        size_side_a = 50 + 2 * max(points_n) * 80 + 80
        size_side_phi = 50 + 2 * max(points_m) * 80 + 80
        geometry_size_x = max(720, size_side_a, size_side_phi)
        geometry_size_y = 50 + (n + m + 1) * 100
        self.root.geometry(f"{geometry_size_x}x{geometry_size_y}")
        self.a_size_n = n
        self.a_points_size_n = points_n
        self.phi_size_m = m
        self.phi_points_size_m = points_m
        self.X_entries = []
        self.Y_entries = []
        self.omega_entries = []
        self.alpha_entries = []
        self.a_tau_entries = []
        self.a_d_entries = []

        self.beta_entries = []
        self.phi_tau_entries = []
        self.phi_d_entries = []
        self.L1 = l1
        self.L2 = l2

        start_print_y = self.print_main_system()
        start_print_y = self.print_function_inputs(start_print_y)

        # Create and place canvas for the vertical line separator between conditions and view
        canvas = tk.Canvas(root, width=2, height=start_print_y, bg='white', highlightthickness=0)
        canvas.place(x=350, y=0)
        canvas.create_line(0, 0, 2, start_print_y, fill='black', width=2)

        start_print_y = self.print_points(start_print_y)

        # Create buttons
        self.solve_button = tk.Button(root, text="Розв'язати", command=self.solve_simplified_equations)
        self.solve_button.place(x=330, y=start_print_y)

        self.print_user_system()

    def solve_equation(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Графіки")

        # Define the number of plots in each row
        n = self.a_size_n  # Number of plots in the first row
        m = self.phi_size_m  # Number of plots in the second row

        width = f"{(n + m) * 220}x{(n + m) * 220}"
        new_window.geometry(width)

        # Create a figure with a specific size and DPI
        fig = Figure(figsize=(12, 6), dpi=100)

        # Create subplots in the first row
        for i in range(n):
            ax = fig.add_subplot(2, n, i + 1)  # 2 rows, n columns, i+1 is the subplot index
            ax.set_title(f'a{i + 1} plot')  # Set title for each subplot
            # Plot some data or customize each subplot as needed

            # Generate data for the plots
            t = np.linspace(0, 10, 400)
            a_averaged = np.exp(-random.randint(2, 17) * t) + np.cos(random.randint(1, 10) * t)
            a_real = a_averaged + random.randint(-10, 10) / 100

            self.save_data_to_file(f"solutions/a_{i}_solution", t, a_averaged, a_real)

            ax.plot(t, a_averaged)
            ax.plot(t, a_real)
            ax.set_title(f'$a{i + 1}$')
            ax.set_ylabel(f"a{i + 1}")
            ax.set_xlabel("τ")

        # Create subplots in the second row
        for j in range(m):
            ax = fig.add_subplot(2, m, n + j + 1)  # 2 rows, m columns, n+j+1 is the subplot index
            ax.set_title(f'φ{j + 1} plot')  # Set title for each subplot
            # Plot some data or customize each subplot as needed
            t = np.linspace(0, 10, 400)
            phi_averaged = random.randint(-1, 1) * t * t - random.randint(-3, 3) * t + 1 / (random.randint(1, 10)) * t
            phi_real = phi_averaged + random.randint(-15, 15) / 100

            self.save_data_to_file(f"solutions/phi_{j}solution", t, phi_averaged, phi_real)

            ax.plot(t, phi_averaged)
            ax.plot(t, phi_real)
            ax.set_title(f'$φ{j + 1}$')
            ax.set_ylabel(f"φ{j + 1}")
            ax.set_xlabel("τ")

        # Adjust layout
        fig.tight_layout()

        # Show the figure
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.solve_simplified_equations()

    def solve_simplified_equations(self):
        x0_vector = [entry.get() for i, entry in enumerate(self.X_entries) if
                     isinstance(entry.get(), str) and i % 2 == 0]
        x1_vector = [entry.get() for i, entry in enumerate(self.X_entries) if
                     isinstance(entry.get(), str) and i % 2 == 1]
        omega_vector = [entry.get() for entry in self.omega_entries if isinstance(entry.get(), str)]
        y_vector = [entry.get() for entry in self.omega_entries if isinstance(entry.get(), str)]

        a_d = [entry.get() for entry in self.a_d_entries if isinstance(entry.get(), str)]
        phi_d = [entry.get() for entry in self.phi_d_entries if isinstance(entry.get(), str)]

        counter = 0
        a_tau = []
        a_alpha = []
        for i in range(0, self.a_size_n):
            a_i = []
            a_alpha_i = []
            for j in range(0, self.a_points_size_n[i]):
                a_i.append(self.a_tau_entries[counter].get())
                a_alpha_i.append(self.alpha_entries[counter].get())
                counter = counter + 1
            a_tau.append(a_i)
            a_alpha.append(a_alpha_i)

        counter = 0
        phi_tau = []
        phi_beta = []
        for i in range(0, self.phi_size_m):
            phi_i = []
            phi_beta_i = []
            for j in range(0, self.phi_points_size_m[i]):
                phi_i.append(self.phi_tau_entries[counter].get())
                phi_beta_i.append(self.beta_entries[counter].get())
                counter = counter + 1
            phi_tau.append(phi_i)
            phi_beta.append(phi_beta_i)

        solver = Solver(x0_vector, x1_vector, omega_vector, y_vector, a_tau, a_alpha, a_d, phi_tau, phi_beta, phi_d, "0.01", self.L1, self.L2)
        solve_result = solver.solve()
        pass

    # Print systems and inputs

    def print_labels(self, labels_info):
        for x, y, text in labels_info:
            label = tk.Label(self.root, text=text, borderwidth=0, relief="solid")
            label.place(x=x, y=y)

    def print_user_system(self, *argc):

        labels_info = [(370, 25, 'Задана система рівнянь')]

        start_print_position_y = 50

        for i in range(0, len(self.X_entries), 2):
            equation_value = f"da{int(i / 2) + 1}/dτ ="
            if self.X_entries[i].get() != "" and self.X_entries[i].get() != "0":
                equation_value = equation_value + self.X_entries[i].get() \
                    .replace("phi1", "φ1").replace("phi2", "φ2").replace("tau", "τ")

            if self.X_entries[i + 1].get() != "" and self.X_entries[i + 1].get() != "0":
                equation_value = equation_value + " + ε( " + self.X_entries[i + 1].get() \
                    .replace("phi1", "φ1").replace("phi2", "φ2").replace("tau", "τ") + " )"

            labels_info.append((370, start_print_position_y, equation_value))
            start_print_position_y = start_print_position_y + 25

        for i in range(0, len(self.omega_entries)):
            equation_value = f"dφ{i + 1}/dτ ="
            if self.omega_entries[i].get() != "" and self.omega_entries[i].get() != "0":
                equation_value = equation_value + " ( " + self.omega_entries[i].get().replace("tau", "τ") + " )/ε"

            if self.Y_entries[i].get() != "" and self.Y_entries[i].get() != "0":
                equation_value = equation_value + " + ε( " + self.Y_entries[i].get() \
                    .replace("phi1", "φ1").replace("phi2", "φ2").replace("tau", "τ") + " )"

            labels_info.append((370, start_print_position_y, equation_value))

            start_print_position_y = start_print_position_y + 25

        labels_info.append((370, start_print_position_y, 'Із багатоточковими умовами'))
        start_print_position_y = start_print_position_y + 25

        alpha_entry_index = 0
        for i in range(0, self.a_size_n):
            condition = ""
            for j in range(0, self.a_points_size_n[i]):
                if (self.alpha_entries[alpha_entry_index].get() != "0"
                        and self.alpha_entries[alpha_entry_index].get() != ""):
                    condition = condition + self.alpha_entries[alpha_entry_index].get() + " * a( " + self.a_tau_entries[
                        alpha_entry_index].get() + " )"
                alpha_entry_index = alpha_entry_index + 1

            condition = condition + " = " + self.a_d_entries[i].get()
            labels_info.append((390, start_print_position_y, condition))
            start_print_position_y = start_print_position_y + 25

        beta_entry_index = 0
        for i in range(0, len(self.phi_d_entries)):
            condition = ""
            for j in range(0, self.phi_points_size_m[i]):
                if self.beta_entries[beta_entry_index].get() != "0" and self.beta_entries[beta_entry_index].get() != "":
                    condition = condition + self.beta_entries[beta_entry_index].get() + " * a( " + self.phi_tau_entries[
                        beta_entry_index].get() + " )"
                beta_entry_index = beta_entry_index + 1

            condition = condition + " = " + self.phi_d_entries[i].get()
            labels_info.append((390, start_print_position_y, condition))
            start_print_position_y = start_print_position_y + 25

        self.print_labels(labels_info)

    def print_main_system(self):
        labels_info = []

        all_a_concatted = ",".join([f"a{i}" for i in range(1, self.a_size_n + 1)])
        all_phi_concatted = ",".join([f"φ{i}" for i in range(1, self.phi_size_m + 1)])

        labels_info.append((50, 25, 'Введіть параметри для системи рівнянь'))

        start_print_x = 50

        for i in range(1, self.a_size_n + 1):
            labels_info.append((70, start_print_x,
                                f"da{i}/dτ = X0{i}(τ,{all_a_concatted}) "
                                f"+ εX{i}(τ,{all_a_concatted},{all_phi_concatted})"))
            start_print_x = start_print_x + 25

        for i in range(1, self.phi_size_m + 1):
            labels_info.append((70, start_print_x,
                                f"φ{i}/dτ = ω{i}(τ,{all_a_concatted})/ε"
                                f" + εY{i}(τ,{all_a_concatted},{all_phi_concatted})"))
            start_print_x = start_print_x + 25

        labels_info.append((50, start_print_x, 'Із багатоточковими умовами'), )
        start_print_x = start_print_x + 25

        alpha_index = 1
        for i in range(1, self.a_size_n + 1):
            label = ""
            for j in range(0, self.a_points_size_n[i - 1]):
                label = label + f"α{alpha_index}a{int(i)}"
                label = label + " + " if j != self.a_points_size_n[i - 1] - 1 else label
            label = label + f" = d{i}"
            labels_info.append((70, start_print_x, label))
            alpha_index = alpha_index + 1
            start_print_x = start_print_x + 25

        beta_index = 1
        for i in range(1, self.phi_size_m + 1):
            label = ""
            for j in range(0, self.phi_points_size_m[i - 1]):
                label = label + f"β{beta_index}φ{int(i)}"
                label = label + " + " if j != self.phi_points_size_m[i - 1] - 1 else label
                beta_index = beta_index + 1
            label = label + f" = d{i + self.a_size_n}"
            labels_info.append((70, start_print_x, label))
            start_print_x = start_print_x + 25
        self.print_labels(labels_info)
        return start_print_x + 25

    def print_function_inputs(self, start_position_y):
        labels_info = []
        all_a_concatted = ",".join([f"a{i}" for i in range(1, self.a_size_n + 1)])
        all_phi_concatted = ",".join([f"φ{i}" for i in range(1, self.phi_size_m + 1)])
        for i in range(1, self.a_size_n + 1):
            labels_info.append((50, start_position_y, f"X0{i}(τ,{all_a_concatted})="))
            labels_info.append((360, start_position_y, f"X{i}(τ,{all_a_concatted},{all_phi_concatted})="))

            entry_var_x0 = tk.StringVar()
            entry_var_x0.trace("w", self.print_user_system)

            entry_x0 = tk.Entry(self.root, width=20, textvariable=entry_var_x0)
            entry_x0.insert(0, f"-{i}*a{i}")
            entry_x0.place(x=50 + len(f"X0{i}(τ,{all_a_concatted})=") * 6, y=start_position_y)

            entry_var_x1 = tk.StringVar()
            entry_var_x1.trace("w", self.print_user_system)

            entry_x1 = tk.Entry(self.root, width=20, textvariable=entry_var_x1)
            entry_x1.insert(0, "cos(phi1-2phi2)")
            entry_x1.place(x=360 + len(f"X{i}(τ,{all_a_concatted},{all_phi_concatted})=") * 6, y=start_position_y)

            self.X_entries.append(entry_x0)
            self.X_entries.append(entry_x1)
            start_position_y = start_position_y + 25

        for i in range(1, self.phi_size_m + 1):
            labels_info.append((50, start_position_y, f"ω{i}(τ,{all_a_concatted})="))
            labels_info.append((360, start_position_y, f"Y{i}(τ,{all_a_concatted},{all_phi_concatted})="))

            entry_omega = tk.StringVar()
            entry_omega.trace("w", self.print_user_system)

            entry_omega = tk.Entry(self.root, width=20, textvariable=entry_omega)
            entry_omega.insert(0, f"2+4tau")
            entry_omega.place(x=50 + len(f"ω{i}(τ,{all_a_concatted})=") * 6, y=start_position_y)

            entry_var_y1 = tk.StringVar()
            entry_var_y1.trace("w", self.print_user_system)

            entry_y1 = tk.Entry(self.root, width=20, textvariable=entry_var_y1)
            entry_y1.insert(0, f"{i + 2}a1")
            entry_y1.place(x=360 + len(f"Y{i}(τ,{all_a_concatted},{all_phi_concatted})=") * 6, y=start_position_y)

            self.omega_entries.append(entry_omega)
            self.Y_entries.append(entry_y1)
            start_position_y = start_position_y + 25

        self.print_labels(labels_info)
        return start_position_y

    def print_points(self, start_position_y):
        labels_info = []

        # print all a labels and points
        alpha_index = 1
        for i in range(0, self.a_size_n):
            tmp_alpha_index = alpha_index
            for j in range(0, self.a_points_size_n[i]):
                labels_info.append((50 + j * 80, start_position_y + 25 * i, f"α{tmp_alpha_index}="))

                entry_alpha = tk.StringVar()
                entry_alpha.trace("w", self.print_user_system)

                alpha_entry = tk.Entry(self.root, width=5, textvariable=entry_alpha)
                alpha_entry.insert(0, f"{random.randint(-3, 3)}")
                alpha_entry.place(x=75 + j * 80, y=start_position_y + 25 * i)
                tmp_alpha_index = tmp_alpha_index + 1
                self.alpha_entries.append(alpha_entry)

            for j in range(0, self.a_points_size_n[i]):
                labels_info.append(
                    (50 + (j + self.a_points_size_n[i]) * 80, start_position_y + 25 * i, f"τ{alpha_index}="))

                entry_tau = tk.StringVar()
                entry_tau.trace("w", self.print_user_system)

                tau_entry = tk.Entry(self.root, width=5, textvariable=entry_tau)
                tau_entry.insert(0, f"{random.randint(0, 10)}")
                tau_entry.place(x=75 + (j + self.a_points_size_n[i]) * 80, y=start_position_y + 25 * i)
                alpha_index = alpha_index + 1
                self.a_tau_entries.append(tau_entry)

            labels_info.append(
                (50 + 2 * self.a_points_size_n[i] * 80, start_position_y + 25 * i, f"d{i + 1}="))

            entry_d = tk.StringVar()
            entry_d.trace("w", self.print_user_system)

            d_entry = tk.Entry(self.root, width=5, textvariable=entry_d)
            d_entry.insert(0, f"{random.randint(-10, 10)}")
            d_entry.place(x=75 + 2 * self.a_points_size_n[i] * 80, y=start_position_y + 25 * i)

            self.a_d_entries.append(d_entry)
            self.print_labels(labels_info)

        start_position_y = start_position_y + 25 * self.a_size_n

        beta_index = 1
        phi_tau_index = alpha_index
        for i in range(0, self.phi_size_m):
            for j in range(0, self.phi_points_size_m[i]):
                labels_info.append((50 + j * 80, start_position_y + 25 * i, f"β{beta_index}="))

                entry_beta = tk.StringVar()
                entry_beta.trace("w", self.print_user_system)

                beta_entry = tk.Entry(self.root, width=5, textvariable=entry_beta)
                beta_entry.insert(0, f"{random.randint(-3, 3)}")
                beta_entry.place(x=75 + j * 80, y=start_position_y + 25 * i)
                beta_index = beta_index + 1
                self.beta_entries.append(beta_entry)

            for j in range(0, self.phi_points_size_m[i]):
                labels_info.append((50 + j * 80 + self.phi_points_size_m[i] * 80, start_position_y + 25 * i,
                                    f"τ{phi_tau_index}="))

                entry_tau = tk.StringVar()
                entry_tau.trace("w", self.print_user_system)

                tau_entry = tk.Entry(self.root, width=5, textvariable=entry_tau)
                tau_entry.insert(0, f"{random.randint(0, 10)}")
                tau_entry.place(x=75 + j * 80 + self.phi_points_size_m[i] * 80, y=start_position_y + 25 * i)
                phi_tau_index = phi_tau_index + 1
                self.phi_tau_entries.append(tau_entry)

            labels_info.append(
                (50 + 2 * self.phi_points_size_m[i] * 80, start_position_y + 25 * i,
                 f"d{i + self.a_size_n + 1}="))

            entry_d = tk.StringVar()
            entry_d.trace("w", self.print_user_system)

            d_entry = tk.Entry(self.root, width=5, textvariable=entry_d)
            d_entry.insert(0, f"{random.randint(-10, 10)}")
            d_entry.place(x=75 + 2 * self.phi_points_size_m[i] * 80, y=start_position_y + 25 * i)

            self.phi_d_entries.append(d_entry)
            self.print_labels(labels_info)

        return start_position_y + 25 * self.phi_size_m

    def save_data_to_file(self, filename, x, y_averaged, y):
        with open(filename, 'w') as file:
            file.write("tau, avaraged solution, real solution\n")  # Write header
            for xi, y_averaged, yi in zip(x, y_averaged, y):
                file.write(f"{xi:.2f} | {y_averaged:.2f} | {yi:.2f}\n")  # Write data points
