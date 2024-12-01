from cmu_graphics import *
from plants import *
from zombies import *
from levels import *
from titleScreen import *
import math
import random
import copy

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

def onAppStart(app):
    app.gameState = 'titleScreen'

    # frontyard
    path = 'frontyard.png'
    image = Image.open(path)
    app.frontYard = CMUImage(image)

    # seed slot
    path = 'emptySeedSlot.png'
    image = Image.open(path)
    app.seedSlot = CMUImage(image)

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
    app.paused = False
    plantPanel(app)

    app.finalWaveStartTimer = None
    # final wave label
    app.finalWaveLabel = False
    app.drawFinalLabel = False
    app.finalLabelTimer = 0
    app.finalLabelDuration = 3
    app.finalLabelFadeTime = 2
    app.finalLabelOpacity = 0


# adding "plants" to the plant panel
# there will be changes for different levels
#   first level will just have sunflower, peashooter, icepea


# def plantPanel(app):
#     # add plants from plants.py
#     # app.plantsPanelList.append(Sunflower(app.plantPanelX + 104, app.plantPanelY + app.plantPanelHeight/2))  # Sunflower
#     # app.plantsPanelList.append(PeaShooter(app.plantPanelX + 200, app.plantPanelY + app.plantPanelHeight/2))  # PeaShooter
#     # app.plantsPanelList.append(IcePeaShooter(app.plantPanelX + 250, app.plantPanelY + app.plantPanelHeight/2)) #icePeaShooter

#     startX = app.plantPanelX + 104
#     y = app.plantPanelY + app.plantPanelHeight/2
#     spacing = 50
#     plantTypes = Levels[app.currentLevel]['plants']

#     for plant in plantTypes:
#         app.plantsPanelList.append(plant(startX, y))
#         print(app.plantsPanelList)
    
#     index = 0
#     for plant in app.plantsPanelList:
#         plant.x = plant.x + spacing * index
#         index += 1


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
            if plant.sunCost <= app.sunPoints:
                app.selectedPlant = plant.copyPlant()
                app.selectedPlant.x, app.selectedPlant.y = mouseX, mouseY
            break

    # sun collection
    for sun in copy.copy(app.sunList):
        if sun.isCollected(mouseX, mouseY):
            app.sunList.remove(sun)
            app.sunPoints += 25
            return

def onMouseDrag(app, mouseX, mouseY):
    if app.selectedPlant:
        app.selectedPlant.x, app.selectedPlant.y = mouseX, mouseY

def onMouseRelease(app, mouseX, mouseY):
    if app.selectedPlant:
        cell = getCell(app, mouseX, mouseY)
        if cell:
            row, col  = cell
            cellLeft, cellTop = getCellLeftTop(app, row, col)
            cellWidth, cellHeight = getCellSize(app)
            app.selectedPlant.x = cellLeft + cellWidth // 2
            app.selectedPlant.y = cellTop + cellHeight // 2
            if (app.selectedPlant.x, app.selectedPlant.y) not in app.plantsLocation:
                app.plantsGridList.append(app.selectedPlant)
                app.plantsLocation.append((app.selectedPlant.x, app.selectedPlant.y))
                app.sunPoints -= app.selectedPlant.sunCost
                app.selectedPlant = None
            else: # resets selected plant to the panel if placed on a cell where there is
                  # already a plant
                app.selectedPlant.resetPosition() 
                app.selectedPlant = None
        else:
            # resets selected plant to the panel if it is not dropped on a valid cell on the grid
            app.selectedPlant.resetPosition()
            app.selectedPlant = None

def onStep(app):
    if not app.gameOverLose and not app.gameOverWin and not app.paused:
        app.counter += 1
        spawnZombies(app, app.currentLevel)

        #plant shooting projectile
        for plant in app.plantsGridList:
            zombiesInRow = [zombie for zombie in app.zombiesList if abs(zombie.y - plant.y) < 10]
            if zombiesInRow and plant.canShoot():
                projectile = plant.shoot()
                app.projectileList.append(projectile)

        # move zombie and check for collision with plant
        for zombie in app.zombiesList:
            zombie.moveZombie()
            for plant in app.plantsGridList:
                if zombie.collisionWithPlant(plant):
                    # do smth with onstep to take care of damageplant
                    zombie.damagePlant(plant, (zombie.damage)/30)
                    if plant.health <= 0:
                        app.plantsGridList.remove(plant)
                        zombie.inMotion = True

        # move projectile and check for collision
        for projectile in app.projectileList:
            projectile.move()
            for zombie in app.zombiesList:
                if projectile.checkCollision(zombie):
                    if isinstance(projectile, icePeaShot):
                        projectile.slowDownEffect(zombie)
                        print(zombie.slowDownEnd)
                    projectile.damageZombie(zombie, projectile.damage)
                    projectile.inMotion = False
                    if zombie.health <= 0:
                        app.zombiesList.remove(zombie)
                    if projectile in app.projectileList:
                        app.projectileList.remove(projectile)
        
        # generating sun from the top of the screen
        if app.counter % 300 == 0:
            sunX = random.randint(app.boardLeft, app.boardLeft + app.boardWidth)
            app.sunList.append(Sun(sunX, 0))

        # generating sun from Sunflower
        for plant in app.plantsGridList:
            if isinstance(plant, Sunflower):
                sun = plant.createSun()
                if sun:
                    app.sunList.append(sun)
        
        # moving and removing sun
        for sun in copy.copy(app.sunList): # edit this; prolly use copy
            sun.move()
            if sun.isExpired():
                app.sunList.remove(sun)

        if not app.gameOverLose and not app.gameOverWin:
            for zombie in app.zombiesList:
                if zombie.x <= app.boardLeft - 40:
                    app.gameOverLose = True
        # animating final wave label
        
        if app.drawFinalLabel:
            elapsedTime = (app.counter-app.finalLabelTimer)/app.stepsPerSecond
            if elapsedTime < app.finalLabelFadeTime: #fading in
                app.finalLabelOpacity = elapsedTime/app.finalLabelFadeTime
            elif elapsedTime < app.finalLabelDuration + app.finalLabelFadeTime:
                app.finalLabelOpacity = 100
            elif elapsedTime < app.finalLabelDuration + (2*app.finalLabelFadeTime): #fading out
                remaining = (app.finalLabelDuration + (2*app.finalLabelFadeTime)) - elapsedTime
                app.finalLabelOpacity = remaining/app.finalLabelFadeTime
            else: app.finalLabel = False

def drawGameOver(app):
    path = 'gameOver.png'
    image = Image.open(path)
    gameOverLoseSign = CMUImage(image)
    if app.gameOverLose:
        drawRect(0, 0, app.width, app.height, opacity=60)
        drawImage(gameOverLoseSign, app.width//2, app.height//2, align='center')
        # drawLabel("Game Over", app.width//2, app.height//2, bold=True, size=50, font='serif')
        # drawLabel("The Zombies Ate Your Brains!", app.width//2, app.height//2 + 50, fill='red', bold=True, size=50, font='serif')
    elif app.gameOverWin:
        drawLabel("Game Over", app.width//2, app.height//2, bold=True, size=50, font='serif')
        drawLabel("You won!", app.width//2, app.height//2 + 50, fill='red', bold=True, size=50, font='serif')

#Grid
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = None if (row+col) % 2 == 0 else None #lightgreen and green
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
    else: #this causes error if user doesnt move the plant to the grid
      return None
    

def redrawAll(app):
    if app.gameState == 'titleScreen':
        drawTitleScreen(app)

    elif app.gameState == 'levels': #change this
        drawLevelSelector(app)

    elif app.gameState == 'gameplay':
        drawImage(app.frontYard, 0, 0, width=app.width, height=app.height)
        drawImage(app.seedSlot, 230, 2, width=app.plantPanelWidth, height=app.plantPanelHeight)
        drawLabel(f'{app.sunPoints}', 270, 60, bold = True)
        drawGrid(app)
        drawPlantPanel(app)
        drawGameOver(app)
        if app.selectedPlant:
            app.selectedPlant.drawPlant()
        # draw all the plants and zombies in their respective lists
        for plant in app.plantsGridList:
            plant.drawPlant()
        
        for zombie in app.zombiesList:
            zombie.drawZombie()
        
        for projectile in app.projectileList:
            projectile.draw()

        for sun in app.sunList:
            sun.drawPlant()
        
        if app.finalWaveLabel:
            drawLabel("Final Wave!", app.width//2, app.height//2, size = 50,
                      bold = True, opacity=app.finalLabelOpacity, align='center', fill='red', font='serif')


def main():
    runApp(width = 978, height = 575)

main()
