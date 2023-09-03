#!/usr/bin/python3

import pygame
import random
Gravity = 0.01

class Rock:
    def __init__(self,mass, xPos, yPos, xVelocity, yVelocity):
        self.mass = mass
        self.xPos = xPos
        self.yPos = yPos
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.radius = (mass/10)**(1./3)
    
    def getDistance(self, otherRock):
        xDistance = abs(self.xPos - otherRock.xPos)
        yDistance = abs(self.yPos - otherRock.yPos)
        totalDistance = (xDistance**2 + yDistance**2)**(1./2)
        return totalDistance

    def checkCollision(self, otherRock):
        totalRadius = self.radius + otherRock.radius
        totalDistance = self.getDistance(otherRock)
        #print(f"total radius {totalRadius}, total distance {totalDistance}")
        if totalDistance > self.radius + otherRock.radius :
            return False
        
        return True

    def applyGravity(self, otherRock):
        xDistance = abs(self.xPos - otherRock.xPos)
        yDistance = abs(self.yPos - otherRock.yPos)
        totalDistance = self.getDistance(otherRock)
        # figure gravity for self
        force = 0
        if totalDistance != 0:
            force = (Gravity*self.mass*otherRock.mass)/(totalDistance**2)

        acceleration = force/self.mass

        xRatio = 0
        yRatio = 0
        if totalDistance != 0 :
            xRatio = xDistance/totalDistance
            yRatio = yDistance/totalDistance

        if self.xPos > otherRock.xPos:
            xDirection = -1
        else :
            xDirection = 1

        if self.yPos > otherRock.yPos:
            yDirection = -1
        else :
            yDirection = 1

        self.xVelocity += (acceleration * xRatio *xDirection)
        self.yVelocity += (acceleration * yRatio *yDirection)
        
        # figure gravity for otherRock
        acceleration = force/otherRock.mass

        xRatio = 0
        yRatio = 0
        if totalDistance != 0 :
            xRatio = xDistance/totalDistance
            yRatio = yDistance/totalDistance

        if self.xPos > otherRock.xPos:
            xDirection = 1
        else :
            xDirection = -1

        if self.yPos > otherRock.yPos:
            yDirection = 1
        else :
            yDirection = -1

        otherRock.xVelocity += (acceleration * xRatio * xDirection)
        otherRock.yVelocity += (acceleration * yRatio * yDirection)

    def doIteration(self):
        self.xPos += self.xVelocity    
        self.yPos += self.yVelocity    
        self.radius = (self.mass/10)**(1./3)
 
    def draw(self, surface):
        pygame.draw.circle(surface,"white",(self.xPos,self.yPos),self.radius)


    def findCenterOfMass(self, rock2):
        xDistance = self.xPos - rock2.xPos 
        yDistance = self.yPos - rock2.yPos 
        massRatio = rock2.mass / (self.mass + rock2.mass)
        xDistance *= massRatio
        yDistance *= massRatio
        return (self.xPos - xDistance, self.yPos - yDistance)
             

class Universe:
    def __init__(self, rockCount, rockMass, xSize, ySize):
        random.seed()
        self.xSize=xSize
        self.ySize=ySize
        self.Rocks = []
        xCenter = xSize/2
        yCenter = ySize/2
        self.centerOfMass=(xSize/2, ySize/2)
        for i in range(0, rockCount):
            xPos = random.randint(0,xSize-1)
            yPos = random.randint(0,ySize-1)
            xVel = random.randint(-3, 3)
            yVel = random.randint(-3, 3)

# The commented lines hwere were an attempt to start the 
# matter cloud spinning which worked but tended to make a
# binary system that flung everything else away forever
#            if yPos > yCenter:
#                xVel = random.randint(0, 1)
#            else: 
#                xVel = random.randint(-1, 0) 
#            if xPos > xCenter:
#                yVel = random.randint(-1, 0)
#            else :
#                yVel = random.randint(0, 1)

            self.Rocks.append(Rock(rockMass, xPos, yPos, xVel, yVel))

 
    def doCollision(self):
        if len(self.Rocks) == 1 :
            return
        Rocks=[]
        for i in range(0, len(self.Rocks)-1):
            if self.Rocks[i] == None :
                continue
            for j in range(i+1, len(self.Rocks)):
                if self.Rocks[j] == None :
                    continue
                if self.Rocks[i].checkCollision(self.Rocks[j]):
                    r1xMomentum = self.Rocks[i].mass * self.Rocks[i].xVelocity
                    r2xMomentum = self.Rocks[j].mass * self.Rocks[j].xVelocity
                    totalxMomentum= r1xMomentum + r2xMomentum
                    
                    r1yMomentum = self.Rocks[i].mass * self.Rocks[i].yVelocity
                    r2yMomentum = self.Rocks[j].mass * self.Rocks[j].yVelocity
                    totalyMomentum= r1yMomentum + r2yMomentum
    
                    centerMass = self.Rocks[i].findCenterOfMass(self.Rocks[j])
                    self.Rocks[i].mass+=self.Rocks[j].mass
                    self.Rocks[i].xPos=centerMass[0]
                    self.Rocks[i].yPos=centerMass[1] 
                    self.Rocks[i].xVelocity = totalxMomentum / self.Rocks[i].mass
                    self.Rocks[i].yVelocity = totalyMomentum / self.Rocks[i].mass
                    Rocks.append(self.Rocks[i])
                    self.Rocks[j] = None
                    self.Rocks[i] = None
                    break
            if self.Rocks[i] != None:
                Rocks.append(self.Rocks[i])
        if self.Rocks[-1] != None:
            Rocks.append(self.Rocks[-1])
        self.Rocks = Rocks

    def doIteration(self):
        self.doCollision()
        centerrock = Rock(0,0,0,0,0)
        xDiff = self.xSize/2-self.centerOfMass[0] 
        yDiff = self.ySize/2-self.centerOfMass[1]
        center = 0  
        for i in range(0, len(self.Rocks)-1):
            for j in range(i+1, len(self.Rocks)):
                self.Rocks[i].applyGravity(self.Rocks[j])
            self.Rocks[i].doIteration()
            self.Rocks[i].xPos += xDiff
            self.Rocks[i].yPos += yDiff
            if(self.Rocks[i].xPos>-10 and self.Rocks[i].xPos<self.xSize+10 and self.Rocks[i].yPos>-10 and self.Rocks[i].yPos<self.xSize+10):
                center = centerrock.findCenterOfMass(self.Rocks[i])
                centerrock.xPos = center[0]
                centerrock.yPos = center[1]
                centerrock.mass += self.Rocks[i].mass
            #print("iteration: ", i)
        self.Rocks[-1].doIteration()
        self.Rocks[-1].xPos += xDiff
        self.Rocks[-1].yPos += yDiff
        if(self.Rocks[-1].xPos>-10 and self.Rocks[-1].xPos<self.xSize+10 and self.Rocks[-1].yPos>-10 and self.Rocks[-1].yPos<self.xSize+10):
            center = centerrock.findCenterOfMass(self.Rocks[-1])
        self.centerOfMass = center
    
    def draw(self, surface):
        for rock in self.Rocks:
            rock.draw(surface)


