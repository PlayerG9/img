#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
see here for the basis:
https://github.com/termcolor/termcolor#readme
https://github.com/termcolor/termcolor/blob/main/src/termcolor/termcolor.py
but it's slightly modified
"""
import functools
import typing as t


class ATTRIBUTE:
    bold = 1
    dark = 2
    underline = 4
    blink = 5
    reverse = 7
    concealed = 8


class BACKGROUND:
    on_black = 40
    on_grey = 0  # Actually black but kept for backwards compatibility
    on_red = 41
    on_green = 42
    on_yellow = 43
    on_blue = 44
    on_magenta = 45
    on_cyan = 46
    on_light_grey = 47
    on_dark_grey = 100
    on_light_red = 101
    on_light_green = 102
    on_light_yellow = 103
    on_light_blue = 104
    on_light_magenta = 105
    on_light_cyan = 106
    on_white = 107


class COLOR:
    black = 30
    grey = 30  # Actually black but kept for backwards compatibility
    red = 31
    green = 32
    yellow = 33
    blue = 34
    magenta = 35
    cyan = 36
    light_grey = 37
    dark_grey = 90
    light_red = 91
    light_green = 92
    light_yellow = 93
    light_blue = 94
    light_magenta = 95
    light_cyan = 96
    white = 97


RESET = "\033[0m"


@functools.cache
def _can_do_color():
    import sys, os
    return (
        hasattr(sys.stdout, "isatty")
        and sys.stdout.isatty()
        and os.environ.get("TERM") != "dumb"
    )


def colored(
    text: str,
    color: str | None = None,
    background: str | None = None,
    attrs: t.Iterable[str] | None = None,
) -> str:
    """Colorize text.
    Available text colors:
        black, red, green, yellow, blue, magenta, cyan, white,
        light_grey, dark_grey, light_red, light_green, light_yellow, light_blue,
        light_magenta, light_cyan.
    Available text highlights:
        on_black, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan, on_white,
        on_light_grey, on_dark_grey, on_light_red, on_light_green, on_light_yellow,
        on_light_blue, on_light_magenta, on_light_cyan.
    Available attributes:
        bold, dark, underline, blink, reverse, concealed.
    Example:
        colored('Hello, World!', 'red', 'on_black', ['bold', 'blink'])
        colored('Hello, World!', 'green')
    """
    if not _can_do_color():
        return text

    fmt_str = "\033[%dm%s"

    if color is not None:
        text = fmt_str % (getattr(COLOR, color), text)

    if background is not None:
        text = fmt_str % (getattr(BACKGROUND, background), text)

    if attrs is not None:
        for attr in attrs:
            text = fmt_str % (getattr(ATTRIBUTE, attr), text)

    return text + RESET
