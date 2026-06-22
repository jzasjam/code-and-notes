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

finally:
    clear()

