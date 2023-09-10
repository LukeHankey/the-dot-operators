#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from collections.abc import Generator
from io import BytesIO
from json import dump, load, loads
from math import sqrt
from operator import itemgetter
from os import listdir, path
from random import choice, randint, shuffle
from typing import Any, cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from PIL import Image
from requests import get

from .fcolor import (
    analogue_palette,
    complementary_color,
    low_saturation,
    monochrome_palette,
    rotate_color,
)
from .modifier import backing

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]
BASE_URL = "https://photoslibrary.googleapis.com/v1/"
BASE_HEADER = {"content-type": "application/json"}
CREDENTIALS_FILENAME = ".credentials.json"
TOKEN_FILENAME = ".token.json"


def get_client_api() -> Credentials:
    """This function gets the client credentials stores local for users"""
    credentials = None

    if path.exists(TOKEN_FILENAME):
        with open(TOKEN_FILENAME) as token_file:
            json_data = load(token_file)

        credentials = Credentials.from_authorized_user_info(json_data)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILENAME, SCOPES
            )
            credentials = cast(Credentials, flow.run_local_server())

        with open(TOKEN_FILENAME, "w") as token_file:
            dump(loads(credentials.to_json()), token_file, indent=1)

    return credentials


def fit(image: Image.Image, num_of_tiles: int) -> Image.Image:
    """Crop image to best size to tiles"""
    num_of_tiles = int(sqrt(num_of_tiles))

    width = image.width // num_of_tiles * num_of_tiles
    height = image.height // num_of_tiles * num_of_tiles

    return image.crop((0, 0, width, height))


def media_items_extractor(
    media_items: list[dict[str, Any]]
) -> Generator[tuple[int, dict[str, Any]], None, None]:
    """Extracts out the desired dictionary items"""
    for item in media_items:
        if item["mimeType"].startswith("image"):
            metadata = item["mediaMetadata"]
            width, height = int(metadata["width"]), int(metadata["height"])

            if width < 500 or height < 500:
                continue

            yield item["id"], {
                "description": item.get("description", ""),
                "size": (width, height),
                "birth": metadata["creationTime"],
                "filename": item["filename"],
                "accessed": 0,
            }


def get_remote_image_catalogue(
    limit: int = 1000,
) -> Generator[tuple[int, dict[str, Any]], None, None]:
    """This function will get whole catalogue local"""
    headers = {
        **BASE_HEADER,
        "Authorization": f"Bearer {get_client_api().token}",
        "pageSize": str(100),
    }

    next_page_token = True
    count = 0

    while next_page_token and (count < limit):
        response = get(BASE_URL + "mediaItems", headers=headers).json()
        for _id, item in media_items_extractor(response["mediaItems"]):
            yield _id, item
            count += 1

        next_page_token = response.get("nextPageToken", False)
        headers["pageToken"] = next_page_token


def get_remote_image(
    _id: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image.Image:
    """This function will request the google photos api"""
    headers = {**BASE_HEADER, "Authorization": f"Bearer {get_client_api().token}"}
    response = get(BASE_URL + "mediaItems/" + _id, headers=headers).json()

    width, height = max_dimensions
    response = get(f"{response['baseUrl']}=w{width}-h{height}", headers=headers)

    return fit(Image.open(BytesIO(response.content)), num_of_tiles)


def get_image(
    filename: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image.Image:
    """This could be extended to by addeding filters, and from other sources"""
    with Image.open(filename) as image:
        image.thumbnail(max_dimensions)
        return fit(image, num_of_tiles)


def rotate_image_color(image: Image.Image) -> Image.Image:
    """Rotate colour wheel on all pixels by fixed a random amount"""
    image = image.copy().convert("RGBA")
    angle = randint(0, 180)

    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x, y))
            image.putpixel((x, y), (*rotate_color(angle, *pixel[:3]), pixel[3]))

    return image


def most_common_color(image: Image.Image) -> tuple[int, int, int]:
    """Find the most common colour on the image through getcolors"""
    common_colors = image.getcolors(image.size[0] * image.size[1])
    common_colors = list(filter(lambda x: x[1][3], common_colors))
    common_colors.sort()

    return common_colors[-1][1][:3]


def get_generated_image(max_size: tuple[int, int], num_of_tiles: int) -> Image.Image:
    """For internal images

    uses logos and puts it onto a voronoi background after spinning its
    color wheel
    """
    with Image.open("images/" + choice(listdir("images"))) as image:
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        image = fit(image, num_of_tiles)

    image = rotate_image_color(image)
    seed_color = complementary_color(*most_common_color(image))

    if low_saturation(*seed_color):
        palette_function = monochrome_palette
    else:
        palette_function = choice([analogue_palette, monochrome_palette])

    background = backing(
        int(max_size[0] * 1.1), int(max_size[1] * 1.1), seed_color, palette_function
    )

    x_offset = (background.width - image.width) // 2
    y_offset = (background.height - image.height) // 2

    background.alpha_composite(image, (x_offset, y_offset))
    return background


def hamming_distance(
    sequence_0: list[tuple[int, int]], sequence_1: list[tuple[int, int]]
) -> int:
    """Find the distance between the solution and the scrambled"""
    return sum(x != y for x, y in zip(sequence_0, sequence_1))


def tile_scrambler(
    tiles: list[tuple[tuple[int, int], Image.Image]]
) -> list[tuple[tuple[int, int], Image.Image]]:
    """Extract out the positions to shuffle then add back in"""
    positions = list(map(itemgetter(0), tiles))
    length = len(positions)

    new_positions = positions[:]
    shuffle(new_positions)

    while hamming_distance(new_positions, positions) != length:
        shuffle(new_positions)

    return list(zip(new_positions, map(itemgetter(1), tiles)))
