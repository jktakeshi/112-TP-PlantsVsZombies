from zombies import *
from time import *
from parabolicMotion import *
import math
from PIL import Image

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
        if abs(self.x - zombie.x) < 5 and abs(self.y - zombie.y) < 10:
            self.damageZombie(zombie, self.damage)
            self.inMotion = False
            return True
        return False

    def damageZombie(self, zombie, damage, slowDown=None):
        zombie.health -= damage
    
    def draw(self):
        drawImage(self.image, self.x, self.y, align='center', width = self.width, height = self.height)

class peaShot(Projectile):
    def __init__(self, x, y):
        super().__init__(x+4, y-7, speed = 10, damage = 10)
        # citation: https://www.reddit.com/r/PlantsVSZombies/comments/16st8wb/the_most_legendary_hd_pea_projectile_hd/
        self.imagePath = 'pea.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.width = 15
        self.height = 15

class icePeaShot(Projectile):
    def __init__(self, x, y):
        super().__init__(x+4, y-7, speed = 8, damage = 10)

        # citation: https://plantsvszombies.wiki.gg/wiki/Snow_Pea/Gallery
        self.imagePath = 'snowpea.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.width = 15
        self.height = 15
        self.slowDownDuration = 4 * app.stepsPerSecond

    def slowDownEffect(self, zombie):
        zombie.applySlowDown(self.slowDown)
        zombie.slowDownEnd = time() + self.slowDownDuration
        

class melonPult(Projectile):
    def __init__(self, startX, startY, targetX, targetY, travelTime=2.0):
        super().__init__(startX, startY, speed = 0, damage = 20)

        # citation: https://plantsvszombies.fandom.com/wiki/Melon-pult/Gallery
        self.imagePath = 'melonProjectile.png'
        image = Image.open(self.imagePath)
        self.image = CMUImage(image)
        self.trajectory = calcParabola(startX, startY, targetX, targetY, travelTime, steps=50)
        self.currentStep = 0
        self.rotation = 0
        self.width, self.height = 30, 30
    
    def move(self):
        if self.currentStep < len(self.trajectory):
            prevX, prevY = self.x, self.y
            self.x, self.y = self.trajectory[self.currentStep]
            self.currentStep += 1

            # rotation of projectile based on velocity
            vx = prevX -self.x
            vy = prevY - self.y
            # citation for atan2: https://docs.python.org/3/library/math.html#math.atan2
            self.rotation += math.degrees(math.atan2(vx, abs(vy))) * 0.1
            image = Image.open(self.imagePath)
            self.image = CMUImage(image.rotate(self.rotation))
        else:
            self.inMotion = False
    def draw(self):
        drawImage(self.image, self.x, self.y, align='center', 
                  width = self.width, height = self.height)

        
    
