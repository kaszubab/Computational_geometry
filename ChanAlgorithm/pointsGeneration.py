import numpy as np
#generating points on rectangle

# #random
# randPoints1 = getRandomPoints(400,0,150)
# #circle
# pointsCircle1 = getCirclePoints(200,(80,-10),10)
# #rectangle
# rectangle1 = getRectangle(500,[(-15,15),(-15,-15),(15,-15),(15,15)])
# #square with diagonals
# crossSquare1 = getCrossSquare(100,100,[(0,0),(20,0),(20,20),(0,20)])



def getRectangle(pointsQuantity, vertices):
    # making assumption that rectangle sides are parallel to axes
    rectangle = []
    points = [np.random.randint(0,4) for x in range(pointsQuantity)]
    for x in points:
        if x == 0:
            y = np.random.uniform(vertices[1][1],vertices[0][1])
            rectangle.append((vertices[0][0],y))
        if x == 1:
            x = np.random.uniform(vertices[1][0],vertices[2][0])
            rectangle.append((x,vertices[1][1]))
        if x == 2:
            y = np.random.uniform(vertices[2][1],vertices[3][1])
            rectangle.append((vertices[2][0],y))
        if x == 3:
            x = np.random.uniform(vertices[0][0],vertices[3][0])
            rectangle.append((x,vertices[0][1]))
    return rectangle

#generating points on the sides and diagonals of rectangle 
def getCrossSquare(pSides, pCross, vertices):
    #rectangle vertices passed as in example below
    square = []
    square += vertices
    square +=[(vertices[0][0],np.random.uniform(vertices[0][1],vertices[3][1])) for x in range(pSides)]
    square += [(np.random.uniform(vertices[0][0],vertices[1][0]),vertices[0][1]) for x in range(pSides)]
    square += [(vertices[0][0]+x,vertices[0][1]+x) for x in np.random.uniform(0,vertices[2][0]-vertices[0][0],pCross)]
    square += [(vertices[3][0]+x,vertices[3][1]-x) for x in np.random.uniform(0,vertices[1][0]-vertices[3][0],pCross)]
    return square

#generating random points from specified range
def getRandomPoints(pointsQuantity, leftBorder, rightBorder):
    randPoints = [(np.random.uniform(leftBorder,rightBorder)
                   ,np.random.uniform(leftBorder,rightBorder)) 
                  for x in range(pointsQuantity)]
    return randPoints

# generating points on circle
def getCirclePoints(pointsQuantity, circleCenter, radius):
    pointsCircle = [(radius*np.sin((np.pi/2)*x)+circleCenter[0],
                     radius*np.cos((np.pi/2)*x)+circleCenter[1])
                    for x in np.random.uniform(0,4,pointsQuantity)]
    return pointsCircle
