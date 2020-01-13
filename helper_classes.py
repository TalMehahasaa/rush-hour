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

    BOARDS = [
        "__ABBP __A_CP _XX_CP QDERRR QDEFGG QHHFII".split(),
        "ABCCPD AB_EPD XXFEPG __FQ_G __HQ__ __HQII".split(),
    ]

    INTERVAL_TIME = .07


class Direction(Enum):
    horizontal = 0
    vertical = 1


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
