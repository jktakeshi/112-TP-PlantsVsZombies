from cmu_graphics import *
from plants import *
from zombies import *
from levels import *
from preGame import *
from titleScreen import *
from parabolicMotion import *
from projectile import *
from PIL import Image, ImageDraw, ImageFont
import math
import random
import copy



font_path = "fonts/seriesOrbit.ttf"
font_size = 20  # Adjust the size as needed
font = ImageFont.truetype(font_path, font_size)

# Create an image to draw text on
image = Image.new("RGBA", (300, 100), (255, 255, 255, 0))  # Transparent background
draw = ImageDraw.Draw(image)

# Draw text using the loaded font
# draw.text((10, 10), "Hello, Series Orbit!", font=font, fill=(0, 0, 0, 255))

def redrawAll(app):
    # drawImage(app.customText, 100, 100)
    draw.text((10, 10), "Hello World!", font=font, fill=(3, 3, 3))
def main():
    runApp()

main()