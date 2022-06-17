import pygame
import random

pygame.init
curentTime = 0
clock = pygame.time.Clock()

GAMELENGTH = 600
GAMEWIDTH = 300
LENGTH = 650 # vertical
WIDTH = 500 # horizontal
BLOCKWIDTH = 30
startValue_y = (LENGTH - GAMELENGTH) // 2
startValue_x = startValue_y

WIN = pygame.display.set_mode((WIDTH, LENGTH))
pygame.display.set_caption("TETRIS")

# COLORS

BACKGROUND = (139,125,107)          # For Background
ORANGE = (255,97,3)             #for game bocks    
PARROTGREEN = (102,205,0)       #for game bocks
SKYBLUE = (152,245,255)         #for game bocks
BLUE = (100,149,237)            #for game bocks
ORCHID = (153,50,204)           #for game bocks
SEAGREEN = (180,238,180)        #for game bocks
GRAY = (161, 161, 161)        # For grid lines

# Shapes

Z = [
        [
            ".00..", 
            "..00.",
            
        ],
        [
            "..0..",
            ".00..",
            ".0...",
        ]
    ]
L = [
        [
            ".0...",
            ".0...",
            ".00.."
        ],        
        [
            "...0.",
            ".000.",
            
        ],
        [
            ".00..",
            "..0..",
            "..0..",
        ],
        [
            ".000.",
            ".0...", 
        ], 
    ]
J = [
        [
            ".000.",
            "...0.",
        ],
        [
            "..0..",
            "..0..",
            ".00..",
        ],
        [
            ".0...",
            ".000.",
        ],
        [
            ".00..",
            ".0...",
            ".0...",
        ],
    ]
I = [
        [
            ".....",
            ".0000"
        ],
        [
            "..0..",
            "..0..",
            "..0..",
            "..0..",
        ],
    ]
T = [
        [
            ".000.",
            "..0..",
        ],
        [
            "..0..",
            "..00.",
            "..0.."
        ],
        [
            "..0..",
            ".000.",
        ],
        [
            "..0..",
            ".00..",
            "..0.."
        ]
    ]
O = [
        [

            "..00.",
            "..00."

        ],
    ]
S = [
        [
            "..00.",
            ".00.."
        ],
        [
            ".0...",
            ".00..",
            "..0.."
        ]
    ]

# CLASS FOR RECTANGLE BLOCKS

class Block:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.color = color
        self.rotation = 0
        self.shape = shape
        self.fall = True


# To draw grid lines
def drawGrid(win, grid, rows, columns):
    win.fill(SKYBLUE)

    for i in range(rows):
        pygame.draw.line(win, GRAY, (startValue_x, startValue_y + i * BLOCKWIDTH), (startValue_x + GAMEWIDTH, startValue_y + i * BLOCKWIDTH), 1)
        for j in range(columns):
            pygame.draw.line(win, GRAY, (startValue_x + j * BLOCKWIDTH, startValue_y), (startValue_x + j * BLOCKWIDTH, startValue_y + GAMELENGTH), 1)
    pygame.draw.line(win, GRAY, (startValue_x, startValue_y + rows * BLOCKWIDTH), (startValue_x + GAMEWIDTH, startValue_y + rows * BLOCKWIDTH), 1)
    pygame.draw.line(win, GRAY, (startValue_x + columns * BLOCKWIDTH, startValue_y), (startValue_x + columns * BLOCKWIDTH, startValue_y + GAMELENGTH), 1)

    for item in grid:
        pygame.draw.rect(win, grid[item], (item[0], item[1], BLOCKWIDTH, BLOCKWIDTH))
            

    pygame.display.update()
# To create place to store blocks
def createSpace(rows, columns, blockAtGame):
    grid = {}
    for i in range(rows):   
        for j in range(columns):
            grid[(startValue_x + 2 + j * BLOCKWIDTH, startValue_y + i * BLOCKWIDTH)] =(0, 0, 0)
            if (j, i) in blockAtGame:
                grid[i, j] = blockAtGame[(i, j)]
    return grid

def getRandom(value):
    return random.choice(value)

# To generate block
def createBlock(shapes, color):
    block  = Block(startValue_x + 2 + 5 * BLOCKWIDTH, startValue_y - 5 * BLOCKWIDTH, getRandom(shapes), getRandom(color))
    return block

def draw(win, formate, block):
    for item in formate:
        pygame.draw.rect(win, block.color, (item[0], item[1], BLOCKWIDTH - 1, BLOCKWIDTH - 1))
    pygame.display.update()

# To draw Block 
def drawBlock(win, block):
    formate = []
    shape = block.shape[ block.rotation % len(block.shape)]
    for i, item in enumerate(shape):
        for j, ite in enumerate(item):
            if ite == "0":
                formate.append((block.x + i * BLOCKWIDTH, block.y + j * BLOCKWIDTH))
    draw(win, formate, block)
    return formate


# To check position to move or not
def checkValidPosition(cucurrentBlock, grid, currentFormatedBlock):
    position = []
    for item in grid:
        if grid[item] ==(0, 0, 0):
            position.append(item)
    for item in currentFormatedBlock:
        if item not in position:
            if item[1] > startValue_y:
                return False
    for items in currentFormatedBlock:
        print(item)
    return True


def deleteRows():
    pass

def checkScore(grid, currentBlock):
    pass

# To check if lost or not
def checkLost():
    pass

# Main Function That Runs First
def main(win, gameWidth, gameLength, startValue_x, startValue_y):
    ROWS = 20
    COLUMNS = 10
    shapes = [Z, L, I, T, O, S, J]
    colors = [ORANGE, PARROTGREEN, BLUE, ORCHID, SEAGREEN]
    running = True
    blockAtGame = {}
    currentBlock = createBlock(shapes, colors)
    nextBlock = createBlock(shapes, colors)
    grid =createSpace(ROWS,COLUMNS, blockAtGame)
    fallSpeed = 0.25 
    fallTime = 0
    
    while running:
        fallTime += clock.get_rawtime()
        clock.tick()
        if fallTime / 1000 > fallSpeed:
            fallTime = 0
            # currentBlock.y += BLOCKWIDTH
            if checkValidPosition(currentBlock, grid, currentFormatedBlock):
                currentBlock.y += BLOCKWIDTH
        currentFormatedBlock = drawBlock(win, currentBlock)
        nextFormatedBlock = drawBlock(win, nextBlock)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    currentBlock.rotation += 1
                    if checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                        currentBlock.rotation -= BLOCKWIDTH
                if event.key == pygame.K_RIGHT:
                    currentBlock.x += 1 * BLOCKWIDTH
                    if checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                        currentBlock.x -= 1
                #if event.key == pygame.K_RIGHT:
                #    currentBlock.x += BLOCKWIDTH
                #    if checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                #        currentBlock.x -= BLOCKWIDTH
                #if event.key == pygame.K_RIGHT:
                #    currentBlock.x += 1 * BLOCKWIDTH
                #    if checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                #        currentBlock.x -= 1
                if event.key == pygame.K_LEFT:
                    currentBlock.x -= 1 * BLOCKWIDTH
                    if checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                        currentBlock.x += 1
                
                if event.key == pygame.K_LEFT:
                    currentBlock.x -= BLOCKWIDTH
                    if  checkValidPosition(currentBlock, grid, currentFormatedBlock) == False:
                        currentBlock.x += BLOCKWIDTH
        
        for ite in currentFormatedBlock:
            if ite[1] >= 595:
                blockAtGame[(ite[0], ite[1])]= currentBlock.color
                currentBlock.fall = False
        if not currentBlock.fall:   
            currentBlock = nextBlock
            nextBlock = createBlock(shapes, colors)   
        drawGrid(win, grid, ROWS, COLUMNS)
           
    pygame.quit()

main(WIN, GAMEWIDTH, GAMELENGTH, startValue_x, startValue_y)
