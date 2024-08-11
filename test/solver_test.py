from Solver import Solver


def first_test():
    solver = Solver(["-2*a1"], [""], [""], [""], [["0.1", "0.2"]],
                    [["3", "-4"]], ["9"], [""], [""], [""], "0.001", "0.0", "0.4")
    solver.solve()


if __name__ == "__main__":
    print("Starting solver test.")
    print("Running first test.")

    first_test()
