from graphics import *
import math

def getInputs():
    validSizes = [5, 7, 9]
    validColors = ['red', 'green', 'blue', 'magenta', 'orange', 'yellow', 'cyan']
    size, colours = '', []

    while not(size in validSizes):
        size = input('Enter size of grid (5/7/9): ')
        if size.isdigit():
            size = int(size)
            if size not in validSizes:
                print('Invalid input: size must be 5, 7 or 9')
        else:
            print('Invalid input: must enter an integer')
        
    while not(len(colours) == 3):
        colour = input('Enter colour (red/green/blue/magenta/orange/yellow/cyan): ')
        if colour in validColors:
            colours.append(colour)
        else:
            print('Invalid input: colour must be red, green, blue, magenta, orange, yellow or cyan')

    return size, colours


# create a 2d array for the pattern and colours
def generatePatterns(size, colours):
    pattern, colourPattern = [], []

    # Generate pattern for patchwork
    for i in range(size):
        pattern.append([])
        for j in range(size):
            if j == i:
                pattern[i].append('f')
            elif i % 2 == 0:
                pattern[i].append('p')
            else:
                pattern[i].append(' ')

    # Generate colour pattern for patchwork
    for y in range(size):
        colourPattern.append([])
        for x in range(size):
            if (y > 0 and y < size-1) and (x > 0 and x < size-1):
                colourPattern[y].append(colours[2])
            elif y % 2 == 0 and x % 2 == 0:
                colourPattern[y].append(colours[0])
            elif y % 2 == 0 and x % 2 == 1 or y % 2 == 1 and x % 2 == 0:
                colourPattern[y].append(colours[1])

    return pattern, colourPattern


def drawRectangle(win, point1, point2, colour, outline='n'):
    rect = Rectangle(point1, point2)
    rect.setFill(colour)
    if outline == 'y':
        rect.setOutline('black')
        rect.setWidth(0.5)
    else:
        rect.setOutline('')
    rect.draw(win)
    return rect


def drawPenulPatch1(win, x, y, colour1):
    colour2='white'
    
    for b in range(0, 100, 20):
        for a in range(0, 100, 20):
            # swap colours on every other row
            if b/2/10 % 2 == 0: 
                startColour, secondColour = colour1, colour2
            else:
                startColour, secondColour = colour2, colour1
            
            if (a+b)/2/10 % 2 == 0: # vertical lines
                for i in range(0, 20, 5):
                    if i % 2 == 0:
                        drawRectangle(win, Point(x+a+i, y+b), Point(x+a+i+5, y+b+20), startColour, 'y')
                    else:
                        drawRectangle(win, Point(x+a+i, y+b), Point(x+a+i+5, y+b+20), secondColour, 'y')
            else: # horizontal lines
                for i in range(0, 20, 5):
                    if i % 2 == 0:
                        drawRectangle(win, Point(x+a, y+b+i), Point(x+a+20, y+b+i+5), startColour, 'y')
                    else:
                        drawRectangle(win, Point(x+a, y+b+i), Point(x+a+20, y+b+i+5), secondColour, 'y')


def drawPenulPatch(win, x, y, colour1):
    colour2=''
    
    for b in range(0, 100, 20):
        for a in range(0, 100, 20):
            # swap colours on every other row
            if b/2/10 % 2 == 0: 
                startColour, secondColour = colour1, colour2
            else:
                startColour, secondColour = colour2, colour1
            
            if (a+b)/2/10 % 2 == 0: # vertical lines
                for i in range(0, 20, 5):
                    if i % 2 == 0:
                        drawRectangle(win, Point(x+a+i, y+b), Point(x+a+i+5, y+b+20), startColour, 'y')
                    else:
                        drawRectangle(win, Point(x+a+i, y+b), Point(x+a+i+5, y+b+20), secondColour, 'y')
            else: # horizontal lines
                for i in range(0, 20, 5):
                    if i % 2 == 0:
                        drawRectangle(win, Point(x+a, y+b+i), Point(x+a+20, y+b+i+5), startColour, 'y')
                    else:
                        drawRectangle(win, Point(x+a, y+b+i), Point(x+a+20, y+b+i+5), secondColour, 'y')


def drawFinalPatch(win, x, y, colour):
    for i in range(0, 100, 10):
        topLeftx = x + i
        topLefty = y + 100 - (i + 10)
        botRightx = x + 10 + i
        botRighty =  y + 100
        drawRectangle(win, Point(topLeftx, topLefty), Point(botRightx, botRighty), colour)


def distanceBetweenPoints(p1, p2):
    return math.sqrt((p2.getX()-p1.getX())**2+(p2.getY()-p1.getY())**2)


def undrawAll(objects):
    for obj in objects:
        obj.undraw()


def editMode(win, size, selectedPatches, patchPattern, colourPattern, padding, modeText):
    newPatchPattern = list(map(list, patchPattern))
    newColourPattern = list(map(list, colourPattern))

    while True:
        key = win.getKey()
        if key == 's': # enter selesction mode
            return patchPattern, colourPattern
        elif key == 'd': # deselect patches 
            selectedPatches = []
        elif key == 'p': # change patches to penultimate patch
            for i in range(len(selectedPatches)):
                row = selectedPatches[i][0]
                column = selectedPatches[i][1]
                newPatchPattern[row][column] = 'p'
        elif key == 'f': # change patches to final patch
            for i in range(len(selectedPatches)):
                row = selectedPatches[i][0]
                column = selectedPatches[i][1]
                newPatchPattern[row][column] = 'f'
        elif key == 'q': # change patches to plain patch
            for i in range(len(selectedPatches)):
                row = selectedPatches[i][0]
                column = selectedPatches[i][1]
                newPatchPattern[row][column] = ' '
        elif key in ['r', 'g', 'b', 'm', 'o', 'y', 'c']: # change colour of patches
            for i in range(len(selectedPatches)):
                row = selectedPatches[i][0]
                column = selectedPatches[i][1]
                if key == 'r':
                    newColourPattern[row][column] = 'red'
                elif key == 'g':
                    newColourPattern[row][column] = 'green'
                elif key == 'b':
                    newColourPattern[row][column] = 'blue'
                elif key == 'm':
                    newColourPattern[row][column] = 'magenta'
                elif key == 'o':
                    newColourPattern[row][column] = 'orange'
                elif key == 'y':
                    newColourPattern[row][column] = 'yellow'
                elif key == 'c':
                    newColourPattern[row][column] = 'cyan'
        if newPatchPattern != patchPattern or newColourPattern != colourPattern:
            for item in win.items[:]:
                item.undraw()
            modeText.draw(win)
            drawPatchWork(win, size, newPatchPattern, newColourPattern, padding)


def selectionMode(win, size, padding):
    okRect = drawRectangle(win, Point(10, 10), Point(40, 40), 'black')
    okText = Text(Point(25, 25), 'OK')
    okText.draw(win).setTextColor('white')

    closeRect = drawRectangle(win, Point(size*100-10, 10), Point(size*100-50, 40), 'black')
    closeText = Text(Point(size*100-30, 25), 'Close') 
    closeText.draw(win).setTextColor('white')

    selectedPatchesList = []
    while True:
        click = win.getMouse()
        if distanceBetweenPoints(click, Point(25, 25)) < 15: # leave selection mode
            undrawAll([okRect, okText, closeRect, closeText])
            return selectedPatchesList, False
        elif distanceBetweenPoints(click, Point(size*100-30, 25)) < 35: # close window and program
            win.close()
            return selectedPatchesList, True
        else: # add clicked on patch to list
            row = int((click.getY()-padding)//100)
            column = int(click.getX()//100)
            if [row, column] not in selectedPatchesList and row >= 0 and column >= 0:
                selectedPatchesList.append([row, column])


def drawPatchWork(win, size, patchPattern, colourPattern, padding):
    for y in range(0, size*100, 100):
        for x in range(0, size*100, 100):
            row = y//100
            column = x//100
            if patchPattern[row][column] == 'f':
                drawFinalPatch(win, x, y+padding, colourPattern[row][column])
            elif patchPattern[row][column] == 'p':
                drawPenulPatch(win, x, y+padding, colourPattern[row][column])
            else:
                drawRectangle(win, Point(x, y+padding), Point(x+100, y+100+padding), colourPattern[row][column])


def main():
    padding = 50 # for selection mode menu
    size, colours = getInputs()
    patchPattern, colourPattern = generatePatterns(size, colours)
    win = GraphWin('Patchwork Coursework', size*100, (size*100)+padding) 

    drawPatchWork(win, size, patchPattern, colourPattern, padding)
    
    mode = Text(Point(size*100/2, 25), '')
    mode.draw(win)

    while True:
        mode.setText('Selection Mode')
        selectedPatches, close = selectionMode(win, size, padding)
        if close == True:
            break
        mode.setText('Edit Mode')
        newPatchPattern, newColourPattern = editMode(win, size, selectedPatches, patchPattern, colourPattern, padding, mode)
        patchPattern, colourPattern = list(map(list, newPatchPattern)), list(map(list, newColourPattern))

main()