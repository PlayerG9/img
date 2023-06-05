#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
from concurrent.futures import ThreadPoolExecutor
import requests


class Downloader:
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1))

    def __enter__(self):
        self.pool.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.__exit__(exc_type, exc_val, exc_tb)

    def continue_download(self, response: requests.Response):
        self.pool.submit(self._download, response)

    def _download(self, response: requests.Response):
        pass
