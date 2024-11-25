from cmu_graphics import *
import sympy as sp
import numpy as np
import MatrixFunctions as mf
import Graph 
import function 
import math


def onAppStart(app):
    # graph app variables
    app.numGridLines = '10'
    app.xScope = '20'
    app.yScope = '20' 
    app.zScope = '20'
    app.selectedScope = None
    
    #scale Mode
    app.stepsPerSecond = 60
    app.width = 1000
    app.height = 1000
    app.graph = Graph.graph(int(app.xScope), int(app.yScope), int(app.zScope), int(app.numGridLines))
    app.matrices = mf.matrices()

    #varibales used in scale point
    #20x20 box is something to consider
    app.scale = 20
    app.xoffset = app.width/2
    app.yoffset = app.height/2

    app.rotating = True

    #function.string_function related variables
    app.function = function.function()
    app.function.string_function = 'sqrt(x)'
    app.function.setSpFunction()
    app.function.generateFunctionPoints(app.graph.xRadius, app.graph.yRadius, app.graph.zRadius, app.graph.numGridLines)
    #app.function.printPoints()
    
    #mode 
    app.funcMode = False
    app.insertMode = True
    app.error = False
    app.scaleMode = False

    #circles are drawing in the correct place spin scaling and lines next

    #apply necessary transformations to each element of the graph not including the function
    #function will be drawn in a seperate function for clarity
def drawGraph(app):

    outerBoxPoints = []
    axisPoints = []
    gridPoints = []

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
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1], fill='red')

    for point in app.graph.gridFrontY:
        backPoint = [point[0] - point[0] * 2, point[1], point[2]]
        transformedPoint1 = makeDrawablePoint(app, point)
        transformedPoint2 = makeDrawablePoint(app, backPoint)
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1], fill='green')

#draw the function 
def drawFunction(app):
    for point in app.function.points:
        transformedPoint = makeDrawablePoint(app, point)
        drawCircle(transformedPoint[0], transformedPoint[1], 4, fill='purple')

def redrawAll(app):

    drawUI(app)

def drawUI(app):
    if app.funcMode:
        drawGraph(app)
        drawFunction(app)

        # draw all relevent labels
        drawLabel(f'function: {app.function.string_function}',(app.width/2),950, size = 20)
        drawLabel(f'X len:  {str(app.graph.xScope)}', 50, 10)
        drawLabel(f'Y len:  {str(app.graph.yScope)}', 50, 30)
        drawLabel(f'Z len:  {str(app.graph.zScope)}', 50, 50)
    elif app.insertMode:
        drawLabel(f'function: {app.function.string_function}', app.width/2, app.height/2, size=60)
        drawLabel('General Key Binds: ', app.width/4 - 60, 20, size = 30)
        drawLabel('Insert Mode Key Binds: ', app.width * 2/4 - 10, 20, size = 30)
        drawLabel('Scale Mode Key Binds: ', app.width * 3/4 + 60, 20, size = 30)

    elif app.scaleMode:
        drawLabel(f'X scale:  {str(app.graph.xScope)}', app.width/2, app.height/2 - 40, size=15)
        drawLabel(f'Y scale:  {str(app.graph.yScope)}', app.width/2, app.height/2, size=15)
        drawLabel(f'Z scale:  {str(app.graph.zScope)}', app.width/2, app.height/2 + 40, size=15)
    elif app.error:
        drawLabel('invalid function entered', 800, 200)


#time based step functions / event loop equivalent
def onStep(app):
#     print(app.selectedScope, app.xScope, app.yScope, app.zScope)
#     print('graph', app.graph.xScope, app.graph.yScope, app.graph.zScope)
    if app.funcMode:
        takeStep(app)
 
#this is properly updating 
def takeStep(app):
    #rotation works
    if app.rotating:
        app.matrices.tx += 0.01
        app.matrices.ty += 0.01
        app.matrices.tz += 0.01
#     print(app.matrices.tx, app.matrices.ty, app.matrices.tz)    
    app.matrices.updateXRotation()
    app.matrices.updateYRotation()
    app.matrices.updateZRotation()




    #mf.projectPoint(app.matrices.)

def onKeyPress(app, key):

    if key == 'S':
        app.scaleMode = True
        app.insertMode = False
        app.funcMode = False
    if key == 'I':
        app.insertMode = True
        app.funcMode = False
        app.scaleMode = False
    if key == 'F':
        try:
            app.error = False
            app.function.setSpFunction()
            app.function.generateFunctionPoints(app.graph.xRadius, app.graph.yRadius, app.graph.zRadius, app.graph.numGridLines)
            app.funcMode = True
            app.insertMode = False
            app.scaleMode = False
        except:
            app.error = True

    if app.insertMode:
        if key == ')' or key == '(': app.function.string_function += key
        if key == '+': app.function.string_function += '+'
        if key == '-': app.function.string_function += '-'
        if key == '*': app.function.string_function += '*'
        if key == '/': app.function.string_function += '/'
        if key.isdigit(): app.function.string_function += key
        if key.isalpha() and len(key) == 1 and key != 'I' and key != 'F': app.function.string_function += key 
        if key == 'backspace': app.function.string_function = app.function.string_function[:-1]
        if key == 'q': app.function.string_function = ''
    if app.funcMode:
        if key == 'r': app.rotating = not app.rotating
        if key == 't': app.matrices.tz += math.pi/12
        if key == 'g': app.matrices.tz -= math.pi/12
        if key == 'w': app.matrices.tx -= math.pi/12
        if key == 's': app.matrices.tx += math.pi/12
        if key == 'a': app.matrices.ty -= math.pi/12
        if key == 'd': app.matrices.ty += math.pi/12
        if key == 'u': 
            app.matrices.tx= app.matrices.ty= app.matrices.tz = 0 
    if app.scaleMode:
        if key == 'x': app.selectedScope = 'x' 
        if key == 'y': app.selectedScope = 'y' 
        if key == 'z': app.selectedScope = 'z'
        if key == 'n': app.selectedScope = 'n'
        if key.isdigit():
            if app.selectedScope == 'x':
                app.xScope += key
            elif app.selectedScope == 'y':
                app.yScope += key
            elif app.selectedScope == 'z':
                app.zScope += key
            elif app.selectedScope == 'n':
                app.numGridLines += key

        if key == 'backspace':
            if app.selectedScope == 'x':
                app.xScope = app.xScope[:-1]
            elif app.selectedScope == 'y':
                app.yScope = app.yScope[:-1]
            elif app.selectedScope == 'z':
                app.zScope = app.zScope[:-1]
            elif app.selectedScope == 'n':
                app.numGridLines = app.numGridLines[:-1]

        if key == 'a': app.graph.scaleGraph(int(app.xScope), int(app.yScope), int(app.zScope), int(app.numGridLines) )

def main(app):
    runApp()

main(app)
