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
        self.color = color
        self.health = 100
        self.originalX = x
        self.originalY = y
        self.lastShotTime = time()
        self.shootingInterval = shootingInterval

        # path = self.imagePath
        # image = Image.open(path)
        # self.Image = CMUImage(image)
    
    def canShoot(self):
        return self.shootingInterval != None and (time()-self.lastShotTime) >= self.shootingInterval

    def drawPlantSeed(self):
        drawImage(self.seedImage, self.x, self.y, align='center', width = 45, height = 50)

    def drawPlant(self):
        drawImage(self.image, self.x, self.y, align='center', width = 45, height = 50)

    def damagePlant(self, damage):
        self.health -= damage
    
    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY
    
    def copyPlant(self):
        return self.__class__(self.originalX, self.originalY)
        

class PeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, color='lightgreen', shootingInterval=1.425)
        self.health = 100
        self.imagePath = 'peaShooter.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        self.seedImagePath = 'peaShooterSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)

        self.sunCost = 100
    
        
    def shoot(self):
        self.lastShotTime = time()
        return peaShot(self.x, self.y)

class IcePeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, color='blue', shootingInterval=2.25)
        self.health = 75
        self.imagePath = 'snowpeaShooter.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        self.seedImagePath = 'snowPeaSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)

        self.sunCost = 175
    
    def shoot(self):
        self.lastShotTime = time()
        return icePeaShot(self.x, self.y)

class Sunflower(Plant): #produces sun every 10 seconds
    def __init__(self, x, y):
        super().__init__(x, y, color='yellow')
        self.prevSunTime = None
        self.imagePath = 'sunflower.png'
        self.sunCount = 0
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        self.seedImagePath = 'sunflowerSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)

        self.sunCost = 50
    
    
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


# app.boardLeft = 240
#     app.boardTop = 75
#     app.boardWidth = 700 
#     app.boardHeight = 475
class Sun(Plant):
    def __init__(self, x, y, heightLimit=None, speed=0.5,lifeTime=15):
        self.x = x
        self.y = y
        self.speed = speed
        self.yDropLimit = random.randint(100, 475)
        self.lifeTime = lifeTime
        self.startLifeTime = None
        self.collected = False
        self.heightLimit = heightLimit
        self.imagePath = 'newSun.png'

        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
    
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
