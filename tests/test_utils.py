from os import chdir, remove
from random import choice
from time import sleep

from jigsaw.utils import TOKEN_FILENAME, get_remote_image, get_remote_image_catalogue

chdir(__import__("jigsaw").utils.__file__.rstrip("utils.py"))

local_media_catalog = dict()
for num, (_id, item) in enumerate(get_remote_image_catalogue(200)):
    local_media_catalog[_id] = item
    print(
        end=f"\x1B[2K {num: 4} images detected {_id[-10:]} {item['filename'][:60]} {item['description']}\r"
    )
print("\x1B[2kFinished!")

for _ in range(10):
    _id = choice(list(local_media_catalog.keys()))
    local_media_catalog.pop(_id)  # don't choose image again
    image = get_remote_image(_id, (500, 500), 3200)
    image.show()
    sleep(1)

if input("Cleanup tokens? [no] "):
    remove(TOKEN_FILENAME)
