#note about orientation
#graphics 3d is going to have -z axis pointing out
#you will need to adust for this when plotting points
#maybe allow for the user to select an orientation with rotation matrices

#main goals for graph:
#graph needs to be scalable with a rescale function
#graph needs to end in correct orientation considering the incorrect orientation of screen 3d graphics

#none of the points in this class should be modified in main 
class graph:

    def __init__(self, xScope, yScope, zScope, numGridLines):
        self.xScope = xScope
        self.yScope = yScope
        self.zScope = zScope

        #the number of lines in each direction on the grid
        self.numGridLines = numGridLines
        self.gridGapY = self.yScope / self.numGridLines
        self.gridGapX = self.xScope / self.numGridLines

        self.xRadius = xScope/2
        self.yRadius = yScope/2
        self.zRadius = zScope/2

        #faces defined clockwise from bottom left
        self.setOuterBox()

        #start at positive x go counter clockwise then up down
        #first point is center of the axis
        self.setAxis()

        #set the grid
        self.setGrid()

        #an array to hold the points to be graphed of the function
        self.fPoints = []


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

    #sets the xy grid
    #this includes the correct code to set each front vertex of the grid
    #need to set points from 0,0,0 so that they are consistent gap from the origin
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

        print(self.gridFrontX)
        print(self.gridFrontY)


    def scaleGraph(self, xScope, yScope, zScope, numGridLines):
        self.xScope = xScope
        self.yScope = yScope
        self.zScope = zScope
        self.numGridLines = numGridLines

        self.gridGapY = self.yScope / self.numGridLines
        self.gridGapX = self.xScope / self.numGridLines
        self.setAxis()
        self.setOuterBox()

    #rotates all points that are part of the graph to correct mathematical orientation
    def correctGraphOrientation(self):
        pass