import copy
import math
from math import sqrt


def fdct(listOfBlocks):
    newlistOfBlocks = []
    for block in listOfBlocks:
        newblock = [[0 for i in range(8)] for j in range(8)]
        if block.blockType != "Y":
            mymatrix = reverseSubsampling(block.blockMatrix)
        else:
            mymatrix = block.blockMatrix
        currentMatrix = substract128(mymatrix)
        u = 0
        v = 0
        while True:
            newblock[u][v] = fdctFormula(currentMatrix, u, v)
            v = v+1
            if v == 8:
                u = u+1
                v = 0
            if u == 8:
                block.blockMatrix = copy.deepcopy(newblock)
                newlistOfBlocks.append(block)
                break
    return newlistOfBlocks


def reverseSubsampling(matrix):
    resultMatrix = [[0 for i in range(8)] for j in range(8)]
    x = y = i = j = 0
    while True:
        resultMatrix[x][y] = matrix[i][j]
        resultMatrix[x+1][y] = matrix[i][j]
        resultMatrix[x][y+1] = matrix[i][j]
        resultMatrix[x+1][y+1] = matrix[i][j]
        j = j+1
        y = y+2
        if j == 4:
            i = i+1
            j = 0
            x = x+2
            y = 0
        if i == 4:
            return resultMatrix


def substract128(matrix):
    resultMatrix = [[0 for i in range(8)] for j in range(8)]
    for i in range(8):
        for j in range(8):
            resultMatrix[i][j] = matrix[i][j]-128
    return resultMatrix


def fdctFormula(matrix, u, v):
    sum = 0
    for x in range(8):
        for y in range(8):
            sum += matrix[x][y]*math.cos(((2*x+1)*u*math.pi)/16) * \
                math.cos(((2*y+1)*v*math.pi)/16)
    if u == 0:
        uval = 1/sqrt(2)
    else:
        uval = 1
    if v == 0:
        vval = 1/sqrt(2)
    else:
        vval = 1
    return 0.25*uval*vval*sum


def quantizate(listOfBlocks):
    resultMatrix = [[0 for i in range(8)] for j in range(8)]
    resultList = []
    Q = [[6, 4, 4, 6, 10, 16, 20, 24],
         [5, 5, 6, 8, 10, 23, 24, 22],
         [6, 5, 6, 10, 16, 23, 28, 22],
         [6, 7, 9, 12, 20, 35, 32, 25],
         [7, 9, 15, 22, 27, 44, 41, 31],
         [10, 14, 22, 26, 32, 42, 45, 37],
         [20, 26, 31, 35, 41, 48, 48, 40],
         [29, 37, 38, 39, 45, 40, 41, 40]]
    for block in listOfBlocks:
        for i in range(8):
            for j in range(8):
                resultMatrix[i][j] = int(block.blockMatrix[i][j]/Q[i][j])
        block.blockMatrix = copy.deepcopy(resultMatrix)
        resultList.append(block)
    return resultList


def dequantizate(listOfBlocks):
    resultMatrix = [[0 for i in range(8)] for j in range(8)]
    resultList = []
    Q = [[6, 4, 4, 6, 10, 16, 20, 24],
         [5, 5, 6, 8, 10, 23, 24, 22],
         [6, 5, 6, 10, 16, 23, 28, 22],
         [6, 7, 9, 12, 20, 35, 32, 25],
         [7, 9, 15, 22, 27, 44, 41, 31],
         [10, 14, 22, 26, 32, 42, 45, 37],
         [20, 26, 31, 35, 41, 48, 48, 40],
         [29, 37, 38, 39, 45, 40, 41, 40]]
    for block in listOfBlocks:
        for i in range(8):
            for j in range(8):
                resultMatrix[i][j] = block.blockMatrix[i][j]*Q[i][j]
        block.blockMatrix = copy.deepcopy(resultMatrix)
        resultList.append(block)
    return resultList


def idct(listOfBlocks):
    newlistOfBlocks = []
    for block in listOfBlocks:
        newblock = [[0 for i in range(8)] for j in range(8)]
        u = 0
        v = 0
        while True:
            newblock[u][v] = idctFormula(block.blockMatrix, u, v)+128
            v = v+1
            if v == 8:
                u = u+1
                v = 0
            if u == 8:
                block.blockMatrix = copy.deepcopy(newblock)
                newlistOfBlocks.append(block)
                break
    return newlistOfBlocks


def idctFormula(matrix, u, v):
    sum = 0
    for x in range(8):
        for y in range(8):
            if x == 0:
                xval = 1/sqrt(2)
            else:
                xval = 1
            if y == 0:
                yval = 1/sqrt(2)
            else:
                yval = 1
            sum += xval*yval * \
                matrix[x][y]*math.cos(((2*u+1)*x*math.pi)/16) * \
                math.cos(((2*v+1)*y*math.pi)/16)

    return 0.25*sum
