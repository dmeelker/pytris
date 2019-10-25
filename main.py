import pygame
import os

import blocks
import playfield
from timer import Stopwatch

screen = None
running = True

blockImage = None
block = None
nextBlock = None
moveLeft = False
moveRight = False

baseFallSpeed = 150
fastFallSpeed = 50
fallSpeed = baseFallSpeed

clock = pygame.time.Clock()
dropStopwatch = Stopwatch(pygame.time.get_ticks())

score = 0
lastLineWasTetris = False

def start():
    initialize()

    while running:
        update()
        render()
        clock.tick(60)

def initialize():
    global screen,clock
    pygame.init()
    pygame.display.set_caption("minimal program")
    screen = pygame.display.set_mode((800, 600))
    pygame.key.set_repeat(100, 50)

    loadImages()

    playfield.initialize((10, 22))

    spawnBlock()

def loadImages():
    global blockImage
    blockImage = pygame.image.load(os.path.join('images', 'block-red.png'))

def update():
    handleEvents()

    time = pygame.time.get_ticks()

    updateBlockDrop(time)

def updateBlockDrop(time):
    timePassed = dropStopwatch.update(time)
    if timePassed > fallSpeed:
        dropStopwatch.reset(time)
        if playfield.blockWillCollideNextStep(block):
            playfield.solidifyBlock(block)
            removeFullRows()
            spawnBlock()
        else:
            block.location = (block.location[0], block.location[1] + 1)

def spawnBlock():
    global block, nextBlock

    if nextBlock is None:
        nextBlock = blocks.Block(blocks.randomBlock())
        nextBlock.image = blockImage
    
    block = nextBlock

    nextBlock = blocks.Block(blocks.randomBlock())
    nextBlock.image = blockImage

def handleEvents():
    global running, moveLeft, moveRight
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                block.rotateLeft()
            elif event.key == pygame.K_x:
                block.rotateRight()
            elif event.key == pygame.K_LEFT:
                moveLeft = True
                if playfield.canBlockBeInLocation(block, (block.location[0] - 1, block.location[1])):
                    block.moveLeft()
            elif event.key == pygame.K_RIGHT:
                moveRight = True
                if playfield.canBlockBeInLocation(block, (block.location[0] + 1, block.location[1])):
                    block.moveRight()
            elif event.key == pygame.K_DOWN:
                startFastDrop()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_DOWN:
                stopFastDrop()

def startFastDrop():
    global fallSpeed
    fallSpeed = fastFallSpeed

def stopFastDrop():
    global fallSpeed
    fallSpeed = baseFallSpeed 

def render():
    screen.fill((0, 0, 0))
    
    playfield.render(screen)
    block.render(screen, block.location)
    nextBlock.render(screen, (12, 2))

    pygame.display.flip()

def removeFullRows():
    global score, lastLineWasTetris
    fullRows = playfield.getFullRows()
    clearedRowCount = len(fullRows)
    if clearedRowCount == 0:
        return
    
    for y in fullRows:
        playfield.removeRow(y)

    score += calculatePointsForClearedRows(clearedRowCount)
    lastLineWasTetris = clearedRowCount == 4
    print('Score: ' + str(score))

def calculatePointsForClearedRows(rowCount):
    if rowCount == 4:
        if lastLineWasTetris:
            return 1200 
        else:
            return 800
    else:
        return rowCount * 100

start()