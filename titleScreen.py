from cmu_graphics import *
from PIL import Image

path = 'titleScreen.png'
image = Image.open(path)
app.titleScreen = CMUImage(image)

def drawTitleScreen(app):
    drawImage(app.titleScreen, 0, 0, width=app.width, height=app.height)
    # drawRect(350, 512, 280, 40, border='black', fill=None)

def titleToLevels(app, mouseX, mouseY):
    if 350 <= mouseX <= 630 and 512 <= mouseY <= 552:
        app.gameState = 'levels'