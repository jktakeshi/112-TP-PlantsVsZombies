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
        self.vx = -speed
        self.vy = 0
        self.newRowY = None
        self.slowDown = False
        self.damage = damage
        self.inMotion = True
        self.changedRows = 0
# move method
    def moveZombie(self):
        cellHeight = app.boardHeight/app.rows
        if self.newRowY != None:
            if abs(self.y - self.newRowY) < 3:
                self.y = self.newRowY
                self.vy = 0
                self.newRowY = None
            else:
                if self.newRowY > self.y: direction = 1
                else: direction = -1
                self.vy = self.speed * direction


        if self.inMotion == True:
            self.x += self.vx
            self.y += self.vy
        # else:
        #     self.x = self.x
    
    def changeRow(self, newRow, app):
        cellHeight = app.boardHeight/app.rows
        self.newRowY = app.boardTop + (cellHeight*newRow) + cellHeight/2


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
            return True
        else:
            # self.inMotion = True
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
        self.normalImage = 'images/regularZombie.png'
        self.lowHealthImage = 'images/zombieBoneless.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class flagZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 100, speed = 0.5, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'images/flagZombie.png'
        self.lowHealthImage = 'images/zombieBoneless.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class coneHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 175, speed = 0.4, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'images/coneHeadZombie.png'
        self.lowHealthImage = 'images/regularZombie.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class bucketHeadZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 350, speed = 0.4, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'images/bucketHeadZombie.png'
        self.lowHealthImage = 'images/regularZombie.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()

class poleVaultingZombie(Zombie):
    def __init__(self, x,  y):
        super().__init__(x, y, health = 150, speed = 0.6, damage = 10)
        self.lowHealth = self.health/3

        # citation: https://plantsvszombies.fandom.com/wiki/Gallery_of_zombies
        self.normalImage = 'images/poleVaultingZombie.png'
        self.lowHealthImage = 'images/poleVaultingNoPole.png'

        self.imagePath = self.normalImage
        self.image = self.imageDraw()