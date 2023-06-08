#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import os.path as p
import time
import threading
import requests
from shutil import get_terminal_size
from ..util.responses import extract_content_size, get_free_filename
from ..logger.codes import Codes


class Downloader:
    def __init__(self, response: requests.Response):
        self.response: requests.Response = response
        self.complete: bool = False
        self.cached: int = 0
        self.content_size: int | None = None
        self.filename: str | None = None
        self._start_time = None
        self._error: BaseException | None = None

    def background_download(self):
        if self.response.ok:
            threading.Thread(target=self.download).start()

    def download(self):
        if not self.response.ok:
            return
        self.content_size = extract_content_size(self.response)
        self.filename = get_free_filename(self.response)
        tmp_file = f".{self.filename}"
        self._start_time = time.time()
        try:
            with open(tmp_file, 'wb') as file:
                for chunk in self.response.iter_content(1024*512):
                    file.write(chunk)
                    self.cached += len(chunk)
        except BaseException as exception:
            if p.isfile(tmp_file):
                os.remove(tmp_file)
            self._error = exception
            raise exception
        else:
            os.rename(tmp_file, self.filename)
            self.complete = True

    def __str__(self):
        if self._error:
            return f"{Codes.FG_RED}{self._error.__class__.__name__}:{Codes.RESTORE_FG} {str(self._error)}"
        terminal_width = get_terminal_size()[0]
        # failed
        if not self.response.ok:
            shortened = self.response.url[-(terminal_width-4):]
            return f"{Codes.FG_RED}{self.response.status_code}{Codes.RESTORE_FG} " \
                   f"{Codes.FG_GREY}{shortened}{Codes.RESTORE_FG}"
        # success
        status = f"{Codes.FG_LIGHT_GREEN}{self.response.status_code}{Codes.RESTORE_FG}"
        if self.complete:  # completed
            return f"{status} {self.filename}"
        if self.content_size is None:  # unknown content-size
            return f"{status} {self.cached / 1024}kb"
        # progress
        percent = self.cached / self.content_size
        stats = self._get_stats(percent)
        if (len(self.filename) + 40) < terminal_width:
            bar_width = min(100, terminal_width - 11 - len(stats) - len(self.filename))
            bar = self._get_progress_bar(bar_width, percent)
            return f"{status} {self.filename} {bar} {percent * 100:3.0f}% {stats}"
        else:
            bar_width = min(100, terminal_width - 10 - len(stats))
            bar = self._get_progress_bar(bar_width, percent)
            return f"{status} {bar} {percent * 100:3.0f}% {stats}"

    @staticmethod
    def _get_progress_bar(width: int, percent: float):
        bar_fill = round(percent * width)
        return f"{Codes.FG_LIGHT_CYAN}{'━' * bar_fill}" \
               f"{Codes.FG_GREY}{'━' * (width - bar_fill)}" \
               f"{Codes.RESTORE_FG}{Codes.RESTORE_BG}"

    def _get_stats(self, percent):
        elapsed = time.time() - self._start_time
        elapsed_str = self._format_interval(elapsed)

        rate = percent / elapsed
        remaining = (1 - percent) / rate if rate else 0
        remaining_str = self._format_interval(remaining) if rate else "--:--"

        return f"[{elapsed_str}<{remaining_str}]"

    @staticmethod
    def _format_interval(t):
        h_m, s = divmod(int(t), 60)
        h, m = divmod(h_m, 60)
        if h:
            return f"{h:d}:{m:02d}:{s:02d}"
        else:
            return f"{m:02d}:{s:02d}"
