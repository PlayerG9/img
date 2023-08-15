#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import time
from concurrent.futures import ThreadPoolExecutor


class DownloadPool:
    def __init__(self, max_workers: int = None):
        self._max_workers = max_workers or min(4, os.cpu_count())
        self._active = 0
        self._pool = ThreadPoolExecutor(max_workers=self._max_workers)

    def __enter__(self):
        self._pool.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._pool.__exit__(exc_type, exc_val, exc_tb)

    def submit(self, download_func):
        def inner():
            self._active += 1
            try:
                return download_func()
            finally:
                self._active -= 1

        self._pool.submit(inner)

        while self._active >= self._max_workers:
            time.sleep(0.01)
