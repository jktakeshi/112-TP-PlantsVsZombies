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
        drawRect(self.x, self.y, 10, 10, fill = 'red')

class regularZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.4, damage = 10)

    def draw(self):
        pass

class flagZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.6, damage = 10)

    def draw(self):
        pass

class coneheadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 175, speed = 0.4, damage = 10)

    def draw(self):
        pass

class bucketHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 350, speed = 0.4, damage = 10)
    
    def draw(self):
        pass