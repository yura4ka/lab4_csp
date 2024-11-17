from CSP import CSP


def ex2():
    variables = {
        "A": {-2, 1, 3, 5},
        "B": range(1, 7),
        "C": range(1, 5),
        "D": range(-5, 5, 2),
    }

    csp = CSP(variables)

    def check(values: dict[str, int]) -> bool:
        a = values.get("A")
        b = values.get("B")
        c = values.get("C")
        d = values.get("D")
        if a is None or b is None or c is None or d is None:
            return True

        return a + 2 * b == 3 * c - d

    csp.add_constraint(variables, check)

    print(csp())
