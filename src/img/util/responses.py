#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import re
import os.path as p
import urllib.parse as urlparse
from requests import Response


def extract_content_size(response: Response):
    try:
        content_size = response.headers['Content-Length']
    except KeyError:
        content_size = None
    else:
        content_size = int(content_size)
    return content_size


def extract_filename(response: Response):
    try:
        return urlparse.unquote(
            next(re.finditer(r'filename=(.+)', response.headers['Content-Disposition'])).group()
        )
    except (KeyError, StopIteration):
        pass

    u = urlparse.urlparse(response.url)
    if '/' in u.path:
        return urlparse.unquote(
            u.path.rsplit('/', 1)[1]
        )

    return urlparse.unquote(u.hostname)


def get_free_filename(response: Response):
    fn = extract_filename(response=response)
    i = 0
    name, ext = p.splitext(fn)
    while p.isfile(fn):
        i += 1
        fn = f"{name} ({i}){ext}"
    return fn


def is_image_type(response: Response):
    try:
        content_type: str = response.headers["Content-Type"]
    except KeyError:
        return False
    else:
        return content_type.startswith("image/")
