import copy
import struct
from PIL import Image
YMatrix = [[0 for i in range(800)] for j in range(600)]
UMatrix = [[0 for i in range(800)] for j in range(600)]
VMatrix = [[0 for i in range(800)] for j in range(600)]


class Block:
    blockMatrix = [[0 for i in range(4)] for j in range(4)]
    blockType = ""
    blockX = 0
    blockY = 0

    def __str__(self):
        return printBigMatrix(self.blockMatrix)+"type="+str(self.blockType)+" x="+str(self.blockX)+" y="+str(self.blockY)

    def __init__(self, matrix, type, x, y):
        self.blockType = type
        self.blockX = x
        self.blockY = y
        if(type == "Y"):
            self.blockMatrix = [[0 for i in range(8)] for j in range(8)]
            self.blockMatrix = copy.deepcopy(matrix)

        else:
            i = 0
            j = 0
            i4X4 = 0
            j4X4 = 0
            newblockMatrix = [[0 for i in range(4)]
                              for j in range(4)]  # for deepcopy

            while True:
                val1 = matrix[i][j]
                val2 = matrix[i+1][j]
                val3 = matrix[i][j+1]
                val4 = matrix[i+1][j+1]
                finalValue = (val1+val2+val3+val4)/4
                newblockMatrix[i4X4][j4X4] = copy.deepcopy(finalValue)

                j4X4 = j4X4+1  # advance on 4x4 matrix
                if j4X4 == 4:
                    i4X4 = i4X4+1
                    j4X4 = 0

                j = j+2  # advance on the U/V big block
                if j == 8:
                    i = i+2
                    j = 0
                if i == 8:  # stop all
                    self.blockMatrix = copy.deepcopy(newblockMatrix)
                    break


def devideIntoMatrix(matrix, type):
    listOfBlocks = []
    littleMatrix = [[0 for i in range(8)] for j in range(8)]
    i = 0
    j = 0
    x = 0
    z = 0
    while True:
        #print(" x= "+str(i)+" z= "+str(j))
        littleMatrix[i][j] = matrix[x][z]

        j = j+1
        z = z+1

        if j == 8:
            i = i+1
            j = 0
            x = x+1
            z = z-8
        if i == 8:
            block = Block(littleMatrix, type, x-8, z)
            listOfBlocks.append(block)
            i = 0
            x = x-8
            z = z+8

        if z == 800:
            x = x+8
            z = 0
        if x == 600:
            return listOfBlocks


def printBigMatrix(matrix):
    string = ""
    for i in range(len(matrix)):
        string += str(matrix[i][:])+"\n"

    return string


def readAll():
    file = open("nt-P3.ppm", "r")
    file.readline()
    file.readline()
    values = file.readline().split()
    file.readline()
    x = values[0]
    y = values[1]

    i = 0
    j = 0
    while True:
        R = file.readline()
        G = file.readline()
        B = file.readline()

        if R == '':
            break
        Y = 0.299*int(R)+0.587*int(G)+0.114*int(B)
        U = 128-0.1687*int(R)-0.3312*int(G)+0.5*int(B)
        V = 128+0.5*int(R)-0.4186*int(G)-0.0813*int(B)
        YMatrix[i][j] = Y
        UMatrix[i][j] = U
        VMatrix[i][j] = V
        j = j+1
        if j == 800:
            i = i+1
            j = 0


def encode():
    readAll()
    Ylist = devideIntoMatrix(YMatrix, "Y")

    Ulist = devideIntoMatrix(UMatrix, "U")

    Vlist = devideIntoMatrix(VMatrix, "V")

    return Ylist, Ulist, Vlist


def recreateBigMatrix(list):
    if list[0].blockType == "Y":
        YMatrix2 = [[0 for i in range(800)] for j in range(600)]
        i4X4 = 0
        j4X4 = 0
        for block in list:
            x8X8 = block.blockX
            y8X8 = block.blockY
            minimatrix = block.blockMatrix
            i4X4 = 0
            j4X4 = 0
            while True:
                YMatrix2[x8X8][y8X8] = minimatrix[i4X4][j4X4]
                j4X4 = j4X4+1
                y8X8 = y8X8+1
                if j4X4 == 8:
                    i4X4 = i4X4+1
                    j4X4 = 0
                    x8X8 = x8X8+1
                    y8X8 = block.blockY
                if i4X4 == 8:
                    break
        return YMatrix2
    else:
        UorVMatrix = [[0 for i4X4 in range(800)] for j4X4 in range(600)]
        i4X4 = 0
        j4X4 = 0
        for block in list:
            x8X8 = block.blockX
            y8X8 = block.blockY
            minimatrix = block.blockMatrix
            i4X4 = 0
            j4X4 = 0
            while True:
                UorVMatrix[x8X8][y8X8] = minimatrix[i4X4][j4X4]
                UorVMatrix[x8X8+1][y8X8] = minimatrix[i4X4][j4X4]
                UorVMatrix[x8X8][y8X8+1] = minimatrix[i4X4][j4X4]
                UorVMatrix[x8X8+1][y8X8+1] = minimatrix[i4X4][j4X4]
                j4X4 = j4X4+1
                y8X8 = y8X8+2
                if j4X4 == 4:
                    i4X4 = i4X4+1
                    j4X4 = 0
                    x8X8 = x8X8+2
                    y8X8 = block.blockY
                if i4X4 == 4:
                    break
        return UorVMatrix


def convertMatrixToRGB(Ylist, Ulist, Vlist):
    for i in range(600):
        for j in range(800):
            Y = Ylist[i][j]
            U = Ulist[i][j]
            V = Vlist[i][j]
            R = int(Y+1.1402*(V-128))
            G = int(Y-0.344*(U-128) - 0.714*(V-128))
            B = int(Y+1.772*(U-128))
            if(R <= 0):
                R = 0
            if(R >= 255):
                R = 255
            if(G <= 0):
                G = 0
            if(G >= 255):
                G = 255
            if (B <= 0):
                B = 0
            if(B >= 255):
                B = 255
            Ylist[i][j] = R
            Ulist[i][j] = G
            Vlist[i][j] = B
    return Ylist, Ulist, Vlist


def writeToFile(RMatrix, GMatrix, BMatrix):
    string = "P6\n# CREATOR: GIMP PNM Filter Version 1.1\n800 600\n255\n"
    f = open("p6.ppm", "wb")
    f.write(bytearray(string.encode()))
    for i in range(600):
        for j in range(800):
            f.write(RMatrix[i][j].to_bytes(1, 'big'))
            f.write(GMatrix[i][j].to_bytes(1, 'big'))
            f.write(BMatrix[i][j].to_bytes(1, 'big'))

    f.close()


def decode(Ymat, Umat, Vmat):
    decodedY = recreateBigMatrix(Ymat)
    decodedU = recreateBigMatrix(Umat)
    decodedV = recreateBigMatrix(Vmat)

    RMatrixDecoded, GMatrixDecoded, BMatrixDecoded = convertMatrixToRGB(
        decodedY, decodedU, decodedV)
    writeToFile(RMatrixDecoded, GMatrixDecoded, BMatrixDecoded)

    image = Image.open("p6.ppm")
    image.show()


class main():

    Ylist, Ulist, Vlist = encode()
    decode(Ylist, Ulist, Vlist)


main()
