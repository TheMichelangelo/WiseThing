import math
import random

import sympy as sp
from scipy.optimize import fsolve


class Solver:
    def __init__(self, x0_vector, x1_vector, omega_vector, y_vector, a_tau, a_alpha, a_d, phi_tau, phi_alpha, phi_d):
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
        for i in range(0, len(self.x0_vector)):
            a_equation_string = f"{self.a_d[i]}" \
                if float(self.a_d[i]) < 0 else f"-{self.a_d[i]}"

            a_substitute_equation = self.x0_vector[i]
            # for j in range(len(self.a_tau[i])-1, 0, -1):
            #    a_substitute_equation = a_substitute_equation.replace("tau", str(self.a_tau[i][j]))
            #    h_value = float(self.a_tau[i][j]) - float(self.a_tau[i][j - 1])
            #    h_value_str = "+" + str(math.fabs(h_value)) if h_value < 0 else "-" + str(h_value)
            #    a_substitute_equation = a_substitute_equation.replace(f"a{i + 1}",
            #                                                          f"(a{i + 1}"
            #                                                          + h_value_str
            #                                                          + "*(" + self.x0_vector[i] + "))")
            #    a_equation_string = (a_equation_string + "+"
            #                         + str(self.a_alpha[i][j-1]) + "*(" + a_substitute_equation + ")")

            # a_equation_string = a_equation_string + "+" + str(self.a_alpha[i][len(self.a_tau[i])-1]) + f"*a{i + 1}"

            for j in range(0, 20):
                tau = random.randint(1, 15)
                a_substitute_equation = a_substitute_equation.replace("tau", str(tau))
                #print(a_substitute_equation)
                a_substitute_equation = a_substitute_equation.replace("a1",
                                                                      "(a1 + 0.1*(" + self.x0_vector[0] + "))")
                if j in (2, 8, 17, 19):
                    a_equation_string = (a_equation_string + "+"
                                         + str(random.randint(2, 20)) + "*(" + a_substitute_equation + ")")
            a_equation_string = a_equation_string + "+" + str(str(random.randint(2, 20))) + "*a"

            a_equation_string = (a_equation_string.replace(".00", "").replace(".0", "")
                                 .replace(",", ".").replace(f"a{i+1}", "a"))
            #print(f"full a1 equation {a_equation_string}")

            # we have build solution for one variable by substitution and want to find this one dot
            # Parse the equation string
            a = sp.symbols('a')
            equation = eval(a_equation_string)
            # Convert the sympy equation to a numerical function
            f_lambdified = sp.lambdify(a, equation, modules=['numpy'])

            # Define a wrapper function for fsolve
            def equation_wrapper(a_value):
                return f_lambdified(a_value)

            # Initial guess for the solution
            initial_guess = 0.1

            # Solve the equation
            solution = fsolve(equation_wrapper, initial_guess)

            # Print the solution
            print(solution)
        pass

    def solve_simplified_system_for_one_point(self):
        pass

    def solve_system_for_one_point(self):
        pass
