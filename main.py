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
    path = 'frontyard.png'
    image = Image.open(path)
    app.frontYard = CMUImage(image)

    # seed slot
    # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot
    path = 'emptySeedSlot.png'
    image = Image.open(path)
    app.seedSlot = CMUImage(image)

    # citation: https://plantsvszombies.fandom.com/wiki/Shovel
    path = 'shovel.png'
    image = Image.open(path)
    app.shovelIcon = CMUImage(image)

    # citation: https://plantsvszombies.fandom.com/wiki/Seed_slot?file=Seed_Slot.png
    path = 'emptySeedSelector.png'
    image = Image.open(path)
    app.emptyTargetIcon = CMUImage(image)

    # citation: https://en.ac-illust.com/clip-art/24289523/target-icon-red
    path = 'targetIcon.png'
    image = Image.open(path)
    app.targetIcon = CMUImage(image)

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
    
    if distance(mouseX, mouseY, 715, 37) <= 25:
        app.shovel = Shovel(715,37)
        app.shovelSelected = True
    
    if distance(mouseX, mouseY, 772, 37) <= 25:
        app.copiedTarget = app.target.copyTarget()
        if app.target.coolingDown == False:
            app.targetSelected = True
            app.gravity = True
            app.gravityLocSelect = True
            app.gravityLoc = (mouseX, mouseY)
            app.copiedTarget.x, app.copiedTarget.y = mouseX, mouseY

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
            app.selectedPlant.x = cellLeft + cellWidth // 2
            app.selectedPlant.y = cellTop + cellHeight // 2
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
            selectedX = cellLeft + cellWidth // 2
            selectedY = cellTop + cellHeight // 2
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
    if not app.gameOverLose and not app.gameOverWin and not app.paused:
        app.counter += 1
        spawnZombies(app, app.currentLevel)

        #plant shooting projectile
        for plant in app.plantsGridList:
            zombiesInRow = [zombie for zombie in app.zombiesList if abs(zombie.y - plant.y) < 10]
            if zombiesInRow and plant.canShoot():
                predictedX, predictedY = predictContact(plant.x, plant.y, zombiesInRow[0], steps = 100, travelTime = 2.0)
                # print(f'predictedX: {predictedX}, zombieX: {zombiesInRow[0].x}')
                if isinstance(plant, melon):
                    projectile = plant.shoot(predictedX, predictedY)
                else:
                    projectile = plant.shoot()
                app.projectileList.append(projectile)

        # move zombie and check for collision with plant
        for zombie in app.zombiesList:
            zombie.moveZombie()
            for plant in app.plantsGridList:
                if zombie.collisionWithPlant(plant):
                    zombie.damagePlant(plant, zombie.damage/app.stepsPerSecond)
                    if plant.health <= 0:
                        app.plantsGridList.remove(plant)
                        zombie.inMotion = True
        
        # gravity and effect duration
        if app.gravity and app.gravityStartTime != None:
            elapsedTime = app.counter/app.stepsPerSecond - app.gravityStartTime 
            if elapsedTime >= app.gravityDuration:
                deactivateGravity(app)        

        # move projectile and check for collision
        for projectile in app.projectileList:
            projectile.move()
            if app.gravity and app.gravityLoc:
                projectile.applyGravity(app.gravityLoc)
                if projectile.reachedGravityCenter:
                    app.projectileList.remove(projectile)
            for zombie in app.zombiesList:
                if projectile.checkCollision(zombie):
                    print('here')
                    if isinstance(projectile, icePeaShot):
                        projectile.slowDownEffect(zombie)
                    projectile.damageZombie(zombie, projectile.damage)
                    if isinstance(projectile, bounceProjectile):
                        if projectile.speed > 0:
                            projectile.bounce(app, zombie, cellHeight = app.boardHeight/app.rows)
                            if projectile.speed <= 2:
                                if projectile in app.projectileList:
                                    app.projectileList.remove(projectile)
                    # else:
                    #     projectile.inMotion = False
                    if 0 < zombie.health <= zombie.lowHealth:
                        zombie.heavyDamage()
                    elif zombie.health <= 0:
                        app.zombiesList.remove(zombie)
                    if isinstance(projectile, bounceProjectile) and projectile in app.projectileList:
                        if not projectile.isBouncing:
                            app.projectileList.remove(projectile)
                
                else:
                    if projectile in app.projectileList and not projectile.inMotion:
                        app.projectileList.remove(projectile)
            # if (app.width < projectile.x or projectile.x < 0 or projectile.y > app.height or 
            #     (app.gravity and app.gravityLoc != None and 
            #      distance(projectile.x, projectile.y, app.gravityLoc[0], app.gravityLoc[1])) < 5):
            #     app.projectileList.remove(projectile)
                # if isinstance(projectile, melonPult):
                #     if projectile.y == zombie.y:
                #         app.projectileList.remove(projectile)
        
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
    # citation: https://plantsvszombies.fandom.com/wiki/Brain/Gallery
    path = 'gameOver.png'
    image = Image.open(path)
    gameOverLoseSign = CMUImage(image)
    if app.gameOverLose:
        drawRect(0, 0, app.width, app.height, opacity=60)
        drawImage(gameOverLoseSign, app.width//2, app.height//2, align='center')
    elif app.gameOverWin:
        drawLabel("Game Over", app.width//2, app.height//2, bold=True, size=50, font='serif')
        drawLabel("You won!", app.width//2, app.height//2 + 50, fill='red', bold=True, size=50, font='serif')

#Grid (from CS Academy)
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
        drawGameOver(app)
        if app.selectedPlant:
            app.selectedPlant.drawPlant()
        if app.shovel:
            app.shovel.drawShovel()
        if app.target:
            app.target.drawTargetSeed()
        drawImage(app.targetIcon, 772, 37, align='center', width = 45, height = 50)
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
        
        if app.finalWaveLabel:
            drawLabel("Final Wave!", app.width//2, app.height//2, size = 50,
                      bold = True, opacity=app.finalLabelOpacity, align='center', fill='red', font='serif')

        if app.gravity and app.gravityLoc and app.target:
            cx, cy = app.gravityLoc
            drawCircle(cx, cy, app.gravityRadius, fill = 'gray', opacity=50)
        
        if app.gravityLocSelect:
            drawLabel("Select a spot", app.width//2, app.height//2, size = 40,
                      bold = True, align='center', font='serif')


def main():
    runApp(width = 978, height = 575)

main()
