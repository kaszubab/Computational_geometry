import time

import pickle

# simple functions used to write convexHull to file
def convexHullToPickle(hull, fileName):
    f = open(fileName+".pickle", "wb+")
    pickle.dump(hull, f)

def convexHullToFile(hull, fileName):
    f = open(fileName+'.txt',"w+")
    f.write(np.array_str(hull.points))
    f.close()
    
# function used to check running time of an algorithm, also return convex hull and saves it 
def algorithmData(algorithm, pointSets, eps = 1e-12, writeToFile=False ):

    convexHulls = []
    results = []
    for x in pointSets.keys():
        begin = time.time()
        convexHull = algorithm(pointSets[x])
        end = time.time()
        
        
        if (writeToFile):
            xs = pointsSets(x)
            Hull = PointsCollection(convexHull)
            convexHullToFile(Hull, xs)
            convexHullToPickle(Hull, xs)
        
        
        results.append((len(pointSets[x]), end - begin))
        print('Algorithm: %s   Set: %s   time: %f s points on convex hull :  %d' % (algorithm.__name__,x, end - begin, len(convexHull)))
        convexHulls.append(convexHull)
    return results,convexHulls
