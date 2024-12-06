from cmu_graphics import *
from projectile import peaShot, icePeaShot, melonPult, bounceProjectile
from PIL import Image
from time import *
import random

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

class Plant:
    def __init__(self, x, y, shootingInterval=None, coolDownTime=15):
        self.x = x
        self.y = y
        self.health = 100
        self.originalX = x
        self.originalY = y
        self.lastShotTime = time()
        self.shootingInterval = shootingInterval
        self.coolDownTime = coolDownTime
        self.startCoolDownTime = None
        self.coolingDown = False
        self.seedOpacity = 100
        self.count = 0
        self.width = 45
        self.height = 50

    def isCoolingDown(self):
        if self.startCoolDownTime == None:
            self.startCoolDownTime = time()
        elapsed = time() - self.startCoolDownTime
        if elapsed > self.coolDownTime:
            self.coolingDown = False
            self.startCoolDownTime = None
        else:
            self.coolingDown = True
            
    def canShoot(self):
        return self.shootingInterval != None and (time()-self.lastShotTime) >= self.shootingInterval

    def drawPlantSeed(self):
        drawImage(self.seedImage, self.x, self.y, align='center', width = 45, height = 50)
        if self.coolingDown:
            elapsed = time() - self.startCoolDownTime
            self.seedOpacity = max(0, (1 - (elapsed/self.coolDownTime))*100)
            drawRect(self.x-45/2, self.y-50/2, 45, 50, 
                     fill='black', opacity=self.seedOpacity)
            if elapsed >= self.coolDownTime:
                self.startCoolDownTime = None
                self.startCoolDownTime = 100
                self.coolingDown = False
    
    def drawPlant(self):
        drawImage(self.image, self.x, self.y, align='center', width = self.width, height = self.height)

    def damagePlant(self, damage):
        self.health -= damage
    
    def resetPosition(self):
        self.x = self.originalX
        self.y = self.originalY
    
    def copyPlant(self):
        return self.__class__(self.originalX, self.originalY)
        

class PeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, shootingInterval=1.425)
        self.health = 100
        # citation: https://plantsvszombies.fandom.com/wiki/Peashooter/Gallery
        self.imagePath = 'images/peaShooter.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        # citation: https://plantsvszombies.fandom.com/wiki/Peashooter/Gallery
        self.seedImagePath = 'images/peaShooterSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)
        self.damage = peaShot(x, y).damage
        self.sunCost = 100
        self.type = 'offensive'
    
    def shoot(self):
        self.lastShotTime = time()
        return peaShot(self.x, self.y)

class IcePeaShooter(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, shootingInterval=2.25)
        self.health = 75
        # citation: https://plantsvszombies.fandom.com/wiki/Snow_Pea/Gallery
        self.imagePath = 'images/snowpeaShooter.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        # citation: https://plantsvszombies.fandom.com/wiki/Snow_Pea/Gallery
        self.seedImagePath = 'images/snowPeaSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)
        self.damage = icePeaShot(x, y).damage
        self.sunCost = 175
        self.type = 'offensive'
    
    def shoot(self):
        self.lastShotTime = time()
        return icePeaShot(self.x, self.y)

class Wallnut(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)

        # citation: https://plantsvszombies.fandom.com/wiki/Wall-nut/Gallery
        self.health = 200
        self.imagePath = 'images/wallnut.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.damage = 0
        # citation: https://plantsvszombies.fandom.com/wiki/Wall-nut/Gallery
        self.seedImagePath = 'images/wallnutSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)

        self.sunCost = 50
        self.coolDownTime = 20
        self.type = 'defensive'

class melon(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, shootingInterval=4)
        self.health = 75

        # citation: https://plantsvszombies.fandom.com/wiki/Melon-pult/Gallery
        self.imagePath = 'images/melon.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.width = 65
        self.height = 65

        # citation: https://plantsvszombies.fandom.com/wiki/Melon-pult/Gallery
        self.seedImagePath = 'images/melonSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)
        self.damage = melonPult(x,y,x+5,y+5,travelTime=2.0).damage
        self.sunCost = 1
        self.type = 'offensive'
    
    def shoot(self, targetX, targetY):
        self.lastShotTime = time()
        return melonPult(self.x, self.y, targetX, targetY)

class Sunflower(Plant):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.prevSunTime = None

        #citation: https://plantsvszombies.fandom.com/wiki/Sunflower/Gallery
        self.imagePath = 'images/sunflower.png'
        self.sunCount = 0
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        #citation: https://plantsvszombies.fandom.com/wiki/Sunflower/Gallery
        self.seedImagePath = 'images/sunflowerSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)
        self.damage = 0
        self.sunCost = 50
        self.collectStartTime = None
        self.type = None
    
    
    def createSun(self):
        if self.prevSunTime == None:
            self.prevSunTime = time()
        if time() - self.prevSunTime >= 8:
            self.prevSunTime = None
            if self.sunCount % 2 == 0:
                return Sun(self.x - 30, self.y + 30, heightLimit = self.y + 10)
            else: 
                return Sun(self.x + 30, self.y + 30, heightLimit = self.y + 10)
        self.sunCount += 1

class Sun(Plant):
    def __init__(self, x, y, heightLimit=None, speed=0.5,lifeTime=15):
        super().__init__(x,y)
        self.x = x
        self.y = y
        self.speed = speed
        self.yDropLimit = random.randint(100, 475)
        self.lifeTime = lifeTime
        self.startLifeTime = None
        self.collected = False
        self.heightLimit = heightLimit
        self.damage = 0
        self.collectStartTime = None

        # citation: https://heroism.fandom.com/wiki/Sun_(Plants_vs._Zombies)
        self.imagePath = 'images/sun.png'

        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
    
    def move(self):
        if self.heightLimit == None:
            if self.y < self.yDropLimit:
                self.y += self.speed
            elif self.startLifeTime == None:
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

class BouncePlant(Plant):
    def __init__(self, x, y):
        super().__init__(x, y, shootingInterval=1.7)
        self.health = 75
        # citation: 
        self.imagePath = 'images/bouncePlant.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)

        # citation: 
        self.seedImagePath = 'images/bouncePlantSeed.png'
        seedImage = Image.open(self.seedImagePath)
        self.seedImage = CMUImage(seedImage)
        self.damage = bounceProjectile(x,y).damage
        self.sunCost = 125
        self.coolDownTime = 15
        self.type = 'offensive'

    def shoot(self):
        self.lastShotTime = time()
        return bounceProjectile(self.x, self.y)