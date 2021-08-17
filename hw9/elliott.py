import os
import matplotlib.pyplot as plt
import collections
import numpy as np

DATA_FILE = "Pew_Survey.csv"
figureCount = 0

def MakePieChart(title, names, values, filename):
    global figureCount
    plt.figure(figureCount)
    figureCount += 1
    plt.pie(values, labels=names)
    plt.title(title)
    plt.savefig(fname=filename)

def ReadData():
    fullPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), DATA_FILE)
    with open(fullPath) as fh:
        fileData = fh.read()
        columnHeaders = fileData.split("\n")[0].split(",")
        columnData = [list(map(lambda x: int(x) if x.isnumeric() else None, data.split(','))) for data in fileData.split("\n")[1:]]
        return [columnHeaders, columnData]

def GenerateAges(headers, data):
    agePosition = headers.index("age")
    labels = ["18-38", "39-58", "59-78", "79-96", ">96", "Don't know", "Refused"]
    group18 = 0
    group39 = 0
    group59 = 0
    group79 = 0
    group97 = 0
    group98 = 0
    group99 = 0

    for datum in data:
        age = datum[agePosition]
        if age == None:
            continue

        if 18 <= age <= 38:
            group18 +=1
        elif 39 <= age <= 58:
            group39 +=1
        elif 59 <= age <= 78:
            group59 +=1
        elif 79 <= age <= 96:
            group79 +=1
        elif age == 97:
            group97 +=1
        elif age == 98:
            group98 +=1
        elif age == 99:
            group99 +=1

    MakePieChart("Basic Age", labels, [group18, group39, group59, group79, group97, group98, group99], "./basicAge")     
    print("---Ages---")
    print(labels)
    print([group18, group39, group59, group79, group97, group98, group99])

def GenerateIncomes(headers, data):
    incomePosition = headers.index("inc")
    labels = ["<10k", "10-20k", "20-30k", "30-40k", "40-50k", "50-75k", "75-100k", "100-150k", ">150k", "Don't know", "Refuse"]
    groups = [0] * len(labels)

    for datum in data:
        income = datum[incomePosition]
        if income == None:
            continue

        if income == 99:
            groups[-1] = groups[-1] + 1
        elif income == 98:
            groups[-2] = groups[-2] + 1
        else:
            groups[income - 1] = groups[income - 1] + 1

    MakePieChart("Basic Income", labels, groups, "./basicIncome")
    print("---Incomes---")
    print(labels)
    print(groups)

def GenerateAgeBasedIncomes(headers, data):
    incomePosition = headers.index("inc")
    agePosition = headers.index("age")

    #Dictionary of form {age: {incomeSum, occurences}}
    ageDict = {}
    for datum in data:
        income = datum[incomePosition]
        age = datum[agePosition]    
        if income > 9 or age > 97:
            continue

        if age not in ageDict.keys():
            ageDict[age] = {"income" : income, "occurences" : 1}
        else:
            ageDict[age]["income"] = ageDict[age]["income"] + income
            ageDict[age]["occurences"] = ageDict[age]["occurences"] + 1
    
    orderedAgeDict = collections.OrderedDict(sorted(ageDict.items()))
    ages = [k for k in orderedAgeDict]
    averageIncome = [orderedAgeDict[k]["income"] / orderedAgeDict[k]["occurences"] for k in orderedAgeDict]
    
    global figureCount
    plt.figure(figureCount)
    figureCount += 1
    plt.plot(ages, averageIncome)
    plt.title("Average Income vs Age")
    plt.xlabel("Age")
    plt.ylabel("Income")
    plt.savefig("./ageAndIncome")
    print("---Income vs age---")
    print(ages)
    print(averageIncome)

def GeneratePolitical(headers, data):
    politicalPosition = headers.index("party")
    labels = ["Republican", "Democrat", "Independent", "No preference", "Other party", "Don't know", "Refused"]
    groups = [0] * len(labels)

    for datum in data:
        party = datum[politicalPosition]
        if party == None:
            continue
        
        if party == 9:
            groups[-1] = groups[-1] + 1
        elif party == 8:
            groups[-2] = groups[-2] + 1
        else:
            groups[party - 1] = groups[party - 1] + 1

    MakePieChart("Political Party", labels, groups, "./politicalParty")
    print("---Political party---")
    print(labels)
    print(groups)

def GeneratePoliticalLean(headers, data):
    politicalPosition = headers.index("partyln")
    labels = ["Republican", "Democrat", "Don't know", "Refused"]
    groups = [0] * len(labels)

    for datum in data:
        party = datum[politicalPosition]
        if party == None:
            continue
        
        if party == 9:
            groups[-1] = groups[-1] + 1
        elif party == 8:
            groups[-2] = groups[-2] + 1
        else:
            groups[party - 1] = groups[party - 1] + 1

    MakePieChart("Political Party Leaning", labels, groups, "./politicalPartyLean")
    print("---Political party lean---")
    print(labels)
    print(groups)
# Analyzes which questions weren't answered the most
def GenerateNoResponses(headers, data):
    noneDict = {}
    for header in headers[1:]:
        noneDict[header] = 0

    for datum in data:
        pos = 0
        for item in datum:
            if item == None:
                noneDict[headers[pos]] = noneDict[headers[pos]] + 1
            pos += 1
    question = []
    occurences = []
    for k,v in noneDict.items():
        if v != 0:
            question.append(k)
            occurences.append(v)

    global figureCount
    plt.figure(figureCount)
    figureCount += 1
    plt.bar(question, occurences)
    plt.ylabel("Occurences")
    plt.xlabel("Survey question")
    plt.title("Most unanswered questions")
    plt.savefig("./noAnswer")
    print("---No response---")
    print(question)
    print(occurences)

def GenerateMostRefused(headers, data):
    refusedDict = {}
    for header in headers[1:]:
        refusedDict[header] = 0

    for datum in data:
        pos = 1
        for item in datum[1:]:
            if pos == 27:
                if item == 99:
                    refusedDict[headers[pos]] = refusedDict[headers[pos]] + 1
                continue    
            if item == 99 or item == 9:
                refusedDict[headers[pos]] = refusedDict[headers[pos]] + 1
            pos += 1
    question = []
    occurences = []
    for k,v in refusedDict.items():
        if v != 0:
            question.append(k)
            occurences.append(v)

    global figureCount
    plt.figure(figureCount)
    figureCount += 1
    plt.bar(question, occurences)
    plt.ylabel("Occurences")
    plt.xlabel("Survey question")
    plt.title("Refused questions")
    plt.savefig("./refusedAnswer")
    print("---Refused response---")
    print(question)
    print(occurences)

def GenerateSex(headers, data):
    sexPosition = headers.index("sex")
    labels = ["Male", "Female"]
    groups = [0] * len(labels)

    for datum in data:
        sex = datum[sexPosition]
        groups[sex - 1] = groups[sex - 1] + 1

    MakePieChart("Sex", labels, groups, "./basicSex")
    print("---Sex---")
    print(labels)
    print(groups)

def GenerateRegion(headers, data):
    position = headers.index("cregion")
    labels = ["Northeast", "Midwest", "South", "West"]
    groups = [0] * len(labels)

    for datum in data:
        value = datum[position]
        groups[value - 1] = groups[value - 1] + 1

    MakePieChart("Region", labels, groups, "./region")
    print("---Region---")
    print(labels)
    print(groups)

def GenerateDeviceUsage(headers, data):
    position = headers.index("device1b")
    position2 = headers.index("device1c")
    position3 = headers.index("device1d")
    labels = ["Tablet", "Desktop/Laptop", "Game Console"]
    groups = [0] * len(labels)

    for datum in data:
        count = 0
        for pos in [position, position2, position3]:
            if datum[pos] == 1:
                groups[count] += 1
            count += 1

    MakePieChart("Devices", labels, groups, "./devices")
    print("---Devices---")
    print(labels)
    print(groups)

def GetResponsesByAge(headers, data, lb, ub):
    position = headers.index("age")
    group = []
    for datum in data:
        if lb <= datum[position] <= ub:
            group.append(datum)
    return group

def GenerateSocialUsageByAgeGroup(headers, data):
    ageGroups = []
    ageGroups.append(GetResponsesByAge(headers, data, 18, 28))
    ageGroups.append(GetResponsesByAge(headers, data, 29, 38))
    ageGroups.append(GetResponsesByAge(headers, data, 39, 48))
    ageGroups.append(GetResponsesByAge(headers, data, 49, 58))
    ageGroups.append(GetResponsesByAge(headers, data, 59, 68))
    ageGroups.append(GetResponsesByAge(headers, data, 69, 78))
    ageGroups.append(GetResponsesByAge(headers, data, 79, 88))
    ageGroups.append(GetResponsesByAge(headers, data, 89, 96))
    
    positions = [headers.index("sns2a"), headers.index("sns2b"), headers.index("sns2c"), headers.index("sns2d"), headers.index("sns2e")]
    
    #Represents list of platforms and the number of occurences 
    smByAgeGroup = []
    for i in range(len(positions)):
        smByAgeGroup.append([0] * len(ageGroups))
    ageGroup = 0
    for group in ageGroups:
        for response in group:
            platform = 0
            for position in positions:
                if response[position] == 1 or response[position] == 2 or response[position] == 3:
                    smByAgeGroup[platform][ageGroup] += 1
                platform += 1
        ageGroup += 1

    labels = ["Twitter", "Instagram", "Facebook", "Snapchat", "Youtube"]
    
    global figureCount
    plt.figure(figureCount)
    figureCount += 1

    x = np.arange(len(labels))
    width = .35
    #fig, ax = plt.subplots()
    #rects1 = ax.bar(x - width/2, smByAgeGroup[0], width, label="18-28")
    
    plt.bar(x-.2, smByAgeGroup[0], width)
    plt.set_ylabel("Occurencens")
    plt.set_title("Platform use by age")
    plt.set_xticks(x)
    plt.set_xtickslabels(labels)
    plt.legend()

    plt.savefig(fname="./platformByAge")

def GenerateSocialMediaUsage(headers, data):
    positions = [headers.index("web1a"),headers.index("web1b"),headers.index("web1c"),
        headers.index("web1d"),headers.index("web1e"),headers.index("web1f"),
        headers.index("web1g"),headers.index("web1h"),headers.index("web1i")]
    labels = ["Twitter", "Instagram", "Facebook", "Snapchat", "YouTube", "WhatsApp", "Pinterest", "LinkedIn", "Reddit"]
    groups = [0] * len(labels)

    for datum in data:
        count = 0
        for pos in positions:
            if datum[pos] == 1:
                groups[count] += 1
            count += 1

    MakePieChart("Social Media usage", labels, groups, "./smUsage")
    print("---Social Media usage---")
    print(labels)
    print(groups)

def GenerateBasicDemographics(headers, data):
    GenerateAges(headers, data)
    GenerateIncomes(headers, data)
    GenerateAgeBasedIncomes(headers, data)
    GeneratePolitical(headers, data)
    GeneratePoliticalLean(headers, data)
    GenerateNoResponses(headers, data)
    GenerateMostRefused(headers, data)
    GenerateSex(headers, data)
    GenerateRegion(headers, data)
    GenerateDeviceUsage(headers, data)
    GenerateSocialMediaUsage(headers, data)
    GenerateSocialUsageByAgeGroup(headers, data)
    #GenerateSocialUsageByDevice(headers, data)

# Main
if __name__ == "__main__":
    headers, data = ReadData()
    GenerateBasicDemographics(headers, data)
    #GenerateMostUnansweredQuestions