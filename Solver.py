import math

import sympy as sp
from scipy.optimize import fsolve

import re


class Solver:
    def __init__(self, x0_vector, x1_vector, omega_vector, y_vector, a_tau, a_alpha, a_d, phi_tau, phi_beta, phi_d,
                 epsilon, l1, l2):
        self.x0_vector = x0_vector
        self.x1_vector = x1_vector
        self.omega_vector = omega_vector
        self.y_vector = y_vector
        self.a_tau = a_tau
        self.a_alpha = a_alpha
        self.a_d = a_d
        self.phi_tau = phi_tau
        self.phi_beta = phi_beta
        self.phi_d = phi_d
        self.epsilon = epsilon
        self.L1 = l1
        self.L2 = l2
        pass

    def solve(self):
        return self.solve_simplified_system()

    '''
        For system da/dt = f(a,t) we use unseen newton method
        So formula for this method is a_(n+1) = a_n + h(f(a_(n+1),t_(n+1)))
        
        We got condition in a way as number_1 * a_(1*) + number2 * a_(2*) + ... + number_q * a_(q*)= d
        Let's show each previous a as next one. For 2 points we'll have something like :
         
            number_1 * (a_2 - h(f(a_2),2*)) + number_2 * a_2 = d
        
        We can then find a_2 from equation and then a_1.
        This approach will be used for both simplified and normal systems.
    '''

    def solve_simplified_system(self):

        a_max_tau = max(float(item) for row in self.a_tau for item in row)
        a_min_tau = min(float(item) for row in self.a_tau for item in row)

        phi_max_tau = max(float(item) for row in self.phi_tau for item in row)
        phi_min_tau = min(float(item) for row in self.phi_tau for item in row)

        a_solution = []
        phi_solution = []
        step_h = 0.01
        points_amount = int((float(self.L2) - float(self.L1)) / step_h) + 1

        variables = [f'a{i + 1}' for i in range(len(self.x0_vector))]
        variable_string = ' '.join(variables)
        variables_tuple = sp.symbols(variable_string)
        if isinstance(variables_tuple, sp.Symbol):
            variables_tuple = (variables_tuple,)
        symbols_dict = dict(zip(variables, variables_tuple))

        phi_variables = [f'phi{i + 1}' for i in range(len(self.omega_vector))]
        phi_variable_string = ' '.join(phi_variables)
        phi_variables_tuple = sp.symbols(phi_variable_string)
        if isinstance(phi_variables_tuple, sp.Symbol):
            phi_variables_tuple = (phi_variables_tuple,)
        phi_symbols_dict = dict(zip(phi_variables, phi_variables_tuple))

        modified_x1_vector = modified_strings = [re.sub(r'phi\d+', '0', s) for s in self.x1_vector]
        modified_y1_vector = modified_strings = [re.sub(r'phi\d+', '0', s) for s in self.x1_vector]

        a_substitute_amount = int((a_max_tau - a_min_tau) / step_h)
        a_substitute_equations = []
        for i in range(0, len(self.x0_vector)):
            a_substitute_equations.append(self.x0_vector[i])

        a_equation_strings = []
        for i in range(0, len(self.x0_vector)):
            a_equation_string = f"{self.a_d[i]}" if float(self.a_d[i]) < 0 else f"-{self.a_d[i]}"
            a_equation_strings.append(a_equation_string)

        for i in range(0, len(self.x0_vector)):
            a_i_solution = [0.0] * points_amount
            a_solution.append(a_i_solution)

        for i in range(0, a_substitute_amount):
            tau = a_max_tau - i * step_h
            for j in range(0, len(self.x0_vector)):
                a_substitute_equations[j] = a_substitute_equations[j].replace("tau", str(tau))
                for a_index_replace in range(0, len(self.x0_vector)):
                    a_substitute_equations[j] = a_substitute_equations[j].replace(
                        f"a{a_index_replace + 1}",
                        f"(a{a_index_replace + 1} + {step_h}*(" + self.x0_vector[a_index_replace] + "))")
                    a_substitute_equations[j] = a_substitute_equations[j].replace("tau", str(tau))
                a_substitute_equations[j] = str(eval(a_substitute_equations[j], symbols_dict))
                if str(tau) in self.a_tau[j]:
                    tau_index = self.a_tau[j].index(str(tau))
                    a_equation_strings[j] = a_equation_strings[j] + "+" + self.a_alpha[j][tau_index] + "*(" + \
                                            a_substitute_equations[j] + ")"

        for i in range(0, len(self.x0_vector)):
            if float(self.a_alpha[i][len(self.a_alpha[i]) - 1]) > 0:
                a_equation_strings[i] = a_equation_strings[i] + "+" + str(
                    self.a_alpha[i][len(self.a_alpha[i]) - 1]) + f"*a{i + 1}"
            else:
                a_equation_strings[i] = a_equation_strings[i] + str(
                    self.a_alpha[i][len(self.a_alpha[i]) - 1]) + f"*a{i + 1}"
            a_equation_strings[i] = a_equation_strings[i].replace(".00", "").replace(",", ".").replace("tau",
                                                                                                       f"{a_min_tau}")
            a_equation_strings[i] = str(eval(a_equation_strings[i], symbols_dict))
            print(f"Full a{i + 1} equation {a_equation_strings[i]}")

        sympy_eqs = [eval(eq, {}, symbols_dict) for eq in a_equation_strings]
        # Convert the sympy equation to a numerical function
        f_lambdified = sp.lambdify(variables_tuple, sympy_eqs, modules=['numpy'])
        # Solve the equation
        initial_guess = [0.5] * len(self.x0_vector)

        solution = fsolve(lambda vars: f_lambdified(*vars), initial_guess)
        # So we have a_n in a_i. Let's find all other a_s
        for i in range(0, len(self.x0_vector)):
            a_solution[i][int(a_max_tau / step_h)] = float(solution[i])

        find_prev_strings = [""] * len(self.x0_vector)
        for a_i_index in range(int(a_max_tau / step_h) - 1, -1, -1):
            for i in range(len(self.x0_vector)):
                find_prev_strings[i] = f"a{i + 1} - {step_h}*(" \
                                       + self.x0_vector[i].replace(".00", "").replace(",", ".").replace("tau", str(
                    a_max_tau - step_h * (int(a_max_tau / step_h) - a_i_index))) + ")"
                for j in range(len(self.x0_vector)):
                    find_prev_strings[i] = find_prev_strings[i].replace(f"a{i + 1}", f"{a_solution[i][a_i_index + 1]}")
                find_prev_strings[i] = find_prev_strings[i] + f"-a{i + 1}"
            sympy_eqs = [eval(eq, {}, symbols_dict) for eq in find_prev_strings]
            f_lambdified = sp.lambdify(variables_tuple, sympy_eqs, modules=['numpy'])
            initial_guess = [0.5] * len(self.x0_vector)
            solution = fsolve(lambda vars: f_lambdified(*vars), initial_guess)
            for ii in range(0, len(self.x0_vector)):
                a_solution[ii][a_i_index] = float(solution[ii])

        find_next_strings = [""] * len(self.x0_vector)
        for a_i_index in range(int(a_max_tau / step_h) + 1, points_amount):
            for i in range(len(self.x0_vector)):
                if a_solution[i][a_i_index - 1] > 0:
                    find_next_strings[i] = f"-{a_solution[i][a_i_index - 1]}"
                else:
                    find_next_strings[i] = f"{math.fabs(a_solution[i][a_i_index - 1])}"
                tau_value = a_max_tau + step_h * (a_i_index - int(a_max_tau / step_h))
                find_next_strings[i] = find_next_strings[i] + f" + a{i + 1} - {step_h}*("
                find_next_strings[i] = find_next_strings[i] + self.x0_vector[i].replace(".00",
                                                                                        "").replace(",", ".").replace(
                    "tau", str(tau_value))
                find_next_strings[i] = find_next_strings[i] + " )"
            sympy_eqs = [eval(eq, {}, symbols_dict) for eq in find_next_strings]
            f_lambdified = sp.lambdify(variables_tuple, sympy_eqs, modules=['numpy'])
            initial_guess = [0.5] * len(self.x0_vector)
            solution = fsolve(lambda vars: f_lambdified(*vars), initial_guess)
            for ii in range(0, len(self.x0_vector)):
                a_solution[ii][a_i_index] = float(solution[ii])

        for i in range(len(a_solution)):
            print(f"a{i + 1} solution {a_solution[i]}")

        phi_substitute_amount = int((phi_max_tau - phi_min_tau) / step_h)
        phi_substitute_equations = []
        for i in range(0, len(self.omega_vector)):
            phi_substitute_equations.append(f"({self.omega_vector[i]})/{self.epsilon} + ({self.y_vector[i]})")

        phi_equation_strings = []
        for i in range(0, len(self.omega_vector)):
            phi_equation_string = f"{self.phi_d[i]}" if float(self.phi_d[i]) < 0 else f"-{self.phi_d[i]}"
            phi_equation_strings.append(phi_equation_string)

        for i in range(0, len(self.omega_vector)):
            phi_i_solution = [0.0] * points_amount
            phi_solution.append(phi_i_solution)

        # On this step we have all a's, so we can calculate phi
        for i in range(0, phi_substitute_amount):
            tau = phi_max_tau - i * step_h
            for j in range(0, len(self.omega_vector)):
                phi_substitute_equations[j] = phi_substitute_equations[j].replace("tau", str(tau))
                for phi_index_replace in range(0, len(self.omega_vector)):
                    replace_phi_string = f"(a{phi_index_replace + 1} + {step_h}*(({self.omega_vector[phi_index_replace]})/{self.epsilon} + ( " + \
                                         self.y_vector[phi_index_replace] + " ) ) )"
                    phi_substitute_equations[j] = phi_substitute_equations[j].replace(f"a{phi_index_replace + 1}",
                                                                                      replace_phi_string)
                    phi_substitute_equations[j] = phi_substitute_equations[j].replace("tau", str(tau))
                phi_substitute_equations[j] = str(eval(phi_substitute_equations[j], phi_symbols_dict))
                if str(tau) in self.phi_tau[j]:
                    tau_index = self.phi_tau[j].index(str(tau))
                    phi_equation_strings[j] = phi_equation_strings[j] + "+" + self.phi_beta[j][tau_index] + "*(" + \
                                              phi_substitute_equations[j] + ")"

        for i in range(0, len(self.omega_vector)):
            if float(self.phi_beta[i][len(self.phi_beta[i]) - 1]) > 0:
                phi_equation_strings[i] = phi_equation_strings[i] + "+" + str(
                    self.phi_beta[i][len(self.phi_beta[i]) - 1]) + f"*phi{i + 1}"
            else:
                phi_equation_strings[i] = phi_equation_strings[i] + str(
                    self.a_alpha[i][len(self.a_alpha[i]) - 1]) + f"*phi{i + 1}"
            phi_equation_strings[i] = phi_equation_strings[i].replace(".00", "").replace(",", ".").replace("tau",
                                                                                                       f"{phi_min_tau}")
            print(f"Full phi{i + 1} equation {phi_equation_strings[i]}")
            phi_equation_strings[i] = str(eval(phi_equation_strings[i], phi_symbols_dict))
            print(f"Full phi{i + 1} equation {phi_equation_strings[i]}")

        sympy_eqs = [eval(eq, {}, phi_symbols_dict) for eq in phi_equation_strings]
        # Convert the sympy equation to a numerical function
        f_lambdified = sp.lambdify(phi_variables_tuple, sympy_eqs, modules=['numpy'])
        # Solve the equation
        initial_guess = [0.5] * len(self.omega_vector)

        solution = fsolve(lambda vars: f_lambdified(*vars), initial_guess)
        # So we have a_n in a_i. Let's find all other a_s
        for i in range(0, len(self.omega_vector)):
            phi_solution[i][int(phi_max_tau / step_h)] = float(solution[i])

        simplified_solution = [a_solution, phi_solution]
        return simplified_solution


def all_a_separate(self):
    for x_0, i in self.x0_vector, len(self.x0_vector):
        for j in range(0, len(self.x0_vector)):
            if j != i and x_0.contans(f"a{j}"):
                return False
    for x_1, i in self.x1_vector, len(self.x1_vector):
        for j in range(0, len(self.x1_vector)):
            if j != i and x_1.contans(f"a{j}"):
                return False
    return True
