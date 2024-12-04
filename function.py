#knowledge of how to use sympy was learned from sympy documentation
#url of sympy documentation: https://docs.sympy.org/latest/index.html
import sympy as sp
import math 

#define a class to hold a string function and then turn it into a lambda expression
#this class uses said lambda expression to generate the points for a function to be drawn in function mode
class function:
    def __init__(self):
        self.string_function = ''
        self.f = None

    #sets the function in sympy
    def setSpFunction(self):
        self.f = sp.parse_expr(self.string_function)
    
    #define a function to get all [x, y, z] vector values based on maxx and maxy and interval size
    #account for possible domain errors with try except 
    def generateFunctionPoints(self, maxx, maxy, maxz, numgridlines):
        lambdaF = sp.lambdify(sp.symbols('x, y'), self.f, 'math')
        self.points = set() 

        # set the interval for point generation in x and y direction 
        intervalSizeX = maxx/(numgridlines//2)
        intervalSizeY = maxy/(numgridlines//2)

        #create list of all points to be iterated over
        xPoints = [x*intervalSizeX for x in range(numgridlines//2 +1)]
        yPoints = [y*intervalSizeY for y in range(numgridlines//2 + 1)]

        #generate function points
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
        return self.points

    #helper function used in development to varify value of generated points 
    def printPoints(self):
        for i in range(len(self.points)):
            if i%5 == 0:
                print('\n')
            print(self.points[i], ', ', end='')



    
