from typing import Callable, Container, Iterable

type Constraint[T] = Callable[[dict[str, T]], bool]


class CSP[T]:
    def __init__(self, domains: dict[str, list[Container]]):
        self.variables = list(domains.keys())
        self.domains = domains
        self.constraints: dict[str, list[Constraint[T]]] = {
            v: [] for v in self.variables
        }

    def add_constraint(self, variables: Iterable[str], constraint: Constraint[T]):
        for v in variables:
            self.constraints[v].append(constraint)

    def __call__(self):
        return self.__backtracking({})

    def __is_consistent(self, variable: str, assignment: dict[str, T]):
        return all(constraint(assignment) for constraint in self.constraints[variable])

    def __select_unassigned_variable(self, assignment: dict[str, T]):
        return next(v for v in self.variables if v not in assignment)

    def __backtracking(self, assignment: dict[str, T]) -> dict[str, T] | None:
        if len(assignment) == len(self.variables):
            return assignment

        var = self.__select_unassigned_variable(assignment)
        for value in self.domains[var]:
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.__is_consistent(var, new_assignment):
                result = self.__backtracking(new_assignment)
                if result:
                    return result

        return None
