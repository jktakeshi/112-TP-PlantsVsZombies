from cmu_graphics import *
# from projectile import *
from plants import *
from PIL import Image 

class Zombie:
    def __init__(self, x, y, health, speed, damage):
        self.x = x
        self.y = y
        self.health = health
        self.speed = speed
        self.slowDown = False
        self.damage = damage
        self.inMotion = True
# move method
    def moveZombie(self):
        if self.inMotion == True:
            self.x -= self.speed
        else:
            self.x = self.x

    # if get hit by ice pea
    def applySlowDown(self, slowDownFactor):
        if not self.slowDown:
            self.speed *= slowDownFactor
            self.slowDown = True
    
    def damagePlant(self, plant, damage):
        plant.health -= damage
    
    def collisionWithPlant(self, plant):
        if abs(self.x - plant.x) < 15 and abs(self.y - plant.y) < 5:
            # self.damagePlant(plant, self.damage)
            self.inMotion = False
            self.moveZombie()
            return True
        else:
            self.inMotion = True
        return False

    def drawZombie(self):
        drawImage(self.image, self.x, self.y, align='center', width = 60, height = 70)

class regularZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.4, damage = 10)
        # self.image = 'regularZombie.png'
        self.imagePath = 'regularZombie.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)


class flagZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.6, damage = 10)
        # self.image = 'flagZombie.png'
        self.imagePath = 'flagZombie.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)



class coneHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 175, speed = 0.4, damage = 10)
        # self.image = 'coneHeadZombie.png'
        self.imagePath = 'coneHeadZombie.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)


class bucketHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 350, speed = 0.4, damage = 10)
        # self.image = 'bucketHeadZombie.png'
        self.imagePath = 'bucketHeadZombie.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)