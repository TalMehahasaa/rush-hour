from enum import Enum
from copy import deepcopy


class Constants:
    SIZE = 6
    COLORS = {
        "X": (1, 0, 0, 1),
        "A": (.2, .9, .5, 1),
        "B": (1, .5, 0, 1),
        "C": (.25, .65, 1, 1),
        "D": (1, .5, .5, 1),
        "E": (.3, 0, .7, 1),
        "F": (0, .4, .2, 1),
        "G": (.05, .05, .2, 1),
        "H": (1, 1, .8, 1),
        "I": (1, 1, .5, 1),
        "J": (.25, .15, .1, 1),
        "K": (.25, .4, .05, 1),
        "O": (.9, .8, 0, 1),
        "P": (.5, 0, .9, 1),
        "Q": (.1, .1, 1, 1),
        "R": (.05, .7, .7, 1),
        "_": (1, 1, 1, 1)
    }


class Direction(Enum):
    horizontal = 1
    vertical = 2


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent


class BoardLogic:
    @staticmethod
    def print_board(values):
        for row in values:
            for value in row:
                print(value, end=" ")
            print()

    @staticmethod
    def find_car_positions(car_value, values):
        positions = []
        for i, row in enumerate(values):
            for j, value in enumerate(row):
                if value == car_value:
                    positions.append((i, j))
        return positions

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
    def is_winning_state(board):
        winning_row = board[Constants.SIZE // 2 - 1]
        x_pos = 100
        for index, cell in enumerate(winning_row):
            if cell == "X":
                x_pos = index
            elif index > x_pos and cell != "_":  # There is a car blocking the exit
                return False
        return True

    @staticmethod
    def bfs(start, cars_info):
        visited = [start.value]
        current_boards = [start]
        while current_boards:
            next_boards = []
            for current_board in current_boards:
                for next_board in BoardLogic.next_boards(current_board.value, cars_info):
                    if next_board.value not in visited:
                        visited.append(next_board.value)
                        next_board.parent = current_board
                        if BoardLogic.is_winning_state(next_board.value):
                            return next_board
                        next_boards.append(next_board)
            current_boards = next_boards

    #####################################################################
    #                           Graphical Logic                         #
    #####################################################################

    @staticmethod
    def possible_moves(car, values):
        if car.value != "_":  # If this is a car
            possible_moves = []
            if car.direction == Direction.horizontal:
                line = values[car.positions[0][0]]  # Get the row the car is in
                indices_of_car = list(zip(*car.positions))[1]  # The indices of the car in the row
            else:
                line = [values[i][car.positions[0][1]] for i in range(Constants.SIZE)]  # Get the column the car is in
                indices_of_car = list(zip(*car.positions))[0]  # The indices of the car in the column

            first = indices_of_car[0]  # The first index of the car
            last = indices_of_car[-1]  # The last index of the car

            counter = 1
            for index in range(first - 1, -1, -1):  # Check moves before car
                if line[index] == "_":  # The cell is empty
                    possible_moves.append(-counter)
                    counter += 1
                else:  # The cell contains a car
                    break

            counter = 1
            for index in range(last + 1, Constants.SIZE):  # Check moves after car
                if line[index] == "_":  # The cell is empty
                    possible_moves.append(counter)
                    counter += 1
                else:  # The cell contains a car
                    break

            return possible_moves
        return []

    @staticmethod
    def make_move(car, move, values):
        if move in BoardLogic.possible_moves(car, values):  # If the move is valid
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

        return values
