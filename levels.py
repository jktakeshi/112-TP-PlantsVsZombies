from cmu_graphics import *
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
        'finalWaveTypes': [regularZombie],
        'finalWaveDelay': 8
    },
    'medium': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 10,
        'finalWaveSpawnRate': 8,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 20,
        'finalWaveTypes': [regularZombie, coneHeadZombie],
        'finalWaveDelay': 8,
        'coneHeadLimit': 5
    },
    'hard': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter, melon, Wallnut],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 9,
        'finalWaveSpawnRate': 7,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 40,
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
        app.gameState = 'preGame'
        plantPanel(app)
    elif 530 <= mouseX <= 830 and 220 <= mouseY <= 280:
        app.currentLevel = 'medium'
        app.gameState = 'preGame'
        plantPanel(app)
    elif 530 <= mouseX <= 830 and 310 <= mouseY <= 370:
        app.currentLevel = 'hard'
        app.gameState = 'preGame'
        plantPanel(app)

class Shovel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y
        path = 'shovelIcon.png'
        image = Image.open(path)
        self.image = CMUImage(image)
    def drawShovel(self):
        drawImage(self.image, self.x, self.y, align='center', width = 45, height = 50)
    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY


def plantPanel(app):
    app.plantsPanelList = []
    startX = app.plantPanelX + 104
    y = app.plantPanelY + app.plantPanelHeight/2
    spacing = 50
    plantTypes = Levels[app.currentLevel]['plants']

    for plant in plantTypes:
        app.plantsPanelList.append(plant(startX, y))
    
    index = 0
    for plant in app.plantsPanelList:
        plant.x = plant.x + spacing * index
        index += 1
    

def spawnZombies(app, currLevel):
    currTime = app.counter/app.stepsPerSecond
    gameLevel = Levels[currLevel]

    # final wave status
    if app.zombiesSpawned == gameLevel['preFinalWaveZombies'] and len(app.zombiesList) == 0 and not app.finalWave:
        if app.finalWaveStartTimer == None:
            app.drawFinalLabel = True
            app.finalWaveStartTimer = currTime
        if currTime - app.finalWaveStartTimer > gameLevel['finalWaveDelay']:
            app.finalWave = True
            app.finalWaveLabel = True
            app.finalLabelTimer = app.counter
            app.finalLabelOpacity = 0
    
    spawnRate = gameLevel['zombieSpawnRate']
    if currLevel in ['hard', 'medium']:
        time = currTime
        rateFactor = min(4.0, 1.0 + (time/300))
        spawnRate /= rateFactor

    # creating intervals for zombies to spawn
    if currTime > gameLevel['startZombieSpawn'] and not app.finalWave:
        if app.zombiesSpawned < gameLevel['preFinalWaveZombies']:
            if currTime % spawnRate < (1/app.stepsPerSecond):
                if currLevel == 'hard':
                    row = smartZombieRow(app)
                else:
                    row = random.choice(range(app.rows))
                zombieType = random.choice(gameLevel['zombies'])
                zombieX, zombieY = getZombieLoc(app, row)
                newZombie = zombieType(zombieX, zombieY)
                app.zombiesList.append(newZombie)
                app.zombiesSpawned += 1
    
    # Final wave
    if app.finalWave:
        if app.finalWaveSpawned < gameLevel['finalWaveZombies']:
            if currTime % spawnRate < 0.8:
                if currLevel == 'hard':
                    row = smartZombieRow(app)
                else:
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

def smartZombieRow(app):
    cellHeight = app.boardHeight/app.rows
    # getting the number of plants per row
    plantCountsRow = [0] * app.rows
    for plant in app.plantsGridList:
        for row in range(app.rows):
            rowTop = app.boardTop + cellHeight*row
            rowBottom = rowTop + cellHeight
            if rowTop <= plant.y <= rowBottom:
                plantCountsRow[row] += 1
    minPlantCount = min(plantCountsRow)
    rowsWithMinPlants = [row for row in range(len(plantCountsRow)) if plantCountsRow[row]==minPlantCount]

    # 90% likelihood for rows with least plants
    if random.random() < 0.9:
        return random.choice(rowsWithMinPlants)
    else:
        return random.choice(range(app.rows))

def getZombieLoc(app, row):
    cellHeight = app.boardHeight/app.rows
    zombieX = app.boardLeft + app.boardWidth + 10
    zombieY = app.boardTop + row * cellHeight + cellHeight//2
    return zombieX, zombieY