from zombies import *
from time import *
from parabolicMotion import *
import math
from PIL import Image

def distance(x1, y1, x2, y2):
    return (((x1-x2)**2) + ((y1-y2)**2))**0.5

class Projectile:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.damage = damage
        self.inMotion = None
        self.slowDown = (2/3)

        self.vx = speed
        self.vy = 0
    
    def move(self):
        # gravity motion
        if app.gravity and app.gravityLoc:
            print('gav here')
            self.applyGravityEffect(app.gravityLoc)
            
        self.x += self.vx
        self.y += self.vy
        self.inMotion = True

        if (self.x, self.y) == app.gravityLoc:
            print('here loc')
            app.reachedGravityCenter = True
        else: app.reachedGravityCenter = False


    def applyGravityEffect(self, gravityLoc):
        (gx, gy) = gravityLoc
        distanceToGavityLoc = distance(self.x, self.y, gx, gy)
        dx = gx - self.x
        dy = gy - self.y

        if distanceToGavityLoc <= app.gravityRadius:

            # formula
            a = app.gravityPull/(distanceToGavityLoc**2)
            ax = a * (dx/distanceToGavityLoc)
            ay = a * (dy/distanceToGavityLoc)
            self.vx += ax
            self.vy += ay
        else:
            self.vx = self.speed * (dx/distanceToGavityLoc)
            self.vy = self.speed * (dy/distanceToGavityLoc)

    def checkCollision(self, zombie):
        if abs(self.x - zombie.x) < 5 and abs(self.y - zombie.y) < 30:
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
        self.startTime = None
        self.travelTime = travelTime
    
    def move(self):
        if self.startTime == None:
            self.startTime = app.counter/app.stepsPerSecond
        
        timeElapsed = (app.counter/app.stepsPerSecond) - self.startTime
        if timeElapsed < self.travelTime:
            fractionTime = timeElapsed/self.travelTime
            self.currentStep = int(fractionTime * (len(self.trajectory)-1))
            prevX, prevY = self.x, self.y
            self.x, self.y = self.trajectory[self.currentStep]

            # rotation of projectile based on velocity
            vx = prevX -self.x
            vy = prevY - self.y
            # citation for atan2: https://docs.python.org/3/library/math.html#math.atan2
            if vx != 0 or vy != 0:
                self.rotation += math.degrees(math.atan2(vx, vy))*0.1
            image = Image.open(self.imagePath)
            self.image = CMUImage(image.rotate(self.rotation))
        else:
            self.inMotion = False
    def draw(self):
        drawImage(self.image, self.x, self.y, align='center', 
                  width = self.width, height = self.height)
        
class bounceProjectile(Projectile):
    def __init__(self, startX, startY):
        super().__init__(startX, startY, speed = 10, damage = 10)

        # citation: https://plantsvszombies.fandom.com/wiki/Melon-pult/Gallery
        self.imagePath = 'bounceProjectile.png'
        self.preImage = Image.open(self.imagePath)
        self.image = CMUImage(self.preImage)

        self.vx = self.speed
        self.vy = 0
        self.width = 20
        self.height = 20
        self.isBouncing = False
        self.taggedZombies = set()
        self.prevAngle = None

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def bounce(self, app, taggedZombie, cellHeight):
        nearestZombie = None
        minDistance = float('inf')
        
        for zombie in app.zombiesList:
            if zombie != taggedZombie and zombie not in self.taggedZombies:
                dyNextZombie = abs(zombie.y - taggedZombie.y)

                if dyNextZombie >= cellHeight:
                    distanceToNewZombie = distance(self.x, self.y, zombie.x, zombie.y)
                    if distanceToNewZombie <= minDistance:
                        nearestZombie = zombie
                        minDistance = distanceToNewZombie
        self.taggedZombies.add(taggedZombie)

        if nearestZombie:
            self.isBouncing = True
            self.changeTrajectory(nearestZombie)
            self.speed -= 2
        else:
            self.isBouncing = False

    def changeTrajectory(self, zombie):
        dx = zombie.x - self.x
        dy = zombie.y - self.y
        distanceToZombie = distance(self.x, self.y, zombie.x, zombie.y)
        travelTime = distanceToZombie/self.speed

        predictedX = zombie.x - (zombie.speed*travelTime)
        predictedY = zombie.y

        newDx = predictedX - self.x
        newDy = predictedY - self.y
        newDistance = distance(predictedX, predictedY, self.x, self.y)
        self.vx = self.speed * (newDx/newDistance)
        self.vy = self.speed * (newDy/newDistance)
        self.rotateProjectile()
    
    def rotateProjectile(self):
        arg = math.degrees(math.atan2(self.vy, self.vx))
        if self.vx != 0 or self.vy != 0:
            image = Image.open(self.imagePath)
            # citation: https://www.codecademy.com/resources/docs/pillow/image/rotate for rotate method
            rotatedImage = image.rotate(-arg, expand=True)
            self.image = CMUImage(rotatedImage)


        
    
