#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""
todo: implement max-depth
"""
import io
import os
import os.path as p
import urllib.parse as urlparse
import typing as t
import requests
from requests.exceptions import HTTPError
import bs4
from ..util.coloring import colored, COLOR
from ..util import progress_bar as pb
from ..util.image_size import get_image_size, UnknownImageFormat
from ..util.responses import extract_content_size, get_free_filename
from ..util.logger import Logger


class ImageScraper:
    def __init__(self, url: str, export: bool, all_links: bool, max_depth: int, min_width: int, min_height: int):
        self.url = url
        self.export = export
        self.all_links = all_links
        self.max_depth = max_depth
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
            for link in soup.select('a[href]:has(img)'):
                urls.append(urlparse.urljoin(source, link['href']))
        for img in soup.select('img[src]'):
            urls.append(urlparse.urljoin(source, img['src']))
        return [url for url in urls if urlparse.urlparse(url).scheme.startswith("http")]

    def handle_urls(self, urls: t.List[str]):
        Logger.enabled = not self.export
        with (
            (pb.PseudoProgressBar() if self.export else pb.ProgressBar()) as progressbar,
        ):
            for i, url in enumerate(urls):
                progressbar.percent = i / len(urls)
                Logger.info("Attempt:", url)
                response = requests.get(url, stream=True)
                if not response.ok:
                    Logger.error(f"[{response.status_code}] response.reason")
                content_type = response.headers.get('Content-Type', "")
                if not content_type.startswith("image/"):
                    Logger.error(f"Not an Image", f"({content_type})")
                    continue
                content_size = extract_content_size(response)
                chunks = response.iter_content(1024*512)
                head = next(chunks)
                if self.min_width or self.min_height:
                    try:
                        width, height = get_image_size(content_size or 100, io.BytesIO(head))
                    except UnknownImageFormat:
                        Logger.warning("Unknown image format. Can't verify image-size")
                        continue
                    if width < self.min_width or height < self.min_height:
                        Logger.error(f"Image too small")
                        continue
                if self.export:
                    print(url)
                    continue
                Logger.success("Download:", url)
                file_path = get_free_filename(response)
                dot_path = f".{file_path}"
                try:
                    with open(dot_path, 'wb') as file:
                        file.write(head)
                        done = len(head)
                        for chunk in chunks:
                            file.write(chunk)
                            done += len(chunk)
                            progressbar.percent = (i / len(urls)) + ((done / content_size) / len(urls))
                except Exception:
                    if p.isfile(dot_path):
                        os.remove(dot_path)
                    raise
                else:
                    os.rename(dot_path, file_path)

    def continue_download(self, response: requests.Response):
        raise NotImplementedError()
