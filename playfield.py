import pygame

cells = []
width = 0
height = 0

def initialize(size):
    global width, height
    width = size[0]
    height = size[1]

    for x in range(width):
        column = []
        for y in range(height):
            column.append(None)
        cells.append(column)

def render(screen):
    for x in range(width):
        for y in range(height):
            cell = cells[x][y]

            if not cell is None:
                screen.blit(cell, (x * 15, y * 15))

def solidifyBlock(block):
    for y in range(block.size):
        for x in range(block.size):
            if block.data[y][x] == 1:
                fieldX = block.location[0] + x
                fieldY = block.location[1] + y

                cells[fieldX][fieldY] = block.image

def blockWillCollideNextStep(block):
    return not canBlockBeInLocation(block, (block.location[0], block.location[1] + 1))

def canBlockBeInLocation(block, location):
    for blockY in range(block.size):
        for blockX in range(block.size):
            if block.data[blockY][blockX] == 1:
                fieldX = location[0] + blockX
                fieldY = location[1] + blockY

                if not locationInField((fieldX, fieldY)):
                    return False
                elif not cells[fieldX][fieldY] is None:
                    return False
    return True

def locationInField(location):
    return not (location[0] < 0 or location[0] >= width or \
        location[1] < 0 or location[1] >= height)

def getFullRows():
    rowNumbers = []

    for y in range(height):
        fullRow = True
        for x in range(width):
            if cells[x][y] is None:
                fullRow = False
                break
        
        if fullRow:
            rowNumbers.append(y)
    
    return rowNumbers

def removeRow(y):
    for x in range(width):
        cells[x][y] = None

    for upperY in reversed(range(y)):
        for x in range(width):
            cells[x][upperY + 1] = cells[x][upperY]
            cells[x][upperY] = None