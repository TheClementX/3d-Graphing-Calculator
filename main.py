from cmu_graphics import *
import sympy as sp
import numpy as np
import MatrixFunctions as mf
import Graph 
import function 


def onAppStart(app):
    app.stepsPerSecond = 60
    app.width = 1000
    app.height = 1000
    app.graph = Graph.graph(20,20,20,15)
    app.matrices = mf.matrices()

    #varibales used in scale point
    #20x20 box is something to consider
    app.scale = 20
    app.xoffset = app.width/2
    app.yoffset = app.height/2

    app.rotating = True

    #equation related variables
    app.function = function.function()
    app.function.string_function = '(x**2) /10 + (y**2) / 10 '
    app.function.setSpFunction()
    app.function.generateFunctionPoints(app.graph.numGridLines, app.graph.numGridLines, 1)
    #app.function.printPoints()

#circles are drawing in the correct place
#add spin scaling and lines next
def drawGraph(app):

    outerBoxPoints = []
    axisPoints = []
    gridPoints = []

    #apply necessary transformations to each element of the graph not including the function
    #function will be drawn in a seperate function for clarity

    #scaling can and should be put into a function at
    #scale outerBox
    for point in app.graph.outerBox:
        transformedPoint = makeDrawablePoint(app, point)       
        #rotation
        outerBoxPoints.append(transformedPoint)
        drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')
    
    #scale Axis
    for point in app.graph.xyzAxis:
        transformedPoint = makeDrawablePoint(app, point)        
        #regular Scaling
        axisPoints.append(transformedPoint)
        drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')

    #scale grid
    for point in app.graph.grid:
        #fix orientation of the grid
        transformedPoint = makeDrawablePoint(app, point)
        gridPoints.append(transformedPoint)
        drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')


    #connect points
    #draw box
    front = outerBoxPoints[:4]
    back = outerBoxPoints[4:]
    for i in range(4):
        if i == 3:
            drawLine(front[i][0], front[i][1], front[0][0], front[0][1])
            drawLine(back[i][0], back[i][1], back[0][0], back[0][1])
        else:
            drawLine(front[i][0], front[i][1], front[i+1][0], front[i+1][1])
            drawLine(back[i][0], back[i][1], back[i+1][0], back[i+1][1])

        drawLine(front[i][0], front[i][1], back[i][0], back[i][1])


    #draw axis
    center = axisPoints[0]
    for point in axisPoints:
        if point is center:
            continue
        drawLine(center[0], center[1], point[0], point[1])

    #draw Grid
    drawGrid(app)

    #draw grid
#does all the point transformation
#includes rotation if app is rotating
def makeDrawablePoint(app, point):
    transformedPoint = app.matrices.correctPointOrientation(point)

    if app.rotating:
        transformedPoint = mf.projectPoint(app.matrices.xRotationMatrix, transformedPoint)
        transformedPoint = mf.projectPoint(app.matrices.yRotationMatrix, transformedPoint)
        transformedPoint = mf.projectPoint(app.matrices.zRotationMatrix, transformedPoint)

    transformedPoint = mf.scalePoint(transformedPoint, app.scale, app.xoffset, app.yoffset)
    transformedPoint = mf.projectPoint(app.matrices.projectionMatrix, transformedPoint)

    return transformedPoint

#draws the grid 
def drawGrid(app):
    for point in app.graph.gridFrontX:
        backPoint = [point[0], point[1] - point[1] * 2, point[2]]
        transformedPoint1 = makeDrawablePoint(app, point)
        transformedPoint2 = makeDrawablePoint(app, backPoint)
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1])

    for point in app.graph.gridFrontY:
        backPoint = [point[0] - point[0] * 2, point[1], point[2]]
        transformedPoint1 = makeDrawablePoint(app, point)
        transformedPoint2 = makeDrawablePoint(app, backPoint)
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1])

#draw the function 
def drawFunction(app):
    for point in app.function.points:
        transformedPoint = makeDrawablePoint(app, point)
        drawCircle(transformedPoint[0], transformedPoint[1], 4, fill='purple')

def redrawAll(app):
    # print(app.graph.xyzAxis)
    # print(app.graph.xyzAxis)
    # print(app.ms.xRotationMatrix)
    drawGraph(app)
    # print(app.function.f, "done")
    # print(app.function.points, "done")
    drawFunction(app)

#time based step functions / event loop equivalent
def onStep(app):
    if app.rotating:
        takeStep(app)
 
#this is properly updating 
def takeStep(app):
    #rotation works
    if app.rotating:
        app.matrices.tx += 0.01
        app.matrices.ty += 0.01
        app.matrices.tz += 0.01
        
        app.matrices.updateXRotation()
        app.matrices.updateYRotation()
        app.matrices.updateZRotation()




    #mf.projectPoint(app.matrices.)

def onKeyPress(app, key):
    if key == 'x': app.equation += 'x'
    if key == 'y': app.equation += 'y'
    if key == '+': app.equation += '+'
    if key == '-': app.equation += '-'
    if key == '*': app.equation += '*'
    if key == '/': app.equation += '/'
    if key.isdigit(): app.equation += key
    if key == 'backspace': app.equation = app.equation[:-1]
    if key == 'c': app.equation = ''
    if key == 'enter': pass


def main(app):
    runApp()

main(app)