"""

    Toothpicks.py By Jackson Kerr

    A program that produces a representation of an nth generation toothpick diagram
    as a png. The program also takes an optional second parameter r which is the
    ratio of the length of the toothpicks in each succeeding generation.

"""
from tkinter import Tk, Canvas, Frame, BOTH
import copy

DEFAULT_MATCHLEN = 50

class Example(Frame):
    canvas = None

    def __init__(self):
        super().__init__()

        self.initialise()

    def placeLine(self, coords, len, isHorizontal):
        """
            Draws a line on the screen, location is given as a single point at the center of the line
        """
        centerX = coords[0]
        centerY = coords[1]

        if isHorizontal:
            self.canvas.create_line(centerX - len/2, centerY, centerX + len/2, centerY)
            return not isHorizontal, [centerX - len/2, centerY], [centerX + len/2, centerY]
        else: 
            self.canvas.create_line(centerX , centerY - len/2, centerX, centerY + len/2)
            return not isHorizontal, [centerX , centerY - len/2], [centerX, centerY + len/2]
        

    def initialise(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        # Test line TODO remove
        #self.placeLine([0, 0], DEFAULT_MATCHLEN, True)

        self.canvas.configure(scrollregion=(-250,-250, 250, 250))
        self.canvas.pack(fill=BOTH, expand=1)

        # 1, 3, 7, 13, 19, 
        n = 5
        r = 0.5
        takenSpaces = []
        nextQueue = [[True, [0, 0]]]

        for i in range(n):
            pickQueue = nextQueue
            nextQueue = []
            matchLen = r * i * DEFAULT_MATCHLEN
            while len(pickQueue) > 0:
                currLocation = pickQueue.pop(0)

                coords = currLocation[1]

                if str(coords) in takenSpaces: continue
                takenSpaces.append(str(coords))

                isHorizontal = currLocation[0]
                nextLocations = self.placeLine(coords, matchLen, isHorizontal)

                nextQueue.append([nextLocations[0], nextLocations[1]])
                nextQueue.append([nextLocations[0], nextLocations[2]])
            i += 1



def main():
    root = Tk()
    ex = Example()
    root.geometry("500x500+1600+500")
    root.minsize(500, 500)
    root.mainloop()



if __name__ == '__main__':
    main()