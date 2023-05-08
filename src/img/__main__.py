#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import sys
import typing as t
import argparse
from . import __version__


class NameSpace:
    url: str

    # grabber
    overwrite: bool
    skips: int
    formats: t.List[str]

    # scraper
    export: bool
    max_depth: int
    min_width: int
    min_height: int

    def __repr__(self):
        return f"<args {self.__dict__}>"


parser = argparse.ArgumentParser(prog="img", description=__doc__, add_help=True,
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-v', '--version', action="version", version=__version__)

grabber = parser.add_argument_group(
    "grabber",
    "Grab a collection of images. Used when passing an image-url"
)
grabber.add_argument('--overwrite', action=argparse.BooleanOptionalAction, default=False,
                     help="whether or not to overwrite existing images")
grabber.add_argument('--skips', type=int, default=0,
                     help="sometimes images are missing. This is the amount of images are allowed to be skipped.")
grabber.add_argument('-F', '--formats', type=lambda s: s.split(","), nargs='?', const="jpg,png", default=[],
                     help=", seperated list of extensions to try if a [404] Not Found is returned")

scraper = parser.add_argument_group(
    "scraper",
    "Scrape a website for images and get these images. Used when passing a website-url"
)
scraper.add_argument('--export', action="store_true", default=False,
                     help="only print the found urls instead of downloading the images.")
scraper.add_argument('-D', '--max-depth', type=int, default=1,
                     help="how many linked pages to scrape")
scraper.add_argument('-W', '--min-width', type=int, default=0,
                     help="minimum width of images to download")
scraper.add_argument('-H', '--min-height', type=int, default=0,
                     help="minimum height of images to download")

parser.add_argument('url', help="the url to start from")


def main():
    args = parser.parse_args(namespace=NameSpace())
    print(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())
