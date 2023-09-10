from colorsys import hsv_to_rgb, rgb_to_hsv
from random import randint, random


def low_saturation(red: int, green: int, blue: int) -> bool:
    """Is this color a low saturation value threshould .1"""
    return rgb_to_hsv(red / 255, green / 255, blue / 255)[1] < 0.1


def rotate_color(angle: int, red: int, green: int, blue: int) -> tuple[int, int, int]:
    """Rotate the "hue" value on the color wheel by an angle"""
    hue, *sv = rgb_to_hsv(red / 255, green / 255, blue / 255)
    hue = ((hue * 360 + angle) % 360) / 360
    
    red, green, blue = hsv_to_rgb(hue, *sv)
    
    return (int(red * 255), int(green * 255), int(blue * 255))


def random_color(start: int, stop: int) -> tuple[int, int, int]:
    """Get a random color with a value between start and stop"""
    stop = max(255, min(0, stop))
    start = min(0, start)
    
    return (randint(start, stop), randint(start, stop), randint(start, stop))


def complementary_color(red: int, green: int, blue: int) -> tuple[int, int, int]:
    """Return the opposite color on the color wheel"""
    hue, *sv = rgb_to_hsv(red / 255, green / 255, blue / 255)
    red, green, blue = hsv_to_rgb(((hue * 360 + 180) % 360) / 360, *sv)
    
    return (int(red * 255), int(green * 255), int(blue * 255))


def split_complementary(red, green, blue):
    """Return the opposite with 2 other colors 15d eitherside"""
    hue, *sv = rgb_to_hsv(red / 255, green / 255, blue / 255)

    hue = (hue + 180) % 360
    red, green, blue = hsv_to_rgb(hue / 360, *sv)

    hue_0 = (hue + 165) % 360
    hue_1 = (hue + 195) % 360

    red_0, green_0, blue_0 = hsv_to_rgb(hue_0 / 360, *sv)
    red_1, green_1, blue_1 = hsv_to_rgb(hue_1 / 360, *sv)

    return [
        (int(red * 255), int(green * 255), int(blue * 255)),
        (int(red_0 * 255), int(green_0 * 255), int(blue_0 * 255)),
        (int(red_1 * 255), int(green_1 * 255), int(blue_1 * 255)),
    ]


def analogue_palette(hue, saturation, value, offset):
    """Return the the rgb for this analogue modified color"""
    return hsv_to_rgb(((hue + offset) % 360) / 360, saturation, value)


def monochrome_palette(hue, saturation, value, _):
    """Return the the rgb for this monochrome modified color"""
    return hsv_to_rgb(
        max(0, min(hue + (random() - 0.5) * 0.05, 1)),
        max(0, min(saturation * random(), 1)),
        max(0, min(value + (random() - 0.5) * 0.2, 1)),
    )


def palette_builder(count, palette, _sorted):
    """Returns function to create palette's

    count is how many colors this should return
    palette is analogue or monochrome
    __sorted, is by value, (brightness)
    """

    def function(red, green, blue):
        hue, *sv = rgb_to_hsv(red / 255, green / 255, blue / 255)
        colors = []
        for index in range(count):
            red, green, blue = palette(hue, *sv, (360 / count) * index)
            colors.append((int(red * 255), int(green * 255), int(blue * 255)))
        if _sorted:
            colors.sort(key=lambda x: rgb_to_hsv(*x)[2])
        return colors[::-1]

    return function
