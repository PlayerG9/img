#!/usr/bin/python3
# -*- coding=utf-8 -*-
r"""

"""
import io
import math
import shutil
import requests
from PIL import Image


OFFSET = 0x2800

X0 = 0
L1 = 1
L2 = 2
L3 = 4
R1 = 8
R2 = 16
R3 = 32
L4 = 64
R4 = 128
OFFSETMAP = {
    (0, 0): L1,
    (0, 1): L2,
    (0, 2): L3,
    (0, 3): L4,
    (1, 0): R1,
    (1, 1): R2,
    (1, 2): R3,
    (1, 3): R4,
}


class ImageViewer:
    def __init__(self, path: str, width: int, height: int, detailed: bool):
        self.path = path
        twidth, theight = shutil.get_terminal_size()
        self.width = width or twidth
        self.height = height or theight
        self.detailed = detailed

    def run(self):
        image = self.load_image()
        print(self.render(image=image))

    def load_image(self) -> Image.Image:
        if self.path.startswith("http://") or self.path.startswith("https://"):
            return self.load_web()
        else:
            return self.load_file()

    def load_file(self) -> Image.Image:
        return Image.open(self.path)

    def load_web(self) -> Image.Image:
        response = requests.get(self.path)
        response.raise_for_status()
        buffer = io.BytesIO(response.content)
        buffer.seek(0)
        return Image.open(buffer)

    def render(self, image: Image.Image) -> str:
        if self.detailed:
            return self.render_detailed(image)
        else:
            return self.render_colored(image)

    @staticmethod
    def avg_color(img: Image.Image) -> int:
        total = 0
        for y in range(img.height):
            for x in range(img.width):
                light, alpha = img.getpixel((x, y))
                total += light * (alpha / 255)
        return round(total / (img.width * img.height))

    def render_colored(self, image: Image.Image) -> str:
        img = image.copy()
        img.thumbnail((self.width, self.height * 2))

        # not using
        # f"\033[48;2;{tr};{tg};{tb}m\033[38;2;{br};{bg};{bb}m\u2584"
        # to *greatly* improve performance by only adding tcodes on color change

        lines = []
        last_top_color = None
        last_bottom_color = None

        for y in range(math.ceil(img.height / 2)):
            characters = []
            if last_top_color:
                r, g, b = last_top_color
                characters.append(f"\033[48;2;{r};{g};{b}m")
            if last_bottom_color:
                r, g, b = last_bottom_color
                characters.append(f"\033[38;2;{r};{g};{b}m")
            for x in range(img.width):
                character = "\u2584"
                top = y * 2
                top_color = img.getpixel((x, top))[:3]
                if top_color != last_top_color:
                    last_top_color = top_color
                    r, g, b = top_color
                    character = f"\033[48;2;{r};{g};{b}m{character}"
                bottom = y * 2 + 1
                bottom_color = img.getpixel((x, bottom))[:3] if bottom <= img.height else (0, 0, 0)
                if bottom_color != last_bottom_color:
                    last_bottom_color = bottom_color
                    r, g, b = bottom_color
                    character = f"\033[38;2;{r};{g};{b}m{character}"

                characters.append(character)

            lines.append(''.join(characters) + '\033[39m\033[49m')
        return '\n'.join(lines)

    def render_detailed(self, image: Image.Image) -> str:
        img = image.convert('LA')
        img.thumbnail((self.width * 2, self.height * 4))
        tw, th = math.ceil(img.width / 2), math.ceil(img.height / 4)
        boundary = self.avg_color(img)
        invert = boundary < 50
        lines = []
        for ty in range(th):
            characters = []
            for tx in range(tw):
                b = X0
                for oy in range(4):
                    for ox in range(2):
                        rx, ry = (tx * 2) + ox, (ty * 4) + oy
                        try:
                            light, alpha = img.getpixel((rx, ry))
                        except IndexError:
                            pass
                        else:
                            color = light * (alpha / 255)
                            if color < boundary if invert else color > boundary:
                                b |= OFFSETMAP[(ox, oy)]
                characters.append(chr(OFFSET + b))
            lines.append(''.join(characters))
        return '\n'.join(lines)
