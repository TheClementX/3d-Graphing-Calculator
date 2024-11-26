import sympy as sp
import numpy as np 
import math 

#takes a string function
#sets a sympy function
#lambdifies function then evaluates it based on an x y range
#only not for parse_expr to work is to use proper sp syntax not including sp.buildin functions

class function:
    def __init__(self):
        self.string_function = ''
        self.f = None

    #sets the function
    def setSpFunction(self):
        self.f = sp.parse_expr(self.string_function)
    
    #get all [x, y, z] vector values based on maxx and maxy and interval size
    #this raises domain errors with sqrt functions
    def generateFunctionPoints(self, maxx, maxy, maxz, numgridlines):
        lambdaF = sp.lambdify(sp.symbols('x, y'), self.f, 'math')
        self.points = set() 

        # set the interval for point generation in x and y direction 
        intervalSizeX = maxx/(numgridlines//2)
        intervalSizeY = maxy/(numgridlines//2)
#         print(intervalSizeX, intervalSizeY)

        xPoints = [x*intervalSizeX for x in range(numgridlines//2 +1)]
        yPoints = [y*intervalSizeY for y in range(numgridlines//2 + 1)]
        #must cast points in the range into ints could cause problems
        for x in xPoints:
            for y in yPoints: 
                
                #x y
                try:
                    xy = (x, y, lambdaF(x, y))
                    if xy not in self.points and -maxz <= xy[2] <= maxz:
                        self.points.add(xy)
                except:
                    pass

                #-x y
                try:
                    nxy = (-x, y, lambdaF(-x, y))
                    if nxy not in self.points and -maxz <= nxy[2] <= maxz:
                        self.points.add(nxy)
                except:
                    pass
                #x -y
                try:
                    xny = (x, -y, lambdaF(x, -y))
                    if xny not in self.points and -maxz <= xny[2] <= maxz:
                        self.points.add(xny)
                except:
                    pass
                #-x -y
                try:
                    nxny = (-x, -y, lambdaF(-x, -y))
                    if nxny not in self.points and -maxz <= nxny[2] <= maxz:
                        self.points.add(nxny)
                except:
                    pass
#         print(self.points) 
        return self.points

    def printPoints(self):
        for i in range(len(self.points)):
            if i%5 == 0:
                print('\n')
            print(self.points[i], ', ', end='')



    
