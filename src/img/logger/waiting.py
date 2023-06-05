#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""


class Waiting:
    # ⠁⠂⠄⡀⢀⠠⠐⠈
    CHARS = '⠁⠂⠄⡀⢀⠠⠐⠈'
    NCHARS = len(CHARS)

    def __init__(self):
        self.index = 0

    def __str__(self):
        spinner = self.CHARS[self.index]
        self.index = (self.index + 1) % self.NCHARS
        return f"Waiting for download to finish {spinner}"
