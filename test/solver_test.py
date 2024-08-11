from Solver import Solver


def first_test():
    solver = Solver(["-2*a1", "4+tau"], [""], [""], [""], [["0.3", "0.4"],["0.2"]],
                    [["3", "-4"],["-2"]], ["9","3"], [""], [""], [""], "0.001", "0.0", "0.5")
    solver.solve()


if __name__ == "__main__":
    print("Starting solver test.")
    print("Running first test.")

    first_test()
