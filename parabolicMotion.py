from cmu_graphics import *


def calcParabola(startX, startY, targetX, targetY, travelTime, steps=100, yDisplacement=80):
    dx = targetX - startX
    midX = (startX + targetX)/2
    topHeight = startY - yDisplacement
    if dx == 0:
        pass
    else: a = (startY - topHeight)/((startX-midX)**2)

    timeStep = travelTime/steps
    vx = dx/travelTime
    trajectory = []
    for step in range(steps + 1):
        x = startX + step*timeStep*vx
        y = a*(x - midX)**2 + topHeight
        trajectory.append((x, y))
    
    return trajectory

def predictContact(startX, startY, zombie, travelTime, steps, gravity = -9.81):
    predictedX = zombie.x - zombie.speed * travelTime
    predictedY = zombie.y

    projectileTrajectory = calcParabola(startX, startY, predictedX, predictedY, travelTime, steps)

    for step in range(len(projectileTrajectory)):
        projectileX, projectileY = projectileTrajectory[step]
        if abs(projectileX - predictedX) < 5 and abs(abs(projectileY - predictedY) < 10):
            return projectileX, projectileY
    return predictedX-5, predictedY

