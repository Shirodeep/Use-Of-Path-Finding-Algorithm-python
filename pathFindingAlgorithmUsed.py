import pygame
import queue
import math
WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Practice project using path finding algorithm")

AQUA = (0,255,255)           # for path finding animation
BANANA = (227,207,87)        # for border of block block
BLACK = (0,0,0)              # for block block
AZURE = (240,255,255)        # for background
DARKORCHID = (153,50,204)    # for starting point
BLUE = (16,78,139)           # for destination point
GRAY = (161,161,161)         # for lines
GREEN = (124,252,0)          # for final path 

class Spot:
    def __init__(self, row, col, width, totalRows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = AZURE
        self.width = width
        self.totalRows = totalRows
        self.neighbours = []

    #making the paths
    def makePath(self):
        self.color = GREEN
    
    def makeStart(self):
        self.color = DARKORCHID
    
    def makeEnd(self):
        self.color = BLUE
    
    def bestPath(self):
        self.color = GREEN
    
    def makeOpen(self):
        self.color = BANANA
    
    def makeBlock(self):
        self.color = BLACK

    def get_pos(self):
        return self.row, self.col
    
    def make_closed(self):
        self.color = AQUA
    
    def isStart(self):
        return self.color == DARKORCHID
    
    def isBlock(self):
        return self.color == BLACK
    
    def resetSpot(self):
        self.color = AZURE
    
    def travellerSpot(self, grid):
        self.neighbours = []
        if self.row < self.totalRows - 1 and not grid[self.row + 1][self.col].isBlock():     #DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
        
        if self.row > 0 and not grid[self.row - 1][self.col].isBlock():                      #UP
            self.neighbours.append(grid[self.row - 1][self.col])
        
        if self.col < self.totalRows - 1 and not grid[self.row][self.col + 1].isBlock():     #RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].isBlock():                      #LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
        
    
    # drawing the colors in rectangle
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
# making the platform
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j * gap, 0), (j * gap, width))            

def draw(win, grid, rows, width):
    win.fill(AZURE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()    

# getting the position
def where_clicked(position, rows, width):
    gap = width // rows
    x, y = position
    row =   x // gap
    col = y // gap
    return row, col

# calculating the distance
def distance(d1, d2):
    x1, y1 = d1
    x2, y2 = d2
    return abs(x1 - x2) + abs(y1 - y2)

def path_finding_function(draw, start, end, grid):
    count = 0
    checking_queue = queue.PriorityQueue()
    checking_queue.put((0, count, start))
    fScore = {}
    gScore = {}
    final_path_to_take = {}
    to_check_if_travelled = {start}
    for row in grid:
        for spot in row:
            fScore[spot] = float("inf")  
            gScore[spot] = float("inf")
    fScore[start] = distance(start.get_pos(),end.get_pos())
    gScore[start] = 0   
    while not checking_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if not start or not end:
            return "Place two position"
            
        current = checking_queue.get()[2]
        # to_check_if_travelled.remove(current)

        if( current == end):
            while current in final_path_to_take:
                print(current)
                current = final_path_to_take[current]
                current.bestPath()
                start.makeStart()
                end.makeEnd()
                draw() 
            return True
                
        for neighbour in current.neighbours:
            tempGScore = gScore[current] + 1
            if tempGScore < gScore[neighbour]:
                final_path_to_take[neighbour] = current
                gScore[neighbour] = tempGScore
                fScore[neighbour] = tempGScore + distance(neighbour.get_pos(),end.get_pos())
                if neighbour  not in to_check_if_travelled:
                    count += 1
                    to_check_if_travelled.add(neighbour)   
                    checking_queue.put((fScore[neighbour], count, neighbour))
                    neighbour.make_closed()
        if current != start:
            current.makeOpen()
        draw()
    return False
        

#defined main function 
def main(win, width):
    algorithm_started = True
    start = None
    end = None
    ROWS = 50
    grid = make_grid(ROWS, width)
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, col = where_clicked(position, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makeStart()
                elif not end and spot != start:
                    end = spot
                    end.makeEnd()
                elif spot != start and spot != end:
                    spot.makeBlock()
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, col = where_clicked(position, ROWS, width)
                spot = grid[row][col]
                spot.resetSpot()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    for rows in grid:
                        for spot in rows:
                            spot.travellerSpot(grid)
                    if algorithm_started:
                        result = path_finding_function(lambda: draw(win, grid, ROWS, width), start, end, grid)
                        algorithm_started = False
                        print(result) 
                if event.key == pygame.K_s:
                    for row in grid:
                        for spot in row:
                            spot.resetSpot()
                            start = None
                            end = None
                            pygame.display.update()
                            algorithm_started = True
                

    pygame.quit() 

main(WIN, WIDTH)