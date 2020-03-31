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

    BEGINNER_BOARDS = [
        "AA___P Q__R_P QXXR_P Q__R__ B___CC B_OOO_".split(),
        "O__P__ O__P__ OXXP__ __AQQQ __A__B __RRRB".split(),
        "_ABBCD _A_ECD _XXE_F __GG_F ___H__ ___H__".split(),
    ]

    INTERMEDIATE_BOARDS = [
        "ABB__O A_P__O XXP__O __PQQQ ____C_ RRR_C_".split(),
        "AABO__ CCBO__ PXXO__ PQQQ__ PDD___ RRR___".split(),
        "__ABB_ __A_C_ _DXXC_ _DEEF_ _OOOF_ ______".split(),
        "A__OOO ABBC__ XXDC_P __D__P __EFFP __EQQQ".split(),  # EASY?
        "OAAP__ O__P__ OXXP__ __BQQQ __B__C __RRRC".split(),
        "_AABB_ CCDDOP QRXXOP QREFOP QREFGG _HHII_".split(),
    ]

    ADVANCED_BOARDS = [
        "__ABBP __A_CP _XX_CP QDERRR QDEFGG QHHFII".split(),
        "AABO__ P_BO__ PXXO__ PQQQ__ ______ ___RRR".split(),
        "__AOOO B_APCC BXXP__ _D_PEE FDGG_H FQQQ_H".split(),
        "__OOOP __ABBP __AXXP __CDEE __CDFF __QQQ_".split(),
        "__ABB_ _CA___ DCXXE_ DFF_E_ OOO_G_ HH__G_".split(),
    ]

    EXPERT_BOARDS = [
        # "AA_OOO ___BCC DXXB_P D_QEEP FFQ__P __QRRR".split(),
        "OAA_B_ OCD_BP OCDXXP QQQE_P __FEGG HHFII_".split(),
    ]

    INTERVAL_TIME = .1


class Direction(Enum):
    horizontal = 0
    vertical = 1


class Difficulty(Enum):
    beginner = 0
    intermediate = 1
    advanced = 2
    expert = 3


class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next


def reverse_list(linked_list):
    """
    Creates a new linked list with a reversed order of the one inputted
    :param Node linked_list: node
    :return Node: reversed node
    """
    new_list = None
    while linked_list:
        linked_list.next, linked_list, new_list = new_list, linked_list.next, linked_list
    return new_list


def length_of_linked_list(linked_list):
    """
    Finds the length of a linked list
    :param Node linked_list: node
    :return int: length
    """
    length = 0
    pointer = linked_list.next
    while pointer:
        length += 1
        pointer = pointer.next
    return length
