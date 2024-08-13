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
        step_h = 0.01
        points_amount = int((float(self.L2) - float(self.L1)) / step_h) + 1

        variables = [f'a{i + 1}' for i in range(len(self.x0_vector))]
        variable_string = ' '.join(variables)
        variables_tuple = sp.symbols(variable_string)
        symbols_dict = dict(zip(variables, variables_tuple))

        phi_variables = [f'phi{i + 1}' for i in range(len(self.omega_vector))]
        phi_variable_string = ' '.join(variables)
        phi_variables_tuple = sp.symbols(variable_string)
        phi_symbols_dict = dict(zip(variables, variables_tuple))

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
                    a_equation_strings[i] = a_equation_strings[i] + "+" + self.a_alpha[j][tau_index] + "*(" + \
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

        sympy_eqs = [eval(a_equation_strings[i], {}, symbols_dict) for eq in a_equation_strings]
        # Convert the sympy equation to a numerical function
        f_lambdified = sp.lambdify(variables_tuple, sympy_eqs, modules=['numpy'])
        # Solve the equation
        initial_guess = [0.5] * len(self.x0_vector)

        solution = fsolve(lambda vars: f_lambdified(*vars), initial_guess)
        print(f"solution: {solution}")
        # So we have a_n in a_i. Let's find all other a_s
        for i in range(0, len(self.x0_vector)):
            a_i_solution[i][int(a_max_tau / step_h)] = float(solution[i][0])

        for i in range(0, 0):
            for a_i_index in range(int(a_max_tau / step_h), 0, -1):
                find_prev_str = f"{a_i_solution[a_i_index]} - {step_h}*(" + self.x0_vector[i].replace(".00",
                                                                                                      "").replace(
                    ".0", "").replace(",", ".").replace(f"a{i + 1}", f"{a_i_solution[a_i_index]}") + ")"
                a_i_solution[a_i_index - 1] = eval(find_prev_str)
            for a_i_index in range(int(a_max_tau / step_h) + 1, points_amount):
                find_prev_str = f"a-{step_h}*(" + self.x0_vector[i].replace(".00",
                                                                            "").replace(
                    ".0", "").replace(",", ".").replace(f"a{i + 1}", "a") + f")-{a_i_solution[a_i_index - 1]}"
                a = sp.symbols('a')
                equation = eval(find_prev_str)
                f_lambdified = sp.lambdify(a, equation, modules=['numpy'])
                a_i_solution[a_i_index] = float(fsolve(f_lambdified, 0.1)[0])
            a_solution.append(a_i_solution)
            # Print the solution
            print(f"Found  a{i + 1} : {a_i_solution}")
        # On this step we have all a's, so we can calculate phi
        phi_solution = []
        for i in range(0, 0):  # , len(self.omega_vector)
            # logic should be the same, we just should add a's on fly calculation
            phi_i_solution = [0.0] * points_amount
            phi_equation_string = f"{self.phi_d[i]}" \
                if float(self.phi_d[i]) < 0 else f"-{self.phi_d[i]}"

            phi_substitute_equation = self.omega_vector[i]
            phi_substitute_amount = int((phi_max_tau - phi_min_tau) / step_h)
            # loop
            '''
                phi_n+1 = phi_n + h*(omega(a_n,tau_n+1)/epsilon)
            '''
            for j in range(phi_substitute_amount):
                tau = a_min_tau + j * step_h
                phi_substitute_equation = phi_substitute_equation.replace("tau", str(tau))
                phi_substitute_equation = phi_substitute_equation.replace(f"a{i + 1}",
                                                                          str(a_solution[i][int(tau / step_h)]))
                phi_substitute_equation = phi_substitute_equation.replace(f"phi{i + 1}",
                                                                          f"(phi{i + 1} + {step_h}*(" +
                                                                          self.omega_vector[
                                                                              i] + f")/{self.epsilon})")

                phi_substitute_equation = str(eval(phi_substitute_equation, phi_symbols_dict))
                if str(tau) in self.phi_tau[i]:
                    tau_index = self.phi_tau[i].index(str(tau))
                    phi_equation_string = phi_equation_string + "+" + self.phi_beta[i][
                        tau_index] + "*(" + phi_substitute_equation + ")"
                pass
            phi_equation_string = phi_equation_string + "+" + str(
                self.phi_beta[i][len(self.phi_beta[i]) - 1]) + f"*phi{i + 1}" \
                if float(self.phi_beta[i][len(self.phi_beta[i]) - 1]) > 0 else phi_equation_string + str(
                self.phi_beta[i][len(self.phi_beta[i]) - 1]) + f"*phi{i + 1}"

            phi_equation_string = phi_equation_string.replace(".00", "").replace(",", ".").replace(
                f"phi{i + 1}", "phi")

            print(f"Full phi{i + 1} equation {phi_equation_string}")

            # we have build solution for one variable by substitution and want to find this one dot
            # Parse the equation string

            phi = sp.symbols('phi')
            equation = eval(phi_equation_string)
            # Convert the sympy equation to a numerical function
            f_lambdified = sp.lambdify(phi, equation, modules=['numpy'])
            # Solve the equation
            solution = fsolve(f_lambdified, 0.1)
            phi_i_solution[int(phi_max_tau / step_h)] = float(solution[0])
            for phi_i_index in range(int(phi_max_tau / step_h), 0, -1):
                find_prev_str = f"{phi_i_solution[phi_i_index]} - {step_h}*(" + self.omega_vector[i].replace(".00",
                                                                                                             "").replace(
                    ".0", "").replace(",", ".").replace(f"a{i + 1}", f"{a_solution[i][phi_i_index]}").replace(
                    f"phi{i + 1}", f"{phi_i_solution[phi_i_index]}").replace(f"tau",
                                                                             f"{phi_min_tau + step_h * phi_i_index}") + f")/{self.epsilon}"
                phi_i_solution[phi_i_index - 1] = eval(find_prev_str)
            for phi_i_index in range(int(phi_max_tau / step_h) + 1, points_amount):
                find_prev_str = f"phi-{step_h}*(" + self.omega_vector[i].replace(".00",
                                                                                 "").replace(
                    ".0", "").replace(",", ".").replace(f"phi{i + 1}", "phi").replace(f"tau",
                                                                                      f"{phi_min_tau + step_h * phi_i_index}").replace(
                    f"a{i + 1}", f"{a_solution[i][phi_i_index]}") + f")-{phi_i_solution[phi_i_index - 1]}"
                phi = sp.symbols('phi')
                equation = eval(find_prev_str)
                f_lambdified = sp.lambdify(phi, equation, modules=['numpy'])
                phi_i_solution[phi_i_index] = float(fsolve(f_lambdified, 0.1)[0])
            # Print the solution
            print(f"Found phi{i + 1} : {phi_i_solution}")
            phi_solution.append(phi_i_solution)

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
