from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from board_logic import BoardLogic
from helper_classes import *


class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)
        self.values = BoardLogic.decrypt_values(Constants.BOARDS[0])
        # TODO: Check difficulty chosen by the player and use a board accordingly
        self.cars_info = BoardLogic.find_cars_info(self.values)
        self.cars = None
        self.update_position_of_cars()

        self.tiles = []
        for i in range(Constants.SIZE):
            row = []
            for j in range(Constants.SIZE):
                tile = Tile((i, j), self)
                row.append(tile)
                self.add_widget(tile)
            self.tiles.append(row)

    def update_position_of_cars(self):
        """Updates the cars attribute with correct positions of the cars to match the screen
            and to keep track of each car so the player can move it"""
        self.cars = dict()
        for car_id in self.cars_info.keys():
            self.cars[car_id] = Car(car_id, self)

    def redraw(self, new_values):
        """Update the GUI to match the logic"""
        self.values = new_values
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.tiles[i][j].change_color(value)


class Car:
    def __init__(self, value, board):
        self.value = value
        self.board = board
        self.positions = BoardLogic.find_car_positions(self.value, self.board.values)
        self.direction, self.length = self.board.cars_info[self.value]


class Tile(Button):
    def __init__(self, position, board):
        super().__init__()
        self.i, self.j = position
        self.board = board
        self.car = self.find_car()  # Find the car that the tile is on
        self.background_color = Constants.COLORS[self.car.value if self.car else "_"]

    def find_car(self):
        value = self.board.values[self.i][self.j]
        if value != "_":
            return self.board.cars[value]

    def on_press(self):
        self.car = self.find_car()
        if self.car:  # If the player pressed on a car
            possible_moves = BoardLogic.possible_moves(self.car, self.board.values)
            if len(possible_moves) > 0:  # If there are moves possible
                if (self.i, self.j) == self.car.positions[-1]:
                    move = 1
                elif (self.i, self.j) == self.car.positions[0]:
                    move = -1
                else:
                    return
                new_values = BoardLogic.make_move(self.car, move, self.board.values)
                self.board.redraw(new_values)

    def change_color(self, value):
        self.background_color = Constants.COLORS[value]


class RestartButton(Button):
    def on_press(self):
        board = self.parent.parent.children[1]
        board.redraw(BoardLogic.decrypt_values(Constants.BOARDS[0]))
        board.update_position_of_cars()
        self.parent.children[1].stop_animation()


class SolveButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = None  # A reference to the board object
        self.current_node = None  # The board being displayed on the screen
        self.event = None  # The animation object. Used to start/ stop the animation
        self.text = "Solve"

    def on_press(self):
        if not self.board:
            self.board = self.parent.parent.children[1]  # Get the reference when the button has been pressed

        if self.text == "Solve":  # If the player clicked Solve
            winning_path = self._get_winning_path()  # Solve the board and get the shortest solution linked list

            number_of_moves_to_solve = length_of_linked_list(winning_path)
            print(number_of_moves_to_solve, "moves to solve")  # Print the number of moves of the solution

            self.current_node = winning_path.parent
            self.event = Clock.schedule_interval(self._callback, Constants.INTERVAL_TIME)  # Start the animation

            self.text = "Stop"

        else:  # If the player clicked Stop
            self.stop_animation()

    def stop_animation(self):
        if not self.text == "Solve":  # If the animation is running
            Clock.unschedule(self.event)
            self.current_node = None
            self.board.update_position_of_cars()
            # Update cars attribute for the player to be able to continue playing
            self.text = "Solve"

    def _callback(self, _):
        if self.current_node:
            self.board.redraw(self.current_node.value)
            self.current_node = self.current_node.parent
        else:  # The board is solved
            self.stop_animation()
            # TODO: Make the car exit

    def _get_winning_path(self):
        current_board = Node(self.board.values)
        cars_info = self.board.cars_info
        path_to_solve = reverse_list(
            BoardLogic.bfs(current_board, cars_info)
        )  # A linked list of the boards leading to a winning solution
        return path_to_solve
