#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
# r"""
#   _                                                                 _
#  (_)_ __ ___   __ _    ___ ___  _ __ ___  _ __ ___   __ _ _ __   __| |
#  | | '_ ` _ \ / _` |  / __/ _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |
#  | | | | | | | (_| | | (_| (_) | | | | | | | | | | | (_| | | | | (_| |
#  |_|_| |_| |_|\__, |  \___\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|
#               |___/
# """
import argparse
from . import __version__
from . import grabber as lib_grabber
from . import scraper as lib_scraper
from . import updater as lib_updater


class FormatterClass(argparse.RawDescriptionHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
    pass


parser = argparse.ArgumentParser(prog="img", description=__doc__,
                                 add_help=True, formatter_class=FormatterClass)
parser.add_argument('-v', '--version', action="version", version=__version__)

subparser = parser.add_subparsers(required=True)

#
# updater
#

update_parser = subparser.add_parser(
    "update",
    help="check for updates and install them",
    description=lib_updater.__doc__,
    # aliases=["upgrade"],
)
update_parser.set_defaults(cls=lib_updater.Updater)
update_parser.add_argument("--check-only", action="store_true",
                           help="only check for a new version but don't upgrade")


#
# grabber
#

grabber_parser = subparser.add_parser(
    "grab",
    help="Grab a collection of images",
    description=lib_grabber.__doc__,
    aliases=["get"],
)
grabber_parser.set_defaults(cls=lib_grabber.ImageGrabber)
# grabber_parser.add_argument('-O', '--overwrite', action=argparse.BooleanOptionalAction, default=False,
#                             help="whether to overwrite existing images")
grabber_parser.add_argument('-S', '--skips', type=int, default=0,
                            help="sometimes images are missing."
                                 "This is the amount of images that are allowed to be skipped/missing.")
# grabber_parser.add_argument('-F', '--formats', type=lambda s: s.split(","), nargs='?', const="jpg,png", default=[],
#                             help=", seperated list of extensions to try if a [404] Not Found is returned")
grabber_parser.add_argument('-H', '--history', action=argparse.BooleanOptionalAction, default=False,
                            help="add the last failed command to the history for better manual fixing")
grabber_parser.add_argument('url',
                            help="the url to start from")

#
# scraper
#

scraper_parser = subparser.add_parser(
    "scrape",
    help="Scrape a website for images and get these",
    description=lib_scraper.__doc__,
    # aliases=[],
)
scraper_parser.set_defaults(cls=lib_scraper.ImageScraper)
scraper_parser.add_argument('-A', '--all-links', action="store_true", default=False,
                            help="check all links if they are images")
# scraper_parser.add_argument('-D', '--max-depth', type=int, default=1,
#                             help="how many linked pages to scrape")
scraper_parser.add_argument('-W', '--min-width', type=int, nargs='?', const=1000, default=None,
                            help="minimum width of images to download")
scraper_parser.add_argument('-H', '--min-height', type=int, nargs='?', const=1000, default=None,
                            help="minimum height of images to download")
scraper_parser.add_argument('url',
                            help="the url to start from")

#
# main
#


def main():
    args = vars(parser.parse_args())
    if __debug__:
        print(args)
    executor = args.pop("cls")(**args)
    executor.run()


if __name__ == '__main__':
    main()
