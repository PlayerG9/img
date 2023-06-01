#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
import sys

import requests
import subprocess
import typing as t
import urllib.parse as urlparse
from ..util.coloring import colored, COLOR
from ..util.responses import extract_content_size, extract_filename


CHUNK_SIZE = 1024 * 100  # 100 kB
# CHUNK_SIZE = 1024  # 1 kB


class HTTPError404(Exception):
    pass


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
        raise NotImplementedError()

    def iter_urls(self) -> t.Iterator[str]:
        parsed = urlparse.urlparse(self.url)
        urlpath = parsed.path

        match = list(re.finditer(r"\d+", urlpath))[-1]
        start, stop = match.start(), match.end()
        number_string = match.group()
        digits_length = len(number_string)
        number = int(number_string)

        before, after = urlpath[:start], urlpath[stop:]

        while True:
            yield urlparse.urlunparse(
                parsed._replace(path=f"{before}{str(number).rjust(digits_length, '0')}{after}")
            )
            number += 1

    def download(self, url: str):
        print("Attempt:", url, "   ", end="\r")
        try:
            response = requests.get(url=url, timeout=(20, None), stream=True)
            if response.status_code == 404:
                raise HTTPError404()
            response.raise_for_status()
        except HTTPError404:
            print(colored("Not Found:", COLOR.red), url, "")
            raise
        except Exception:
            print(colored("Failed:", COLOR.red), url, "   ")
            raise
        else:
            print(colored("Download:", COLOR.green), url, " ")

    def add_to_history(self, new_url: str):
        url_index = sys.argv.index(self.url)
        arguments = sys.argv.copy()
        arguments[url_index] = new_url
        subprocess.run(["history", "-s", *arguments])
