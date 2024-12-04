3D Graphing Calculator Read Me:
  This app implements a 3d graphing calculator using sympy. This app can graph any 3D function in terms of x and y.
  This app uses 4 different modes: help, scale, insert, and function mode. Help mode is accessible by clicking the help
  button and lists a quick guide to using the app. Function mode is accesible using the function mode button and is where
  the calculators graph is drawn. Insert mode is where the user may insert user defined functions in terms of x and y.
  Scale mode is where the user may edit the dimensions and precision of the graph in function mode.

Dependencies: in order to run this project you will need:
  -python 3
  -sympy 
  -cmu desktop graphics and its dependencies (documentation: https://academy.cs.cmu.edu/desktop)
  -it is recommend to create a virtual environment with your favorite python tool to run this code

How to Run Using a Shell:
  1. install all dependencies using pip
  2. if dependencies are installed globally skip to step 4
  3. if dependencies are installed using virtual environments, activate your venv in a shell
  4. open the source folder directory using your favorite shell
  5. run main.py using the command: python3 main.py

How to Run Using VsCode:
  1. install all dependencies using pip
  2. if dependencies are installed globally skip to step 4
  3. if dependencies are installed using virtual environments, activate your venv in vscodes shell window
  4. select main.py
  5. click run in the upper right hand corner or type: python3 main.py in vscodes shell window

Shortcuts:
  while not necessary these shortcuts can be ussed to navigate the calculator:
  F: go to function mode
  I: go to insert mode
  S: go to scale mode
  r: toggle rotation in functiono mode
  +/-: adjust zoom in function mode
  u: reset function orientation in function mode
  w/s: rotate around x axis in function mode
  a/d: rotate around z axis in function mode
  t/g: rotate around y axis in function mode
