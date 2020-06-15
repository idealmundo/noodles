from os import system

def initLife(y,x,init):
    grid = []
    line = []
    for row in range(y):
        line = []
        for col in range(x):
            if (row,col) in init:
                line.append(True)
            else:
                line.append(False)
        grid.append(line)
    return grid


def printLife(grid,clear=True):
    if clear:
        system('clear')
    out = ''
    for y,row in enumerate(grid):
        for x,col in enumerate(row):
            if grid[y][x]:
                out += 'X'
            else:
                out +='.'
        out += '\n'
    print(out)
 
def updateLife(grid):
    newGrid = []
    for y in range(len(grid)):
        newLine = []
        for x in range(len(grid[0])):
            count = 0
            for r in [y-1,y,y+1]:
                for c in [x-1,x,x+1]:
                    if r ==-1:
                        row = len(grid) - 1
                    elif r == len(grid):
                        row  = 0
                    else:
                        row = r
#                    print (y,r,row)
                    if c == -1:
                        col = len(grid[0]) -1
                    elif c == len(grid[0]):
                        col = 0
                    else:
                        col = c
 #                   print(x,c,col)
                    if (row,col) != (y,x) and grid[row][col]:
                        count +=1
#              print ('count: ' ,count)
            if count <2:
                newLine.append(False)
            if count == 2:
                newLine.append(grid[y][x])
            elif count == 3:
                newLine.append(True)
            elif count >3:
                newLine.append(False)
        newGrid.append(newLine)
    return newGrid
                
                        
                    
def runLife(grid,gen,startGen):
    print(startGen -gen)
    if gen == 0:
        return
    grid = updateLife(grid)
    printLife(grid)
    return runLife(grid,gen-1,startGen)


def updateLife2(grid):
    newGrid = []
    for y in range(len(grid)):
        newLine = []
        for x in range(len(grid[0])):
            count = 0
            for r in [y-1,y,y+1]:
                for c in [x-1,x,x+1]:
                    if r ==-1:
                        continue
                    elif r == len(grid):
                        continue
                    else:
                        row = r
#                    print (y,r,row)
                    if c == -1:
                        continue
                    elif c == len(grid[0]):
                        continue
                    else:
                        col = c
 #                   print(x,c,col)
                    if (row,col) != (y,x) and grid[row][col]:
                        count +=1
#              print ('count: ' ,count)
            if count <2:
                newLine.append(False)
            if count == 2:
                newLine.append(grid[y][x])
            elif count == 3:
                newLine.append(True)
            elif count >3:
                newLine.append(False)
        newGrid.append(newLine)
    return newGrid

def runLife2(grid,gen,startGen):
    print(startGen -gen)
    if gen == 0:
        return
    grid = updateLife2(grid)
    printLife(grid)
    return runLife2(grid,gen-1,startGen)
