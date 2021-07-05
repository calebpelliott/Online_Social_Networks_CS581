import os
from datetime import datetime

# Gets filename to pull data from
def GetUserInput():
    dataFp = ""

    # Loop until valid file path is entered
    while(True):
        dataFp = input("Please input filename: ")
        fullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), dataFp)

        if os.path.exists(fullPath):
            break
        print("Error: "+ fullPath + " not found")
    
    with open(fullPath, 'r') as f:
        data = f.read()
        nodes = data.split("\n")
        # Removes any empty lines
        nodes[:] = [node for node in nodes if node != '']
        return [nodes, dataFp]


def CreateTables(nodes):
    allRelationsTable = {}

    for node in nodes:
        nodeData = node.split(",")
        reviewer = int(nodeData[0])
        reviewee = int(nodeData[1])
        trust    = int(nodeData[2])

        allRelationsTable.setdefault(reviewer, ({}, {}))[0][reviewee] = trust
        allRelationsTable.setdefault(reviewee, ({}, {}))[1][reviewer] = trust    

    return allRelationsTable

def GetRelatedNodes(allRelations, node):
    return set(list(allRelations[node][0].keys()) + list(allRelations[node][1].keys()))


def GetRelationBetweenNodes(allRelations, node1, node2):
    #Check if node2 is pointed to by node1
    if node2 in allRelations[node1][0].keys():
        return allRelations[node1][0][node2]
    #Check if node2 points to node1
    elif node2 in allRelations[node1][1].keys():
        return allRelations[node1][1][node2]
    else:
        raise ValueError("No relation between gives nodes")

def FindTriads(allRelations):
    uniqueTriads = set()
    allNodes = allRelations.keys()
    counter = 0
    for node in allNodes:
        counter += 1
        if counter % 100 == 0:
            print(str(float(counter/len(allNodes)) * 100) + "% complete")
        # first order nodes are all nodes that point to node or are pointed at by node 
        firstOrderNodes = GetRelatedNodes(allRelations, node)

        for firstOrderNode in firstOrderNodes:
            secondOrderNodes = GetRelatedNodes(allRelations, firstOrderNode)

            for secondOrderNode in secondOrderNodes:
                if(node in GetRelatedNodes(allRelations, secondOrderNode)):
                    newSet = frozenset({node, firstOrderNode, secondOrderNode})
                    uniqueTriads.add(newSet)

    return uniqueTriads

def GetTriadTypes(allRelations, triads):
    #Counter of triad types mapped as follows: TTT = 3, TTD = 1, TDD = -1, DDD = -3
    edgeCombos = {3 : 0, 1 : 0, -1 : 0, -3 : 0}

    for triadSet in triads:
        triad = list(triadSet)
        edgeType = GetRelationBetweenNodes(allRelations, triad[0], triad[1]) + \
            GetRelationBetweenNodes(allRelations, triad[0], triad[2]) + \
            GetRelationBetweenNodes(allRelations, triad[1], triad[2])
        edgeCombos[edgeType] = edgeCombos[edgeType] + 1

    edgeTypes = {"TTT" : edgeCombos[3], "TTD" : edgeCombos[1], "TDD" : edgeCombos[-1], "DDD" : edgeCombos[-3]}
    return edgeTypes

def GetRelationData(nodes):
    numEdges = len(nodes)
    numPositive = 0

    for node in nodes:
        if node.split(',')[2] == '1':
            numPositive += 1
    return [numEdges, numPositive]

def PrintStats(filename, start, end, numEdges, numPositive, allTriads, triadTypes, expectedDist, actualDist):
    print("Data from file: " + filename)
    print("Number of triangles: " + str(len(allTriads)))
    print("Trust edges: " + str(numPositive) + ". Probability: " + str(float(numPositive/numEdges) * 100) + "%")
    print("Distrust edges: " + str(numEdges - numPositive) + ". Probability: " + str(float((numEdges - numPositive)/numEdges) * 100) + "%")
    print("Edges used: " + str(numEdges))
    print("Triangle Types:")
    for type, count in triadTypes.items():
        print(type + ": " + str(count))
    print("Expected Distribution:")
    for type, count in expectedDist.items():
        print(type + ": " + count)
    print("Actual Distribution:")
    for type, count in actualDist.items():
        print(type + ": " + count)
    print("Start Time = " + start)
    print("End Time = " + end)

def CalculateDistribution(numEdges, numPositive, numTriads, actualTypes):
    percentPositive = float(numPositive / numEdges)
    percentNegative = float(1 - percentPositive)

    expectedDist = {}
    actualDist = {}

    tttExpected = " percent: " + str(float(pow(percentPositive, 3)) * 100) + "%. number: " + str(float(pow(percentPositive, 3) * numTriads))
    ttdExpected = " percent: " + str(float(pow(percentPositive, 2) * percentNegative) * 100 * 3) + "%. number: " + str(float(pow(percentPositive, 2) * percentNegative * numTriads))
    tddExpected = " percent: " + str(float(pow(percentNegative, 2) * percentPositive) * 100 * 3) + "%. number: " + str(float(pow(percentNegative, 2) * percentPositive * numTriads))
    dddExpected = " percent: " + str(float(pow(percentNegative, 3)) * 100) + "%. number: " + str(float(pow(percentNegative, 3) * numTriads))

    expectedDist["TTT"] = tttExpected
    expectedDist["TTD"] = ttdExpected
    expectedDist["TDD"] = tddExpected
    expectedDist["DDD"] = dddExpected

    for type, count in actualTypes.items():
        expected = " percent: " + str(float(count/numTriads) * 100) + "%. number: " + str(count)
        actualDist[type] = expected

    return [expectedDist, actualDist]
# Main
if __name__ == "__main__":
    # Get user input
    nodes, filename = GetUserInput()

    #Start timer after user input
    start = datetime.now()
    start = start.strftime("%H:%M:%S")

    numEdges, numPositive = GetRelationData(nodes)
    allRelations = CreateTables(nodes)
    allTriads = FindTriads(allRelations)
    triadTypes = GetTriadTypes(allRelations, allTriads)
    expectedDist, actualDist = CalculateDistribution(numEdges, numPositive, len(allTriads), triadTypes)

    end = datetime.now()
    end = end.strftime("%H:%M:%S")

    PrintStats(filename, start, end, numEdges, numPositive, allTriads, triadTypes, expectedDist, actualDist)
