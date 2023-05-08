#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""

import os
import re
import sys
import urllib.parse
import requests
from img.util.progress_bar import ProgressBar
from img.util.coloring import colored


CHUNK_SIZE = 1024 * 100  # 100 kB
# CHUNK_SIZE = 1024  # 1 kB


class HTTPError404(Exception):
    pass


def img_get(url: str):
    failed_once = False

    for curl in url_iter(url):
        try:
            download(curl)
        except HTTPError404:
            if url == curl:
                print(f"{colored('404 Not Found', 'red')} ({curl})")
                sys.exit(1)
            if not failed_once:
                failed_once = True
                continue
            return
        else:
            failed_once = False


def url_iter(url: str):
    yield url

    parsed = urllib.parse.urlparse(url)
    path = parsed.path

    match = list(re.finditer(r"\d+", path))[-1]
    start, stop = match.start(), match.end()
    number_string = match.group()
    str_length = len(number_string)
    number = int(number_string)

    before, after = path[:start], path[stop:]

    while True:
        number += 1
        yield urllib.parse.urlunparse(
            parsed._replace(path=f"{before}{str(number).rjust(str_length, '0')}{after}")
        )


def download(url: str):
    print("Attempt:", url, "   ", end="\r")
    try:
        response = requests.get(url=url, timeout=(20, None), stream=True)
        if response.status_code == 404:
            raise HTTPError404()
        response.raise_for_status()
    except HTTPError404:
        print(colored("Not Found:", 'red'), url, "")
        raise
    except Exception:
        print(colored("Failed:", 'red'), url, "   ")
        raise
    else:
        print(colored("Download:", 'green'), url, " ")

    content_size, info_length = extract_content_size(response=response)

    # skip-download if file with same size already exists
    fn = extract_filename(url=url, response=response)
    if os.path.isfile(fn) and os.path.getsize(fn) == content_size:
        print(f"{fn} already exist. skipping download")
        return

    # find next free filename
    filename = get_free_filename(url=url, response=response)
    dot_name = f".{filename}"
    print(f"Writing to {filename}...", end='')

    try:
        with open(dot_name, 'wb') as file, ProgressBar() as bar:
            progress = 0.0
            for chunk in response.iter_content(CHUNK_SIZE):
                file.write(chunk)
                progress += len(chunk)
                bar.percent = progress / content_size if content_size else 0.0
    except Exception:
        if os.path.isfile(dot_name):
            os.remove(dot_name)
        raise
    else:
        os.rename(dot_name, filename)


def get_free_filename(url: str, response: requests.Response):
    fn = extract_filename(url=url, response=response)
    i = 0
    name, ext = os.path.splitext(fn)
    while os.path.isfile(fn):
        i += 1
        fn = f"{name} ({i}){ext}"
    return fn


def extract_content_size(response: requests.Response):
    try:
        content_size = response.headers['Content-length']
        info_length = len(content_size)
    except KeyError:
        content_size = None
        info_length = 1
    else:
        content_size = int(content_size)
    return content_size, info_length


def extract_filename(url: str, response: requests.Response):
    try:
        content_disposition = response.headers['Content-Disposition']
        return next(re.finditer("filename=(.+)", content_disposition))
    except KeyError:
        parsed = urllib.parse.urlparse(url=url)
        return os.path.split(parsed.path)[1]
