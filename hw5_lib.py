#Name: Christopher Asfour
#ID: 14599382
#File Name: hw5_lib.py

from graphics import *
import random

class Paddle:
    def __init__(self, window, space_from_bottom, paddle_width, paddle_height):
        paddle_x = (window.getWidth()-paddle_width)/2
        paddle_y = window.getHeight() - space_from_bottom
        self.rectangle = Rectangle(Point(paddle_x, paddle_y), Point(paddle_x + paddle_width, paddle_y + paddle_height))
        self.rectangle.setFill("light green")
        self.rectangle.setOutline("white")
        self.rectangle.draw(window)

    def moveByKey(self, key, win_width, offset):
        if key == "Left":
            if self.rectangle.getP1().getX() != 0:
                self.rectangle.move(-offset, 0)
        if key == "Right":
            if self.rectangle.getP2().getX() != win_width:
                self.rectangle.move(offset, 0)
        
    def getSurfaceCenter(self):
        x1 = self.rectangle.getP1().getX()
        x2 = self.rectangle.getP2().getX()
        y1 = self.rectangle.getP1().getY()
        point = Point(((x1+x2)/2), y1)
        return point

    def resetToCenter(self, window):
        paddleX = self.getSurfaceCenter().getX()
        diffX = 0        
        diffX = (window.getWidth() / 2) - paddleX;
        self.rectangle.move(diffX, 0)

    def getRectangle(self):
        return self.rectangle

class Brick:
    def __init__(self, x, y, width, height, color, window, text):
        self.rectangle = Rectangle(Point(x, y), Point(x+width, y+height))
        self.rectangle.setFill(color)
        self.rectangle.draw(window)
        self.text = text

    def getRectangle(self):
        return self.rectangle

    def getScore(self):
        score = 0
        for c in self.text:
            score += ord(c) - ord('a')
        return score

class Ball:
    def __init__(self, window, paddle, radius):
        p = paddle.getSurfaceCenter()
        self.circle = Circle(Point(p.getX(), p.getY()-radius), radius)
        self.circle.setFill("yellow")
        self.circle.draw(window)
        self.direction = [0, 0]

    def moveIt(self):
        self.circle.move(self.direction[0], self.direction[1])

    def resetToPaddle(self, paddle):
        surfaceCenter = paddle.getSurfaceCenter()
        surfaceCenterX = surfaceCenter.getX()
        surfaceCenterY = surfaceCenter.getY()
        ballX = self.circle.getCenter().getX()
        ballY = self.circle.getCenter().getY()
        distX = 0
        if(distX > surfaceCenterX):
            distX = ballX - surfaceCenterX
        else:
            distX = surfaceCenterX - ballX
        distY = surfaceCenterY - ballY
        self.circle.move(distX, distY - self.circle.getRadius())

    def setRandomDirectionSpeed(self, min_speed=0.85, max_speed=3.0):
        randomX = random.randint(0,1)
        #print(randomX)
        #print(min_speed, " ", max_speed)
        if randomX == 0:
            self.direction = [random.uniform(min_speed, max_speed), random.uniform((-min_speed), (-max_speed))]
        elif randomX == 1:
            self.direction = [random.uniform(-min_speed, -max_speed), random.uniform((-min_speed), (-max_speed))]
        #print(self.direction)

    def getDirectionSpeed(self):
        return self.direction

    def setDirectionSpeed(self, d):
        #print("SET DIRECTION SPEED")
        #print(d, '\n')
        self.direction = d

    def reverseX(self):
        self.direction[0] = (self.direction[0]) * (-1)

    def reverseY(self):
        self.direction[1] = (self.direction[1]) * (-1)


    def checkHitWindow(self, window):
        #top
        if self.circle.getP1().getY() <= 0:
            return True
        #left
        if self.circle.getP1().getX() <= 0:
            return True
        #right
        if self.circle.getP2().getX() >= window.getWidth():
            return True
        return False
        

    def checkHit(self, rectangle):
        rectangle_height = rectangle.getP1().getY() - rectangle.getP2().getY()
        rectangle_width = rectangle.getP2().getX() - rectangle.getP1().getX()
        #check blue
        #if (self.circle.getP1().getX() <= rectangle.getP2().getX() and self.circle.getP2().getX() >= rectangle.getP1().getX()):
            #if (self.circle.getP1().getY() <= rectangle.getP1().getY() and self.circle.getP2().getY() >= rectangle.getP2().getY()):
                #return True

        #check green
        #check if greater than right side
        if ((rectangle.getP2().getX() + self.circle.getRadius())) < (self.circle.getP1().getX()):
            return False
        #check if less than left side
        if ((rectangle.getP1().getX()) - (self.circle.getRadius())) > (self.circle.getP2().getX()):
            return False
        #check if greater than top
        if ((rectangle.getP1().getY()) - (self.circle.getRadius())) > (self.circle.getP2().getY()):
            return False
        #check if less than bottom
        if ((rectangle.getP2().getY()) + (self.circle.getRadius())) < (self.circle.getP1().getY()):
            return False

        #check pink
        #check if in right side
        if (self.circle.getCenter().getX() <= rectangle.getP2().getX() + self.circle.getRadius()):#left of right side of pink zone
            if (self.circle.getCenter().getX() >= rectangle.getP2().getX() - self.circle.getRadius()):# right of rectangle middle
                return True
        #check if in left side
        if (self.circle.getCenter().getX() >= rectangle.getP1().getX() - self.circle.getRadius()):
            if (self.circle.getCenter().getX() <= rectangle.getP1().getX() + self.circle.getRadius()):
                return True
        #check if in top
        if (self.circle.getCenter().getY() >= rectangle.getP1().getY() - self.circle.getRadius()):# below top of pink zone
            if (self.circle.getCenter().getY() <= rectangle.getP1().getY() + (rectangle_height/2)): # above rectangle middle
                return True
        #check if in bottom
        if (self.circle.getCenter().getY() <= rectangle.getP2().getY() + self.circle.getRadius()):# above bottom of pink zone
            if (self.circle.getCenter().getY() >= rectangle.getP1().getY() + (rectangle_height/2)): # above rectangle middle
                return True

        #check red
        #top right P3 declaration
        P3 = Point(rectangle.getP2().getX(), rectangle.getP1().getY())
        #bottom left P4 declaration
        P4 = Point(rectangle.getP1().getX(), rectangle.getP2().getY())
        
        #check top left corner
        if(((self.circle.getCenter().getX() - rectangle.getP1().getX())**(2) + (self.circle.getCenter().getY() - rectangle.getP1().getY())**(2))**(.5) <= self.circle.getRadius()):
            return True
        #check top right corner
        if(((self.circle.getCenter().getX() - P3.getX())**(2) + (self.circle.getCenter().getY() - P3.getY())**(2))**(.5) <= self.circle.getRadius()):
            return True 
        #check bottom right corner
        if (((self.circle.getCenter().getX() - rectangle.getP2().getX())**(2) + (self.circle.getCenter().getY() - rectangle.getP2().getY())**(2))**(.5) <= self.circle.getRadius()):
            return True
        #check bottom left corner
        if(((self.circle.getCenter().getX() - P4.getX())**(2) + (self.circle.getCenter().getY() - P4.getY())**(2))**(.5) <= self.circle.getRadius()):
            return True

        #everything else failed
        #pink-dashed zone
        return False

        

        
            
    
def setupMessageScoreAndLifeInput(window, offset_from_center_x, offset_from_bottom):
    width = window.getWidth()
    center = (width)/2
    height = window.getHeight()
    a = center + offset_from_center_x
    b = center + (2 * offset_from_center_x)
    score_label = Text(Point((a), (height - offset_from_bottom)), "SCORE: ")
    score_label.setTextColor("white")
    score_label.draw(window)
    score_num_text = Text(Point((b), (height - offset_from_bottom)), "0")
    score_num_text.setTextColor("white")
    score_num_text.draw(window)

    c = center - (2 * offset_from_center_x)
    d = center - (offset_from_center_x)
    life_text = Text(Point((c), (height - offset_from_bottom)), "LIFE: ")
    life_text.setTextColor("white")
    life_text.draw(window)
    life_input = Entry(Point((d), (height - offset_from_bottom)), 3)
    life_input.setText("")
    life_input.draw(window)

    #Red Text
    e = height - (2 * offset_from_bottom)
    message_text = Text(Point((center), e), "")
    message_text.setTextColor("red")
    message_text.draw(window)

    return message_text, score_num_text, life_text, life_input

def getLinesOfWords(filename):
    word_list = []
    new_word_list = []
    infile = open(filename, "r")

    for line in infile:
      line = line.lower()
      for char in line:
        if (char.isalnum() == True):
          word_list.append(char)
        else:
          word_list.append(" ")
      joined_lines =  "".join(word_list)
      split_lines = joined_lines.split()
      
      temp_split_lines = split_lines.copy()
      for word in temp_split_lines:
        if (len(word) < 2 or len(word) > 8):
          split_lines.remove(word)
      new_word_list.append(split_lines)
      word_list = []

    return new_word_list
    
def makeLifeStatic(window, life_input):
    y = life_input.getText()
    life = int(y)
    location = life_input.getAnchor()
    output = Text(location, "")
    output.setText(str(life))
    output.setTextColor("white")
    life_input.undraw()
    output.draw(window)
    return life, output
    
    

def updateScore(score_offset, score_num_text):
    text = score_num_text.getText()
    intText = int(text)
    intText = intText + score_offset
    text = str(intText)
    score_num_text.setText(text)