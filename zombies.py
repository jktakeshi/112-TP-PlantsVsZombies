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
        if abs(self.x - plant.x) < 35 and abs(self.y - plant.y) < 10:
            self.inMotion = False
            self.moveZombie()
            return True
        else:
            self.inMotion = True
        return False
    
    def heavyDamage(self):
        self.imagePath = self.lowHealthImage
        self.image = self.imageDraw()

    def imageDraw(self):
        image = Image.open(self.imagePath)
        return CMUImage(image)

    def drawZombie(self):
        drawImage(self.image, self.x, self.y, align='center', width = 60, height = 70)

class regularZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.4, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'regularZombie.png'
        self.lowHealthImage = 'zombieBoneless.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class flagZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.5, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'flagZombie.png'
        self.lowHealthImage = 'zombieBoneless.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class coneHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 175, speed = 0.4, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'coneHeadZombie.png'
        self.lowHealthImage = 'regularZombie.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class bucketHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 350, speed = 0.4, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'bucketHeadZombie.png'
        self.lowHealthImage = 'regularZombie.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class poleVaultingZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 150, speed = 0.6, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'poleVaultingZombie.png'
        self.lowHealthImage = 'poleVaultingNoPole.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()
