from sudoku import Sudoku


def main():
    s = Sudoku()
    p1 = (0, 0, 1)
    p2 = (0, 4, 1)
    p3 = (4, 0, 1)
    p4 = (1, 1, 1)
    print(s.play(*p1))
    print(s.play(*p2))
    print(s.play(*p3))
    print(s.play(*p4))

    print(s)


if __name__ == '__main__':
    main()