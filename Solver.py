import math
import random

import sympy as sp
from scipy.optimize import fsolve


class Solver:
    def __init__(self, x0_vector, x1_vector, omega_vector, y_vector, a_tau, a_alpha, a_d, phi_tau, phi_alpha, phi_d,
                 epsilon, L1, L2):
        self.x0_vector = x0_vector
        self.x1_vector = x1_vector
        self.omega_vector = omega_vector
        self.y_vector = y_vector
        self.a_tau = a_tau
        self.a_alpha = a_alpha
        self.a_d = a_d
        self.phi_tau = phi_tau
        self.phi_alpha = phi_alpha
        self.phi_d = phi_d
        self.epsilon = epsilon
        self.L1 = L1
        self.L2 = L2
        pass

    def solve(self):
        self.solve_simplified_system()
        pass

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

        a_solution = []
        step_h = 0.1
        points_amount = int((float(self.L2) - float(self.L1)) / step_h) + 1
        for i in range(0, len(self.x0_vector)):
            a_i_solution = [0] * points_amount
            a_equation_string = f"{self.a_d[i]}" \
                if float(self.a_d[i]) < 0 else f"-{self.a_d[i]}"

            a_substitute_equation = self.x0_vector[i]
            a_substitute_amount = int((a_max_tau - a_min_tau) / step_h)

            for j in range(0, a_substitute_amount):
                tau = a_min_tau + j * step_h
                a_substitute_equation = a_substitute_equation.replace("tau", str(tau))
                a_substitute_equation = a_substitute_equation.replace(f"a{i + 1}",
                                                                      f"(a{i + 1} + {step_h}*(" + self.x0_vector[
                                                                          i] + "))")
                if str(tau) in self.a_tau[i]:
                    tau_index = self.a_tau[i].index(str(tau))
                    a_equation_string = a_equation_string + "+" + self.a_alpha[i][
                        tau_index] + "*(" + a_substitute_equation + ")"

            a_equation_string = a_equation_string + "+" + str(self.a_alpha[i][len(self.a_alpha[i]) - 1]) + f"*a{i + 1}" \
                if float(self.a_alpha[i][len(self.a_alpha[i]) - 1]) > 0 else a_equation_string + str(
                self.a_alpha[i][len(self.a_alpha[i]) - 1]) + f"*a{i + 1}"

            a_equation_string = a_equation_string.replace(".00", "").replace(".0", "").replace(",", ".").replace(
                f"a{i + 1}", "a")

            print(f"Full a{i} equation {a_equation_string}")

            # we have build solution for one variable by substitution and want to find this one dot
            # Parse the equation string
            a = sp.symbols('a')
            equation = eval(a_equation_string)
            # Convert the sympy equation to a numerical function
            f_lambdified = sp.lambdify(a, equation, modules=['numpy'])
            # Solve the equation
            solution = fsolve(f_lambdified, 0.1)
            # Print the solution
            print(f"First found a in a{i} is {solution}")

            # So we have a_n in a_i. Lets find all other a_s
            a_i_solution[int(a_max_tau / step_h)] = float(solution[0])
            for a_i_index in range(int(a_max_tau / step_h), 0, -1):
                find_prev_str = f"{a_i_solution[a_i_index]} - {step_h}*(" + self.x0_vector[i].replace(".00",
                                                                                                          "").replace(
                    ".0", "").replace(",", ".").replace(f"a{i + 1}", f"{a_i_solution[a_i_index]}") + ")"
                a_i_solution[a_i_index - 1] = eval(find_prev_str)

            a_solution.append(a_i_solution)
            for a_i_index in range(int(a_max_tau / step_h) + 1, points_amount):
                find_prev_str = f"a-{step_h}*(" + self.x0_vector[i].replace(".00",
                                                                                                          "").replace(
                    ".0", "").replace(",", ".").replace(f"a{i + 1}","a") + f")-{a_i_solution[a_i_index - 1]}"
                a = sp.symbols('a')
                equation = eval(find_prev_str)
                f_lambdified = sp.lambdify(a, equation, modules=['numpy'])
                a_i_solution[a_i_index] = float(fsolve(f_lambdified, 0.1)[0])
        print(a_solution)
        return a_solution



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


def solve_simplified_system_for_one_point(self):
    pass


def solve_system_for_one_point(self):
    pass
