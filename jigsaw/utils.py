#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from collections.abc import Generator
from io import BytesIO
from json import dump, load, loads
from math import sqrt
from operator import itemgetter
from os import path
from random import shuffle
from typing import Any, cast

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from PIL import Image
from requests import get

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
