from cmu_graphics import *
from PIL import Image
from levels import *

def drawPregame(app):
    # citation: https://pvz-rp.fandom.com/wiki/Player%27s_House
    drawImage(app.frontYard, 0, 0, width=app.width, height=app.height)
    # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot
    drawImage(app.seedSlot, 230, 2, width=app.plantPanelWidth, height=app.plantPanelHeight)
    # citation: https://plantsvszombies.fandom.com/wiki/Shovel
    drawImage(app.shovelIcon, 715, 37, align='center', width = 45, height = 50)
    drawLabel(f'{app.sunPoints}', 270, 60, bold = True)
    drawLabel("Press the spacebar to play", app.width/2, app.height/2, bold = True, size=50)

def onKeyPress(self, key):
    if key == "space":
        app.gameState = 'gameplay'
        app.paused = False
        plantPanel(app)

