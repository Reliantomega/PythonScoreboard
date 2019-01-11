#!/usr/bin/python

##Created by Grant Alberts
##Please forgive me, but python is a much messier language to write in. This Program will not look nice.
##I Will try to comment the best I can. Thanks for Understanding.
##Written with Python 3.7.0

##Compensate for pythons inability to get its crap together
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import math

#class

class Feild:
    def __init__(self, label, name, row):
        self.value = 0
        self.label = label
        self.name = name
        self.rowPos = row

        ##Making the TKINTER widjects inside the fuction lets see how this goes

        self.labelWidget = Label(top, text=self.label)
        self.entryWidget = Entry(top, width=6)
        self.plusButton = Button(top, text="+", width = 3, command=self.add)
        self.minusButton = Button(top, text = "-", width = 3, command=self.minus)
        self.text = Text(top, height=1, width=3)
        self.clearButton = Button(top, text="Clear", command=self.clear)
        self.updateButton = Button(top, text="update", command = self.manualUpdate)

    #This function is for Updating the Score.
    def updateScore(self):
        self.changeText(self.value)

    #This function is mostly isn't used, but the time it is, it is extremely useful
    def checkZero(self):
        if self.value <= 0:
            return 1

    #This function is used for checking is the balls, strikes, or outs. It's not very elegant, and I nee to find a better solution
    def checkBSO(self):
        if self.name == "balls":
            if self.value >= 4:
                return 1
            else:
                return 0
        elif self.name == "strikes":
            if self.value >= 3:
                return 1
            else:
                return 0
        elif self.name == "outs":
            if self.value >=3:
                return 1
            else:
                return 0
        else:
            return 0
    #This function adds one to the Value. its called by the Add button
    def add(self):
        check = self.checkBSO()
        if check != 1:
            self.value += 1
            writeFile(self.name, str(self.value))
            self.updateScore()

    #This function subtracts one to the Value. It's called by the Subtract button
    def minus(self):
        zero = self.checkZero()
        if zero != 1:
            self.value -=1
            self.updateScore()
            writeFile(self.name, str(self.value))

    #This function clears the score. It is called by the Clear button and the Clear all button.
    def clear(self):
        self.value = 0
        writeFile(self.name, str(self.value))
        self.updateScore()

    #This function is for manually updating the Value. It first trys to convert to an int, but otherwise writes as a string
    def manualUpdate(self):
        val = self.entryWidget.get()

        try:
            self.value = int(val)
        except Exception as e:
            self.value = val

        self.changeText(self.value)
        writeFile(self.name, str(self.value))
        self.entryWidget.delete(0, END)

    #This changes the text widget, but doesn't change the File. This is beause I'm lazy
    def changeText(self, value):
        self.text.delete('1.0', END)
        self.text.insert(END, value)

    #This function is pretty big one. It places all the Widgets created earlier
    def placeWids(self):
        self.labelWidget.grid(column=0, row=self.rowPos)
        self.text.grid(column=1, row=self.rowPos)
        self.entryWidget.grid(column=2, row=self.rowPos)
        self.plusButton.grid(column = 3, row=self.rowPos)
        self.minusButton.grid(column = 4, row = self.rowPos)
        self.clearButton.grid(column = 5, row = self.rowPos)
        self.updateButton.grid(column = 6, row = self.rowPos)

##Class for the Drop Down Menus.

class DropDown:
    def __init__(self, presets):
        self.currentBoard = "baseball"
        self.presets = presets
        self.optionVar = StringVar()
        self.optionList = ["Baseball/Softball", "Volleyball", "Wrestling", "Soccer"]
        self.optionVar.set(self.optionList[0])
        self.dropDown = OptionMenu(top, self.optionVar, *self.optionList, command=self.changeBoards)
        self.dropDown.grid(column = 0, row = 0)
##This function changes the Board to the selected preset from the drop down menu.
    def changeBoards(self, boardPreset):
        if boardPreset == "Baseball/Softball":
            clearGrid(self.presets[self.currentBoard])
            self.currentBoard = "baseball"
            buildBoard(self.presets["baseball"])
        elif boardPreset == "Wrestling":
            clearGrid(self.presets[self.currentBoard])
            self.currentBoard = "wrestling"
            buildBoard(self.presets["wrestling"])
        elif boardPreset == "Volleyball":
            clearGrid(self.presets[self.currentBoard])
            self.currentBoard = "volleyball"
            buildBoard(self.presets["volleyball"])
        elif boardPreset == "Soccer":
            clearGrid(self.presets[self.currentBoard])
            self.currentBoard = "soccer"
            buildBoard(self.presets["soccer"])
        else:
            pass
        clearScores()

#main container
top = Tk()
top.title("Score Board")

##Dictonary of Presets
presets = {
    "baseball": [Feild("Home Score", "homeScore", 1), \
    Feild("Visitor Score", "visScore", 2), \
    Feild("Period", "period", 3), \
    Feild("Ball", "balls", 4), \
    Feild("Strikes", "strikes", 5), Feild("Outs", "outs", 6)], \
    "volleyball":[Feild("Home Score", "homeScore", 1), \
    Feild("Visitor Score", "visScore", 2), Feild("Period", "period", 3), \
    Feild("Home Fouls", "homeFouls", 4), \
    Feild("Visitor Fouls", "visFouls", 5)], \
    "wrestling": [Feild("Home Score", "homeScore", 1), \
    Feild("Visitor Score", "visScore", 2), \
    Feild("Period", "period", 3), \
    Feild("Home Fouls", "homeFouls", 4), \
    Feild("Visitor Fouls", "visFouls", 5)], \
    "soccer": [Feild("Home Score", "homeScore", 1), \
    Feild("Visitor Score", "visScore", 2), \
    Feild("Period", "period", 3)]
 }

##Helper Funcitons

#This writes out to a file
def writeFile(name, value):
    fileObj = open(name +".txt", "w")
    fileObj.write(value)
    fileObj.close()

#This builds the Score Board, using the preset array that is defined earlier.
def buildBoard(preset):
    for ob in preset:
        ob.updateScore()
        ob.placeWids()

#This function is probably unneseciary. It calls the the Exit Function to end the program. Ut was the only way for me to not
#get a popup.
def exitFun():
    exit()

#This Function clears all scores, called by the clear all button.
def clearScores():
    for ob in presets[dropMenu.currentBoard]:
        ob.clear()

#This clears all the elements in the grid. Its pretty nifty
def clearGrid(set):
    for items in top.grid_slaves():
        if int(items.grid_info()["row"]) <= len(set) and int(items.grid_info()["row"]) >= 1:
            items.grid_forget()

#This changes the Board from one preset to another
dropMenu = DropDown(presets)
buildBoard(presets[dropMenu.currentBoard])


#exit button
exitButton = Button(top, command=exitFun, text = "Exit")
exitButton.grid(column = 0, row = 9)

#Clear Scores buttons
clearButton = Button(top, command= clearScores, text = "Clear all scores")
clearButton.grid(column = 1, row=9)

##TKinter's mainloop thing. Not quite sure what mainloop is and what it does but it needs it.
top.mainloop();
