import os

class Node:
    def __init__(self) -> None:
        pass

# Gets filename to pull data from
def GetUserInput():

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
        return nodes


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
    #Counter of triad types mapped as follows: TTT = 3, TTD = 1, TDD = -1, DDD = -3
    edgeCombos = {3 : 0, 1 : 0, -1 : 0, -3 : 0}
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
                    if not newSet in uniqueTriads:
                        edgeType = GetRelationBetweenNodes(allRelations, node, firstOrderNode) + \
                            GetRelationBetweenNodes(allRelations, node, secondOrderNode) + \
                            GetRelationBetweenNodes(allRelations, firstOrderNode, secondOrderNode)
                        edgeCombos[edgeType] = edgeCombos[edgeType] + 1
                    uniqueTriads.add(newSet)
                    
    
    #for triad in uniqueTriads:
    #    print(triad)

    print("Total # triads: " + str(len(uniqueTriads)))
    print(edgeCombos)
    return uniqueTriads
        
def GetRelationData(nodes):
    numEdges = len(nodes)
    numPositive = 0

    for node in nodes:
        if node.split(',')[2] == '1':
            numPositive += 1
    print("Num edges: " + str(numEdges) + ". Num positive edges: " + str(numPositive))
    return [numEdges, numPositive]

# Main
if __name__ == "__main__":
    # Get user input
    nodes = GetUserInput()

    numEdges, numPositive = GetRelationData(nodes)
    allRelations = CreateTables(nodes)
    allTriads = FindTriads(allRelations)
