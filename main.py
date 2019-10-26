import pygame
import pygame.freetype
import os

import blocks
import playfield
from timer import Stopwatch

screen = None
running = True

backdropImage = None
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

playFieldArea = pygame.Rect(322, 110, 150, 300)
nextBlockArea = pygame.Rect(496, 110, 60, 60)
scoreArea = pygame.Rect(496, 194, 159, 62)

font = None
scoreLabel = None
highScoreLabel = None
score = 0
highScore = 0
lastLineWasTetris = False

def start():
    initialize()

    while running:
        update()
        render()
        clock.tick(60)

def initialize():
    global screen,clock,font
    pygame.init()
    pygame.display.set_caption("Pytris")
    screen = pygame.display.set_mode((800, 600))
    pygame.key.set_repeat(100, 50)

    font = pygame.freetype.Font(None)
    
    updateHighScore(0)

    loadImages()
    screen.blit(backdropImage, (0, 0))

    newGame()

def newGame():
    updateScore(0)

    playfield.initialize((10, 22))
    spawnBlock()

def loadImages():
    global backdropImage,blockImage

    backdropImage = pygame.image.load(os.path.join('images', 'backdrop.png'))
    blockImage = pygame.image.load(os.path.join('images', 'block-red.png'))

def update():
    handleEvents()

    time = pygame.time.get_ticks()

    updateBlockDrop(time)
    if playfield.lineContainsBlocks(1):
        endGame()

def endGame():
    global score, highScore
    print('Game over!')
    updateHighScore(score)
    newGame()

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
    block.location = ((playfield.width / 2) - (block.size / 2),0)

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
    screen.fill((0, 0, 0), playFieldArea)
    screen.fill((0, 0, 0), nextBlockArea)
    screen.fill((0, 0, 0), scoreArea)
    
    screen.set_clip(playFieldArea)
    playfield.render(screen, (playFieldArea.left, playFieldArea.top - 30))
    block.render(screen, (playFieldArea.left + (block.location[0] * 15), playFieldArea.top - 30 + (block.location[1] * 15)))
    screen.set_clip(None)

    screen.blit(scoreLabel[0], (scoreArea.left + 5, scoreArea.top + 5))
    screen.blit(highScoreLabel[0], (scoreArea.left + 5, scoreArea.top + 20))
    

    nextBlock.render(screen, (nextBlockArea.left, nextBlockArea.top))

    pygame.display.flip()

def removeFullRows():
    global lastLineWasTetris
    fullRows = playfield.getFullRows()
    clearedRowCount = len(fullRows)
    if clearedRowCount == 0:
        return
    
    for y in fullRows:
        playfield.removeRow(y)

    updateScore(score + calculatePointsForClearedRows(clearedRowCount))
    lastLineWasTetris = clearedRowCount == 4

def updateScore(newScore):
    global score
    score = newScore
    updateScoreLabel()

def updateScoreLabel():
    global scoreLabel
    scoreLabel = font.render(str(score), fgcolor = (255, 255, 255), size=12)

def updateHighScore(newScore):
    global highScore
    highScore = newScore
    updateHighScoreLabel()

def updateHighScoreLabel():
    global highScoreLabel
    highScoreLabel = font.render(str(highScore), fgcolor = (255, 255, 255), size=12)

def calculatePointsForClearedRows(rowCount):
    if rowCount == 4:
        if lastLineWasTetris:
            return 1200 
        else:
            return 800
    else:
        return rowCount * 100

start()