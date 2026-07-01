import time
import sys

sys.path.append("/usr/bin")
from rq_led_utils import (
    get_led_config,
    create_neopixel_strip,
    chunked_show,
    map_xy_to_pixel,
)

# --------------------------------------------------
# Setup
# --------------------------------------------------

config = get_led_config()

pixels = create_neopixel_strip(
    config["led_count"],
    config["pixel_order"],
    brightness=config["led_default_brightness"],
)

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WAIT = 3


def clear():
    pixels.fill(BLACK)
    chunked_show(pixels)


def set_pixel(x, y, color):
    idx = map_xy_to_pixel(x, y)
    if idx is not None:
        pixels[idx] = color


# --------------------------------------------------
# Example 1 - Horizontal Line
# --------------------------------------------------

def horizontal_line():
    clear()

    y = 3

    for x in range(24):
        set_pixel(x, y, GREEN)

    chunked_show(pixels)


# --------------------------------------------------
# Example 2 - Vertical Line
# --------------------------------------------------

def vertical_line():
    clear()

    x = 12

    for y in range(8):
        set_pixel(x, y, RED)

    chunked_show(pixels)


# --------------------------------------------------
# Example 3 - "Quantum Measurement"
# --------------------------------------------------

def quantum_measurement():
    clear()

    measurement = "10110010"

    for qubit, bit in enumerate(measurement):

        if bit == "1":
            color = BLUE
        else:
            color = (40, 40, 40)  # dim white

        set_pixel(qubit + 8, 3, color)

    chunked_show(pixels)

# --------------------------------------------------
# Example 4 - "SHU Lettering"
# --------------------------------------------------

SHU_COLOURS = [
    (98, 45, 145),    # Purple
    (0, 168, 150),    # Teal
    (226, 0, 116),    # Pink
]

FONT = {

    "S": [
    "0111111",
    "1111110",
    "1110000",
    "1111110",
    "0111111",
    "0000111",
    "1111111",
    "0111110",
    ],
    
    "H": [
    "1100011",
    "1100011",
    "1100011",
    "1111111",
    "1111111",
    "1100011",
    "1100011",
    "1100011",
    ],
    
    "U": [
    "1100011",
    "1100011",
    "1100011",
    "1100011",
    "1100011",
    "1100011",
    "1111111",
    "0111110",
    ],

}

def draw_char(x0, y0, ch, colour):
    bitmap = FONT[ch]

    for y, row in enumerate(bitmap):
        for x, pixel in enumerate(row):
            if pixel == "1":
                set_pixel(x0 + x, y0 + y, colour)

def shu_logo(delay=2):

    for colour in SHU_COLOURS:

        clear()

        draw_char(0, 0, "S", colour)
        draw_char(8, 0, "H", colour)
        draw_char(16, 0, "U", colour)

        chunked_show(pixels)

        time.sleep(delay)

# --------------------------------------------------
# Main
# --------------------------------------------------

try:

    print("Showing horizontal line...")
    horizontal_line()
    time.sleep(WAIT)
    clear()

    print("Showing vertical line...")
    vertical_line()
    time.sleep(WAIT)
    clear()

    print("Showing quantum measurement...")
    quantum_measurement()
    time.sleep(WAIT)

    print("Showing SHU...")
    shu_logo()

finally:
    clear()

