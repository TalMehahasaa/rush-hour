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
                tile = KivyTile((i, j), self.cars_info, self)
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

    def redraw(self, new_values):
        self.values = new_values
        for i, row in enumerate(self.values):
            for j, value in enumerate(row):
                self.tiles[i][j].change_color(value)


class KivyTile(Button):
    def __init__(self, position, cars_info, kivy_board):
        super().__init__()
        self.i, self.j = position
        self.kivy_board = kivy_board
        self.car_value = self.kivy_board.values[self.i][self.j]  # The value of the car that the tile is on
        self.background_color = Constants.COLORS[self.car_value]
        self.cars_info = cars_info

    def on_press(self):
        car_positions = BoardLogic.find_car_positions(self.car_value, self.kivy_board.values)
        possible_moves = BoardLogic.possible_moves(self.car_value, self.kivy_board.values, self.cars_info)
        if len(possible_moves) > 0:  # If there are moves possible
            if (self.i, self.j) == car_positions[-1]:
                move = 1
            elif (self.i, self.j) == car_positions[0]:
                move = -1
            else:
                move = 0
            new_values = BoardLogic.make_move(self.car_value, move, self.kivy_board.values, self.cars_info)
            self.kivy_board.redraw(new_values)

    def change_color(self, value):
        self.background_color = Constants.COLORS[value]


class MyApp(App):
    def build(self):
        self.title = "Rush Hour"
        return KivyBoard()


if __name__ == '__main__':
    MyApp().run()
