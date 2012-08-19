    # Python Scripts for the Netrunner CCG definition for OCTGN
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

import re

Advance = ("Advance", "73b8d1f2-cd54-41a9-b689-3726b7b86f4f")
Generic = ("Generic", "b384957d-22c5-4e7d-a508-3990c82f4df6")
Bits = ("Bits", "19be5742-d233-4ea1-a88a-702cfec930b1")
Scored = ("Scored", "10254d1f-6335-4b90-b124-b01ec131dd07")
Not_rezzed = ("Not rezzed", "8105e4c7-cb54-4421-9ae2-4e276bedee90")
#Derezzed = ("Derezzed", "ae34ee21-5309-46b3-98de-9d428f59e243")
Trace_value = ("Trace value", "01feb523-ac36-4dcd-970a-515aa8d73e37")
Link_value = ("Link value", "3c429e4c-3c7a-49fb-96cc-7f84a63cc672")
PlusOne= ("+1", "aa261722-e12a-41d4-a475-3cc1043166a7")
MinusOne= ("-1", "48ceb18b-5521-4d3f-b5fb-c8212e8bcbae")
         
#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------
ds = ""
Automations = {'Play, Score and Rez': True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'Start/End-of-Turn'      : True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
               'Damage Prevention'      : True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
               'Damage'             : True}

UniBits = True # If True, game will display bits as unicode characters ❶, ❷, ❿ etc

ModifyDraw = False #if True the audraw should warn the player to look at r&D instead 
TraceValue = 0

DifficultyLevels = { }

Stored_Type = {}
Stored_Keywords = {}
Stored_Cost = {}
Stored_AutoActions = {}

MemoryRequirements = { }
InstallationCosts = { }
maxActions = 3
scoredAgendas = 0
currAction = 0
playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is

DMGwarn = True # A boolean varialbe to track whether we've warned the player about doing automatic damage.
Dummywarn = True # Much like above, but it serves to remind the player not to trash some cards.
DummyTrashWarn = True
ExposeTargetsWarn = True # A boolean variable that reminds the player to select multiple targets to expose for used by specific cards like Encryption Breakthrough
RevealandShuffleWarn = True # Similar to above.
newturn = True #We use this variable to track whether a player has yet to do anything this turn.
endofturn = False #We use this variable to know if the player is in the end-of-turn phase.
failedRequirement = True #A Global boolean that we set in case an Autoscript cost cannot be paid, so that we know to abort the rest of the script.

debugVerbosity = -1
#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------

mdict = dict(Advance = ("Advance", "73b8d1f2-cd54-41a9-b689-3726b7b86f4f"),
             Generic = ("Generic", "b384957d-22c5-4e7d-a508-3990c82f4df6"),
             Bits = ("Bits", "19be5742-d233-4ea1-a88a-702cfec930b1"),
             Scored = ("Scored", "10254d1f-6335-4b90-b124-b01ec131dd07"),
             Not_rezzed = ("Not rezzed", "8105e4c7-cb54-4421-9ae2-4e276bedee90"),
             Derezzed = ("Derezzed", "ae34ee21-5309-46b3-98de-9d428f59e243"),
             Trace_value = ("Trace value", "01feb523-ac36-4dcd-970a-515aa8d73e37"),
             Link_value = ("Link value", "3c429e4c-3c7a-49fb-96cc-7f84a63cc672"),
             PlusOnePerm = ("Permanent +1", "f6230db2-d222-445f-85dd-406ea12d92f6"),
             PlusOne= ("Temporary+1", "aa261722-e12a-41d4-a475-3cc1043166a7"),
             MinusOne= ("Temporary-1", "48ceb18b-5521-4d3f-b5fb-c8212e8bcbae"),
             DaemonMU = ("Daemon MU", "6e46d937-786c-4618-b02c-d7d5ffd3b1a5"),
             BaseLink = ("Base Link", "226b0f44-bbdc-4960-86cd-21f404265562"),
             virusButcherBoy = ("Butcher Boy","5831fb18-7cdf-44d2-8685-bdd392bb9f1c"),
             virusCascade = ("Cascade","723a0cca-7a05-46a8-a681-6e06666042ee"),
             virusCockroach = ("Cockroach","cda4cfcb-6f2d-4a7f-acaf-d796b8d1edee"),
             virusGremlin = ("Gremlin","032d2efa-e722-4218-ba2b-699dc80f0b94"),
             virusThought = ("Thought","811b9153-93cb-4898-ad9f-68864452b9f4"),
             virusFait = ("Fait","72c89567-72aa-446d-a9ea-e158c22c113a"),
             virusBoardwalk = ("Boardwalk","8c48db01-4f12-4653-a31a-3d22e9f5b6e9"),
             virusIncubate = ("Incubate","eccc2ee3-2bca-4563-8196-54de4909d313"),
             virusPattel = ("Pattel","93a124c4-d2fe-4f58-9531-1396675c64dd"),
             protectionMeatDMG = ("Meat Damage protection","f50fbac7-a147-4941-8d77-56cf9ea672ea"),
             protectionNetDMG = ("Net Damage protection","84527bb1-6b34-4ace-9b11-7e19a6e353c7"),
             protectionBrainDMG = ("Brain damage protection","8a0612d7-202b-44ec-acdc-84ff93e7968d"),
             protectionNetBrainDMG = ("Net & Brain Damage protection","42072423-2599-4e70-80b6-56127b7177d9"),
             protectionAllDMG = ("Complete Damage protection","04d72620-17d1-4189-9abb-a2c48ddf7d42"),
             protectionVirus = ("Virus protection","6242317f-b706-4e39-b60a-32958d00a8f8"),
             BrainDMG = ("Brain Damage","05250943-0c9f-4486-bb96-481c025ce0e0"))

turns = [
   'Start of Game',
   "It is now Corporation's Turn",
   "It is now Runner's Turn",
   "It is now End of Turn"]

trashEasterEgg = [
   "You really shouldn't try to trash this kind of card.",
   "No really, stop trying to trash this card. You need it.",
   "Just how silly are you?",
   "You just won't rest until you've trashed a setup card will you?",
   "I'm warning you...",
   "OK, NOW I'm really warning you...",
   "Shit's just got real!",
   "Careful what you wish for..."]
trashEasterEggIDX = 0
 
ScoredColor = "#00ff44"
SelectColor = "#009900"
EmergencyColor = "#ff0000"
DummyColor = "#000000" # Marks cards which are supposed to be out of play, so that players can tell them apart.
RevealedColor = "#ffffff"

Xaxis = 'x'
Yaxis = 'y'
#---------------------------------------------------------------------------
# General functions
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

#---------------------------------------------------------------------------
# Generic Netrunner functions
#---------------------------------------------------------------------------

def uniBit(count):
   if debugVerbosity >= 1: notify(">>> uniBit(){}".format(extraASDebug())) #Debug
   count = num(count)
   if UniBits:
      if count == 1: return '❶'
      elif count == 2: return '❷'
      elif count == 3: return '❸'
      elif count == 4: return '❹'
      elif count == 5: return '❺'
      elif count == 6: return '❻'
      elif count == 7: return '❼'
      elif count == 8: return '❽'
      elif count == 9: return '❾'
      #elif count == 10: return '❿' Doesn't display that well. Need to fix the font.
      else: return "({})".format(count)
   else: return "({})".format(count)
 
def uniAction():
   if debugVerbosity >= 1: notify(">>> uniAction(){}".format(extraASDebug())) #Debug
   if UniBits: return '⏎'
   else: return '|>'

def chooseWell(limit, choiceText, default = None):
   if debugVerbosity >= 1: notify(">>> chooseWell(){}".format(extraASDebug())) #Debug
   if default == None: default = 0# If the player has not provided a default value for askInteger, just assume it's the max.
   choice = limit # limit is the number of choices we have
   if limit > 1: # But since we use 0 as a valid choice, then we can't actually select the limit as a number
      while choice >= limit:
         choice = askInteger("{}".format(choiceText), default)
         if not choice: return False
         if choice > limit: whisper("You must choose between 0 and {}".format(limit - 1))
   else: choice = 0 # If our limit is 1, it means there's only one choice, 0.
   return choice

def findMarker(card, markerDesc): # Goes through the markers on the card and looks if one exist with a specific description
   if debugVerbosity >= 1: notify(">>> findMarker(){}".format(extraASDebug())) #Debug
   foundKey = None
   if markerDesc in mdict: markerDesc = mdict[markerDesc][0] # If the marker description is the code of a known marker, then we need to grab the actual name of that.
   for key in card.markers:
      if debugVerbosity >= 4: notify("### Key: {}\nmarkerDesc: {}".format(key[0],markerDesc)) # Debug
      if re.search(r'{}'.format(markerDesc),key[0]) or markerDesc == key[0]:
         foundKey = key
         if debugVerbosity >= 3: notify("### Found {} on {}".format(key[0],card))
         break
   if debugVerbosity >= 4: notify("<<< findMarker() by returning: {}".format(foundKey))
   return foundKey
   
def getKeywords(card): # A function which combines the existing card keywords, with markers which give it extra ones.
   if debugVerbosity >= 1: notify(">>> getKeywords(){}".format(extraASDebug())) #Debug
   global Stored_Keywords
   #confirm("getKeywords") # Debug
   keywordsList = []
   strippedKeywordsList = card.Keywords.split('-')
   for cardKW in strippedKeywordsList:
      strippedKW = cardKW.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
      if strippedKW: keywordsList.append(strippedKW) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.   
   if card.markers:
      for key in card.markers:
         markerKeyword = re.search('Keyword:([\w ]+)',key[0])
         if markerKeyword:
            #confirm("marker found: {}\n key: {}".format(markerKeyword.groups(),key[0])) # Debug
            if markerKeyword.group(1) == 'Wall' or markerKeyword.group(1) == 'Sentry' or markerKeyword.group(1) == 'Code Gate': #These keywords are mutually exclusive. An Ice can't be more than 1 of these
               if 'Wall' in keywordsList: keywordsList.remove('Wall')
               if 'Sentry' in keywordsList: keywordsList.remove('Sentry')
               if 'Code Gate' in keywordsList: keywordsList.remove('Code Gate')
            if re.search(r'Breaker',markerKeyword.group(1)):
               if 'Wall Breaker' in keywordsList: keywordsList.remove('Wall Breaker')
               if 'Sentry Breaker' in keywordsList: keywordsList.remove('Sentry Breaker')
               if 'Code Gate Breaker' in keywordsList: keywordsList.remove('Code Gate Breaker')
            keywordsList.append(markerKeyword.group(1))
            
   keywords = ''
   for KW in keywordsList:
      keywords += '{}-'.format(KW)
   Stored_Keywords[card] = keywords[:-1] # We also update the global variable for this card, which is used by many functions.
   if debugVerbosity >= 4: notify("<<< getKeywords() by returning: {}".format(keywords[:-1]))
   return keywords[:-1] # We need to remove the trailing dash '-'
   
def pileName(group):
   if debugVerbosity >= 1: notify(">>> pileName(){}".format(extraASDebug())) #Debug   
   if debugVerbosity >= 3: notify(">>> pile player: {}".format(group.player)) #Debug   
   if group.name == 'Trash/Archives(Face-up)':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'Face-up Archives'
      else: name = 'Trash'
   elif group.name == 'R&D/Stack':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'R&D'
      else: name = 'Stack'
   elif group.name == 'Archives(Hidden)': name = 'Hidden Archives'
   else:
      if group.player.getGlobalVariable('ds') == 'corp': name = 'HQ'
      else: name = 'Hand'
   if debugVerbosity >= 4: notify("<<< pileName() by returning: {}".format(name))
   return name
   
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


   
#---------------------------------------------------------------------------
# Actions indication
#---------------------------------------------------------------------------

def useAction(group = table, x=0, y=0, count = 1):
   if debugVerbosity >= 1: notify(">>> useAction(){}".format(extraASDebug())) #Debug
   global currAction
   mute()
   extraText = ''
   actionsReduce = findCounterPrevention(me.Actions, 'Actions', me)
   if actionsReduce: notify(":::WARNING::: {} had to forfeit their next {} actions".format(me, actionsReduce))
   me.Actions -= actionsReduce
   if me.Actions < count: 
      if not confirm("You have no more actions left for this turn. Are you sure you want to continue?"): return 'ABORT'
      else: extraText = ' (Exceeding Max!)'
   me.Actions -= count
   currAction += count
   if count == 2: return "{} {} {} takes Double Action #{} and #{}{}".format(uniAction(),uniAction(),me,currAction - 1, currAction,extraText)
   elif count == 3: return "{} {} {} {} takes Triple Action #{}, #{} and #{}{}".format(uniAction(),uniAction(),uniAction(),me,currAction - 2, currAction - 1, currAction,extraText)
   else: return "{} {} takes Action #{}{}".format(uniAction(),me,currAction,extraText) # We give act +1 because otherwise the first action would be action #0.

def goToEndTurn(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> goToEndTurn(){}".format(extraASDebug())) #Debug
   mute()
   global endofturn, currAction, newturn
   if ds == "":
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   if me.Actions > 0: # If the player has not used all their actions for this turn, remind them, just in case.
      if not debugVerbosity and not confirm("You have not taken all your actions for this turn, are you sure you want to declare end of turn"): return
   if len(me.hand) > currentHandSize(): #If the player is holding more cards than their hand max. remind them that they need to discard some 
                                        # and put them in the end of turn to allow them to do so.
      if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
         if not debugVerbosity and not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
         else: notify(":::Warning::: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
      else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
         if ds == "corp": notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
         else: notify ("Runner {} is rebooting all systems for the day.".format(me))
         if not debugVerbosity: andconfirm(':::Warning:::\n\n You have more card in your hand than your current hand size maximum of {}. Please discard enough and then use the "Declare End of Turn" action again.'.format(currentHandSize()))
         endofturn = True
         return
   endofturn = False
   newturn = False
   currAction = 0
   atTurnStartEndEffects('End')
   if ds == "corp": notify ("=> The Corporation of {} has reached CoB (Close of Business hours).".format(me))
   else: notify ("=> Runner {} has gone to sleep for the day.".format(me))

def goToSot (group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> goToSot(){}".format(extraASDebug())) #Debug
   global newturn, endofturn
   mute()
   if endofturn or currAction or newturn:
      if not debugVerbosity and not confirm("You have not yet properly ended you previous turn. You need to use F12 after you've finished all your actions.\n\nAre you sure you want to continue?"): return
      else: 
         if len(me.hand) > currentHandSize(): # Just made sure to notify of any shenanigans
            notify(":::Warning::: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
         else: notify(":::Warning::: {} has skipped their End-of-Turn phase".format(me))
         endofturn = False
   if ds == "":
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   actionsReduce = findCounterPrevention(maxActions, 'Actions', me) # Checking if the player has any effects which force them to forfeit actions.
   if actionsReduce: extraTXT = " ({} forfeited)".format(actionsReduce)
   else: extraTXT = ''
   if me.Actions < 0: 
      if not debugVerbosity and not confirm("Your actions were negative from last turn. Was this a result of a penalty you suffered from a card?"): 
         me.Actions = maxActions - actionsReduce # If the player did not have a penalty, then we assume those were extra actions granted by some card effect, so we make sure they have their full maximum
      else: 
         me.Actions += maxActions - actionsReduce # If it was a penalty, then it remains with them for this round, which means they have less actions to use.
         notify("{} is starting with {} less actions this turn, due to a penalty from a previous turn.")
   else: me.Actions = maxActions - actionsReduce
   myCards = (card for card in table if card.controller == me and card.owner == me)
   for card in myCards: 
      if card in Stored_Type and Stored_Type[card] != 'Ice': card.orientation &= ~Rot90 # Refresh all cards which can be used once a turn.
   newturn = True
   atTurnStartEndEffects('Start') # Check all our cards to see if there's any Start of Turn effects active.
   if ds == "corp": notify("=> The offices of {}'s Corporation are now open for business. They have {} actions for this turn{}.".format(me,me.Actions,extraTXT))
   else: notify ("=> Runner {} has woken up. They have {} actions for this turn{}.".format(me,me.Actions,extraTXT))

def modActions(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> modActions(){}".format(extraASDebug())) #Debug
   global maxActions
   mute()
   bkup = maxActions
   maxActions = askInteger("What is your current maximum Actions per turn?", maxActions)
   if maxActions == None: maxActions = bkup # In case the player closes the window, we restore their previous max.
   else: notify("{} has set their Max Actions to {} per turn".format(me,maxActions))
#------------------------------------------------------------------------------
# Table group actions
#------------------------------------------------------------------------------

def switchAutomation(type,command = 'Off'):
   if debugVerbosity >= 1: notify(">>> switchAutomation(){}".format(extraASDebug())) #Debug
   global Automations
   if (Automations[type] and command == 'Off') or (not Automations[type] and command == 'Announce'):
      notify ("--> {}'s {} automations are OFF.".format(me,type))
      if command != 'Announce': Automations[type] = False
   else:
      notify ("--> {}'s {} automations are ON.".format(me,type))
      if command != 'Announce': Automations[type] = True
   
def switchPlayAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchPlayAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Play, Score and Rez')
   
def switchStartEndAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchStartEndAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Start/End-of-Turn')

def switchDMGAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchDMGAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Damage')

def switchPreventDMGAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchDMGAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Damage Prevention')
        
def switchUniBits(group,x=0,y=0,command = 'Off'):
   if debugVerbosity >= 1: notify(">>> switchUniBits(){}".format(extraASDebug())) #Debug
   global UniBits
   if UniBits and command != 'On':
      whisper("Bits and Actions will now be displayed as normal ASCII.".format(me))
      UniBits = False
   else:
      whisper("Bits and Actions will now be displayed as Unicode.".format(me))
      UniBits = True

def ImAProAtThis(group, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> ImAProAtThis(){}".format(extraASDebug())) #Debug
   global DMGwarn, Dummywarn, DummyTrashWarn, ExposeTargetsWarn, RevealandShuffleWarn
   DMGwarn = False 
   Dummywarn = False 
   ExposeTargetsWarn = False
   RevealandShuffleWarn = False
   DummyTrashWarn = False
   whisper("-- All Newbie warnings have been disabled. Play safe.")
        
def createStartingCards():
   if debugVerbosity >= 1: notify(">>> createStartingCards(){}".format(extraASDebug())) #Debug
   traceCard = table.create("c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8", 0, 155 * playerside, 1, True) #The Trace card
   storeSpecial(traceCard)
   if ds == "corp":
      table.create("2a0b57ca-1714-4a70-88d7-25fdf795486f", 150, 160 * playerside, 1, True)
      table.create("181de100-c255-464f-a4ed-4ac8cd728c61", 300, 160 * playerside, 1, True)
      table.create("59665835-0b0c-4710-99f7-8b90377c35b7", 450, 160 * playerside, 1, True)
      AV = table.create("feaadfe5-63fc-443e-b829-b9f63c346d11", 0, 250 * playerside, 1, True) # The Virus Scan card.
      storeSpecial(AV)
   else:
      TC = table.create("f58c40eb-bb11-4bad-9562-030d906ea352", 0, 250 * playerside, 1, True) # The Technical Difficulties card.
      storeSpecial(TC)      

def intJackin(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> intJackin(){}".format(extraASDebug())) #Debug
   global ds, maxActions,newturn,endofturn, currAction, debugVerbosity
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions
   mute()
   debugVerbosity = -1 # Jackin means normal game.
   ds = ""
   if not table.isTwoSided(): 
      if not confirm("This game is designed to be played on a two-sided table. Things will be wonky otherwise!! Please start a new game and makde sure the  the appropriate button is checked. Are you sure you want to continue?"): return   
   chooseSide()
   stack = me.piles['R&D/Stack']
   if len(stack) == 0:
      whisper ("Please load a deck first!")
      return
   TopCard = stack[0]
   TopCard.moveTo(me.piles['Trash/Archives(Face-up)'])
   if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
   ds = TopCard.Player
   me.setGlobalVariable('ds', ds)
   TopCard.moveTo(me.piles['R&D/Stack'])
   if checkDeckNoLimit(stack) != 0: notify ("SHOULD RETURN")
   me.counters['Bit Pool'].value = 5
   me.counters['Max Hand Size'].value = 5
   me.counters['Tags'].value = 0
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 0
   Stored_Type.clear()
   Stored_Cost.clear()
   Stored_Keywords.clear()
   Stored_AutoActions.clear()
   newturn = False 
   endofturn = False
   currAction = 0
   if ds == "corp":
      maxActions = 3
      #me.Actions = maxActions # We now do that during SoT
      me.Memory = 0
      NameDeck = "R&D"
      notify("{} is playing as Corporation".format(me))      
   else:
      maxActions = 4
      #me.Actions = maxActions # We now do that during SoT
      me.Memory = 4
      NameDeck = "Stack"
      notify("{} is playing as Runner".format(me))
   createStartingCards()
   for type in Automations: switchAutomation(type,'Announce')
   shuffle(me.piles['R&D/Stack'])
   notify ("{}'s {} is shuffled ".format(me,NameDeck) )
   drawMany (me.piles['R&D/Stack'], 5) 

def storeSpecial(card): 
# Function stores into a shared variable some special cards that other players might look up.
   if debugVerbosity >= 1: notify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
   specialCards = eval(me.getGlobalVariable('specialCards'))
   specialCards[card.Type] = card._id
   me.setGlobalVariable('specialCards', str(specialCards))

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   if debugVerbosity >= 1: notify(">>> getSpecial(){}".format(extraASDebug())) #Debug
   specialCards = eval(player.getGlobalVariable('specialCards'))
   if debugVerbosity >= 4: notify("<<< getSpecial() by returning: {}".format(Card(specialCards[cardType])))
   return Card(specialCards[cardType])
   
def start_token(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> start_token(){}".format(extraASDebug())) #Debug
   card, quantity = askCard("[Type] = 'Setup'")
   if quantity == 0: return
   table.create(card, x, y, quantity)

def createSDF(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> createSDF(){}".format(extraASDebug())) #Debug
   table.create("98a40fb6-1fea-4283-a036-567c8adade8e", x, y, 1, True)
   
#------------------------------------------------------------------------------
# Run...
#------------------------------------------------------------------------------
def intRun(ActionCost, Name):
   if debugVerbosity >= 1: notify(">>> intRun(){}".format(extraASDebug())) #Debug
   notify ("{} to start a run on {}.".format(ActionCost,Name))

def runHQ(group, x=0,Y=0):
   if debugVerbosity >= 1: notify(">>> runHQ(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "HQ")

def runRD(group, x=0,Y=0):
   if debugVerbosity >= 1: notify(">>> runRD(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "R&D")

def runArchives(group, x=0,Y=0):
   if debugVerbosity >= 1: notify(">>> runArchives(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun (ActionCost, "the Archives")

def runSDF(group, x=0,Y=0):
   if debugVerbosity >= 1: notify(">>> runSDF(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "a subsidiary data fort")

#------------------------------------------------------------------------------
# Tags...
#------------------------------------------------------------------------------
def pay2andDelTag(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> pay2andDelTag(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   if ds != "runner":
      whisper("Only runners can use this action")
      return
   if me.Tags < 1: 
      whisper("You don't have any tags")
      return
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   dummyCard = getSpecial('Tracing') # Just a random card to pass to the next function. Can't be bothered to modify the function to not need this.
   reduction = reduceCost(dummyCard, 'DelTag', 2)
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))
   if payCost(2 - reduction) == "ABORT": 
      me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   me.counters['Tags'].value -= 1
   notify ("{} and pays {}{} to lose a tag.".format(ActionCost,uniBit(2 - reduction),extraText))

#------------------------------------------------------------------------------
# Markers
#------------------------------------------------------------------------------
def intAddBits ( card, count):
   if debugVerbosity >= 1: notify(">>> intAddBits(){}".format(extraASDebug())) #Debug
   mute()
   if ( count > 0):
      card.markers[Bits] += count
      if ( card.isFaceUp == True): notify("{} adds {} from the bank on {}.".format(me,uniBit(count),card))
      else: notify("{} adds {} on a card.".format(me,uniBit(count)))

def addBits(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addBits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many Bits?", 1)
   if count == None: return
   intAddBits(card, count)
	
def remBits(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> remBits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Bits?", 1)
   if count == None: return
   if count > card.markers[Bits]: count = card.markers[Bits]
   card.markers[Bits] -= count
   if card.isFaceUp == True: notify("{} removes {} from {}.".format(me,uniBit(count),card))
   else: notify("{} removes {} from a card.".format(me,uniBit(count)))

def remBits2BP (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> remBits2BP(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Bits?", 1)
   if count == None: return
   if count > card.markers[Bits]: count = card.markers[Bits]
   card.markers[Bits] -= count
   me.counters['Bit Pool'].value += count 
   if card.isFaceUp == True: notify("{} removes {} from {} to their Bit Pool.".format(me,uniBit(count),card))
   else: notify("{} takes {} from a card to their Bit Pool.".format(me,uniBit(count)))

def addPlusOne(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addPlusOne(){}".format(extraASDebug())) #Debug
   mute()
   if MinusOne in card.markers:
      card.markers[MinusOne] -= 1
   else: 
      card.markers[PlusOne] += 1
   notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addMinusOne(){}".format(extraASDebug())) #Debug
   mute()
   if PlusOne in card.markers:
      card.markers[PlusOne] -= 1
   else:
      card.markers[MinusOne] += 1
   notify("{} adds one -1 marker on {}.".format(me,card))

def addMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
   if debugVerbosity >= 1: notify(">>> addMarker(){}".format(extraASDebug())) #Debug
   mute()
   marker, quantity = askMarker() # Ask the player how many of the same type they want.
   if quantity == 0: return
   for card in cards: # Then go through their cards and add those markers to each.
      card.markers[marker] += quantity
      notify("{} adds {} {} counter to {}.".format(me, quantity, marker[0], card))	

#------------------------------------------------------------------------------
# advancing cards
#------------------------------------------------------------------------------
def advanceCardP(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> advanceCardP(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   reduction = reduceCost(card, 'Advance', 1)
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))
   if payCost(1 - reduction) == "ABORT": 
      me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   card.markers[Advance] += 1
   if card.isFaceUp: notify("{} and paid {}{} to advance {}.".format(ActionCost,uniBit(1 - reduction),extraText,card))
   else: notify("{} and paid {}{} to advance a card.".format(ActionCost,uniBit(1 - reduction),extraText))

def addXadvancementCounter(card, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> addXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many counters?", 1)
   if count == None: return
   card.markers[mdict['Advance']] += count
   if card.isFaceUp == True: notify("{} adds {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> delXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many counters?", 1)
   if count == None: return
   if count > card.markers[Advance]: count = card.markers[Advance]
   card.markers[Advance] -= count
   if card.isFaceUp == True: notify("{} removes {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def advanceCardM(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> advanceCardM(){}".format(extraASDebug())) #Debug
   mute()
   card.markers[mdict['Advance']] -= 1
   if (card.isFaceUp == True): notify("{} removes 1 advancement counter on {}.".format(me,card))
   else: notify("{} removes 1 advancement counter on a card.".format(me))

#---------------------
# Trace
#----------------------

def inputTraceValue (card, x=0,y=0, limit = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> inputTraceValue(){}".format(extraASDebug())) #Debug
   global TraceValue
   mute()
   limitText = ''
   betReplaced = False
   card = getSpecial('Tracing')
   if not card.isFaceUp and not confirm("You're already placed a bet. Replace it with a new one?"): return
   else: betReplaced = True
   limit = num(limit) # Just in case
   if debugVerbosity >= 3: notify("### Trace Limit: {}".format(limit))
   if limit > 0: limitText = '\n\n(Max Trace Power: {})'.format(limit)
   TraceValue = askInteger("Bet How Many?{}".format(limitText), 0)
   if TraceValue == None: 
      whisper(":::Warning::: Trace bid aborted by player.")
      return 'ABORT'
   while limit > 0 and TraceValue > limit:
      TraceValue = askInteger("Please bet equal or less than the max trace power!\nBet How Many?{}".format(limitText), 0)
      if TraceValue == None: 
         whisper(":::Warning::: Trace bid aborted by player.")
         return 'ABORT'
   card.markers[Bits] = 0
   card.isFaceUp = False
   if not silent: 
      if not betReplaced: notify("{} chose a Trace Value.".format(me))
      else: notify("{} changed their hidden Trace Value.".format(me))
   Stored_Type[card] = "Tracing"
	
def revealTraceValue (card, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> revealTraceValue(){}".format(extraASDebug())) #Debug
   mute()
   global TraceValue
   card = getSpecial('Tracing')
   card.isFaceUp = True
   card.markers[Bits] = TraceValue
   notify ( "{} reveals a Trace Value of {}.".format(me,TraceValue))
   if TraceValue == 0: autoscriptOtherPlayers('TraceAttempt') # if the trace value is 0, then we consider the trace attempt as valid, so we call scripts triggering from that.
   TraceValue = 0

def payTraceValue (card, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> payTraceValue(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   card = getSpecial('Tracing')
   reduction = reduceCost(card, 'Trace', card.markers[Bits])
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))
   if payCost(card.markers[Bits] - reduction)  == 'ABORT': return
   notify ("{} pays {} for the Trace Value{}.".format(me,uniBit(card.markers[Bits]),extraText))
   card.markers[Bits] = 0
   autoscriptOtherPlayers('TraceAttempt')

def cancelTrace ( card, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> cancelTrace(){}".format(extraASDebug())) #Debug
   mute()
   card.isFaceUp = True
   TraceValue = 0
   card.markers[Bits] = 0
   notify ("{} cancels the Trace Value.".format(me) )

#------------------------------------------------------------------------------
# Counter & Damage Functions
#-----------------------------------------------------------------------------

def payCost(count = 1, cost = 'not_free', counter = 'BP'): # A function that removed the cost provided from our bit pool, after checking that we have enough.
   if debugVerbosity >= 1: notify(">>> payCost(){}".format(extraASDebug())) #Debug
   if cost == 'free': return 'free'
   count = num(count)
   if count <= 0 : return 0# If the card has 0 cost, there's nothing to do.
   if counter == 'BP':
      if me.counters['Bit Pool'].value < count and not confirm("You do not seem to have enough Bits in your pool to take this action. Are you sure you want to proceed? \
         \n(If you do, your Bit Pool will go to the negative. You will need to increase it manually as required.)"): return 'ABORT' # If we don't have enough Bits in the pool, we assume card effects or mistake and notify the player that they need to do things manually.
      me.counters['Bit Pool'].value -= count
   elif counter == 'AP': # We can also take costs from other counters with this action.
      if me.counters['Agenda Points'].value < count and not confirm("You do not seem to have enough Agenda Points to take this action. Are you sure you want to proceed? \
         \n(If you do, your Agenda Points will go to the negative. You will need to increase them manually as required.)"): return 'ABORT'
      me.counters['Agenda Points'].value -= count
   return uniBit(count)

def reduceCost(card, type = 'Rez', fullCost = 0):
   if debugVerbosity >= 1: notify(">>> reduceCost(). Action is: {}".format(type)) #Debug
   #confirm("Bump ReduceCost") # Debug
   reduction = 0
   for c in table:
      Autoscripts = c.AutoScript.split('||')
      for autoS in Autoscripts:
         if debugVerbosity >= 3: notify("### Checking {} with AS: {}".format(c, autoS)) #Debug
         reductionSearch = re.search(r'Reduce([0-9#]+)Cost({}|All)-for([A-Z][A-Za-z ]+)(-not[A-Za-z_& ]+)?'.format(type), autoS) 
         if c.controller == me and reductionSearch and c.markers[Not_rezzed] == 0 and c.isFaceUp: # If the above search matches (i.e. we have a card with reduction for Rez and a condition we continue to check if our card matches the condition)
            if debugVerbosity >= 4: notify("### Possible Match found in {}".format(c)) # Debug         
            if reductionSearch.group(4): 
               exclusion = re.search(r'-not([A-Za-z_& ]+)'.format(type), reductionSearch.group(4))
               if exclusion and (re.search(r'{}'.format(exclusion.group(1)), Stored_Type[card]) or re.search(r'{}'.format(exclusion.group(1)), Stored_Keywords[card])): continue
            if reductionSearch.group(3) == 'All' or re.search(r'{}'.format(reductionSearch.group(3)), Stored_Type[card]) or re.search(r'{}'.format(reductionSearch.group(3)), Stored_Keywords[card]): #Looking for the type of card being reduced into the properties of the card we're currently paying.
               if debugVerbosity >= 3: notify(" ### Search match! Group is {}".format(reductionSearch.group(1))) # Debug
               if reductionSearch.group(1) != '#':
                  reduction += num(reductionSearch.group(1)) # if there is a match, the total reduction for this card's cost is increased.
               else: 
                  while fullCost > 0 and c.markers[mdict['Bits']] > 0: 
                     reduction += 1
                     fullCost -= 1
                     c.markers[mdict['Bits']] -= 1
                     if fullCost == 0: break
   return reduction

def intdamageDiscard(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> intdamageDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0:
      notify ("{} cannot discard at random. Have they flatlined?".format(me))
   else:
      card = group.random()
      if ds == 'corp': card.moveTo(me.piles['Archives(Hidden)'])
      else: card.moveTo(me.piles['Trash/Archives(Face-up)'])
      notify("{} discards {} at random.".format(me,card))

def addBrainDmg(group, x = 0, y = 0):
   mute()
   if debugVerbosity >= 1: notify(">>> addBrainDmg(){}".format(extraASDebug())) #Debug
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(1, 'Brain', me): # If we find any defense against it, inform that it was prevented
      notify ("{} prevents 1 Brain Damage.".format(me))
   else: 
      applyBrainDmg()
      notify ("{} suffers 1 Brain Damage.".format(me) )
      intdamageDiscard(me.hand)

def applyBrainDmg(player = me):
   if debugVerbosity >= 1: notify(">>> applyBrainDmg(){}".format(extraASDebug())) #Debug
   specialCard = getSpecial('Counter Hold', player)
   specialCard.markers[mdict['BrainDMG']] += 1
   
def addMeatDmg(group, x = 0, y = 0):
   mute()
   if debugVerbosity >= 1: notify(">>> addMeatDmg(){}".format(extraASDebug())) #Debug
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(1, 'Meat', me):
      notify ("{} prevents 1 Meat Damage.".format(me))
   else: 
      notify ("{} suffers 1 Meat Damage.".format(me))
      intdamageDiscard(me.hand)

def addNetDmg(group, x = 0, y = 0):
   mute()
   if debugVerbosity >= 1: notify(">>> addNetDmg(){}".format(extraASDebug())) #Debug
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(1, 'Net', me):
      notify ("{} prevents 1 Net Damage.".format(me))
   else: 
      notify ("{} suffers 1 Net Damage.".format(me))
      intdamageDiscard(me.hand)
      
def getBit(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> getBit(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   bitsReduce = findCounterPrevention(1, 'Bits', me)
   if bitsReduce: extraTXT = " ({} forfeited)".format(uniBit(bitsReduce))
   else: extraTXT = ''
   notify ("{} and receives {}{}.".format(ActionCost,uniBit(1 - bitsReduce),extraTXT))
   me.counters['Bit Pool'].value += 1 - bitsReduce
    
#------------------------------------------------------------------------------
# Card Actions
#------------------------------------------------------------------------------
   
def scrAgenda(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> scrAgenda(){}".format(extraASDebug())) #Debug
   global Stored_Type, Stored_Keywords, Stored_AutoActions, scoredAgendas
   mute()
   cheapAgenda = False
   if card.markers[mdict['Scored']] > 0: 
      notify ("This agenda has already been scored")
      return
   if ds == 'runner' and card.Type != "Agenda" and not card.isFaceUp:
      card.isFaceUp = True
      random = rnd(100,1000) # Hack Workaround
      if card.Type != "Agenda":
         whisper ("You can only score Agendas")
         card.isFaceUp = False
         return
   if ds == 'runner': 
      Stored_Type[card] = card.Type
      Stored_Keywords[card] = getKeywords(card)
      Stored_AutoActions[card] = card.AutoAction
      agendaTxt = "liberate"
   else: agendaTxt = "score"
   if Stored_Type[card] == "Agenda":
      if ds == 'corp' and card.markers[mdict['Advance']] < num(Stored_Cost[card]):
         if confirm("You have not advanced this agenda enough to score it. Bypass?"): 
            cheapAgenda = True
            currentAdv = card.markers[mdict['Advance']]
         else: return
      elif not confirm("Do you want to {} this agenda?".format(agendaTxt)): return
      card.isFaceUp = True
      if chkTargeting(card) == 'ABORT': 
         card.isFaceUp = False
         notify("{} cancels their action".format(me))
         return
      ap = num(card.Stat)
      card.markers[mdict['Not_rezzed']] = 0
      card.markers[mdict['Scored']] += 1
      apReduce = findCounterPrevention(ap, 'Agenda Points', me)
      if apReduce: extraTXT = " ({} forfeited)".format(apReduce)
      else: extraTXT = ''      
      me.counters['Agenda Points'].value += ap - apReduce
      card.moveToTable(-600 - scoredAgendas * cwidth(card) / 6, 60 - yaxisMove(card) + scoredAgendas * cheight(card) / 2 * playerside, False)
      scoredAgendas += 1
      notify("{} {}s {} and receives {} agenda point(s){}".format(me, agendaTxt, card, ap - apReduce,extraTXT))
      if cheapAgenda: notify(":::Warning:::{} did not have enough advance tokens ({} out of {})! ".format(card,currentAdv,card.Cost))
      executeAutomations(card,agendaTxt)
      if me.counters['Agenda Points'].value >= 7 : notify("{} wins the game!".format(me))
      card.markers[mdict['Advance']] = 0 # We only want to clear the advance counters after the automations, as they may still be used.
   else:
      whisper ("You can't score this card")

def isRezzable (card):
   if debugVerbosity >= 1: notify(">>> isRezzable(){}".format(extraASDebug())) #Debug
   mute()
   Type = Stored_Type[card]
   if Type == "Ice" or Type == "Node" or Type == "Upgrade": return True
   else: return False

def intRez (card, cost = 'not free', x=0, y=0, silent = False):
   if debugVerbosity >= 1: notify(">>> intRez(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   rc = ''
   if card.markers[Not_rezzed] == 0: 
      whisper("you can't rez a rezzed card")
      return 'ABORT'
   if not isRezzable(card): 
      whisper("Not a rezzable card")
      return 'ABORT'
   if chkTargeting(card) == 'ABORT': 
      notify("{} cancels their action".format(me))
      return
   reduction = reduceCost(card, 'Rez', num(Stored_Cost[card]))
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))
   rc = payCost(num(Stored_Cost[card]) - reduction, cost)
   if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == "free": extraText = " at no cost"
   elif rc != 0: rc = "for {}".format(rc)
   else: rc = ''
   card.isFaceUp = True
   card.markers[Not_rezzed] -= 1
   if not silent:
      if card.Type == 'Ice': notify("{} has rezzed {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Node': notify("{} has acquired {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Upgrade': notify("{} has installed {} {}{}.".format(me, card, rc, extraText))
   random = rnd(10,100) # Bug workaround.
   executeAutomations(card,'rez')
    

def rezForFree (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rezForFree(){}".format(extraASDebug())) #Debug
   intRez(card, "free")

def derez(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> derez(){}".format(extraASDebug())) #Debug
   mute()
   if card.markers[Not_rezzed] == 0:
      if not isRezzable(card): 
         whisper ("Not a rezzable card")
         return 'ABORT'
      else:
         card.markers[Bits] = 0
         card.markers[Not_rezzed] += 1
         if not silent: notify("{} derezzed {}".format(me, card))
         executeAutomations(card,'derez')
   else:
      notify ( "you can't derez a unrezzed card")
      return 'ABORT'
      

def expose(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> expose(){}".format(extraASDebug())) #Debug
   if not card.isFaceUp:
      mute()
      card.isFaceUp = True
      if not silent: notify("{} exposed {}".format(me, card))
   else:
      notify("This card is already exposed")
      return 'ABORT'

def rolld6(group = table, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> rolld6(){}".format(extraASDebug())) #Debug
   mute()
   n = rnd(1, 6)
   if not silent: notify("{} rolls {} on a 6-sided die.".format(me, n))
   return n

def selectAsTarget (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> selectAsTarget(){}".format(extraASDebug())) #Debug
   card.target(True)

def clear(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> clear(){}".format(extraASDebug())) #Debug
   mute()
   notify("{} clears {}.".format(me, card))
   if card.highlight != DummyColor :card.highlight = None
   card.markers[mdict['BaseLink']] = 0
   card.markers[mdict['PlusOne']] = 0
   card.markers[mdict['MinusOne']] = 0
   card.target(False)

def intTrashCard(card, stat, cost = "not free",  ActionCost = '', silent = False):
   if debugVerbosity >= 1: notify(">>> intTrashCard(){}".format(extraASDebug())) #Debug
   global trashEasterEggIDX, DummyTrashWarn
   mute()
   MUtext = ""
   rc = ''
   extraText = ''
   if ActionCost == '': 
      ActionCost = '{} '.format(me) # If not actions were used, then just announce our name.
      goodGrammar = 'es' # LOL Grammar Nazi
   else: 
      ActionCost += ' and '
      goodGrammar = ''
   cardowner = card.owner
   if card.Type == "Tracing" or card.Type == "Counter Hold" or card.Type == "Data Fort": 
      whisper("{}".format(trashEasterEgg[trashEasterEggIDX]))
      if trashEasterEggIDX < 7:
         trashEasterEggIDX += 1
         return 'ABORT'
      elif trashEasterEggIDX == 7: 
         card.moveToBottom(cardowner.piles['Trash/Archives(Face-up)'])
         trashEasterEggIDX = 0
         return
   if card.highlight == DummyColor and DummyTrashWarn and not confirm(":::Warning!:::\n\nYou are about to trash a dummy card. You will not be able to restore it without using the effect that created it originally.\n\nAre you sure you want to proceed? (This message will not appear again)"): 
      DummyTrashWarn = False
      return
   else: DummyTrashWarn = False
   reduction = reduceCost(card, 'Trash', stat)
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))    
   rc = payCost(num(stat) - reduction, cost)
   if rc == "ABORT": return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == 0: 
      if ActionCost.endswith(' and'): ActionCost[:-len(' and')] # if we have no action cost, we don't need the connection.
   else: 
      ActionCost += "pays {} to".format(rc) # If we have Bit cost, append it to the Action cost to be announced.
      goodGrammar = ''
   if card.isFaceUp:
      if num(card.properties["MU Required"]) > 0 and not card.markers[mdict['DaemonMU']]:
         cardowner.Memory += num(card.properties["MU Required"])
         MUtext = ", freeing up {} MUs".format(card.properties["MU Required"])
      if rc == "free" and not silent: notify("{} trashed {} at no cost{}.".format(me, card, MUtext))
      elif not silent: notify("{} trash{} {}{}{}.".format(ActionCost, goodGrammar, card, extraText, MUtext))
      executeAutomations(card,'trash')
      card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
   elif (ds == "runner" and cardowner == me) or (ds == "corp" and cardowner != me ): #I'm the runner and I trash my card or I 'm the corp and I trash a runner card
      card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
      if rc == "free" and not silent: notify ("{} trashed {} at no cost.".format(me,card))
      elif not silent: notify("{} trash{} {}{}.".format(ActionCost, goodGrammar, card, extraText))
   else: #I'm the corp and I trash my card or I'm the runner and I trash a corp's card
      card.moveTo(cardowner.piles['Archives(Hidden)'])
      if rc == "free" and not silent: notify("{} trashed a hidden card at no cost.".format(me))
      elif not silent: notify("{} trash{} a hidden card.".format(ActionCost, goodGrammar))

def trashCard (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> trashCard(){}".format(extraASDebug())) #Debug
   intTrashCard(card, card.Stat)
        
def trashForFree (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> trashForFree(){}".format(extraASDebug())) #Debug
   intTrashCard(card, card.Stat, "free")

def pay2AndTrash(card, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> pay2AndTrash(){}".format(extraASDebug())) #Debug
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   intTrashCard(card, 2, ActionCost = ActionCost)

def exileCard(card, silent = False):
   if debugVerbosity >= 1: notify(">>> exileCard(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the shared pile and outside of view.
   mute()
   if card.Type == "Tracing" or card.Type == "Counter Hold" or card.Type == "Data Fort": 
      whisper("This kind of card cannot be exiled!")
      return 'ABORT'
   elif card.owner != me:
      whisper("You can only exile your own cards!")
      return 'ABORT'   
   else:
      if card.isFaceUp and num(card.properties["MU Required"]) > 0 and not card.markers[mdict['DaemonMU']]:
         card.owner.Memory += num(card.properties["MU Required"])      
      executeAutomations(card,'trash')
      card.moveTo(shared.exile)
   if not silent: notify("{} exiled {}.".format(me,card))
   
   
def uninstall(card, destination = 'hand', silent = False):
   if debugVerbosity >= 1: notify(">>> uninstall(){}".format(extraASDebug())) #Debug
   # Returns an installed card into our hand.
   mute()
   if destination == 'R&D' or destination == 'Stack': group = me.piles['R&D/Stack']
   else: group = me.hand
   #confirm("destination: {}".format(destination)) # Debug
   if card.Type == "Tracing" or card.Type == "Counter Hold" or card.Type == "Data Fort": 
      whisper("This kind of card cannot be uninstalled!")
      return 'ABORT'
   elif card.owner != me:
      whisper("You can only uninstall your own cards!")
      return 'ABORT'   
   else: 
      if card.isFaceUp and num(card.properties["MU Required"]) > 0 and not card.markers[mdict['DaemonMU']]:
         card.owner.Memory += num(card.properties["MU Required"])      
      executeAutomations(card,'uninstall')
      card.moveTo(group)
   if not silent: notify("{} uninstalled {}.".format(me,card))

def possess(daemonCard, programCard, silent = False):
   if debugVerbosity >= 1: notify(">>> possess(){}".format(extraASDebug())) #Debug
   #This function takes as arguments 2 cards. A Daemon and a program requiring MUs, then assigns the program to the Daemon, restoring the used MUs to the player.
   count = num(programCard.properties["MU Required"])
   if count > daemonCard.markers[mdict['DaemonMU']]:
      whisper("{} does not have enough free MUs to possess {}.".format(daemonCard, programCard))
      return 'ABORT'
   elif programCard.markers[mdict['DaemonMU']]:
      whisper("{} is already possessed by a daemon.".format(programCard))
      return 'ABORT'
   else: 
      daemonCard.markers[mdict['DaemonMU']] -= count
      programCard.markers[mdict['DaemonMU']] += count
      programCard.owner.Memory += count # We return the MUs the card would be otherwise using.
      if not silent: notify("{} installs {} into {}".format(me,programCard,daemonCard))

      
def useCard(card,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> useCard(){}".format(extraASDebug())) #Debug
   if card.highlight == None:
      card.highlight = SelectColor
      notify ( "{} uses the ability of {}.".format(me,card) )
   else:
      if card.highlight == DummyColor:
         if not confirm("This highlight signifies that this card is technically trashed\
                       \nIn other words, this is a dummy card to signify a lingering effect left behind\
                       \nClearing this dummy card will automatically remove it from the game.\
                     \n\nAre you sure you want to continue?"):
            return
         else: card.moveTo(me.piles['Trash/Archives(Face-up)'])
      notify("{} clears {}.".format(me, card))
      card.highlight = None
      card.target(False)

def rulings(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rulings(){}".format(extraASDebug())) #Debug
   mute()
   if not card.isFaceUp: return
   #openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))
   openUrl('http://www.netrunneronline.com/search/?q={}'.format(card.name)) # Errata is not filled in most card so this works better until then

def checkUnique (card):
   if debugVerbosity >= 1: notify(">>> checkUnique(){}".format(extraASDebug())) #Debug
   mute()
   if not re.search(r'Unique', getKeywords(card)): return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and c.name == card.name and re.search(r'Unique', getKeywords(c)) ]
   if len(ExistingUniques) != 0 and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be trashed at no cost)".format(card.name)) : return False
   else:
      for uniqueC in ExistingUniques: trashForFree(uniqueC)
   return True   
   
def oncePerTurn(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> oncePerTurn(){}".format(extraASDebug())) #Debug
   mute()
   if card.orientation == Rot90:
      if not confirm("The once-per-turn ability of {} has already been used this turn\nBypass restriction?.".format(card.name)): return 'ABORT'
      else: 
         if not silent: notify('{} activates the once-per-turn ability of {} another time'.format(me, card))
   else:
      if not silent: notify('{} activates the once-per-turn ability of {}'.format(me, card))
   card.orientation = Rot90
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def currentHandSize(player = me):
   if debugVerbosity >= 1: notify(">>> currentHandSizel(){}".format(extraASDebug())) #Debug
   specialCard = getSpecial('Counter Hold', player)
   if specialCard.markers[mdict['BrainDMG']]: currHandSize =  player.counters['Max Hand Size'].value - specialCard.markers[mdict['BrainDMG']]
   else: currHandSize = player.counters['Max Hand Size'].value
   return currHandSize

def intPlay(card, cost = 'not_free'):
   if debugVerbosity >= 1: notify(">>> intPlay(){}".format(extraASDebug())) #Debug
   global Stored_Type, Stored_Cost, Stored_Keywords,Stored_AutoActions
   extraText = ''
   mute() 
   chooseSide() # Just in case...
   if (card.Type == 'Operation' or card.Type == 'Prep') and chkTargeting(card) == 'ABORT': return # If it's an Operation or Prep and has targeting requirements, check with the user first.
   if re.search(r'Double', getKeywords(card)): NbReq = 2 # Some cards require two actions to play. This variable is passed to the useAction() function.
   else: NbReq = 1 #In case it's not a "Double" card. Then it only uses one action to play.
   ActionCost = useAction(count = NbReq)
   if ActionCost == 'ABORT': return  #If the player didn't have enough actions and opted not to proceed, do nothing.
   if checkUnique(card) == False: return #If the player has the unique card and opted not to trash it, do nothing.
   if not checkNotHardwareDeck(card): return	#If player already has a deck in play and doesnt want to play that card, do nothing.
   Stored_Type[card] = card.Type
   Stored_Keywords[card] = getKeywords(card)
   Stored_Cost[card] = card.Cost
   Stored_AutoActions[card] = card.AutoAction
   if card.Type == 'Prep' or card.Type == 'Operation': action = 'Play'
   else: action = 'Install'
   MUtext = ''
   rc = ''
   if card.Type == 'Resource' and re.search(r'Hidden', getKeywords(card)): hiddenresource = 'yes'
   else: hiddenresource = 'no'
   if card.Type == 'Ice' or card.Type == 'Agenda' or card.Type == 'Node' or (card.Type == 'Upgrade' and not re.search(r'Region', getKeywords(card))):
      card.moveToTable(-180, 160 * playerside - yaxisMove(card), True) # Agendas, Nodes and non-region Upgrades all are played to the same spot now.
      if Stored_Type[card] == 'Ice': 
         card.orientation ^= Rot90
         card.moveToTable(-180, 65 * playerside - yaxisMove(card), True) # Ice are moved a bit more to the front and played sideways.
      card.markers[Not_rezzed] += 1
      notify("{} to install a card.".format(ActionCost))
   elif card.Type == 'Program' or card.Type == 'Prep' or card.Type == 'Resource' or card.Type == 'Hardware':
      if num(card.properties["MU Required"]) > 0:
         me.Memory -= num(card.properties["MU Required"])
         MUtext = ", using up {} MUs".format(card.properties["MU Required"])
      if card.Type == 'Resource' and hiddenresource == 'yes':
         card.moveToTable(-180, 230 * playerside - yaxisMove(card), True)
         notify("{} to install a hidden resource.".format(ActionCost))
         executeAutomations(card,action.lower())
         return
      reduction = reduceCost(card, action, num(card.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
      if reduction: extraText = " (reduced by {})".format(uniBit(reduction)) #If it is, make sure to inform.
      rc = payCost(num(card.Cost) - reduction, cost)
      if rc == "ABORT": 
         me.Actions += NbReq # If the player didn't notice they didn't have enough bits, we give them back their action
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = ''
      if card.Type == 'Program':
         card.moveToTable(-150, 65 * playerside - yaxisMove(card), False)
         for targetLookup in table: # We check if we're targeting a daemon to install the program in.
            if targetLookup.targetedBy and targetLookup.targetedBy == me and re.search(r'Daemon',getKeywords(targetLookup)) and possess(targetLookup, card, silent = True) != 'ABORT':
               MUtext = ", installing it into {}".format(targetLookup)
               break         
         notify("{}{} to install {}{}{}.".format(ActionCost, rc, card, extraText,MUtext))
      elif card.Type == 'Prep':
         card.moveToTable(0, 0 - yaxisMove(card), False)
         notify("{}{} to prep with {}{}.".format(ActionCost, rc, card, extraText))
      elif card.Type == 'Hardware':
         card.moveToTable(-210, 160 * playerside - yaxisMove(card), False)
         notify("{}{} to purchase {}{}{}.".format(ActionCost, rc, card, extraText,MUtext))
      elif card.Type == 'Resource' and hiddenresource == 'no':
         card.moveToTable(180, 240 * playerside - yaxisMove(card), False)
         notify("{}{} to acquire {}{}{}.".format(ActionCost, rc, card, extraText,MUtext))
      else:
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to play {}{}{}.".format(ActionCost, rc, card, extraText,MUtext))
   else:
      reduction = reduceCost(card, action, num(card.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
      if reduction: extraText = " (reduced by {})".format(uniBit(reduction)) #If it is, make sure to inform.
      rc = payCost(num(card.Cost) - reduction, cost)
      if rc == "ABORT": 
         me.Actions += NbReq # If the player didn't notice they didn't have enough bits, we give them back their action
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = '' # When the cast costs nothing, we don't include the cost.
      if card.Type == 'Operation':
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to initiate {}{}.".format(ActionCost, rc, card, extraText))
      elif card.Type == 'Upgrade' and re.search(r'Region', getKeywords(card)):
         card.moveToTable(-220, 240 * playerside - yaxisMove(card), False)
         notify("{}{} to open a base of operations in {}{}.".format(ActionCost, rc, card, extraText))
      else:
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to play {}{}.".format(ActionCost, rc, card, extraText))           
   executeAutomations(card,action.lower())

def chkTargeting(card):
   if debugVerbosity >= 1: notify(">>> chkTargeting(){}".format(extraASDebug())) #Debug
   global ExposeTargetsWarn, RevealandShuffleWarn
   if re.search(r'Targeted', card.AutoScript) and not findTarget(card.AutoScript) and not confirm("This card requires a valid target for it to work correctly.\
                                                                                                 \nIf you proceed without a target, strange things might happen.\
                                                                                               \n\nProceed anyway?"): return 'ABORT'
   if re.search(r'isExposeTarget', card.AutoScript) and ExposeTargetsWarn:
      if confirm("This card will automatically provide a bonus depending on how many non-exposed derezzed cards you've selected.\
                \nMake sure you've selected all the cards you wish to expose and have peeked at them before taking this action\
                \nSince this is the first time you take this action, you have the opportunity now to abort and select your targets before traying it again.\
              \n\nDo you want to abort this action?\
                \n(This message will not appear again)"): 
         ExposeTargetsWarn = False
         return 'ABORT'
      else: ExposeTargetsWarn = False # Whatever happens, we don't show this message again. 
   if re.search(r'Reveal&Shuffle', card.AutoScript) and RevealandShuffleWarn:
      if confirm("This card will automatically provide a bonus depending on how many cards you selected to reveal (i.e. place on the table) from your hand.\
                \nMake sure you've selected all the cards (of any specific type required) you wish to reveal to the other players\
                \nSince this is the first time you take this action, you have the opportunity now to abort and select your targets before trying it again.\
              \n\nDo you want to abort this action?\
                \n(This message will not appear again)"): 
         RevealandShuffleWarn = False
         return 'ABORT'
      else: RevealandShuffleWarn = False # Whatever happens, we don't show this message again. 
   if re.search(r'HandTarget', card.AutoScript) or re.search(r'HandTarget', card.AutoAction):
      hasTarget = False
      for c in me.hand:
         if c.targetedBy and c.targetedBy == me: hasTarget = True
      if not hasTarget: 
         whisper(":::Warning::: This card effect requires that you have one of more cards targeted from your hand. Aborting!")
         return 'ABORT'

def checkNotHardwareDeck (card):
   if debugVerbosity >= 1: notify(">>> checkNotHardwareDeck(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type != "Hardware" or not re.search(r'Deck', getKeywords(card)): return True
   ExistingDecks = [ c for c in table
         if c.owner == me and c.isFaceUp and re.search(r'Deck', getKeywords(c)) ]
   if len(ExistingDecks) != 0 and not confirm("You already have at least one hardware deck in play. Are you sure you want to install {}?\n\n(If you do, your installed Decks will be automatically trashed at no cost)".format(card.name)): return False
   else: 
      for HWDeck in ExistingDecks: trashForFree(HWDeck)
   return True   
   
def playForFree(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> playForFree(){}".format(extraASDebug())) #Debug
   intPlay(card,"free")

def movetoTopOfStack(card):
   if debugVerbosity >= 1: notify(">>> movetoTopOfStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   card.moveTo(deck)
   notify ("{} moves a card to top of their {}.".format(me,pileName(deck)))

def movetoBottomOfStack(card):
   if debugVerbosity >= 1: notify(">>> movetoBottomOfStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   card.moveToBottom(deck)
   notify ("{} moves a card to Bottom of their {}.".format(me,pileName(deck)))

def handtoArchives(card):
   if debugVerbosity >= 1: notify(">>> handtoArchives(){}".format(extraASDebug())) #Debug
   if ds == "runner": return
   mute()
   card.moveTo(me.piles['Trash/Archives(Face-up)'])
   notify ("{} moves a card to their face-up Archives.".format(me))

def handDiscard(card):
   if debugVerbosity >= 1: notify(">>> handDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if ds == "runner": 
      card.moveTo(me.piles['Trash/Archives(Face-up)'])
      if endofturn: 
         if card.Type == 'Program': notify("{} has killed a hanging process.".format(me))
         elif card.Type == 'Prep': notify("{} has thrown away some notes.".format(me))
         elif card.Type == 'Hardware': notify("{} has deleted some spam mail.".format(me))
         elif card.Type == 'Resource': notify("{} has reconfigured some net protocols.".format(me))
         else: notify("{} has power cycled some hardware.".format(me))
         if len(me.hand) == currentHandSize(): 
            notify("{} has now discarded down to their max handsize of {}".format(me, currentHandSize()))
      else: notify("{} discards {}.".format(me,card))
   else:
      card.moveTo(me.piles['Archives(Hidden)'])
      if endofturn: 
         random = rnd(1, 5)
         if random == 1: notify("{}'s Internal Audit has corrected some tax book discrepancies.".format(me))
         if random == 2: notify("{} has downsized a department.".format(me))
         if random == 3: notify("{}'s Corporation has sent some hardware to secure recycling.".format(me))
         if random == 4: notify("{} has sold off some stock options".format(me))
         if random == 5: notify("{} has liquidated some assets.".format(me))
         if len(me.hand) == currentHandSize(): 
            notify("{} has now discarded down to their max handsize of {}".format(me, currentHandSize()))
      else: notify("{} discards a card.".format(me))
    
def handRandomDiscard(group, count = None, player = None, destination = None, silent = False):
   if debugVerbosity >= 1: notify(">>> handRandomDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if not player: player = me
   if not destination: 
      if ds == "runner": destination = player.piles['Trash/Archives(Face-up)']
      else: destination = player.piles['Archives(Hidden)']
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Discard how many cards?", 1)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your hand to complete this action. Will discard as many as possible")   
   for iter in range(count):
      if debugVerbosity >= 4: notify("#### : handRandomDiscard() iter: {}".format(iter + 1)) # Debug
      card = group.random()
      if card == None: return iter + 1 # If we have no more cards, then return how many we managed to discard.
      card.moveTo(destination)
      if not silent: notify("{} discards {} at random.".format(player,card))
   if debugVerbosity >= 2: notify("<<< handRandomDiscard() with return {}".format(iter + 1)) #Debug
   return iter + 1 #We need to increase the iter by 1 because it starts iterating from 0
    		
def showatrandom(group):
   if debugVerbosity >= 1: notify(">>> showatrandom(){}".format(extraASDebug())) #Debug
   mute()
   card = group.random()
   if card == None: return
   card.moveToTable(0, 0 - yaxisMove(card), False)
   notify("{} show {} at random.".format(me,card))

def handtoStack (group, silent = False):
   if debugVerbosity >= 1: notify(">>> handtoStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   for c in group: c.moveTo(deck)
   if not silent: notify ("{} moves their whole {} to their {}.".format(me,pileName(group),pileName(deck)))
   else: return(pileName(group),pileName(deck),len(group)) # Return a tuple with the names of the groups.


#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------
def shuffle(group):
   if debugVerbosity >= 1: notify(">>> shuffle(){}".format(extraASDebug())) #Debug
   group.shuffle()

def draw(group):
   if debugVerbosity >= 1: notify(">>> draw(){}".format(extraASDebug())) #Debug
   global newturn
   mute()
   if len(group) == 0: return
   if ds == 'corp' and newturn: 
      group[0].moveTo(me.hand)
      notify("--> {} perform's the turn's mandatory draw.".format(me))
      newturn = False
   else:
      ActionCost = useAction()
      if ActionCost == 'ABORT': return
      group[0].moveTo(me.hand)
      notify("{} to draw a card.".format(ActionCost))


def drawMany(group, count = None, destination = None, silent = False):
   if debugVerbosity >= 1: notify(">>> drawMany(){}".format(extraASDebug())) #Debug
   if debugVerbosity >= 3: notify("source: {}\ndestination: {}".format(group.name,destination.name))
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   if debugVerbosity >= 4: notify("<<< drawMany() woth return: {}".format(count))
   return count

def toarchives(group = me.piles['Archives(Hidden)']):
   if debugVerbosity >= 1: notify(">>> toarchives(){}".format(extraASDebug())) #Debug
   mute()
   Archives = me.piles['Trash/Archives(Face-up)']
   for c in group: c.moveTo(Archives)
   #Archives.shuffle()
   notify ("{} moves Hidden Archives to their Face-Up Archives.".format(me))

def archivestoStack(group, silent = False):
   if debugVerbosity >= 1: notify(">>> archivestoStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   for c in group: c.moveTo(deck)
   #Archives.shuffle()
   if not silent: notify ("{} moves their {} to {}.".format(me,pileName(group),pileName(deck)))
   else: return(pileName(group),pileName(deck))

def mill(group):
   if debugVerbosity >= 1: notify(">>> mill(){}".format(extraASDebug())) #Debug
   if len(group) == 0: return
   mute()
   count = askInteger("Mill how many cards?", 1)
   if count == None: return
   if ds == "runner": destination = me.piles['Trash/Archives(Face-up)']
   else: destination = me.piles['Archives(Hidden)']
   for c in group.top(count): c.moveTo(destination)
   notify("{} mills the top {} cards from their {} to {}.".format(me, count,pileName(group),pileName(destination)))

def moveXtopCardtoBottomStack(group):
   if debugVerbosity >= 1: notify(">>> moveXtopCardtoBottomStack(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0: return
   count = askInteger("Move how many cards?", 1)
   if count == None: return
   for c in group.top(count): c.moveToBottom(group)
   notify("{} moves the top {} cards from their {} to the bottom of {}.".format(me, count,pileName(group),pileName(group)))


def checkDeckNoLimit (group):
   if debugVerbosity >= 1: notify(">>> checkDeckNoLimit(){}".format(extraASDebug())) #Debug
   if ( ds == ""):
      whisper ("Choose a side first.")
      return 
   notify (" -> Checking deck of {} ...".format(me) )
   ok = 0
   loDeckCount = len(group)
   if ( loDeckCount < 45 ):
      ok = -1
      notify ( ":::ERROR::: Only {} cards in {}'s Deck.".format(loDeckCount,me) )
   mute()
   if ( ds == "corp"):
      loAP = 0.0
      loRunner = 0
      for card in group:
         card.moveTo(me.piles['Trash/Archives(Face-up)'])
         if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
         if card.Type == 'Agenda': loAP += num(card.Stat)
         if card.Player == "runner": loRunner = 1
         card.moveToBottom(group)
      if loAP/loDeckCount < 2.0/5.0:
         notify(":::ERROR::: Only {} Agenda Points in {}'s R&D.".format(loAP/1,me))
         ok = -1
      if loRunner == 1:
         notify(":::ERROR::: Runner Cards found in {}'s R&D.".format(me))
         ok = -1
   else:
      loCorp = 0
      for card in group:
         card.moveTo(me.piles['Trash/Archives(Face-up)'])
         if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
         if card.Player == "corp": loCorp = 1
         card.moveToBottom(group)

      if loCorp == 1:
         notify(":::ERROR::: Corp Cards found in {}'s Stack.".format(me))
         ok = -1
   if ok == 0: notify("-> Deck of {} OK !".format(me))
   return ok

#------------------------------------------------------------------------------
# Automations
#------------------------------------------------------------------------------
def executeAutomations(card,action = ''):
   if debugVerbosity >= 1: notify(">>> executeAutomations(){}".format(extraASDebug())) #Debug
   if not Automations['Play, Score and Rez']: return
   if not card.isFaceUp: return
   AutoScript = card.AutoScript
   if AutoScript == "": return
   if re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', AutoScript): 
     executePlayScripts(card, action)
     return
   #else: confirm("No new ones") # Debug
   Execute = 0

   if action == "play" or action == "rez" or action == "scores": Execute = 1
   if ( (action == "trash" and card.markers[Not_rezzed] == 0) or action == "derez") and re.search(r'ReverseYes', AutoScript): Execute = -1
   if Execute == 0: return
   Param1 = num(card.ParamAS1)*Execute
   Param2 = num(card.ParamAS2)*Execute
   if AutoScript == "autoGainXDrawY": autoGainXDrawY(card,Param1,Param2)
   elif AutoScript == "autoGainXIfY": autoGainXIfY(card,Param1,Param2)
   elif AutoScript == "autoGainX": autoGainX(card,Param1,Param2)
   elif AutoScript == "autoDrawX" : autoDrawX(card,Param1,Param2)
   elif AutoScript == "autoAddBitsCounter": autoAddBitsCounter(card,Param1,Param2)
   elif AutoScript == "autoGainXYTags": autoGainXYTags(card,Param1,Param2 )
   elif AutoScript == "autoGainXYBadPub": autoGainXYBadPub(card,Param1,Param2)
   elif AutoScript == "autoAddGenericCounter": autoAddGenericCounter(card,Param1,Param2)
   elif AutoScript == "autoRun": autoRun(card)
   elif AutoScript == "autoRunHQ": autoRunFort("HQ")
   elif AutoScript == "autoRunRD": autoRunFort("R&D")
   elif AutoScript == "autoRunArchives": autoRunFort("the Archives")
   elif AutoScript == "autoLooseTags": autoLooseTags (card, Param1)
   elif AutoScript == "autoRollDice": autoRollDice (Param1)
   elif AutoScript == "autoRefreshToX": autoRefreshToX(card,Param1)
   elif AutoScript == "autoRefreshHand": autoRefreshHand(card,Param1)
   elif re.search(r'autoAddMUAndBitsCounter', AutoScript): autoAddMUAndCounter(card,Param1,Param2)
   elif re.search(r'MUHandSizeBitsCounter', AutoScript): autoaddMUHandSizeBitsCounter(card,Param1,Param2)
   elif re.search(r'autoAddMU', AutoScript): autoAddMU(card,Param1,Param2)
   elif re.search(r'autoAddHandSize', AutoScript): autoAddHandSize(card,Param1,Param2)
   elif re.search(r'autoAddXtraAction', AutoScript): autoAddXtraAction(card,Param1,Param2)
   elif re.search(r'autoModifyDraw', AutoScript): autoModifyDraw(card,Param1,Param2)

def autoGainXDrawY ( card, Param1, Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	drawMany ( me.piles['R&D/Stack'], Param2, True)
	notify ( "--> {} gains {} bits and draws {} cards.".format(me,Param1,Param2) )

def autoGainX ( card, Param1,Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	notify ( "--> {} gains {} bits.".format(me,Param1) )

def autoDrawX ( card, Param1,Param2):
	mute()
	drawMany ( me.piles['R&D/Stack'], Param1, True)
	notify ( "--> {} draws {} card(s).".format(me,Param1) )

def autoAddBitsCounter ( card, Param1, Param2 ):
	intAddBits ( card, Param1)

def autoAddMU ( card, Param1, Param2 ):
	mute()
	Owner = card.owner
	Owner.counters['Memory'].value +=Param1
	notify (" --> {} max MU is now {}.".format(Owner,Owner.counters['Memory'].value) )

def autoAddMUAndCounter ( card, Param1, Param2 ):
	autoAddMU ( card, Param1, Param2 )
	intAddBits ( card, Param2)

def autoAddHandSize(card,Param1,Param2):
    Owner = card.owner
    Owner.counters['Max Hand Size'].value += Param1
    notify ("--> {} max Hand Size is now {}.".format(Owner,Owner.counters['Max Hand Size'].value) )

def autoaddMUHandSizeBitsCounter ( card, Param1, Param2):
    autoAddMUAndCounter(card,Param1,Param2)
    autoAddHandSize(card,Param1,Param2)

def autoGainXYTags( card, Param1, Param2):
	autoGainX ( card, Param1, 0)
	me.counters['Tags'].value +=Param2
	notify ( "--> {} gets {} Tags.".format(me,Param2) )

def autoGainXYBadPub ( card, Param1, Param2):
	autoGainX ( card, Param1, 0)
	me.counters['Bad Publicity'].value +=Param2
	notify ( "--> {} gets {} Bad Publicy Points.".format(me,Param2) )

def autoGainXIfY ( card, Param1, Param2):
	if ( me.counters['Bit Pool'].value >= Param2): autoGainX ( card, Param1, 0)
	else:
		mute()
		me.counters['Bit Pool'].value = 0
		notify ("--> {} looses all bits.".format(me) )

def autoAddGenericCounter (card,Param1,Param2):
	mute()
	card.markers[Generic] += Param1
	notify("{} adds {} generic markers on {}.".format(me,uniBit(Param1),card))

def autoAddXtraAction (card, Param1, Param2):
	global maxActions
	mute()
	maxActions += Param1
	notify ( "--> {}'s max actions per turn are now {}.".format(me,maxActions) )

def autoModifyDraw ( card, Param1, Param2):
	global ModifyDraw
	if ( Param1 == 1): ModifyDraw = True
	else: ModifyDraw = False

def autoRun (card):
	notify (" --> {} declares a run !.".format(me) )

def autoRunFort (fort):
	notify (" --> {} declares a run on {}!.".format(me,fort) )

def autoLooseTags (card, Param1 ):
	mute()
	notify ("here")
	if (me.counters['Tags'].value == 0):
		notify ( " --> no tag to loose !")
		return
	
	if ( Param1 == 999):
		me.counters['Tags'].value = 0
		notify (" --> {} looses all tags.".format(me) )

	else:
		me.counters['Tags'].value -= Param1
		notify (" --> {} looses {} tags.".format(me,Param1) )

def autoRollDice (NbDice):
	mute()
	Acc = 0
	for i in range(1,NbDice):
		N = rnd(1, 6)
		Acc += N
		notify (" --> {} rolls a die and gets {}.".format(me,N) )

	return Acc

def autoRefreshToX (card, Param1):
	mute()
	handtoStack (0)
	if ( ds == "corp"): archivestoStack(me.piles['Archives(Hidden)'])
	archivestoStack(me.piles['Trash/Archives(Face-up)'])
	shuffle(me.piles['R&D/Stack'])
	drawMany (me.piles['R&D/Stack'], Param1, True)
	notify (" --> {} shuffles and draws {} cards.".format(me,Param1) )

def autoRefreshHand ( card, Param1):
	mute()
	if ( Param1 == 999): ToDraw = len(me.hand)
	else: ToDraw = Param1
	handtoStack (0)
	shuffle(me.piles['R&D/Stack'])
	drawMany (me.piles['R&D/Stack'], ToDraw, True)
	notify (" --> {} shuffles and draws {} cards.".format(me,ToDraw) )

def executePlayScripts(card, action):
   if debugVerbosity >= 1: notify(">>> executePlayScripts(){}".format(extraASDebug())) #Debug
   global failedRequirement
   failedRequirement = False
   X = 0
   Autoscripts = card.AutoScript.split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
   AutoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
   for autoS in AutoScriptsSnapshot: # Checking and removing any "AtTurnStart" actions.
      if re.search(r'atTurn(Start|End)', autoS) or re.search(r'-isTrigger', autoS): Autoscripts.remove(autoS)
      if re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: Autoscripts.remove(autoS)
      if re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: Autoscripts.remove(autoS)
      if re.search(r'CustomScript', autoS): 
         customScript(card,action)
         Autoscripts.remove(autoS)
   if len(Autoscripts) == 0: return
   announceText = "{}".format(me)
   for AutoS in Autoscripts:
      if debugVerbosity >= 3: notify("### First Processing: {}".format(AutoS)) # Debug
      effectType = re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', AutoS)
      if ((effectType.group(1) == 'onRez' and action != 'rez') or
          (effectType.group(1) == 'onPlay' and action != 'play') or
          (effectType.group(1) == 'onInstall' and action != 'install') or
          (effectType.group(1) == 'onScore' and action != 'score') or
          (effectType.group(1) == 'onLiberation' and action != 'liberate') or
          (effectType.group(1) == 'onTrash' and (action != 'trash' or action!= 'uninstall' or action != 'derez')) or
          (effectType.group(1) == 'onDerez' and action != 'derez')): continue # We don't want onPlay effects to activate onTrash for example.
      if re.search(r'-isOptional', AutoS):
         if not confirm("This card has an optional ability you can activate at this point. Do you want to do so?"): 
            notify("{} opts not to activate {}'s optional ability".format(me,card))
            return 'ABORT'
         else: notify("{} activates {}'s optional ability".format(me,card))
      selectedAutoscripts = AutoS.split('$$')
      if debugVerbosity >= 3: notify ('### selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for activeAutoscript in selectedAutoscripts:
         if debugVerbosity >= 2: notify("### Second Processing: {}".format(activeAutoscript)) # Debug
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         targetC = findTarget(activeAutoscript)
         if debugVerbosity >= 4: notify("#### targetC: {}".format(targetC)) # Debug
         effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\|: -]*)', activeAutoscript)
         if debugVerbosity >= 3: notify('### effects: {}'.format(effect.groups())) #Debug
         if effectType.group(1) == 'whileRezzed' or effectType.group(1) == 'whileScored':
            if action == 'derez' or ((action == 'trash' or action == 'uninstall') and card.markers[Not_rezzed] == 0): Removal = True
            else: Removal = False
         elif action == 'derez' or action == 'trash': return # If it's just a one-off event, and we're trashing it, then do nothing.
         else: Removal = False
         if effect.group(1) == 'Gain' or effect.group(1) == 'Lose':
            if Removal: 
               if effect.group(1) == 'Gain': passedScript = "Lose{}{}".format(effect.group(2),effect.group(3))
               elif effect.group(1) == 'SetTo': passedScript = "SetTo{}{}".format(effect.group(2),effect.group(3))
               else: passedScript = "Gain{}{}".format(effect.group(2),effect.group(3))
            else: 
               if effect.group(1) == 'Gain': passedScript = "Gain{}{}".format(effect.group(2),effect.group(3))
               elif effect.group(1) == 'SetTo': passedScript = "SetTo{}{}".format(effect.group(2),effect.group(3))
               else: passedScript = "Lose{}{}".format(effect.group(2),effect.group(3))
            if effect.group(4): passedScript += effect.group(4)
            if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
            if GainX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
         else: 
            passedScript = "{}".format(effect.group(0))
            if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
            if effect.group(1) == 'Draw': 
               if DrawX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if re.search(r'(Put|Remove|Refill|Use|Infect)', effect.group(1)): 
               if TokensX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'Roll': 
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if rollTuple == 'ABORT': return
               X = rollTuple[1] 
            if effect.group(1) == 'RequestInt': 
               numberTuple = RequestInt(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if numberTuple == 'ABORT': return
               X = numberTuple[1] 
            if effect.group(1) == 'Discard': 
               discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if discardTuple == 'ABORT': return
               X = discardTuple[1] 
            if re.search(r'Run', effect.group(1)): 
               if RunX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'Trace': 
               if TraceX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if re.search(r'Reshuffle', effect.group(1)): 
               reshuffleTuple = ReshuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if reshuffleTuple == 'ABORT': return
               X = reshuffleTuple[1]
            if re.search(r'Shuffle', effect.group(1)): 
               if ShuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'CreateDummy': 
               if CreateDummy(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'ChooseKeyword': 
               if ChooseKeyword(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'Inflict': 
               if InflictX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if re.search(r'(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)', effect.group(1)): 
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
         if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
#------------------------------------------------------------------------------
# Autoactions
#------------------------------------------------------------------------------

def useAbility(card, x = 0, y = 0): # The start of autoscript activation.
   if debugVerbosity >= 1: notify(">>> useAbility(){}".format(extraASDebug())) #Debug
   mute()
   global failedRequirement
   failedRequirement = False # We set it to false when we start a new autoscript.
   if (card in Stored_Type and Stored_Type[card] == 'Tracing') or card.model == 'c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8': # If the player double clicks on the Tracing card...
      if card.isFaceUp and not card.markers[Bits]: inputTraceValue(card, limit = 0)
      elif card.isFaceUp and card.markers[Bits]: payTraceValue(card)
      elif not card.isFaceUp: revealTraceValue(card)
      return
   if not card in Stored_AutoActions:
      if not card.isFaceUp:
         card.isFaceUp = True
         cFaceD = True
      else: cFaceD = False
      random = rnd(10,300)
      if debugVerbosity >= 3: notify(">>> Storing Autoactions for {}".format(card)) #Debug
      Stored_AutoActions[card] = card.AutoAction
      if cFaceD: card.isFaceUp = False
   if not card.isFaceUp or card.markers[Not_rezzed]:
      if re.search(r'onAccess',Stored_AutoActions[card]) and confirm("This card has an ability that can be activated even when unrezzed. Would you like to activate that now?"): card.isFaceUp = True # Activating an on-access ability requires the card to be exposed, it it's no already.
      elif re.search(r'Hidden',Stored_Keywords[card]): card.isFaceUp # If the card is a hidden resource, just turn it face up for its imminent use.
      elif Stored_Type[card] == 'Agenda': 
         scrAgenda(card) # If the player double-clicks on an Agenda card, assume they wanted to Score it.
         return
      else: 
         intRez(card) # If card is face down or not rezzed assume they wanted to rez       
         return
   elif not Automations['Play, Score and Rez'] or Stored_AutoActions[card] == "": 
      useCard(card) # If card is face up but has no autoscripts, or automation is disabled just notify that we're using an action.
      return
   elif re.search(r'CustomScript', Stored_AutoActions[card]): 
      if chkTargeting(card) == 'ABORT': return
      customScript(card,'use') # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   ### Checking if card has multiple autoscript options and providing choice to player.
   Autoscripts = Stored_AutoActions[card].split('||')
   AutoScriptSnapshot = list(Autoscripts)
   for autoS in AutoScriptSnapshot: # Checking and removing any actionscripts which were put here in error.
      if (re.search(r'while(Rezzed|Scored)', autoS) 
         or re.search(r'on(Play|Score|Install)', autoS) 
         or re.search(r'AtTurn(Start|End)', autoS)
         or card.markers[Not_rezzed] and not re.search(r'onAccess', autoS) # If the card is still unrezzed and the ability does not have "onAccess" on it, it can't be used.
         or (re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor)
         or (re.search(r'(CreateDummy|excludeDummy)', autoS) and card.highlight == DummyColor)): # Dummies in general don't create new dummies
         Autoscripts.remove(autoS)
   if debugVerbosity >= 3: notify("### Removed bad options")
   if len(Autoscripts) == 0:
      useCard(card) # If the card had only "WhileInstalled"  or AtTurnStart effect, just announce that it is being used.
      return      
   if len(Autoscripts) > 1: 
      abilConcat = "This card has multiple abilities.\nWhich one would you like to use?\n\n" # We start a concat which we use in our confirm window.
      for idx in range(len(Autoscripts)): # If a card has multiple abilities, we go through each of them to create a nicely written option for the player.
         notify("Autoscripts {}".format(Autoscripts)) # Debug
         abilRegex = re.search(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):([A-Z][A-Za-z ]+)([0-9]*)([A-Za-z ]*)-?(.*)", Autoscripts[idx]) # This regexp returns 3-4 groups, which we then reformat and put in the confirm dialogue in a better readable format.
         if debugVerbosity >= 2: notify("### Choice Regex is {}".format(abilRegex.groups())) # Debug
         if abilRegex.group(1) != '0': abilCost = 'Use {} Actions'.format(abilRegex.group(1))
         else: abilCost = '' 
         if abilRegex.group(2) != '0': 
            if abilCost != '': 
               if abilRegex.group(3) != '0' or abilRegex.group(4) != '0': abilCost += ', '
               else: abilCost += ' and '
            abilCost += 'Pay {} Bits'.format(abilRegex.group(2))
         if abilRegex.group(3) != '0': 
            if abilCost != '': 
               if abilRegex.group(4) != '0': abilCost += ', '
               else: abilCost += ' and '
            abilCost += 'Lose {} Agenda Points'.format(abilRegex.group(3))
         if abilRegex.group(4) != '0': 
            if abilCost != '': abilCost += ' and '
            if abilRegex.group(4) == '1': abilCost += 'Trash this card'
            else: abilCost += 'Use (Once per turn)'
         if abilRegex.group(1) == '0' and abilRegex.group(2) == '0' and abilRegex.group(3) == '0' and abilRegex.group(4) == '0':
            abilCost = 'Activate'
         if abilRegex.group(6):
            if abilRegex.group(6) == '999': abilX = 'all'
            else: abilX = abilRegex.group(6)
         else: abilX = abilRegex.group(6)
         abilConcat += '{}: {} to {} {} {}'.format(idx, abilCost, abilRegex.group(5), abilX, abilRegex.group(7)) # We add the first three groups to the concat. Those groups are always Gain/Hoard/Prod ## Favo/Solaris/Spice
         if debugVerbosity >= 4: notify("### About to check rest of choice regex")
         if abilRegex.group(8): # If the autoscript has a fourth group, then it means it has subconditions. Such as "per Holding" or "by Rival"
            subconditions = abilRegex.group(8).split('$$') # These subconditions are always separated by dashes "-", so we use them to split the string
            for idx2 in range(len(subconditions)):
               if idx2 > 0: abilConcat += ' and'
               subadditions = subconditions[idx2].split('-')
               for idx3 in range(len(subadditions)):
                  if debugVerbosity >= 4: notify("### Checking subaddition {}:{}".format(idx2,idx3))
                  if re.search(r'warn[A-Z][A-Za-z0-9 ]+', subadditions[idx3]): continue # Don't mention warnings.
                  abilConcat += ' {}'.format(subadditions[idx3]) #  Then we iterate through each distinct subcondition and display it without the dashes between them. (In the future I may also add whitespaces between the distinct words)
         abilConcat += '\n' # Finally add a newline at the concatenated string for the next ability to be listed.
      abilChoice = len(Autoscripts) + 1 # Since we want a valid choice, we put the choice in a loop until the player exists or selects a valid one.
      while abilChoice >= len(Autoscripts):
         abilChoice = askInteger('{}'.format(abilConcat), 0) # We use the ability concatenation we crafted before to give the player a choice of the abilities on the card.
         if abilChoice == None: return # If the player closed the window, abort.
      selectedAutoscripts = Autoscripts[abilChoice].split('$$') # If a valid choice is given, choose the autoscript at the list index the player chose.
   else: selectedAutoscripts = Autoscripts[0].split('$$')
   timesNothingDone = 0 # A variable that keeps track if we've done any of the autoscripts defined. If none have been coded, we just engage the card.
   X = 0 # Variable for special costs.
   if card.highlight == DummyColor: lingering = ' the lingering effect of' # A text that we append to point out when a player is using a lingering effect in the form of a dummy card.
   else: lingering = ''
   for activeAutoscript in selectedAutoscripts:
      #confirm("Active Autoscript: {}".format(activeAutoscript)) #Debug
      ### Checking if any of the card's effects requires one or more targets first
      if re.search(r'Targeted', activeAutoscript) and not findTarget(activeAutoscript): return
   for activeAutoscript in selectedAutoscripts:
      targetC = findTarget(activeAutoscript)
      ### Warning the player in case we need to
      if chkWarn(card, activeAutoscript) == 'ABORT': return
      ### Checking the activation cost and preparing a relevant string for the announcement
      actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", activeAutoscript) 
      # This is the cost of the card.  It starts with A which is the amount of Actions needed to activate
      # After A follows B for Bit cost, then for aGenda cost.
      # T takes a binary value. A value of 1 means the card needs to be trashed.
      if actionCost: # If there's no match, it means we've already been through the cost part once and now we're going through the '$$' part.
         if actionCost.group(1) != '0': # If we need to use actions
            Acost = useAction(count = num(actionCost.group(1)))
            if Acost == 'ABORT': return
            else: announceText = Acost
         else: announceText = '{}'.format(me) # A variable with the text to be announced at the end of the action.
         if actionCost.group(2) != '0': # If we need to pay bits
            reduction = reduceCost(card, 'Use', num(actionCost.group(2)))
            if reduction: extraText = " (reduced by {})".format(uniBit(reduction))  
            else: extraText = ''
            Bcost = payCost(num(actionCost.group(2)) - reduction)
            if Bcost == 'ABORT': # if they can't pay the cost afterall, we return them their actions and abort.
               me.Actions += num(actionCost.group(1))
               return
            if actionCost.group(1) != '0':
               if actionCost.group(3) != '0' or actionCost.group(4) != '0': announceText += ', '
               else: announceText += ' and '
            else: announceText += ' '
            announceText += 'pays {}{}'.format(uniBit(num(actionCost.group(2)) - reduction),extraText)
         if actionCost.group(3) != '0': # If we need to pay agenda points...
            Gcost = payCost(actionCost.group(3), counter = 'AP')
            if Gcost == 'ABORT': 
               me.Actions += num(actionCost.group(1))
               me.counters['Bit Pool'].value += num(actionCost.group(2))
               return
            if actionCost.group(1) != '0' or actionCost.group(2)  != '0':
               if actionCost.group(4) != '0': announceText += ', '
               else: announceText += ' and '
            else: announceText += ' '
            announceText += 'liquidates {} Agenda Points'.format(actionCost.group(3))
         if actionCost.group(4) != '0': # If the card needs to be trashed...
            if (actionCost.group(4) == '2' and oncePerTurn(card, silent = True) == 'ABORT') or (actionCost.group(4) == '1' and not confirm("This action will trash the card as a cost. Are you sure you want to continue?")):
               # On trash cost, we confirm first to avoid double-click accidents
               me.Actions += num(actionCost.group(1))
               me.counters['Bit Pool'].value += num(actionCost.group(2))
               me.counters['Agenda Points'].value += num(actionCost.group(3))
               return
            if actionCost.group(1) != '0' or actionCost.group(2) != '0' or actionCost.group(3) != '0': announceText += ' and '
            else: announceText += ' '
            if actionCost.group(4) == '1': announceText += 'trashes {} to use its ability'.format(card)
            else: announceText += 'activates the once-per-turn ability of{} {}'.format(lingering,card)
         else: announceText += ' to activate{} {}'.format(lingering,card) # If we don't have to trash the card, we need to still announce the name of the card we're using.
         if actionCost.group(1) == '0' and actionCost.group(2) == '0' and actionCost.group(3) == '0' and actionCost.group(4) == '0':
            if card.Type == 'Ice': announceText = '{} activates the subroutine of {}'.format(me, card)
            else: announceText = '{} activates the free ability of{} {}'.format(me, lingering, card)
         announceText += ' in order to'
      elif not announceText.endswith(' in order to') and not announceText.endswith(' and'): announceText += ' and'
      if debugVerbosity >= 3: notify("### Entering useAbility() Choice with Autoscript: {}".format(activeAutoscript)) # Debug
      ### Calling the relevant function depending on if we're increasing our own counters, the hoard's or putting card markers.
      if re.search(r'\b(Gain|Lose|SetTo)([0-9]+)', activeAutoscript): announceText = GainX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bCreateDummy', activeAutoscript): announceText = CreateDummy(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bReshuffle([A-Za-z& ]+)', activeAutoscript): 
         reshuffleTuple = ReshuffleX(activeAutoscript, announceText, card) # The reshuffleX() function is special because it returns a tuple.
         announceText = reshuffleTuple[0] # The first element of the tuple contains the announceText string
         X = reshuffleTuple[1] # The second element of the tuple contains the number of cards that were reshuffled from the hand in the deck.
      elif re.search(r'\bRoll([0-9]+)', activeAutoscript): 
         rollTuple = RollX(activeAutoscript, announceText, card) # Returns like reshuffleX()
         announceText = rollTuple[0] 
         X = rollTuple[1] 
      elif re.search(r'\bRequestInt', activeAutoscript): 
         numberTuple = RequestInt(activeAutoscript, announceText, card) # Returns like reshuffleX()
         announceText = numberTuple[0] 
         X = numberTuple[1] 
      elif re.search(r'\bDiscard[0-9]+', activeAutoscript): 
         discardTuple = DiscardX(activeAutoscript, announceText, card, targetC, n = X) # Returns like reshuffleX()
         announceText = discardTuple[0] 
         X = discardTuple[1] 
      elif re.search(r'\b(Put|Remove|Refill|Use|Infect)([0-9]+)', activeAutoscript): announceText = TokensX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bTransfer([0-9]+)', activeAutoscript): announceText = TransferX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bDraw([0-9]+)', activeAutoscript): announceText = DrawX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bShuffle([A-Za-z& ]+)', activeAutoscript): announceText = ShuffleX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bRun([A-Za-z& ]+)', activeAutoscript): announceText = RunX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bTrace([0-9]+)', activeAutoscript): announceText = TraceX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bInflict([0-9]+)', activeAutoscript): announceText = InflictX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)', activeAutoscript): announceText = ModifyStatus(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bSimplyAnnounce', activeAutoscript): announceText = SimplyAnnounce(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bChooseKeyword', activeAutoscript): announceText = ChooseKeyword(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bUseCustomAbility', activeAutoscript): announceText = UseCustomAbility(activeAutoscript, announceText, card, targetC, n = X)
      else: timesNothingDone += 1
      if debugVerbosity >= 4: notify("<<< useAbility() choice") # Debug
      if announceText == 'ABORT': 
         autoscriptCostUndo(card, selectedAutoscripts[0]) # If nothing was done, try to undo. The first item in selectedAutoscripts[] contains the cost.
         return
      if failedRequirement: break # If part of an AutoAction could not pay the cost, we stop the rest of it.
   if announceText.endswith(' in order to'): # If our text annouce ends with " to", it means that nothing happened. Try to undo and inform player.
      autoscriptCostUndo(card, selectedAutoscripts[0])
      notify("{} but there was nothing to do.".format(announceText[:-len(' in order to')]))
   elif announceText.endswith(' and'):
      announceText = announceText[:-len(' and')] # If for some reason we end with " and" (say because the last action did nothing), we remove it.
   else: # If we did something and everything finished as expected, then take the costs.
      if re.search(r"T1:", selectedAutoscripts[0]): 
         executeAutomations (card,'trash')
         card.moveTo(card.owner.piles['Trash/Archives(Face-up)'])
      notify("{}.".format(announceText)) # Finally announce what the player just did by using the concatenated string.

def autoscriptCostUndo(card, Autoscript): # Function for undoing the cost of an autoscript.
   if debugVerbosity >= 1: notify(">>> autoscriptCostUndo(){}".format(extraASDebug())) #Debug
   whisper("--> Undoing action...")
   actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", Autoscript)
   me.Actions += num(actionCost.group(1))
   me.counters['Bit Pool'].value += num(actionCost.group(2))
   me.counters['Agenda Points'].value += num(actionCost.group(3))
   if re.search(r"T2:", Autoscript):
      random = rnd(10,5000) # A little wait...
      card.orientation = Rot0

def findTarget(Autoscript): # Function for finding the target of an autoscript
   if debugVerbosity >= 1: notify(">>> findTarget(){}".format(extraASDebug())) #Debug
   targetC = None
   #confirm("Looking for targets.\n\nAutoscript: {}".format(Autoscript)) #Debug
   foundTargets = []
   if re.search(r'Targeted', Autoscript):
      validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
      validNamedTargets = [] # a list that holds any name or allegiance that a card must have, in order to be a valid target.
      invalidTargets = [] # a list that holds any type that a card must not be to be a valid target.
      invalidNamedTargets = [] # a list that holds the name or allegiance that the card must not have to be a valid target.
      requiredAllegiances = []
      whatTarget = re.search(r'\bat([A-Za-z_{},& ]+)[-]?', Autoscript) # We signify target restrictions keywords by starting a string with "or"
      if whatTarget: validTargets = whatTarget.group(1).split('_or_') # If we have a list of valid targets, split them into a list, separated by the string "_or_". Usually this results in a list of 1 item.
      ValidTargetsSnapshot = list(validTargets) # We have to work on a snapshot, because we're going to be modifying the actual list as we iterate.
      for chkTarget in ValidTargetsSnapshot: # Now we go through each list item and see if it has more than one condition (Eg, non-desert fief)
         if re.search(r'_and_', chkTarget):  # If there's a string "_and_" between our restriction keywords, then this keyword has mutliple conditions
            multiConditionTargets = chkTarget.split('_and_') # We put all the mutliple conditions in a new list, separating each element.
            for chkCondition in multiConditionTargets:
               regexCondition = re.search(r'(no[nt]){?([A-Za-z,& ]+)}?', chkCondition) # Do a search to see if in the multicondition targets there's one with "non" in front
               if regexCondition and regexCondition.group(1):
                  if regexCondition.group(2) not in invalidTargets == 'non': invalidTargets.append(regexCondition.group(2)) # If there is, move it without the "non" into the invalidTargets list.
               elif regexCondition and regexCondition.group(1) == 'not':
                  if regexCondition.group(2) not in invalidNamedTargets: invalidNamedTargets.append(regexCondition.group(2))
               else: validTargets.append(chkCondition) # Else just move the individual condition to the end if validTargets list
            validTargets.remove(chkTarget) # Finally, remove the multicondition keyword from the valid list. Its individual elements should now be on this list or the invalid targets one.
         else:
            regexCondition = re.search(r'(no[nt]){?([A-Za-z,& ]+)}?', chkTarget)
            if regexCondition and regexCondition.group(1) == 'non' and regexCondition.group(2) not in invalidTargets: # If the keyword has "non" in front, it means it's something we need to avoid, so we move it to a different list.
               invalidTargets.append(regexCondition.group(2))
               validTargets.remove(chkTarget)
               continue
            if regexCondition and regexCondition.group(1) == 'not' and regexCondition.group(2) not in invalidNamedTargets: # Same as above but keywords with "not" in front as specific card names.
               invalidNamedTargets.append(regexCondition.group(2))
               validTargets.remove(chkTarget)
               continue
            regexCondition = re.search(r'{([A-Za-z,& ]+)}', chkTarget)
            if regexCondition and regexCondition.group(1) not in validNamedTargets: # Same as above but keywords in {curly brackets} are exact names in front as specific card names.
               validNamedTargets.append(regexCondition.group(1))
               validTargets.remove(chkTarget)
      for targetLookup in table: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
         if ((targetLookup.targetedBy and targetLookup.targetedBy == me) or re.search(r'AutoTargeted', Autoscript)) and chkPlayer(Autoscript, targetLookup.controller, False): # The card needs to be targeted by the player. If the card needs to belong to a specific player (me or rival) this also is taken into account.
            #whisper('checking {}'.format(targetLookup)) # Debug
            if not targetLookup.isFaceUp: # If we've targeted a subdued card, we turn it temporarily face-up to grab its properties.
               targetLookup.isFaceUp = True
               cFaceD = True
            else: cFaceD = False
            if len(validTargets) == 0 and len(validNamedTargets) == 0: targetC = targetLookup # If we have no target restrictions, any targeted  card will do.
            else:
               for validtargetCHK in validTargets: # look if the card we're going through matches our valid target checks
                  if re.search(r'{}'.format(validtargetCHK), targetLookup.Type) or re.search(r'{}'.format(validtargetCHK), getKeywords(targetLookup)) or re.search(r'{}'.format(validtargetCHK), targetLookup.Player):
                     targetC = targetLookup
               for validtargetCHK in validNamedTargets: # look if the card we're going through matches our valid target checks
                  if validtargetCHK == targetLookup.name:
                     targetC = targetLookup
            if len(invalidTargets) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
               for invalidtargetCHK in invalidTargets:
                  if re.search(r'{}'.format(invalidtargetCHK), targetLookup.Type) or re.search(r'{}'.format(invalidtargetCHK), getKeywords(targetLookup)) or re.search(r'{}'.format(invalidtargetCHK), targetLookup.Player):
                     targetC = None
            if len(invalidNamedTargets) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
               for invalidtargetCHK in invalidNamedTargets:
                  if invalidtargetCHK == targetLookup.name:
                     targetC = None
            if re.search(r'isRezzed', Autoscript) and targetLookup.markers[mdict['Not_rezzed']]: targetC = None
            if re.search(r'isUnrezzed', Autoscript) and not targetLookup.markers[mdict['Not_rezzed']]: targetC = None
            if cFaceD: targetLookup.isFaceUp = False
            #if targetC and not targetC in foundTargets: confirm("about to append target Card: {}".format(targetC.name)) # Debug
            if targetC and not targetC in foundTargets: foundTargets.append(targetC) # I don't know why but the first match is always processed twice by the for loop.
      if targetC == None and not re.search(r'AutoTargeted', Autoscript): 
         targetsText = ''
         if len(validTargets) > 0: targetsText += "\nValid Target types: {}.".format(validTargets)
         if len(validNamedTargets) > 0: targetsText += "\nSpecific Valid Targets: {}.".format(validNamedTargets)
         if len(invalidTargets) > 0: targetsText += "\nInvalid Target types: {}.".format(invalidTargets)
         if len(invalidNamedTargets) > 0: targetsText += "\nSpecific Invalid Targets: {}.".format(invalidNamedTargets)
         if not chkPlayer(Autoscript, targetLookup.controller, False): 
            allegiance = re.search(r'by(Opponent|Me)', Autoscript)
            requiredAllegiances.append(allegiance.group(1))
         if re.search(r'isRezzed', Autoscript): targetsText += "\nValid Status: Rezzed."
         if re.search(r'isUnrezzed', Autoscript): targetsText += "\nValid Status: Unrezzed."
         if len(requiredAllegiances) > 0: targetsText += "\nValid Target Allegiance: {}.".format(requiredAllegiances)
         whisper("You need to target a valid card before using this action{}".format(targetsText))
   #confirm("List is: {}".format(foundTargets)) # Debug
   if debugVerbosity >= 4: 
      tlist = []
      for foundTarget in foundTargets: tlist.append(foundTarget.name) # Debug
      notify("<<< findTarget() by returning: {}".format(tlist))
   return foundTargets
   
def chkWarn(card, Autoscript): # Function for checking that an autoscript announces a warning to the player
   if debugVerbosity >= 1: notify(">>> chkWarn(){}".format(extraASDebug())) #Debug
   warning = re.search(r'warn([A-Z][A-Za-z0-9 ]+)-?', Autoscript)
   if warning:
      if warning.group(1) == 'Discard': 
         if not confirm("This action requires that you discard some cards. Have you done this already?"):
            whisper("--> Aborting action. Please discard the necessary amount of cards and run this action again")
            return 'ABORT'
      if warning.group(1) == 'ReshuffleOpponent': 
         if not confirm("This action will reshuffle your opponent's pile. Are you sure?\n\n[Important: Please ask your opponent not to take any actions with their piles until this actions is complete or the game might crash]"):
            whisper("--> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'Reshuffle': 
         if not confirm("This action will reshuffle your piles. Are you sure?"):
            whisper("--> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'Workaround':
         notify(":::Note:::{} is using a workaround autoscript".format(me))
      if warning.group(1) == 'LotsofStuff': 
         if not confirm("This card performs a lot of complex actions that will very difficult to undo. Are you sure you want to proceed?"):
            whisper("--> Aborting action.")
            return 'ABORT'
   return 'OK'

def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for modifying counters or global variables
   if debugVerbosity >= 1: notify(">>> GainX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global maxActions
   gain = 0
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   if debugVerbosity >= 2: notify("### action groups: {}. Autoscript: {}".format(action.groups(0),Autoscript)) # Debug
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0:
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if debugVerbosity >= 4: notify("GainX() after per") #Debug
   if action.group(1) == 'Lose': 
      gain *= -1
      gainReduce = 0
   else: gainReduce = findCounterPrevention(gain * multiplier, action.group(3), targetPL) # If we're going to gain counter, then we check to see if we have any markers which might reduce the cost.
   #confirm("multiplier: {}, gain: {}, reduction: {}".format(multiplier, gain, gainReduce)) # Debug
   if re.match(r'Bits', action.group(3)): # Note to self: I can probably comprress the following, by using variables and by putting the counter object into a variable as well.
      if action.group(1) == 'SetTo': targetPL.counters['Bit Pool'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bit Pool'].value = 0
      else: targetPL.counters['Bit Pool'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Bit Pool'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bit Pool'].value = 0
   elif re.match(r'Agenda Points', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Agenda Points'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Agenda Points'].value = 0
      else: targetPL.counters['Agenda Points'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Agenda Points'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Agenda Points'].value = 0
   elif re.match(r'Actions', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Actions = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Actions = 0
      else: targetPL.Actions += (gain * multiplier) - gainReduce
   elif re.match(r'MU', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Memory = 0 # If we're setting to a specific value, we wipe what it's currently.
      else: targetPL.Memory += (gain * multiplier) - gainReduce
      if targetPL.Memory < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.Memory = 0
   elif re.match(r'Bad Publicity', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Bad Publicity'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bad Publicity'].value = 0
      else: targetPL.counters['Bad Publicity'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Bad Publicity'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bad Publicity'].value = 0
   elif re.match(r'Tags', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Tags = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Tags = 0
      else: targetPL.Tags += (gain * multiplier) - gainReduce
      if targetPL.Tags < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.Tags = 0
   elif re.match(r'Max Action', action.group(3)): 
      if targetPL == me: 
         if action.group(1) == 'SetTo': maxActions = 0 # If we're setting to a specific value, we wipe what it's currently.
         maxActions += gain * multiplier
      else: notify("--> {} loses {} max action. They must make this modification manually".format(targetPL,gain * multiplier))
   elif re.match(r'Hand Size', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Max Hand Size'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      targetPL.counters['Max Hand Size'].value += gain * multiplier
      if targetPL.counters['Max Hand Size'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(action.group(3)))
         else: targetPL.counters['Max Hand Size'].value = 0
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   if notification != 'Automatic': # Since the verb is in the middle of the sentence, we want it lowercase.
      if action.group(1) == 'Gain': verb = 'gain'
      elif action.group(1) == 'Lose': 
         if re.search(r'isCost', Autoscript): verb = 'pay'
         else: verb = 'lose'
      else: verb = 'set to'
      if notification == 'Quick':
         if verb == 'gain' or verb == 'lose' or verb == 'pay': verb += 's'
         else: verb = 'sets to'
   else: verb = action.group(1) # Automatic notifications start with the verb, so it needs to be capitaliszed. 
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   else: total = abs(gain * multiplier) # Else it's just the absolute value which we announce they "gain" or "lose"
   if debugVerbosity >= 3: notify("### Gainx() about to announce")
   if notification == 'Quick': announceString = "{}{} {} {} {}".format(announceText, otherTXT, verb, total, action.group(3))
   else: announceString = "{}{} {} {} {}".format(announceText, otherTXT, verb, total, action.group(3))
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< Gain()")
   return announceString

def TransferX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for converting tokens to counter values
   if debugVerbosity >= 1: notify(">>> TransferX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   #breakadd = 1
   total = 0
   totalReduce = 0
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   action = re.search(r'\bTransfer([0-9]+)([A-Za-z ]+)-?', Autoscript)
   if action.group(2) == 'Bits': destGroup = me.counters['Bit Pool']
   elif action.group(2) == 'Actions': destGroup = me.counters['Actions']
   else:
      whisper(":::WARNING::: Not a valid transfer. Aborting!")
      return 'ABORT'
   for targetCard in targetCards:
      foundMarker = None
      for key in targetCard.markers:
         #confirm("Key: {}\n\nChoice: {}".format(key[0],keywords[choice])) # Debug
         if key[0] == action.group(2):
            foundMarker = key
            #confirm("Added:{}".format(existingKeyword))
      if not foundMarker: 
         whisper("There was nothing to transfer from {}.".format(targetCard))
         continue
      if action.group(1) == '999':
         if targetCard.markers[foundMarker]: count = targetCard.markers[foundMarker]
         else: count = 0
      else: count = num(action.group(1))
      if targetCard.markers[foundMarker] < count: 
         if re.search(r'isCost', Autoscript):
            whisper("You must have at least {} {} on the card to take this action".format(action.group(1),action.group(2)))
            return 'ABORT'
         elif targetCard.markers[foundMarker] == 0 and notification: return 'ABORT'
      for transfer in range(count):
         if targetCard.markers[foundMarker] > 0: 
            transferReduce = findCounterPrevention(1, action.group(2), me) 
            targetCard.markers[foundMarker] -= 1
            if transferReduce: totalReduce += 1
            total += 1 - totalReduce
            destGroup.value += 1 - transferReduce
         else:
            #breakadd -= 1 # We decrease the transfer variable by one, to make sure we announce the correct total.
            break # If there's no more tokens to transfer, break out of the loop.
   #confirm("total: {}".format(total)) # Debug
   if total == 0 and totalReduce == 0: return 'ABORT' # If both totals are 0, it means nothing was generated, so there's no need to mention anything.
   if totalReduce: reduceTXT = " ({} forfeited)".format(totalReduce)
   else: reduceTXT = ''
   if notification == 'Quick': announceString = "{} takes {} {}{}.".format(announceText, total,action.group(2),reduceTXT)
   elif notification == 'Automatic': announceString = "{} Transfers {} {} to {}{}.".format(announceText, total,action.group(2),me,reduceTXT)
   else: announceString = "{} takes {} {} from {}{}.".format(announceText, total, action.group(2), targetCardlist,reduceTXT)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< TransferX()")
   return announceString   

def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for adding tokens to cards
   if debugVerbosity >= 1: notify(">>> TokensX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   if len(targetCards) == 0:
      targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
      targetCardlist = ' on it' 
   else:
      targetCardlist = ' on' # A text field holding which cards are going to get tokens.
      for targetCard in targetCards:
         targetCardlist += ' {},'.format(targetCard)
   #confirm("TokensX List: {}".format(targetCardlist)) # Debug
   foundKey = False # We use this to see if the marker used in the AutoAction is already defined.
   infectTXT = '' # We only inject this into the announcement when this is an infect AutoAction.
   preventTXT = '' # Again for virus infections, to note down how much was prevented.
   action = re.search(r'\b(Put|Remove|Refill|Use|Infect)([0-9]+)([A-Za-z: ]+)-?', Autoscript)
   #confirm("{}".format(action.group(3))) # Debug
   if action.group(3) in mdict: token = mdict[action.group(3)]
   else: # If the marker we're looking for it not defined, then either create a new one with a random color, or look for a token with the custom name we used above.
      if action.group(1) == 'Infect': 
         victim = ofwhom(Autoscript)
         if targetCards[0] == card: targetCards[0] = getSpecial('Counter Hold',victim)
      if targetCards[0].markers:
         for key in targetCards[0].markers:
            #confirm("Key: {}\n\naction.group(3): {}".format(key[0],action.group(3))) # Debug
            if key[0] == action.group(3):
               foundKey = True
               token = key
      if not foundKey: # If no key is found with the name we seek, then create a new one with a random colour.
         #counterIcon = re.search(r'-counterIcon{([A-Za-z]+)}', Autoscript) # Not possible at the moment
         #if counterIcon and counterIcon.group(1) == 'plusOne':             # See https://github.com/kellyelton/OCTGN/issues/446
         #   token = ("{}".format(action.group(3)),"aa261722-e12a-41d4-a475-3cc1043166a7")         
         #else:
         rndGUID = rnd(1,8)
         token = ("{}".format(action.group(3)),"00000000-0000-0000-0000-00000000000{}".format(rndGUID)) #This GUID is one of the builtin ones
   count = num(action.group(2))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   for targetCard in targetCards:
      #confirm("TargetCard ID: {}".format(targetCard._id)) # Debug
      if action.group(1) == 'Put': modtokens = count * multiplier
      elif action.group(1) == 'Refill': modtokens = count - targetCard.markers[token]
      elif action.group(1) == 'Infect':
         targetCardlist = '' #We don't want to mention the target card for infections. It's always the same.
         victim = ofwhom(Autoscript)
         if targetCard == card: targetCard = getSpecial('Counter Hold',victim) # For infecting targets, the target is never the card causing the effect.
         modtokens = count * multiplier
         if re.search('virus',token[0]) and token != mdict['protectionVirus']: # We don't want us to prevent putting virus protection tokens, even though we put them with the "Infect" keyword.
            Virusprevented = findVirusProtection(targetCard, victim, modtokens)
            if Virusprevented > 0:
               preventTXT = ' ({} prevented)'.format(Virusprevented)
               modtokens -= Virusprevented
         infectTXT = ' {} with'.format(victim)
         #notify("Token is {}".format(token[0])) # Debug
      elif action.group(1) == 'Use':
         if not targetCard.markers[token] or count > targetCard.markers[token]: 
            whisper("There's not enough counters left on the card to use this ability!")
            return 'ABORT'
         else: modtokens = -count * multiplier
      else: #Last option is for removing tokens.
         if count == 999: # 999 effectively means "all markers on card"
            if action.group(3) == 'Virus': pass # We deal with removal of viruses later.
            elif action.group(3) == 'BrainDMG': # We need to remove brain damage from the counter hold
               targetCardlist = ''
               victim = ofwhom(Autoscript)
               if not targetCard or targetCard == card: targetCard = getSpecial('Counter Hold',victim)
               if targetCard.markers[token]: count = targetCard.markers[token]
               else: count = 0
               #confirm("count: {}".format(count)) # Debug
            elif targetCard.markers[token]: count = targetCard.markers[token]
            else: 
               whisper("There was nothing to remove.")
               count = 0
         elif re.search(r'isCost', Autoscript) and (not targetCard.markers[token] or (targetCard.markers[token] and count > targetCard.markers[token])):
            whisper ("No markers to remove. Aborting!")
            return 'ABORT'
         elif not targetCard.markers[token]: 
            whisper("There was nothing to remove.")        
            count = 0 # If we don't have any markers, we have obviously nothing to remove.
         modtokens = -count * multiplier
      if action.group(3) == 'Virus' and count == 999: # This combination means that the Corp is cleaning all viruses.
         targetCard.markers[mdict['virusButcherBoy']] = 0
         targetCard.markers[mdict['virusCascade']] = 0
         targetCard.markers[mdict['virusCockroach']] = 0
         targetCard.markers[mdict['virusGremlin']] = 0
         targetCard.markers[mdict['virusThought']] = 0      
         targetCard.markers[mdict['virusBoardwalk']] = 0
         targetCard.markers[mdict['virusIncubate']] = 0
         for c in table: 
            if c.Type == 'Data Fort' and c.owner == me: c.markers[mdict['virusFait']] = 0 # Fait viruses exist on Data Forts, so we clean all of them there.
            if c.Type == 'Ice' and c.owner == me: c.markers[mdict['virusPattel']] = 0 # Pattel viruses exist on Ice, so we clean all of them there.
      else: targetCard.markers[token] += modtokens
   if abs(num(action.group(2))) == abs(999): total = 'all'
   else: total = abs(modtokens)
   if action.group(1) == 'Refill': announceString = "{} {} to {} {}".format(announceText, action.group(1), count, token[0]) # We need a special announcement for refill, since it always needs to point out the max.
   elif re.search(r'\bRemove999Virus', Autoscript): announceString = "{} to clean all viruses from their corporate network".format(announceText)
   elif re.search(r'forfeitCounter:',action.group(3)):
      counter = re.search(r'forfeitCounter:(\w+)',action.group(3))
      if not victim or victim == me: announceString = '{} forfeit their next {} {}'.format(announceText,total,counter.group(1)) # If we're putting on forfeit counters, we don't announce it as an infection.
      else: announceString = '{} force {} to forfeit their next {} {}'.format(announceText, victim, total,counter.group(1))
   else: announceString = "{} {}{} {} {} counters{}{}".format(announceText, action.group(1).lower(),infectTXT, total, token[0],targetCardlist,preventTXT)
   if notification == 'Automatic' and modtokens != 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 2: notify("### TokensX() String: {}".format(announceString)) #Debug
   if debugVerbosity >= 4: notify("<<< TokensX()")
   return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DrawX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   destiVerb = 'draw'
   action = re.search(r'\bDraw([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript)
   if targetPL != me: destiVerb = 'move'
   if re.search(r'-fromTrash', Autoscript): source = targetPL.piles['Trash/Archives(Face-up)']
   else: source = targetPL.piles['R&D/Stack']
   if re.search(r'-toStack', Autoscript): 
      destination = targetPL.piles['R&D/Stack']
      destiVerb = 'move'
   elif re.search(r'-toTrash', Autoscript):
      if targetPL.getGlobalVariable('ds') == 'corp': destination = targetPL.piles['Archives(Hidden)']
      else: destination = targetPL.piles['Trash/Archives(Face-up)']
      destiVerb = 'trash'   
   else: destination = targetPL.hand
   if destiVerb == 'draw' and ModifyDraw and not confirm("You have a card effect in play that modifies the amount of cards you draw. Have you already looked at the relevant cards on the top of your deck before taking this action?\n\n(Answering 'No' will abort this action so that you can first check your deck"): return 'ABORT'
   draw = num(action.group(1))
   if draw == 999:
      multiplier = 1
      if currentHandSize(targetPL) >= len(targetPL.hand): # Otherwise drawMany() is going to try and draw "-1" cards which somehow draws our whole deck except one card.
         count = drawMany(source, currentHandSize(targetPL) - len(targetPL.hand), destination, True) # 999 means we refresh our hand
      else: count = 0 
      #confirm("cards drawn: {}".format(count)) # Debug
   else: # Any other number just draws as many cards.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = drawMany(source, draw * multiplier, destination, True)
   if targetPL == me:
      if destiVerb != 'trash': destPath = " to their {}".format(destination.name)
      else: destPath = ''
   else: 
      if destiVerb != 'trash': destPath = " to {}'s {}".format(targetPL,destination.name)
      else: destPath = ''
   if debugVerbosity >= 3: notify("### About to announce.")
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} draws {} cards".format(announceText, count)
   elif targetPL == me: announceString = "{} {} {} cards from their {}{}".format(announceText, destiVerb, count, pileName(source), destPath)
   else: announceString = "{} {} {} cards from {}'s {}".format(announceText, destiVerb, count, targetPL, pileName(source), destPath)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< DrawX()")
   return announceString

def DiscardX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DiscardX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bDiscard([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   discardNR = num(action.group(1))
   if discardNR == 999:
      multiplier = 1
      discardNR = len(targetPL.hand) # 999 means we discard our whole hand
   else: # Any other number just discard as many cards at random.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = handRandomDiscard(targetPL.hand, discardNR * multiplier, targetPL, silent = True)
      if re.search(r'isCost', Autoscript) and count < discardNR:
         whisper("You do not have enough cards in your hand to discard")
         return ('ABORT',0)
   if count == 0: return (announceText,count) # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} discards {} cards".format(announceText, count)
   else: announceString = "{}{} discard {} cards from their hand".format(announceText,otherTXT, count)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< DiscardX()")
   return (announceString,count)
         
def ReshuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ReshuffleX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   mute()
   X = 0
   action = re.search(r'\bReshuffle([A-Za-z& ]+)', Autoscript)
   #confirm("Bump1! Autoscript = {}, Action1 = {}".format(Autoscript, action.group(1))) # Debug
   if action.group(1) == 'HQ':
      namestuple = handtoStack(me.hand, True) # We do a silent hand reshuffle into the deck, which returns a tuple
      X = namestuple[2] # The 3rd part of the tuple is how many cards were in our hand before it got shuffled.
   elif action.group(1) == 'Archives':
      if ds == "corp": archivestoStack(me.piles['Archives(Hidden)'], True)
      namestuple = archivestoStack(me.piles['Trash/Archives(Face-up)'], True)    
   else: 
      whisper("Wat Group? [Error in autoscript!]")
      return 'ABORT'
   shuffle(me.piles['R&D/Stack'])
   if notification == 'Quick': announceString = "{} shuffles their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   else: announceString = "{} shuffle their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< ReshuffleX()")
   return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ShuffleX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   mute()
   action = re.search(r'\bShuffle([A-Za-z& ]+)', Autoscript)
   targetPL = ofwhom(Autoscript)
   if action.group(1) == 'Trash' or action.group(1) == 'Archives': pile = targetPL.piles['Trash/Archives(Face-up)']
   elif action.group(1) == 'Stack' or action.group(1) == 'R&D': pile = targetPL.piles['R&D/Stack']
   elif action.group(1) == 'Hidden Archives': pile = targetPL.piles['Archives(Hidden)']
   random = rnd(10,100) # Small wait (bug workaround) to make sure all animations are done.
   shuffle(pile)
   if notification == 'Quick': announceString = "{} shuffles their {}".format(announceText, pile.name)
   elif targetPL == me: announceString = "{} shuffle their {}".format(announceText, pile.name)
   else: announceString = "{} shuffle {}' {}".format(announceText, targetPL, pile.name)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< ShuffleX()")
   return announceString
   
def RollX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RollX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRoll([0-9]+)Dice', Autoscript)
   count = num(action.group(1))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   d6 = rolld6(silent = True) # For now we always roll 1d6. If we ever have a autoaction which needs more then 1, I'll implement it.
   if notification == 'Quick': announceString = "{} rolls {} on a die".format(announceText, d6)
   else: announceString = "{} roll {} on a die".format(announceText, d6)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< RollX()")
   return (announceString, d6)

def RequestInt(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RequestInt(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRequestInt(-Min)?([0-9]*)(-div)?([0-9]*)(-Max)?([0-9]*)', Autoscript)
   if action.group(2): 
      min = num(action.group(2))
      minTXT = ' (minimum {})'.format(min)
   else: 
      min = 0
      minTXT = ''
   if action.group(6): 
      max = num(action.group(6))
      minTXT += ' (maximum {})'.format(max)
   else: 
      max = None
   if action.group(4): 
      div = num(action.group(4))
      minTXT += ' (must be a multiple of {})'.format(div)
   else: div = 1
   number = min - 1
   while number < min or number % div or (max and number > max):
      number = askInteger("This effect requires that you provide an 'X'. What should that number be?{}".format(minTXT),min)
      if number == None: 
         whisper("Aborting Function")
         return 'ABORT'
   if debugVerbosity >= 4: notify("<<< RequestInt()")
   return (announceText, number) # We do not modify the announcement with this function.
   
def RunX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RunX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRun([A-Z][A-Za-z& ]+)', Autoscript)
   if action.group(1) == 'Generic': runTarget = ''
   else: runTarget = ' on {}'.format(action.group(1))
   if notification == 'Quick': announceString = "{} starts a run{}".format(announceText, runTarget)
   else: announceString = "{} start a run{}".format(announceText, runTarget)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< RunX()")
   return announceString

def SimplyAnnounce(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> SimplyAnnounce(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bSimplyAnnounce{([A-Za-z&,\. ]+)}', Autoscript)
   if notification == 'Quick': announceString = "{} {}".format(announceText, action.group(1))
   else: announceString = "{} {}".format(announceText, action.group(1))
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< SimplyAnnounce()")
   return announceString

def CreateDummy(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for creating dummy cards.
   if debugVerbosity >= 1: notify(">>> CreateDummy(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   global Dummywarn
   dummyCard = None
   action = re.search(r'\bCreateDummy[A-Za-z0-9_ -]*(-with)(?!onOpponent|-doNotTrash)([A-Za-z0-9_ -]*)', Autoscript)
   #confirm('actions: {}'.format(action.groups())) # debug
   targetPL = ofwhom(Autoscript)
   for c in table:
      if c.model == card.model and c.controller == targetPL and c.highlight == DummyColor: dummyCard = c # We check if already have a dummy of the same type on the table.
   if not dummyCard:
      if Dummywarn and re.search('onOpponent',Autoscript):
         if not confirm("This action creates an effect for your opponent and a way for them to remove it.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nYou opponent can activate any abilities meant for them on the Dummy card. If this card has one, they can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nOnce the dummy card is on the table, please right-click on it and select 'Pass control to {}'\
                     \n\nDo you want to see this warning again?".format(targetPL)): Dummywarn = False      
      elif Dummywarn:
         if not confirm("This card's effect requires that you trash it, but its lingering effects will only work automatically while a copy is in play.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nSome cards provide you with an ability that you can activate after they're been trashed. If this card has one, you can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nDo you want to see this warning again?"): Dummywarn = False
      elif re.search(r'onOpponent', Autoscript): confirm('The dummy card just created is meant for your opponent. Please right-click on it and select "Pass control to {}"'.format(targetPL))
      dummyCard = table.create(card.model, 500, 50 * playerside, 1) # This will create a fake card like the one we just created.
      dummyCard.highlight = DummyColor
   #confirm("Dummy ID: {}\n\nList Dummy ID: {}".format(dummyCard._id,passedlist[0]._id)) #Debug
   if not re.search(r'doNotTrash',Autoscript): card.moveTo(card.owner.piles['Trash/Archives(Face-up)'])
   if action.group(1): announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard, n = n) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   if debugVerbosity >= 4: notify("<<< CreateDummy()")
   return announceString # Creating a dummy isn't announced.

def ChooseKeyword(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for marking cards to be of a different keyword than they are
   if debugVerbosity >= 1: notify(">>> ChooseKeyword(){}".format(extraASDebug())) #Debug
   #confirm("Reached ChooseKeyword") # Debug
   choiceTXT = ''
   targetCardlist = ''
   existingKeyword = None
   if targetCards is None: targetCards = []
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   action = re.search(r'\bChooseKeyword{([A-Za-z\| ]+)}', Autoscript)
   #confirm("search results: {}".format(action.groups())) # Debug
   keywords = action.group(1).split('|')
   #confirm("List: {}".format(keywords)) # Debug
   if len(keywords) > 1:
      for i in range(len(keywords)): choiceTXT += '{}: {}\n'.format(i, keywords[i])
      choice = len(keywords)
   else: choice = 0
   while choice > len(keywords) - 1: 
      choice = askInteger("Choose one of the following keywords to assign to this card:\n\n{}".format(choiceTXT),0)
      if choice == None: return 'ABORT'
   for targetCard in targetCards:
      if targetCard.markers:
         for key in targetCard.markers:
            #confirm("Key: {}\n\nChoice: {}".format(key[0],keywords[choice])) # Debug
            if re.search('Keyword:',key[0]):
               existingKeyword = key
               #confirm("Added:{}".format(existingKeyword))
      if re.search(r'{}'.format(keywords[choice]),targetCard.Keywords):
         if existingKeyword: targetCard.markers[existingKeyword] = 0
         else: pass # If the keyword is anyway the same printed on the card, and it had no previous keyword, there is nothing to do
      elif existingKeyword:
         #confirm("Searching for {} in {}".format(keywords[choice],existingKeyword[0])) # Debug               
         if re.search(r'{}'.format(keywords[choice]),existingKeyword[0]): pass # If the keyword is the same as is already there, do nothing.
         else: 
            targetCard.markers[existingKeyword] = 0
            TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
      else: TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
   if notification == 'Quick': announceString = "{} marks {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   else: announceString = "{} mark {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< ChooseKeyword()")
   return announceString
            
def TraceX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> TraceX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bTrace([0-9]+)', Autoscript)
   multiplier = per(Autoscript, card, n, targetCards)
   Tracelimit = num(action.group(1)) * multiplier
   inputTraceValue(card, limit = Tracelimit)
   if action.group(1) != '0': limitText = ' (max power: {})'.format(Tracelimit)
   else: limitText = ''
   if notification == 'Quick': announceString = "{} starts a trace{}".format(announceText, limitText)
   else: announceString = "{} start a trace{}".format(announceText, limitText)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< TraceX()")
   return announceString

def ModifyStatus(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for modifying the status of a card on the table.
   if debugVerbosity >= 1: notify(">>> ModifyStatus(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   action = re.search(r'\b(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)(Target|Parent|Multi|Myself)[-to]*([A-Z][A-Za-z&_ ]+)?', Autoscript)
   if action.group(2) == 'Myself': 
      del targetCards[:] # Empty the list, just in case.
      targetCards.append(card)
   #confirm("groups: {}".format(action.groups())) #  Debug
   if action.group(3): dest = action.group(3)
   else: dest = 'hand'
   #confirm("dest: {}".format(dest)) # Debug
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   #confirm("List: {}".format(targetCards)) #Debug
   #for targetCard in targetCards: notify("ModifyX TargetCard: {}".format(targetCard)) #Debug
   for targetCard in targetCards:
      if action.group(1) == 'Rez' and intRez(targetCard, 'free', silent = True) != 'ABORT': pass
      elif action.group(1) == 'Derez'and derez(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Expose' and expose(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Uninstall' and uninstall(targetCard, dest, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Possess' and possess(card, targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Trash':
         if targetCard.owner != me: whisper(":::Note::: No automatic discard action is taken. Please ask the owner of the card to do take this action themselves.") # We do not discard automatically because it's easy to make a mistake that will be difficult to undo this way.
         elif intTrashCard(targetCard, targetCard.Stat, "free", silent = True) == 'ABORT': return 'ABORT' # If we're the owner however, it means that most likely it's ok to proceed and trash it.
      elif action.group(1) == 'Exile':
         if targetCard.owner != me: whisper(":::Note::: No automatic discard action is taken. Please ask the owner of the card to do take this action themselves.") # We do not discard automatically because it's easy to make a mistake that will be difficult to undo this way.
         elif exileCard(targetCard, silent = True) == 'ABORT': return 'ABORT'
      else: return 'ABORT'
      if action.group(2) != 'Multi': break # If we're not doing a multi-targeting, abort after the first run.
   if notification == 'Quick': announceString = "{} {}es {}".format(announceText, action.group(1), targetCardlist)
   else: announceString = "{} {} {}".format(announceText, action.group(1), targetCardlist)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< ModifyStatus()")
   return announceString
         
def InflictX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for inflicting Damage to players (even ourselves)
   if debugVerbosity >= 1: notify(">>> InflictX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   global DMGwarn, failedRequirement
   localDMGwarn = True #A variable to check if we've already warned the player during this damage dealing.
   action = re.search(r'\b(Inflict)([0-9]+)(Meat|Net|Brain)Damage', Autoscript) # Find out what kind of damage we're going
   multiplier = per(Autoscript, card, n, targetCards)
   enhancer = findEnhancements(Autoscript) #See if any of our cards increases damage we deal
   targetPL = ofwhom(Autoscript) #Find out who the target is
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0: #See if the target needs to be tagged.
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   elif re.search(r'ifTagged2', Autoscript) and targetPL.Tags < 2: #See if the target needs to be double tagged.
      whisper("Your opponent needs to be tagged twice to use this action")
      return 'ABORT'
   if enhancer > 0: enhanceTXT = ' (Enhanced: +{})'.format(enhancer) #Also notify that this is the case
   else: enhanceTXT = ''
   DMG = (num(action.group(2)) * multiplier) + enhancer #Calculate our damage
   preventTXT = ''
   if Automations['Damage']: #The actual effects happen only if the Damage automation switch is ON. It should be ON by default.
      if DMGwarn and localDMGwarn:
         localDMGwarn = False # We don't want to warn the player for every point of damage.
         if not confirm("You are about to inflict damage on another player.\
                       \nBefore you do that, please make sure that your opponent is not currently manipulating their hand or this might cause the game to crash.\
                     \n\nImportant: Before proceeding, ask your opponent to activate any cards they want that add protection against this type of damage\
                     \n\nDo you want this warning message will to appear again next time you do damage? (Recommended)"): DMGwarn = False
      if re.search(r'nonPreventable', Autoscript): 
         DMGprevented = 0
         preventTXT = ' (Unpreventable)'
      else: DMGprevented = findDMGProtection(DMG, action.group(3), targetPL)
      if DMGprevented > 0:
         preventTXT = ' ({} prevented)'.format(DMGprevented)
         DMG -= DMGprevented
      for DMGpt in range(DMG): #Start applying the damage
         if len(targetPL.hand) == 0 or currentHandSize(targetPL) == 0: 
            notify(":::Warning:::{} has flatlined!".format(targetPL)) #If the target does not have any more cards in their hand, inform they've flatlined.
            break
         else: #Otherwise, warn the player doing it for the first time
            DMGcard = targetPL.hand.random() # Pick a random card from their hand
            if targetPL.getGlobalVariable('ds') == 'corp': DMGcard.moveTo(targetPL.piles['Archives(Hidden)']) # If they're a corp, move it to the hidden archive
            else: DMGcard.moveTo(targetPL.piles['Trash/Archives(Face-up)']) #If they're a runner, move it to trash.
            if action.group(3) == 'Brain':  
               #targetPL.counters['Max Hand Size'].value -= 1 # If it's brain damage, also reduce the player's maximum handsize.               
               applyBrainDmg(targetPL)
   if targetPL == me: targetPL = 'theirself' # Just changing the announcement to fit better.
   if re.search(r'isRequirement', Autoscript) and DMG < 1: failedRequirement = True # Requirement means that the cost is still paid but other actions are not going to follow.
   if notification == 'Quick': announceString = "{} suffers {} {} damage{}".format(announceText,DMG,action.group(3),preventTXT)
   else: announceString = "{} inflict {} {} damage{} to {}{}".format(announceText,DMG,action.group(3),enhanceTXT,targetPL,preventTXT)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 4: notify("<<< InflictX()")
   return announceString

def findDMGProtection(DMGdone, DMGtype, targetPL): # Find out if the player has any card preventing damage
   if debugVerbosity >= 1: notify(">>> findDMGProtection(){}".format(extraASDebug())) #Debug
   if not Automations['Damage Prevention']: return 0
   protectionFound = 0
   protectionType = 'protection{}DMG'.format(DMGtype) # This is the string key that we use in the mdict{} dictionary
   for card in table:
      if card.controller == targetPL and card.markers[mdict[protectionType]]:
         while DMGdone > 0 and card.markers[mdict[protectionType]] > 0: # For each point of damage we do.
            protectionFound += 1 # We increase the protection found by 1
            DMGdone -= 1 # We reduce how much damage we still need to prevent by 1
            card.markers[mdict[protectionType]] -= 1 # We reduce the card's damage protection counters by 1
         if DMGdone == 0: break # If we've found enough protection to alleviate all damage, stop the search.
   if DMGtype == 'Net' or DMGtype == 'Brain': altprotectionType = 'protectionNetBrainDMG' # To check for the combined Net & Brain protection counter as well.
   else: altprotectionType = None
   for card in table: # We check for the combined protections after we use the single protectors.
      if card.controller == targetPL and altprotectionType and card.markers[mdict[altprotectionType]]:
         while DMGdone > 0 and card.markers[mdict[altprotectionType]] > 0: # For each point of damage we do.
            protectionFound += 1 # We increase the protection found by 1
            DMGdone -= 1 # We reduce how much damage we still need to prevent by 1
            card.markers[mdict[altprotectionType]] -= 1 # We reduce the card's damage protection counters by 1
         if DMGdone == 0: break # If we've found enough protection to alleviate all damage, stop the search.
   for card in table: # Finally we check for complete damage protection (i.e. protection from all types)
      if card.controller == targetPL and card.markers[mdict['protectionAllDMG']]:
         while DMGdone > 0 and card.markers[mdict['protectionAllDMG']] > 0: 
            protectionFound += 1 
            DMGdone -= 1
            card.markers[mdict['protectionAllDMG']] -= 1 
         if DMGdone == 0: break
   if debugVerbosity >= 4: notify("<<< findDMGProtection() by returning: {}".format(protectionFound))
   return protectionFound

def findEnhancements(Autoscript): #Find out if the player has any cards increasing damage dealt.
   if debugVerbosity >= 1: notify(">>> findEnhancements(){}".format(extraASDebug())) #Debug
   enhancer = 0
   DMGtype = re.search(r'\bInflict[0-9]+(Meat|Net|Brain)Damage', Autoscript)
   if DMGtype:
      enhancerMarker = 'enhanceDamage:{}'.format(DMGtype.group(1))
      if debugVerbosity >= 4: notify('#### encancerMarker: {}'.format(enhancerMarker))
      for card in table:
         if debugVerbosity >= 3: notify("### Checking {}".format(card)) #Debug
         cardENH = re.search(r'Enhance([0-9]+){}Damage'.format(DMGtype.group(1)), card.AutoScript)
         if card.controller == me and not card.markers[Not_rezzed] and cardENH: enhancer += num(cardENH.group(1))
         if card.controller == me and card.markers and not card.markers[Not_rezzed]:
            foundMarker = findMarker(card, enhancerMarker)
            if foundMarker: 
               enhancer += card.markers[foundMarker]
               card.markers[foundMarker] = 0
   if debugVerbosity >= 4: notify("<<< findEnhancements() by returning: {}".format(enhancer))
   return enhancer

def findVirusProtection(card, targetPL, VirusInfected): # Find out if the player has any virus preventing counters.
   if debugVerbosity >= 1: notify(">>> findVirusProtection(){}".format(extraASDebug())) #Debug
   protectionFound = 0
   if card.markers[mdict['protectionVirus']]:
      while VirusInfected > 0 and card.markers[mdict['protectionVirus']] > 0: # For each virus infected...
         protectionFound += 1 # We increase the protection found by 1
         VirusInfected -= 1 # We reduce how much viruses we still need to prevent by 1
         card.markers[mdict['protectionVirus']] -= 1 # We reduce the card's virus protection counters by 1
   if debugVerbosity >= 4: notify("<<< findVirusProtection() by returning: {}".format(protectionFound))
   return protectionFound

def findCounterPrevention(count, counter, targetPL): # Find out if the player has any markers preventing them form gaining specific counters (Bits, Agenda Points etc)
   if debugVerbosity >= 1: notify(">>> findCounterPrevention(){}".format(extraASDebug())) #Debug
   #confirm("Looking for Counter Prevention") # Debug
   preventionFound = 0
   forfeit = None
   preventionType = 'preventCounter:{}'.format(counter)
   forfeitType = 'forfeitCounter:{}'.format(counter)
   #confirm("Wut") # Debug
   for card in table:
      foundMarker = None # We clear the found markers before checking each card.
      if card.controller == targetPL and card.markers:
         for key in card.markers:
            #confirm("Key: {}\n\nChoice: {}".format(key[0],keywords[choice])) # Debug
            if key[0] == preventionType or key[0] == forfeitType:
               foundMarker = key
               #confirm("Added:{}".format(existingKeyword))
      else: continue # If the card doesn't have any markers, it doesn't offer any prevention.
      #confirm("Wutwut") # Debug
      if foundMarker: # If we found a counter prevention marker of the specific type we're looking for...
         while count > 0 and card.markers[foundMarker] > 0: # For each point of damage we do.
            preventionFound += 1 # We increase the prevention found by 1
            count -= 1 # We reduce how much counter we still need to add by 1
            card.markers[foundMarker] -= 1 # We reduce the specific counter prevention counters by 1
         if count == 0: break # If we've found enough protection to alleviate all counters, stop the search.
   if debugVerbosity >= 4: notify("<<< findCounterPrevention() by returning: {}".format(preventionFound))
   return preventionFound

def ofwhom(Autoscript): 
   if debugVerbosity >= 1: notify(">>> ofwhom(){}".format(extraASDebug())) #Debug
   if re.search(r'o[fn]Opponent', Autoscript):
      if len(players) > 1:
         for player in players:
            if player != me and player.getGlobalVariable('ds') != ds: 
               targetPL = player # Opponent needs to be not us, and of a different type. 
                                 # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
      else : 
         if debugVerbosity >= 1: whisper("There's no valid Opponents! Selecting myself.")
         targetPL = me
   else: targetPL = me
   return targetPL
   
def per(Autoscript, card = None, count = 0, targetCards = None, notification = None): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   if debugVerbosity >= 1: notify(">>> per(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   div = 1
   ignore = 0
   per = re.search(r'\b(per|upto)(Target|Parent|Every)?([A-Z][^-]*)-?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable.   
   if per: # If the  search was successful...
      if debugVerbosity >= 2: notify("Groups: {}. Count: {}".format(per.groups(),count)) #Debug
      if per.group(2) and (per.group(2) == 'Target' or per.group(2) == 'Every'): # If we're looking for a target or any specific type of card, we need to scour the requested group for targets.
         #confirm("Bump per Tablesearch") #Debug
         perCHK = per.group(3).split('_on_') # First we check to see if in our conditions we're looking for markers or card properties, to remove them from the checks
         perCHKSnapshot = list(perCHK)
         #confirm("Group3: {}\nperCHK: {}".format(per.group(3),perCHK)) #Debug
         for chkItem in perCHKSnapshot:
            if re.search(r'(Marker|Property|Any)',chkItem):
               perCHK.remove(chkItem) # We remove markers and card.properties from names of the card keywords  we'll be looking for later.
         #confirm("perCHK: {}".format(perCHK)) #Debug
         perItemMatch = [] # A list with all the properties we'll need to match on each card on the table.
         perItemExclusion = [] # A list with all the properties we'll need to match on each card on the table.
         cardProperties = [] #we're making a big list with all the properties of the card we need to match
         multiplier = 0
         iter = 0
         # We need to put all the different card keywords we'll be looking for in two lists. So we iterate through the available items and split on _or_ and _and_
         # The following code is not perfect (it will not figure out two different card types with different exclusions for example, but there's no such cards (yet)
         for chkItem in perCHK: 
            perItems = chkItem.split('_or_')              
            for perItem in perItems:
               subItems = perItem.split('_and_')
               for subItem in subItems:
                  regexCondition = re.search(r'{?([A-Z][A-Za-z0-9, ]*)}?', subItem)
                  if re.search(r'no[nt]', subItem): # If this is an exclusion item, we put it on the exclusion list.
                     perItemExclusion.append(regexCondition.group(1))
                  else:
                     perItemMatch.append(regexCondition.group(1))
         if debugVerbosity >= 2: notify('+++ Matches: {}\nExclusions: {}'.format(perItemMatch, perItemExclusion)) # Debug
         if re.search(r'fromHand', Autoscript): cardgroup = [c for c in me.hand]
         else: cardgroup = [c for c in table]
         for c in cardgroup: # Go through each card on the table and gather its properties, then see if they match.
            del cardProperties[:] # Cleaning the previous entries
            cFaceD = False # Variable to note down if a card was face-down when we were checking it, or not.
            if c.targetedBy and not c.isFaceUp: # If the card we're checking is not face up, we turn it temporarily to grab its properties for checking. We only check targeted cards though.
               c.isFaceUp = True
               cFaceD = True
               random = rnd(10,100) # Bug workaround.
            cardProperties.append(c.name) # We are going to check its name
            cardProperties.append(c.Type) # It's type
            cardSubtypes = getKeywords(c).split('-') # And each individual trait. Traits are separated by " - "
            for cardSubtype in cardSubtypes:
               strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
               if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
            cardProperties.append(c.Player) # We are also going to check if the card is for runner or corp.
            if cFaceD: c.isFaceUp = False # If the card was originally face-down, return it to that state again.
            perCHK = True # Variable to show us if the card we're checking is still passing all the requirements.
            #confirm("Bump") #Debug
            if debugVerbosity >= 3: notify("### Starting check with {}.\nProperties: {}".format(c, cardProperties)) # Debug
            for perItem in perItemMatch: # Now we check if the card properties include all the properties we need
               if perItem not in cardProperties: perCHK = False # The perCHK starts as True. We only need one missing item to turn it to False, since they all have to exist.
            for perItem in perItemExclusion:
               if perItem in cardProperties: perCHK = False # Pretty much the opposite of the above.
            if perCHK: # If we still have not dismissed the card and we're supposed to reveal them to the other players...
               #notify("group2: {}. card is: {}. Targeting is: {}".format(per.group(2),c,c.targetedBy))
               if re.search(r'isExposeTarget', Autoscript) and c.isFaceUp: perCHK = False                             # We exclude the card if it's supposed to get exposed but can't (i.e. see encryption breakthrough)
               if re.search(r'isRezzed', Autoscript) and (c.markers[Not_rezzed] or not c.isFaceUp): perCHK = False    # We exclude the card if it's supposed to be rezzed but isn't
               if re.search(r'isUnrezzed', Autoscript) and (c.isFaceUp or not c.markers[Not_rezzed]): perCHK = False  # We exclude the card if it's supposed to be unrezzed but isn't
               if re.search(r'Target',per.group(2)) and (not c.targetedBy or not c.targetedBy == me): perCHK = False  # We exclude the card if we only gather targets but it's not one.
            if perCHK: # Here we find out how much multiplier we get from those cards.
               if debugVerbosity >= 3: notify("### Target Found: {}".format(c)) # Debug
               if re.search(r'isExposeTarget', Autoscript) and not c.isFaceUp and c.targetedBy == me: expose(c) # If the card is supposed to be exposed to get the benefit, then do so now.
               if re.search(r'(Reveal&Shuffle|Reveal&Recover)', Autoscript) and c.targetedBy and c.targetedBy == me: 
                  c.moveToTable((70 * iter) - 150, 0 - yaxisMove(card), False) # If the card is supposed to be revealed to get the benefit, then we do so now
                  c.highlight = RevealedColor
                  notify("- {} reveals {} from their hand".format(me,c))
                  iter +=1
               if re.search(r'SendToTrash', Autoscript) and c.targetedBy and c.targetedBy == me: handDiscard(c)
               if re.search(r'Marker',per.group(3)): #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
                  markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # If we're looking for markers on the card, increase the multiplier by the number of markers found.
                  marker = findMarker(card, markerName.group(1))
                  if marker: multiplier += card.markers[marker]
               elif re.search(r'Property',per.group(3)): # If we're looking for a specific property on the card, increase the multiplier by the total of the properties on the cards found.
                  property = re.search(r'Property{([\w ]+)}',per.group(3))
                  multiplier += num(c.properties[property.group(1)]) # Don't forget to turn it into an integer first!
               else: multiplier += 1 * chkPlayer(Autoscript, c.controller, False) # If the perCHK remains 1 after the above loop, means that the card matches all our requirements. We only check faceup cards so that we don't take into acoount peeked face-down ones.
                                                                                  # We also multiply it with chkPlayer() which will return 0 if the player is not of the correct allegiance (i.e. Rival, or Me)
         #confirm("Finished checking") # Debug
         revealedCards = [c for c in table if c.highlight == RevealedColor] # If we have any revealed cards that need to be reshuffled, we need to do so now.
         if re.search(r'Reveal&Shuffle', Autoscript) and len(revealedCards) > 0: 
            confirm("The cards you've just revealed will be reshuffled into your deck once your opponents have had a chance to look at them.\
                   \nOnce you are ready, press any button to reshuffle them back into your deck")
            for c in revealedCards: c.moveTo(me.piles['R&D/Stack'])
            random = rnd(10,500) # Bug workaround.
            shuffle(me.piles['R&D/Stack'])
            notify("- {} Shuffles their revealed cards back into their deck".format(me))
         if re.search(r'Reveal&Recover', Autoscript) and len(revealedCards) > 0: 
            confirm("The cards you've just revealed will be returned to your hand once your opponents have had a chance to look at them.\
                   \nOnce you are ready, press any button to return them to your hand.")
            for c in revealedCards: c.moveTo(me.hand)
            notify("- {} returns the revealed cards back into their hand".format(me))
      else: #If we're not looking for a particular target, then we check for everything else.
         if debugVerbosity >= 3: notify("### Doing no table lookup") # Debug.
         if per.group(3) == 'X': multiplier = count # Probably not needed and the next elif can handle alone anyway.
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
         elif re.search(r'Marker',per.group(3)):
            markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the card.autoscript
            marker = findMarker(card, markerName.group(1))
            if marker: multiplier = card.markers[marker]
            else: multiplier = 0
         elif re.search(r'Property',per.group(3)):
            property = re.search(r'Property{([\w ]+)}',per.group(3))
            multiplier = card.properties[property.group(1)]
      if debugVerbosity >= 3: notify("### Checking ignore") # Debug.            
      ignS = re.search(r'-ignore([0-9]+)',Autoscript)
      if ignS: ignore = num(ignS.group(1))
      if debugVerbosity >= 3: notify("### Checking div") # Debug.            
      divS = re.search(r'-div([0-9]+)',Autoscript)
      if divS: div = num(divS.group(1))
   else: multiplier = 1
   if debugVerbosity >= 3: notify("<<< per() with Multiplier: {}".format((multiplier - ignore) / div)) # Debug
   return (multiplier - ignore) / div

def chkPlayer(Autoscript, controller, manual): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   if debugVerbosity >= 1: notify(">>> chkPlayer(){}".format(extraASDebug())) #Debug
   byOpponent = re.search(r'byOpponent', Autoscript)
   byMe = re.search(r'byMe', Autoscript)
   if debugVerbosity >= 3: notify("### byMe: {}. byOpponent: {}".format(byMe,byOpponent))
   if manual: return 1 #manual means that the actions was called by a player double clicking on the card. In which case we always do it.
   elif not byOpponent and not byMe: return 1 # If the card has no restrictions on being us or a rival.
   elif byOpponent and controller != me: return 1 # If the card needs to be played by a rival.
   elif byMe and controller == me: return 1 # If the card needs to be played by us.
   if debugVerbosity >= 4: notify("<<< chkPlayer() with Return 0") # Debug
   else: return 0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 which will make the multiplier 0.
   
def autoscriptOtherPlayers(lookup, count = 1): # Function that triggers effects based on the opponent's cards.
# This function is called from other functions in order to go through the table and see if other players have any cards which would be activated by it.
# For example a card that would produce bits whenever a trace was attempted. 
   if debugVerbosity >= 1: notify(">>> autoscriptOtherPlayers(){}".format(extraASDebug())) #Debug
   if not Automations['Play, Score and Rez']: return # If automations have been disabled, do nothing.
   for card in table:
      #notify('Checking {}'.format(card)) # Debug
      if not card.isFaceUp or card.markers[mdict['Not_rezzed']]: continue # Don't take into accounts cards that are not rezzed.
      costText = '{} activates {} to'.format(card.controller, card) 
      if re.search(r'{}'.format(lookup), card.AutoScript): # Search if in the script of the card, the string that was sent to us exists. The sent string is decided by the function calling us, so for example the ProdX() function knows it only needs to send the 'GeneratedSpice' string.
         Autoscripts = card.AutoScript.split('||')
         AutoScriptSnapshot = list(Autoscripts)
         for autoS in AutoScriptSnapshot: # Checking and removing anything other than whileRezzed or whileScored.
            if not re.search(r'while(Rezzed|Scored)', autoS): Autoscripts.remove(autoS)
         if len(Autoscripts) == 0: return
         for AutoS in Autoscripts:
            #confirm('Autoscripts: {}'.format(AutoS)) # Debug
            effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{} -]*)', AutoS)
            passedScript = "{}".format(effect.group(0))
            #confirm('effects: {}'.format(passedScript)) #Debug
            if effect.group(1) == 'Gain' or effect.group(1) == 'Lose':
               GainX(passedScript, costText, card, notification = 'Automatic', n = count) # If it exists, then call the GainX() function, because cards that automatically do something when other players do something else, always give the player something directly.
            if re.search(r'(Put|Remove|Refill|Use|Infect)', effect.group(1)): 
               TokensX(passedScript, costText, card, notification = 'Automatic', n = count)
   if debugVerbosity >= 4: notify("<<< autoscriptOtherPlayers()") # Debug
   
def customScript(card, action = 'play'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   if debugVerbosity >= 1: notify(">>> customScript(){}".format(extraASDebug())) #Debug
   global ModifyDraw
   #confirm("Customscript") # Debug
   if card.name == 'Microtech AI Interface' and action == 'use':
      targetPL = ofwhom('ofOpponent')
      group = targetPL.piles['R&D/Stack']
      cut = askInteger("How many cards from your opponent's deck do you wish to cut to the bottom?", 20)
      for c in group.top(cut): c.moveToBottom(group)
      notify("{} cuts the top {} cards from {}'s R&D to the bottom.".format(me, cut, targetPL))
   elif card.name == 'Crash Everett, Inventive Fixer':
      if action == 'play': ModifyDraw = True
      elif action == 'trash' or action =='uninstall': ModifyDraw = False
   elif card.name == 'New Blood' and action == 'play':
      previousIce = None
      firstIce = None
      lastIce = None # Just being thorough...
      for c in table:
         if c.controller == me and c in Stored_Type and Stored_Type[c] == 'Ice' and c.markers[Not_rezzed]:
            if not firstIce: firstIce = c
            c.isFaceUp = False
            if previousIce:
               coinflip = rnd(1,2) # As I said, just being thoroughly random ^_^
               if coinflip == 1: # We switch the current one with the previous one
                  xp, yp = previousIce.position # We save the previous Ice's position we checked in order to move them later
                  previousIce.moveToTable(c.position[0],c.position[1]) # We move the previous Ice we found to this position
                  c.moveToTable(xp,yp) # And we move the Ice we're currently checking to the previous position.
               else: #We move the first one to the current one's position, the previous one to the first one's position, and the current one to the previous one's position.
                  if previousIce == firstIce: continue # However do nothing if it's on the first pair of Ice, as the first is going to be the same as the previous one.
                  xp, yp = previousIce.position
                  xf, yf = firstIce.position
                  firstIce.moveToTable(c.position[0],c.position[1]) 
                  previousIce.moveToTable(xf, yf) 
                  c.moveToTable(xp,yp) 
               previousIce = None
            else: previousIce = c
      if previousIce: # If we have a "previous Ice" it means this is the last card, and it was an odd number of Ice, so it hasn't been swapped at all.
         coinflip = rnd(1,2)
         if coinflip == 1: # We switch the current one with the first one
            xp, yp = previousIce.position 
            previousIce.moveToTable(firstIce.position[0],firstIce.position[1]) 
            firstIce.moveToTable(xp,yp) 
         else: pass # We leave the last ice were it was.
      confirm("Your unrezzed Ice has been turn face down and slightly scrambled to throw off your opponent. You can close this window and continue exchanging pairs")
   elif card.name == 'Dr. Dreff' and action == 'use':
      for c in me.hand:
         if c.targetedBy and c.targetedBy == me:
            if c.type != 'Ice':
               whisper(":::ERROR::: Invalid Card. Please Select an Ice")
               return
            if payCost(num(c.Cost) / 2) == 'ABORT': return
            c.moveToTable(0,cheight(c) * playerside)
            c.highlight = EmergencyColor
            notify("{} activates {} in order to emergency rez {} for {} for this run".format(me,card,c,uniBit(num(c.Cost) / 2)))
            return # We don't want to play more than one Ice if the player has for some reason targeted more than 1.
   elif card.name == 'Social Engineering' and action == 'play':
      hiddenCount = askInteger("How many bits do you want to hide?\n\nMin: 2\nMax: {}".format(me.counters['Bit Pool'].value),2)
      while me.counters['Bit Pool'].value < hiddenCount or hiddenCount < 2:
         hiddenCount = askInteger(":::ERROR::: You cannot hide more bits than you have in your Bit Pool, or less than 2. Close this window to abort!\
                               \n\nHow many bits do you want to hide?\n\nMin: 2\nMax: {}".format(me.counters['Bit Pool'].value),2)
         if hiddenCount == None: 
            notify("{} has aborted their Social Engineering attempt".format(me))
            card.moveTo(me.hand)
            me.counters['Bit Pool'].value += 1
            me.counters['Actions'].value += 1
            return
      targetPL = ofwhom('ofOpponent')
      notify(":::Warning::: {} is making a social engineering attempt! {} must now try to guess how many bits they are hiding (min 2, max {})".format(me, targetPL, me.counters['Bit Pool'].value))
      confirm("You have now hidden this amount of bits. Once your opponent makes a guess, press any button to reveal the true amount.")
      notify("{} was hiding {} bits".format(me,hiddenCount))
   elif card.name == 'Corporate War' and action == 'score':
      if me.counters['Bit Pool'].value >= 12:
         bitsReduce = findCounterPrevention(12, 'Bits', me)
         if bitsReduce: extraTXT = " ({} forfeited)".format(uniBit(bitsReduce))
         else: extraTXT = ''               
         notify("{} has won the corporate war and their spoils are {} Bits{}".format(me,12 - bitsReduce,extraTXT))
         me.counters['Bit Pool'].value += 12 - bitsReduce
      else:
         notify("{} has lost the corporate war and their Bit Pool is reduced to 0".format(me))
         me.counters['Bit Pool'].value = 0
   elif card.name == 'Mystery Box' and action == 'use':
      group = me.piles['R&D/Stack']
      haveTarget = False
      foundPrograms = [c for c in table if c.highlight == RevealedColor]
      for targetCHK in foundPrograms: # We quickly check if the player has selected a target before using the Mystery Box again.
         if targetCHK.targetedBy and targetCHK.targetedBy == me: haveTarget = True
      if len(foundPrograms) == 1: # If we only found one program then it's necessarily selected by default.
         selectedProgram = foundPrograms[0]
         selectedProgram.highlight = None
         selectedProgram.moveToTable(-150, 65 * playerside - yaxisMove(card), False) # Move it to the normal position we install programs
         card.moveTo(me.piles['Trash/Archives(Face-up)'])
         shuffle(group)
         notify("{}'s Mystery Box has automatically installed {} free of cost".format(me,selectedProgram))
      elif len(foundPrograms) > 1:
         if not haveTarget: 
            whisper(":::ERROR::: Please select a target before using the Mystery Box again. Aborting!")
            return
         selectedProgram = None
         for targetSeek in foundPrograms:
            if not selectedProgram and targetSeek.targetedBy and targetSeek.targetedBy == me: # We only want to select the first program we find. The rest we ignore.
               selectedProgram = targetSeek
               selectedProgram.highlight = None
               selectedProgram.moveToTable(-150, 65 * playerside - yaxisMove(card), False) # Move it to the normal position we install programs
            else: targetSeek.moveToBottom(group) # If the program is highlighted but not targeted, then send it back to the stack.
         shuffle(group)                  
         card.moveTo(me.piles['Trash/Archives(Face-up)'])
         notify("{}'s Mystery Box has automatically installed {} free of cost".format(me,selectedProgram))
   elif card.name == 'Security Purge' and action == 'score':
      group = me.piles['R&D/Stack']
      haveTarget = False
      iter = 0
      for c in group.top(3):
         c.moveToTable((70 * iter) - 150, 0 - yaxisMove(card), False)
         c.orientation ^= Rot90
         if c.type != 'Ice': c.moveTo(me.piles['Trash/Archives(Face-up)'])
         else: iter +=1
      if iter: # If we found any ice in the top 3
         notify("{} initiates a Security Purge and reveals {} Ice from the top of their R&D. These ice are automatically installed and rezzed".format(me, iter))
      else: notify("{} initiates a Security Purge but it finds nothing to purge.".format(me))
   elif action == 'use': useCard(card)

def atTurnStartEndEffects(Time = 'Start'): # Function which triggers card effects at the start or end of the turn.
   if debugVerbosity >= 1: notify(">>> atTurnStartEndEffects() at time: {}".format(Time)) #Debug
   if not Automations['Start/End-of-Turn']: return
   TitleDone = False
   for card in table:
      if card.controller != me: continue
      if debugVerbosity >= 4: notify("### {} Autoscript: {}".format(card, card.AutoScript))
      Autoscripts = card.AutoScript.split('||')
      for AutoScript in Autoscripts:
         if debugVerbosity >= 4: notify("### split Autoscript: {}".format(AutoScript))
         effect = re.search(r'atTurn(Start|End):([A-Z][A-Za-z]+)([0-9]+)([A-Za-z0-9 ]+)(.*)', AutoScript)
         if debugVerbosity >= 2 and effect: notify("!!! effects: {}".format(effect.groups()))
         if not effect: continue
         if re.search(r'excludeDummy', AutoScript) and card.highlight == DummyColor: continue
         if re.search(r'onlyforDummy', AutoScript) and card.highlight != DummyColor: continue
         if effect.group(1) != Time: continue # If it's a start-of-turn effect and we're at the end, or vice-versa, do nothing.
         if effect.group(5) and re.search(r'isOptional', effect.group(5)) and not confirm("{} can have the following optional ability activated at the start of your turn:\n\n[ {} {} {} ]\n\nDo you want to activate it?".format(card.name, effect.group(2), effect.group(3),effect.group(4))): continue
         if not TitleDone: notify(":::{}'s {}-of-Turn Effects:::".format(me,effect.group(1)))
         TitleDone = True
         if debugVerbosity >= 2: notify("### effects: {}".format(effect.groups())) # Debug
         effectNR = num(effect.group(3))
         passedScript = '{}'.format(effect.group(0))
         if debugVerbosity >= 3: notify("### passedScript: {}".format(passedScript))
         if card.highlight == DummyColor: announceText = "{}'s lingering effects:".format(card)
         else: announceText = "{}:".format(card)
         if effect.group(2) == 'Gain' or effect.group(2) == 'Lose':
            GainX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Transfer':
            TransferX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Draw':
            DrawX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Refill' or effect.group(2) == 'Remove':
            TokensX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Inflict':
            InflictX(passedScript, announceText, card, notification = 'Automatic')
   if me.counters['Bit Pool'].value < 0: 
      notify(":::Warning::: {}'s {}-of-turn effects cost more Bits than {} had in their Bit Pool!".format(me,Time,me))
   if ds == 'corp' and Time =='Start': draw(me.piles['R&D/Stack'])
   if TitleDone: notify(":::--------------------------:::".format(me))

#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global Stored_Type, Stored_Cost, ds, Stored_Keywords, debugVerbosity
   mute()
   if debugVerbosity >=0:
      if debugVerbosity == 0: debugVerbosity = 1
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      notify("Debug verbosity is now: {}".format(debugVerbosity))
      return
   for player in players:
      if player.name == 'db0' or player.name == 'dbzer0': debugVerbosity = 0
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   testcards = ["429dc83b-8c45-439b-b31a-b08afcb61314", # Project Zurich
                "f2ddb0b1-af2b-4d8d-bac1-ea0cd8a2a43d", # Death from Above
                "c7ac08e2-2190-47de-a345-6b1e9e5e770b", # Raymond Ellison
                "31cb5ed8-ca36-4637-b78f-ec10c1c28526", # Rent-to-Own Contract # This will need one of those markers that have their own abilities
                "b10c3681-9bb3-481b-af86-64649b6e78db", # Morphing Tool
                "a159245f-3527-4a0b-895a-0db43515231d", # Liberated Savings Account
                "d0d575f8-fbd4-4da1-8c0e-bca28a7310ea", # Please Don't Choke Anyone
                "b5712c36-5e00-4e5d-836a-43d9047b5a4a"] # Arasaka Owns You
   if not ds: ds = "corp"
   me.setGlobalVariable('ds', ds) 
   me.counters['Bit Pool'].value = 50
   me.counters['Max Hand Size'].value = 5
   me.counters['Tags'].value = 1
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 10
   me.Actions = 15
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      chooseSide()
      createStartingCards()
   for idx in range(len(testcards)):
      test = table.create(testcards[idx], (70 * idx) - 150, 0, 1, True)
      Stored_Type[test] = test.Type
      Stored_Keywords[test] = getKeywords(test)
      Stored_Cost[test] = test.Cost
      Stored_AutoActions[test] = test.AutoAction
      #random = rnd(10,500)
      if test.Type == 'Ice' or test.Type == 'Agenda' or test.Type == 'Node':
         test.isFaceUp = False
         test.markers[Not_rezzed] += 1
         
def extraASDebug(Autoscript = None):
   if Autoscript and debugVerbosity >= 3: return ". Autoscript:{}".format(Autoscript)
   else: return ''

def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if debugVerbosity >= 1: notify(">>> inspectCard(){}".format(extraASDebug())) #Debug
   ASText = "This card has the following automations:\n"
   if re.search(r'onPlay', card.Autoscript): ASText += '\n * It will have an effect when coming into play from your hand.'
   if re.search(r'onScore', card.Autoscript): ASText += '\n * It will have an effect when being scored.'
   if re.search(r'onRez', card.Autoscript): ASText += '\n * It will have an effect when its being rezzed.'
   if re.search(r'whileRezzed', card.Autoscript): ASText += '\n * It will has a continous effect while in play.'
   if re.search(r'whileScored', card.Autoscript): ASText += '\n * It will has a continous effect while scored.'
   if re.search(r'atTurnStart', card.Autoscript): ASText += '\n * It will perform an automation at the start of your turn.'
   if re.search(r'atTurnEnd', card.Autoscript): ASText += '\n * It will perform an automation at the end of your turn.'
   if card.AutoAction != '': 
      if ASText == 'This card has the following automations:\n': ASText == '\nThis card will perform one or more automated actions when you double click on it.'
      else: ASText += '\n\nThis card will also perform one or more automated actions when you double click on it.'
   if ASText == 'This card has the following automations:\n': ASText = '\nThis card has no automations.'
   if card.type == 'Tracing': confirm("This is your tracing card. Double click on it to start a tracing bid. It will ask you for your bid and then hide the amount.\
                                   \n\nOnce both players have made their bid, double-click on it again to reveal your hidden total.\
                                   \n\nAfter deciding who won the trace attempt, double click on the card one last time to pay the cost. This will automatically use bits from cards that pay for tracing if you have any.")
   elif card.type == 'Data Fort': confirm("These are your data forts. Start stacking your Ice above them and your Agendas, Upgrades and Nodes below them.\
                                     \nThey have no automated abilities")
   elif card.type == 'Counter Hold': confirm("This is your Counter Hold. This card stores all the beneficial and harmful counters you might accumulate over the course of the game.\
                                          \n\nIf you're playing a corp, viruses and other such tokens will be put here. By double clicking them, you'll spend three actions to clean all viruses from your cards.\
                                          \nIf you're playing a runner, brain damage markers and any tokens the corp gives you will be put here.\
                                        \n\nTo remove any token manually, simply drag & drop it out of this card.")
   else:
      if debugVerbosity: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(card.AutoScript,card.AutoAction)
      else: finalTXT = "Card Text: {}\n\n{}\n\nWould you like to see the card rulings?".format(card.Rules,ASText)
      if confirm("{}".format(finalTXT)):
         rulings(card)
