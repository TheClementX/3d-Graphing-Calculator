#class used to store all graph variables
#this class defines functions to manipulate graph dimensions
class graph:

    def __init__(self, xScope, yScope, zScope, numGridLines):
        #variables to define full range of axises
        self.xScope = xScope
        self.yScope = yScope
        self.zScope = zScope

        #variables to set number of grid lines to either side of the origin 
        #set the interval size (grid gap) for generating function points with function class
        self.numGridLines = numGridLines
        self.gridGapY = self.yScope / self.numGridLines
        self.gridGapX = self.xScope / self.numGridLines

        #set max distance from origin in any perpendicular direction
        self.xRadius = xScope/2
        self.yRadius = yScope/2
        self.zRadius = zScope/2

        #instantiate outer box points
        self.setOuterBox()

        #instantiate axis points
        self.setAxis()

        #instantiate grid points
        self.setGrid()

    #define function to update and instantiate axis points for drawing
    def setAxis(self):
        self.xyzAxis = [
            [0,0,0],
            [self.xRadius, 0,0],
            [0, 0, self.zRadius * -1.0],
            [self.xRadius * -1.0, 0, 0],
            [0, 0, self.zRadius],
            [0, self.yRadius, 0],
            [0, self.yRadius * -1.0, 0]
        ]

    #define function to update and instantiate box points for drawing
    def setOuterBox(self):
        self.outerBox = [
            #front face 
            [-self.xRadius, -self.yRadius, self.zRadius], 
            [-self.xRadius, self.yRadius, self.zRadius],
            [self.xRadius, self.yRadius, self.zRadius],
            [self.xRadius, -self.yRadius, self.zRadius],
            #back face
            [-self.xRadius, -self.yRadius,-self.zRadius],
            [-self.xRadius, self.yRadius,-self.zRadius],
            [self.xRadius, self.yRadius,-self.zRadius],
            [self.xRadius, -self.yRadius,-self.zRadius]

        ]

    #define function to set the points necessary to draw the xy grid
    def setGrid(self):
        self.grid =[
            [-self.xRadius, -self.yRadius, 0],
            [-self.xRadius, self.yRadius, 0],
            [self.xRadius, self.yRadius, 0],
            [self.xRadius, -self.yRadius, 0]
        ]

        self.gridFrontX = []
        for i in range(int(self.numGridLines//2+1)):
            x = 0 + i * self.gridGapX
            self.gridFrontX.append([x, self.yRadius, 0]) 
            self.gridFrontX.append([-x, self.yRadius, 0])

        self.gridFrontY = []
        for j in range(int(self.numGridLines//2+1)):
            y = 0 + j * self.gridGapY
            self.gridFrontY.append([self.xRadius, y, 0])
            self.gridFrontY.append([self.xRadius, -y, 0])

    #define function to scale the graph
    def scaleGraph(self, xScope, yScope, zScope, numGridLines):
        self.xScope = xScope
        self.yScope = yScope
        self.zScope = zScope
        self.xRadius = xScope/2
        self.yRadius = yScope/2
        self.zRadius = zScope/2
        self.numGridLines = numGridLines

        self.gridGapY = self.yScope / self.numGridLines
        self.gridGapX = self.xScope / self.numGridLines
        self.setAxis()
        self.setOuterBox()
        self.setGrid()

