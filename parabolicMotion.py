from cmu_graphics import *
import math

def calcParabola(startX, startY, targetX, targetY, travelTime, steps=100, yDisplacement=80):
    dx = targetX - startX
    midX = (startX + targetX)/2
    topHeight = startY - yDisplacement
    a = (startY - topHeight)/((startX-midX)**2)

    timeStep = travelTime/steps
    vx = dx/travelTime
    trajectory = []
    for step in range(steps + 1):
        x = startX + step*timeStep*vx
        y = a*(x - midX)**2 + topHeight
        trajectory.append((x, y))
    
    return trajectory



    # dx = targetX - startX  # Horizontal distance
    # dy = targetY - topHeight  # Vertical distance

    # # Calculate horizontal velocity
    # vx = dx / duration

    # # Calculate initial vertical velocity to reach peak
    # vy = (-gravity * duration / 2) - (dy / duration)

    # trajectory = []
    # for step in range(steps + 1):
    #     t = (step / steps) * duration
    #     x = startX + vx * t
    #     y = startY + vy * t + 0.5 * gravity * t**2
    #     trajectory.append((x, y))

    # return trajectory


def predictContact(startX, startY, zombie, travelTime, steps, gravity = -9.81):
    predictedX = zombie.x - zombie.speed * travelTime
    predictedY = zombie.y

    projectileTrajectory = calcParabola(startX, startY, predictedX, predictedY, travelTime, steps)

    for step in range(len(projectileTrajectory)):
        projectileX, projectileY = projectileTrajectory[step]
        if abs(projectileX - predictedX) < 5 and abs(abs(projectileY - predictedY) < 10):
            return projectileX, projectileY
    return predictedX-2, predictedY

