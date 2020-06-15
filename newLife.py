from os import system
from time import sleep
import random
import datetime
import json

def updateLife(points):
    newPoints = []
    checkedPoints = []
    for point in points:
        y = point[0]
        x = point[1]
        if point not in checkedPoints:
            checkedPoints.append(point)
            if checkPoint(point,points):
                newPoints.append(point)
        for r in [y-1,y,y+1]:
            for c in [x-1,x,x+1]:
                if (r,c) != point and (r,c) not in points and (r,c) not in checkedPoints and (r,c) not in newPoints:
                    checkedPoints.append((r,c))
                    if checkPoint((r,c),points):
                        newPoints.append((r,c))
    return newPoints


def checkPoint(point,points):       
    y = point[0]
    x = point[1]
    count = 0
    for r in [y-1,y,y+1]:
        for c in [x-1,x,x+1]:
            if (r,c) != point and (r,c) in points:
                count +=1
    if count == 2 and point in points:
        return True
    elif count == 3:
        return True
    else:
        return False

def printLife(r,c,points,clear = True,yOff=0,xOff=0,lines = 1,noPoint='.',pnt = '✖',markOrigin=False):
    grid = ''
    empty = True
    foundOrigin = False
    for ro in reversed(range(0,r)):
        row = ro-int(r/2)+yOff
        line = ''
        for co in range(0,c):
            col = co-int(c/2)+xOff
            if (row,col) == (0,0) and markOrigin:
                line+='O'
                foundOrigin = True
            elif (ro,co) == (0,c-1) and markOrigin and not foundOrigin:
                line+=noPoint + '\n' + 'View centered on '+str((row+int(r/2),col-int(c/2)))
            elif (row,col) in points or [row,col] in points:
                line+=pnt
                empty = False
            else:
                if lines > 1 and row%lines == 0:
                    line +=','
                elif lines > 1 and col%lines == 0:
                    line +=','
                else:
                    line+=noPoint
        line+='\n'
        grid+=line
    if clear:
        system('clear')
    print(grid[:-1])
    return empty


def runLife(r,c,points,gen,startGen):
    if gen == 0:
        return
    points = updateLife(points)
    printLife(r,c,points)
    print(str(startGen-gen))
    sleep(.2)
    return runLife(r,c,points,gen-1,startGen)

def runLifeLong(r,c,points,gen,startGen,disp=True):
    if gen<startGen:
        print('Gen must be more than StartGen')
        return
    for i in range(startGen,gen):
        points = updateLife(points)
        if disp:
            printLife(r,c,points)
        print('Generation: ' + str(i+1))
    if not disp:
        printLife(r,c,points)
        print('Generation: ' + str(i+1))
    return(points,i)

def genLifeSeries(points,gen,startGen,showProg=True):
    out = [(startGen,points)]
    if gen<startGen:
        print('Gen must be more than StartGen')
        return
    for i in range(startGen,gen):
        if showProg and i%25 == 0:
            print (i)
        points = updateLife(points)
        out.append((i+1,points))
        if points == []:
            return out
    return out

def printLifeSeries(r,c,series,startGen,endGen,delay,yOff = 0,xOff = 0,optOff = False,lines =1,info = '',markOrigin = False):
    staticList = []
    testFactor = 100
    isStatic = False
    if startGen < series[0][0]:
        print('startGen too low! Series begins at ' + str(series[0][0]))
        return
    if endGen == 0:
        endGen = len(series)
    if endGen > len(series) + series[0][0]:
        print('endGen too high! Series ends at ' + str(len(series) + series[0][0]-1))
        return
    for i in range(startGen-series[0][0],endGen-series[0][0]):
        if False:
            break
        else:
            if len(staticList) >= 13:
                staticList.pop(0)
                staticList.append(series[i][1])
                if checkStatic(staticList,testFactor,yOff,xOff):
                    print('Display has reached static state')
                    sleep(4)
                    return i
            else:
                try:
                    staticList.append(series[i][1])
                except IndexError as e:
                    print(str(e))
        if printLife(r,c,series[i][1],True,yOff,xOff,lines=lines,markOrigin=markOrigin):
            if optOff:
                try:
                    yAvg,xAvg = optimizeOffset(series[i+1][1])
                    yOff= yAvg
                    xOff= xAvg
                    markOrigin = True
                except IndexError as e:
                    print(str(e))
            else:        
                print('No life remains nearby')
                sleep(4)
                return(i)
        print('Generation: ' + str(i+1))
        if info:
            print(info)
        sleep(delay)
    return i+1

def checkStatic(staticList,testFactor,yOff=0,xOff=0):
    newStat = []
    yMin = 0-testFactor+yOff
    yMax = testFactor+yOff
    xMin = 0-testFactor+xOff
    xMax = testFactor+xOff
    for points in staticList:
        tempPoints = []
        for point in points:
            if point[0] > yMin and point[0] < yMax and point[1] > xMin and point[1] < yMax:
                tempPoints.append(point)
        newStat.append(tempPoints)
    comp = newStat[0]
    for step in [1,2,3,4,6]:
        same = True
        for l in range(step,len(newStat),step):              
            if newStat[l]!=comp:
                same = False
        if same:
            return True
    return False            

def optimizeOffset(points):
    yMin = points[0][0]
    yMax = points[0][0]
    xMin = points[0][1]
    xMax = points[0][1]
    for point in points:
        if point[0] < yMin:
            yMin = point[0]
        if point[0] > yMax:
            yMax = point[0]
        if point[1] < xMin:
            xMin = point[0]
        if point[1] > yMax:
            xMax = point[0]
#        print((yMin,yMax,xMin,xMax))
#        print((yMin-yMax,xMin-xMax))
    return int((yMin+yMax)/2),int((xMin+xMax)/2)


def findMoving(staticList):
    backlist = []
    movingPoints = []
    for points in staticList:
        backlist.append(points)
    backlist.reverse()
    for step in [6]:
        tempList = []
        for point in backlist[0]:
            for l in range(step,len(backlist),step):
                if point not in backlist[l] and point not in movingPoints:
                    movingPoints.append(point)
    return movingPoints
    
    
def notInter(a,b):
    out = [] 
    for e in a: 
        if e not in b:
            out.append(e) 
    return out

def inter(a,b):
    out = [] 
    for e in a: 
        if e in b:
            out.append(e) 
    return out 



def ranLifePoints(r,c,highseed):
    out = []
    for row in range(r):
        for col in range(c):
            a = random.randint(0,highseed)
            if a == 1:
                out.append((row,col))
    return out,(r,c,highseed)
                

def makeSeries(reps=25):
    timestamp = '{:%Y%m%d_%H%M%M}'.format(datetime.datetime.now()) 
    seedList = []
    count = 0
    with open('/home/david/lifeSeeds.txt','a') as f:
        f.write(timestamp + '\n')
    while(count < reps):
        seed,dims = ranLifePoints(random.randint(3,10),random.randint(3,10),random.randint(1,4))
        series = genLifeSeries(seed,500,0)
        gens = printLifeSeries(48,188,series,0,0,.3,optOff=True,lines = 1,info = seed)
        with open('/home/david/lifefiles/'+'{:%Y%m%d_%H%M%M}'.format(datetime.datetime.now())+ '_' + str(dims)[1:-1].replace(', ','-')+'_seedfile_' + str(gens)+'-gens.json','w') as f:
            f.write(json.dumps(series))
        seedList.append((seed,gens))
        with open('/home/david/lifeSeeds.txt','a') as f:
            f.write(str(count) + '\n' + json.dumps((seed,gens))+ '\n')
        count +=1
    return seedList



def makeFour(pat):
    a = []
    b = []
    c = []
    d = []
    for point in pat:
        a.append(point)
        b.append((point[0]*-1,point[1]))
        c.append((point[0],point[1]*-1))
        d.append((point[0]*-1,point[1]*-1))
    return a,b,c,d

def transformPat(pat,factor):
    out = []
    for point in pat:
        out.append((point[0]+factor[0],point[1]+factor[1]))
    return out



def parseRle(rle):
    nums = '0123456789'
    out = []
    li = rle.split('\n')
    lr = li[1].split('$')
    row = 0
    col = 0
    for r in lr:
        l = len(r)
        i = 0
        while(r[i]!='$'):
            print('curChar ',r[i])
            print( out)
            print('col ',col)
            if r[i] == 'b':
                col+=1
                i+=1
            elif r[i] == 'o':
                out.append((row,col))
                col+=1
                i+=1
            else:
                if r[i] in nums:
                    num = r[i]
                    b = 1
                    while(r[i+b] in nums):
                        print(row,col,b,r[i+b])
                        num+=r[i+b]
                        print('num ',num)
                        b+=1
                    runCount = int(num)
                    print('runcount ',runCount)
                    print('nextChar ',r[i+b])
                    if r[i+b] == 'b':
                        col +=runCount
                        i = i+b+1
                    elif r[i+b] == 'o':
                        for c in range(col,col+runCount):
                            out.append((row,c))
                        i = i+b+1
                        col+=runCount
                    elif r[i+b] == '$':
                        break
        row+=1
    return out                        
                    
