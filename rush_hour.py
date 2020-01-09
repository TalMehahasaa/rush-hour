from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from helper_classes import Constants, Direction, BoardLogic, Node
from kivy.clock import Clock


class Wrapper(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = 1
        self.board = Board()
        self.add_widget(self.board)
        self.add_widget(SolveButton())


class SolveButton(Button):
    def __init__(self):
        super().__init__()
        self.pointer = None
        self.event = None

    def on_press(self):
        if not self.event:
            linked_list = BoardLogic.bfs(Node(self.parent.board.values), self.parent.board.cars_info)
            linked_list = reverse_list(linked_list)
            pointer = linked_list
            size = -1
            while pointer:
                BoardLogic.print_board(pointer.value)
                print()
                pointer = pointer.parent
                size += 1
            print(size, "moves to solve")
            self.pointer = linked_list.parent
            self.event = Clock.schedule_interval(lambda a: self.callback(), Constants.INTERVAL_TIME)
            self.text = "Stop"
        else:
            Clock.unschedule(self.event)
            self.event = None
            self.pointer = None
            self.text = "Solve"
            self.parent.board.update_cars()  # Update cars attribute for the player to be able to continue playing

    def callback(self):
        if self.pointer:
            self.parent.board.redraw(self.pointer.value)
            self.pointer = self.pointer.parent


def reverse_list(head):
    new_head = None
    while head:
        head.parent, head, new_head = new_head, head.parent, head
    return new_head


class Board(GridLayout):
    def __init__(self):
        super().__init__()
        self.cols = Constants.SIZE
        self.values = None
        self.cars_info = None
        self.cars = None
        self._create_starting_board()

        self.tiles = []
        for i in range(Constants.SIZE):
            row = []
            for j in range(Constants.SIZE):
                tile = Tile((i, j), self)
                row.append(tile)
                self.add_widget(tile)
            self.tiles.append(row)

    def _create_starting_board(self):
        self.values = BoardLogic.get_values()

        self.cars_info = BoardLogic.get_cars_info(self.values)
        self.update_cars()

    def update_cars(self):
        self.cars = dict()
        for key in self.cars_info.keys():
            self.cars[key] = Car(key, self)

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
        if self.car:
            possible_moves = BoardLogic.possible_moves(self.car, self.board.values)
            if len(possible_moves) > 0:  # If there are moves possible
                if (self.i, self.j) == self.car.positions[-1]:
                    move = 1
                elif (self.i, self.j) == self.car.positions[0]:
                    move = -1
                else:
                    move = 0
                new_values = BoardLogic.make_move(self.car, move, self.board.values)
                self.board.redraw(new_values)

    def change_color(self, value):
        self.background_color = Constants.COLORS[value]


class MyApp(App):
    def build(self):
        self.title = "Rush Hour"
        wrapper = Wrapper()
        return wrapper


if __name__ == '__main__':
    MyApp().run()
