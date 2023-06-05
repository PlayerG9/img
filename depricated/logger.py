#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import functools
import sys
from src.img.logger.coloring import colored, COLOR


class Logger:
    enabled: bool = True
    file = sys.stdout

    @classmethod
    def delete_last_line(cls):
        # attempt one
        # print(f"\033[A{' ' * self.terminal_width()}\033[A")

        # attempt two
        cls.file.write('\x1b[1A')  # cursor up one line
        cls.file.write('\x1b[2K')  # delete last line

    @classmethod
    def _wrap(cls, func):
        @functools.wraps
        def wrapped(*args, **kwargs):
            if not cls.enabled:
                return
            replace = kwargs.pop('replace')
            if replace:
                cls.delete_last_line()
            func(*args, **kwargs)

        return wrapped

    @classmethod
    @_wrap
    def debug(cls, message, *extra, sep=" "):
        cls.print(colored(message, COLOR.grey), *extra, sep=sep)

    @classmethod
    @_wrap
    def info(cls, message, *extra, sep=" "):
        cls.print(message, *extra, sep=sep)

    @classmethod
    @_wrap
    def success(cls, message, *extra, sep=" "):
        cls.print(colored(message, COLOR.green), *extra, sep=sep)

    @classmethod
    @_wrap
    def warning(cls, message, *extra, sep=" "):
        cls.print(colored(message, COLOR.yellow), *extra, sep=sep)

    @classmethod
    @_wrap
    def error(cls, message, *extra, sep=" "):
        cls.print(colored(message, COLOR.red), *extra, sep=sep)

    @classmethod
    def print(cls, *values, sep=" "):
        print(*values, sep=sep, file=cls.file)
