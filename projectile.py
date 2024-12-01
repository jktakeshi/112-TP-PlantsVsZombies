from zombies import *
from time import *

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.inMotion = None
        self.slowDown = (2/3)
    
    def move(self):
        self.x += self.speed
        self.inMotion = True

    def checkCollision(self, zombie):
        if abs(self.x - zombie.x) < 5 and abs(self.y - zombie.y) < 5:
            self.damageZombie(zombie, self.damage)
            # zombie.damageZombie(self.damage)
            self.inMotion = False
            return True
        return False

    def damageZombie(self, zombie, damage, slowDown=None):
        zombie.health -= damage
    
    def draw(self):
        drawImage(self.image, self.x, self.y, align='center', width = self.width, height = self.height)

class peaShot(Projectile):
    def __init__(self, x, y,):
        super().__init__(x, y, speed = 10, damage = 10)
        # self.image = 'pea.png'
        self.imagePath = 'pea.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.width = 15
        self.height = 15

class icePeaShot(Projectile):
    def __init__(self, x, y,):
        super().__init__(x, y, speed = 8, damage = 10)
        self.imagePath = 'snowpea.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.width = 15
        self.height = 15
        self.slowDownDuration = 4 * 30 # 4 seconds

# add duration here
    def slowDownEffect(self, zombie):
        zombie.applySlowDown(self.slowDown)
        print(zombie.speed)
        zombie.slowDownEnd = time() + self.slowDownDuration
        # while self.slowDownDuration > 0:
        #     zombie.applySlowDown(self.slowDown)
        #     self.slowDownDuration -= 1
        # zombie.slowDown = False
        # zombie.speed /= self.slowDown
    
