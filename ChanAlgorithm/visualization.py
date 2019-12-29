import copy
from part2.Scenes import *
import part2.graham
from part2.helperFunctions import *


def visualizeConvexHull(convexHull):
    lines = []
    for x in range(len(convexHull)-1):
        lines.append([convexHull[x],convexHull[x+1]])
    lines.append([convexHull[len(convexHull)-1],convexHull[0]])
    return LinesCollection(lines), PointsCollection(convexHull)


def ChanVisualize(pointsInput, eps = 10*-12):
    
    randPoints = pointsInput
    iteration = 1

    while True:
        
        m = min(2**(2**iteration),len(pointsInput))
        
        Scenes = []
        convexHulls = []
        
        if m == len(pointsInput):
            cHull =  part2.graham.graham_scan(randPoints)
            miniLines, miniPoints = visualizeConvexHull(cHull)
            Scenes.append(Scene([PointsCollection(randPoints),PointsCollection(cHull)] ,[miniLines]))
            return Scenes
            
        

        for x in range(int(len(randPoints)/m)+1):

            miniConvexHull = part2.graham.graham_scan(randPoints[m*x:(x+1)*m])

            convexHulls.append(miniConvexHull)

        if convexHulls[-1] == []:
            del(convexHulls[-1])

        startPoint,_ = bottomLeft(randPoints)

        GreatConvexHull = []
        GreatConvexHull.append(startPoint)

        i = 0

        lines,points = [],[]

        for x in convexHulls:
            miniLines, miniPoints = visualizeConvexHull(x)
            lines.append(miniLines)
            points.append(miniPoints)

       
        Scenes.append(Scene([PointsCollection(randPoints)] + points,lines))
        Scenes.append(Scene([PointsCollection(randPoints)] + points+[PointsCollection(GreatConvexHull)] ,lines))

        smallestOrientationOfEachHull = []
        
        for x in convexHulls:
            index = modifiedBinSearch(x,GreatConvexHull[-1], eps)%len(x)
            if x[index] == GreatConvexHull[-1]:
                index += 1;
            smallestOrientationOfEachHull.append((x[index%len(x)],index%len(x)))
        
        for id,x in enumerate(convexHulls):
                
            index = smallestOrientationOfEachHull[id][1]
            startIndex = index
                
            while determiner1(GreatConvexHull[-1], smallestOrientationOfEachHull[id][0], x[(index + 1)%len(x)]) <= 10**-12:
                index = (index+1) % len(x)
                smallestOrientationOfEachHull[id] = (x[index],index)
                if (index == startIndex):
                    break
                

            if x[index%len(x)] == GreatConvexHull[-1]:
                index += 1;
            smallestOrientationOfEachHull[id] = (x[index%len(x)],index%len(x))        
        
        
        while 1:
            
            if (i == m):
                GreatConvexHull = None
                break
            
            point1 = GreatConvexHull[-1]
            


            Scenes.append(Scene([PointsCollection(randPoints),
                                 PointsCollection([x[0] for x in smallestOrientationOfEachHull],color='Red'),
                                 PointsCollection(copy.deepcopy(GreatConvexHull),color = 'Yellow'),
                                 PointsCollection([GreatConvexHull[-1]],color = 'Black')
                                ],lines))

            nextPoint = smallestOrientationOfEachHull[0][0]

            for x in smallestOrientationOfEachHull:
                detResult = determiner1(point1, nextPoint, x[0])
                if detResult <= 10 ** -8:
                    if detResult <= -10 ** -8 or (detResult > -10 ** -8 and squaredDist(point1, x[0]) > squaredDist(point1,nextPoint)):  
                        nextPoint = x[0]

            if nextPoint == GreatConvexHull[0]:
                break
            GreatConvexHull.append(nextPoint)
            
            if len (GreatConvexHull) > 2 and determiner1(GreatConvexHull[-3],GreatConvexHull[-2],GreatConvexHull[-1]) <= 10**-12:
                hullpoint1 = GreatConvexHull.pop()
                GreatConvexHull.pop()
                GreatConvexHull.append(hullpoint1)
            
            for id,x in enumerate(convexHulls):
                
                index = smallestOrientationOfEachHull[id][1]
                startIndex = index
                
                while determiner1(GreatConvexHull[-1], smallestOrientationOfEachHull[id][0], x[(index + 1)%len(x)]) <= 10**-12:
                    index = (index+1) % len(x)
                    smallestOrientationOfEachHull[id] = (x[index],index)
                    if (index == startIndex):
                        break
                

                if x[index%len(x)] == GreatConvexHull[-1]:
                    index += 1;
                smallestOrientationOfEachHull[id] = (x[index%len(x)],index%len(x))
            
            Scenes.append(Scene([PointsCollection(randPoints),
                                 PointsCollection([x[0] for x in smallestOrientationOfEachHull],color='Red'),
                                 PointsCollection(copy.deepcopy(GreatConvexHull),color = 'Yellow'),
                                 PointsCollection([GreatConvexHull[-1]],color = 'Black')
                                ],lines))
            i+= 1

        
        if not GreatConvexHull is None:
            break
        iteration += 1

        
            
    miniLines, miniPoints = visualizeConvexHull(GreatConvexHull)
    Scenes.append(Scene([PointsCollection(randPoints),PointsCollection(copy.deepcopy(GreatConvexHull))] ,[miniLines]))

    return Scenes

def visualizeModifiedBinSearch(convexHull, startPoint,eps):
    
    Scenes = []
    
    #initialize left and right point and left orientations
    l = 0
    r = len(convexHull)
    l_before = orientation(startPoint, convexHull[0], convexHull[-1], determiner1, eps)
    l_after = orientation(startPoint, convexHull[0], convexHull[(l+1) % len(convexHull)], determiner1, eps)
    #classical loop from bin search algorithm 
    Scenes.append(Scene([PointsCollection(convexHull + [startPoint]),
                         PointsCollection([convexHull[l]], color = 'yellow'),
                        PointsCollection([convexHull[r-1]], color = 'red')]))
    
    while l < r :
        #calculate middle point and its orientations
        c = int((l+r)/2)
        c_before = orientation(startPoint, convexHull[c], convexHull[(c - 1) % len(convexHull)], determiner1, eps)
        c_after = orientation(startPoint, convexHull[c], convexHull[(c + 1) % len(convexHull)], determiner1, eps)
        c_side = orientation(startPoint, convexHull[l], convexHull[c], determiner1, eps)
        Scenes.append(Scene([PointsCollection(convexHull + [startPoint]),
                         PointsCollection([convexHull[l]], color = 'yellow'),
                        PointsCollection([convexHull[r-1]], color = 'red'),
                        PointsCollection([convexHull[c]], color = 'green')]))
        #point is on the right of its successor and predecessor
        if c_before != 1 and c_after != 1:
            Scenes.append(Scene([PointsCollection(convexHull + [startPoint]),
                         PointsCollection([convexHull[l]], color = 'yellow'),
                        PointsCollection([convexHull[r-1]], color = 'red'),
                        PointsCollection([convexHull[c]], color = 'pink')]))
            return Scenes
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
    Scenes.append(Scene([PointsCollection(convexHull + [startPoint]),
                        PointsCollection([convexHull[l%len(convexHull)]], color = 'pink'),
                        PointsCollection([convexHull[r-1]], color = 'red')]))
            
    return Scenes
