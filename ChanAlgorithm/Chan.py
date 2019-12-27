import part2.graham

from part2.helperFunctions import *
#Chan algorithm to compute convex Hull

def Chan(pointsInput, eps = 10**-12):
    
    randPoints = pointsInput
    iteration = 1

    while True:
        
        m = min(2**(2**iteration),len(pointsInput))
        
        convexHulls = []
        
        if m == len(pointsInput):
            cHull =  part2.graham.graham_scan(randPoints)
            return cHull
            
        

        for x in range(int(len(randPoints)/m)+1):

            miniConvexHull = part2.graham.graham_scan(randPoints[m*x:(x+1)*m])

            convexHulls.append(miniConvexHull)

        if convexHulls[-1] == []:
            del(convexHulls[-1])

        startPoint,_ = bottomLeft(randPoints)

        GreatConvexHull = []
        GreatConvexHull.append(startPoint)

        i = 0
        smallestOrientationOfEachHull = []
        
        for x in convexHulls:
            index = modifiedBinSearch(x,GreatConvexHull[-1], eps)%len(x)
            if x[index] == GreatConvexHull[-1]:
                index += 1;
            smallestOrientationOfEachHull.append((x[index%len(x)],index%len(x)))
        
        for id,x in enumerate(convexHulls):
                
            index = smallestOrientationOfEachHull[id][1]
            startIndex = index
                
            while determiner1(GreatConvexHull[-1], smallestOrientationOfEachHull[id][0], x[(index + 1)%len(x)]) <= eps:
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

            nextPoint = smallestOrientationOfEachHull[0][0]

            for x in smallestOrientationOfEachHull:
                detResult = determiner1(point1, nextPoint, x[0])
                if detResult <= eps:
                    if detResult <= eps or (detResult > eps and squaredDist(point1, x[0]) > squaredDist(point1,nextPoint)):  
                        nextPoint = x[0]

            if nextPoint == GreatConvexHull[0]:
                break
            GreatConvexHull.append(nextPoint)
            
            if len (GreatConvexHull) > 2 and determiner1(GreatConvexHull[-3],GreatConvexHull[-2],GreatConvexHull[-1]) <= eps:
                hullpoint1 = GreatConvexHull.pop()
                GreatConvexHull.pop()
                GreatConvexHull.append(hullpoint1)
            
            for id,x in enumerate(convexHulls):
                
                index = smallestOrientationOfEachHull[id][1]
                startIndex = index
                
                while determiner1(GreatConvexHull[-1], smallestOrientationOfEachHull[id][0], x[(index + 1)%len(x)]) <= eps:
                    index = (index+1) % len(x)
                    smallestOrientationOfEachHull[id] = (x[index],index)
                    if (index == startIndex):
                        break
                

                if x[index%len(x)] == GreatConvexHull[-1]:
                    index += 1;
                smallestOrientationOfEachHull[id] = (x[index%len(x)],index%len(x))

            i+= 1

        
        if not GreatConvexHull is None:
            break
        iteration += 1


    return GreatConvexHull


