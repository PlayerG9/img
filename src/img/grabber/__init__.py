#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import typing as t


class ImageGrabber:
    def __init__(self, url: str, overwrite: bool, skips: int, formats: t.List[str]):
        self.url = url
        self.overwrite = overwrite
        self.skips = skips
        self.formats = formats

    def run(self):
        raise NotImplementedError()
