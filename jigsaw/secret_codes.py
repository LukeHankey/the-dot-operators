#!/usr/bin/venv python3
"""Our way to match the theme 'secret codes'"""
from collections.abc import Generator
from copy import deepcopy

from PIL.Image import Image
from PIL.ImageChops import difference
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype

NUM_OF_TILES = 3200


def insert_newline_in_centered_space(string: str) -> str:
    """This is so lines can wrap for multiline output"""
    split_string = list(string)
    left_offset = len(split_string) // 2
    right_offset = len(split_string) // 2 + 1

    while True:
        if split_string[left_offset] == " ":
            split_string[left_offset] = "\n"
            break
        elif split_string[right_offset] == " ":
            split_string[right_offset] = "\n"
            break

        right_offset -= 1
        left_offset += 1

    return "".join(split_string)


def fitted_text_mask(image: Image, text: str) -> Image:
    """Write text to the image that fits to the edges"""
    image = deepcopy(image)  # deepcopy to prevent modifying the original
    width, height = image.size

    font_size = 1
    font_name = "DejaVuSans-ExtraLight.ttf"

    try:
        truetype(font_name, size=font_size)
    except OSError:
        font_name = "arial.ttf"

    text_parameters = {  # default parameters for `multiline_textbbox`
        "font": truetype(font_name, size=font_size),
        "anchor": None,
        "spacing": 32,
        "align": "center",
    }

    # dummy draw to see the first bbox
    draw = Draw(image)
    *_, text_width, text_height = draw.multiline_textbbox(
        (0, 0), text, **text_parameters
    )

    while text_width < width and text_height < height:
        font_size += 1
        text_parameters["font"] = truetype(font_name, font_size)
        *_, text_width, text_height = draw.multiline_textbbox(
            (0, 0), text, **text_parameters
        )

        # if trailing off edge make multiline
        if text_width >= width and "\n" not in text:
            text = insert_newline_in_centered_space(text)
            *_, text_width, text_height = draw.multiline_textbbox(
                (0, 0), text, **text_parameters
            )

    # decrement as we have gone to far then draw the text for real
    font_size -= 1
    text_parameters["font"] = truetype(font_name, font_size)
    draw = Draw(image)
    draw.text((0, 0), text, "white", **text_parameters)

    return image


def filter_tiles(
    text_tiles: list[tuple[tuple[int, int], Image]],
    normal_tiles: list[tuple[tuple[int, int], Image]],
) -> Generator[tuple[tuple[int, int], Image | None], None, None]:
    """Generator to find matching tiles

    If tiles do not match they are set to None, to tell the GUI
    no tile here, skip, move to next tile
    """
    for (_, stile), (np, ntile) in zip(text_tiles, normal_tiles):
        if not difference(stile, ntile).getbbox():
            yield (np, ntile)
        else:
            yield (np, None)
