from copy import deepcopy
from random import choice

from helper_classes import *


class BoardLogic:
    @staticmethod
    def next_boards(values, cars_info):
        """
        :param values: A non graphical representation of a board
        :param cars_info:  Dictionary with information for each car in the board
        :return: List of nodes that represent all the boards that can be reached within one move from the board inputted
        """
        next_boards = []  # Initialize the list of next boards
        for i, row in enumerate(values):  # For each row in the board
            for j, value in enumerate(row):  # For each cell in the row
                if value == "_":  # If the cell is empty
                    if i != 0:  # If there is a cell above
                        car_value = values[i - 1][j]  # The value of the cell above
                        if car_value != "_":  # If the cell above is a car
                            if cars_info[car_value][0] == Direction.vertical:  # If the car above moves vertically
                                next_board = deepcopy(values)  # Make a copy of the current board
                                car_length = cars_info[car_value][1]

                                # Move the car:
                                next_board[i - car_length][j] = "_"
                                next_board[i][j] = car_value

                                next_boards.append(Node(next_board))  # Add the next board to the next boards list

                    if j != 0:  # If there is a cell to the left
                        car_value = values[i][j - 1]  # The value of the cell to the left
                        if car_value != "_":  # If the cell to the left is a car
                            if cars_info[car_value][0] == Direction.horizontal:  # If the left car moves horizontally
                                next_board = deepcopy(values)  # Make a copy of the current board
                                car_length = cars_info[car_value][1]

                                # Move the car:
                                next_board[i][j - car_length] = "_"
                                next_board[i][j] = car_value

                                next_boards.append(Node(next_board))  # Add the next board to the next boards list

                    if i != Constants.SIZE - 1:  # If there is a cell below
                        car_value = values[i + 1][j]  # The value of the cell below
                        if car_value != "_":  # If the cell below is a car
                            if cars_info[car_value][0] == Direction.vertical:  # If the below car moves vertically
                                next_board = deepcopy(values)  # Make a copy of the current board
                                car_length = cars_info[car_value][1]

                                # Move the car:
                                next_board[i + car_length][j] = "_"
                                next_board[i][j] = car_value

                                next_boards.append(Node(next_board))  # Add the next board to the next boards list

                    if j != Constants.SIZE - 1:  # If there is a cell to the right
                        car_value = values[i][j + 1]  # The value of the cell to the right
                        if car_value != "_":  # If the cell to the right is a car
                            if cars_info[car_value][0] == Direction.horizontal:  # If the right car moves horizontally
                                next_board = deepcopy(values)  # Make a copy of the current board
                                car_length = cars_info[car_value][1]

                                # Move the car:
                                next_board[i][j + car_length] = "_"
                                next_board[i][j] = car_value

                                next_boards.append(Node(next_board))  # Add the next board to the next boards list

        return next_boards

    @staticmethod
    def bfs(start, cars_info):
        """
        :param start: A node that represents the board shown on screen when the bfs is called
        :param cars_info: Dictionary with information for each car in the board
        :return: Path to the solved board
        """
        if BoardLogic.is_win(start.value):  # If the board is already solved
            return start  # Return the starting board
        visited = [start.value]  # Initialize the list of visited boards
        current_boards = [start]  # List of all the boards in the current level
        while current_boards:  # While there are boards in the current level.
            # If this while loop finishes, there is no solution to the board inputted.
            next_boards = []  # List of all the boards in the next level.
            for current_board in current_boards:  # For each board in the current level.
                for next_board in BoardLogic.next_boards(current_board.value, cars_info):
                    # For each next board that can be reached within one move from the current board.
                    if next_board.value not in visited:  # If that next board hasn't been checked already.
                        visited.append(next_board.value)
                        # Append that next board to the list of visited boards so it won't be checked twice.
                        next_board.next = current_board  # Set the parent of the next board to the current board.
                        #  This is done so we'll have a path from that next board all the way to the initial board.
                        if BoardLogic.is_win(next_board.value):  # If that next board is a solved board.
                            return Node.reverse_list(next_board)
                            # Return the reversed linked list of the boards representing a path to the solved board.
                        next_boards.append(next_board)
                        # Append that next board to the list of all boards in the next level.
            current_boards = next_boards
            # We've finished going over the level,
            # so all the boards in the next level are now the boards in the current level.

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
