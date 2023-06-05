#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import re
import time

import sys
import requests
import subprocess
import typing as t
import urllib.parse as urlparse
from concurrent.futures import ThreadPoolExecutor
from ..logger import Logger, Waiting
from ..downloader import Downloader


class ImageGrabber:
    def __init__(self, url: str, overwrite: bool, skips: int, formats: t.List[str], history: bool):
        self.url = url
        self.overwrite = overwrite
        self.skips = skips
        self.formats = formats
        self.history = history
        self.attempted = 0
        self.downloaded = 0

    def run(self):
        tries = 0
        max_workers = min(8, os.cpu_count())
        active = 0
        with (Logger(), ThreadPoolExecutor(max_workers) as pool):
            for url in self.iter_urls():
                self.attempted += 1

                response = requests.get(url=url, timeout=(20, None), stream=True)
                downloader = Downloader(response)
                Logger.print(downloader)

                if response.status_code == 404:
                    if tries < self.skips:
                        tries += 1
                        continue
                    break
                response.raise_for_status()

                tries = 0
                self.downloaded += 1
                active += 1

                def download():
                    nonlocal active
                    downloader.download()
                    active -= 1

                pool.submit(download)

                while active >= max_workers:
                    time.sleep(0.01)

            Logger.print(Waiting())
            Logger.print(f"Exc-hook {sys.excepthook}")
        Logger.undo_last_line()
        print(f"Found and downloaded {self.downloaded} images")

    def prepare_url(self) -> str:
        # already prepared
        if re.search(r"\{\d+}", self.url) is not None:
            return self.url

        parsed = urlparse.urlparse(self.url)
        match = list(re.finditer(r"\d+", parsed.path))[-1]
        start, num_str, stop = match.start(), match.group(), match.end()
        return urlparse.urlunparse(
            parsed._replace(path=f"{parsed.path[:start]}{{{num_str}}}{parsed.path[stop:]}")
        )

    def iter_urls(self):
        basis = self.prepare_url()

        def repl(match: re.Match) -> str:
            num_str = match.group(1)
            return str(int(num_str) + i).rjust(len(num_str), "0")

        i = 0

        while True:
            yield re.sub(r"\{(\d+)}", repl, basis)
            i += 1

    def add_to_history(self, new_url: str):
        url_index = sys.argv.index(self.url)
        arguments = sys.argv.copy()
        arguments[url_index] = new_url
        subprocess.check_call(["history", "-s", *arguments])
