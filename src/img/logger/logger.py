#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import time
import threading
from .codes import Codes


class Logger:
    lines = []
    max_update = 25  # maximum number of entries to update
    interval = 0.5
    _last_size = 0
    _auto_updating = False
    _thread: threading.Thread = None

    @classmethod
    def __enter__(cls):
        cls._auto_updating = True
        cls._thread = threading.Thread(target=cls._background_updater)
        cls._thread.start()

    @classmethod
    def __exit__(cls, exc_type, exc_val, exc_tb):
        cls._auto_updating = False
        cls._thread.join(cls.interval * 10)
        cls.update()  # dunno how helpful
        cls.reset()

    @classmethod
    def _background_updater(cls):
        while cls._auto_updating:
            cls.update()
            time.sleep(cls.interval)

    @classmethod
    def print(cls, value):
        cls.lines.append(value)
        if not cls._auto_updating:
            cls.update()

    @classmethod
    def reset(cls):
        cls.lines.clear()

    @classmethod
    def undo_last_line(cls):
        cls._send(Codes.MOVE_CURSOR_UP)
        cls._send(Codes.DELETE_LINE)

    @classmethod
    def update(cls):
        diff = len(cls.lines) - cls._last_size
        cls._send(Codes.MOVE_CURSOR_UP * min(cls.max_update - diff, cls._last_size))
        for value in cls.lines[-cls.max_update:]:
            if value.__class__.__module__ == '__builtin__':
                cls._send(Codes.MOVE_CURSOR_DOWN)  # eq to \n
                continue
            cls._send(Codes.DELETE_LINE)
            try:
                value = str(value)
            except Exception as exc:
                value = f"{type(exc).__name__}: {exc}"
            print(value, flush=False)
        cls._last_size = len(cls.lines)
        sys.stdout.flush()

    @staticmethod
    def _send(code: str):
        sys.stdout.write(code)
