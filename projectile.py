from zombies import *


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
        self.image = 'pea.png'
        self.width = 10
        self.height = 10

class icePeaShot(Projectile):
    def __init__(self, x, y,):
        super().__init__(x, y, speed = 8, damage = 10)
        self.freezeEffect = 2
        self.image = 'snowpea.png'
        self.width = 10
        self.height = 10

# add duration here
    def slowDownEffect(self, zombie):
        zombie.applySlowDown(self.slowDown)
    
