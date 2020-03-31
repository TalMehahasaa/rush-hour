from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from board_logic import BoardLogic
from helper_classes import *


class CustomButton(Button):
    pass


class WinningMessage(Popup):
    def __init__(self, board, **kwargs):
        super().__init__(**kwargs)
        self.board = board


class RestartButton(CustomButton):
    def on_press(self):
        board = self.parent.parent.children[1]
        board.restart()
        self.parent.children[1].stop_animation()


class SolveButton(CustomButton):
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

            self.current_node = winning_path.next
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
            self.current_node = self.current_node.next
        else:  # The board is solved
            self.stop_animation()
            WinningMessage(self.board).open()

    def _get_winning_path(self):
        current_board = Node(self.board.values)
        cars_info = self.board.cars_info
        path_to_solve = reverse_list(
            BoardLogic.bfs(current_board, cars_info)
        )  # A linked list of the boards leading to a winning solution
        return path_to_solve
