#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
see here for the basis:
https://github.com/pollev/python_progress_bar#readme
https://github.com/pollev/python_progress_bar/blob/master/python_progress_bar/progress_bar.py
but it's heavily modified
"""
import curses
import shutil
import time


# Constants
CODE_SAVE_CURSOR = "\033[s"
CODE_RESTORE_CURSOR = "\033[u"
CODE_CURSOR_IN_SCROLL_AREA = "\033[1A"
COLOR_FG = '\033[30m'
COLOR_BG = '\033[42m'
COLOR_BG_BLOCKED = '\033[43m'
RESTORE_FG = '\033[39m'
RESTORE_BG = '\033[49m'


class ProgressBar:
    _current_nr_lines: int = 0
    _start_time: float = 0
    _statistics: bool = True
    _progress: float = None
    _blocking: bool = False

    @staticmethod
    def get_current_nr_lines():
        return shutil.get_terminal_size((80, 20)).lines

    @staticmethod
    def get_current_nr_cols():
        return shutil.get_terminal_size((80, 20)).columns

    def __init__(self, statistics: bool):
        self._statistics = statistics

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value: float):
        self._progress = value

    def __enter__(self):
        self.setup()
        return self

    def setup(self):
        # Setup curses support (to get information about the terminal we are running in)
        curses.setupterm()

        self._current_nr_lines = self.get_current_nr_lines()
        lines = self._current_nr_lines - 1

        # Scroll down a bit to avoid visual glitch when the screen area shrinks by one row
        self._send_code("\n")

        # Save cursor
        self._send_code(CODE_SAVE_CURSOR)
        # Set scroll region (this will place the cursor in the top left)
        self._send_code("\033[0;" + str(lines) + "r")

        # Restore cursor but ensure it's inside the scrolling area
        self._send_code(CODE_RESTORE_CURSOR)
        self._send_code(CODE_CURSOR_IN_SCROLL_AREA)

        # Start empty progress bar
        self._progress = 0.0

        # Setup start time
        self._start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def shutdown(self):
        lines = self.get_current_nr_lines()
        # Save cursor
        self._send_code(CODE_SAVE_CURSOR)
        # Set scroll region (this will place the cursor in the top left)
        self._send_code("\033[0;" + str(lines) + "r")
    
        # Restore cursor but ensure it's inside the scrolling area
        self._send_code(CODE_RESTORE_CURSOR)
        self._send_code(CODE_CURSOR_IN_SCROLL_AREA)
    
        # We are done so clear the scroll bar
        self._clear_progress_bar()
    
        # Scroll down a bit to avoid visual glitch when the screen area grows by one row
        self._send_code("\n\n")

    def blocking(self):
        self._blocking = True

    def resume(self):
        self._blocking = False

    @staticmethod
    def _send_code(code: str):
        print(code, end='')

    @staticmethod
    def _format_interval(t):
        h_m, s = divmod(int(t), 60)
        h, m = divmod(h_m, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        else:
            return f"{m:02d}:{s:02d}"

    def _clrscr(self):
        self._send_code(curses.tparm(curses.tigetstr("el")).decode())

    def _clear_progress_bar(self):
        lines = self.get_current_nr_lines()
        # Save cursor
        self._send_code(CODE_SAVE_CURSOR)

        # Move cursor position to last row
        self._send_code("\033[" + str(lines) + ";0f")

        # clear progress bar
        self._clrscr()

        # Restore cursor position
        self._send_code(CODE_RESTORE_CURSOR)

    def _draw_progress_bar(self, percentage):
        lines = self.get_current_nr_lines()

        if lines != self._current_nr_lines:
            self.setup()

        # Save cursor
        self._send_code(CODE_SAVE_CURSOR)

        # Move cursor position to last row
        self._send_code("\033[" + str(lines) + ";0f")

        # Clear progress bar
        self._clrscr()

        # Draw progress bar
        self._send_code(percentage)

        # Restore cursor position
        self._send_code(CODE_RESTORE_CURSOR)

    def _block_progress_bar(self, percentage):
        lines = self.get_current_nr_lines()
        # Save cursor
        self._send_code(CODE_SAVE_CURSOR)

        # Move cursor position to last row
        self._send_code("\033[" + str(lines) + ";0f")

        # Clear progress bar
        self._clrscr()

        # Draw progress bar
        self.blocking()
        self._send_code(percentage)

        # Restore cursor position
        self._send_code(CODE_RESTORE_CURSOR)

    def __print_bar_text(self, percentage):
        color = f"{COLOR_FG}{COLOR_BG}"
        if self._blocking:
            color = f"{COLOR_FG}{COLOR_BG_BLOCKED}"

        cols = self.get_current_nr_cols()
        if self._statistics:
            # Create right side of progress bar with statistics
            r_bar = self._prepare_r_bar(percentage)
            bar_size = cols - 18 - len(r_bar)
        else:
            r_bar = ""
            bar_size = cols - 17

        # Prepare progress bar
        complete_size = (bar_size * percentage) / 100
        remainder_size = bar_size - complete_size
        progress_bar = f"[{color}{'█' * int(complete_size)}{RESTORE_FG}{RESTORE_BG}{'.' * int(remainder_size)}]"

        # Print progress bar
        self._send_code(f" Progress {percentage}% {progress_bar} {r_bar}\r")

    def _prepare_r_bar(self, n):
        elapsed = time.time() - self._start_time
        elapsed_str = self._format_interval(elapsed)

        # Percentage/second rate (or second/percentage if slow)
        rate = n / elapsed
        inv_rate = 1 / rate if rate else None
        rate_noinv_fmt = f"{f'{rate:5.2f}' if rate else '?'}pct/s"
        rate_inv_fmt = f"{f'{inv_rate:5.2f}' if inv_rate else '?'}s/pct"
        rate_fmt = rate_inv_fmt if inv_rate and inv_rate > 1 else rate_noinv_fmt

        # Remaining time
        remaining = (100 - n) / rate if rate else 0
        remaining_str = self._format_interval(remaining) if rate else "?"

        r_bar = f"[{elapsed_str}<{remaining_str}, {rate_fmt}]"
        return r_bar
