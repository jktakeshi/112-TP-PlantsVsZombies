from cmu_graphics import *

def activateGravity(app, x, y):
    app.gravity = True
    app.gravityLoc = x, y
    app.gravityStartTime = app.counter/app.stepsPerSecond

def deactivateGravity(app):
    app.gravity = False
    app.gravityLoc = None
    app.gravityStartTime = None
