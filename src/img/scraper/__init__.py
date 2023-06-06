#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
todo: implement max-depth
"""
import os
import time
import typing as t
import urllib.parse as urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
import bs4
from ..logger.coloring import colored, COLOR
from ..logger import Logger, Waiting
from ..downloader import Downloader


class ImageScraper:
    # def __init__(self, url: str, all_links: bool, max_depth: int, min_width: int, min_height: int):
    def __init__(self, url: str, all_links: bool):
        self.url = url
        self.all_links = all_links
        # self.max_depth = max_depth
        # self.min_width = min_width
        # self.min_height = min_height

    def run(self):
        html = self.fetch_website(self.url, check=False)
        urls = self.find_all_urls(self.url, html)
        self.handle_urls(urls)

    @staticmethod
    def fetch_website(url: str, check=True) -> bytes:
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type', "")
        if not content_type != "text/html":
            if check:
                raise LookupError(f"Bad Content-Type ({content_type!r})")
            else:
                print(colored(f"Bad Content-Type ({content_type!r})", COLOR.yellow))
        return response.content

    def find_all_urls(self, source: str, html: bytes):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        urls = []
        if self.all_links:
            for link in soup.select('a[href]:has(img)'):
                urls.append(urlparse.urljoin(source, link['href']))
        for img in soup.select('img[src]'):
            urls.append(urlparse.urljoin(source, img['src']))
        return [url for url in urls if url.startswith("http")]

    def handle_urls(self, urls: t.List[str]):
        max_workers = min(8, os.cpu_count())
        active = 0
        try:
            with (Logger(), ThreadPoolExecutor(max_workers) as pool):
                for url in urls:
                    response = requests.get(url=url, timeout=(20, None), stream=True)
                    downloader = Downloader(response)
                    Logger.print(downloader)

                    active += 1

                    def download():
                        nonlocal active
                        downloader.download()
                        active -= 1

                    pool.submit(download)

                    while active >= max_workers:
                        time.sleep(0.01)

                Logger.print(Waiting())
            Logger.undo_last_line()
        except KeyboardInterrupt:
            pass
