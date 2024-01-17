# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification

def isFloat(y):
    try:
        float(y)
        return True
    except:
        return False


def sumvalues(values):
    """Calculates the sum of a list/array"""
    listSum = 0
    A = [float(x) for x in values if isFloat(x)]
    for item in A:
        listSum += item
    return listSum


def maxvalue(values):
    """Calculates the largest value in a list/array"""
    templistMax = -1
    A = [float(x) for x in values if isFloat(x)]
    for item in A:
        if item > templistMax:
            templistMax = (item)
    if templistMax == -1:
        listMax = "No Data"
    else:
        listMax = str(templistMax)
    return listMax


def minvalue(values):
    """Calculates the smallest value in a list/array"""
    A = [float(x) for x in values if isFloat(x)]
    try:
        listMin = A[0]
        for item in A:
            if item < listMin:
                listMin = item
    except:
        listMin = "No data"
    return listMin


def meanvalue(values):
    """Calculates the mean value of a list/array"""
    try:
        A = [float(x) for x in values if isFloat(x)]
        listMean = str(sumvalues(A) / len(A))
    except:
        listMean = "No data"
    return listMean


def countvalue(values, x):
    """Finds the total amount of item x in a list/array"""
    totalX = 0
    for item in values:
        if item == x:
            totalX += 1
    return totalX
