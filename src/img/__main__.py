#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import argparse
from . import __version__, img_get


class NameSpace:
    url: str

    def __repr__(self):
        return f"<args {self.__dict__}>"


parser = argparse.ArgumentParser(prog="img", description=__doc__, add_help=True,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--version', action="version", version=__version__)
parser.add_argument('url', help="the url to start from")


def main():
    args = parser.parse_args(namespace=NameSpace())
    img_get(args.url)
    return 0


if __name__ == '__main__':
    sys.exit(main())
