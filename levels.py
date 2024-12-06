from cmu_graphics import *
from plants import *
from zombies import *
from PIL import Image
import random
from time import *

# citation: https://gombis.com/vm/plants-vs-zombies searched on google (thumbnail)
path = 'images/levelSelector.png'
image = Image.open(path)
app.levelSelector = CMUImage(image)
Levels = {
    'easy': {
        'plants': [Sunflower, PeaShooter, Wallnut],
        'zombies': [regularZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 13,
        'finalWaveSpawnRate': 10,
        'preFinalWaveZombies': 10,
        'finalWaveZombies': 15,
        'finalWaveTypes': [regularZombie],
        'finalWaveDelay': 8
    },
    'medium': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter, Wallnut, BouncePlant],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 11,
        'finalWaveSpawnRate': 9,
        'preFinalWaveZombies': 15,
        'finalWaveZombies': 20,
        'finalWaveTypes': [regularZombie, coneHeadZombie],
        'finalWaveDelay': 8,
        'coneHeadLimit': 5
    },
    'hard': {
        'plants': [Sunflower, PeaShooter, IcePeaShooter, melon, Wallnut, BouncePlant],
        'zombies': [regularZombie, coneHeadZombie],
        'startZombieSpawn': 10,
        'zombieSpawnRate': 11,
        'finalWaveSpawnRate': 8,
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
    startX = 555
    width = 300
    startY = 130
    height = 90
    for i in range(3):
        if i == 0:
            label = "Easy"
        elif i == 1:
            label = 'Medium'
        elif i == 2:
            label = "Hard"
        # citation: https://plantsvszombies.fandom.com/wiki/Plants_vs._Zombies_2/Gallery_of_plant_sprites
        drawImage('images/selectLevelPanel.png', startX + width//2 - i*20, startY + i*gap + height//2, align='center')
        drawLabel(label, startX + width//2 - i*20, startY + i*gap + height//2, bold=True, font='serif', size = 40, rotateAngle=8)
        
def levelsToGame(app, mouseX, mouseY):
    if 548 <= mouseX <= 842 and 110 <= mouseY <= 190:
        app.currentLevel = 'easy'
        app.gameState = 'preGame'
        plantPanel(app)
    elif 528 <= mouseX <= 830 and 245 <= mouseY <= 290:
        app.currentLevel = 'medium'
        app.gameState = 'preGame'
        plantPanel(app)
    elif 508 <= mouseX <= 830 and 332 <= mouseY <= 422:
        app.currentLevel = 'hard'
        app.gameState = 'preGame'
        plantPanel(app)

class Shovel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y
        # citation: https://plantsvszombies.fandom.com/wiki/Shovel
        path = 'images/shovelIcon.png'
        image = Image.open(path)
        self.image = CMUImage(image)
    def drawShovel(self):
        drawImage(self.image, self.x, self.y, align='center', width = 45, height = 50)
    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY

class TargetIcon:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y
        # citation: https://en.ac-illust.com/clip-art/24289523/target-icon-red
        path = 'images/targetIcon.png'
        image = Image.open(path)
        self.image = CMUImage(image)
        self.coolDownTime = 30
        self.coolingDown = False
        self.startCoolDownTime = None
        self.seedOpacity = 100

        # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot?file=Seed_Slot.png
        self.seedImagePath = 'images/emptySeedSelector.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)

    def drawTarget(self):
        drawImage(self.image, self.x, self.y, align='center', width = 45, height = 50)

    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY

    def drawTargetSeed(self):
        drawImage(self.image, self.x, self.y, align='center', width = 45, height = 50)
        drawImage(self.seedImage, self.originalX, self.originalY, align='center', width = 45, height = 50)
        if self.coolingDown:
            elapsed = time() - self.startCoolDownTime
            self.seedOpacity = max(0, (1 - (elapsed/self.coolDownTime))*100)
            drawRect(self.x-45/2, self.y-50/2, 45, 50, 
                     fill='black', opacity=self.seedOpacity)
            if elapsed >= self.coolDownTime:
                self.startCoolDownTime = None
                self.startCoolDownTime = 100
                self.coolingDown = False

    def isCoolingDown(self):
        if self.startCoolDownTime == None:
            self.startCoolDownTime = time()
        elapsed = time() - self.startCoolDownTime
        if elapsed > self.coolDownTime:
            self.coolingDown = False
            self.startCoolDownTime = None
        else:
            self.coolingDown = True

    def copyTarget(self):
        return self.__class__(self.originalX, self.originalY)


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
            app.finalWaveStartTimer = app.counter/app.stepsPerSecond
        elapsedTime = currTime - app.finalWaveStartTimer 
        if 2 <= (elapsedTime) <= 6:
            app.drawFinalLabel = True
        elif elapsedTime > 6: 
            app.drawFinalLabel = False
            app.finalWave = True
            app.finalWaveStartTimer = None
    
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
        if app.finalWaveStartTimer == None:
            app.finalWaveStartTimer = currTime
        elapsedTime = currTime - app.finalWaveStartTimer
        # gradual increase in spawning of zombies
        finalSpawnRate = gameLevel['finalWaveSpawnRate'] - (elapsedTime/50)

        if app.finalWaveSpawned < gameLevel['finalWaveZombies']:
            if currTime % finalSpawnRate < 0.3:
                if currLevel in ['hard', 'medium']:
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

    # moving zombies diagonally based on row plant damage
    if currLevel == 'hard':
        if currTime > 60:
            plantRowsDamage = calculateRowsDamage(app)
            for zombie in app.zombiesList:
                cellHeight = app.boardHeight/app.rows
                changeZombieRow(zombie, plantRowsDamage, cellHeight)

def smartZombieRow(app):
    plantRowsDamage = calculateRowsDamage(app)
    minDamageCount = min(plantRowsDamage)
    rowsWithMinDamage = [row for row in range(len(plantRowsDamage)) if plantRowsDamage[row]==minDamageCount]
    
    # 90% likelihood for rows with least plants
    if random.random() < 0.9:
        return random.choice(rowsWithMinDamage)
    else:
        return random.choice(range(app.rows))

def changeZombieRow(zombie, plantRowsDamage, cellHeight):
    if zombie.changedRows < 2:
        currRow = int((zombie.y - app.boardTop)/cellHeight)
        if  0 <= currRow < app.rows:
            adjRows = [row for row in [currRow-1, currRow+1] if 0 <= row < app.rows]
            for adjRow in adjRows:
                if plantRowsDamage[adjRow] < plantRowsDamage[currRow]:
                    zombie.changeRow(adjRow, app)
                    zombie.changedRows += 1
                    break

def getZombieLoc(app, row):
    cellHeight = app.boardHeight/app.rows
    zombieX = app.boardLeft + app.boardWidth + 10
    zombieY = app.boardTop + row * cellHeight + cellHeight//2
    return zombieX, zombieY

def calculateRowsDamage(app):
    cellHeight = app.boardHeight/app.rows
    # getting the number of plants per row
    plantRowsDamage = [0] * app.rows
    for plant in app.plantsGridList:
        for row in range(app.rows):
            rowTop = app.boardTop + cellHeight*row
            rowBottom = rowTop + cellHeight
            if rowTop <= plant.y <= rowBottom:
                plantRowsDamage[row] += plant.damage
    return plantRowsDamage