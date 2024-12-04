from cmu_graphics import *
from plants import *
from zombies import *
from levels import *
from preGame import *
from titleScreen import *
from parabolicMotion import *
from projectile import *
from PIL import Image
import math
import random
import copy



def onAppStart(app):
    app.imagePath = 'bounceProjectile.png'
    originalImage = Image.open(app.imagePath)
    maxDimension = max(originalImage.width, originalImage.height)
    paddedImage = Image.new("RGBA", (maxDimension, maxDimension), (0, 0, 0, 0))  # Transparent background
    paddedImage.paste(originalImage, 
                        ((maxDimension - originalImage.width) // 2, 
                           (maxDimension - originalImage.height) // 2))
    rotatedImage = paddedImage.rotate(45, resample=Image.BICUBIC, expand=True)

    app.image = CMUImage(rotatedImage)
    # arg = 45
    # rotatedImage = Image.open(app.imagePath)
    # app.image = CMUImage(rotatedImage.rotate(arg))

def redrawAll(app):
    drawImage(app.image, 50, 50, align='center', width = 80, height = 80)
    drawImage(app.image, 50, 200, align='center')

def main():
    runApp()

main()