from plants import *
from zombies import *
from PIL import Image
import random
from time import *

path = 'levelSelector.png'
image = Image.open(path)
app.levelSelector = CMUImage(image)

Levels = {
    'easy': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter],
        'zombies': [regularZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 13,
        'finalWaveSpawnRate': 10,
        'preFinalWaveZombies': 1,
        'finalWaveZombies': 10,
        'finalWaveTypes': [regularZombie, coneHeadZombie],
        'finalWaveDelay': 8
    },
    'medium': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 10,
        'finalWaveSpawnRate': 8,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 15,
        'finalWaveTypes': [regularZombie, coneHeadZombie, bucketHeadZombie],
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
    startX = app.plantPanelX + 104
    y = app.plantPanelY + app.plantPanelHeight/2
    spacing = 50
    plantTypes = Levels[app.currentLevel]['plants']

    
    for plant in plantTypes:
        # print(plant)
        # print('---')
        app.plantsPanelList.append(plant(startX, y))
    
    index = 0
    for plant in app.plantsPanelList:
        plant.x = plant.x + spacing * index
        index += 1
        
def spawnZombies(app, currLevel):
    currTime = app.counter/app.stepsPerSecond
    # print(currTime)
    gameLevel = Levels[currLevel]
    # final wave status
    if app.zombiesSpawned == gameLevel['preFinalWaveZombies'] and len(app.zombiesList) == 0 and not app.finalWave:
        if app.finalWaveStartTimer == None:
            app.drawFinalLabel = True
            app.finalWaveStartTimer = currTime
            print(f'{time()}, {app.finalWave}')
        if currTime - app.finalWaveStartTimer > gameLevel['finalWaveDelay']:
            print(currTime - app.finalWaveStartTimer)
            app.finalWave = True
            app.finalWaveLabel = True
            app.finalLabelTimer = app.counter
            app.finalLabelOpacity = 0
    # creating intervals for zombies to spawn
    if currTime > gameLevel['startZombieSpawn'] and not app.finalWave:
        if app.zombiesSpawned < gameLevel['preFinalWaveZombies']:
            if (app.counter/app.stepsPerSecond) % gameLevel['zombieSpawnRate'] == 0:
                zombieType = random.choice(gameLevel['zombies'])
                # spawning zombies based on wave
                # if app.zombiesSpawned < gameLevel['preFinalWaveZombies']:
                #     zombieType = random.choice(gameLevel['zombies'])
                # else:
                #     zombieType = random.choice(gameLevel['finalWaveTypes'])
                
                row = random.choice(range(app.rows))
                zombieX, zombieY = getZombieLoc(app, row)
                newZombie = zombieType(zombieX, zombieY)
                app.zombiesList.append(newZombie)
                app.zombiesSpawned += 1
        # elif app.zombiesSpawned == gameLevel['preFinalWaveZombies'] and not finalWave:
        # shouldnt be needing the line above if finalWave works
    
    # Final wave
    if app.finalWave:
        if app.finalWaveSpawned < gameLevel['finalWaveZombies']:
            if (app.counter/app.stepsPerSecond) % gameLevel['finalWaveSpawnRate'] == 0:
                row = random.choice(range(app.rows))
                zombieX, zombieY = getZombieLoc(app, row)
                if app.finalWaveSpawned == 0:
                    newZombie = flagZombie(zombieX, zombieY)
                else:
                    zombieType = random.choice(gameLevel['finalWaveTypes'])
                    newZombie = zombieType(zombieX, zombieY)
                app.zombiesList.append(newZombie)
                app.finalWaveSpawned += 1
        elif app.finalWaveSpawned == gameLevel['finalWaveZombies'] and len(app.zombiesList) == 0:
            app.gameOverWin = True
        
def getZombieLoc(app, row):
    cellHeight = app.boardHeight/app.rows
    zombieX = app.boardLeft + app.boardWidth + 10
    zombieY = app.boardTop + row * cellHeight + cellHeight//2
    return zombieX, zombieY