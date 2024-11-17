from CSP import CSP


def ex1():
    variables = {
        "A": {1, 2, 3, 5, 8, 13},
        "B": range(-10, 11, 2),
        "C": range(0, 5),
        "D": range(-10, 10),
    }

    csp = CSP(variables)

    def compare(v1: str, v2: str, values: dict[str, int]) -> bool:
        a, b = values.get(v1), values.get(v2)
        if a is None or b is None:
            return True
        return a < b

    csp.add_constraint(["A", "B"], lambda values: compare("A", "B", values))
    csp.add_constraint(["B", "C"], lambda values: compare("B", "C", values))
    csp.add_constraint(["C", "D"], lambda values: compare("C", "D", values))

    print(csp())
