from CSP import CSP


def __input_sudoku():
    print("Enter the sudoku:")
    return [[int(n) for n in input().split(" ")] for _ in range(9)]


def __is_valid_sudoku(grid: list[list[int]]) -> bool:
    result = []
    for i in range(9):
        for j in range(9):
            if (s := str(grid[i][j])) != "0":
                result += [(i, s), (s, j), (i // 3, j // 3, s)]
    return len(result) == len(set(result))


def sudoku():
    grid = __input_sudoku()

    if not __is_valid_sudoku(grid):
        print("Invalid sudoku")
        return

    domain = range(1, 10)
    variables = {i: domain for i in range(81) if grid[i // 9][i % 9] == 0}
    csp = CSP(variables)

    def update_grid(values: dict[int, int]):
        new_grid = []
        for i in range(9):
            row = [values.get(i * 9 + j) or grid[i][j] for j in range(9)]
            new_grid.append(row)
        return new_grid

    def check_sudoku(values: dict[int, int]) -> bool:
        return __is_valid_sudoku(update_grid(values))

    csp.add_constraint(variables, check_sudoku)

    result = csp()
    if result is None:
        print("No solution found")
        return

    grid = update_grid(result)
    for row in grid:
        print(row)
