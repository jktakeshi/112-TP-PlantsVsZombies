from cmu_graphics import *
from projectile import peaShot, icePeaShot
from PIL import Image
from time import *
import random

# path = 'peaShooter.png'
# image = Image.open(path)
# app.peaShooter = CMUImage(image)

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

class Plant:
    def __init__(self, x, y, color, shootingInterval=None):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = color
        self.health = 100
        self.originalX = x
        self.originalY = y
        self.lastShotTime = time()
        self.shootingInterval = shootingInterval

        # path = self.image
        # image = Image.open(path)
        # app.Image = CMUImage(image)
    
    def canShoot(self):
        return self.shootingInterval != None and (time()-self.lastShotTime) >= self.shootingInterval

    def drawPlant(self):
        drawImage(app.Image, self.x, self.y, align='center', width = 50, height = 50)

    def damagePlant(self, damage):
        self.health -= damage
    
    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY
    
    def copyPlant(self):
        return Plant(self.x, self.y, self.color)

class PeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, color='lightgreen', shootingInterval=1.425)
        self.health = 100
        self.image = 'peaShooter.png'
        
    def shoot(self):
        self.lastShotTime = time()
        return peaShot(self.x, self.y)

class IcePeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, color='blue', shootingInterval=2.25)
        self.health = 75
        self.image = 'snowpeaShooter.png'
    def shoot(self):
        self.lastShotTime = time()
        return icePeaShot(self.x, self.y)

class Sunflower(Plant): #produces sun every 10 seconds
    def __init__(self, x, y):
        super().__init__(x, y, color='yellow')
        self.prevSunTime = None
        self.image = 'sunflower.png'
        self.sunCount = 0
    
    def createSun(self):
        if self.prevSunTime == None:
            self.prevSunTime = time()
        if time() - self.prevSunTime >= 10:
            self.prevSunTime = None
            if self.sunCount % 2 == 0:
                return Sun(self.x - 30, self.y + 30, heightLimit = self.y + 10)
            else: 
                return Sun(self.x + 30, self.y + 30, heightLimit = self.y + 10)
        self.sunCount += 1

class Sun(Plant):
    def __init__(self, x, y, heightLimit=None, speed=0.5,lifeTime=15):
        self.x = x
        self.y = y
        self.speed = speed
        self.yDropLimit = random.randint(100, 700)
        self.lifeTime = lifeTime
        self.startLifeTime = None
        self.collected = False
        self.heightLimit = heightLimit
        self.image = 'newSun.png'
    
    def move(self):
        if self.heightLimit == None:
            if self.y < self.yDropLimit:
                self.y += self.speed
            elif self.startLifeTime == None:
                # start when sun lifetime when it stops moving
                self.startLifeTime = time()
        else:
            if self.y < self.heightLimit:
                self.y += self.speed
            elif self.startLifeTime == None:
                self.startLifeTime = time()
    
    def isCollected(self, mouseX, mouseY):
        return distance(mouseX, mouseY, self.x, self.y) <= 15
    
    def isExpired(self):
        if self.startLifeTime != None:
            return (time() - self.startLifeTime) >= self.lifeTime
        else:
            return False
