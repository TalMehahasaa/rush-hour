from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from copy import deepcopy
from helper_classes import Constants, Direction, BoardLogic


class KivyBoard(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = Constants.SIZE
        self.board = Board()
        self.tiles = []
        for i in range(Constants.SIZE):
            row = []
            for j in range(Constants.SIZE):
                tile = KivyTile((i, j), self.board)
                row.append(tile)
                self.add_widget(tile)
            self.tiles.append(row)

    def redraw(self):
        for i in range(Constants.SIZE):
            for j in range(Constants.SIZE):
                self.tiles[i][j].change_color(Constants.COLORS[self.board.values[i][j]])


class Board:
    def __init__(self):
        self.values = [["_" for _ in range(Constants.SIZE)] for _ in range(Constants.SIZE)]
        self.cars = []
        self.generate_board()

        for car in self.cars:
            BoardLogic.possible_moves(car, self.values)

        BoardLogic.print_board(self.values)

    def generate_board(self):
        # TODO: Generate a random board by choosing a difficulty
        # Difficulties: Easy- 10, Medium- 30, Hard- 50, Expert- 100
        self.cars.append(Car('P', (0, 0), 3, Direction.vertical, self))
        self.cars.append(Car("B", (4, 0), 2, Direction.vertical, self))
        self.cars.append(Car("A", (0, 1), 2, Direction.horizontal, self))
        self.cars.append(Car("X", (2, 1), 2, Direction.horizontal, self))
        self.cars.append(Car("C", (4, 1), 2, Direction.horizontal, self))
        self.cars.append(Car("Q", (1, 3), 3, Direction.vertical, self))
        self.cars.append(Car("R", (5, 2), 3, Direction.horizontal, self))
        self.cars.append(Car("O", (3, 5), 3, Direction.vertical, self))


class Car:
    def __init__(self, value, pos, length, direction, board):
        self.value = value
        self.direction = direction
        self.length = length
        self.board = board
        self.positions = self._find_positions(pos)

        self.put_values_in_board()

    def _find_positions(self, pos):
        positions = []
        for offset in range(self.length):
            if self.direction == Direction.horizontal:
                positions.append((pos[0], pos[1] + offset))
            else:
                positions.append((pos[0] + offset, pos[1]))
        return positions

    def put_values_in_board(self):
        for pos in self.positions:
            self.board.values[pos[0]][pos[1]] = self.value


class KivyTile(Button):
    def __init__(self, position, board):
        super().__init__()
        self.position = position
        self.board = board
        self.background_color = Constants.COLORS[self.board.values[self.position[0]][self.position[1]]]

    def on_press(self):
        for car in self.board.cars:
            if self.position in car.positions:
                possible_moves = BoardLogic.possible_moves(car, self.board.values)
                if len(possible_moves):
                    if self.position == car.positions[-1]:
                        move = 1
                    elif self.position == car.positions[0]:
                        move = -1
                    else:
                        move = 0

                    next_board = BoardLogic.change_board(car, move, self.board.values)
                    if next_board:
                        self.board.values = next_board
                        self.parent.redraw()

    def change_color(self, new_color):
        self.background_color = new_color


class MyApp(App):
    def build(self):
        self.title = "Rush Hour"
        return KivyBoard()


if __name__ == '__main__':
    MyApp().run()
