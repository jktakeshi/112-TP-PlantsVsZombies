from cmu_graphics import *
from plants import *
from zombies import *
import math
import random
import copy

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

def onAppStart(app):
    app.frontYard = 'frontyard.png'
    app.plantsPanelList = []
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

    app.plantPanelX = 230
    app.plantPanelY = 2
    app.plantPanelWidth = 400
    app.plantPanelHeight = 70

    app.sunList = []
    app.sunPoints = 0

    app.counter = 0
    plantPanel(app)


# adding "plants" to the plant panel
# there will be changes for different levels
#   first level will just have sunflower, peashooter, icepea
def plantPanel(app):
    app.plantsPanelList.append(Sunflower(app.plantPanelX + 45, app.plantPanelY + app.plantPanelHeight/2))  # Sunflower
    app.plantsPanelList.append(PeaShooter(app.plantPanelX + 75, app.plantPanelY + app.plantPanelHeight/2))  # PeaShooter
    app.plantsPanelList.append(IcePeaShooter(app.plantPanelX + 115, app.plantPanelY + app.plantPanelHeight/2)) #icePeaShooter

# plant panel outline
def drawPlantPanel(app):
    drawRect(app.plantPanelX, app.plantPanelY, app.plantPanelWidth, app.plantPanelHeight, fill=None, border  = 'black')
    for plant in app.plantsPanelList:
        plant.drawPlant()
    
def onMousePress(app, mouseX, mouseY):
    for plant in app.plantsPanelList:
        if distance(mouseX, mouseY, plant.x, plant.y) <= 20:
            app.selectedPlant = copy.deepcopy(plant)
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
    app.counter += 1
    # generating zombies on random
    if random.random() < 0.005: #change this logic for the different levels
        row = random.choice(range(app.rows))
        cellWidth, cellHeight = getCellSize(app)
        zombieX = app.boardLeft + app.boardWidth + 10
        zombieY = app.boardTop + row * cellHeight + cellHeight//2
        newZombie = regularZombie(zombieX, zombieY) # edit to accom for diff zombies
        app.zombiesList.append(newZombie)

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
                print(f'plant: {plant.health}, zombie: {zombie.damage}')
                print(f'zombie: {zombie.health}')
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
                # print('hi')
    
    # moving and removing sun
    for sun in copy.copy(app.sunList): # edit this; prolly use copy
        sun.move()
        if sun.isExpired():
            app.sunList.remove(sun)

#Grid
def drawGrid(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = None if (row+col) % 2 == 0 else None #lightgreen and green
            drawCell(app, row, col, color)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill = color, border='black')

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
    drawImage(app.frontYard, 0, 0, width=app.width, height=app.height)
    drawGrid(app)
    drawPlantPanel(app)
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
    
    drawLabel(f'Sun Points: {app.sunPoints}', 75, 50)

def main():
    runApp(width = 978, height = 575)

main()
