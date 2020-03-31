from copy import deepcopy
from random import choice

from helper_classes import *


class BoardLogic:
    @staticmethod
    def next_boards(board, cars_info):
        next_boards = []
        for i, row in enumerate(board):
            for j, value in enumerate(row):
                if value == "_":
                    if i != 0:  # If there is a cell above
                        car_value = board[i - 1][j]
                        if car_value != "_":  # If there is a car in the above cell
                            if cars_info[car_value][0] == Direction.vertical:  # If the car above moves vertically
                                next_board = deepcopy(board)
                                car_length = cars_info[car_value][1]
                                # Move the car
                                next_board[i - car_length][j] = "_"
                                next_board[i][j] = car_value
                                # Add the next board to the next boards list
                                next_boards.append(Node(next_board))

                    if j != 0:  # If there is a cell to the left
                        car_value = board[i][j - 1]
                        if car_value != "_":  # If there is a car in the cell to the left
                            if cars_info[car_value][0] == Direction.horizontal:  # If the left car moves horizontally
                                next_board = deepcopy(board)
                                car_length = cars_info[car_value][1]
                                # Move the car
                                next_board[i][j - car_length] = "_"
                                next_board[i][j] = car_value
                                # Add the next board to the next boards list
                                next_boards.append(Node(next_board))

                    if i != Constants.SIZE - 1:  # If there is a cell below
                        car_value = board[i + 1][j]
                        if car_value != "_":  # If there is a car below
                            if cars_info[car_value][0] == Direction.vertical:  # If the below car moves vertically
                                next_board = deepcopy(board)
                                car_length = cars_info[car_value][1]
                                # Move the car
                                next_board[i + car_length][j] = "_"
                                next_board[i][j] = car_value
                                # Add the next board to the next boards list
                                next_boards.append(Node(next_board))

                    if j != Constants.SIZE - 1:  # If there is a cell to the right
                        car_value = board[i][j + 1]
                        if car_value != "_":  # If there is a car to the right
                            if cars_info[car_value][0] == Direction.horizontal:  # If the right car moves horizontally
                                next_board = deepcopy(board)
                                car_length = cars_info[car_value][1]
                                # Move the car
                                next_board[i][j + car_length] = "_"
                                next_board[i][j] = car_value
                                # Add the next board to the next boards list
                                next_boards.append(Node(next_board))

        return next_boards

    @staticmethod
    def bfs(start, cars_info):
        if BoardLogic.is_win(start.value):
            return start
        visited = [start.value]
        current_boards = [start]
        while current_boards:
            next_boards = []
            for current_board in current_boards:
                for next_board in BoardLogic.next_boards(current_board.value, cars_info):
                    if next_board.value not in visited:
                        visited.append(next_board.value)
                        next_board.next = current_board
                        if BoardLogic.is_win(next_board.value):
                            return next_board
                        next_boards.append(next_board)
            current_boards = next_boards

    @staticmethod
    def choose_board(difficulty):
        """
        Chooses a random starting board based on the difficulty
        :param difficulty: The difficulty chosen by the player
        :return: A non graphical representation of the board (values)
        """
        if difficulty == Difficulty.beginner:
            chosen_board = choice(Constants.BEGINNER_BOARDS)
        elif difficulty == Difficulty.intermediate:
            chosen_board = choice(Constants.INTERMEDIATE_BOARDS)
        elif difficulty == Difficulty.advanced:
            chosen_board = choice(Constants.ADVANCED_BOARDS)
        else:
            chosen_board = choice(Constants.EXPERT_BOARDS)
        return BoardLogic.decrypt_values(chosen_board)

    #####################################################################
    #                           Player Logic                         #
    #####################################################################

    @staticmethod
    def is_win(values):
        """
        Checks whether the red car can escape freely
        :param values: A non graphical representation of a board
        :return bool: True if win, False otherwise
        """
        winning_row = values[Constants.SIZE // 2 - 1]  # The row that has the red car
        for value in winning_row[::-1]:  # Go over the row in a reversed order
            if value == "X":  # If it sees the red car
                return True
            elif value == "_":  # If it sees no car
                continue
            else:  # If it sees a car blocking the exit
                return False

    @staticmethod
    def decrypt_values(encrypted_board):
        """
        Get the initial values of a board
        :param encrypted_board: A string that represents a starting board and is easy to write
        :return: A matrix that represents the board non-graphically
        """
        values = []
        for i in range(Constants.SIZE):
            values.append(list(encrypted_board[i]))
        return values

    @staticmethod
    def find_cars_info(values):
        """Finds the orientation and length of each car"""
        cars_info = dict()
        for row in values:
            for j, value in enumerate(row):
                if value != "_" and value not in cars_info.keys():
                    length = 3 if value >= "O" else 2
                    if value == "X":
                        length = 2
                    if j > 0 and row[j - 1] == value:
                        direction = Direction.horizontal
                    elif j < Constants.SIZE - 1 and row[j + 1] == value:
                        direction = Direction.horizontal
                    else:
                        direction = Direction.vertical
                    cars_info[value] = (direction, length)
        return cars_info

    @staticmethod
    def find_car_positions(car_value, values):
        positions = []
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                if value == car_value:
                    positions.append((i, j))
        return positions

    @staticmethod
    def possible_moves(car, values):
        possible_moves = []
        if car.direction == Direction.horizontal:
            i, j = car.positions[0]
            if j - 1 != -1 and values[i][j - 1] == "_":
                possible_moves.append(-1)
            i, j = car.positions[-1]
            if j + 1 != Constants.SIZE and values[i][j + 1] == "_":
                possible_moves.append(1)
        else:
            i, j = car.positions[0]
            if i - 1 != -1 and values[i - 1][j] == "_":
                possible_moves.append(-1)
            i, j = car.positions[-1]
            if i + 1 != Constants.SIZE and values[i + 1][j] == "_":
                possible_moves.append(1)
        return possible_moves

    @staticmethod
    def make_move(car, move, values):
        new_positions = []
        for i, j in car.positions:
            if car.direction == Direction.vertical:
                new_positions.append((i + move, j))
            else:
                new_positions.append((i, j + move))

        new_values = deepcopy(values)

        for i, j in car.positions:  # Remove previous car position
            new_values[i][j] = "_"

        for i, j in new_positions:  # Put car in it's new position
            new_values[i][j] = car.value

        car.positions = new_positions
        return new_values
