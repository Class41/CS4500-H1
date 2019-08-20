# Author: Vasyl Onufriyev
# Project: Homework 1
# Purpose: Implement circles and arrows game
# Started: 8.20.19
# Completed:
import random
import sys


class Circle:
    def __init__(self, checkedStatus, arrows):
        self.checkedStatus = checkedStatus
        self.arrows = arrows

    def getCheckedStatus(self):
        return self.checkedStatus

    def getRandomArrow(self):
        return self.arrows[random.randint(0, len(self.arrows))]

    def addToArrowArary(self, circleObj):
        self.arrows.append(circleObj)


def main():
    fileIn = open("HW1infile.txt")
    try:
        numCircles = int(fileIn.readline())
        numArrows = int(fileIn.readline())
    except:
        print("Something is wrong with the input...please check and try again.")
        return

    print("Number of circles read: " + str(numCircles))
    print("Number of arrows read: " + str(numArrows))

    if numCircles == 0 or type(numCircles) != int:
        print("You must have at least one circle.")
        return

    if numArrows < (numCircles * (numCircles - 1)) / 2 or type(numCircles) != int:
        print("The number of arrow specified do not meet the bare-minimum requirements for a strongly connected graph.")
        return

    circles = []

    for x in range(0, numCircles - 1):
        circles.append(Circle(False, []))

    iterator = 0
    try:
        for iterator in range(0, numArrows):
            arrowSpec = fileIn.readline().split(' ')
            if arrowSpec is None or len(arrowSpec) < 2:
                raise Exception("Not enough valid lines in input file. Expected " + str((numArrows + 2)))
    except Exception as e:
        print("Something went wrong! (Stopped on input line #" +
              str((iterator + 3)) + "): " + str(e))


if __name__ == "__main__":
    main()
