from soln import parse_input


def main():
    numbers, boards = parse_input()

    # call out numbers
    boards_left = len(boards)
    for number in numbers:
        for board in boards:
            if not board.is_complete:
                board.mark(number)
                if board.is_complete:
                    boards_left -= 1
                    if boards_left == 0:
                        print(board.value * number)
                        return


if __name__ == "__main__":
    main()
