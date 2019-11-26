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
        "G": (1, 1, 1, 1),
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


class BoardLogic:
    @staticmethod
    def print_board(values):
        print("****************")
        for row in values:
            print(row)
        print("****************")

    @staticmethod
    def change_board(car, move, values):
        if move in BoardLogic.possible_moves(car, values):
            new_positions = []
            for i, j in car.positions:
                if car.direction == Direction.vertical:
                    new_positions.append((i + move, j))
                else:
                    new_positions.append((i, j + move))

            new_values = deepcopy(values)
            for i, j in car.positions:
                new_values[i][j] = "_"
            for i, j in new_positions:
                new_values[i][j] = car.value

            car.positions = new_positions
            return new_values

    @staticmethod
    def possible_moves(car, values):
        possible_moves = []
        if car.direction == Direction.horizontal:
            line = values[car.positions[0][0]]  # Get the row the car is in
            indices_of_car = list(zip(*car.positions))[1]  # The indices of the car in the row
        else:
            line = [car.board.values[i][car.positions[0][1]] for i in
                    range(Constants.SIZE)]  # Get the column the car is in
            indices_of_car = list(zip(*car.positions))[0]  # The indices of the car in the column

        first = indices_of_car[0]  # The first index of the car
        last = indices_of_car[-1]  # The last index of the car

        counter = 1
        for index in range(first - 1, -1, -1):
            if line[index] == "_":  # The cell is empty
                possible_moves.append(-counter)
                counter += 1
            else:  # The cell has a car
                break

        counter = 1
        for index in range(last + 1, Constants.SIZE):
            if line[index] == "_":  # The cell is empty
                possible_moves.append(counter)
                counter += 1
            else:
                break

        return possible_moves
