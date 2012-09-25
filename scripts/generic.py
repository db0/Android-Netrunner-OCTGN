    # Python Scripts for the Android:Netrunner LCG definition for OCTGN
    # Copyright (C) 2012  Konstantine Thoukydides

    # This python script is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this script.  If not, see <http://www.gnu.org/licenses/>.

###==================================================File Contents==================================================###
# This file contains generic game-agnostic scripts. They can be ported as-is in any kind of game.
# * [Generic] funcrion do basic stuff like convert a sting into a number or store your card's properties.
# * [Custom Windows Forms] are functions which create custom-crafted WinForms on the table. The MultipleChoice form is heavily commented.
# * [Card Placement] Are dealing with placing or figuring where to place cards on the table
###=================================================================================================================###

import re

playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is

### Variables that hold the properties of a card.
Stored_Type = {}
Stored_Keywords = {}
Stored_Cost = {}
Stored_AutoActions = {}
Stored_AutoScripts = {}

#---------------------------------------------------------------------------
# Custom Windows Forms
#---------------------------------------------------------------------------

import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import Application, Form, Button, Label, DockStyle, AnchorStyles, FormStartPosition, RadioButton, Panel
from System.Drawing import Color

def calcStringLabelSize(STRING): 
# A function which returns a slowly expansing size for a label. The more characters, the more the width expands to allow more characters on the same line.
   newlines = 0
   for char in STRING:
      if char == '\n': newlines += 1
   STRINGwidth = 200 + (len(STRING) / 4)
   STRINGheight = 30 + (20 * newlines) + (30 * (STRINGwidth / 100))
   return (STRINGwidth, STRINGheight)
   
def formStringEscape(STRING): # A function to escape some characters that are not otherwise displayed by WinForms, like amperasands '&'
   slist = list(STRING)
   escapedString = ''
   for s in slist:
      if s == '&': char = '&&'
      else: char = s
      escapedString += char
   return escapedString

class OKWindow(Form): # This is a WinForm which creates a simple window, with some text and an OK button to close it.
   def __init__(self,InfoTXT):
      self.StartPosition = FormStartPosition.CenterScreen
      (STRwidth, STRheight) = calcStringLabelSize(InfoTXT)
      FORMheight = 130 + STRheight
      FORMwidth = 100 + STRwidth
      self.Text = 'Information'
      self.Height = FORMheight
      self.Width = FORMwidth
      self.AutoSize = True
      self.MinimizeBox = False
      self.MaximizeBox = False
      self.TopMost = True
      self.BringToFront()
      
      label = Label()
      label.Text = formStringEscape(InfoTXT)
      label.Top = 30
      label.Left = 30
      label.Height = STRheight
      label.Width = STRwidth
      #label.AutoSize = True #Well, that's shit.

      button = Button()
      button.Text = "OK"
      button.Width = 100
      button.Top = FORMheight - 80
      button.Left = (FORMwidth / 2) - 50
      button.Anchor = AnchorStyles.Bottom

      button.Click += self.buttonPressed

      self.Controls.Add(label)
      self.Controls.Add(button)

   def buttonPressed(self, sender, args):
      self.Close()

def information(Message):
   if debugVerbosity >= 1: notify(">>> information() with message: {}".format(Message))
   if Automations['WinForms']:
      Application.EnableVisualStyles()
      form = OKWindow(Message)
      form.ShowDialog()
   else: 
      confirm(Message)
   
   
class RadioWindow(Form):
 
   def __init__(self, BoxTitle, BoxOptions):
      self.Text = "Select an Option"
      self.index = 0
      self.confirmValue = None
      self.MinimizeBox = False
      self.MaximizeBox = False
      self.StartPosition = FormStartPosition.CenterScreen
      self.AutoSize = True
      self.TopMost = True
      self.BringToFront()
      
      (STRwidth, STRheight) = calcStringLabelSize(BoxTitle)

      labelPanel = Panel()
      labelPanel.Dock = DockStyle.Top
      labelPanel.Height = STRheight
      labelPanel.Width = STRwidth
      labelPanel.AutoSize = True
      #labelPanel.BackColor = Color.LightSlateGray # Debug
      
      radioPanel = Panel()
      radioPanel.Dock = DockStyle.Top
      radioPanel.AutoSize = True
      #radioPanel.BackColor = Color.LightSalmon # Debug

      self.Controls.Add(radioPanel) # Don't know why, but the lower panel needs to be placed first.
      self.Controls.Add(labelPanel)

      label = Label()
      label.Text = formStringEscape(BoxTitle)
      label.Top = 30
      label.Left = 25
      label.Height = STRheight
      label.Width = STRwidth
      labelPanel.Controls.Add(label)
      
      radioPush = Panel() # Just to put the radio buttons a bit more to the middle
      radioPush.Left = 30
      radioPanel.Controls.Add(radioPush)
      
      for option in BoxOptions:
         btn = RadioButton()
         btn.Name = str(self.index)
         self.index = self.index + 1
         btn.Text = formStringEscape(option)
         btn.Dock = DockStyle.Top
         btn.Checked = False
         btn.CheckedChanged += self.checkedChanged
         radioPush.Controls.Add(btn)
         btn.BringToFront()

      button = Button()
      button.Text = "Confirm"
      button.Width = 100
      button.Dock = DockStyle.Bottom
      button.Click += self.buttonPressed
      self.Controls.Add(button)
 
   def buttonPressed(self, sender, args):
      self.Close()
 
   def checkedChanged(self, sender, args):
      self.confirmValue = int(sender.Name)
 
   def getIndex(self):
      return self.confirmValue
 
def radioChoice(title, options):
   if debugVerbosity >= 1: notify(">>> radioChoice()".format(Message))
   if Automations['WinForms']:
      Application.EnableVisualStyles()
      form = RadioWindow(title, options)
      form.ShowDialog()
      choice = form.getIndex()
   else:
      concatTXT = title + '\n\n'
      for iter in range(len(options)):
         concatTXT += '{}:--> {}\n'.format(iter,options[iter])
      choice = askInteger(concatTXT,0)
   if debugVerbosity >= 3: notify("<<< radioChoice()".format(Message))
   return choice
 
   
class MultiChoiceWindow(Form):
 # This is a windows form which creates a multiple choice form, with a button for each choice. 
 # The player can select more than one, and they are then returned as a list of integers
   def __init__(self, FormTitle, FormChoices,CPType): # We initialize our form, expecting 3 variables. 
                                                      # FormTitle is the title of the window itself
                                                      # FormChoices is a list of strings which we use for the names of the buttons
                                                      # CPType is combined with FormTitle to give a more thematic window name.
      self.Text = CPType # We just store the variable locally
      self.index = 0 # We use this variable to set a number to each button
      self.MinimizeBox = False # We hide the minimize button
      self.MaximizeBox = False # We hide the maximize button
      self.StartPosition = FormStartPosition.CenterScreen # We start the form at the center of the player's screen
      self.AutoSize = True # We allow the form to expand in size depending on its contents
      self.BringToFront() # Not sure. Brine put that here >_<
      self.TopMost = True # We make sure our new form will be on the top of all other windows. If we didn't have this here, fullscreen OCTGN would hide the form.
      self.origTitle = formStringEscape(FormTitle) # Used when modifying the label from a button
      
      self.confirmValue = [] # This is our list which will hold the choices of the players as integers
      
      (STRwidth, STRheight) = calcStringLabelSize(FormTitle) # We dynamically calculate the size of the text label to be displayed as info to the player.
      labelPanel = Panel() # We create a new panel (e.g. container) to store the label.
      labelPanel.Dock = DockStyle.Top # We Dock the label's container on the top of the form window
      labelPanel.Height = STRheight # We setup the dynamic size
      labelPanel.Width = STRwidth
      labelPanel.AutoSize = True # We allow the panel to expand dynamically according to the size of the label
      #labelPanel.BackColor = Color.LightSlateGray # Debug
      
      choicePanel = Panel() # We create a panel to hold our buttons
      choicePanel.Dock = DockStyle.Top # We dock this below the label panel
      choicePanel.AutoSize = True # We allow it to expand in size dynamically
      #radioPanel.BackColor = Color.LightSalmon # Debug

      self.Controls.Add(choicePanel) # Don't know why, but the lower panel needs to be placed first.
      self.Controls.Add(labelPanel)

      self.label = Label() # We create a label object which will hold the multiple choice description text
      self.label.Text = formStringEscape(FormTitle) # We escape any strings that WinForms doesn't like, like ampersand and store it in the label
      self.label.Top = 30 # We place the label 30 pixels from the top size of its container panel, and 50 pixels from the left.
      self.label.Left = 50
      self.label.Height = STRheight # We set its dynamic size
      self.label.Width = STRwidth
      labelPanel.Controls.Add(self.label) # We add the label to its container
      
      choicePush = Panel() # An extra secondary container for the buttons, that is not docked, to allow us to slightly change its positioning
      choicePush.Left = 50 # We move it 50 pixels to the left
      choicePush.AutoSize = True # We allow it to expand dynamically
      choicePanel.Controls.Add(choicePush) # We add it to its parent container
      
      for option in FormChoices: # We dynamically add as many buttons as we have options
         btn = Button() # We initialize a button object
         btn.Name = str(self.index) # We name the button equal to its numeric value, plus its effect.
         btn.Text = str(self.index) + ':--> ' + formStringEscape(option)
         self.index = self.index + 1 # The internal of the button is also the choice that will be put in our list of integers. 
         btn.Dock = DockStyle.Top # We dock the buttons one below the other, to the top of their container (choicePush)
         btn.AutoSize = True # Doesn't seem to do anything
         btn.Height = 60 # We make them nice and big
         btn.Click += self.choiceMade # This triggers the function which records each choice into the confirmValue[] list
         choicePush.Controls.Add(btn) # We add each button to its panel
         btn.BringToFront() # Add new buttons to the bottom of existing ones (Otherwise the buttons would be placed in reverse numerical order)

      finishButton = Button() # We add a button to Finish the selection
      finishButton.Text = "Finish Selection"
      finishButton.Width = 100
      finishButton.Dock = DockStyle.Bottom # We dock it to the bottom of the form.
      #button.Anchor = AnchorStyles.Bottom
      finishButton.Click += self.finishPressed # We call its function
      self.Controls.Add(finishButton) # We add the button to the form
 
      cancelButton = Button() # We add a bytton to Cancel the selection
      cancelButton.Text = "Cancel"
      cancelButton.Width = 100
      cancelButton.Dock = DockStyle.Bottom
      #button.Anchor = AnchorStyles.Bottom
      cancelButton.Click += self.cancelPressed
      self.Controls.Add(cancelButton)

   def finishPressed(self, sender, args): # The function called from the finishButton.
      self.Close()  # It just closes the form

   def cancelPressed(self, sender, args): # The function called from the cancelButton
      self.confirmValue = 'ABORT' # It replaces the choice list with an ABORT message which is parsed by the calling function
      self.Close() # And then closes the form
 
   def choiceMade(self, sender, args): # The function called when pressing one of the choice buttons
      self.confirmValue.append(int(sender.Name)) # We append the button's name to the existing choices list
      self.label.Text = self.origTitle + "\n\nYour current choices are:\n{}".format(self.confirmValue) # We display what choices we've made until now to the player.
 
   def getIndex(self): # The function called after the form is closed, to grab its choices list
      return self.confirmValue  

def multiChoice(title, options,card): # This displays a choice where the player can select more than one ability to trigger serially one after the other
   if debugVerbosity >= 1: notify(">>> multiChoice()".format(Message))
   if Automations['WinForms']: # If the player has not disabled the custom WinForms, we use those
      Application.EnableVisualStyles() # To make the window look like all other windows in the user's system
      if card.Type == 'ICE': CPType = 'Intrusion Countermeasures Electronics'  # Just some nice fluff
      elif re.search(r'Icebreaker', card.Keywords): CPType = 'ICEbreaker GUI'
      elif card.Type == 'Hardware': CPType = 'Dashboard'
      else: CPType = 'Control Panel'
      form = MultiChoiceWindow(title, options, CPType) # We create an object called "form" which contains an instance of the MultiChoice windows form.
      form.ShowDialog() # We bring the form to the front to allow the user to make their choices
      choices = form.getIndex() # Once the form is closed, we check an internal variable within the form object to grab what choices they made
   else: # If the user has disabled the windows forms, we use instead the OCTGN built-in askInteger function
      concatTXT = title + "\n\n(Tip: You can put multiple abilities one after the the other (e.g. '110'). Max 9 at once)\n\n" # We prepare the text of the window with a concat string
      for iter in range(len(options)): # We populate the concat string with the options
         concatTXT += '{}:--> {}\n'.format(iter,options[iter])
      choicesInteger = askInteger(concatTXT,0) # We now ask the user to put in an integer.
      if not choicesInteger: choices = 'ABORT' # If the user just close the window, abort.
      else: 
         choices = list(str(choicesInteger)) # We convert our number into a list of numeric chars
         for iter in range(len(choices)): choices[iter] = int(choices[iter]) # we convert our list of chars into a list of integers      
   if debugVerbosity >= 3: notify("<<< multiChoice() with list: {}".format(Message,choices))
   return choices # We finally return a list of integers to the previous function. Those will in turn be iterated one-by-one serially.
      
#---------------------------------------------------------------------------
# Generic
#---------------------------------------------------------------------------

def num (s):
   #if debugVerbosity >= 1: notify(">>> num(){}".format(extraASDebug())) #Debug
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def chooseSide(): # Called from many functions to check if the player has chosen a side for this game.
   if debugVerbosity >= 1: notify(">>> chooseSide(){}".format(extraASDebug())) #Debug
   mute()
   global playerside, playeraxis
   if playerside == None:  # Has the player selected a side yet? If not, then...
     if me.hasInvertedTable():
        playeraxis = Yaxis
        playerside = -1
     else:
        playeraxis = Yaxis
        playerside = 1
   if debugVerbosity >= 4: notify("<<< chooseSide(){}".format(extraASDebug())) #Debug

def displaymatch(match):
   if match is None:
      return None
   return '<Match: {}, groups={}>'.format(match.group(), match.groups())
   
def storeProperties(card): # Function that grabs a cards important properties and puts them in a dictionary
   mute()
   coverExists = False
   if debugVerbosity >= 1: notify(">>> storeProperties(){}".format(extraASDebug())) #Debug
   global Stored_Cost, Stored_Type, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts, identName
   cFaceD = False
   if card.name == 'Card' and Stored_Type.get(card,'?') == '?':
      if not card.isFaceUp and card.group == table:
         if card.controller != me: # If it's not our card, then we cover it up shortly while grabbing its properties
            x,y = card.position
            cover = table.create("ac3a3d5d-7e3a-4742-b9b2-7f72596d9c1b",x,y,1,False)
            cover.moveToTable(x,y,False)
            if card.orientation == Rot90: cover.orientation = Rot90
            coverExists = True
         card.isFaceUp = True
         cFaceD = True
         loopcount = 0
         while card.name == 'Card':
            rnd(1,10)
            loopcount += 1
            if loopcount == 5:
               whisper(":::Error::: Card properties can't be grabbed. Aborting!")
               break
   if Stored_Type.get(card,'?') == '?' or (Stored_Type.get(card,'?') != card.Type and card.Type != '?'):
      if debugVerbosity >= 3: notify("### {} not stored. Storing...".format(card))
      Stored_Cost[card] = card.Cost
      Stored_Type[card] = card.Type
      Stored_Keywords[card] = getKeywords(card)
      Stored_AutoActions[card] = CardsAA.get(card.model,'')
      Stored_AutoScripts[card] = CardsAS.get(card.model,'')
      if card.Type == 'Identity': identName = card.name
   if cFaceD: card.isFaceUp = False
   if coverExists: 
      rnd(1,10) # To give time to the card facedown automation to complete.
      cover.moveTo(shared.exile) # now destorying cover card
   if debugVerbosity >= 3: notify("<<< storeProperties()")

def fetchProperty(card, property): 
   mute()
   if debugVerbosity >= 1: notify(">>> fetchProperty(){}".format(extraASDebug())) #Debug
   cFaceD = False
   if card.properties[property] == '?':
      if not card.isFaceUp: 
         card.isFaceUp = True
         cFaceD = True
      loopChk(card,'Type')
   if cFaceD: card.isFaceUp = False
   if debugVerbosity >= 3: notify("<<< fetchProperty() by returning: {}".format(card.properties[property]))
   return card.properties[property]

def loopChk(card,property = 'Type'):
   if debugVerbosity >= 1: notify(">>> loopChk(){}".format(extraASDebug())) #Debug
   loopcount = 0
   while card.properties[property] == '?':
      rnd(1,10)
      loopcount += 1
      if loopcount == 5:
         whisper(":::Error::: Card property can't be grabbed. Aborting!")
         return 'ABORT'
   if debugVerbosity >= 4: notify("<<< loopChk()") #Debug
   return 'OK'         
   
def sortPriority(cardList):
   if debugVerbosity >= 1: notify(">>> sortPriority()") #Debug
   priority1 = []
   priority2 = []
   priority3 = []
   sortedList = []
   for card in cardList:
      if card.highlight == PriorityColor: # If a card is clearly highlighted for priority, we use its counters first.
         priority1.append(card)
      elif card.targetedBy and card.targetedBy == me: # If a card it targeted, we give it secondary priority in losing its counters.
         priority2.append(card)   
      else: # If a card is neither of the above, then the order is defined on how they were put on the table.
         priority3.append(card) 
   sortedList.extend(priority1)
   sortedList.extend(priority2)
   sortedList.extend(priority3)
   if debugVerbosity >= 3: 
      tlist = []
      for sortTarget in sortedList: tlist.append(sortTarget.name) # Debug   
      notify("<<< sortPriority() returning {}".format(tlist)) #Debug
   return sortedList
   
def oncePerTurn(card, x = 0, y = 0, silent = False, act = 'manual'):
   if debugVerbosity >= 1: notify(">>> oncePerTurn(){}".format(extraASDebug())) #Debug
   mute()
   if card.orientation == Rot90:
      if act != 'manual': return 'ABORT' # If the player is not activating an effect manually, we always fail silently. So as not to spam the confirm.
      elif not confirm("The once-per-turn ability of {} has already been used this turn\nBypass restriction?.".format(card.name)): return 'ABORT'
      else: 
         if not silent: notify('{} activates the once-per-turn ability of {} another time'.format(me, card))
   else:
      if not silent: notify('{} activates the once-per-turn ability of {}'.format(me, card))
   card.orientation = Rot90

#---------------------------------------------------------------------------
# Card Placement functions
#---------------------------------------------------------------------------

def cwidth(card, divisor = 10):
   #if debugVerbosity >= 1: notify(">>> cwidth(){}".format(extraASDebug())) #Debug
# This function is used to always return the width of the card plus an offset that is based on the percentage of the width of the card used.
# The smaller the number given, the less the card is divided into pieces and thus the larger the offset added.
# For example if a card is 80px wide, a divisor of 4 will means that we will offset the card's size by 80/4 = 20.
# In other words, we will return 1 + 1/4 of the card width. 
# Thus, no matter what the size of the table and cards becomes, the distances used will be relatively the same.
# The default is to return an offset equal to 1/10 of the card width. A divisor of 0 means no offset.
   if divisor == 0: offset = 0
   else: offset = card.width() / divisor
   return (card.width() + offset)

def cheight(card, divisor = 10):
   #if debugVerbosity >= 1: notify(">>> cheight(){}".format(extraASDebug())) #Debug
   if divisor == 0: offset = 0
   else: offset = card.height() / divisor
   return (card.height() + offset)

def yaxisMove(card):
   #if debugVerbosity >= 1: notify(">>> yaxisMove(){}".format(extraASDebug())) #Debug
# Variable to move the cards played by player 2 on a 2-sided table, more towards their own side. 
# Player's 2 axis will fall one extra card length towards their side.
# This is because of bug #146 (https://github.com/kellyelton/OCTGN/issues/146)
   if me.hasInvertedTable(): cardmove = cheight(card)
   else: cardmove = cardmove = 0
   return cardmove
