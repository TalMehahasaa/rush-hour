from enum import Enum


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
        "G": (.05, .05, .2, 1),
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

    # TODO: Have multiple boards for each difficulty
    BOARDS = [
        "__ABBP __A_CP _XX_CP QDERRR QDEFGG QHHFII".split(),
        "ABCCPD AB_EPD XXFEPG __FQ_G __HQ__ __HQII".split(),
    ]

    INTERVAL_TIME = .1


class Direction(Enum):
    horizontal = 0
    vertical = 1


class Difficulty(Enum):
    easy = 0
    medium = 1
    hard = 2


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent


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


def print_board(values):
    for row in values:
        for value in row:
            print(value, end=" ")
        print()
