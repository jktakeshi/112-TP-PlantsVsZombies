from cmu_graphics import *
from plants import *
from zombies import *
from levels import *
from preGame import *
from titleScreen import *
from parabolicMotion import *
from projectile import *
from gravity import *
from PIL import Image
import math
import random
import copy
from autoplay import *

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

def onAppStart(app):
    app.gameState = 'titleScreen'
    app.shovel = None
    app.shovelSelected = False

    app.target = TargetIcon(772,37)
    app.targetSelected = False
    app.copiedTarget = None

    # frontyard
    # citation: https://pvz-rp.fandom.com/wiki/Player%27s_House
    path = 'images/frontyard.png'
    image = Image.open(path)
    app.frontYard = CMUImage(image)

    # seed slot
    # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot
    path = 'images/emptySeedSlot.png'
    image = Image.open(path)
    app.seedSlot = CMUImage(image)

    # empty seed selector
    # citation = https://plantsvszombies.fandom.com/wiki/Seed_slot?file=Seed_Slot.png
    path = 'images/emptySeedSelector.png'
    image = Image.open(path)
    app.emptySeedSelector = CMUImage(image)

    # citation: https://plantsvszombies.fandom.com/wiki/Shovel
    path = 'images/shovel.png'
    image = Image.open(path)
    app.shovelIcon = CMUImage(image)

    # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot?file=Seed_Slot.png
    path = 'images/emptySeedSelector.png'
    image = Image.open(path)
    app.emptyTargetIcon = CMUImage(image)

    # citation: https://en.ac-illust.com/clip-art/24289523/target-icon-red
    path = 'images/targetIcon.png'
    image = Image.open(path)
    app.targetIcon = CMUImage(image)

    # citation: https://www.vectorstock.com/royalty-free-vector/pause-play-button-icon-vector-26538112
    path = 'images/playPauseButton.png'
    image = Image.open(path)
    app.playPauseButton = CMUImage(image)

    # citation: https://www.bilibili.tv/en/video/2041211460 thumbnail of the video (searched on google)
    path = 'images/finalWave.png'
    image = Image.open(path)
    app.finalWaveImage = CMUImage(image)

    # plant panel
    app.plantsPanelList = []
    app.plantPanelX = 230
    app.plantPanelY = 2
    app.plantPanelWidth = 450
    app.plantPanelHeight = 70

    # plants on grid
    app.plantsGridList = []
    app.plantsLocation = []
    app.selectedPlant = None
    app.selectedPlantSeed = None
    app.current = None
 

    app.zombiesList = []
    app.projectileList = []

    app.rows, app.cols = 5, 9
    app.cellSize = 30
    app.boardLeft = 240
    app.boardTop = 75
    app.boardWidth = 700 
    app.boardHeight = 475

    app.sunList = []
    app.sunPoints = 50

    app.currentLevel = 'easy'
    app.counter = 0
    app.finalWave = False
    app.zombiesSpawned = 0
    app.finalWaveSpawned = 0

    app.gameOverLose = False
    app.gameOverWin = False
    app.paused = True
    plantPanel(app)

    app.finalWaveStartTimer = None
    # final wave label
    app.finalWaveLabel = False
    app.drawFinalLabel = False
    app.finalLabelTimer = 0
    app.finalLabelDuration = 3
    app.finalLabelFadeTime = 2
    app.finalLabelOpacity = 0

    app.gravity = False
    app.gravityLoc = None
    app.gravityLocSelect = False
    app.gravityPull = 5000
    app.gravityRadius = 280
    app.gravityStartTime = None
    app.gravityDuration = 4

    app.autoplay = False
    app.autoplayCount = 0
    app.autoplayStatus = 'Off'

# plant panel outline
def drawPlantPanel(app):
    drawRect(app.plantPanelX, app.plantPanelY, app.plantPanelWidth, app.plantPanelHeight, fill=None)
    for plant in app.plantsPanelList:
        plant.drawPlantSeed()
        
def onMousePress(app, mouseX, mouseY):
    if app.gameState == 'titleScreen':
        titleToLevels(app, mouseX, mouseY)

    elif app.gameState == 'levels':
        levelsToGame(app, mouseX, mouseY)

    for plant in app.plantsPanelList:
        if distance(mouseX, mouseY, plant.x, plant.y) <= 25:
            if plant.sunCost <= app.sunPoints and plant.coolingDown == False:
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
                app.selectedPlant.x, app.selectedPlant.y = mouseX, mouseY
            break

    # sun collection
    for sun in copy.copy(app.sunList):
        if sun.isCollected(mouseX, mouseY):
            app.sunList.remove(sun)
            app.sunPoints += 25
            return
    # shovel selection
    if distance(mouseX, mouseY, 715, 37) <= 25:
        app.shovel = Shovel(715,37)
        app.shovelSelected = True
    
    # gravity effect
    if distance(mouseX, mouseY, 772, 37) <= 25:
        app.copiedTarget = app.target.copyTarget()
        if app.target.coolingDown == False:
            app.targetSelected = True
            app.gravity = True
            app.gravityLocSelect = True
            app.gravityLoc = (mouseX, mouseY)
            app.copiedTarget.x, app.copiedTarget.y = mouseX, mouseY
    # autoplay
    if distance(mouseX, mouseY, 829, 37) <= 25:
        if app.autoplayCount%2 == 0:
            app.autoplay = True
            app.autoplayStatus = 'On'
        else: 
            app.autoplay = False
            app.autoplayStatus = 'Off'
        app.autoplayCount += 1

def onMouseDrag(app, mouseX, mouseY):
    if app.selectedPlant:
        app.selectedPlant.x, app.selectedPlant.y = mouseX, mouseY
    if app.shovelSelected:
        app.shovel.x, app.shovel.y = mouseX, mouseY
    if app.targetSelected:
        app.copiedTarget.x, app.copiedTarget.y = mouseX, mouseY
        app.gravityLoc = (mouseX, mouseY)

def onMouseRelease(app, mouseX, mouseY):
    if app.selectedPlant:
        cell = getCell(app, mouseX, mouseY)
        if cell:
            row, col  = cell
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            app.selectedPlant.x = cellLeft + cellWidth / 2
            app.selectedPlant.y = cellTop + cellHeight / 2
            if (app.selectedPlant.x, app.selectedPlant.y) not in app.plantsLocation:
                app.plantsGridList.append(app.selectedPlant)
                app.plantsLocation.append((app.selectedPlant.x, app.selectedPlant.y))
                app.sunPoints -= app.selectedPlant.sunCost
                app.selectedPlant = None
                app.currentPlant.isCoolingDown()

            else: # resets selected plant to the panel if placed on a cell where there is
                  # already a plant
                app.selectedPlant.resetPosition() 
                app.selectedPlant = None
        else:
            # resets selected plant to the panel if it is not dropped on a valid cell on the grid
            app.selectedPlant.resetPosition()
            app.selectedPlant = None
    if app.shovelSelected:
        cell = getCell(app, mouseX, mouseY)
        if cell:
            row, col  = cell
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            selectedX = cellLeft + cellWidth / 2
            selectedY = cellTop + cellHeight / 2
            if (selectedX, selectedY) in app.plantsLocation:
                index = app.plantsLocation.index((selectedX, selectedY))
                app.sunPoints += app.plantsGridList[index].sunCost
                app.plantsGridList.pop(index)
                app.plantsLocation.pop(index)
                
        app.shovel.resetPosition()
        app.shovelSelected = False
    
    if app.targetSelected:
        app.gravityLoc = (mouseX, mouseY)
        app.gravityStartTime = app.counter/app.stepsPerSecond
        app.gravityLocSelect = False
        app.copiedTarget.resetPosition()
        app.copiedTargetSelected = False
        cell = getCell(app, mouseX, mouseY)
        
        if not cell:
            app.gravity = False
            app.targetSelected = False
        else:
            app.target.isCoolingDown()
            app.targetSelected = True

def onKeyPress(app, key):
    if key == "space":
        app.gameState = 'gameplay'
        app.paused = False
        plantPanel(app)


def onStep(app):
    if app.autoplay:
        collectSun(app)
        plantDecision(app)

    if not app.gameOverLose and not app.gameOverWin and not app.paused:
        app.counter += 1
        spawnZombies(app, app.currentLevel)

        #plant shooting projectile
        for plant in app.plantsGridList:
            zombiesInRow = [zombie for zombie in app.zombiesList if abs(zombie.y - plant.y) < 10]
            if zombiesInRow and plant.canShoot():
                predictedX, predictedY = predictContact(plant.x, plant.y, zombiesInRow[0], steps = 1000, travelTime = 2.0)
                if isinstance(plant, melon):
                    projectile = plant.shoot(predictedX, predictedY)
                else:
                    projectile = plant.shoot()
                app.projectileList.append(projectile)

        # move projectile
        for projectile in app.projectileList:
            projectile.move()

            # gavity effect
            if app.gravity and app.gravityLoc:
                projectile.applyGravity(app.gravityLoc)
                if projectile.reachedGravityCenter:
                    app.projectileList.remove(projectile)
            # checking for collision
            for zombie in app.zombiesList:
                if projectile.checkCollision(zombie):
                    projectile.inMotion = False
                    # for slow down effect
                    if isinstance(projectile, icePeaShot):
                        projectile.slowDownEffect(zombie)

                    projectile.damageZombie(zombie, projectile.damage)
                    # bouncing projectile effect
                    if isinstance(projectile, bounceProjectile):
                        if projectile.speed > 0:
                            projectile.bounce(app, zombie, cellHeight = app.boardHeight/app.rows)
                            if projectile.speed <= 2:
                                if projectile in app.projectileList:
                                    app.projectileList.remove(projectile)
                        if projectile in app.projectileList and not projectile.isBouncing:
                            app.projectileList.remove(projectile)

                    else:
                        projectile.inMotion = False
                        if projectile in app.projectileList:
                            app.projectileList.remove(projectile)
                    if 0 < zombie.health <= zombie.lowHealth:
                        zombie.heavyDamage()
                    elif zombie.health <= 0:
                        app.zombiesList.remove(zombie)
            # if projectile.y == zombie.y:
            #     app.projectileList.remove(projectile)

        # move zombie and check for collision with plant
        for zombie in app.zombiesList:
            zombie.moveZombie()
            for plant in app.plantsGridList:
                if zombie.collisionWithPlant(plant):
                    zombie.inMotion = False
                    zombie.damagePlant(plant, zombie.damage/app.stepsPerSecond)
                if plant.health <= 0:
                    zombie.inMotion = True
                    app.plantsGridList.remove(plant)
        
        # gravity and effect duration
        if app.gravity and app.gravityStartTime != None:
            elapsedTime = app.counter/app.stepsPerSecond - app.gravityStartTime 
            if elapsedTime >= app.gravityDuration:
                deactivateGravity(app)        
        
        # generating sun from the top of the screen
        if app.counter % (app.stepsPerSecond * 10) == 0:
            sunX = random.randint(app.boardLeft, app.boardLeft + app.boardWidth)
            app.sunList.append(Sun(sunX, 0))

        # generating sun from Sunflower
        for plant in app.plantsGridList:
            if isinstance(plant, Sunflower):
                sun = plant.createSun()
                if sun:
                    app.sunList.append(sun)
        
        # moving and removing sun
        for sun in copy.copy(app.sunList):
            sun.move()
            if sun.isExpired():
                app.sunList.remove(sun)

        if not app.gameOverLose and not app.gameOverWin:
            for zombie in app.zombiesList:
                if zombie.x <= app.boardLeft - 40:
                    app.gameOverLose = True

def drawGameOver(app):
    # citation: https://plantsvszombies.fandom.com/wiki/Brain/Gallery
    path = 'images/gameOver.png'
    image = Image.open(path)
    gameOverLoseSign = CMUImage(image)

    winPath = 'images/gameOverWin.png'
    winImage = Image.open(winPath)
    gameOverWinSign = CMUImage(winImage)
    if app.gameOverLose:
        drawRect(0, 0, app.width, app.height, opacity=60)
        drawImage(gameOverLoseSign, app.width/2, app.height/2, align='center')
    elif app.gameOverWin:
        drawRect(0, 0, app.width, app.height, opacity=60)
        drawImage(gameOverWinSign, app.width/2, app.height/2, align='center')

# drawing grid (from CS Academy)
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = None if (row+col) % 2 == 0 else None
            drawCell(app, row, col, color)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = color)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth/app.cols
    cellHeight = app.boardHeight/app.rows
    return (cellWidth, cellHeight)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None
    
def redrawAll(app):
    # citation: https://rainyday.blog/2015/07/31/first-impressions-plants-vs-zombies/
    if app.gameState == 'titleScreen':
        drawTitleScreen(app)

    elif app.gameState == 'levels': 
        drawLevelSelector(app)

    elif app.gameState == 'preGame': 
        drawPregame(app)

    elif app.gameState == 'gameplay' and not app.paused:
        drawImage(app.frontYard, 0, 0, width=app.width, height=app.height)
        drawImage(app.seedSlot, 230, 2, width=app.plantPanelWidth, height=app.plantPanelHeight)
        drawImage(app.shovelIcon, 715, 37, align='center', width = 45, height = 50)
        drawLabel(f'{app.sunPoints}', 270, 60, bold = True)
        drawGrid(app)
        drawPlantPanel(app)
        
        if app.selectedPlant:
            app.selectedPlant.drawPlant()
        if app.shovel:
            app.shovel.drawShovel()
        if app.target:
            app.target.drawTargetSeed()
        drawImage(app.targetIcon, 772, 37, align='center', width = 45, height = 50)
        drawImage(app.emptySeedSelector, 829, 37, align='center', width = 45, height = 50)
        drawImage(app.playPauseButton, 829, 37, align='center', width = 45, height = 50)
        drawImage(app.emptySeedSelector, 851, 12, width = 90, height = 50)
        drawLabel(f'Autoplay: {app.autoplayStatus}', 896, 37, font = 'serif', bold=True)


        if app.copiedTarget:
            app.copiedTarget.drawTarget()
        
        
        for plant in app.plantsGridList:
            plant.drawPlant()
        
        for zombie in app.zombiesList:
            zombie.drawZombie()
        
        for projectile in app.projectileList:
            projectile.draw()

        for sun in app.sunList:
            sun.drawPlant()

        drawGameOver(app)
        
        if app.drawFinalLabel:
            drawImage(app.finalWaveImage, app.width/2, app.height/2, align='center')
           
        if app.gravity and app.gravityLoc and app.target:
            cx, cy = app.gravityLoc
            drawCircle(cx, cy, app.gravityRadius, fill = 'gray', opacity=50)
        
        if app.gravityLocSelect:
            drawLabel("Select a spot", app.width/2, app.height/2, size = 40,
                      bold = True, align='center', font='serif')


def main():
    runApp(width = 978, height = 575)

main()
