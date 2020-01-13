from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from board_logic import BoardLogic
from helper_classes import Constants, Direction, Node


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
        self.current_board = None  # The board being displayed on the screen
        self.event = None  # The animation object. Used to start/ stop the animation
        self.text = "Solve"

    def on_press(self):
        if self.text == "Solve":  # If the player clicked Solve
            winning_path = self.get_winning_path()  # Solve the board and get the shortest solution linked list

            number_of_moves_to_solve = length_of_linked_list(winning_path)
            print(number_of_moves_to_solve, "moves to solve")  # Print the number of moves of the solution

            self.current_board = winning_path.parent
            self.event = Clock.schedule_interval(self.callback, Constants.INTERVAL_TIME)  # Start the animation

            self.text = "Stop"

        else:  # If the player clicked Stop
            Clock.unschedule(self.event)
            self.current_board = None

            self.parent.board.update_cars()  # Update cars attribute for the player to be able to continue playing
            self.text = "Solve"

    def callback(self, dt):
        if self.current_board:
            self.parent.board.redraw(self.current_board.value)
            self.current_board = self.current_board.parent
        else:  # The board is solved
            Clock.unschedule(self.event)  # Stop the animation
            self.parent.board.update_cars()  # Update cars attribute for the player to be able to continue playing
            # TODO: Make the car exit
            self.text = "Done"

    def get_winning_path(self):
        current_board = Node(self.parent.board.values)
        cars_info = self.parent.board.cars_info
        path_to_solve = reverse_list(
            BoardLogic.bfs(current_board, cars_info)
        )  # A linked list of the boards leading to a winning solution
        return path_to_solve


def reverse_list(head):
    new_head = None
    while head:
        head.parent, head, new_head = new_head, head.parent, head
    return new_head


def length_of_linked_list(linked_list):
    counter = 0
    pointer = linked_list.parent
    while pointer:
        counter += 1
        pointer = pointer.parent
    return counter


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
