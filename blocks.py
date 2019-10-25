import random

iShape = \
    [[0, 0, 0, 0], \
     [1, 1, 1, 1], \
     [0, 0, 0, 0], \
     [0, 0, 0, 0]]

lShape = \
    [[1, 0, 0], \
     [1, 1, 1], \
     [0, 0, 0]]

reverseLShape = \
    [[0, 0, 1], \
     [1, 1, 1], \
     [0, 0, 0]]

blockShape = \
    [[0, 0, 0, 0], \
     [0, 1, 1, 0], \
     [0, 1, 1, 0], \
     [0, 0, 0, 0]]

stepShape = \
    [[0, 1, 1], \
     [1, 1, 0], \
     [0, 0, 0]]

reverseStepShape = \
    [[1, 1, 0], \
     [0, 1, 1], \
     [0, 0, 0]]

triPoint = \
    [[0, 1, 0], \
     [1, 1, 1], \
     [0, 0, 0]]

blockTypes = [iShape, lShape, reverseLShape, blockShape, stepShape, reverseStepShape, triPoint]

def randomBlock():
    return blockTypes[random.randint(0, len(blockTypes) - 1)]

class Block:
    data = None
    size = 0
    location = (0,0)
    image = None
    
    def __init__(self, data):
        self.data = data
        self.size = len(data[0])

    def render(self, screen, location):
        for y in range(self.size):
            for x in range(self.size):
                if self.data[y][x] == 1:
                    screen.blit(self.image, ((location[0] * 15) + (x * 15), (location[1] * 15) + (y * 15)))

    def rotateRight(self):
        originalData = self.getCopyOfData()
        self.clearData()

        for y in range(self.size):
            for x in range(self.size):
                # x_new = 1 - (y_old - (size - 2))
                # y_new = x_old
                self.data[x][1 - (y - (self.size - 2))] = originalData[y][x]

    def rotateLeft(self):
        self.rotateRight()
        self.rotateRight()
        self.rotateRight()

    def moveLeft(self):
        self.location = (self.location[0] - 1, self.location[1])

    def moveRight(self):
        self.location = (self.location[0] + 1, self.location[1])

    def getCopyOfData(self):
        copy = []
        for y in range(self.size):
            copy.append(list(self.data[y]))
        return copy

    def clearData(self):
        for y in range(self.size):
            for x in range(self.size):
                self.data[y][x] = 0