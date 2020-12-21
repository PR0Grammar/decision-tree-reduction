import math;

def getProbabilityOfQuestion(ind, freq, givenMap):
    n = sum(freq)
    numOfRows = len(freq)
    freqOfRows = 0

    for i in range(numOfRows):
        matches = True
        for k in givenMap:
            if(ind[k][i] != givenMap[k]):
                matches = False
        if(matches):
            freqOfRows += freq[i]
    
    givenStr = ""
    for k in givenMap:
        givenStr += (k + ": " + str(givenMap[k]) + ", ")
    
    ans = (freqOfRows / n)
    print("P(" + givenStr + ") = " + str(ans))
    return ans

def getInformationMeasure(ind, dep, freq, givenMap):
    infoMeasure = 0

    totalFreqSum = 0
    numOfRows = len(freq)
    types = sorted(list(set(dep)))
    
    # Sample size now with GIVEN
    for i in range(numOfRows):
        valid = True
        for k in givenMap:
            if(givenMap[k] != ind[k][i]):
                valid = False
        if(valid):
            totalFreqSum += freq[i]
    
    givenStr=""
    for k in givenMap:
        givenStr += (k + ": " + str(givenMap[k]) + ", ")
    print("I(" + givenStr + "-> ER) = -1 * (")
    
    # for each type
    for i in range(len(types)):
        type_ = types[i]
        typeFreqSum = 0

        # check indepedent variable values in row match up to given
        for j in range(numOfRows):
            givenRowValuesMatch = True
            for k in givenMap:
                if(givenMap[k] != ind[k][j]):
                    givenRowValuesMatch = False
            # check if the depedent variable in that row matches the current type we're checking
            if(dep[j] != type_):
                givenRowValuesMatch = False

            # if the given row values match, then add that rows frequency
            if(givenRowValuesMatch):
                typeFreqSum += freq[j]
        if(totalFreqSum == 0):
            print(str(0) + " +")
        else:
            freqPercentage = typeFreqSum / totalFreqSum
            if(freqPercentage > 0):
                v = (freqPercentage * math.log(freqPercentage, 2))
                infoMeasure += v
                print(str(v) + " +")
            else:
                print(str(0) + " +")
    infoMeasure = -(infoMeasure)
    print(")")
    print("= " + str(infoMeasure))
    return infoMeasure

def getExpectedValue(ind, dep, freq, given, givenMap, given_i):
    if(given_i >= len(given)):
        # Once a value for each indpedent variable has been chosen
        # caluculate info measure and probability of the indepdent variables
        val = (getInformationMeasure(ind, dep, freq, givenMap) * getProbabilityOfQuestion(ind, freq, givenMap))
        print('\n')
        return val

    expectedVal = 0
    givenChar = given[given_i]
    values = sorted(list(set(ind[givenChar])))

    # Choose a value for for indepdent variable
    for v in values:
        givenMap[givenChar] = v
        expectedVal += getExpectedValue(ind, dep, freq, given, givenMap, given_i + 1)
    
    return expectedVal

def getNextCharacteristic(ind, dep, freq, given):
    bestExpectedVal = float('inf')
    nextChar = ""

    # Take a indepdent variable that is not given
    # Assume its given, and calculate the expected value
    for k in ind:
        if(k in given):
            continue
        given.append(k)
        expectedVal = getExpectedValue(ind, dep, freq, given, {}, 0)
        print("E[I(Q: " + ", ".join(given) + " -> ER] = " + str(expectedVal))
        print("_______________________________________________________________\n")
        given.pop()

        if(expectedVal < bestExpectedVal):
            ("Expected value of " + k + " of value " + str(bestExpectedVal) + " is better than " + nextChar +"\n")
            bestExpectedVal = expectedVal
            nextChar = k
    print("The next characteristic/level in the tree is: ", nextChar)
    print("_______________________________________________________________\n")
    return (nextChar, bestExpectedVal)


def makeDecisionTree(ind, dep, freq, given):
    expected = float('inf')

    while(expected > 0):
        label, expected_next = getNextCharacteristic(ind, dep, freq, given)
        given.append(label)
        expected = expected_next
    
    return given

def printData(ind, dep, freq):
    label, depData = dep
    
    print("__________Decision Tree__________\n")
    print("__Variables__")
    print("Independent Variables(discretized): ")
    for k in ind:
        print(k)
    print('\n')
    print("Dependent Variable(discretized):\n"+label)

    print('\n')
    print("__Table__")
    for k in ind:
        print(k + ": ", ind[k])
    print(label + ": ", depData)
    print("frequency: ", freq, "\n")

def main(ind, dep, freq):
    # print data
    depLabel, depData = dep
    printData(ind, dep, freq)
    decisionTree = makeDecisionTree(ind, depData, freq, [])

    print("The tree should be: " + "-> ".join(decisionTree))

# Data
# NOTE: 
# Each column represents one "entry" of classifcation, so the number of rows in indepdent variables, dependent variable and frequency must match

independent = {
    "x1": [1,2,0,3,4,4,4,3,0,4,4,0],
    "x2": [1,4,1,1,1,3,2,3,0,2,2,5],
    "x3": [1,5,2,3,5,5,5,6,0,4,5,7],
    "x4": [0,4,4,3,1,4,4,3,2,1,1,4],
    "x5": [1,0,1,0,1,1,1,1,1,1,1,1],
    "x6": [1,0,1,0,1,1,1,1,1,1,1,1],
    "x7": [1,0,1,3,4,1,1,0,2,2,2,2],
    "x8": [1,3,1,0,2,1,5,5,5,1,4,3],
    "x9": [1,3,1,0,1,1,1,3,3,3,3,1],
    "x10": [2,2,2,2,4,5,3,3,1,3,3,1],
    "x11": [1,2,3,3,3,3,3,6,5,2,3,4]
}

frequency = [7,2,151,201,65,102,4,33,32,43,31,12]

dependent = ("dependent variable label", [0,0,0,1,1,1,0,3,0,0,0,0])


main(independent, dependent, frequency)