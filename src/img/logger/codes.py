#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""


class Codes:
    RESET = "\033[0m"

    ATTR_BOLD = "\033[1m"
    ATTR_NO_BOLD = "\033[21m"
    ATTR_DARK = "\033[2m"
    ATTR_NO_DARK = "\033[22m"
    ATTR_UNDERLINE = "\033[4m"
    ATTR_NO_UNDERLINE = "\033[24m"
    ATTR_BLINK = "\033[5m"
    ATTR_NO_BLINK = "\033[25m"
    ATTR_REVERSE = "\033[7m"
    ATTR_NO_REVERSE = "\033[27m"
    ATTR_CONCEALED = "\033[8m"
    ATTR_REVEALED = "\033[28m"

    BG_BLACK = "\033[40m"
    BG_GREY = "\033[0m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_LIGHT_GREY = "\033[47m"
    BG_DARK_GREY = "\033[100m"
    BG_LIGHT_RED = "\033[101m"
    BG_LIGHT_GREEN = "\033[102m"
    BG_LIGHT_YELLOW = "\033[103m"
    BG_LIGHT_BLUE = "\033[104m"
    BG_LIGHT_MAGENTA = "\033[105m"
    BG_LIGHT_CYAN = "\033[106m"
    BG_WHITE = "\033[107m"

    FG_BLACK = "\033[30m"
    FG_GREY = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_YELLOW = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_LIGHT_GREY = "\033[37m"
    FG_DARK_GREY = "\033[90m"
    FG_LIGHT_RED = "\033[91m"
    FG_LIGHT_GREEN = "\033[92m"
    FG_LIGHT_YELLOW = "\033[93m"
    FG_LIGHT_BLUE = "\033[94m"
    FG_LIGHT_MAGENTA = "\033[95m"
    FG_LIGHT_CYAN = "\033[96m"
    FG_WHITE = "\033[97m"

    MOVE_CURSOR_UP = '\033[1A'
    MOVE_CURSOR_DOWN = '\033[1B'
    MOVE_CURSOR_FORWARD = '\033[1C'
    MOVE_CURSOR_BACKWARD = '\033[1D'
    MOVE_CURSOR_PREV_LINE = '\033[1F'
    MOVE_CURSOR_NEXT_LINE = '\033[1E'
    DELETE_LINE = '\033[2K'

    SCROLL_UP = "\033[1S"
    SCROLL_DOWN = "\033[1T"

    SHOW_CURSOR = "\033[?25h"
    HIDE_CURSOR = "\033[?25l"

    SAVE_CURSOR = "\033[s"
    RESTORE_CURSOR = "\033[u"
    CURSOR_IN_SCROLL_AREA = "\033[1A"
    RESTORE_FG = "\033[39m"
    RESTORE_BG = "\033[49m"
