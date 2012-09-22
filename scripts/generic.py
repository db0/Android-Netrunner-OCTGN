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

from System.Windows.Forms import Application, Form, Button, Label, DockStyle, AnchorStyles, FormStartPosition

import clr
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import Application, Form, Button, Label, DockStyle, AnchorStyles, FormStartPosition

class OKWindow(Form):
   def __init__(self,InfoTXT):
      newlines = 0
      self.StartPosition = FormStartPosition.CenterScreen
      for char in InfoTXT:
         if char == '\n': newlines += 1
      STRwidth = 200 + (len(InfoTXT) / 4)
      STRheight = 30 + (20 * newlines) + (30 * (STRwidth / 100))
      FORMheight = 130 + STRheight
      FORMwidth = 100 + STRwidth
      self.Text = 'Information'
      self.Height = FORMheight
      self.Width = FORMwidth
      self.AutoSize = True
      
      label = Label()
      label.Text = InfoTXT
      label.Top = 30
      label.Left = 50
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
   if debugVerbosity >= 1: notify("Message: {}".format(Message))
   Application.EnableVisualStyles()
   form = OKWindow(Message)
   form.ShowDialog()
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
