from plants import *
from zombies import *
from PIL import Image

path = 'levelSelector.png'
image = Image.open(path)
app.levelSelector = CMUImage(image)

Levels = {
    'easy': {
        'plants': [Sunflower, PeaShooter],
        'zombies': [regularZombie],
        'startZombieSpawn': 13,
        'zombieSpawnRate': 4,
        'finalWaveSpawnRate': 2,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 10,
        'finalWaveTypes': [flagZombie, regularZombie],
        'finalWaveDelay': 8
    },
    'medium': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 13,
        'zombieSpawnRate': 3,
        'finalWaveSpawnRate': 1,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 15,
        'finalWaveTypes': [flagZombie, regularZombie, coneHeadZombie],
        'finalWaveDelay': 8,
        'coneHeadLimit': 5
    }
}

def drawLevelSelector(app):
    drawImage(app.levelSelector, 0, 0, width=app.width, height=app.height)
    gap = 90
    startX = 530
    width = 300
    startY = 130
    height = 60
    for i in range(3):
        drawRect(startX, startY + i*gap, width, height, fill=None, border='black')
        if i == 0:
            label = "Easy"
        elif i == 1:
            label = 'Medium'
        elif i == 2:
            label = "Hard"
        drawLabel(label, startX + width//2, startY + i*gap + height//2, bold=True, font='serif', size = 40)

def levelsToGame(app, mouseX, mouseY):
    if 530 <= mouseX <= 830 and 130 <= mouseY <= 190:
        app.currentLevel = 'easy'
        app.gameState = 'gameplay'
        plantPanel(app)
    elif 530 <= mouseX <= 830 and 220 <= mouseY <= 280:
        app.currentLevel = 'medium'
        app.gameState = 'gameplay'
        plantPanel(app)
    elif 530 <= mouseX <= 830 and 310 <= mouseY <= 370:
        app.currentLevel = 'hard'
        app.gameState = 'gameplay'
        plantPanel(app)

def plantPanel(app):
    # add plants from plants.py
    # app.plantsPanelList.append(Sunflower(app.plantPanelX + 104, app.plantPanelY + app.plantPanelHeight/2))  # Sunflower
    # app.plantsPanelList.append(PeaShooter(app.plantPanelX + 200, app.plantPanelY + app.plantPanelHeight/2))  # PeaShooter
    # app.plantsPanelList.append(IcePeaShooter(app.plantPanelX + 250, app.plantPanelY + app.plantPanelHeight/2)) #icePeaShooter
    app.plantsPanelList = []
    print('---')
    startX = app.plantPanelX + 104
    y = app.plantPanelY + app.plantPanelHeight/2
    spacing = 50
    plantTypes = Levels[app.currentLevel]['plants']

    
    for plant in plantTypes:
        # print(plant)
        # print('---')
        app.plantsPanelList.append(plant(startX, y))
        print(app.plantsPanelList)
    
    index = 0
    for plant in app.plantsPanelList:
        plant.x = plant.x + spacing * index
        index += 1
        
    
