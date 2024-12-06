from cmu_graphics import *
import copy
from zombies import *
from plants import *
from levels import *


def collectSun(app):
    # collecting sun
    for sun in app.sunList:
        if sun.collectStartTime == None:
            sun.collectStartTime = time() 
        addedTime = random.randint(4,9)
        if time() > sun.collectStartTime + addedTime:
            app.sunPoints += 25
            app.sunList.remove(sun)
            sun.collectStartTime = None

def plantDefensivePlants(app, row):
    # select wallnut
    for plant in app.plantsPanelList:
        if isinstance(plant, Wallnut):
            if plant.sunCost <= app.sunPoints and not plant.coolingDown:
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
                plantPlantOnRow(app, row)

def plantOffensivePlants(app, row):
    for plant in app.plantsPanelList:
        if isinstance(plant, (BouncePlant, PeaShooter, IcePeaShooter, melon)):
            if app.sunPoints >= 300 and plant.sunCost <= app.sunPoints and not plant.coolingDown: 
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
            elif app.sunPoints >= 175 and plant.sunCost <= app.sunPoints and not plant.coolingDown: 
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
            elif app.sunPoints >= 125 and plant.sunCost <= app.sunPoints and not plant.coolingDown: 
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
            elif app.sunPoints >= 100 and plant.sunCost <= app.sunPoints and not plant.coolingDown: 
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
            plantPlantOnRow(app, row)

def plantSunflower(app, row):
    totalPlants = len(app.plantsGridList)
    maxSunflowers = totalPlants // 3
    for plant in app.plantsPanelList:
        if isinstance(plant, Sunflower):
            if totalPlants > 3 and plant.count >= maxSunflowers:
                break
            if plant.sunCost <= app.sunPoints and not plant.coolingDown:
                app.selectedPlant = plant.copyPlant()
                app.currentPlant = plant
                plant.count += 1
                plantPlantOnRow(app, row)
                

# plants plant on row
def plantPlantOnRow(app, row):
    if app.selectedPlant:
        cellWidth, cellHeight = app.boardWidth/app.cols, app.boardHeight/app.rows
        # changed here
        selectedY = app.boardTop + cellHeight*row+ + cellHeight/2
        for col in range(app.cols):
            if isinstance(app.selectedPlant, Sunflower) and col != 0:
                continue
            selectedX = app.boardLeft + cellWidth*col + cellWidth/2
            if isinstance(app.selectedPlant, Wallnut):
                if plantsToRight(app, selectedY, selectedX):
                    continue
            if (selectedX, selectedY) not in app.plantsLocation:
                print(selectedX, selectedY)
                app.selectedPlant.x, app.selectedPlant.y = selectedX, selectedY
                app.plantsGridList.append(app.selectedPlant)
                app.plantsLocation.append((selectedX, selectedY))
                app.sunPoints -= app.selectedPlant.sunCost
                app.currentPlant.isCoolingDown()
                app.selectedPlant = None
                break

def plantsToRight(app, selectedY, selectedX):
    for plant in app.plantsGridList:
        if abs(plant.y - selectedY) < app.boardHeight/app.rows:
            if plant.x > selectedX:
                return True
    return False

# zombiecount per row
def zombiesPerRow(app):
    zombieCountsPerRow = [0] * app.rows
    for zombie in app.zombiesList:
        row = getRow(app, zombie.y)
        if row != None:
            zombieCountsPerRow[row] += 1
    return zombieCountsPerRow

def predictZombieSpawn(app, currRow, zombieCountsPerRow, plantsRowDamage):
    minDx = float('inf')
    distanceBestRow = None
    distanceBestScore = float('inf')
    for zombie in app.zombiesList:
        dx = zombie.x - app.boardLeft
        row = getRow(app, zombie.y)
        if dx < minDx: 
            minDx = dx
            distanceBestRow = row
    distanceBestScore = plantsRowDamage[distanceBestRow] - zombieCountsPerRow[distanceBestRow]*1.5

    bestScore = float('inf')
    bestRow = None
    for i in range(len(zombieCountsPerRow)):
        currScore = plantsRowDamage[i] - zombieCountsPerRow[i]
        if currScore <= bestScore:
            bestScore = currScore
            bestRow = i
    if distanceBestScore <= bestScore:
        return distanceBestRow
    return bestRow

# makeplantdecision using predictzombie and calcrowdamage
def plantDecision(app):
    zombiesCountsPerRow = zombiesPerRow(app)
    plantDamagePerRow = calculateRowsDamage(app)

    dangerRows = set()
    for zombie in app.zombiesList:
        currRow = getRow(app, zombie.y)
        dangerRow = predictZombieSpawn(app, currRow, zombiesCountsPerRow, plantDamagePerRow)
        dangerRows.add(dangerRow)
        print(dangerRows)
    
    if app.counter < 10*app.stepsPerSecond:
        for row in range(app.rows):
            plantSunflower(app, row)
    
    for row in dangerRows:
        if requireOffensivePlant(app, row) and app.sunPoints >= 100:
            plantOffensivePlants(app, row)
        elif requireDefensivePlant(app, row) and app.sunPoints >= 50:
            plantDefensivePlants(app, row)
    
    for row in range(app.rows):
        if row not in dangerRows:
            plantSunflower(app, row)

def requireOffensivePlant(app, row):
    zombiesCountsPerRow = zombiesPerRow(app)
    plantDamagePerRow = calculateRowsDamage(app)
    return plantDamagePerRow[row] < sum(zombiesCountsPerRow)*10

def requireDefensivePlant(app, row):
    zombiesCountsPerRow = zombiesPerRow(app)
    plantsInRow = []
    offensivePlants = 0
    defensivePlants = 0
    for plant in app.plantsGridList:
        if getRow(app, plant.y) == row:
            if isinstance(plant, Wallnut):
                return False
            plantsInRow.append(plant)
    for plant in plantsInRow:
        if plant.type == 'defensive': defensivePlants += 1
        elif plant.type == 'offensive': offensivePlants += 1
    if offensivePlants == 0 or defensivePlants >= 1:
        return False
    return len(plantsInRow) < sum(zombiesCountsPerRow)*10

def getRow(app, zombieY):
    cellHeight = app.boardHeight/app.rows
    for row in range(app.rows):
        rowTop = app.boardTop + row*cellHeight
        rowBottom = rowTop + cellHeight
        if rowTop <= zombieY <= rowBottom:
            return row
    return None
