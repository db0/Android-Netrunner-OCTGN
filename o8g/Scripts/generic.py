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

try:
    import os
    if os.environ['RUNNING_TEST_SUITE'] == 'TRUE':
        from meta import Automations
        Form = object
except ImportError:
    pass

playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is

### Variables that hold the properties of a card.
Stored_Name = {}
Stored_Type = {}
Stored_Keywords = {}
Stored_Cost = {}
Stored_AutoActions = {}
Stored_AutoScripts = {}

### Subscriber lists.

supercharged = []
customized = []

#---------------------------------------------------------------------------
# Custom Windows Forms
#---------------------------------------------------------------------------

try:
   import clr
   clr.AddReference("System.Drawing")
   clr.AddReference("System.Windows.Forms")

   from System.Windows.Forms import *
   from System.Drawing import Color
except:
   Automations['WinForms'] = False
   
def calcStringLabelSize(STRING): 
# A function which returns a slowly expansing size for a label. The more characters, the more the width expands to allow more characters on the same line.
   newlines = 0
   for char in STRING:
      if char == '\n': newlines += 1
   STRINGwidth = 200 + (len(STRING) / 4)
   STRINGheight = 30 + ((20 - newlines) * newlines) + (30 * (STRINGwidth / 100))
   return (STRINGwidth, STRINGheight)

def calcStringButtonHeight(STRING): 
# A function which returns a slowly expansing size for a label. The more characters, the more the width expands to allow more characters on the same line.
   newlines = 0
   for char in STRING:
      if char == '\n': newlines += 1
   STRINGheight = 30 + (8 * newlines) + (7 * (len(STRING) / 20))
   return STRINGheight
   
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
      
      labelPanel = Panel()
      labelPanel.Dock = DockStyle.Top
      labelPanel.AutoSize = True
      labelPanel.BackColor = Color.White

      self.timer_tries = 0
      self.timer = Timer()
      self.timer.Interval = 200
      self.timer.Tick += self.onTick
      self.timer.Start()
      
      label = Label()
      label.Text = formStringEscape(InfoTXT)
      if debugVerbosity >= 2: label.Text += '\n\nTopMost: ' + str(self.TopMost) # Debug
      label.Top = 30
      label.Left = (self.ClientSize.Width - STRwidth) / 2
      label.Height = STRheight
      label.Width = STRwidth
      labelPanel.Controls.Add(label)
      #label.AutoSize = True #Well, that's shit.

      button = Button()
      button.Text = "OK"
      button.Width = 100
      button.Top = FORMheight - 80
      button.Left = (FORMwidth - 100) / 2
      button.Anchor = AnchorStyles.Bottom

      button.Click += self.buttonPressed

      self.Controls.Add(labelPanel)
      self.Controls.Add(button)

   def buttonPressed(self, sender, args):
      self.timer.Stop()
      self.Close()

   def onTick(self, sender, event):
      if self.timer_tries < 3:
         self.TopMost = False
         self.Focus()
         self.Activate()
         self.TopMost = True
         self.timer_tries += 1
            
def information(Message):
   debugNotify(">>> information() with message: {}".format(Message))
   if Automations['WinForms']:
      Application.EnableVisualStyles()
      form = OKWindow(Message)
      form.BringToFront()
      form.ShowDialog()
   else: 
      confirm(Message)
   
   
class SingleChoiceWindow(Form):
 
   def __init__(self, BoxTitle, BoxOptions, type, defaultOption, pages = 0, cancelButtonBool = True, cancelName = 'Cancel'):
      self.Text = "Select an Option"
      self.index = 0
      self.confirmValue = None
      self.MinimizeBox = False
      self.MaximizeBox = False
      self.StartPosition = FormStartPosition.CenterScreen
      self.AutoSize = True
      self.TopMost = True
      
      (STRwidth, STRheight) = calcStringLabelSize(BoxTitle)
      self.Width = STRwidth + 50

      self.timer_tries = 0
      self.timer = Timer()
      self.timer.Interval = 200
      self.timer.Tick += self.onTick
      self.timer.Start()
      
      labelPanel = Panel()
      labelPanel.Dock = DockStyle.Top
      labelPanel.AutoSize = True
      labelPanel.BackColor = Color.White
      
      separatorPanel = Panel()
      separatorPanel.Dock = DockStyle.Top
      separatorPanel.Height = 20
      
      choicePanel = Panel()
      choicePanel.Dock = DockStyle.Top
      choicePanel.AutoSize = True

      self.Controls.Add(labelPanel)
      labelPanel.BringToFront()
      self.Controls.Add(separatorPanel)
      separatorPanel.BringToFront()
      self.Controls.Add(choicePanel)
      choicePanel.BringToFront()

      label = Label()
      label.Text = formStringEscape(BoxTitle)
      if debugVerbosity >= 2: label.Text += '\n\nTopMost: ' + str(self.TopMost) # Debug
      label.Top = 30
      label.Left = (self.ClientSize.Width - STRwidth) / 2
      label.Height = STRheight
      label.Width = STRwidth
      labelPanel.Controls.Add(label)
      
      bufferPanel = Panel() # Just to put the radio buttons a bit more to the middle
      bufferPanel.Left = (self.ClientSize.Width - bufferPanel.Width) / 2
      bufferPanel.AutoSize = True
      choicePanel.Controls.Add(bufferPanel)
            
      for option in BoxOptions:
         if type == 'radio':
            btn = RadioButton()
            if defaultOption == self.index: btn.Checked = True
            else: btn.Checked = False
            btn.CheckedChanged += self.checkedChanged
         else: 
            btn = Button()
            btn.Height = calcStringButtonHeight(formStringEscape(option))
            btn.Click += self.choiceMade
         btn.Name = str(self.index)
         self.index = self.index + 1
         btn.Text = formStringEscape(option)
         btn.Dock = DockStyle.Top
         bufferPanel.Controls.Add(btn)
         btn.BringToFront()

      button = Button()
      button.Text = "Confirm"
      button.Width = 100
      button.Dock = DockStyle.Bottom
      button.Click += self.buttonPressed
      if type == 'radio': self.Controls.Add(button) # We only add the "Confirm" button on a radio menu.
 
      buttonNext = Button()
      buttonNext.Text = "Next Page"
      buttonNext.Width = 100
      buttonNext.Dock = DockStyle.Bottom
      buttonNext.Click += self.nextPage
      if pages > 1: self.Controls.Add(buttonNext) # We only add the "Confirm" button on a radio menu.

      cancelButton = Button() # We add a bytton to Cancel the selection
      cancelButton.Text = cancelName # We can rename the cancel button if we want to.
      cancelButton.Width = 100
      cancelButton.Dock = DockStyle.Bottom
      #button.Anchor = AnchorStyles.Bottom
      cancelButton.Click += self.cancelPressed
      if cancelButtonBool: self.Controls.Add(cancelButton)
      
   def buttonPressed(self, sender, args):
      self.timer.Stop()
      self.Close()

   def nextPage(self, sender, args):
      self.confirmValue = "Next Page"
      self.timer.Stop()
      self.Close()
 
   def cancelPressed(self, sender, args): # The function called from the cancelButton
      self.confirmValue = None # It replaces the choice list with an ABORT message which is parsed by the calling function
      self.timer.Stop()
      self.Close() # And then closes the form
      
   def checkedChanged(self, sender, args):
      self.confirmValue = sender.Name
      
   def choiceMade(self, sender, args):
      self.confirmValue = sender.Name
      self.timer.Stop()
      self.Close()
      
   def getIndex(self):
      return self.confirmValue

   def onTick(self, sender, event):
      if self.timer_tries < 3:
         self.TopMost = False
         self.Focus()
         self.Activate()
         self.TopMost = True
         self.timer_tries += 1

def SingleChoice(title, options, type = 'button', default = 0, cancelButton = True, cancelName = 'Cancel'):
   debugNotify(">>> SingleChoice()".format(title))
   if Automations['WinForms']:
      optChunks=[options[x:x+7] for x in xrange(0, len(options), 7)]
      optCurrent = 0
      choice = "New"
      while choice == "New" or choice == "Next Page" or (choice == None and not cancelButton):
         Application.EnableVisualStyles()
         form = SingleChoiceWindow(title, optChunks[optCurrent], type, default, pages = len(optChunks), cancelButtonBool = cancelButton, cancelName = cancelName)
         form.BringToFront()
         form.ShowDialog()
         choice = form.getIndex()
         debugNotify("choice is: {}".format(choice), 2)
         if choice == "Next Page": 
            debugNotify("Going to next page", 3)
            optCurrent += 1
            if optCurrent >= len(optChunks): optCurrent = 0
         elif choice != None: 
            choice = num(form.getIndex()) + (optCurrent * 7) # if the choice is not a next page, then we convert it to an integer and give that back, adding 8 per number of page passed
   else:
      concatTXT = title + '\n\n'
      for iter in range(len(options)):
         concatTXT += '{}:--> {}\n'.format(iter,options[iter])
      choice = askInteger(concatTXT,0)
   debugNotify("<<< SingleChoice() with return {}".format(choice), 3)
   return choice

   
class MultiChoiceWindow(Form):
 # This is a windows form which creates a multiple choice form, with a button for each choice. 
 # The player can select more than one, and they are then returned as a list of integers
   def __init__(self, FormTitle, FormChoices,CPType, pages = 0,currPage = 0, existingChoices = []): # We initialize our form, expecting 3 variables. 
                                                      # FormTitle is the title of the window itself
                                                      # FormChoices is a list of strings which we use for the names of the buttons
                                                      # CPType is combined with FormTitle to give a more thematic window name.
      self.Text = CPType # We just store the variable locally
      self.index = 0 # We use this variable to set a number to each button
      self.MinimizeBox = False # We hide the minimize button
      self.MaximizeBox = False # We hide the maximize button
      self.StartPosition = FormStartPosition.CenterScreen # We start the form at the center of the player's screen
      self.AutoSize = True # We allow the form to expand in size depending on its contents
      self.TopMost = True # We make sure our new form will be on the top of all other windows. If we didn't have this here, fullscreen OCTGN would hide the form.
      self.origTitle = formStringEscape(FormTitle) # Used when modifying the label from a button
      
      self.confirmValue = existingChoices
      debugNotify("existingChoices = {}".format(self.confirmValue))
      self.nextPageBool = False  # self.nextPageBool is just remembering if the player has just flipped the page.
      self.currPage = currPage
      
      self.timer_tries = 0 # Ugly hack to fix the form sometimes not staying on top of OCTGN
      self.timer = Timer() # Create a timer object
      self.timer.Interval = 200 # Speed is at one 'tick' per 0.2s
      self.timer.Tick += self.onTick # Activate the event function on each tick
      self.timer.Start() # Start the timer.
      
      (STRwidth, STRheight) = calcStringLabelSize(FormTitle) # We dynamically calculate the size of the text label to be displayed as info to the player.
      labelPanel = Panel() # We create a new panel (e.g. container) to store the label.
      labelPanel.Dock = DockStyle.Top # We Dock the label's container on the top of the form window
      labelPanel.Height = STRheight # We setup the dynamic size
      labelPanel.Width = STRwidth
      labelPanel.AutoSize = True # We allow the panel to expand dynamically according to the size of the label
      labelPanel.BackColor = Color.White
      
      choicePanel = Panel() # We create a panel to hold our buttons
      choicePanel.Dock = DockStyle.Top # We dock this below the label panel
      choicePanel.AutoSize = True # We allow it to expand in size dynamically
      #radioPanel.BackColor = Color.LightSalmon # Debug

      separatorPanel = Panel() # We create a panel to separate the labels from the buttons
      separatorPanel.Dock = DockStyle.Top # It's going to be docked to the middle of both
      separatorPanel.Height = 20 # Only 20 pixels high

      self.Controls.Add(labelPanel) # The panels need to be put in the form one by one
      labelPanel.BringToFront() # This basically tells that the last panel we added should go below all the others that are already there.
      self.Controls.Add(separatorPanel)
      separatorPanel.BringToFront() 
      self.Controls.Add(choicePanel) 
      choicePanel.BringToFront() 

      self.label = Label() # We create a label object which will hold the multiple choice description text
      #if len(self.confirmValue): self.label.Text = formStringEscape(FormTitle) + "\n\nYour current choices are:\n{}".format(self.confirmValue) # We display what choices we've made until now to the player.
      self.label.Text = formStringEscape(FormTitle) # We escape any strings that WinForms doesn't like, like ampersand and store it in the label
      if debugVerbosity >= 2: self.label.Text += '\n\nTopMost: ' + str(self.TopMost) # Debug
      self.label.Top = 30 # We place the label 30 pixels from the top size of its container panel, and 50 pixels from the left.
      self.label.Left = 50
      self.label.Height = STRheight # We set its dynamic size
      self.label.Width = STRwidth
      labelPanel.Controls.Add(self.label) # We add the label to its container
      
      choicePush = Panel() # An extra secondary container for the buttons, that is not docked, to allow us to slightly change its positioning
      choicePush.Left = (self.ClientSize.Width - choicePush.Width) / 2 # We move it 50 pixels to the left
      choicePush.AutoSize = True # We allow it to expand dynamically
      choicePanel.Controls.Add(choicePush) # We add it to its parent container
      
      for option in FormChoices: # We dynamically add as many buttons as we have options
         btn = Button() # We initialize a button object
         btn.Name = str(self.index) # We name the button equal to its numeric value, plus its effect.
         btn.Text = str(self.index) + ':--> ' + formStringEscape(option)
         self.index = self.index + 1 # The internal of the button is also the choice that will be put in our list of integers. 
         btn.Dock = DockStyle.Top # We dock the buttons one below the other, to the top of their container (choicePush)
         btn.AutoSize = True # Doesn't seem to do anything
         btn.Height = calcStringButtonHeight(formStringEscape(option))
         btn.Click += self.choiceMade # This triggers the function which records each choice into the confirmValue[] list
         choicePush.Controls.Add(btn) # We add each button to its panel
         btn.BringToFront() # Add new buttons to the bottom of existing ones (Otherwise the buttons would be placed in reverse numerical order)

      buttonNext = Button()
      buttonNext.Text = "Next Page"
      buttonNext.Width = 100
      buttonNext.Dock = DockStyle.Bottom
      buttonNext.Click += self.nextPage
      if pages > 1: self.Controls.Add(buttonNext) # We only add the "Confirm" button on a radio menu.

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

   def nextPage(self, sender, args):
      self.nextPageBool = True
      self.timer.Stop()
      self.Close()
 
   def finishPressed(self, sender, args): # The function called from the finishButton.
      self.timer.Stop()
      self.Close()  # It just closes the form

   def cancelPressed(self, sender, args): # The function called from the cancelButton
      self.confirmValue = 'ABORT' # It replaces the choice list with an ABORT message which is parsed by the calling function
      self.timer.Stop()
      self.Close() # And then closes the form
 
   def choiceMade(self, sender, args): # The function called when pressing one of the choice buttons
      self.confirmValue.append((self.currPage * 7) + int(sender.Name)) # We append the button's name to the existing choices list
      self.label.Text = self.origTitle + "\n\nYour current choices are:\n{}".format(self.confirmValue) # We display what choices we've made until now to the player.
 
   def getIndex(self): # The function called after the form is closed, to grab its choices list
      if self.nextPageBool: 
         self.nextPageBool = False
         return "Next Page"
      else: return self.confirmValue

   def getStoredChoices(self): # The function called after the form is closed, to grab its choices list
      return self.confirmValue

   def onTick(self, sender, event): # Ugly hack required because sometimes the winform does not go on top of all
      if self.timer_tries < 3: # Try three times to bring the form on top
         if debugVerbosity >= 2: self.label.Text = self.origTitle + '\n\n### Timer Iter: ' + str(self.timer_tries)
         self.TopMost = False # Set the form as not on top
         self.Focus() # Focus it
         self.Activate() # Activate it
         self.TopMost = True # And re-send it to top
         self.timer_tries += 1 # Increment this counter to stop after 3 tries.

def multiChoice(title, options,card): # This displays a choice where the player can select more than one ability to trigger serially one after the other
   debugNotify(">>> multiChoice()".format(title))
   if Automations['WinForms']: # If the player has not disabled the custom WinForms, we use those
      optChunks=[options[x:x+7] for x in xrange(0, len(options), 7)]
      optCurrent = 0
      choices = "New"
      currChoices = []
      while choices == "New" or choices == "Next Page":
         Application.EnableVisualStyles() # To make the window look like all other windows in the user's system
         if card.Type == 'ICE': CPType = 'Intrusion Countermeasures Electronics'  # Just some nice fluff
         elif re.search(r'Icebreaker', card.Keywords): CPType = 'ICEbreaker GUI'
         elif card.Type == 'Hardware': CPType = 'Dashboard'
         else: CPType = 'Control Panel'
         debugNotify("About to open form")
         form = MultiChoiceWindow(title, optChunks[optCurrent], CPType, pages = len(optChunks), currPage = optCurrent, existingChoices = currChoices) # We create an object called "form" which contains an instance of the MultiChoice windows form.
         form.ShowDialog() # We bring the form to the front to allow the user to make their choices
         choices = form.getIndex() # Once the form is closed, we check an internal variable within the form object to grab what choices they made
         if choices == "Next Page": 
            debugNotify("Going to next page", 3)
            optCurrent += 1
            if optCurrent >= len(optChunks): optCurrent = 0
            currChoices = form.getStoredChoices()
            debugNotify("currChoices = {}".format(currChoices))            
   else: # If the user has disabled the windows forms, we use instead the OCTGN built-in askInteger function
      concatTXT = title + "\n\n(Tip: You can put multiple abilities one after the the other (e.g. '110'). Max 9 at once)\n\n" # We prepare the text of the window with a concat string
      for iter in range(len(options)): # We populate the concat string with the options
         concatTXT += '{}:--> {}\n'.format(iter,options[iter])
      choicesInteger = askInteger(concatTXT,0) # We now ask the user to put in an integer.
      if not choicesInteger: choices = 'ABORT' # If the user just close the window, abort.
      else: 
         choices = list(str(choicesInteger)) # We convert our number into a list of numeric chars
         for iter in range(len(choices)): choices[iter] = int(choices[iter]) # we convert our list of chars into a list of integers      
   debugNotify("<<< multiChoice() with list: {}".format(choices), 3)
   return choices # We finally return a list of integers to the previous function. Those will in turn be iterated one-by-one serially.
      
#---------------------------------------------------------------------------
# Generic
#---------------------------------------------------------------------------

def debugNotify(msg = 'Debug Ping!', level = 2):
   if not re.search(r'<<<',msg) and not re.search(r'>>>',msg):
      hashes = '#' 
      for iter in range(level): hashes += '#' # We add extra hashes at the start of debug messages equal to the level of the debug+1, to make them stand out more
      msg = hashes + ' ' +  msg
   else: level = 1
   if debugVerbosity >= level: notify(msg)

def barNotifyAll(color, msg, remote = False): # A function that takes care to send barNotifyAll() messages to all players
   mute()
   for player in getPlayers():
      if player != me and not remote: remoteCall(player,'barNotifyAll',[color,msg,True])
   notifyBar(color,msg)
   
def num (s):
   #debugNotify(">>> num(){}".format(extraASDebug())) #Debug
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0
      
def numOrder(num):
    """Return the ordinal for each place in a zero-indexed list.

    list[0] (the first item) returns '1st', list[1] return '2nd', etc.
    """
    def int_to_ordinal(i):
        """Return the ordinal for an integer."""
        # if i is a teen (e.g. 14, 113, 2517), append 'th'
        if 10 <= i % 100 < 20:
            return str(i) + 'th'
        # elseif i ends in 1, 2 or 3 append 'st', 'nd' or 'rd'
        # otherwise append 'th'
        else:
            return  str(i) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(i % 10, "th")

    return int_to_ordinal(num + 1)

def chooseSide(): # Called from many functions to check if the player has chosen a side for this game.
   debugNotify(">>> chooseSide(){}".format(extraASDebug())) #Debug
   mute()
   global playerside, playeraxis
   if playerside == None:  # Has the player selected a side yet? If not, then...
     if me.hasInvertedTable():
        playeraxis = Yaxis
        playerside = -1
     else:
        playeraxis = Yaxis
        playerside = 1
   debugNotify("<<< chooseSide(){}".format(extraASDebug()), 4) #Debug

def displaymatch(match):
   if match is None:
      return None
   return '<Match: {}, groups={}>'.format(match.group(), match.groups())
   
def storeProperties(card, forced = False): # Function that grabs a cards important properties and puts them in a dictionary
   mute()
   try:
      debugNotify(">>> storeProperties(){}".format(extraASDebug())) #Debug
      global Stored_Name, Stored_Cost, Stored_Type, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts, identName
      if (card.Name == '?' and Stored_Name.get(card._id,'?') == '?') or forced:
         if not card.isFaceUp and ((card.group == table and card.owner == me) or forced): # If card is not ours and it's face down, we cannot store its properties without revealing it to the player via the full game log
                                                                                             # See https://github.com/kellyelton/OCTGN/issues/879
            card.peek()
            loopChk(card)
      if (Stored_Name.get(card._id,'?') == '?' and card.Name != '?') or (Stored_Name.get(card._id,'?') != card.Name and card.Name != '?') or forced:
         debugNotify("{} not stored. Storing...".format(card), 3)
         Stored_Name[card._id] = card.Name
         Stored_Cost[card._id] = card.Cost
         Stored_Type[card._id] = card.Type
         getKeywords(card)
         Stored_AutoActions[card._id] = CardsAA.get(card.model,'')
         Stored_AutoScripts[card._id] = CardsAS.get(card.model,'')
         if card.Type == 'Identity' and card.owner == me: identName = card.Name
      elif card.Name == '?':
         debugNotify("Could not store card properties because it is hidden from us")
         return 'ABORT'
      debugNotify("<<< storeProperties()", 3)
   except: notify("!!!ERROR!!! In storeProperties()")

def fetchProperty(card, property): 
   mute()
   debugNotify(">>> fetchProperty(){}".format(extraASDebug())) #Debug
   if property == 'name' or property == 'Name': currentValue = Stored_Name.get(card._id,'?')
   elif property == 'Cost': currentValue = Stored_Cost.get(card._id,'?')
   elif property == 'Type': currentValue = Stored_Type.get(card._id,'?')
   elif property == 'Keywords': currentValue = Stored_Keywords.get(card._id,'?')
   elif property == 'AutoScripts': currentValue = Stored_AutoScripts.get(card._id,'?')
   elif property == 'AutoActions': currentValue = Stored_AutoActions.get(card._id,'?')
   else: currentValue = card.properties[property]
   if currentValue == '?' or currentValue == 'Card':
      debugNotify("Card property: {} unreadable = {}".format(property,currentValue), 4) #Debug
      if not card.isFaceUp and card.group == table and card.owner == me:
         debugNotify("Need to peek card to read its properties.", 3) #Debug
         if debugVerbosity >= 0 and confirm("Peek at card? (>>>fetchProperty())"): card.peek()
         loopChk(card)
      debugNotify("Ready to grab real properties.", 3) #Debug
      if property == 'name': currentValue = card.Name # Now that we had a chance to peek at the card, we grab its property again.
      else: 
         currentValue = card.properties[property]
         debugNotify("Grabbing {}'s {} manually: {}.".format(card,property,card.properties[property]), 3)
         #storeProperties(card) # Commented out because putting it here can cause an infinite loop
   debugNotify("<<< fetchProperty() by returning: {}".format(currentValue), 4)
   if not currentValue: currentValue = ''
   return currentValue

def clearCovers(): # Functions which goes through the table and clears any cover cards
   debugNotify(">>> clearCovers()") #Debug
   for cover in table:
      if cover.model == 'ac3a3d5d-7e3a-4742-b9b2-7f72596d9c1b': cover.moveTo(me.piles['Removed from Game'])

def findOpponent():
   # Just a quick function to make the code more readable
   return ofwhom('ofOpponent')
   
def loopChk(card,property = 'Type'):
   debugNotify(">>> loopChk(){}".format(extraASDebug())) #Debug
   loopcount = 0
   while card.properties[property] == '?':
      rnd(1,10)
      update()
      loopcount += 1
      if loopcount == 5:
         whisper(":::Error::: Card property can't be grabbed. Aborting!")
         return 'ABORT'
   debugNotify("<<< loopChk()", 3) #Debug
   return 'OK'         
   
def sortPriority(cardList):
   debugNotify(">>> sortPriority()") #Debug
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
      for sortTarget in sortedList: tlist.append(fetchProperty(sortTarget, 'name')) # Debug   
      notify("<<< sortPriority() returning {}".format(tlist)) #Debug
   return sortedList
   
def oncePerTurn(card, x = 0, y = 0, silent = False, act = 'manual'):
   debugNotify(">>> oncePerTurn(){}".format(extraASDebug())) #Debug
   mute()
   if card.orientation == Rot90:
      if act != 'manual': return 'ABORT' # If the player is not activating an effect manually, we always fail silently. So as not to spam the confirm.
      elif not confirm("The once-per-turn ability of {} has already been used this turn\nBypass restriction?.".format(fetchProperty(card, 'name'))): return 'ABORT'
      else: 
         if not silent and act != 'dryRun': notify('{} activates the once-per-turn ability of {} another time'.format(me, card))
   else:
      if not silent and act != 'dryRun': notify('{} activates the once-per-turn ability of {}'.format(me, card))
   if act != 'dryRun': 
      if card.controller != me: remoteCall(card.controller,'rotCard',card) # Cannot remote call this or ABT installing more than 1 ICE will trigger HB:ETF ability 3 times
      else: card.orientation = Rot90
   debugNotify("<<< oncePerTurn() exit OK", 3) #Debug

def chkRestrictionMarker(card, Autoscript, silent = False, act = 'manual'): # An additional oncePerTurn restriction, that works with markers (with cards that have two different once-per-turn abilities)
   debugNotify(">>> chkRestrictionMarker(){}".format(extraASDebug())) #Debug
   mute()
   restrictedMarkerRegex  = re.search(r"restrictionMarker([A-Za-z0-9_:' ]+)",Autoscript)
   if restrictedMarkerRegex:
      debugNotify("restrictedMarker = {}".format(restrictedMarkerRegex.group(1)))
      restrictedMarker = findMarker(card, restrictedMarkerRegex.group(1))
      if restrictedMarker:
         if act != 'manual': return 'ABORT' # If the player is not activating an effect manually, we always fail silently. So as not to spam the confirm.
         elif not confirm("The once-per-turn ability of {} has already been used this turn\nBypass restriction?.".format(fetchProperty(card, 'name'))): return 'ABORT'
         else: 
            if not silent and act != 'dryRun': notify('{} activates the once-per-turn ability of {} another time'.format(me, card))
      else:
         if not silent and act != 'dryRun': notify('{} activates the once-per-turn ability of {}'.format(me, card))
      if act != 'dryRun': TokensX('Put1{}-isSilent'.format(restrictedMarkerRegex.group(1)), '', card)
   debugNotify("<<< chkRestrictionMarker()") #Debug

def clearRestrictionMarkers(remoted = False):
   debugNotify(">>> clearRestrictionMarkers(){}".format(extraASDebug())) #Debug
   if not remoted:
      for player in getPlayers():
         remoteCall(player,'clearRestrictionMarkers',[True])
   for card in table:
      if card.controller == me: 
         for Autoscript in CardsAS.get(card.model,'').split('||'):
            restrictedMarkerRegex  = re.search(r"restrictionMarker([A-Za-z0-9_:' ]+)",Autoscript)
            if restrictedMarkerRegex:
               restrictedMarker = findMarker(card, restrictedMarkerRegex.group(1))
               if restrictedMarker: card.markers[restrictedMarker] = 0
   debugNotify("<<< clearRestrictionMarkers()") #Debug
         
def delayed_whisper(text): # Because whispers for some reason execute before notifys
   rnd(1,10)
   whisper(text)   
   
def chkModulator(card, modulator, scriptType = 'onPlay'): # Checks the card's autoscripts for the existence of a specific modulator
   debugNotify(">>> chkModulator() looking for {}".format(modulator)) #Debug
   debugNotify("scriptType = {}".format(scriptType)) #Debug
   ModulatorExists = False
   Autoscripts = CardsAS.get(card.model,'').split('||')
   for autoS in Autoscripts:
      debugNotify("Checking {}'s AS: {}".format(card,autoS))
      if not re.search(r'{}'.format(scriptType),autoS): 
         debugNotify("Rejected!",4)
         continue
      # We check the script only if it matches the script type we're looking for.
      # So if we're checking if a specific onTrash modulator exists on the card, we only check for "onTrash" scripts.
      if re.search(r'{}'.format(modulator),autoS): 
         debugNotify("Modulator Matches!",4)
         ModulatorExists = True
   debugNotify("<<< chkModulator() with return {}".format(ModulatorExists)) #Debug
   return ModulatorExists

def fetchHost(card):
   debugNotify(">>> fetchHost()") #Debug
   host = None
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostID = hostCards.get(card._id,None)
   if hostID: host = Card(hostID) 
   debugNotify("<<< fetchHost() with return {}".format(host)) #Debug
   return host
   
def compareValue(comparison, value, requirement):
   debugNotify(">>> compareValue()")
   debugNotify("{} {} {}?".format(value,comparison,requirement))
   if comparison == 'eq' and value != requirement: return False # 'eq' stands for "Equal to"
   if comparison == 'le' and value > requirement: return False # 'le' stands for "Less or Equal"
   if comparison == 'ge' and value < requirement: return False # 'ge' stands for "Greater or Equal"
   if comparison == 'lt' and value >= requirement: return False # 'lt' stands for "Less Than"
   if comparison == 'gt' and value <= requirement: return False # 'gt' stands for "Greater Than"
   debugNotify("<<< compareValue() with return True")
   return True # If none of the requirements fail, we return true
           
#---------------------------------------------------------------------------
# Card Placement functions
#---------------------------------------------------------------------------

def cwidth(card, divisor = 10):
   #debugNotify(">>> cwidth(){}".format(extraASDebug())) #Debug
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
   #debugNotify(">>> cheight(){}".format(extraASDebug())) #Debug
   if divisor == 0: offset = 0
   else: offset = card.height() / divisor
   return (card.height() + offset)

def yaxisMove(card):
   #debugNotify(">>> yaxisMove(){}".format(extraASDebug())) #Debug
# Variable to move the cards played by player 2 on a 2-sided table, more towards their own side. 
# Player's 2 axis will fall one extra card length towards their side.
# This is because of bug #146 (https://github.com/kellyelton/OCTGN/issues/146)
   if me.hasInvertedTable(): cardmove = cheight(card)
   else: cardmove = cardmove = 0
   return cardmove

  
#---------------------------------------------------------------------------
# Remote Calls
#---------------------------------------------------------------------------   

def grabPileControl(pile, player = me):
   debugNotify(">>> grabPileControl(){}".format(extraASDebug())) #Debug
   debugNotify("Grabbing control of {}'s {} on behalf of {}".format(pile.player,pile.name,player))
   if pile.controller != player:
      if pile.controller != me: remoteCall(pile.controller,'passPileControl',[pile,player])
      else: passPileControl(pile,player) # We don't want to do a remote call if the current controller is ourself, as the call we go out after we finish all scripts, which will end up causing a delay later while the game is checking if control pass is done.
   count = 0
   while pile.controller != player: 
      if count >= 2 and not count % 2: notify("=> {} is still trying to take control of {}...".format(player,pileName(pile)))
      rnd(1,100)
      count += 1
      if count >= 3: 
         notify(":::ERROR::: Pile Control not passed! Will see errors.")
         break   
   debugNotify("<<< grabPileControl(){}".format(extraASDebug())) #Debug

def passPileControl(pile,player):
   debugNotify(">>> passPileControl(){}".format(extraASDebug())) #Debug
   mute()
   update()
   pile.setController(player)
   debugNotify("<<< passPileControl(){}".format(extraASDebug())) #Debug
      
def grabCardControl(card, player = me):
   debugNotify(">>> grabCardControl(){}".format(extraASDebug())) #Debug
   debugNotify("Grabbing control of {} on behalf of {}".format(card,player))
   if card.group != table: debugNotify(":::WARNING::: Cannot grab card control while in a pile. Aborting!")
   else:
      if card.controller != player: 
         if card.controller != me: remoteCall(card.controller,'passCardControl',[card,player])
         else: passCardControl(card,player) # We don't want to do a remote call if the current controller is ourself, as the call we go out after we finish all scripts, which will end up causing a delay later while the game is checking if control pass is done.
      count = 0
      while card.controller != player: 
         if count >= 2 and not count % 2: notify("=> {} is still trying to take control of {}...".format(player,card))
         rnd(1,100)
         count += 1
         if count >= 3: 
            notify(":::ERROR::: Card Control not passed! Will see errors.")
            break   
   debugNotify("<<< grabCardControl(){}".format(extraASDebug())) #Debug
   
def passCardControl(card,player):
   debugNotify(">>> passCardControl(){}".format(extraASDebug())) #Debug
   debugNotify("card ={}, player = {}".format(card,player))
   mute()
   update()
   debugNotify("Getting ready to pass card control")
   if card.controller != player: card.setController(player)
   debugNotify("<<< passCardControl()") #Debug
      
def changeCardGroup(card, group, sendToBottom = False): # A cumulative function to take care for handling card and group control when moving a card from one group to another.
   debugNotify(">>> changeCardGroup(){}".format(extraASDebug())) #Debug
   debugNotify("Will move {} to {}'s {}".format(card,group.player,group.name))
   prevGroup = card.group
   if prevGroup == table: grabCardControl(card) # We take control of the card, but only if it's on the table, otherwise we can't.
   else: grabPileControl(prevGroup)
   grabPileControl(group) # We take control of the target pile
   storeProperties(card) # Since we're at it, we might as well store its properties for later
   debugNotify("Finished Taking Control. Moving card to different group",1)
   if sendToBottom: card.moveToBottom(group)
   else: card.moveTo(group) # We move the card into the target pile
   if group.player != group.controller: grabPileControl(group,group.player) # We return control of the target pile to its original owner.
   if prevGroup != table and prevGroup.player != prevGroup.controller: grabPileControl(prevGroup,prevGroup.player) # If we took control of a whole pile to allow us to move the card, we return it now
   debugNotify("<<< changeCardGroup(){}".format(extraASDebug())) #Debug

def placeOnTable(card,x,y,facedownStatus = False): # A function that asks the current card controller to move a card to another table position
   if card.controller == me: card.moveToTable(x, y, facedownStatus)
   else: remoteCall(card.controller,'placeOnTable',[card,x,y,facedownStatus])
   
def indexSet(card,index): # A function that asks the current card controller to move the card to a specific index.
   if card.controller == me: 
      if index == 'front': card.sendToFront()
      elif index == 'back': card.sendToBack()
      else: card.setIndex(index) 
   else: remoteCall(card.controller,'indexSet',[card,index])
   
def rotCard(card):
   mute()
   card.orientation = Rot90
      
def grabVisibility(group):
   mute()
   group.setVisibility('me')      
#---------------------------------------------------------------------------
# Patron Functions
#---------------------------------------------------------------------------   

def prepPatronLists():
   global supercharged,customized
   supercharged = SuperchargedSubs + CustomSubs + CardSubs
   customized = CustomSubs + CardSubs
   debugNotify("supercharged = {}".format(supercharged))
   
def superCharge(card):
   if me.name.lower() in supercharged: card.switchTo('Supercharged')
   if me.name.lower() in CardSubs: card.switchTo(me.name.lower())
      
def announceSupercharge():
   if me.name.lower() in supercharged:
      notify("   \n+=+ {}\n".format(CustomMsgs.get(me.name.lower(),SuperchargedMsg))) # We either announce a player's custom message, or the generic supercharged one
      
def announceSoT():
   statsTXT = "They have {}, {} cards and {} {} starting this turn.".format(uniCredit(me.Credits),len(me.hand),me.Clicks,uniClick())
   if ds == "corp": 
      announceTXT = "The offices of {} ({}) are now open for business.".format(identName,me)
      if corpStartMsgs.get(me.name.lower(),None): customTXT = "\n\n{}\n".format(corpStartMsgs[me.name.lower()])
      else: customTXT = ''
      #notify("=> The offices of {} ({}) are now open for business.\n They have {} and {} {} for this turn.".format(identName,me,uniCredit(me.Credits),me.Clicks,uniClick()))
   else:
      announceTXT = "{} ({}) has woken up.".format(identName,me)
      if runnerStartMsgs.get(me.name.lower(),None): customTXT = "\n\n{}\n".format(runnerStartMsgs[me.name.lower()])
      else: customTXT = ''
      #notify ("=> {} ({}) has woken up. They have {} and {} {} for this turn.".format(identName,me,uniCredit(me.Credits),me.Clicks,uniClick()))
   #if ds == 'runner': barNotifyAll('#AA0000',"{} has started their turn".format(me))
   #else: barNotifyAll('#0000FF',"{} has started their turn".format(me))
   notify("=> {}{}".format(announceTXT,customTXT)) 
   notify("=> {}".format(statsTXT))
   if ds == 'runner' and chkTags(): notify(":::Reminder::: {} is Tagged!".format(identName))

def announceEoT():
   statsTXT = "They end their turn with {}, {} cards in their {}, and {} cards in their {}.".format(uniCredit(me.Credits),len(me.hand),pileName(me.hand),len(me.piles['R&D/Stack']),pileName(me.piles['R&D/Stack']))
   if ds == "corp": 
      announceTXT = "{} ({}) has reached CoB.".format(identName, me)
      if corpEndMsgs.get(me.name.lower(),None): customTXT = "\n\n{}\n".format(corpEndMsgs[me.name.lower()])
      else: customTXT = ''
   else:
      announceTXT = "{} ({}) has gone to sleep for the day.".format(identName,me)
      if runnerEndMsgs.get(me.name.lower(),None): customTXT = "\n\n{}\n".format(runnerEndMsgs[me.name.lower()])
      else: customTXT = ''
   #if ds == 'runner': barNotifyAll('#880000',"{} has ended their turn".format(me))
   #else: barNotifyAll('#0000AA',"{} has ended their turn".format(me))
   notify("=> {}{}".format(announceTXT,customTXT)) 
   notify("=> {}".format(statsTXT))
      