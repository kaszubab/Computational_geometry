# computing determinant of 3 points
# takes 3 tuples consisting of 2 floats 
def determiner1(a,b,c):
    return a[0]*b[1] + a[1]*c[0] + b[0]*c[1] - a[0]*c[1] - a[1]*b[0] - b[1]*c[0]

#squared distance of 2 points (tuples with floats)
def squaredDist(a,b):
    return (a[0]-b[0])**2 + (a[1]-b[1])**2


#finds the desirable left-bottommost point which we start constructing convex hull from
def bottomLeft(points):
    minPoint = points[0]
    minPointId = 0
    for i in range (len(points)):
        if(points[i][1] < minPoint[1]):
            minPoint = points[i]
            minPointId = i
        elif(points[i][1] == minPoint[1] and points[i][0] < minPoint[0]):
            minPoint = points[i]
            minPointId = i
    return minPoint,minPointId


# orientation function used as comparator (returns -1 for left turn, 1 for right turn and 0 for points on line)

def orientation(a,b,c,det,eps):
    detResult = det(a,b,c)
    if abs(detResult) == 0:
        return 0
    if detResult > 0:
        return -1
    return 1

#bin search used to find initial points suspected of being in final hull

def modifiedBinSearch(convexHull, startPoint,eps):
    #initialize left and right point and left orientations
    l = 0
    r = len(convexHull)
    l_before = orientation(startPoint, convexHull[0], convexHull[-1], determiner1, eps)
    l_after = orientation(startPoint, convexHull[0], convexHull[(l+1) % len(convexHull)], determiner1, eps)
    #classical loop from bin search algorithm 
    while l < r :
        #calculate middle point and its orientations
        c = int((l+r)/2)
        c_before = orientation(startPoint, convexHull[c], convexHull[(c - 1) % len(convexHull)], determiner1, eps)
        c_after = orientation(startPoint, convexHull[c], convexHull[(c + 1) % len(convexHull)], determiner1, eps)
        c_side = orientation(startPoint, convexHull[l], convexHull[c], determiner1, eps)
        #point is on the right of its successor and predecessor
        if c_before != 1 and c_after != 1:
            return c
        #point is on the left side of left point and left point is on the right of its predessor or on the same side of its neighbours
        #or point is on the right side of left point and predecessor is on the right
        elif c_side == -1 and (l_after == 1 or l_before == l_after) or (c_side == 1 and c_before == 1):
            r = c
        #otherwise
        else:
            l = c + 1
            if l < len(convexHull) :
                l_before = -c_after
                l_after = orientation(startPoint, convexHull[l], convexHull[(l + 1) % len(convexHull)], determiner1, eps)
            
    return l;