#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import threading
import time

import requests
from ..downloader import Downloader
from ..logger import Logger, Waiting, Codes
from ..util.responses import is_image_type


class WGet:
    def __init__(self, url: str):
        self.url = url

    def run(self):
        response = requests.get(self.url, timeout=(20, None), stream=True)
        if not is_image_type(response=response):
            Logger.print(f"{Codes.FG_LIGHT_YELLOW}Warning:{Codes.RESTORE_FG} probably not an image")

        downloader = Downloader(response)
        Logger.print(downloader)

        Logger.print(Waiting())
        thread = threading.Thread(target=downloader.download)
        thread.start()
        while thread.is_alive():
            Logger.update()
            time.sleep(0.2)
        Logger.pop_last_line()
        Logger.print(f"{Codes.FG_LIGHT_GREEN}Image Downloaded{Codes.RESTORE_FG}")
        Logger.update()
