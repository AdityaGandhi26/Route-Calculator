### Code tested with Pyzo running the default Python shell ###
### To load script for execution - in Pyzo - click Run and then Run File as Script ###
### Only need to execute the runCalc() function to execute all tests and get results ###

# Assign values to road junctions for use with Cost/Distance Matrix
values = dict();
values['A'] = 0;
values['B'] = 1;
values['C'] = 2;
values['D'] = 3;
values['E'] = 4;

def runCalc():
    
    # The dataset
    data = data = [('A','B',5),('B','C',4),('C','D',7),('D','C',8),('D','E',6),('A','D',5),('C','E',2),('E','B',3),('A','E',7)];
    
    # Generate the graph and cost matrix
    (graph,costMatrix) = generateGraphAndCostMatrix(data);
    
    # Display Graph and Cost Matrix
    print("Graph : ")
    print(graph)
    
    print("\n")
    
    print("Cost Matrix : ")
    print(costMatrix)
    
    print("\n")
    
    # Test Cases for Finding Specific Path Cost
    testPaths = [['A','B','C'],['A','D'],['A','D','C'],['A','E','B','C','D'],['A','E','D']]
    
    for pathIndex in range(0, len(testPaths)):
        path = testPaths[pathIndex]
        cost = getCostSpecificPath(path,costMatrix)
        
        print("Path : ", path)
        
        if cost == None:
            print("NO SUCH ROUTE")
        else:
            print("Cost : ", cost)
            
    print("\n")
        
    # Test Cases for Finding All Routes with Max Path Length
    paths = allRoutes(graph, 'C', 'C', 3)
    print("All Paths : ")
    print(paths)
    print(len(paths))
    
    print("\n")
    
    # Test Case for Finding All Routes with exact number of junctions
    paths = allRoutesExactLength(graph, 'A', 'C', 4)
    print("All Paths : ")
    print(paths)
    print(len(paths))
    
    print("\n")
    
    # Test Case for Finding Shortest Route (in terms of distance to travel)
    
    (path, cost) = getShortestRoute(graph, costMatrix, 'A', 'C')
    
    print("Shortest Route from 'A' to 'C' : ", path)
    print("Cost of Path : ", cost)
    
    print("\n")
    
    (path, cost) = getShortestRoute(graph, costMatrix, 'B', 'B')
    
    print("Shortest Route from 'B' to 'B' : ", path)
    print("Cost of Path : ", cost)
     
    print("\n")
    
    # Test Case for Finding All Routes with Distance less than certain amount
    paths = allRoutesMaxDistance(graph, costMatrix, 0, 'C', 'C', 30)
    print("Distance Less than 30 from 'C' to 'C' : ")
    print(paths)
    print("Number of Paths : ", len(paths))
    
    
    
def generateGraphAndCostMatrix(data):
    # Create lists to hold links between letters/road junctions
    a = [];
    b = [];
    c = [];
    d = [];
    e = [];
    
    # Hold costs/distances in a matrix - -1 means no direct route, 0 means itself
    costMatrix = [[0,-1,-1,-1,-1],[-1,0,-1,-1,-1],[-1,-1,0,-1,-1],[-1,-1,-1,0,-1],[-1,-1,-1,-1,0]];
    
    # Add connection to relevant list
    for i in range(0, len(data)):
        if data[i][0] == 'A':
            a.append(data[i][1]);
        
        if data[i][0] == 'B':
            b.append(data[i][1]);
        
        if data[i][0] == 'C':
            c.append(data[i][1]);
        
        if data[i][0] == 'D':
            d.append(data[i][1]);
        
        if data[i][0] == 'E':
            e.append(data[i][1]);

        # Update Cost Matrix
        costMatrix[values[data[i][0]]][values[data[i][1]]] = data[i][2];
        
    # Generate Graph
    graph = {'A': a,
             'B': b,
             'C': c,
             'D': d,
             'E': e}
             
    return (graph,costMatrix)
    
# Recursive function to get path from one node to another
def getPath(graph, start, end, path=[]):
    path = path + [start]
    
    if start == end:
        return path
    
    if start not in graph:
        return None
        
    for node in graph[start]:
        if node not in path:
            newpath = getPath(graph,node, end, path)
            if newpath: return newpath
    return None
    
# Recursive function to get all distinct routes from one node to another 
def allRoutesNoMaxLength(graph, start, end, path=[]):
        path = path + [start]
        
        if start == end:
            return [path]
            
        if start not in graph:
            return []
            
        paths = []
        
        for node in graph[start]:
            if node not in path:
                
                newpaths = allRoutesNoMaxLength(graph, node, end, path)
                
                for newpath in newpaths:
                    paths.append(newpath)
                    
        return paths
        
# Recursive function to get all routes from one node to another with less than a certain number of connections
def allRoutes(graph, start, end, maxPathLength, path=[]):
    path = path + [start]
    
    if start == end and len(path) != 1:
        return [path]
    
    if start not in graph:
        return []
        
    if maxPathLength == 0 and start == end:
        return path
        
    if maxPathLength == 0:
        return []
        
    paths = []
    
    for node in graph[start]:
        newpaths = allRoutes(graph, node, end, maxPathLength-1, path)
            
        for newpath in newpaths:
            paths.append(newpath)
                
    return paths

# Recursive function to get all routes from one node to another with an exact number of connections
def allRoutesExactLength(graph, start, end, pathLength, path=[]):
    path = path + [start]
    
    if start == end and len(path) == pathLength+1:
        return [path]
    
    if start not in graph:
        return []
        
    if pathLength == 0:
        return []
        
    if len(path) > pathLength:
        return []
        
    paths = []
    
    for node in graph[start]:
        newpaths = allRoutesExactLength(graph, node, end, pathLength, path)
            
        for newpath in newpaths:
            paths.append(newpath)
                
    return paths
    
# Function to get the cost/distance for a specific path
def getCostSpecificPath(path, costMatrix):
    cost = 0
    
    for i in range(0, (len(path)-1)):
        start = path[i]
        end = path[i+1]
        
        costOfSection = costMatrix[values[start]][values[end]]
        
        if costOfSection == -1:
            return None
            
        cost = cost + costOfSection
    
    
    return cost

# Function to get the shortest route from one node to another
def getShortestRoute(graph, costMatrix, start, end):
    paths = allRoutes(graph, start, end, 5)
    
    cheapestPathIndex = 0;
    cost = -1;
    
    for i in range(0, len(paths)):
        costOfPath = getCostSpecificPath(paths[i], costMatrix)
        
        if cost == -1:
            cost = costOfPath
            cheapestPathIndex = i
        elif costOfPath < cost:
            cost = costOfPath
            cheapestPathIndex = i
    
    return (paths[cheapestPathIndex], cost)
        
# Recursive function to get all routes within a specific maximum distance/cost
def allRoutesMaxDistance(graph, costMatrix, cost, start, end, maxDistance, path=[]):
    path = path + [start]
    paths = []
    
    if maxDistance <= 0:
        return []
    
    if start == end and len(path) != 1:
        paths.append(path)
    
    if start not in graph:
        return []
        
    for node in graph[start]:
        costToNode = costMatrix[values[path[len(path)-1]]][values[node]]
        distance = maxDistance - costToNode
        
        newpaths = allRoutesMaxDistance(graph,costMatrix, cost, node, end, distance, path)
            
        for newpath in newpaths:
            paths.append(newpath)
                
    return paths
        
        
        