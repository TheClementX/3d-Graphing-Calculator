from cmu_graphics import *
import sympy as sp
import MatrixFunctions as mf

#import user created files
import Graph 
import function 
import math
from Button import *

#function to hold all relevant app variables and buttons
def onAppStart(app):
    # graph app variables
    app.setMaxShapeCount(10_000)

    #set default graph dimensions and precision
    app.numGridLines = '40'
    app.xScope = '20'
    app.yScope = '20' 
    app.zScope = '20'
    app.selectedScope = None
    app.drawGrid = True
    app.drawBox = True
    
    #set necessary variables for project function 
    #set up cmu graphics variables and instantiate necessary graphs
    app.stepsPerSecond = 60
    app.width = 1000
    app.height = 1000
    app.graph = Graph.graph(int(app.xScope), int(app.yScope), int(app.zScope), int(app.numGridLines))
    app.matrices = mf.matrices()

    #variables used to project graph points and function points to the screen
    app.scaleString = '20'
    app.scale = None
    setScaleFactor(app)
    app.xoffset = app.width/2
    app.yoffset = app.height/2
    app.rotating = True

    #variables for setting graph function
    #necessary function calls to create first graph instance
    app.function = function.function()
    app.function.string_function = 'x**2 - y**2'
    app.function.setSpFunction()
    app.function.generateFunctionPoints(app.graph.xRadius, app.graph.yRadius, app.graph.zRadius, app.graph.numGridLines)
    
    #variables to set the apps mode 
    app.funcMode = False
    app.insertMode = True
    app.error = False
    app.scaleMode = False
    app.helpMode = False

    #instantiation of buttons used throughout the app 
    app.scaleButton = Button(175, 50, 'Enter Scale Mode', 20)
    app.insertButton = Button(200, 50, 'Enter Insert Mode', 20)
    app.functionButton = Button(200,50,'Enter Function Mode', 20)
    app.zoomInButton = Button(125,50, 'Zoom +', 15)
    app.zoomOutButton = Button(125, 50, 'Zoom -', 15)
    app.helpButton = Button(75,50,'Help', 20)
    app.rotateButton = Button(150,50, 'Rotate on/off', 15)
    app.resetButton = Button(150,50,'Reset', 20)

    #instantiation of function mode's movement buttons
    app.upButton = Button(50,50,'up', 15)
    app.downButton = Button(50,50,'down', 15)
    app.leftButton = Button(50,50,'left', 15)
    app.rightButton = Button(50,50,'right', 15)

    #instantiation of scale mode buttons 
    app.xPlusButton = Button(150,50, 'X Scale +', 20)
    app.xMinusButton = Button(150,50, 'X Scale -', 20)
    app.yPlusButton = Button(150,50, 'Y Scale +', 20)
    app.yMinusButton = Button(150,50, 'Y Scale -', 20)
    app.zPlusButton = Button(150,50, 'Z Scale +', 20)
    app.zMinusButton = Button(150,50, 'Z Scale -', 20)
    app.nPlusButton = Button(150, 50, 'Grid Lines +', 20)
    app.nMinusButton = Button(150, 50, 'Grid Lines -', 20)
    app.gridToggleButton = Button(100,50, 'Grid On', 20)
    app.boxToggleButton = Button(100, 50, 'Box On', 20)

#utility function to set app.scale (the drawing scale factor)
def setScaleFactor(app):
    app.scale = int(app.scaleString)

#drawing helper function to draw all necessary graph elements   
def drawGraph(app):
    #instantion of point lists for drawing
    outerBoxPoints = []
    axisPoints = []
    gridPoints = []

    #logic to scale outerBox of the graph
    for point in app.graph.outerBox:
        transformedPoint = makeDrawablePoint(app, point)       
        outerBoxPoints.append(transformedPoint)
    
    #logic to scale Axis of the graph
    for point in app.graph.xyzAxis:
        transformedPoint = makeDrawablePoint(app, point)        
        axisPoints.append(transformedPoint)

    #logic to scale gridlines of the graph
    for point in app.graph.grid:
        transformedPoint = makeDrawablePoint(app, point)
        gridPoints.append(transformedPoint)


    #logic to draw outer box of the graph
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


    #logic to draw axis of the graph
    center = axisPoints[0]
    for point in axisPoints:
        if point is center:
            continue
        drawLine(center[0], center[1], point[0], point[1])

    #call to drawGrid helper function to draw the graph Grid
    if app.drawGrid:
        drawGrid(app)

#funtion to apply perspective projection and rotate points if app is rotating
def makeDrawablePoint(app, point):
    #convert point orientation mathematical x,y,z orienation
    transformedPoint = app.matrices.correctPointOrientation(point)

    #use rotation matrix with current theta values to position point properly on the screen
    transformedPoint = mf.projectPoint(app.matrices.xRotationMatrix, transformedPoint)
    transformedPoint = mf.projectPoint(app.matrices.yRotationMatrix, transformedPoint)
    transformedPoint = mf.projectPoint(app.matrices.zRotationMatrix, transformedPoint)

    #scale the point and then apply perspective projection to it
    transformedPoint = mf.scalePoint(transformedPoint, app.scale, app.xoffset, app.yoffset)
    transformedPoint = mf.projectPoint(app.matrices.projectionMatrix, transformedPoint)

    return transformedPoint

#helper function to draw the grid of the graph
def drawGrid(app):
    #draw x lines
    for point in app.graph.gridFrontX:
        backPoint = [point[0], point[1] - point[1] * 2, point[2]]
        transformedPoint1 = makeDrawablePoint(app, point)
        transformedPoint2 = makeDrawablePoint(app, backPoint)
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1], fill='red')

    #draw y lines
    for point in app.graph.gridFrontY:
        backPoint = [point[0] - point[0] * 2, point[1], point[2]]
        transformedPoint1 = makeDrawablePoint(app, point)
        transformedPoint2 = makeDrawablePoint(app, backPoint)
        drawLine(transformedPoint1[0], transformedPoint1[1], transformedPoint2[0], transformedPoint2[1], fill='green')

#helper function to iterate through function points and draw them to the screen
def drawFunction(app):
    for point in app.function.points:
        transformedPoint = makeDrawablePoint(app, point)
        drawCircle(transformedPoint[0], transformedPoint[1], 4, fill='purple')

#draw function 
def redrawAll(app):
    drawUI(app)

#function to draw all relevant UI aspects for the current app mode
#uses the mode boolean variables from app to determine mode
def drawUI(app):
    #draw help button so it is always visible
    app.helpButton.drawButton(50, 950)

    #draw help mode elements
    if app.helpMode:
        #set button visibility to avoid accidental button presses of invisible buttons
        app.functionButton.visible = False
        app.scaleButton.visible = False
        app.insertButton.visible = False
        app.zoomInButton.visible = False
        app.zoomOutButton.visible = False

        #draw relevant information on screen 
        #draw general instructions
        drawRect(50,50,900, app.height/4, fill = None, border ='black', borderWidth = 5)
        drawLabel('General Instructions: ', 165, 75, size = 20, bold = True)
        drawLabel('Click help to enter/exit help mode', app.width/2, 75, size = 20)
        drawLabel('This calculator uses four modes: scale, insert, function, and help mode ', app.width/2, 125, size = 20)
        drawLabel('In scale mode you can scale the graph and adjust precision using number of grid lines', app.width/2, 175, size = 20)
        drawLabel('In function mode you can view the function', app.width/2, 225, size = 20)
        drawLabel('In insert mode you can set the function to be graphed using the keyboard', app.width/2, 275, size = 20)

        #draw scale mode instructions
        drawRect(50,350 , 900, app.height/4, fill = None, border ='black', borderWidth = 5)
        drawLabel('Scale Mode Instructions: ', 185, 375, size = 20, bold = True)
        drawLabel('to select the field to be changed press x,y,z or n on the keyboard', app.width/2, 425, size = 20)
        drawLabel('then type in the change you want to be made', app.width/2, 475, size = 20)
        drawLabel('press the "a" key to apply the changes to the graph ', app.width/2, 525, size = 20)
        drawLabel('alternatively press the buttons to change graph properties by +/-2', app.width/2, 575, size = 20)
        
        #draw Function mode instructions
        drawRect(50, 650 , 900, app.height/4 , fill = None, border ='black', borderWidth = 5)
        drawLabel('Function Mode Instructions: ', 200, 675, size =20, bold = True )
        drawLabel('In function mode you can view the function entered in insert mode ', app.width/2, 725, size = 20)
        drawLabel('press the zoom + or zoom - button to change zoom', app.width/2, 775, size = 20)
        drawLabel('press the rotating button to stop/start rotation', app.width/2, 825, size = 20)
        drawLabel('use w/s, a/d, and t/g or arrow buttons to rotate the graph', app.width/2, 875, size = 20)

    #draw function mode elements
    elif app.funcMode:
        #set button visibility
        app.functionButton.visible = False
        app.insertButton.visible = True
        app.scaleButton.visible = True
        app.zoomInButton.visible = True
        app.zoomOutButton.visible = True

        #draw title
        drawLabel('Function Mode', app.width/2, 50, size = 60, italic = True)

        #draw graph and function using helper functions
        drawFunction(app)
        drawGraph(app)

        # draw all relevent labels
        drawLabel(f'function: {app.function.string_function}',(app.width/2),100, size = 30)
        drawLabel(f'X len:  {str(app.graph.xScope)}', 50, 20, size = 20)
        drawLabel(f'Y len:  {str(app.graph.yScope)}', 50, 60, size = 20)
        drawLabel(f'Z len:  {str(app.graph.zScope)}', 50, 100, size = 20)
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

    #draw insert mode elements
    elif app.insertMode:
        app.insertButton.visible = False
        app.scaleButton.visible = True
        app.functionButton.visible = True

        drawLabel('3D Graphing Calculator', app.width/2, 50, size = 60, bold = True, italic = True)
        drawLabel('Insert Mode', app.width/2, 150, size = 60, italic = True)
        drawLabel('press Help for instructions', app.width/2, 250, size = 30, italic = True)
        drawLabel(f'f(x, y) = {app.function.string_function}', app.width/2 , app.height/2 - 50, size=60)
        drawLabel('(Enter a function in terms of x and y)', app.width/2, app.height/2+20, size=30)
        drawLabel('(use standard function names and () to surround variables)', app.width/2, app.height/2+60, size=30)
        drawLabel('(use ** for exponential functions)', app.width/2, app.height/2+100, size=30)
        app.scaleButton.drawButton(200, 950)
        app.functionButton.drawButton(400, 950)

    #draw scale mode elements
    elif app.scaleMode:
        #set button visibility 
        app.scaleButton.visible = False
        app.insertButton.visible = True
        app.functionButton.visible = True

        #draw relevant labels/information
        drawLabel('Scale Mode', app.width/2, 50, size = 60, italic = True)
        drawLabel(f'X scale:  {str(app.xScope)}', app.width/2, app.height/2 - 40, size=30)
        drawLabel(f'Y scale:  {str(app.yScope)}', app.width/2, app.height/2, size=30)
        drawLabel(f'Z scale:  {str(app.zScope)}', app.width/2, app.height/2 + 40, size=30)
        drawLabel(f'Num GridLines:  {str(app.numGridLines)}', app.width/2, app.height/2 + 80, size=30)
        drawLabel(f'Grid Lines On: {app.drawGrid}', app.width/2, app.height/2-80, size = 30)
        drawLabel(f'Box On: {app.drawBox}', app.width/2, app.height/2-120, size = 30)
        
        #draw buttons
        app.insertButton.drawButton(200, 950)
        app.functionButton.drawButton(425, 950)

        #draw scale buttons
        app.xPlusButton.drawButton(app.width/2 - 350, 700)
        app.xMinusButton.drawButton(app.width/2 - 350, 800)
        app.yPlusButton.drawButton(app.width/2 - 150, 700)
        app.yMinusButton.drawButton(app.width/2 - 150, 800)
        app.zPlusButton.drawButton(app.width/2 + 150, 700)
        app.zMinusButton.drawButton(app.width/2 + 150, 800)
        app.nPlusButton.drawButton(app.width/2 + 350, 700)
        app.nMinusButton.drawButton(app.width/2 + 350, 800)
        app.gridToggleButton.drawButton(app.width/2, 700)
        app.boxToggleButton.drawButton(app.width/2, 800)

#time based step functions / event loop equivalent
def onStep(app):
    if app.funcMode:
        takeStep(app)

#update theta variables and value of rotation matrices on step 
def takeStep(app):
    #update theta values
    if app.rotating:
        app.matrices.tx += 0.01
        app.matrices.ty += 0.01
        app.matrices.tz += 0.01

    #update rotation matrices
    app.matrices.updateXRotation()
    app.matrices.updateYRotation()
    app.matrices.updateZRotation()


#function to determine if buttons are pressed and trigger subsequent actions
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
        try:
            app.error = False
            app.function.setSpFunction()
            app.function.generateFunctionPoints(app.graph.xRadius, app.graph.yRadius, app.graph.zRadius, app.graph.numGridLines)
            app.funcMode = True
            app.insertMode = False
            app.scaleMode = False
        except:
            pass

    if app.upButton.getPressed(mouseX, mouseY): app.matrices.tx -= math.pi/12
    if app.downButton.getPressed(mouseX, mouseY): app.matrices.tx += math.pi/12
    if app.leftButton.getPressed(mouseX, mouseY): app.matrices.ty += math.pi/12
    if app.rightButton.getPressed(mouseX, mouseY): app.matrices.ty -= math.pi/12
    if app.resetButton.getPressed(mouseX, mouseY):
        app.matrices.ty = 0 
        app.matrices.tz = 0 
        app.matrices.tx = 0
    if app.rotateButton.getPressed(mouseX, mouseY): app.rotating = not app.rotating
    if app.scaleMode:
        if app.xPlusButton.getPressed(mouseX, mouseY) and int(app.xScope) < 50:
            app.xScope = str(int(app.xScope) + 2)
        if app.xMinusButton.getPressed(mouseX, mouseY) and int(app.xScope) > 0:
            app.xScope = str(int(app.xScope) - 2)

        if app.yPlusButton.getPressed(mouseX, mouseY) and int(app.yScope) < 50:
            app.yScope = str(int(app.yScope) + 2)
        if app.yMinusButton.getPressed(mouseX, mouseY) and int(app.yScope) > 0:
            app.yScope = str(int(app.yScope) - 2)
            
        if app.zPlusButton.getPressed(mouseX, mouseY) and int(app.zScope) < 50:
            app.zScope = str(int(app.zScope) + 2)
        if app.zMinusButton.getPressed(mouseX, mouseY) and int(app.zScope) > 0:
            app.zScope = str(int(app.zScope) - 2)
            
        if app.nPlusButton.getPressed(mouseX, mouseY) and int(app.numGridLines) < 100:
            app.numGridLines = str(int(app.numGridLines) + 2)
        if app.nMinusButton.getPressed(mouseX, mouseY) and int(app.numGridLines) > 0:
            app.numGridLines = str(int(app.numGridLines) - 2)
        if app.gridToggleButton.getPressed(mouseX, mouseY):
            app.drawGrid = not app.drawGrid
        if app.boxToggleButton.getPressed(mouseX, mouseY):
            app.drawBox = not app.drawBox
            
        #update graph and function based on scale mode changes
        app.graph.scaleGraph(int(app.xScope), int(app.yScope), int(app.zScope), int(app.numGridLines) )
        app.function.generateFunctionPoints(app.graph.xRadius, app.graph.yRadius, app.graph.zRadius, app.graph.numGridLines)

#function for key press key binds used during development 
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
            pass 

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

#call to the main function and main function definition
def main(app):
    runApp()

main(app)
