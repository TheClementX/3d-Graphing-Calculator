import math

class matrices:
    def __init__(self):
        #this stores theta
        self.tx = 0.01
        self.ty = 0.01
        self.tz = 0.01
        #projection matrix 
        #this is the simple version which I think should work for my purposes
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

    #takes in a point and corrects its orientation with rotation to correct mathematical orientation
    #rotate around x counter clockwise by pi/2
    #rotate around z counter clockwise by 3pi/2
    #works though it is clunky    
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


    # all matrices rotate counter clockwise around the positive acxis facing forward
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
#scales into pixels
def scalePoint(point, scale, xoffset, yoffset):
    result = []

    result.append(point[0]*scale + xoffset)
    result.append(point[1]*scale + yoffset)
    result.append(point[2])

    return result

def projectPoint(projection, point):
    result = [0,0,0]
    result[0] = point[0]*projection[0][0] + point[1]*projection[0][1] + point[2]*projection[0][2]
    result[1] = point[0]*projection[1][0] + point[1]*projection[1][1] + point[2]*projection[1][2]
    result[2] = point[0]*projection[2][0] + point[1]*projection[2][1] + point[2]*projection[2][2]

    return result
