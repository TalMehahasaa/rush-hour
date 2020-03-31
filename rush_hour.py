from kivy.uix.gridlayout import GridLayout

from kivy_objects import *


class Board(GridLayout):
    def __init__(self, **kwargs):
        super(Board, self).__init__(**kwargs)

        self.tiles = []
        for i in range(Constants.SIZE):
            row = []
            for j in range(Constants.SIZE):
                tile = Tile((i, j), self)
                row.append(tile)
                self.add_widget(tile)
            self.tiles.append(row)

        self.starting_values = None
        self.values = None
        self.cars_info = None
        self.cars = None

    def create_board(self, difficulty):
        self.starting_values = BoardLogic.choose_board(difficulty)
        self.redraw(self.starting_values)
        self.update_attributes(self.starting_values)

    def restart(self):
        """Redraws the board and updates the position of the cars based on the starting values"""
        self.redraw(self.starting_values)
        self.update_position_of_cars()

    def update_position_of_cars(self):
        """Updates the cars attribute with correct positions of the cars to match the screen
            and to keep track of each car so the player can move it"""
        self.cars = dict()
        for car_id in self.cars_info.keys():
            self.cars[car_id] = Car(car_id, self)

    def redraw(self, new_values):
        """
        Update graphics based on the new_values parameter
        :param new_values: a non graphical representation of a board
        """
        self.values = new_values
        for i, row in enumerate(new_values):
            for j, value in enumerate(row):
                self.tiles[i][j].change_color(value)

    def update_attributes(self, new_values):
        """
        Update attributes of the board based on the new_values parameter
        :param new_values: a non graphical representation of a board
        """
        self.values = new_values
        self.cars_info = BoardLogic.find_cars_info(new_values)
        self.update_position_of_cars()


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
        self.car = None

    def find_car(self):
        value = self.board.values[self.i][self.j]
        if value != "_":
            return self.board.cars[value]

    def on_press(self):
        self.car = self.find_car()
        if self.car:  # If the player pressed on a car
            possible_moves = BoardLogic.possible_moves(self.car, self.board.values)
            if len(possible_moves) > 0:  # If there are moves possible
                if (self.i, self.j) == self.car.positions[-1] and 1 in possible_moves:
                    move = 1
                elif (self.i, self.j) == self.car.positions[0] and -1 in possible_moves:
                    move = -1
                else:
                    return
                new_values = BoardLogic.make_move(self.car, move, self.board.values)
                self.board.redraw(new_values)
        if BoardLogic.is_win(self.board.values):
            my_popup = WinningMessage(self.board)
            my_popup.open()

    def change_color(self, value):
        self.background_color = Constants.COLORS[value]
