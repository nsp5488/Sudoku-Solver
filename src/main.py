from sudoku import Sudoku


def main():
    s = Sudoku()
    s._generate_game()
    # s.fill_board()

    print(s)


if __name__ == '__main__':
    main()