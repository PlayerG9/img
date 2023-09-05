#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import os
import sys
import shutil
import tempfile
import zipfile
from pathlib import Path
import typing as t
from distutils.version import LooseVersion
import requests
from ..logger.coloring import colored, COLOR
from ..util.progress_bar import ProgressBar
from .. import __version__


class Updater:
    def __init__(self, check_only: bool):
        self.check_only = check_only

    def run(self):
        release = self.get_release()
        own = LooseVersion(__version__)
        remote = LooseVersion(release["tag_name"].removeprefix("v"))
        if own > remote:
            print(colored("Your version is higher that the latest release. "
                          "You have to manually resolve this issue", COLOR.red),
                  f"({own} > {remote})")
        elif own == remote:
            print(colored("Newest version already installed", COLOR.green), f"({own})")
        else:
            print(colored("Newer version available", COLOR.yellow), f"({own} < {remote})")
            if not self.check_only:
                self.install_newest_version(release)

    def get_release(self) -> 'Release':
        response = requests.get("https://api.github.com/repos/PlayerG9/img/releases/latest")
        response.raise_for_status()
        return response.json()

    def install_newest_version(self, release: 'Release'):
        if self.check_if_zipapp():
            self.update_archive(release)
        else:
            self.update_repository(release)

    def check_if_zipapp(self):
        return zipfile.is_zipfile(sys.argv[0])

    def update_repository(self, release):
        raise NotImplementedError("Automatically updating of the repository is currently not supported.")

    def update_archive(self, release: 'Release'):
        asset = release["assets"][0]
        response = requests.get(asset["browser_download_url"], stream=True)
        total = asset["size"]
        archive_path = Path(sys.argv[0])
        temp_path = tempfile.mktemp()
        with (
            ProgressBar() as progress,
            open(temp_path, 'wb') as temp_file,
        ):
            downloaded = 0
            for chunk in response.iter_content(1024 * 100):
                temp_file.write(chunk)
                downloaded += len(chunk)
                progress.percent = downloaded / total

            mode = archive_path.stat().st_mode
            os.remove(archive_path)
            shutil.move(temp_path, archive_path)
            archive_path.chmod(mode)

        print(colored("Successfully updated", COLOR.green))


class Release(t.TypedDict):
    html_url: str
    id: int
    tag_name: str
    name: str
    assets: t.List['Assets']


class Assets(t.TypedDict):
    name: str
    size: int
    browser_download_url: str
