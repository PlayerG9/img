#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
todo: implement max-depth
"""
import typing as t
import urllib.parse as urlparse
import requests
import bs4
from ..logger.coloring import colored, COLOR
from ..logger import Logger, Waiting
from ..downloader import Downloader, DownloadPool
from ..util.responses import is_image_type


class ImageScraper:
    # def __init__(self, url: str, all_links: bool, max_depth: int, min_width: int, min_height: int):
    def __init__(self, url: str, all_links: bool, min_width: int, min_height: int):
        self.url = url
        self.all_links = all_links
        # self.max_depth = max_depth
        self.min_width = min_width
        self.min_height = min_height

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
            for link in soup.select('a[href]:has(img[src])'):
                url = urlparse.urljoin(source, link['href'])
                if url not in urls:
                    urls.append(url)
        for img in soup.select('img[src]'):
            url = urlparse.urljoin(source, img['src'])
            if url not in urls:
                urls.append(url)
        return [url for url in urls if url.startswith("http")]

    def handle_urls(self, urls: t.List[str]):
        try:
            with Logger(), DownloadPool() as pool:
                for url in urls:
                    response = requests.get(url=url, timeout=(20, None), stream=True)
                    if not is_image_type(response):
                        continue
                    downloader = Downloader(response, min_width=self.min_width, min_height=self.min_height)
                    Logger.print(downloader)

                    pool.submit(downloader.download)

                Logger.print(Waiting())
            Logger.undo_last_line()
        except KeyboardInterrupt:
            pass
