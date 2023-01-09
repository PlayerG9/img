#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
MIT License

Copyright (c) 2023 PlayerG9

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
__version_info__ = (0, 1, 0)
__version__ = ".".join(str(_) for _ in __version_info__)

import os
import re
import urllib.parse
import requests
from .util import printProgressBar


class HTTPError404(Exception):
    pass


def img_get(url: str):
    for iurl in url_iter(url):
        try:
            download(iurl)
        except HTTPError404:
            if url == iurl:
                raise
            return


def url_iter(url: str):
    yield url

    match = list(re.finditer(r"\d+", url))[-1]
    start, stop = match.start(), match.end()
    number_string = match.group()
    str_length = len(number_string)
    number = int(number_string)

    before, after = url[:start], url[stop:]

    while True:
        number += 1
        yield f"{before}{str(number).rjust(str_length, '0')}{after}"


def download(url: str):
    print("Download", url)
    response = requests.get(url=url, timeout=(20, None), stream=True)
    if response.status_code == 404:
        raise HTTPError404()
    response.raise_for_status()

    try:
        content_size = response.headers['Content-length']
    except KeyError:
        content_size = None
    else:
        content_size = int(content_size)

    filename = get_filename(url=url, response=response)
    print(f"Writing to {filename}...")

    try:
        with open(filename, 'wb') as file:
            progress = 0
            for chunk in response.iter_content():
                file.write(chunk)
                progress += len(chunk)
                printProgressBar(progress, content_size or 1, length=70)  # terminal size is 80 so reduced to 70
    except Exception:
        if os.path.isfile(filename):
            os.remove(filename)
        raise


def get_filename(url: str, response: requests.Response):
    fn = extract_filename(url=url, response=response)
    i = 0
    name, ext = os.path.splitext(fn)
    while os.path.isfile(fn):
        i += 1
        fn = f"{name} ({i}){ext}"
    return fn


def extract_filename(url: str, response: requests.Response):
    try:
        content_disposition = response.headers['Content-Disposition']
        return re.findall("filename=(.+)", content_disposition)[0]
    except KeyError:
        parsed = urllib.parse.urlparse(url=url)
        return os.path.split(parsed.path)[1]
