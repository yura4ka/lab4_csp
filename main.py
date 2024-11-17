from examples.example1 import ex1
from examples.example2 import ex2
from examples.sudoku import sudoku


def main():
    print("""1 - Example 1
2 - Example 2
3 - Sudoku""")
    print(">", end=" ")
    s = input()
    if s == "1":
        ex1()
    if s == "2":
        ex2()
    if s == "3":
        sudoku()


if __name__ == "__main__":
    main()
