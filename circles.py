""" 
# Author: Vasyl Onufriyev
# Project: Homework 2
# Purpose: Implement circles and arrows game w/ additional connectivity checks
# Started: 8.27.19
# Completed: 8.28.19

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
    The number of arrows is equal/greaterthan to n where n is the number of circles,
    or in other words the number on the first line of the input file.

    Circles are numbered from 1 to n

    ** Rules **
    The arrows game consists of a simple ruleset:
    1.  Start at a 1st circle in the graph and place a "marker"
    2.  Choose a random path from the current node or "circle" in the 
        graph and proceed to any connected
    3.  Move the "current marker" location to the newly traversed node
    4.  Repeat steps 2 & 3 until all nodes in the graph have been visited
    5.  Repeat steps 1-4 until NUMGAMES games are completed

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

    The output file of this program is called HW2OnufriyevOutfile.txt and will contain the 
    top several lines of the input file, I.E the number of circles and arrows in play within
    the game and analytical data such as the total number of circles visited, average number 
    of checks in a circle throughout the game, and the max number of checks for each game played.

    In addition, there is also mins/maxes/averages of NUMGAMES games at the very bottom. These values
    are calcualted using the results of the NUMGAMES games. 

    ** Assumtions For Calculations **
    I assume that the circle that you begin the game on should be included for the calculations
    for how many circles were visited throughout the game and is marked as checked the moment 
    the game begins.

"""


import secrets
import sys
import math

NUMGAMES = 10 #number of games to emulate
MAXCHECKS = 1000000 #checkmarks in circles total limit for a game. Exit game if exceeded

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
        self.checkedCount = checkedCount #running counter of visits
        self.arrows = arrows #arrows are a set of integers which correspond to the index of the
                             #Circles array which are mentioned below in the other functions
        self.isFlagged = False #default flag value, used for connectivity checks

    def getCheckedStatus(self):
        return self.checkedCount

    def getRandomArrow(self):
        return self.arrows[secrets.randbelow(len(self.arrows)) - 1] #select a random defined arrow and return.
                                                                    #uses CRYPTOGRAPHICALLY SECURE library

    def addToArrowArray(self, circleObj): #adds a given circle to the array
        self.arrows.append(circleObj)
    
    def getArrows(self): #gets the arrow int array
        return self.arrows
    
    def getCheckCount(self): #gets how many times this circle was visited
        return self.checkedCount
    
    def setVisited(self): #sets that this circle was visited
        self.checkedCount += 1

    def flagMe(self): #sets a flag on this circle. used for path validation
        self.isFlagged = True
    
    def clearFlag(self): #clears flag see flagMe()
        self.isFlagged = False

    def getFlag(self): #gets flag see flagMe()
        return self.isFlagged


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


def getArrows(fileIn, outputFile, numCircles, numArrows):
    circles = []
    for x in range(0, numCircles): #creates a cicle object for each circle in play
        circles.append(Circle(0, []))

    iterator = 0 #used to help with error detection
    try:
        for iterator in range(0, numArrows): #for every line after the first two
            arrowSpec = fileIn.readline().split(' ') #break down the input in X X format
            if arrowSpec is None or len(arrowSpec) < 2 or len(arrowSpec) > 2: #if there is no input or less than expected input or more
                raise Exception("Not enough valid lines in input file. Expected " + str((numArrows + 2))) #complain
            else: #this is called if the proper number of inputs have been found
                if(int(arrowSpec[0]) < 1 or int(arrowSpec[1]) < 1 or
                 int(arrowSpec[0]) > numCircles or int(arrowSpec[1]) > numCircles): #making sure when converted to array notation, 
                                                                                    #we don't go negative. Numbers expected are expected to be bigger than 1. 
                                                                                    #Also, make sure that the starting or ending positions of arrows 
                                                                                    #don't exceed the number of circles.
                    raise Exception("Expected arrow start and end positions to be in range of 1 to " + str(numCircles))
                else:
                    circles[int(arrowSpec[0]) - 1].addToArrowArray(int(arrowSpec[1]) - 1) #If input is fine, only then add it to array of circles. 
                                                                                          #Assuming input for start end is X Y
                                                                                          #At position X - 1 (since array start at 0)
                                                                                          #set value equal to Y, I.E arrow destination
                                                                                          #which is a index in the circles array
    except Exception as e:
        print("Something went wrong! (Stopped on input line #" +
              str((iterator + 3)) + "): " + str(e)) #display detailed debug output in case there is a problem
        outputFile.write("Something went wrong! (Stopped on input line #" +
              str((iterator + 3)) + "): " + str(e))
        return None

    return circles


"""
# Function: verifyConnectivity
# Purpose: Given the input circle array, check if each circle can get to every other circle
           using some combination of traversing between cicles 1-n. This specific function handles
           checking that all circles at least have one in/out and then kickstarts the recursion
           function. The 0 arrow test is there to short circuit the test.
"""


def verifyConnectivity(circles):
    for circle in circles: #for each circle, does each one have at LEAST one output arrow?
        if len(circle.getArrows()) == 0:
            return 0 #if not, then the graph can't be connected

    for circle in circles: #for each circle
        flagEverythingConnected(circles, circle) #flag all accessable circles
        if validateFlags(circles) == -1: #are there any unflagged circles?
            return -1 #then we aren't connected
        clearFlags(circles) #clear the flags for the next initilazation circle

    return 1


"""
# Function: flagEverythingConnected
# Purpose: Given the circle array and a specific circle, flag the current circle we are in
           then find a connected circle that has yet to be flagged. Once one has been found,
           go visit that one recursively. Then once that path has been explored, and recursion
           unwinds, we return back to the spot where we found the unflagged circle. We then check
           the next circle in our arrows list that hasn't been flagged yet and flag that etc.
"""


def flagEverythingConnected(circles, circle):
    circle.flagMe() #flag me

    for targetCircle in circle.getArrows(): #for every circle I am connected to
        if circles[targetCircle].getFlag() == False: #is the connected circle flagged? If not
            flagEverythingConnected(circles, circles[targetCircle]) #let's flag it and have it do the same


"""
# Function: validateFlags
# Purpose: Ran normally after flagEverythingConnected(). Verifies that from the start circle, as detailed
           in verifyConnectivity(), that we reached all other circles in the graph. If not, we return a 
           failure result.
"""


def validateFlags(circles):
    for circle in circles: #for each circle
        if circle.getFlag() == False: #if there is a circle that hasn't been visited
            return -1 #that means that there is a circle that is inaccessable
    return 1


"""
# Function: clearFlags
# Purpose: After we have validated the flags using validateFlags(), we now need to clear them so the next
           round doesn't get confused. For each circle, clear the flag!
"""


def clearFlags(circles):
    for circle in circles: #for each circle, remove the flag if any
        circle.clearFlag()


"""
# Function: playTheGame
# Purpose: Given a set of circles, the number of circles and arrows, selects the first circle to start at
           then proceeds to select a random connection off the starting node continues randomly selecting
           arrows and checking if all node are visited until all nodes are visited at least once
"""


def playTheGame(circles, numCircles, numArrows, outputFile):
    currentCircle = 0 #start at circle #1
    circles[currentCircle].setVisited() #set the starting node as visited
    allNodesHit = False
    checks = 0

    #print("Beginning graph traversal")
    while allNodesHit != True: #while nodes are still unvisited
        newVisitingCircle = circles[currentCircle].getRandomArrow()
        
        #print("Traversing " + str(currentCircle + 1) + " => " + str(newVisitingCircle + 1))
        #outputFile.write("Traversing " + str(currentCircle + 1) + " => " + str(newVisitingCircle + 1) + "\n")
        
        currentCircle = newVisitingCircle #the current circle is now the circle we just visited
        circles[currentCircle].setVisited() #add a "visited" count to this circle
        checks = checks + 1 #used to make sure we don't exceed the check cap for this game
        allNodesHit = True #assume we hit all nodes

        for circle in circles: #for each circle, check if the visited count is 0. If yes, then we havent visited it!
            if circle.checkedCount == 0:
                allNodesHit = False #our above assumption that all nodes visited was wrong. Keep playing
                break #since there is a unvisited node, we don't care about the rest. We're looping again anyways

        if(checks >= MAXCHECKS - 1): #have we exceeded the number of checks allowed per game?
            print("\nGame terminated: Exceeded max number of checks")
            outputFile.write("\n\nGame terminated: Exceeded max number of checks")
            sys.exit() #exits the game

    return outputResults(circles, numCircles, numArrows, outputFile)
    


"""
# Function: outputResults
# Purpose: Gets called by the playTheGame function and displays the result of the game
"""


def outputResults(circles, numCircles, numArrows, outputFile):    
    #file output version
    outputFile.write("Number of circles used for the game is: " + str(numCircles))
    outputFile.write("\nNumber of arrows user for this game is: " + str(numArrows))
    
    #console output version
    print("Number of circles used for the game is: " + str(numCircles))
    print("Number of arrows user for this game is: " + str(numArrows))

    totalChecks = 0 #total number of checks in a game
    maxChecks = 0 #max number of checks in game (on a single circle)
    minChecks = 2147483647 #min number of checks in a game (on a single circle)

    for circle in circles: #for each circle in the circle array
        totalChecks += circle.getCheckCount() #add this circle's hitcount to the total
        if circle.getCheckCount() > maxChecks: #if this circle has more hits than the last max
            maxChecks = circle.getCheckCount() #this is now the new max
        if circle.getCheckCount() < minChecks: #if this circle has less hits than the last min
            minChecks = circle.getCheckCount() #this is now the new min

    #file output
    outputFile.write("\nTotal number of circles visited is: " + str(totalChecks))
    outputFile.write("\nAverage number of circle hits: " + str(float(totalChecks) / float(numCircles))) #total checks divided by total circles = #checks/circles avg
    outputFile.write("\nMax number of circle hits: " + str(maxChecks) + "\n\n")

    #console output
    print("Total number of circles visited is: " + str(totalChecks))
    print("Average number of circle hits: " + str(float(totalChecks) / float(numCircles)))
    print("Max number of circle hits: " + str(maxChecks) + "\n")

    return [totalChecks, minChecks, maxChecks, float(totalChecks) / float(numCircles)] #return array of game statitics to main for future proccessing


"""
# Function: finalWriteAndClose
# Purpose: Gets called at the end of all NUMGAMES games and displayed/prints averages/mins/maxes to output file. Closes in/out files after
"""


def finalWriteAndClose(outputFile, fileIn, avgNumTotalChecks, avgNumChecksSingleCircle,
     maxNumTotalChecks, minNumTotalChecks, maxNumCircleChecks, minNumCircleChecks):
    #file output
    outputFile.write("\nAverage number of total checks in a game is: " + str(avgNumTotalChecks))
    outputFile.write("\nAverage number of single circle checks in a game is: " + str(avgNumChecksSingleCircle))
    #console output
    print("Average number of total checks in a game is: " + str(avgNumTotalChecks))
    print("Average number of single circle checks in a game is: " + str(avgNumChecksSingleCircle))

    #file output
    outputFile.write("\nMax number of checks total in any game is: " + str(maxNumTotalChecks))
    outputFile.write("\nMin number of checks total in any game is: " + str(minNumTotalChecks))
    #console output
    print("Max number of checks total in any game is: " + str(maxNumTotalChecks))
    print("Min number of checks total in any game is: " + str(minNumTotalChecks))

    #file output
    outputFile.write("\nMax number of single circle checks in any game is: " + str(maxNumCircleChecks))
    outputFile.write("\nMin number of single circle checks in any game is: " + str(minNumCircleChecks))
    #console output
    print("Max number of single circle checks in any game is: " + str(maxNumCircleChecks))
    print("Min number of single circle checks in any game is: " + str(minNumCircleChecks))

    outputFile.flush() #flushes and closes output file
    outputFile.close()
    fileIn.flush() #flushes and closes input file
    fileIn.close()

"""
# Function: main
# Purpose: Does main stuff like booting up the project, getting the input file and reading in
           the top two lines (circle and arrow count) then passing the data along to the circle
           generator which returns a circle data set which is then passed into the play function
"""


def main():
    outputFile = None #placeholder for outputfile stream
    fileIn = None #placeholder for inputfilestream

    avgNumTotalChecks = 0.00 #The average number of total checks per game
    maxNumTotalChecks = 0 #The maximum number of total checks in a single game
    minNumTotalChecks = 2147483647 #The minimum number of total checks in a single game
    avgNumChecksSingleCircle = 0.00 #The average number of checks on a single circle over all the games
    maxNumCircleChecks = 0 #The minimum number of single circle checks
    minNumCircleChecks = 2147483647 #The maximum number of single circle checks

    for rounds in range(0, NUMGAMES):
        try: #attempts to open the output and input files in that order. In case input fails, we want to have output open
            if outputFile == None: #if this is the first time the program is running
                outputFile = open("HW2OnufriyevOutfile.txt", "w")  #open file
            if fileIn == None: #if this is the first time the program is running
                fileIn = open("HW1infile.txt") #open file
            else:
                fileIn.seek(0) #if this is a subsequent time playing the game, just reset to the start of file
        except Exception as e:
            print("There was a problem loading a file => " + str(e))
            outputFile.write("There was a problem loading a file => " + str(e))
            return

        try:
            numCircles = int(fileIn.readline()) #typecasting can fail in the case that a letter or array is input
            numArrows = int(fileIn.readline())
        except:
            print("Something is wrong with the input...please check and try again.")
            outputFile.write("Something is wrong with the input...please check and try again.")
            return

        #print("Number of circles read: " + str(numCircles))
        #print("Number of arrows read: " + str(numArrows))

        if numCircles < 2 or numCircles > 20 or type(numCircles) != int: #cant play if circle count is 0
            print("You must have at 2 circles and a max of 10.")
            outputFile.write("You must have at 2 circles and a max of 10.")
            return

        if numArrows < numCircles or type(numCircles) != int: #n is the minimum number of arrows to play and be valid
            print("The number of arrow specified do not meet the bare-minimum requirements for a strongly connected graph.")
            outputFile.write("The number of arrow specified do not meet the bare-minimum requirements for a strongly connected graph.")
            return


        circles = getArrows(fileIn, outputFile, numCircles, numArrows) #generates arrows and returns the array of circles

        if circles == None: #in case something went wrong
            return

        sys.setrecursionlimit(2147483647) #sets recusion limit so python doesn't bork itself during path checks with large circle count
        if verifyConnectivity(circles) != 1:
            print("Not a connected graph! Please check your input and try again.")
            outputFile.write("Not a connected graph! Please check your input and try again.")
            return

        gameResults = playTheGame(circles, numCircles, numArrows, outputFile) #total, min, max, circ avg result for game stored in set
        gameTotal = gameResults[0] #total checks in circles of game
        gameMin = gameResults[1] #min num checks in circle of game
        gameMax = gameResults[2] #max num checks in circle of game
        gamePerCircleAverage = gameResults[3] #average checks per circle in game

        avgNumTotalChecks = avgNumTotalChecks + gameTotal #add to total of checks
        avgNumChecksSingleCircle = avgNumChecksSingleCircle + gamePerCircleAverage #add to total average checks

        if maxNumTotalChecks < gameTotal: #if the existing max checks is less than the total from the latest game
            maxNumTotalChecks = gameTotal #this is now the new max
        if minNumTotalChecks > gameTotal: #if the existing min checks is greater than the total from the latest game
            minNumTotalChecks = gameTotal #this is now the new min

        if minNumCircleChecks > gameMin: #if number of min checks in a circle is greater than the latest game
            minNumCircleChecks = gameMin #this is now the min (circle)
        if maxNumCircleChecks < gameMax: #if number of max checks in a circle is less than the latest game
            maxNumCircleChecks = gameMax #this is now the max (circle)


    avgNumTotalChecks = avgNumTotalChecks / NUMGAMES #average is calculated as total/total games
    avgNumChecksSingleCircle = avgNumChecksSingleCircle / NUMGAMES #average of averages is calculated by taking total averages / total games

    finalWriteAndClose(outputFile, fileIn, avgNumTotalChecks, avgNumChecksSingleCircle, #write everything we just calculated to the file at end of game
        maxNumTotalChecks, minNumTotalChecks, maxNumCircleChecks, minNumCircleChecks)


if __name__ == "__main__":
    main()
