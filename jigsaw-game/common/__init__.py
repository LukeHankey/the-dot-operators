#!/usr/bin/venv python3
"""Core Image Manipulation functionality"""

from math import sqrt
import requests
from PIL import Image
import random
#from PIL.Image import Image, open


def get_image(
    filename: str, max_dimensions: tuple[int, int], num_of_tiles: int
) -> Image:
    """This could be extended to by addeding filters, and from other sources"""
##    with open(filename) as image:
##        image.thumbnail(max_dimensions)
##        num_of_tiles = int(sqrt(num_of_tiles))
##        width = image.width // num_of_tiles
##        height = image.height // num_of_tiles
##        image = image.crop((0, 0, num_of_tiles * width, num_of_tiles * height))
    PEXELS_API_KEY = '1cK1A6oZ1wPOB49B2qMohsQCWp2aIEU8FlRzQIt9bL3AzXzjle5fmRsh'
    api = API(PEXELS_API_KEY)
    api.search('Coding', page=1, results_per_page=5)
    photos = api.get_entries()
    photo = random.choice(photos)
    try:
        Code = str(int(photo.url[-7:-1]))
    except:
        Code = photo.url[-6:-1]
    my_url = "https://images.pexels.com/photos/"+Code+"/pexels-photo-"+Code+'.jpeg'
    print('HERE',my_url)
    my_img = Image.open(requests.get(my_url, stream=True).raw)
    my_img.show()
    
    return Image

from pexels_api import API


