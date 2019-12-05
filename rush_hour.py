from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from helper_classes import Constants, Direction, BoardLogic


class KivyBoard(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = Constants.SIZE
        self.values = None
        self.cars_info = None
        self._create_starting_board()

        self.tiles = []
        for i in range(Constants.SIZE):
            row = []
            for j in range(Constants.SIZE):
                tile = KivyTile((i, j), self)
                row.append(tile)
                self.add_widget(tile)
            self.tiles.append(row)

    def _create_starting_board(self):
        self.values = [
            ["_"] * 4,
            ["X", "X", "_", "A"],
            ["B", "_", "_", "A"],
            ["B", "P", "P", "P"]
        ]
        self.cars_info = {
            "X": (Direction.horizontal, 2),
            "A": (Direction.vertical, 2),
            "B": (Direction.vertical, 2),
            "P": (Direction.horizontal, 3)
        }

        self.cars = {
            "X": Car("X", self),
            "A": Car("A", self),
            "B": Car("B", self),
            "P": Car("P", self),
        }

    def make_move(self, car, move):
        if move in BoardLogic.possible_moves(car, self.values):  # If the move is valid
            new_positions = []
            for i, j in car.positions:
                if car.direction == Direction.vertical:
                    new_positions.append((i + move, j))
                else:
                    new_positions.append((i, j + move))

            new_values = self.values

            for i, j in car.positions:  # Remove previous car position
                new_values[i][j] = "_"

            for i, j in new_positions:  # Put car in it's new position
                new_values[i][j] = car.value

            car.positions = new_positions
            self.values = new_values

    def redraw(self, new_values):
        self.values = new_values
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.tiles[i][j].change_color(value)


class Car:
    def __init__(self, value, kivy_board):
        self.value = value
        self.kivy_board = kivy_board
        self.positions = BoardLogic.find_car_positions(self.value, self.kivy_board.values)
        self.direction, self.length = self.kivy_board.cars_info[self.value]


class KivyTile(Button):
    def __init__(self, position, kivy_board):
        super().__init__()
        self.i, self.j = position
        self.kivy_board = kivy_board
        self.car = self.find_car()  # Find the car that the tile is on
        self.background_color = Constants.COLORS[self.car.value if self.car else "_"]

    def find_car(self):
        value = self.kivy_board.values[self.i][self.j]
        if value != "_":
            return self.kivy_board.cars[value]

    def on_press(self):
        self.car = self.find_car()
        if self.car:
            possible_moves = BoardLogic.possible_moves(self.car, self.kivy_board.values)
            if len(possible_moves) > 0:  # If there are moves possible
                if (self.i, self.j) == self.car.positions[-1]:
                    move = 1
                elif (self.i, self.j) == self.car.positions[0]:
                    move = -1
                else:
                    move = 0
                new_values = BoardLogic.make_move(self.car, move, self.kivy_board.values)
                self.kivy_board.redraw(new_values)

        # print("*************")
        # BoardLogic.print_board(self.kivy_board.values)
        # print("*************\n")
        # next_boards = BoardLogic.next_boards(self.kivy_board.values, self.kivy_board.cars_info)
        # for index, board in enumerate(next_boards):
        #     print("Next board #", index + 1)
        #     BoardLogic.print_board(board)
        #     print()

    def change_color(self, value):
        self.background_color = Constants.COLORS[value]


class MyApp(App):
    def build(self):
        self.title = "Rush Hour"
        return KivyBoard()


if __name__ == '__main__':
    MyApp().run()
