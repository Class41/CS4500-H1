""" 
# Author: Vasyl Onufriyev
# Project: Homework 1
# Purpose: Implement circles and arrows game
# Started: 8.20.19
# Completed: 8.20.19

* Game Rules *

    ** Input **
    The input file is called HW1infile.txt, inputs are as follows:
    Line 1:         # of circles to be employed during the game
    Line 2:         # of edges or "arrows" to be used between the circles
    Line 3 - n:     Arrows denoted as start-end positions

    Example input file:
    5
    10
    1 2
    2 3
    3 4
    4 5
    5 2
    3 1
    1 3
    3 3
    1 4
    5 3

    ** Assumptions **
    The number of arrows is equal to n where n is the number of circles,
    or in other words the number on the first line of the input file.

    It is assumed that data that will be provided will be a strongly connected graph
    and a circuit can be completed on the graph.

    Circles are numbered from 1 to n

    ** Rules **
    The arrows game consists of a simple ruleset:
    1.  Start at a random point in the graph and place a "marker"
    2.  Choose a random path from the current node or "circle" in the 
        graph and proceed to any connected
    3.  Move the "current marker" location to the newly traversed node
    4.  Repeat steps 2 & 3 until all nodes in the graph have been visited

* Program Structure Explained *
    ** Possible Bugs **
    If any bugs are encountered, they are most likely linked to the input file
    not having content on lines but are just left empty. Input file should only 
    contain lines with content. EOF checking is used to determine input set

    ** Data Structures **
    The primary data structure of this program is called "Circle" and is defined as a class.
    On init, it expects a checked counter and a vector of arrows which are simply integers
    to other Circle objects in a larger Circle list. Some functionality was added and was
    intentionally not used simply for future assignment compatibility.

    ** External Files **
    The input file for this project is Hw1infile.txt, the details of what should be in that 
    file are explained above.

    The output file of this program is called HW1OnufriyevOutfile.txt and will contain the 
    top several lines of the input file, I.E the number of circles and arrows in play within
    the game and analytical data such as the total number of circles visited, average number 
    of checks in a circle throughout the game, and the max number of checks 

    ** Assumtions For Calculations **
    I assume that the circle that you begin the game on should be included for the calculations
    for how many circles were visited throughout the game and is marked as checked the moment 
    the game begins.

"""

import random
import sys

"""
# Class: Circle
# Purpose: The Circle class functions as a datastrcuture for information in this project
           Circle stores the check count on the node, and also the arrows that are going
           out of the circle and their destinations. Helper functions inside the class
           assist in getting the data out and modifying the private variables.

           For the purpose of this project, it takes in just standard 0 and empty array as
           parameters, but I designed this to be future-proof in case of expansion
"""
class Circle:
    def __init__(self, checkedCount, arrows):
        self.checkedCount = checkedCount
        self.arrows = arrows

    def getCheckedStatus(self):
        return self.checkedCount

    def getRandomArrow(self):
        return self.arrows[random.randint(0, len(self.arrows) - 1)]

    def addToArrowArray(self, circleObj):
        self.arrows.append(circleObj)
    
    def getArrows(self):
        return self.arrows
    
    def getCheckCount(self):
        return self.checkedCount
    
    def setVisited(self):
        self.checkedCount += 1

"""
# Function: convertFromArray
# Purpose: Used during the mapping proccess of data to convert array notation back to
           expected humanly-readable notation and insert spaces to seperate output
           on the console
"""
def convertFromArray(x):
    x += 1
    return str(x) + " "

"""
# Function: getArrows
# Purpose: Given the input file, the circle count, and arrow count, generates a set
           of Circle objects in a list form that contains their attributes and interactions
           with the other circle objects. For example, the circle at position 0 would store
           data for input data file data that mentions "Circle 1", and that Circle 1 has a 
           arrow pointing to circles 3,4,5. This Circle is now stored in the array at position
           0.
"""
def getArrows(fileIn, numCircles, numArrows):
    circles = []
    for x in range(0, numCircles):
        circles.append(Circle(0, []))

    iterator = 0
    try:
        for iterator in range(0, numArrows):
            arrowSpec = fileIn.readline().split(' ')
            if arrowSpec is None or len(arrowSpec) < 2:
                raise Exception("Not enough valid lines in input file. Expected " + str((numArrows + 2)))
            else:
                if(int(arrowSpec[0]) < 1 or int(arrowSpec[1]) < 1 or int(arrowSpec[0]) > numCircles or int(arrowSpec[1]) > numCircles):
                    raise Exception("Expected arrow start and end positions to be in range of 1 to " + str(numCircles))
                else:
                    circles[int(arrowSpec[0]) - 1].addToArrowArray(int(arrowSpec[1]) - 1)
    except Exception as e:
        print("Something went wrong! (Stopped on input line #" +
              str((iterator + 3)) + "): " + str(e))
        return None

    return circles

"""
# Function: playTheGame
# Purpose: Given a set of circles, the number of circles and arrows, selects a random circle to start at
           then proceeds to select a random connection off the starting node continues randomly selecting
           arrows and checking if all node are visited until all nodes are visited at least once
"""
def playTheGame(circles, numCircles, numArrows):
    currentCircle = random.randint(0, numCircles - 1) #I know you said "in circle 1" in the assingment, 
                                                      #but I assumed that was randomly chosen out of the 3 possible
    circles[currentCircle].setVisited()
    allNodesHit = False

    print("Beginning graph traversal")
    while allNodesHit != True:
        newVisitingCircle = circles[currentCircle].getRandomArrow()
        print("Traversing " + str(currentCircle + 1) + " => " + str(newVisitingCircle + 1))
        currentCircle = newVisitingCircle
        circles[currentCircle].setVisited()
        allNodesHit = True

        for circle in circles:
            if circle.checkedCount == 0:
                allNodesHit = False
                break
                
    outputResults(circles, numCircles, numArrows)
    
def outputResults(circles, numCircles, numArrows):
    outputFile = open("HW1OnufriyevOutfile.txt", "w")
    outputFile.write("Number of circles used for the game is: " + str(numCircles))
    outputFile.write("\nNumber of arrows user for this game is: " + str(numArrows))

    print("Number of circles used for the game is: " + str(numCircles))
    print("Number of arrows user for this game is: " + str(numArrows))

    totalChecks = 0;
    maxChecks = 0

    for circle in circles:
        totalChecks += circle.getCheckCount()
        if circle.getCheckCount() > maxChecks:
            maxChecks = circle.getCheckCount()

    outputFile.write("\nTotal number of circles visited is: " + str(totalChecks))
    outputFile.write("\nAverage number of circle hits: " + str(float(totalChecks) / float(numCircles)))
    outputFile.write("\nMax number of circle hits: " + str(maxChecks))

    print("Total number of circles visited is: " + str(totalChecks))
    print("Average number of circle hits: " + str(float(totalChecks) / float(numCircles)))
    print("Max number of circle hits: " + str(maxChecks))


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

    if numArrows < numCircles or type(numCircles) != int:
        print("The number of arrow specified do not meet the bare-minimum requirements for a strongly connected graph.")
        return

    circles = getArrows(fileIn, numCircles, numArrows)

    if circles == None:
        return

    for pos in range(0, len(circles)):
        print(str(pos + 1) + " is pointing to => " + "".join(map(convertFromArray, circles[pos].getArrows())))

    playTheGame(circles, numCircles, numArrows)

if __name__ == "__main__":
    main()
