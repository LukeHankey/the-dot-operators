#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from io import BytesIO
from json import dump, load
from math import sqrt
from os import path
from random import shuffle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from PIL import Image
from requests import get

SCOPES = ["https://www.googleapis.com/auth/photoslibrary.readonly"]


def get_client_api(credentials_filename, token_filename):
    """This function gets the client credentials stores local for users"""
    credentials = None
    if path.exists(token_filename):
        with open(token_filename, "rb") as token_file:
            credentials = load(token_file)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_filename, SCOPES
            )
            credentials = flow.run_local_server()
        with open(token_filename, "wb") as token_file:
            dump(credentials, token_file)
    return credentials


def fit(image: Image.Image, num_of_tiles: int):
    """Crop image to best size to tiles"""
    num_of_tiles = int(sqrt(num_of_tiles))
    width = image.width // num_of_tiles * num_of_tiles
    height = image.height // num_of_tiles * num_of_tiles
    return image.crop((0, 0, width, height))


def get_remote_image(max_dimensions: tuple[int, int], num_of_tiles: int) -> Image.Image:
    """This function will request the google photos api"""
    url = "https://photoslibrary.googleapis.com/v1/mediaItems"
    token = get_client_api(".credentials.json", ".token.json").token
    headers = {"content-type": "application/json", "Authorization": "Bearer " + token}
    response = get(url, headers=headers)
    for item in response.json()["mediaItems"]:
        if item["mimeType"].startwith("image"):
            base_url = item["baseUrl"]
            break  # insert memory check logic
    width, height = max_dimensions
    response = get(f"{base_url}=w{width}-h{height}", headers=headers)
    with Image.open(BytesIO(response.content)) as image:
        return fit(image, num_of_tiles)


def get_image(
    filename: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image.Image:
    """This could be extended to by addeding filters, and from other sources"""
    with Image.open(filename) as image:
        image.thumbnail(max_dimensions)
        return fit(image, num_of_tiles)


def tile_scrambler(
    tiles: dict[tuple[int, int], Image.Image]
) -> list[tuple[tuple[int, int], Image.Image]]:
    """Extract out the positions to shuffle then add back in"""
    # extract out the positions to shuffle then add back in
    positions = list(tiles)
    shuffle(positions)
    return zip(positions, tiles.values())
