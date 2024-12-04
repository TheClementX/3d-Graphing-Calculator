from cmu_graphics import *

#define a class to make simple buttons
class Button:
    def __init__(self, w, h, text, size):
        self.w = w
        self.h = h
        self.text = text
        self.size = size
        self.x = None
        self.y = None
        self.visible = False

    #define a function to draw buttons
    def drawButton(self, x, y):
        self.visible = True
        self.x = x
        self.y = y
        drawRect(x, y, self.w, self.h, fill=None, border='black', borderWidth=5, align='center')
        drawLabel(self.text, self.x, self.y, size = self.size)

    #define a function to see if a button has been pressed 
    def getPressed(self, mouseX, mouseY):
        if self.x == None or self.y == None or not self.visible:
            return False
        elif mouseX >self.x-self.w/2 and mouseX < self.x + self.w/2 and mouseY > self.y - self.h/2 and mouseY < self.y + self.h/2:
            return True
        return False
    
