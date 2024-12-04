import math

#define a class to store all necessary matrices and matrix operations
#these functions and matrices are used to create rotation and perspective projection when graphing
class matrices:
    def __init__(self):
        #instantiate theta values
        self.tx = 0.01
        self.ty = 0.01
        self.tz = 0.01

        #instantiate a projection matrix to turn 3d vectors into 2d vectors
        #I learned the concept of perspective projection from the youtuber Pythonista_
        #this is the url of a video tutorial showing how to rotate boxes in pygame using perspective projection
        #https://www.youtube.com/watch?v=qw0oY6Ld-L0
        self.projectionMatrix = [
            [1,0,0],
            [0,1,0],
            [0,0,0]
        ]

        #rotation matrices
        self.updateXRotation()
        self.updateYRotation()
        self.updateZRotation()

        #used to rotate every point to proper xyz orientation
        oRotationMatrix = []

    #define a function to take in a point and corrects its orientation to correct mathematical graphing
    #rotate around x counter clockwise by pi/2
    #rotate around z counter clockwise by 3pi/2
    def correctPointOrientation(self, point):
        tempx = self.tx
        tempz = self.tz

        self.tx = math.pi/2
        self.updateXRotation()
        self.tz = (3*math.pi)/2
        self.updateZRotation()

        result = projectPoint(self.xRotationMatrix, point)
        result = projectPoint(self.yRotationMatrix, result)

        self.tx = tempx
        self.updateXRotation()
        self.tz = tempz
        self.updateZRotation()

        return result


    #define a function to instantiate x,y,z rotation matrices
    #these rotation matrices are taken from wikipedia: https://en.wikipedia.org/wiki/Rotation_matrix
    #the knowledge of how to use them and apply linear transformations was learned from 3 blue 1 brown
    #I watched his course on essence of linear algebra: 
    #https://www.youtube.com/watch?v=fNk_zzaMoSs&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab
    def updateXRotation(self):
        self.xRotationMatrix = [
            [1, 0, 0],
            [0, math.cos(self.tx), -math.sin(self.tx)],
            [0, math.sin(self.tx), math.cos(self.tx)]
        ]

    def updateYRotation(self):
        self.yRotationMatrix = [
            [math.cos(self.ty), 0 , math.sin(self.ty)],
            [0,1,0],
            [-math.sin(self.ty), 0, math.cos(self.ty)]
        ]

    def updateZRotation(self):
        self.zRotationMatrix = [
            [math.cos(self.tz), -math.sin(self.tz), 0],
            [math.sin(self.tz), math.cos(self.tz) , 0],
            [0,0,1]
        ] 

#define a function to scale a point into a pixel point
def scalePoint(point, scale, xoffset, yoffset):
    result = []

    result.append(point[0]*scale + xoffset)
    result.append(point[1]*scale + yoffset)
    result.append(point[2])

    return result

#define a function to apply a single linear transformation to a point
def projectPoint(projection, point):
    result = [0,0,0]
    result[0] = point[0]*projection[0][0] + point[1]*projection[0][1] + point[2]*projection[0][2]
    result[1] = point[0]*projection[1][0] + point[1]*projection[1][1] + point[2]*projection[1][2]
    result[2] = point[0]*projection[2][0] + point[1]*projection[2][1] + point[2]*projection[2][2]

    return result
