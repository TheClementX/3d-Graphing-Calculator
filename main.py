from cmu_graphics import *
import sympy as sp
import numpy as np
import MatrixFunctions as mf
import Graph 
import function 
import math
from Button import *

def onAppStart(app):
    # graph app variables
    app.setMaxShapeCount(10_000)
    app.numGridLines = '10'
    app.xScope = '30'
    app.yScope = '20' 
    app.zScope = '20'
    app.selectedScope = None
    app.drawGrid = True
    app.drawBox = True
    
    #scale Mode
    app.stepsPerSecond = 60
    app.width = 1000
    app.height = 1000
    app.graph = Graph.graph(int(app.xScope), int(app.yScope), int(app.zScope), int(app.numGridLines))
    app.matrices = mf.matrices()

    #varibales used in scale point
    #20x20 box is something to consider
    app.scaleString = '20'
    app.scale = None
    setScaleFactor(app)

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
    app.insertMode = False
    app.error = False
    app.scaleMode = False
    app.helpMode = True

    #buttons
    app.scaleButton = Button(150, 50, 'Scale Mode', 20,)
    app.insertButton = Button(175, 50, 'Insert Mode', 20)
    app.functionButton = Button(175,50,'Function Mode', 20)
    app.zoomInButton = Button(125,50, 'Zoom +', 15)
    app.zoomOutButton = Button(125, 50, 'Zoom -', 15)
    app.helpButton = Button(75,50,'Help', 20)
    app.rotateButton = Button(150,50, 'Rotate', 20)
    app.resetButton = Button(150,50,'Reset', 20)

    #movement buttons
    app.upButton = Button(50,50,'up', 15)
    app.downButton = Button(50,50,'down', 15)
    app.leftButton = Button(50,50,'left', 15)
    app.rightButton = Button(50,50,'right', 15)
    #circles are drawing in the correct place spin scaling and lines next

    #apply necessary transformations to each element of the graph not including the function
    #function will be drawn in a seperate function for clarity

#handle the zoom of the drawing
def setScaleFactor(app):
    app.scale = int(app.scaleString)
   
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
#         drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')
    
    #scale Axis
    for point in app.graph.xyzAxis:
        transformedPoint = makeDrawablePoint(app, point)        
        #regular Scaling
        axisPoints.append(transformedPoint)
#         drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')

    #scale grid
    for point in app.graph.grid:
        #fix orientation of the grid
        transformedPoint = makeDrawablePoint(app, point)
        gridPoints.append(transformedPoint)
#         drawCircle(transformedPoint[0], transformedPoint[1], 5, fill='red')


    #connect points
    #draw box
    if app.drawBox:
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
    if app.drawGrid:
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
    app.helpButton.drawButton(50, 950)
    if app.helpMode:
        app.functionButton.visible = False
        app.scaleButton.visible = False
        app.insertButton.visible = False
        app.zoomInButton.visible = False
        app.zoomOutButton.visible = False

        #draw relevant information on screen 
        drawRect(50,50,900, app.height/4, fill = None, border ='black', borderWidth = 5)
        drawLabel('General Instructions: ', 165, 75, size = 20, bold = True)
        drawLabel('Click help to enter/exit help mode', app.width/2, 75, size = 20)
        drawLabel('This calculator uses four modes: scale, insert, function, and help mode ', app.width/2, 125, size = 20)
        drawLabel('In scale mode you can scale the graph and adjust precision using number of grid lines', app.width/2, 175, size = 20)
        drawLabel('In function mode you can view the function', app.width/2, 225, size = 20)
        drawLabel('In insert mode you can set the function to be graphed using the keyboard', app.width/2, 275, size = 20)

        drawRect(50,350 , 900, app.height/4, fill = None, border ='black', borderWidth = 5)
        drawLabel('Scale Mode Instructions: ', 185, 375, size = 20, bold = True)
        drawLabel('to select the field to be changed press x,y,z or n on the keyboard', app.width/2, 425, size = 20)
        drawLabel('then type in the change you want to be made', app.width/2, 475, size = 20)
        drawLabel('press the "a" key to apply the changes to the graph ', app.width/2, 525, size = 20)
        drawLabel('alternatively press the buttons to change graph properties by +/-2', app.width/2, 575, size = 20)
        
        drawRect(50, 650 , 900, app.height/4 , fill = None, border ='black', borderWidth = 5)
        drawLabel('Function Mode Instructions: ', 200, 675, size =20, bold = True )
        drawLabel('In function mode you can view the function entered in insert mode ', app.width/2, 725, size = 20)
        drawLabel('press the zoom + or zoom - button to change zoom', app.width/2, 775, size = 20)
        drawLabel('press the rotating button to stop/start rotation', app.width/2, 825, size = 20)
        drawLabel('use w/s, a/d, and t/g or arrow buttons to rotate the graph', app.width/2, 875, size = 20)



    elif app.funcMode:
        app.functionButton.visible = False
        app.insertButton.visible = True
        app.scaleButton.visible = True
        app.zoomInButton.visible = True
        app.zoomOutButton.visible = True

        drawLabel('Function Mode', app.width/2, 50, size = 60, italic = True)
        drawFunction(app)
        drawGraph(app)

        # draw all relevent labels
        drawLabel(f'function: {app.function.string_function}',(app.width/2),100, size = 20)
        drawLabel(f'X len:  {str(app.graph.xScope)}', 50, 10)
        drawLabel(f'Y len:  {str(app.graph.yScope)}', 50, 30)
        drawLabel(f'Z len:  {str(app.graph.zScope)}', 50, 50)
        drawLabel(f'zoom: {app.scale}', 920, 10, size = 15)
        drawLabel(f'next zoom: {app.scaleString}', 920, 30, size = 15)

        #draw Buttons 
        app.scaleButton.drawButton(200, 950)
        app.insertButton.drawButton(400, 950)
        app.zoomInButton.drawButton(920, 80)
        app.zoomOutButton.drawButton(920, 140)
        app.rotateButton.drawButton(920, 200)
        app.resetButton.drawButton(920, 260)

        #draw movement buttons
        app.upButton.drawButton(875, 875)
        app.downButton.drawButton(875, 975)
        app.rightButton.drawButton(950, 925)
        app.leftButton.drawButton(800, 925)

    elif app.insertMode:
        app.insertButton.visible = False
        app.scaleButton.visible = True
        app.functionButton.visible = True

        drawLabel('3D Graphing Calculator', app.width/2, 50, size = 60, bold = True, italic = True)
        drawLabel('Insert Mode', app.width/2, 150, size = 60, italic = True)
        drawLabel(f'f(x, y) = {app.function.string_function}', app.width/2 , app.height/2 - 50, size=60)
        app.scaleButton.drawButton(200, 950)
        app.functionButton.drawButton(400, 950)

    elif app.scaleMode:
        app.scaleButton.visible = False
        app.insertButton.visible = True
        app.functionButton.visible = True

        drawLabel('Scale Mode', app.width/2, 50, size = 60, italic = True)
        drawLabel('press I to return to insert mode', app.width/2, 100, size = 20, bold = True)
        drawLabel(f'X scale:  {str(app.xScope)}', app.width/2, app.height/2 - 40, size=30)
        drawLabel(f'Y scale:  {str(app.yScope)}', app.width/2, app.height/2, size=30)
        drawLabel(f'Z scale:  {str(app.zScope)}', app.width/2, app.height/2 + 40, size=30)
        drawLabel(f'Num GridLines:  {str(app.numGridLines)}', app.width/2, app.height/2 + 80, size=30)

        drawLabel(f'Grid Lines On: {app.drawGrid}', app.width/2, app.height/2-80, size = 30)
        drawLabel(f'Box On: {app.drawBox}', app.width/2, app.height/2-120, size = 30)
        
        app.insertButton.drawButton(200, 950)
        app.functionButton.drawButton(400, 950)
    elif app.error:
        drawLabel('invalid function entered', 800, 200)

#time based step functions / event loop equivalent
def onStep(app):
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



def onMousePress(app, mouseX, mouseY):
    if app.zoomInButton.getPressed(mouseX, mouseY):
        if app.scale < 50: app.scale += 2
    if app.zoomOutButton.getPressed(mouseX, mouseY):
        if app.scale >0: app.scale -= 2
    if app.helpButton.getPressed(mouseX, mouseY):
        app.helpMode = not app.helpMode
        if not app.funcMode and not app.scaleMode and not app.insertMode: app.insertMode = True
    if app.scaleButton.getPressed(mouseX, mouseY):
        app.scaleMode = True
        app.funcMode = False
        app.insertMode = False
    if app.insertButton.getPressed(mouseX, mouseY):
        app.insertMode = True
        app.funcMode = False
        app.scaleMode = False
    if app.functionButton.getPressed(mouseX, mouseY):
        app.funcMode = True
        app.insertMode = False
        app.scaleMode = False 
    if app.upButton.getPressed(mouseX, mouseY): app.matrices.tx -= math.pi/12
    if app.downButton.getPressed(mouseX, mouseY): app.matrices.tx += math.pi/12
    if app.leftButton.getPressed(mouseX, mouseY): app.matrices.ty += math.pi/12
    if app.rightButton.getPressed(mouseX, mouseY): app.matrices.ty -= math.pi/12
    if app.resetButton.getPressed(mouseX, mouseY):
        app.matrices.ty = 0 
        app.matrices.tz = 0 
        app.matrices.tx = 0
    if app.rotateButton.getPressed(mouseX, mouseY): app.rotating = not app.rotating

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
        if key == '?': app.function.string_function = ''
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
        if key.isdigit(): app.scaleString += key
        if key == 'backspace': app.scaleString = app.scaleString[:-1]
        if key == 'enter': setScaleFactor(app)
        if key == '+' and app.scale < 50: app.scale += 2
        if key == '-' and app.scale > 2: app.scale -= 2


    if app.scaleMode:
        if key == 'x': app.selectedScope = 'x' 
        if key == 'y': app.selectedScope = 'y' 
        if key == 'z': app.selectedScope = 'z'
        if key == 'n': app.selectedScope = 'n'
        if key == 'g': app.drawGrid = not app.drawGrid
        if key == 'b': app.drawBox = not app.drawBox
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
