#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import argparse
from . import __version__


class NameSpace:
    def __repr__(self):
        return f"<args {self.__dict__}>"


parser = argparse.ArgumentParser(prog="img-get", description=__doc__, add_help=True,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--version', action="version", version=__version__)


def main():
    args = parser.parse_args(namespace=NameSpace)


if __name__ == '__main__':
    sys.exit(main())
