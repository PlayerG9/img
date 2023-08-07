#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import re
import shlex
import sys
import requests
import urllib.parse as urlparse
from ..logger import Logger, Waiting
from ..downloader import Downloader, DownloadPool
from ..util.responses import is_image_type


class ImageGrabber:
    # def __init__(self, url: str, overwrite: bool, skips: int, formats: t.List[str], history: bool):
    def __init__(self, url: str, skips: int, history: bool):
        self.url = url
        # self.overwrite = overwrite
        self.skips = skips
        # self.formats = formats
        self.history = history
        self.attempted = 0
        self.downloaded = 0

    def run(self):
        tries = 0
        try:
            with Logger(), DownloadPool() as pool:
                for url in self.iter_urls():
                    self.attempted += 1

                    response = requests.get(url=url, timeout=(20, None), stream=True)
                    if not is_image_type(response):
                        if tries < self.skips:
                            tries += 1
                            continue
                        break
                    downloader = Downloader(response)
                    Logger.print(downloader)

                    if response.status_code == 404:
                        if tries < self.skips:
                            tries += 1
                            continue
                        if self.history:
                            self.add_to_history(url)
                        break
                    response.raise_for_status()

                    tries = 0
                    self.downloaded += 1

                    pool.submit(downloader.download)

                Logger.print(Waiting())
            Logger.undo_last_line()
        except KeyboardInterrupt:
            pass
        print(f"Found and downloaded {self.downloaded} images")

    def prepare_url(self) -> str:
        # already prepared
        if re.search(r"\{\d+}", self.url) is not None:
            return self.url

        parsed = urlparse.urlparse(self.url)
        matches = list(re.finditer(r"\d+", parsed.path))
        if not matches:
            print("Failed to identify increment in provided url")
            sys.exit(1)
        match = matches[-1]
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
        r"""
        maybe use readline instead of custom implementation
        """
        return  # not implemented yet
        url_index = sys.argv.index(self.url)
        arguments = sys.argv.copy()
        arguments[url_index] = new_url
        with open(os.path.expanduser("~/.bash_history"), 'a') as history:
            history.write(f"{shlex.join(arguments)}\n")
