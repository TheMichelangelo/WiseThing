from Solver import Solver


def first_test():
    solver = Solver(x0_vector=["-2*a1+a2", "4+tau"], x1_vector=[""], omega_vector=["-a1+tau"], y_vector=[""],
                    a_tau=[["0.3", "0.4"], ["0.33"]], a_alpha=[["3", "-4"], ["-2"]],
                    a_d=["9", "3"], phi_tau=[["0.3"]], phi_beta=[["5"]], phi_d=["1"], epsilon="0.01", l1=0, l2=0.5)
    solver.solve()


if __name__ == "__main__":
    print("Starting solver test.")
    print("Running first test.")

    first_test()
