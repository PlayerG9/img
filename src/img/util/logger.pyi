#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys as __sys


class Logger:
    enabled: bool
    file = __sys.stdout

    @staticmethod
    def delete_last_line(): ...

    @staticmethod
    def debug(message: str, *extra, sep: str = " ", replace: bool = False) -> None: ...

    @staticmethod
    def info(message: str, *extra, sep: str = " ", replace: bool = False) -> None: ...

    @staticmethod
    def warning(message: str, *extra, sep: str = " ", replace: bool = False) -> None: ...

    @staticmethod
    def error(message: str, *extra, sep: str = " ", replace: bool = False) -> None: ...
    

    @staticmethod
    def print(*values, sep: str = " "): ...
