from tkinter import *
import sys
import random

"""
    Toothpicks.py By Jackson Kerr

    run with python3 Toothpicks.py <Generation> [Generational Ratio]

    Produces a representation of an nth generation toothpick diagram
    on the screen suitably scaled to fit the window.

    Gen 1 = a single horizontal toothpick.

    Generation n:
        For each toothpick in generation n-1 that has not had toothpicks 
        added to it, place two more toothpicks, each being perpendicular 
        to the original, and touching its ends at their midpoints.

    The optional second parameter represents the ratio of the length of 
    the toothpicks in each succeeding generation (ie. r = 0.8 means each 
    toothpick would be 0.8x as long as those in the previous generation).

    Args:
        -c Draw toothpicks in random colours
        -s Keep window open for only 5 seconds
"""

DEFAULT_MATCHLEN = 1
RANDOMLY_COLOUR_MATCHES = False
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000

root = None
frame = None
lineBounds = None

class ToothpicksCanvas(Canvas):

    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)

    def placeLine(self, coords, len, isHorizontal):
        """
            Draws a line in the window.

            coords:         List of len 2 containing the x, y coordinate of the new line.
            len:            The length of the new line.
            isHorizintal:   If true, the line will be drawn horizontally, else vertically.
        """
        centerX = coords[0]
        centerY = coords[1]

        lineColour = 'black'
        if RANDOMLY_COLOUR_MATCHES:
            de=("%02x"%random.randint(0,255))
            re=("%02x"%random.randint(0,255))
            we=("%02x"%random.randint(0,255))
            lineColour="#"+de+re+we

        if isHorizontal:
            self.create_line(centerX - len/2, centerY, centerX + len/2, centerY, fill = lineColour)
        else: 
            self.create_line(centerX , centerY - len/2, centerX, centerY + len/2, fill = lineColour)

    def drawLines(self, lines):
        """
            Given a list of the format [ [isHorizontal, [x coordinate, y coordinate], length], ... ]
            Call the placeline method for each item.
        """
        for line in lines:
            isHorizontal = line[0]
            coords = line[1]
            matchLen = line[2]

            self.placeLine(coords, matchLen, isHorizontal)
        


def main():
    # Handle args
    if "-h" in sys.argv:
        sys.argv.remove("-h")
        printHelp()
        exit()
    if '-c' in sys.argv: 
        sys.argv.remove("-c")
        global RANDOMLY_COLOUR_MATCHES
        RANDOMLY_COLOUR_MATCHES = True

    # Get the required number of generations
    if len(sys.argv) < 2: 
        print("Invalid input, use -h for help")
        exit()
    gen_num = int(sys.argv[1])

    # Get the change in line length between generations
    gen_mod = 1
    if (len(sys.argv) > 2):
        gen_mod = float(sys.argv[2])

    # Stores the furthest distance where a line is drawn
    xBound = 0
    yBound = 0

    # Queue for dfs adding of lines
    nextQueue = [[True, [0, 0], DEFAULT_MATCHLEN]]
    lines = []
    for i in range(gen_num):
        pickQueue = nextQueue
        nextQueue = []
        while len(pickQueue) > 0:
            currLocation = pickQueue.pop(0)

            # For readability
            isHorizontal = currLocation[0]
            coords = currLocation[1]
            matchLen = currLocation[2]

            # Add line to list of lines to be drawn
            lines.append([isHorizontal, coords, matchLen])

            # Add next coords
            if isHorizontal:
                x = coords[0]
                y = coords[1]
                nextQueue.append([False, [x - matchLen/2, y], matchLen * gen_mod])
                nextQueue.append([False, [x + matchLen/2, y], matchLen * gen_mod])
            else:
                x = coords[0]
                y = coords[1]
                nextQueue.append([True, [x, y + matchLen/2], matchLen * gen_mod])
                nextQueue.append([True, [x, y - matchLen/2], matchLen * gen_mod])

            if isHorizontal:
                if x + matchLen/2 > xBound: xBound = x + matchLen/2
                if y > yBound: yBound = y
            else:
                if y + matchLen/2 > yBound: yBound = y + matchLen/2
                if x > xBound: xBound = x
        i += 1

    # Modifiers for converting 0-1 coordinate to board coordinate
    xMod = ((WINDOW_WIDTH-50)/2)/xBound
    yMod = ((WINDOW_HEIGHT-50)/2)/yBound
    
    mod = xMod
    if yMod < xMod: mod = yMod

    # Convert 0-1 coords to board coords
    for i in range(len(lines)):
        line = lines[i]
        
        isHorizontal = line[0]
        coords = line[1]
        lineLen = line[2]

        line[1] = [coords[0]*mod, coords[1]*mod]
        if isHorizontal: line[2] = line[2] * mod
        else:            line[2] = line[2] * mod

    # Create canvas
    global root, frame
    root = Tk()
    frame = Frame(root)
    frame.pack(fill=BOTH, expand=YES)
    canvas = ToothpicksCanvas(frame,width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="grey", highlightthickness=0)
    canvas.pack(fill=BOTH, expand=YES)
    root.resizable(False, False)

    # Draw Lines
    ToothpicksCanvas.drawLines(canvas, lines)

    # Center scroll region at 0 0
    canvas.configure(scrollregion=(-WINDOW_WIDTH/2, -WINDOW_HEIGHT/2, WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

    # Enter main loop
    root.mainloop()

def printHelp():
    print("""
    Toothpicks.py By Jackson Kerr

    run with python3 Toothpicks.py <Generation> [Generational Ratio]

    Produces a representation of an nth generation toothpick diagram
    on the screen suitably scaled to fit the window.

    Gen 1 = a single horizontal toothpick.

    Generation n:
        For each toothpick in generation n-1 that has not had toothpicks 
        added to it, place two more toothpicks, each being perpendicular 
        to the original, and touching its ends at their midpoints.

    The optional second parameter represents the ratio of the length of 
    the toothpicks in each succeeding generation (ie. r = 0.8 means each 
    toothpick would be 0.8x as long as those in the previous generation).

    Args:
        -c Draw toothpicks in random colours
        -s Keep window open for only 5 seconds
    """)

if __name__ == "__main__":
    main()
