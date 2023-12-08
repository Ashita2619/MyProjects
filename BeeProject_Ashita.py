#################################################
# BeeProject_Ashita.py
# name: Ashita Jawali
# andrew id: ajawali
# Bee gif taken from https://bestanimations.com/gifs/Cute-Honey-Bee-Art.html
# Background taken from https://wallpapercave.com/beautiful-landscape-android-wallpapers 
# Main Screen taken from https://www.pexels.com/search/garden%20background/ 
# for sinodidal movement of the flowers and pollens took some idea from https://www.geeksforgeeks.org/visualize-sinusoidal-waves-using-python/ 
# for the music'https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3'
# for the sound play button image taken from https://www.shutterstock.com/image-vector/speaker-set-icon-sound-vector-illustration-2158140597
# for sprites animation and wings flapping of the bees and helper bees  took from KirbleBirdStarter.py taught in the class
# for the pollens and the flowers coming every two seconds was also taken from KirbleBirdStarter.py from the piazza post
# for the main screen and the button class was also take from the document which was sent in piazza.
# To debug the code particularly the obstacle counter that part  because it was not printing in the canvas 
#and the helper bee were collecting two pollens at the same time 
#so took some help of AI 
#################################################

from cmu_graphics import *
from PIL import Image,ImageOps
import os, pathlib
import math, time,random
from functools import cache

# #################################################
# # Bee Class
# #################################################
class Bee:

    def __init__(self,speedX=0.1,speedY=0.1):
        #Load the bee gif
        # https://bestanimations.com/gifs/Cute-Honey-Bee-Art.html Image taken from here
        myBee = Image.open('Bee.gif') 
        self.direction = "right"
        # took from the KirblBirdStarter.py starter file
        # create an empty list for left sprites and for right sprites
        self.spriteRightList = []
        self.spriteLeftList = []

        # animation for the right sprite
        for frame in range(myBee.n_frames):
            myBee.seek(frame)
            fr = myBee.resize((myBee.size[0]//8,myBee.size[1]//8))
            fr = CMUImage(fr)
            self.spriteRightList.append(fr)
        self.spriteRightList.pop(0)

        # animation for the left sprite
        for frame in range(myBee.n_frames):
            myBee.seek(frame)
            fr = myBee.resize((myBee.size[0]//8,myBee.size[1]//8))
            fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteLeftList.append(fr)
        self.spriteLeftList.pop(0)

        # set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0
        # set the x and y position of the bee
        self.x,self.y = 200,200
        # inventory list to collect the pollen colors collected
        self.pollenInventory = []
        # other parameters initialized
        self.radius = 20
        self.score = 0
        self.speedX = speedX
        self.speedY = speedY

    # draws the image of bee gif based on the mouse direction
    def drawPlayer(self):
        if self.direction == "right":
            drawImage(self.spriteRightList[self.spriteCounter],self.x,self.y,align="bottom-left")
        else:
            drawImage(self.spriteLeftList[self.spriteCounter],self.x,self.y,align="bottom-left")



    # move the bees  with some speed according to the distance of the mouse and the bee
    def playerOnStep(self,app):
        # check if bee is moving out of canvas bounds and adjust position
        if self.x < 100:
            self.x = 100
        if self.x > app.width - 100:
            self.x = app.width - 100
        if self.y < 100:
            self.y = 100
        if self.y > app.height - 100:
            self.y = app.height - 100

        dist = distance(self.x,self.y,app.mx, app.my)
        #Update the sprite more often when wings are flapping faster
        # Was taken from the piazza post from the kirbleBirdStarter.py
        self.stepCounter += 1
        if self.stepCounter >= (10 / (dist + 6)): 
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteRightList)
            self.stepCounter = 0
        
        # check for the distance and accordingly change the speed/ acceleration of the bees
        if dist <= 15:
            self.x = app.mx
            self.y = app.my
        else:
            self.x += self.speedX
            self.y += self.speedY
        self.speedX = (app.mx - self.x) * 0.8
        self.speedY = (app.my - self.y) * 0.8
            
        # update position based on speed and direction
        if self.x < app.mx:
            self.direction = "right"
        elif self.x > app.mx:
            self.direction = "left"
    
    @cache
    # flapping of the bee function from the kirbleBirdStarter starter file
    def flap(self):
        self.dy = -3
     

# ################################################
# Helper Bee class
# ################################################
class HelperBee(Bee):
    # Inheritance of the bee class
    def __init__(self):
        super().__init__()
        self.color = "yellow"
        self.x = random.randrange(0,300)
        self.y = random.randrange(0,300)
        self.target = None
        # This is a list which contains the color which the helper bee has collected underneath the legs and also
        # this will be displayed on the top left corner
        self.helperBeeInventory = []
        
    
    # draws the helper bee image for both the directions according to the mouse directions movement
    def drawHelperBee(self):
        if self.direction == "right":
            drawImage(self.spriteRightList[self.spriteCounter],self.x,self.y,align="center")
        else:
            drawImage(self.spriteLeftList[self.spriteCounter],self.x,self.y,align="center")
        

        
    # gets the minimum distance out of all the other ungathered and unpollinated pollens which will basically be its target
    # and will move in that direction
    def targetPollen(self,app):
        flowerPosition = {(pollen.x, pollen.y,pollen.color):distance(app.pollen.x,app.pollen.y,app.helperbee.x,app.helperbee.y) for pollen in app.pollens}
        minDistance = min(flowerPosition.values())
        minLocation = [key for key,value in flowerPosition.items() if value == minDistance]
        minimumLocation = sorted(minLocation)
            
        # choosing the closest flower that meets the conditions
        self.target = (minimumLocation[0][0], minimumLocation[0][1])
        
        if app.pollen.pollinated == False:
            # calculate the distance bbetween the target position and the bees position
            dist = distance(self.x,self.y,self.target[0],self.target[1])
            # checks if the distance is less than move slowly or move faster
            if dist <= 10:
                self.x = self.target[0]
                self.y = self.target[1]
            else:
                self.x += self.speedX
                self.y += self.speedY
            self.speedX = (self.target[0] - self.x) * 0.9
            self.speedY = (self.target[1] - self.y) * 0.9
            
            # changing the directions based on the target positions direction
            if self.x < self.target[0]:
                self.direction = "right"
            elif self.x > self.target[0]:
                self.direction = "left"
           
       
   
    # for the helper bee movement move the bees  with some speed according to the distance of the target 
    # which has the minimum distance and the bee
    def helperbeeonStep(self,app):
        dist = distance(self.x,self.y,self.x,self.y)
        # for flapping of the wings
        self.stepCounter += 1
        if self.stepCounter >= (10 / (dist + 6)): 
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteRightList)
            self.stepCounter = 0

        # don't let the bees move away from the screen
        if self.x < 100:
            self.x = 100
        if self.x > app.width - 100:
            self.x = app.width - 100
        if self.y < 100:
            self.y = 100
        if self.y > app.height - 100:
            self.y = app.height - 100


    @cache
    # flap function 
    # flapping of the bee function from the kirbleBirdStarter starter file
    def flap(self):
        super().flap()


# ################################################
# HelperBee 1 class
# ################################################
class HelperBee1(Bee):
    # Inheritance of the bee class
    def __init__(self):
        super().__init__()
        self.color = "yellow"
        self.x = random.randrange(0,100)
        self.y = random.randrange(0,100)
        self.r = 10
        self.target = True
        self.unpollinated = True
        # This is a list which contains the color which the helper bee has collected underneath the legs and also
        # this will be displayed on the top left corner
        self.helperBee1Inventory = []

    # draws the helper bee 1 for both the directions based on the mouse movement direction
    def drawHelperBee(self):
        if self.direction == "right":
            drawImage(self.spriteRightList[self.spriteCounter],self.x,self.y)
        else:
            drawImage(self.spriteLeftList[self.spriteCounter],self.x,self.y)


    # gets the minimum distance out of all the other ungathered and unpollinated pollens which will basically will be your target pollens    
    def targetFlower(self,app):
        if self.target and self.unpollinated:
            self.target = None
        if self.target == None:
            flowerPosition = {(pollen.x, pollen.y,pollen.color):distance(app.pollen.x,app.pollen.y,app.helperbee.x,app.helperbee.y) for pollen in app.pollens}
            minDistance = min(flowerPosition.values())
            minLocation = [key for key,value in flowerPosition.items() if value == minDistance]
            minimumLocation = sorted(minLocation)
            
                
        # choosing the closest flower that meets the conditions
        self.target = (minimumLocation[1][0], minimumLocation[1][1])
        
        if app.pollen.pollinated == False:
            # calculate the distance bbetween the target position and the bees position
            dist = distance(self.x,self.y,self.target[0],self.target[1])
            # checks if the distance is less than move slowly or move faster
            if dist <= 20:
                self.x = self.target[0]
                self.y = self.target[1]
                
            else:
                self.x += self.speedX
                self.y += self.speedY
            self.speedX = (self.target[0] - self.x) * 0.9
            self.speedY = (self.target[1] - self.y) * 0.9

            # update position based on speed and direction
            if self.x < self.target[0]:
                self.direction = "right"
            elif self.x > self.target[0]:
                self.direction = "left"
    
    
    # for the helper bee movement based on the distance of the target and the helper bee position
    def helperonStep(self,app):
        dist = distance(self.x,self.y,self.target[0],self.target[1])
        # flapping the wings according to the distance
        self.stepCounter += 1
        if self.stepCounter >= (10 / (dist + 6)): 
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteRightList)
            self.stepCounter = 0

        # don't let the bees move away from the screen
        if self.x < 100:
            self.x = 100
        if self.x > app.width - 100:
            self.x = app.width - 100
        if self.y < 100:
            self.y = 100
        if self.y > app.height - 100:
            self.y = app.height - 100 

    @cache
    # flaps the helper bee wings
    # flapping of the bee function from the kirbleBirdStarter starter file
    def flap(self):
        super().flap()
         

# ################################################
#   Flowers with Pollens Class
# ################################################           
# This is a pollen class which are nothing but your flowers with pollens 
# the pollens will move sinusoidally and when pollen gets collected by all the bees it becomes hollow
class Pollen:
    def __init__(self,x,y,radius,dx,dy,color):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = 5
        self.dy = 10
        self.color = color
        self.pollinated = False
        self.gathered = True
        self.ringed = False
        self.size = 20
        self.maxRadius = 10
        # sinosidal movment parameter
        # https://www.geeksforgeeks.org/visualize-sinusoidal-waves-using-python/ 
        self.angle = random.uniform(0,10)

    # draws the ringed pollens
    def drawPollen(self):
        if self.ringed:
            drawCircle(self.x,self.y,self.radius,fill=None,border=self.color)
        else:
            drawCircle(self.x,self.y,self.radius,fill=self.color,border=self.color)
       
    # this function creates the list of pollens randomly creating the position with even having red color and odd having pink 
    @staticmethod
    def createPollenList(numPollens,maxFlowerCount):
        PollenList = []
        for i in range(numPollens):
            if i % 2 == 0:
                color = "red"
            else:
                color = "pink"
            x = random.randrange(50, 450)
            y = random.randrange(500, 550)
            dx = 5
            flower = Pollen(x,y,10,dx,10,color)
            if len(PollenList) < maxFlowerCount:
                PollenList.append(flower)
        return PollenList 
    
    # This function moves the pollens from bottom to top in sinosidal motion
    def pollenOnStep(self,PollenList):
        # sinosidal movement
        # https://www.geeksforgeeks.org/visualize-sinusoidal-waves-using-python/ 
        self.x += (self.radius * math.sin(self.angle))
        # bottom to top movement
        self.y -= self.dy
        # This is to check if the pollens has moved out of the canvas then just remove from the pollenList
        if self.y < 0:
            PollenList.remove(self)

    # This function takes into the pollens and check if it has been collected/gathered and appends it to my inventory 
    def checkPollination(self, app):
        if self.gathered and distance(self.x, self.y, app.bee.x, app.bee.y) <= 15:
            app.bee.pollenInventory.append(self.color)
            self.pollinated = True
            self.gathered = False
            self.ringed = True # once it collects the pollens it will change to the ringed shape
        
        # if the length of the inventory is more than 6 which means it shldnt take more than 6 underneath 
        # his legs and also in the inventory
        if len(app.bee.pollenInventory) > 6:
            app.bee.pollenInventory.pop(0)
            
    # This draws the pollens underneath the bees            
    def drawPollenUnderneathBee(self,app):
        for i in range(len(app.bee.pollenInventory)):
            drawCircle(app.bee.x + app.bee.radius + 5 + (i*4), app.bee.y, 5, fill=app.bee.pollenInventory[i],border="black")

    # This function takes into the pollens and check if it has been collected/gathered and appends it to my  helper bee inventory 
    def checkPollinationHelper(self,app):
        if distance(self.x, self.y, app.helperbee.x, app.helperbee.y) <= 15:
            if len(app.helperbee.helperBeeInventory)<6:
                if self.color not in app.helperbee.helperBeeInventory:
                    app.helperbee.helperBeeInventory.append(self.color)
            self.pollinated = True
            self.gathered = False
            self.ringed = True # once it collects the pollens it will change to the ringed shape
        
        # If the length of the  helper bee inventory is more than 6 which means it shldnt take more than 6 underneath 
        # his legs and also in the helper bee inventory
        if len(app.helperbee.helperBeeInventory ) > 6:
            app.helperbee.helperBeeInventory.pop(0)

    # draws the pollens underneath the helper bee     
    def drawPollenUnderneathHelperBee(self,app):
        offset = 20
        for i in range(len(app.helperbee.helperBeeInventory)):
            drawCircle(app.helperbee.x + (i*4), app.helperbee.y + offset, 5, fill=app.helperbee.helperBeeInventory[i],border="black")

    # This function takes into the pollens and check if it has been collected/gathered and appends it to my  helper bee inventory
    def checkPollinationHelperBee(self,app):
        if distance(self.x, self.y, app.helperbee1.x, app.helperbee1.y) <= 15:
            if len(app.helperbee1.helperBee1Inventory) <6:
                if self.color not in app.helperbee1.helperBee1Inventory: 
                    app.helperbee1.helperBee1Inventory.append(self.color)
            self.pollinated = True
            self.gathered = False
            self.ringed = True # once it collects the pollens it will change to the ringed shape
        
        # check if it has reached some value otherwise just pop from the list as it wont take into consideration
        # or it wont carry more than 6 pollens
        if len(app.helperbee1.helperBee1Inventory) > 6:
            app.helperbee1.helperBee1Inventory.pop(0)

    # draws the pollens underneath the helper bees 1
    def drawPollenUnderneathHelperBee1(self,app):
        offset2 = 50
        for j in range(len(app.helperbee1.helperBee1Inventory)):
            drawCircle(app.helperbee1.x +15+ (j*4), app.helperbee1.y + offset2, 5, fill=app.helperbee1.helperBee1Inventory[j],border="black")



# ################################################
# Flower class to be pollinated
# ################################################
# This is a class flower which is to be pollinated so it should move sinusoidally and grows gradually if the same color 
# pollens has been touched and simultaneously one of the same pollen color will be 
# deleted from his legs and also from the inventory
class Flower:

    def __init__(self,x,y,dx,color):
        # The paramters defined 
        self.x = x
        self.y = y
        self.r = 10
        self.dx = random.randrange(2,5)
        self.dy = 20
        self.color = color
        self.pollinated = False
        self.gathered = False
        self.growing = True
        self.pollenGrowing = True
        self.size = 30
        self.counter = 0
        # sinosidal movment parameter
        # https://www.geeksforgeeks.org/visualize-sinusoidal-waves-using-python/ 
        self.angle = random.uniform(0,10)
        

     # This function draws the flower which is nothing but in ringed shape   
    def drawFlower(self,thickness):
        # draw the outer circle
        drawCircle(self.x,self.y,self.r,fill= None,border=self.color)
        # draw the inner circle
        innerRadius = max(self.r-thickness,0)
        drawCircle(self.x,self.y,innerRadius,border=self.color,borderWidth=2,fill=self.color)

    # This function will take into consideration the flower movement 
    def flowerOnStep(self):
        # Sinosidal movement
        # https://www.geeksforgeeks.org/visualize-sinusoidal-waves-using-python/ 
        self.x += (self.r * math.sin(self.angle))
        # bottom to top movement
        self.y -= self.dy

    # This function creates the flower List which has basically the x,y position of flower 
    # the color and the speed with which it moves and it is a static method
    @staticmethod
    def createFlowerList(numFlowers):
        flowerList = []
        for i in range(numFlowers):
            if i % 2 == 0:
                color = "red"
            else:
                color = "pink"
            x = random.randrange(50, 450)
            y = random.randrange(500, 550)
            dx = random.randrange(2, 5)
            flower = Flower(x, y, dx, color)
            flowerList.append(flower)
        return flowerList

    # This function checks if the flower has been pollinated or not for the player bees
    def checkFlowerPollinated(self,app):
            self.startTimer = time.time()
            self.growing = True
            for pollenColor in app.bee.pollenInventory:
                # if the distance is less than some value it should touch and increase accordingly
                if distance(self.x,self.y,app.bee.x,app.bee.y) <= 15:
                    if pollenColor == self.color:
                        app.bee.pollenInventory.remove(pollenColor)
                        while self.r <= 30: # 30 is nothing but some maxValue for it to stop growing
                            self.r += 1
                            self.startTimer += time.time()
                        # increment score when everytime the bee pollinates a flower
                        app.bee.score += 10
                        break
            self.growing = False

    # This function checks if the flower has been pollinated or not for the helper bee
    def checkFlowerPollinatedHelper(self,app):
            self.startTimer = time.time()
            self.growing = True
            for pollenColor in app.helperbee.helperBeeInventory:
                # if the distance is less than some value it should touch and increase accordingly
                if distance(self.x,self.y,app.helperbee.x,app.helperbee.y) <= 15:
                    if pollenColor == self.color:
                        app.helperbee.helperBeeInventory.remove(pollenColor)
                        while self.r <= 30: # 30 is nothing but some maxValue for it to stop growing
                            self.r += 1
                            self.startTimer += time.time()
                        # increment score when  everytime the bee pollinates a flower
                        app.bee.score += 10
                        break
            self.growing = False

    # This function checks if the flower has been pollinated or not for the helper bee1
    def checkFlowerPollinatedHelperBee(self,app):
            self.startTimer = time.time()
            self.growing = True
            for pollenColor in app.helperbee1.helperBee1Inventory:
                # if the distance is less than some value it should touch and increase accordingly
                if distance(self.x,self.y,app.helperbee1.x,app.helperbee1.y) <= 15:
                    if pollenColor == self.color:
                        app.helperbee1.helperBee1Inventory.remove(pollenColor)
                        while self.r <= 30:# 30 is nothing but some maxValue for it to stop growing
                            self.r += 1
                            self.startTimer += time.time()
                        # increment score when  everytime the bee pollinates a flower 
                        app.bee.score += 10
                        break
            self.growing = False

    # This is to check if the pollen which has been still in the screen
    def pollenGraduallyGrowing(self,app):
        if not app.pollen.pollinated and app.pollen.color == self.color:
            app.pollen.radius += 30
            
# ################################################
#  Obstacle Class
# ################################################
# This is the class which creates the obstacle which falls from the top rather than how my flowers and pollens goes up
class Obstacle:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 10
        self.dx = random.randrange(2,5)
        self.dy = 5
        self.color = "black"
        self.counter = 0
        self.touched = False

    # draws the obstacle with white border   
    def drawObstacle(self):
        drawCircle(self.x,self.y,self.r,fill=self.color,border="white")

    # This function creates the obstacle list which can be easily accessed or drawn on the canvas and its a static method
    @staticmethod
    def createObstacle(obstacles):
        obstaclesList = []
        for i in range(obstacles):
            x = 450
            y = 0
            obstacle = Obstacle(x,y)
            obstaclesList.append(obstacle)
        return obstaclesList

    # This function jsut moves the obstacles from top to bottom and keeps a counter
    def ObstacleOnStep(self,app):
        self.y += self.dy
        # The logic is taken from AI (Chatgpt) becuase it was not getting printed even is it was updating the count
        if  not self.touched and distance(self.x,self.y,app.bee.x,app.bee.y)<= self.r + app.bee.radius:
            self.counter += 1
        if self.counter == 5 and not app.gameOver:
            app.gameOver = True
        
# ################################################
#   Button Class
# ################################################

# This is the button class which is used for button clicking and checking the press and do some intended work accordingly
# This was taken from the demo.py files sent on the piazza but changed some parts according to my requirements.
class Button:
    def __init__(self,left,top,width,height,fun):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.fun = fun
        self.sound = False

    # checks for the sound play or paused
    def checkForSound(self,app):
        if app.paused:
            app.paused = False
            app.sound.play(loop=True)
        else:
            app.paused = True
            app.sound.pause()

          
# ################################################
#   Animation 
# ################################################
# This chunk of code includes the parameters required for the graphics or animation to run and to show it in the canvas
# This is used to intialize the paramters or the requirements
def onAppStart(app):
    resetApp(app)

# This is useful when you are resetting or restarting the game  
def resetApp(app):
    # https://www.pexels.com/search/garden%20background/
    image1 = Image.open("Sceneary.jpeg")
    app.image1 = CMUImage(image1)
    # https://wallpapercave.com/beautiful-landscape-android-wallpapers
    image = Image.open("Background.jpg")
    app.image = CMUImage(image)
    app.imageWidth,app.imageHeight = image.width,image.height
    app.bee = Bee()
    app.helperbee = HelperBee()
    app.helperbee1 = HelperBee1()
    # https://www.shutterstock.com/image-vector/speaker-set-icon-sound-vector-illustration-2158140597
    image3 = Image.open("sound.jpg")
    app.image2 = CMUImage(image3)
    app.imageWidth2,app.imageHeight2 = image3.width//4,image3.height//4
    url = 'https://s3.amazonaws.com/cmu-cs-academy.lib.prod/sounds/Drum1.mp3' # This was taken from CS academy
    app.sound = Sound(url)
    app.mx ,app.my = 0,0
    app.flowers = Flower.createFlowerList(10)
    app.flower = Flower(10,10,10,"red")
    app.pollens = Pollen.createPollenList(10,20)
    app.pollen = Pollen(10,10,10,5,5,"red")
    app.obstacles = Obstacle.createObstacle(5)
    app.obstacle = Obstacle(10,10)
    app.button = Button(10,10,app.imageWidth2,app.imageHeight2,Button.checkForSound)
    app.mousePressed = True
    app.stepsPerSecond = 2
    app.startFlowerTime = time.time()
    app.startPollenTime = time.time()
    app.startObstacleTime = time.time()
    app.paused = False
    app.counter = 0
    app.score = 0
    app.gameOver = False
    app.labelText = "Lives Left: 0"
    

# ################################################
#  Main Screen 
# ################################################
# The similar idea given by the demo python file in piazza and which he taught us in the class
# This will be the mainscreen of the game where in when you press enter you will go to the game interface 
# This was taken from the demo.py which was posted in piazza
def mainScreen_redrawAll(app):
    drawRect(200,270,app.width/2,app.height/2,fill="grey",opacity=75,align="center")
    drawImage(app.image1,0,0,width=500,height=500)
    newWidth, newHeight = (app.imageWidth2,app.imageHeight2)
    drawImage(app.image2,10,10,width=newWidth,height=newHeight)
    drawLabel("Press Enter",app.width/2,app.height/2,size=26,bold=True,fill="gold")
    drawLabel("Welcome to the Bee Pollination Game!", app.width/2, 20, size = 20,fill="black",bold=True,align="center")
    drawLabel("Press r to restart the game",app.width/2, 40,fill="black",font="arial",size=18,align="center",bold=True)
    drawLabel("Press p to pause the game",app.width/2,60,fill='black',font="arial",size=18,align="center",bold=True)
    drawLabel("Press play button to play and pause the sound",app.width/2,80,fill='gold',font="arial",size=18,align="center",bold=True)
    drawLabel("Collect as much pollen and pollinate to win the game",app.width/2,100,fill="gold",font="arial",size=18,align="center",bold=True)
    drawLabel("Be mindful of the obstacles You will only get five lives",app.width/2,120,fill="magenta",font="arial",size=18,align="center",bold=True,italic=True)
    
    
   
# Press enter to move onto the next game page or interface
def mainScreen_onKeyPress(app,key):
    if key == "enter":
        setActiveScreen("game")
    

# This when pressed will play and pause the sound accordingly
def mainScreen_onMousePress(app,mouseX,mouseY):
     if (app.button.left <= mouseX <= app.button.left + app.button.width) and (app.button.top <= mouseY <= app.button.top + app.button.height):
        app.button.checkForSound(app)
    

# ################################################
# Game Screen/Interface
# ################################################
# The similar idea given by the demo python file in piazza and which he taught us in the class
# This is for the mouse movement and inturn changing the positions also where the mouse goes
def game_onMouseMove(app,mouseX,mouseY):
    app.mx = mouseX
    app.my = mouseY
    
# This function will do everything on step 
def game_onStep(app):
    if not app.paused and not app.gameOver:
        app.bee.playerOnStep(app)
        app.helperbee.targetPollen(app)
        app.helperbee.helperbeeonStep(app)
        app.helperbee1.targetFlower(app)
        app.helperbee1.helperonStep(app)
        # loop through every flower instances and get 
        # into the screen every 2 seconds after the flowers goes out
        # of the screen
        for flower in app.flowers:
            flower.flowerOnStep()
            if (time.time()- app.startFlowerTime > app.stepsPerSecond):
                app.flowers.append(Flower(random.randrange(50, 450), 450, random.randrange(2, 5), random.choice(["red", "pink"])))
                app.startFlowerTime = time.time()
            flower.checkFlowerPollinated(app)
            flower.checkFlowerPollinatedHelper(app)
            flower.checkFlowerPollinatedHelperBee(app)
            flower.pollenGraduallyGrowing(app)
            

        # loop through every pollen instances and get 
        # into the screen every 2 seconds after the flowers goes out
        # of the screen
        for pollen in app.pollens:
            pollen.pollenOnStep(app.pollens)
            if (time.time()- app.startPollenTime > app.stepsPerSecond):
                app.pollens.append(Pollen(random.randrange(50, 450), 450,10, random.randrange(2, 5),10, random.choice(["red", "pink"])))
                app.startPollenTime = time.time()
            pollen.checkPollination(app)
            pollen.checkPollinationHelper(app)
            pollen.checkPollinationHelperBee(app)
           
        # loop through every obstacle instances and get 
        # into the screen every 2 seconds after the flowers goes out
        # of the screen
        for obstacle in app.obstacles:
            obstacle.ObstacleOnStep(app)
            if distance(obstacle.x,obstacle.y,app.bee.x,app.bee.y) <= obstacle.r + app.bee.radius: 
                # The logic is taken from AI (Chatgpt) becuase it was not getting printed even is it was updating the count
                obstacle.counter += 1
                app.labelText = f"Lives Left: {obstacle.counter}"
                if obstacle.counter == 5:
                    app.gameOver = True
                    break
            if app.gameOver:
                return
            # This is similar to the logic of KirbleBirdStarter.py
            if (time.time()- app.startObstacleTime > 7):
                app.obstacles.append(Obstacle(random.randrange(50, 450), 0))
                app.startObstacleTime = time.time()
         

# Thisn function when you press a key will so the following things like paused and reset to play the game from the starting
def game_onKeyPress(app,key):
    if key =="p":
        app.paused = not app.paused
    if key == "r":
        resetApp(app)

    # Same as the KirbleBirdStarter.py
    # flappy bee
    app.bee.flap()
    # flappy helper bees
    app.helperbee.flap()
    app.helperbee1.flap()
    
# This will contain all the drawing functions which will be drawn in the game interface
def game_redrawAll(app):
    drawRect(389,50,80,80,fill="grey")
    newWidth, newHeight = (app.imageWidth + 50,app.imageHeight)
    drawImage(app.image,0,0,width=newWidth,height=newHeight)
    drawLabel("Game Interface!",app.width/2,20,fill="white",font="monospace",size=25,align="center",bold=True,italic=True)
    drawLabel("BeeInventory:",60,20,fill="orange",bold = True,italic=True)
    drawLabel("HelperBeeInventory:",60,60,fill="orange",bold = True,italic=True)
    drawLabel("HelperBee1Inventory:",60,100,fill="orange",bold = True,italic=True)
    
    # The bee inventory drawing
    x = 50
    y = 40
    for i in  range(len(app.bee.pollenInventory)):
        color = app.bee.pollenInventory[i]
        drawCircle(x,y,10,fill=None,border=color,borderWidth=3)
        x += 15
    
    # The helper bee inventory drawing
    x1 = 50
    y1 = 80
    for j in range(len(app.helperbee.helperBeeInventory)):
        color = app.helperbee.helperBeeInventory[j]
        drawCircle(x1,y1,10,fill=None,border=color,borderWidth=3)
        x1 += 15

    # The helper bee 1 inventory drawing
    x2 = 50
    y2 = 120
    for k in range(len(app.helperbee1.helperBee1Inventory)):
        color = app.helperbee1.helperBee1Inventory[k]
        drawCircle(x2,y2,10,fill=None,border=color,borderWidth=3)
        x2 += 15
        
    
    # Call Pollen's draw method
    for pollens in app.pollens:
        pollens.drawPollen()
        

    # Call Bee's draw method
    app.bee.drawPlayer()

    # Call the Bee's underneath pollen drawing under his legs
    app.pollen.drawPollenUnderneathBee(app)
 

    # Call Helper Bee draw method
    app.helperbee.drawHelperBee()

    # Call the  Helper Bee's underneath pollen drawing under his legs
    app.pollen.drawPollenUnderneathHelperBee(app)
    
    
    # Call the Helper Bee draw method
    app.helperbee1.drawHelperBee()

    # Call the  Helper Bee's underneath pollen drawing under his legs
    app.pollen.drawPollenUnderneathHelperBee1(app)

    # Consider writing the score on the top left corner 
    drawLabel(f"Score: {app.bee.score}",389,50,align="left",fill="orange",bold=True,italic=True,size=16)
    
    # Call Flower's draw method
    for flower in app.flowers:
        flower.drawFlower(5)

    # Call the Obstacle's draw method
    for obstacle in app.obstacles:
        obstacle.drawObstacle()
        

    # draw the game over message if the game is over
    if app.gameOver:
        drawLabel("Game Over!", 250, 250, fill="purple", bold=True, italic=True, size=40,font="monospace",align="center")
    else:
        drawLabel(app.labelText, 421, 80, fill="orange", bold=True, italic=True)

    
# This is the helper function which will just calculate the distances everytime it is called.
def distance(x1,y1,x2,y2):
    return (((x2-x1)**2 + (y2-y1)**2)**0.5)
  
#################################################
# main
#################################################

def main():
    runAppWithScreens(initialScreen="mainScreen",width=500,height=500)

if __name__ == '__main__':
    main()