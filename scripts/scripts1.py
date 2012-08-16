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
               'Damage'             : True}

UniBits = True # If True, game will display bits as unicode characters ❶, ❷, ❿ etc

ModifyDraw = False #if True the audraw should warn the player to look at r&D instead 
TraceValue = 0

DifficultyLevels = { }

TypeCard = {}
KeywordCard = {}
CostCard = {}

MemoryRequirements = { }
InstallationCosts = { }
maxActions = 3
scoredAgendas = 0
playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is

DMGwarn = True # A boolean varialbe to track whether we've warned the player about doing automatic damage.
Dummywarn = True # Much like above, but it serves to remind the player not to trash some cards.
DummyTrashWarn = True
ExposeTargetsWarn = True # A boolean variable that reminds the player to select multiple targets to expose for used by specific cards like Encryption Breakthrough
RevealandShuffleWarn = True # Similar to above.
newturn = True #We use this variable to track whether a player has yet to do anything this turn.
endofturn = False #We use this variable to know if the player is in the end-of-turn phase.
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
             PlusOne= ("+1", "aa261722-e12a-41d4-a475-3cc1043166a7"),
             MinusOne= ("-1", "48ceb18b-5521-4d3f-b5fb-c8212e8bcbae"),
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
   if not s: return 0
   try:
      return int(s)
   except ValueError:
      return 0

def chooseSide(): # Called from many functions to check if the player has chosen a side for this game.
   mute()
   global playerside, playeraxis
   if playerside == None:  # Has the player selected a side yet? If not, then...
     if me.hasInvertedTable():
        playeraxis = Yaxis
        playerside = -1
     else:
        playeraxis = Yaxis
        playerside = 1

def uniBit(count):
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
        elif count == 10: return '❿'
        else: return "({})".format(count)
    else: return "({})".format(count)
 
def uniAction():
   if UniBits: return '⏎'
   else: return '|>'

def chooseWell(limit, choiceText, default = None):
   if default == None: default = 0# If the player has not provided a default value for askInteger, just assume it's the max.
   choice = limit # limit is the number of choices we have
   if limit > 1: # But since we use 0 as a valid choice, then we can't actually select the limit as a number
      while choice >= limit:
         choice = askInteger("{}".format(choiceText), default)
         if not choice: return False
         if choice > limit: whisper("You must choose between 0 and {}".format(limit - 1))
   else: choice = 0 # If our limit is 1, it means there's only one choice, 0.
   return choice   
#---------------------------------------------------------------------------
# Card Placement functions
#---------------------------------------------------------------------------

def cwidth(card, divisor = 10):
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
   if divisor == 0: offset = 0
   else: offset = card.height() / divisor
   return (card.height() + offset)

def yaxisMove(card):
# Variable to move the cards played by player 2 on a 2-sided table, more towards their own side. 
# Player's 2 axis will fall one extra card length towards their side.
# This is because of bug #146 (https://github.com/kellyelton/OCTGN/issues/146)
   if me.hasInvertedTable(): cardmove = cheight(card)
   else: cardmove = cardmove = 0
   return cardmove

def getKeywords(card): # A function which combines the existing card keywords, with markers which give it extra ones.
   global KeywordCard
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
               keywordsList.append(markerKeyword.group(1))
            else: keywordsList.append(markerKeyword.group(1))
            
   keywords = ''
   for KW in keywordsList:
      keywords += '{}-'.format(KW)
   KeywordCard[card] = keywords[:-1] # We also update the global variable for this card, which is used by many functions.
   #notify("List {}\n\nResult: {}".format(keywordsList,keywords[:-1])) # Debug
   return keywords[:-1] # We need to remove the trailing dash '-'
   
#---------------------------------------------------------------------------
# Actions indication
#---------------------------------------------------------------------------

def useAction(group = table, x=0, y=0, count = 1):
   mute()
   extraText = ''
   if me.Actions < count: 
      if not confirm("You have no more actions left. Are you sure you want to continue?"): return 'ABORT'
      else: extraText = ' (Exceeding Max!)'
   act = (maxActions - me.Actions) + 1# maxActions is different for corp and runner and is set during jackIn()
                                      # We give act +1 because otherwise the first action would be action #0.
   me.Actions -= count
   if count == 2: return "{} {} {} takes Double Action #{} and #{}{}".format(uniAction(),uniAction(),me,act, act + 1,extraText)
   elif count == 3: return "{} {} {} {} takes Triple Action #{}, #{} and #{}{}".format(uniAction(),uniAction(),uniAction(),me,act, act + 1,act + 2,extraText)
   else: return "{} {} takes Action #{}{}".format(uniAction(),me,act,extraText) # We give act +1 because otherwise the first action would be action #0.

def goToEndTurn(group, x = 0, y = 0):
    mute()
    global endofturn
    if ds == "":
        whisper ("Please perform the game setup first (Ctrl+Shift+S)")
        return
    if me.Actions > 0: # If the player has not used all their actions for this turn, remind them, just in case.
        if not confirm("You have not taken all your actions for this turn, are you sure you want to declare end of turn"): return
    if len(me.hand) > currentHandSize(): #If the player is holding more cards than their hand max. remind them that they need to discard some 
                                                       # and put them in the end of turn to allow them to do so.
        if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
            if not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
            else: notify(":::Warning::: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
        else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
            if ds == "corp": notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
            else: notify ("Runner {} is rebooting all systems for the day.".format(me))
            confirm(':::Warning:::\n\n You have more card in your hand than your current hand size maximum of {}. Please discard enough and then use the "Declare End of Turn" action again.'.format(currentHandSize()))
            endofturn = True
            return
    endofturn = False
    newturn = False
    atTurnStartEndEffects('End')
    if ds == "corp": notify ("=> The Corporation of {} has reached CoB (Close of Business hours).".format(me))
    else: notify ("=> Runner {} has gone to sleep for the day.".format(me))

def goToSot (group, x=0,y=0):
    global newturn, endofturn
    mute()
    if endofturn:
        if not confirm("You have not yet properly ended you previous turn. Are you sure you want to continue?"): return
        else: 
            if len(me.hand) > currentHandSize(): # Just made sure to notify of any shenanigans
                notify(":::Warning::: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
            else: notify(":::Warning::: {} has skipped their End-of-Turn phase".format(me))
            endofturn = False
    if ds == "":
        whisper ("Please perform the game setup first (Ctrl+Shift+S)")
        return
    if me.Actions < 0: 
        if not confirm("Your actions were negative from last turn. Was this a result of a penalty you suffered from a card?"): 
            me.Actions = maxActions # If the player did not have a penalty, then we assume those were extra actions granted by some card effect, so we make sure they have their full maximum
        else: 
            me.Actions += maxActions # If it was a penalty, then it remains with them for this round, which means they have less actions to use.
            notify("{} is starting with {} less actions this turn, due to a penalty from a previous turn. They have {} actions this turn".format(me,maxActions - me.Actions, me.Actions))
    else: me.Actions = maxActions
    myCards = (card for card in table if card.controller == me and card.owner == me)
    for card in myCards: 
      if card in TypeCard and TypeCard[card] != 'Ice': card.orientation &= ~Rot90 # Refresh all cards which can be used once a turn.
    newturn = True
    atTurnStartEndEffects('Start') # Check all our cards to see if there's any Start of Turn effects active.
    if ds == "corp": notify("=> The offices of {}'s Corporation are now open for business.".format(me))
    else: notify ("=> Runner {} has woken up".format(me))

def modActions(group,x=0,y=0):
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
   global Automations
   if (Automations[type] and command == 'Off') or (not Automations[type] and command == 'Announce'):
      notify ("--> {}'s {} automations are OFF.".format(me,type))
      if command != 'Announce': Automations[type] = False
   else:
      notify ("--> {}'s {} automations are ON.".format(me,type))
      if command != 'Announce': Automations[type] = True
   
def switchPlayAutomation(group,x=0,y=0):
   switchAutomation('Play, Score and Rez')
   
def switchStartEndAutomation(group,x=0,y=0):
   switchAutomation('Start/End-of-Turn')

def switchDMGAutomation(group,x=0,y=0):
   switchAutomation('Damage')
        
def switchUniBits(group,x=0,y=0,command = 'Off'):
    global UniBits
    if UniBits and command != 'On':
        whisper("Bits and Actions will now be displayed as normal ASCII.".format(me))
        UniBits = False
    else:
        whisper("Bits and Actions will now be displayed as Unicode.".format(me))
        UniBits = True

def ImAProAtThis(group, x=0, y=0):
   global DMGwarn, Dummywarn, DummyTrashWarn, ExposeTargetsWarn, RevealandShuffleWarn
   DMGwarn = False 
   Dummywarn = False 
   ExposeTargetsWarn = False
   RevealandShuffleWarn = False
   DummyTrashWarn = False
   whisper("-- All Newbie warnings have been disabled. Play safe.")
        
def createStartingCards():
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
    global ds, maxActions
    mute()
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
    if ds == "corp":
        maxActions = 3
        me.Actions = maxActions
        me.Memory = 0
        NameDeck = "R&D"
        notify("{} is playing as Corporation".format(me))      
    else:
        maxActions = 4
        me.Actions = maxActions
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
   specialCards = eval(me.getGlobalVariable('specialCards'))
   specialCards[card.Type] = card._id
   me.setGlobalVariable('specialCards', str(specialCards))

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   specialCards = eval(player.getGlobalVariable('specialCards'))
   return Card(specialCards[cardType])
   
def start_token(group, x = 0, y = 0):
    card, quantity = askCard("[Type] = 'Setup'")
    if quantity == 0: return
    table.create(card, x, y, quantity)

#------------------------------------------------------------------------------
# Run...
#------------------------------------------------------------------------------
def intRun(ActionCost, Name):
	notify ("{} to start a run on {}.".format(ActionCost,Name))

def runHQ(group, x=0,Y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "HQ")

def runRD(group, x=0,Y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "R&D")

def runArchives(group, x=0,Y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun (ActionCost, "the Archives")

def runSDF(group, x=0,Y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if ds == "runner": intRun(ActionCost, "a subsidiary data fort")

#------------------------------------------------------------------------------
# Tags...
#------------------------------------------------------------------------------
def pay2andDelTag(group, x = 0, y = 0):
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
	mute()
	if ( count > 0):
		card.markers[Bits] += count
		if ( card.isFaceUp == True): notify("{} adds {} from the bank on {}.".format(me,uniBit(count),card))
		else: notify("{} adds {} on a card.".format(me,uniBit(count)))

def addBits(card, x = 0, y = 0):
   mute()
   count = askInteger("Add how many Bits?", 1)
   if count == None: return
   intAddBits(card, count)
	
def remBits(card, x = 0, y = 0):
   mute()
   count = askInteger("Remove how many Bits?", 1)
   if count == None: return
   if count > card.markers[Bits]: count = card.markers[Bits]
   card.markers[Bits] -= count
   if card.isFaceUp == True: notify("{} removes {} from {}.".format(me,uniBit(count),card))
   else: notify("{} removes {} from a card.".format(me,uniBit(count)))

def remBits2BP (card, x = 0, y = 0):
   mute()
   count = askInteger("Remove how many Bits?", 1)
   if count == None: return
   if count > card.markers[Bits]: count = card.markers[Bits]
   card.markers[Bits] -= count
   me.counters['Bit Pool'].value += count 
   if card.isFaceUp == True: notify("{} removes {} from {} to their Bit Pool.".format(me,uniBit(count),card))
   else: notify("{} takes {} from a card to their Bit Pool.".format(me,uniBit(count)))

def addPlusOne(card, x = 0, y = 0):
   mute()
   if MinusOne in card.markers:
      card.markers[MinusOne] -= 1
   else: 
      card.markers[PlusOne] += 1
   notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
   mute()
   if PlusOne in card.markers:
      card.markers[PlusOne] -= 1
   else:
      card.markers[MinusOne] += 1
   notify("{} adds one -1 marker on {}.".format(me,card))

def addMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
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
   mute()
   count = askInteger("Add how many counters?", 1)
   if count == None: return
   card.markers[Advance] += count
   if card.isFaceUp == True: notify("{} adds {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
   mute()
   count = askInteger("Remove how many counters?", 1)
   if count == None: return
   if count > card.markers[Advance]: count = card.markers[Advance]
   card.markers[Advance] -= count
   if card.isFaceUp == True: notify("{} removes {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def advanceCardM(card, x = 0, y = 0):
	mute()
	card.markers[Advance] -= 1
	if ( card.isFaceUp == True): notify("{} removes 1 advancement counter on {}.".format(me,card))
	else: notify("{} removes 1 advancement counter on a card.".format(me))

#---------------------
# Trace
#----------------------

def inputTraceValue (card, x=0,y=0, limit = 0, silent = False):
   global TraceValue
   mute()
   limitText = ''
   betReplaced = False
   card = getSpecial('Tracing')
   if not card.isFaceUp and not confirm("You're already placed a bet. Replace it with a new one?"): return
   else: betReplaced = True
   limit = num(limit) # Just in case
   if limit > 0: limitText = '\n\n(Max Trace Power: {})'.format(limit)
   TraceValue = askInteger("Bet How Many?{}".format(limitText), 0)
   if TraceValue == None: 
      whisper(":::Warning::: Trace bid aborted by player.")
      return
   while limit > 0 and TraceValue > limit:
      TraceValue = askInteger("Please bet equal or less than the max trace power!\nBet How Many?{}".format(limitText), 0)
      if TraceValue == None: 
         whisper(":::Warning::: Trace bid aborted by player.")
         return
   card.markers[Bits] = 0
   card.isFaceUp = False
   if not silent: 
      if not betReplaced: notify("{} chose a Trace Value.".format(me))
      else: notify("{} changed their hidden Trace Value.".format(me))
   TypeCard[card] = "Tracing"
	
def revealTraceValue (card, x=0,y=0):
   mute()
   global TraceValue
   card = getSpecial('Tracing')
   card.isFaceUp = True
   card.markers[Bits] = TraceValue
   notify ( "{} reveals a Trace Value of {}.".format(me,TraceValue))
   if TraceValue == 0: autoscriptOtherPlayers('TraceAttempt') # if the trace value is 0, then we consider the trace attempt as valid, so we call scripts triggering from that.
   TraceValue = 0

def payTraceValue (card, x=0,y=0):
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
   mute()
   card.isFaceUp = True
   TraceValue = 0
   card.markers[Bits] = 0
   notify ("{} cancels the Trace Value.".format(me) )

#------------------------------------------------------------------------------
# Other functions
#-----------------------------------------------------------------------------

def createSDF(group,x=0,y=0):
      table.create("98a40fb6-1fea-4283-a036-567c8adade8e", x, y, 1, True)

def intdamageDiscard(group,x=0,y=0):
   mute()
   if len(group) == 0:
      notify ("{} cannot discard at random. Have they flatlined?".format(me))
   else:
      card = group.random()
      if ds == 'corp': card.moveTo(me.piles['Archives(Hidden)'])
      else: card.moveTo(me.piles['Trash/Archives(Face-up)'])
      notify("{} discards {} at random.".format(me,card))

def addBrainDmg(group, x = 0, y = 0):
   applyBrainDmg()
   notify ("{} suffers 1 Brain Damage.".format(me) )
   intdamageDiscard(me.hand)

def applyBrainDmg(player = me):
   specialCard = getSpecial('Counter Hold', player)
   specialCard.markers[mdict['BrainDMG']] += 1

def currentHandSize(player = me):
   specialCard = getSpecial('Counter Hold', player)
   if specialCard.markers[mdict['BrainDMG']]: currHandSize =  player.counters['Max Hand Size'].value - specialCard.markers[mdict['BrainDMG']]
   else: currHandSize = player.counters['Max Hand Size'].value
   return currHandSize
   
def addMeatNetDmg(group, x = 0, y = 0):
    notify ("{} suffers 1 Net or Meat Damage.".format(me) )
    intdamageDiscard(me.hand)

def getBit(group, x = 0, y = 0):
    ActionCost = useAction()
    if ActionCost == 'ABORT': return
    notify ("{} and receives {}.".format(ActionCost,uniBit(1)))
    me.counters['Bit Pool'].value += 1
    
#------------------------------------------------------------------------------
# Other functions on card
#------------------------------------------------------------------------------

def payCost(count = 1, cost = 'not_free', counter = 'BP'): # A function that removed the cost provided from our bit pool, after checking that we have enough.
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
   #confirm("Bump ReduceCost") # Debug
   reduction = 0
   for c in table:
      #notify("Checking {} with AS: {}".format(c, c.AutoScript)) #Debug
      reductionSearch = re.search(r'Reduce([0-9#]+)Cost{}-for([A-Z][A-Za-z ]+)(-not[A-Za-z_& ]+)?'.format(type), c.AutoScript) 
      if c.controller == me and reductionSearch and c.markers[Not_rezzed] == 0 and c.isFaceUp: # If the above search matches (i.e. we have a card with reduction for Rez and a condition we continue to check if our card matches the condition)
         #confirm("Possible Match found in {}".format(c)) # Debug         
         if reductionSearch.group(3): 
            exclusion = re.search(r'-not([A-Za-z_& ]+)'.format(type), reductionSearch.group(3))
            if exclusion and (re.search(r'{}'.format(exclusion.group(1)), TypeCard[card]) or re.search(r'{}'.format(exclusion.group(1)), KeywordCard[card])): continue
         if reductionSearch.group(2) == 'All' or re.search(r'{}'.format(reductionSearch.group(2)), TypeCard[card]) or re.search(r'{}'.format(reductionSearch.group(2)), KeywordCard[card]): #Looking for the type of card being reduced into the properties of the card we're currently paying.
            #confirm("Search match! Group is {}".format(reductionSearch.group(1))) # Debug
            if reductionSearch.group(1) != '#':
               reduction += num(reductionSearch.group(1)) # if there is a match, the total reduction for this card's cost is increased.
            else: 
               while fullCost > 0 and c.markers[mdict['Bits']] > 0: 
                  reduction += 1
                  fullCost -= 1
                  c.markers[mdict['Bits']] -= 1
                  if fullCost == 0: break
   return reduction
   
def scrAgenda(card, x = 0, y = 0):
   global TypeCard, KeywordCard, scoredAgendas
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
      TypeCard[card] = card.Type
      KeywordCard[card] = getKeywords(card)
      agendaTxt = "liberate"
   else: agendaTxt = "score"
   if TypeCard[card] == "Agenda":
      if ds == 'corp' and card.markers[mdict['Advance']] < card.Stat:
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
      card.markers[mdict['Advance']] = 0
      card.markers[mdict['Not_rezzed']] = 0
      card.markers[mdict['Scored']] += 1
      me.counters['Agenda Points'].value += ap
      card.moveToTable(-600 - scoredAgendas * cwidth(card) / 6, 60 - yaxisMove(card) + scoredAgendas * cheight(card) / 2 * playerside, False)
      scoredAgendas += 1
      notify("{} {}s {} and receives {} agenda point(s)".format(me, agendaTxt, card, ap))
      if cheapAgenda: notify(":::Warning:::{} did not have enough advance tokens ({} out of {})! ".format(card,currentAdv,card.Cost))
      if me.counters['Agenda Points'].value >= 7 : notify("{} wins the game!".format(me))
      executeAutomations(card,agendaTxt)
   else:
      whisper ("You can't score this card")

def isRezzable (card):
	mute()
	Type = TypeCard[card]
	if Type == "Ice" or Type == "Node" or Type == "Upgrade": return True
	else: return False

def intRez (card, cost = 'not free', x=0, y=0, silent = False):
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
   reduction = reduceCost(card, 'Rez', num(CostCard[card]))
   if reduction: extraText = " (reduced by {})".format(uniBit(reduction))
   rc = payCost(num(CostCard[card]) - reduction, cost)
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
	intRez(card, "free")

def derez(card, x = 0, y = 0, silent = False):
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
   if not card.isFaceUp:
      mute()
      card.isFaceUp = True
      if not silent: notify("{} exposed {}".format(me, card))
   else:
      notify("This card is already exposed")
      return 'ABORT'

def rolld6(group = table, x = 0, y = 0, silent = False):
   mute()
   n = rnd(1, 6)
   if not silent: notify("{} rolls {} on a 6-sided die.".format(me, n))
   return n

def selectAsTarget (card, x = 0, y = 0):
    card.target(True)

def clear(card, x = 0, y = 0):
   notify("{} clears {}.".format(me, card))
   card.highlight = None
   card.markers[mdict['BaseLink']] = 0
   card.markers[mdict['PlusOne']] = 0
   card.markers[mdict['MinusOne']] = 0
   card.target(False)

def intTrashCard(card, stat, cost = "not free",  ActionCost = '', silent = False):
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
	intTrashCard(card, card.Stat)
        
def trashForFree (card, x = 0, y = 0):
	intTrashCard(card, card.Stat, "free")

def pay2AndTrash(card, x=0, y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   intTrashCard(card, 2, ActionCost = ActionCost)

def exileCard(card, silent = False):
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
   if card.highlight == None:
      card.highlight = SelectColor
      notify ( "{} uses the ability of {}.".format(me,card) )
   else:
      if card.highlight == DummyColor and not confirm("This highlight signifies that this card is technically trashed\nAre you sure you want to clear the card's highlight?"):
         return
      notify("{} clears {}.".format(me, card))
      card.highlight = None
      card.target(False)

def rulings(card, x = 0, y = 0):
  mute()
  if not card.isFaceUp: return
  openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))

def checkNotHardwareDeck (card):
   mute()
   if card.Type != "Hardware" or not re.search(r'Deck', getKeywords(card)): return True
   ExistingDecks = [ c for c in table
         if c.owner == me and c.isFaceUp and re.search(r'Deck', getKeywords(c)) ]
   if len(ExistingDecks) != 0 and not confirm("You already have at least one hardware deck in play. Are you sure you want to install {}?\n\n(If you do, your installed Decks will be automatically trashed at no cost)".format(card.name)): return False
   else: 
      for HWDeck in ExistingDecks: trashForFree(HWDeck)
   return True   

def checkUnique (card):
   mute()
   if not re.search(r'Unique', getKeywords(card)): return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and c.name == card.name and re.search(r'Unique', getKeywords(c)) ]
   if len(ExistingUniques) != 0 and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be trashed at no cost)".format(card.name)) : return False
   else:
      for uniqueC in ExistingUniques: trashForFree(uniqueC)
   return True   
   
def oncePerTurn(card, x = 0, y = 0, silent = False):
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
def intPlay(card, cost = 'not_free'):
   global TypeCard, CostCard, KeywordCard
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
   TypeCard[card] = card.Type
   KeywordCard[card] = getKeywords(card)
   CostCard[card] = card.Cost
   MUtext = ''
   rc = ''
   if card.Type == 'Resource' and re.search(r'Hidden', getKeywords(card)): hiddenresource = 'yes'
   else: hiddenresource = 'no'
   if card.Type == 'Ice' or card.Type == 'Agenda' or card.Type == 'Node' or (card.Type == 'Upgrade' and not re.search(r'Region', getKeywords(card))):
      card.moveToTable(-180, 160 * playerside - yaxisMove(card), True) # Agendas, Nodes and non-region Upgrades all are played to the same spot now.
      if TypeCard[card] == 'Ice': 
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
         notify("{} to install a card.".format(ActionCost))
         executeAutomations(card,'play')
         return
      reduction = reduceCost(card, 'Install', num(card.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
      if reduction: extraText = " (reduced by {})".format(uniBit(reduction)) #If it is, make sure to inform.
      rc = payCost(num(card.Cost) - reduction, cost)
      if rc == "ABORT": 
         me.Actions += NbReq # If the player didn't notice they didn't have enough bits, we give them back their action
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
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
      rc = payCost(card.Cost, cost)
      if rc == "ABORT": 
         me.Actions += NbReq # If the player didn't notice they didn't have enough bits, we give them back their action
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      if card.Type == 'Operation':
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to initiate {}{}.".format(ActionCost, rc, card, extraText))
      elif card.Type == 'Upgrade' and re.search(r'Region', getKeywords(card)):
         card.moveToTable(-220, 240 * playerside - yaxisMove(card), False)
         notify("{}{} to open a base of operations in {}{}.".format(ActionCost, rc, card, extraText))
      else:
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to play {}{}.".format(ActionCost, rc, card, extraText))           
   executeAutomations(card,'play')

def chkTargeting(card):
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

def playForFree(card, x = 0, y = 0):
	intPlay(card,"free")

def movetoTopOfStack(card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveTo(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to top of {}.".format(me,nameStack) )

def movetoBottomOfStack(card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveToBottom(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to Bottom of {}.".format(me,nameStack) )

def handtoArchives(card):
	if ds == "runner": return
	mute()
	card.moveTo(me.piles['Trash/Archives(Face-up)'])
	notify ("{} moves a card to their face-up Archives.".format(me))

def handDiscard(card):
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
    
def handRandomDiscard(group):
    mute()
    card = group.random()
    if card == None: return
    if ds == "corp" :
        card.moveTo(me.piles['Archives(Hidden)'])
        notify("{} discards a card at random.".format(me))
    else:
        card.moveTo(me.piles['Trash/Archives(Face-up)'])
        notify("{} discards {} at random.".format(me,card))
    		
def showatrandom(group):
	mute()
	card = group.random()
	if card == None: return
	card.moveToTable(0, 0 - yaxisMove(card), False)
	notify("{} show {} at random.".format(me,card))

def handtoStack (group, silent = False):
   mute()
   Stack = me.piles['R&D/Stack']
   handlength = len(me.hand)
   for c in me.hand: c.moveTo(Stack)
   if ds == "runner":
      nameHand = "Hand"
      nameStack = "Stack"
   else:
      nameHand = "HQ"
      nameStack = "R&D"
   if not silent: notify ("{} moves {} to {}.".format(me,nameHand,nameStack))
   else: return(nameHand,nameStack,handlength) # Return a tuple with the names of the groups.


#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------
def shuffle(group):
	group.shuffle()

def draw(group):
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
   mute()
   if not destination: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): c.moveTo(destination)
   if not silent: notify("{} draws {} cards.".format(me, count))
   return count

def toarchives(group = me.piles['Archives(Hidden)']):
	mute()
	Archives = me.piles['Archives(Hidden)']
	for c in group: c.moveTo(Archives)
	#Archives.shuffle()
	notify ("{} moves Hidden Archives to Archives.".format(me))

def archivestoStack(group, silent = False):
   mute()
   Stack = me.piles['R&D/Stack']
   for c in group: c.moveTo(Stack)
   #Archives.shuffle()
   if ( ds == "runner"):
      nameTrash = "Trash"
      nameStack = "Stack"
   else:
      nameTrash = "Archives"
      nameStack = "R&D"
   if not silent: notify ("{} moves {} to {}.".format(me,nameTrash,nameStack))
   else: return(nameTrash,nameStack)

def mill(group):
   if len(group) == 0: return
   mute()
   count = askInteger("Mill how many cards?", 1)
   if count == None: return
   if ( ds == "runner"):
      for c in group.top(count): c.moveTo(me.piles['Trash/Archives(Face-up)'])
      nameStack = "Stack"
      nameTrash = "Trash"
   else:
      for c in group.top(count): c.moveTo(me.piles['Archives(Hidden)'])
      nameStack = "HQ"
      nameTrash = "Archives H"
      notify("{} mills the top {} cards from {} to {}.".format(me, count,nameStack,nameTrash))

def moveXtopCardtoBottomStack(group):
   mute()
   if len(group) == 0: return
   count = askInteger("Move how many cards?", 1)
   if count == None: return
   for c in group.top(count): c.moveToBottom(group)
   if ds == "runner": nameStack = "Stack"
   else: nameStack = "R&D"
   notify("{} moves the top {} cards from {} to bottom of {}.".format(me, count,nameStack,nameStack))


def checkDeckNoLimit (group):
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
    if not Automations['Play, Score and Rez']: return
    if not card.isFaceUp: return
    AutoScript = card.AutoScript
    if AutoScript == "": return
    if re.search(r'(onRez|onPlay|onScore|whileRezzed|whileScored):', AutoScript): 
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
   X = 0
   Autoscripts = card.AutoScript.split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
   AutoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
   for autoS in AutoScriptsSnapshot: # Checking and removing any "AtTurnStart" actions.
      if re.search(r'atTurn(Start|End)', autoS) or re.search(r'-isTrigger', autoS): Autoscripts.remove(autoS)
      if re.search(r'CustomScript', autoS): 
         customScript(card,action)
         Autoscripts.remove(autoS)
   if len(Autoscripts) == 0: return
   announceText = "{}".format(me)
   for AutoS in Autoscripts:
      #confirm("Processing: {}".format(AutoS)) # Debug
      effectType = re.search(r'(onRez|onScore|onPlay|whileRezzed|whileScored):', AutoS)
      if ((effectType.group(1) == 'onRez' and action != 'rez') or
          (effectType.group(1) == 'onPlay' and action != 'play') or
          (effectType.group(1) == 'onScore' and action != 'score') or
          (effectType.group(1) == 'onTrash' and (action != 'trash' or action!= 'uninstall')) or
          (effectType.group(1) == 'onDerez' and action != 'derez')): continue # We don't want onPlay effects to activate onTrash for example.
      selectedAutoscripts = AutoS.split('$$')
      #confirm('selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for activeAutoscript in selectedAutoscripts:
         #confirm("Processing: {}".format(activeAutoscript)) # Debug
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         targetC = findTarget(activeAutoscript)
         #confirm("targetC: {}".format(targetC)) # Debug
         effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\| -]*)', activeAutoscript)
         #confirm('effects: {}'.format(effect.groups())) #Debug
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
            #confirm("passedscript: {}".format(passedScript)) # Debug
            if GainX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
         else: 
            passedScript = "{}".format(effect.group(0))
            #confirm("passedscript: {}".format(passedScript)) # Debug
            if effect.group(1) == 'Draw': 
               if DrawX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if re.search(r'(Put|Remove|Refill|Use|Infect)', effect.group(1)): 
               if TokensX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            if effect.group(1) == 'Roll': 
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if rollTuple == 'ABORT': return
               X = rollTuple[1] 
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
         
#------------------------------------------------------------------------------
# Autoactions
#------------------------------------------------------------------------------
#                                         a  b  c  d  e  f  g  h i j k l
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
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
   else: confirm("Card Text: {}\n\n{}".format(card.Rules,ASText))

def useAbility(card, x = 0, y = 0): # The start of autoscript activation.
   mute()
   if (card in TypeCard and TypeCard[card] == 'Tracing') or card.model == 'c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8': # If the player double clicks on the Tracing card...
      if card.isFaceUp and not card.markers[Bits]: inputTraceValue(card, limit = 0)
      elif card.isFaceUp and card.markers[Bits]: payTraceValue(card)
      elif not card.isFaceUp: revealTraceValue(card)
      return
   if not card.isFaceUp or card.markers[Not_rezzed]:
      if TypeCard[card] == 'Agenda': scrAgenda(card) # If the player double-clicks on an Agenda card, assume they wanted to Score it.
      else: intRez(card) # If card is face down or not rezzed assume they wanted to rez       
      return
   elif not Automations['Play, Score and Rez'] or card.AutoAction == "": 
      useCard(card) # If card is face up but has no autoscripts, or automation is disabled just notify that we're using an action.
      return
   elif re.search(r'CustomScript', card.AutoAction): 
      if chkTargeting(card) == 'ABORT': return
      customScript(card,'use') # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   ### Checking if card has multiple autoscript options and providing choice to player.
   Autoscripts = card.AutoAction.split('||')
   AutoScriptSnapshot = list(Autoscripts)
   for autoS in AutoScriptSnapshot: # Checking and removing any actionscripts which were put here in error.
      if re.search(r'while(Rezzed|Scored)', autoS) or re.search(r'on(Play|Score|Install)', autoS) or re.search(r'AtTurn(Start|End)', autoS): Autoscripts.remove(autoS)
   if len(Autoscripts) == 0:
      useCard(card) # If the card had only "WhileInstalled"  or AtTurnStart effect, just announce that it is being used.
      return      
   if len(Autoscripts) > 1: 
      abilConcat = "This card has multiple abilities.\nWhich one would you like to use?\n\n" # We start a concat which we use in our confirm window.
      for idx in range(len(Autoscripts)): # If a card has multiple abilities, we go through each of them to create a nicely written option for the player.
         #notify("Autoscripts {}".format(Autoscripts)) # Debug
         abilRegex = re.search(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):([A-Z][a-z ]+)([0-9]*)([A-Za-z ]*)-?([A-Za-z -{},]*)", Autoscripts[idx]) # This regexp returns 3-4 groups, which we then reformat and put in the confirm dialogue in a better readable format.
         #confirm("abilRegex is {}".format(abilRegex.groups())) # Debug
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
         if abilRegex.group(8): # If the autoscript has a fourth group, then it means it has subconditions. Such as "per Holding" or "by Rival"
            subconditions = abilRegex.group(8).split('$$') # These subconditions are always separated by dashes "-", so we use them to split the string
            for idx2 in range(len(subconditions)):
               if idx2 > 0: abilConcat += ' and'
               subadditions = subconditions[idx2].split('-')
               for idx3 in range(len(subadditions)):
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
            else: announceText += 'activates the once-per-turn ability of {}'.format(card)
         else: announceText += ' to activate {}'.format(card) # If we don't have to trash the card, we need to still announce the name of the card we're using.
         if actionCost.group(1) == '0' and actionCost.group(2) == '0' and actionCost.group(3) == '0' and actionCost.group(4) == '0':
            announceText = '{} activates the free ability of {}'.format(me, card)
         announceText += ' in order to'
      elif not announceText.endswith(' in order to') and not announceText.endswith(' and'): announceText += ' and'
      #confirm("Bump: {}".format(activeAutoscript)) # Debug
      ### Calling the relevant function depending on if we're increasing our own counters, the hoard's or putting card markers.
      if re.search(r'\b(Gain|Lose|SetTo)([0-9]+)', activeAutoscript): announceText = GainX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bReshuffle([A-Za-z& ]+)', activeAutoscript): 
         reshuffleTuple = ReshuffleX(activeAutoscript, announceText, card) # The reshuffleX() function is special because it returns a tuple.
         announceText = reshuffleTuple[0] # The first element of the tuple contains the announceText string
         X = reshuffleTuple[1] # The second element of the tuple contains the number of cards that were reshuffled from the hand in the deck.
      elif re.search(r'Roll([0-9]+)', activeAutoscript): 
         rollTuple = RollX(activeAutoscript, announceText, card) # Returns like reshuffleX()
         announceText = rollTuple[0] 
         X = rollTuple[1] 
      elif re.search(r'\b(Put|Remove|Refill|Use|Infect)([0-9]+)', activeAutoscript): announceText = TokensX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bTransfer([0-9]+)', activeAutoscript): announceText = TransferX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bDraw([0-9]+)', activeAutoscript): announceText = DrawX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bShuffle([A-Za-z& ]+)', activeAutoscript): announceText = ShuffleX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bRun([A-Za-z& ]+)', activeAutoscript): announceText = RunX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bTrace([0-9]+)', activeAutoscript): announceText = TraceX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bInflict([0-9]+)', activeAutoscript): announceText = InflictX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)', activeAutoscript): announceText = ModifyStatus(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bSimplyAnnounce', activeAutoscript): announceText = SimplyAnnounce(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bCreateDummy', activeAutoscript): announceText = CreateDummy(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bChooseKeyword', activeAutoscript): announceText = ChooseKeyword(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bUseCustomAbility', activeAutoscript): announceText = UseCustomAbility(activeAutoscript, announceText, card, targetC, n = X)
      else: timesNothingDone += 1
      if announceText == 'ABORT': 
         autoscriptCostUndo(card, selectedAutoscripts[0]) # If nothing was done, try to undo. The first item in selectedAutoscripts[] contains the cost.
         return
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
   whisper("--> Undoing action...")
   actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", Autoscript)
   me.Actions += num(actionCost.group(1))
   me.counters['Bit Pool'].value += num(actionCost.group(2))
   me.counters['Agenda Points'].value += num(actionCost.group(3))
   if re.search(r"T2:", Autoscript):
      random = rnd(10,5000) # A little wait...
      card.orientation = Rot0

def findTarget(Autoscript): # Function for finding the target of an autoscript
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
   #for foundTarget in foundTargets: notify('found target: {}'.format(foundTarget)) # Debug
   return foundTargets
   
def chkWarn(card, Autoscript): # Function for checking that an autoscript announces a warning to the player
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

def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for modifying counters or global variables
   if targetCards is None: targetCards = []
   global maxActions
   #confirm("Bump GainX") #Debug
   gain = 0
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   #confirm("Bump1: {}".format(action.groups(0))) # Debug
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0:
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   if action.group(1) == 'Lose': gain *= -1
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if re.match(r'Bit', action.group(3)): # Note to self: I can probably comprress the following, by using variables and by putting the counter object into a variable as well.
      if action.group(1) == 'SetTo': targetPL.counters['Bit Pool'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bit Pool'].value = 0
      else: targetPL.counters['Bit Pool'].value += gain * multiplier
      if targetPL.counters['Bit Pool'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bit Pool'].value = 0
   elif re.match(r'Agenda Point', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Agenda Points'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Agenda Points'].value = 0
      else: targetPL.counters['Agenda Points'].value += gain * multiplier
      if targetPL.counters['Agenda Points'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Agenda Points'].value = 0
   elif re.match(r'Action', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Actions = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Actions = 0
      else: targetPL.Actions += gain * multiplier
   elif re.match(r'MU', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Memory = 0 # If we're setting to a specific value, we wipe what it's currently.
      else: targetPL.Memory += gain * multiplier
      if targetPL.Memory < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.Memory = 0
   elif re.match(r'Bad Publicity', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Bad Publicity'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bad Publicity'].value = 0
      else: targetPL.counters['Bad Publicity'].value += gain * multiplier
      if targetPL.counters['Bad Publicity'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bad Publicity'].value = 0
   elif re.match(r'Tag', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Tags = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Tags = 0
      else: targetPL.Tags += gain * multiplier
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
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   else: total = abs(gain * multiplier) # Else it's just the absolute value which we announce they "gain" or "lose"
   if notification == 'Quick': announceString = "{} {}s {} {}".format(announceText, action.group(1).lower(), total, action.group(3))
   else: announceString = "{}{} {} {} {}".format(announceText, otherTXT, action.group(1).lower(), total, action.group(3))
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   return announceString

def TransferX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for converting tokens to counter values
   if targetCards is None: targetCards = []
   breakadd = 1
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   action = re.search(r'\bTransfer([0-9]+)Bits?-to(Bit Pool|Discard)', Autoscript)
   for targetCard in targetCards:
      if action.group(1) == '999':
         if targetCard.markers[Bits]: count = targetCard.markers[Bits]
         else: count = 0
      else: count = num(action.group(1))
      if targetCard.markers[Bits] < count: 
         if re.search(r'isCost', Autoscript):
            whisper("You must have at least {} Bits on the card to take this action".format(action.group(1)))
            return 'ABORT'
         elif targetCard.markers[Bits] == 0 and not notification: 
            whisper("There was nothing to transfer.")
            return 'ABORT'
         elif targetCard.markers[Bits] == 0 and notification: return 'ABORT'
      for transfer in range(count):
         if targetCard.markers[Bits] > 0: 
            targetCard.markers[Bits] -= 1
            if action.group(2) == 'Bit Pool': 
               card.owner.counters['Bit Pool'].value += 1
               destination = "{}'s bit pool".format(card.owner)
            elif action.group(2) == 'Discard': destination = "the Discard Pile" # If the tokens are discarded, do nothing more.
         else: 
            breakadd -= 1 # We decrease the transfer variable by one, to make sure we announce the correct total.
            break # If there's no more tokens to transfer, break out of the loop.
   if notification == 'Quick': announceString = "{} takes {} bits".format(announceText, transfer + breakadd)
   else: announceString = "{} transfer {} bits from {} to {}".format(announceText, transfer + breakadd, targetCardlist, destination)
   if notification: notify('--> {}.'.format(announceString))
   return announceString   

def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for adding tokens to cards
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
   #confirm("Bumpa") # Debug
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
         if token != mdict['protectionVirus']: # We don't want us to prevent putting virus protection tokens, even though we put them with the "Infect" keyword.
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
   else: announceString = "{} {}{} {} {} counters{}{}".format(announceText, action.group(1).lower(),infectTXT, total, token[0],targetCardlist,preventTXT)
   if notification == 'Automatic' and modtokens != 0: notify('--> {}.'.format(announceString))
   return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for drawing X Cards from the house deck to your hand.
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
   else: destination = targetPL.hand
   if destiVerb == 'draw' and ModifyDraw and not confirm("You have a card effect in play that modifies the amount of cards you draw. Have you already looked at the relevant cards on the top of your deck before taking this action?\n\n(Answering 'No' will abort this action so that you can first check your deck"): return 'ABORT'
   draw = num(action.group(1))
   if draw == 999:
      multiplier = 1
      count = drawMany(source, currentHandSize(targetPL) - len(targetPL.hand), destination, True) # 999 means we refresh our hand
      #confirm("cards drawn: {}".format(count)) # Debug
   else: # Any other number just draws as many cards.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = drawMany(source, draw * multiplier, destination, True)
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} draws {} cards".format(announceText, count)
   elif targetPL == me: announceString = "{} {} {} cards from their {} to their {}".format(announceText, destiVerb, count, source.name, destination.name)
   else: announceString = "{} {} {} cards from {}'s {} to {}'s {}".format(announceText, destiVerb, count, targetPL, source.name, targetPL, destination.name)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   return announceString

def ofwhom(Autoscript):
   if re.search(r'o[fn]Opponent', Autoscript):
      if len(players) > 1:
         for player in players:
            if player != me and player.getGlobalVariable('ds') != ds: 
               targetPL = player # Opponent needs to be not us, and of a different type. 
                                 # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
      else : 
         whisper("There's no Opponents! Selecting myself.")
         targetPL = me
   else: targetPL = me
   return targetPL
   
def ReshuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Function for reshuffling a pile into the R&D/Stack
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
   return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Function for reshuffling a pile into the R&D/Stack
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
   return announceString
   
def RollX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for drawing X Cards from the house deck to your hand.
   if targetCards is None: targetCards = []
   action = re.search(r'\bRoll([0-9]+)Dice', Autoscript)
   count = num(action.group(1))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   d6 = rolld6(silent = True) # For now we always roll 1d6. If we ever have a autoaction which needs more then 1, I'll implement it.
   if notification == 'Quick': announceString = "{} rolls {} on a die".format(announceText, d6)
   else: announceString = "{} roll {} on a die".format(announceText, d6)
   if notification: notify('--> {}.'.format(announceString))
   return (announceString, d6)
   
def RunX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for drawing X Cards from the house deck to your hand.
   if targetCards is None: targetCards = []
   action = re.search(r'\bRun([A-Z][A-Za-z& ]+)', Autoscript)
   if action.group(1) == 'Generic': runTarget = ''
   else: runTarget = ' on {}'.format(action.group(1))
   if notification == 'Quick': announceString = "{} starts a run{}".format(announceText, runTarget)
   else: announceString = "{} start a run{}".format(announceText, runTarget)
   if notification: notify('--> {}.'.format(announceString))
   return announceString

def SimplyAnnounce(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for drawing X Cards from the house deck to your hand.
   if targetCards is None: targetCards = []
   action = re.search(r'\bSimplyAnnounce{([A-Za-z&,\. ]+)}', Autoscript)
   if notification == 'Quick': announceString = "{} {}".format(announceText, action.group(1))
   else: announceString = "{} {}".format(announceText, action.group(1))
   if notification: notify('--> {}.'.format(announceString))
   return announceString

def CreateDummy(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for creating dummy cards.
   if targetCards is None: targetCards = []
   global Dummywarn
   action = re.search(r'\bCreateDummy(-with)?([A-Za-z0-9_]*)', Autoscript)
   #confirm('actions: {}'.format(action.groups())) # debug
   if Dummywarn and not confirm("This card's effect requires that you trash it, but its lingering effects will only work automatically while a copy is in play.\
                               \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                             \n\nSome cards provide you with an ability that you can activate after they're been trashed. If this card has one, you can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                             \n\nDo you want to see this warning again?"): Dummywarn = False
   dummyCard = table.create(card.model, 500, 50 * playerside, 1) # This will create a fake card like the one we just created.
   dummyCard.highlight = DummyColor
   #confirm("Dummy ID: {}\n\nList Dummy ID: {}".format(dummyCard._id,passedlist[0]._id)) #Debug   
   card.moveTo(card.owner.piles['Trash/Archives(Face-up)'])
   if action.group(1): announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   return announceString # Creating a dummy isn't announced.

def ChooseKeyword(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for marking cards to be of a different keyword than they are
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
   for i in range(len(keywords)): choiceTXT += '{}: {}\n'.format(i, keywords[i])
   choice = len(keywords)
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
      if re.search(r'{}'.format(keywords[choice]),getKeywords(targetCard)):
         if existingKeyword: targetCard.markers[existingKeyword] = 0
         else: pass # If the keyword is anyway the same, and it had no previous keyword, there is nothing to do
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
   return announceString
            
def TraceX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for drawing X Cards from the house deck to your hand.
   if targetCards is None: targetCards = []
   action = re.search(r'\bTrace([0-9]+)', Autoscript)
   inputTraceValue(card, limit = num(action.group(1)))
   if action.group(1) != '0': limitText = ' (max power: {})'.format(action.group(1))
   else: limitText = ''
   if notification == 'Quick': announceString = "{} starts a trace{}".format(announceText, limitText)
   else: announceString = "{} start a trace{}".format(announceText, limitText)
   if notification: notify('--> {}.'.format(announceString))
   return announceString

def ModifyStatus(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for modifying the status of a card on the table.
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
      if action.group(1) == 'Rez' and intRez(targetCard, silent = True) != 'ABORT': pass
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
   return announceString
         
def InflictX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Function for inflicting Damage to players (even ourselves)
   if targetCards is None: targetCards = []
   global DMGwarn 
   localDMGwarn = True #A variable to check if we've already warned the player during this damage dealing.
   action = re.search(r'\b(Inflict)([0-9]+)(Meat|Net|Brain)Damage', Autoscript) # Find out what kind of damage we're going
   multiplier = per(Autoscript, card, n, targetCards)
   enhancer = findEnhancements(Autoscript) #See if any of our cards increases damage we deal
   if enhancer > 0: enhanceTXT = ' (Enhanced: +{})'.format(enhancer) #Also notify that this is the case
   else: enhanceTXT = ''
   targetPL = ofwhom(Autoscript) #Find out who the target is
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0: #See if the target needs to be tagged.
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   elif re.search(r'ifTagged2', Autoscript) and targetPL.Tags < 2: #See if the target needs to be double tagged.
      whisper("Your opponent needs to be tagged twice to use this action")
      return 'ABORT'
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
   if notification == 'Quick': announceString = "{} suffers {} {} damage".format(announceText,DMG,action.group(3))
   else: announceString = "{} inflict {} {} damage{} to {}{}".format(announceText,DMG,action.group(3),enhanceTXT,targetPL,preventTXT)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   return announceString

def findDMGProtection(DMGdone, DMGtype, targetPL): # Find out if the player has any card preventing damage
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
   return protectionFound

def findEnhancements(Autoscript): #Find out if the player has any cards increasing damage dealt.
   enhancer = 0
   DMGtype = re.search(r'\bInflict[0-9]+(Meat|Net|Brain)Damage', Autoscript)
   if DMGtype:
      for card in table:
         cardENH = re.search(r'Enhance([0-9]+){}Damage'.format(DMGtype.group(1)), card.AutoScript)
         if card.controller == me and not card.markers[Not_rezzed] and cardENH: enhancer += num(cardENH.group(1))
   return enhancer

def findVirusProtection(card, targetPL, VirusInfected): # Find out if the player has any virus preventing counters.
   protectionFound = 0
   if card.markers[mdict['protectionVirus']]:
      while VirusInfected > 0 and card.markers[mdict['protectionVirus']] > 0: # For each virus infected...
         protectionFound += 1 # We increase the protection found by 1
         VirusInfected -= 1 # We reduce how much viruses we still need to prevent by 1
         card.markers[mdict['protectionVirus']] -= 1 # We reduce the card's virus protection counters by 1
   return protectionFound
   
def per(Autoscript, card = None, count = 0, targetCards = None, notification = None): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   #confirm("Bump per") #Debug
   if targetCards is None: targetCards = []
   per = re.search(r'\b(per|upto)(Target|Parent|Every)?([A-Z][A-Za-z0-9{}_ ]*)-?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable.   
   if per: # If the  search was successful...
      #confirm("Groups: {}. Count: {}".format(per.groups(),count)) #Debug
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
         #notify('Matches: {}\nExclusions: {}'.format(perItemMatch, perItemExclusion)) # Debug
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
            #notify("Starting check with {}.\nProperties: {}".format(c, cardProperties)) # Debug
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
               #notify("Found: {}".format(c)) # Debug
               if re.search(r'isExposeTarget', Autoscript) and not c.isFaceUp and c.targetedBy == me: expose(c) # If the card is supposed to be exposed to get the benefit, then do so now.
               if re.search(r'(Reveal&Shuffle|Reveal&Recover)', Autoscript) and c.targetedBy and c.targetedBy == me: 
                  c.moveToTable((70 * iter) - 150, 0 - yaxisMove(card), False) # If the card is supposed to be revealed to get the benefit, then we do so now
                  c.highlight = RevealedColor
                  notify("- {} reveals {} from their hand".format(me,c))
                  iter +=1
               if re.search(r'SendToTrash', Autoscript) and c.targetedBy and c.targetedBy == me: handDiscard(c)
               if re.search(r'Marker',per.group(3)): #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
                  marker = re.search(r'Marker{([\w ]+)}',per.group(3)) # If we're looking for markers on the card, increase the multiplier by the number of markers found.
                  multiplier += c.markers[mdict[marker.group(1)]]
               elif re.search(r'Property',per.group(3)): # If we're looking for a specific property on the card, increase the multiplier by the total of the properties on the cards found.
                  property = re.search(r'Property{([\w ]+)}',per.group(3))
                  multiplier += num(c.properties[property.group(1)]) # Don't forget to turn it into an integer first!
               else: multiplier += 1 * chkPlayer(Autoscript, c.controller, False) # If the perCHK remains 1 after the above loop, means that the card matches all our requirements. We only check faceup cards so that we don't take into acoount peeked face-down ones.
                                                                                  # We also multiply it with chkPlayer() which will return 0 if the player is not of the correct allegiance (i.e. Rival, or Me)
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
         #confirm("No table lookup done") # Debug.
         if per.group(3) == 'X': multiplier = count      
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
         elif re.search(r'Marker',per.group(3)):
            marker = re.search(r'Marker{([\w ]+)}',per.group(3))
            multiplier = card.markers[mdict[marker.group(1)]]
         elif re.search(r'Property',per.group(3)):
            property = re.search(r'Property{([\w ]+)}',per.group(3))
            multiplier = card.properties[property.group(1)]
   else: multiplier = 1
   return multiplier

def chkPlayer(Autoscript, controller, manual): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   byOpponent = re.search(r'byOpponent', Autoscript)
   byMe = re.search(r'byMe', Autoscript)
   if manual: return 1 #manual means that the actions was called by a player double clicking on the card. In which case we always do it.
   elif not byOpponent and not byMe: return 1 # If the card has no restrictions on being us or a rival.
   elif byOpponent and controller != me: return 1 # If the card needs to be played by a rival.
   elif byMe and controller == me: return 1 # If the card needs to be played by us.
   else: return 0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 which will make the multiplier 0.
   
def autoscriptOtherPlayers(lookup, count = 1): # Function that triggers effects based on the opponent's cards.
# This function is called from other functions in order to go through the table and see if other players have any cards which would be activated by it.
# For example a card that would produce bits whenever a trace was attempted. 
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
            effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_& -]*)', AutoS)
            passedScript = "{}".format(effect.group(0))
            #confirm('effects: {}'.format(passedScript)) #Debug
            if effect.group(1) == 'Gain' or effect.group(1) == 'Lose':
               GainX(passedScript, costText, card, notification = 'Automatic', n = count) # If it exists, then call the GainX() function, because cards that automatically do something when other players do something else, always give the player something directly.
            if re.search(r'(Put|Remove|Refill|Use|Infect)', effect.group(1)): 
               TokensX(passedScript, costText, card, notification = 'Automatic', n = count)
   
def customScript(card, action = 'play'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
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
         if c.controller == me and c in TypeCard and TypeCard[c] == 'Ice' and c.markers[Not_rezzed]:
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
         notify("{} has won the corporate war and their spoils are 12 Bits".format(me))
         me.counters['Bit Pool'].value += 12
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
      else:
         iter = 0
         for c in group.top(5):
            c.moveToTable((70 * iter) - 150, 0 - yaxisMove(card), False)
            c.highlight = RevealedColor
            if c.type != 'Program': c.moveToBottom(group)
            else: iter +=1
         if iter > 1: # If we found any programs in the top 5
            notify("{} activates the Mystery Box and reveals {} Programs from the top of their Stack. They now have to select one to bring into play at no cost".format(me, iter))
            confirm("The cards with the white highlight on the table are the programs that existed within the top 5 cards of your Stack\
                   \nPlease Target one of them (shift + click) and then double click on the Mystery Box again to complete this action")
         elif iter == 1: customScript(card,'use') # Recursion FTW!
         else: notify("{} activates the Mystery Box but it fizzles out.".format(me))
   elif action == 'use': useCard(card)
   
def TrialError(group, x=0, y=0): # Debugging
   global TypeCard, CostCard, ds, KeywordCard
   testcards = ["185ef5c7-5fb5-4b57-b67a-8d1dc311a0b9", # Bel-Digmo Antibody
                "692b1e14-e381-40f6-beb0-ba55b9bbd3e5", # Bug Zapper
                "5045ca08-46b8-456f-88cd-9ce3acf49f22", # Hacker Tracker Central
                "c48c91d0-8253-42b3-9c69-918a464445e0", # Encryption breakthrough
                "2cd201db-a2fe-49d0-b5e1-14197b88172e", # Corp. negotiation centre.
                "3db0bf1a-f262-4fcd-a3e7-1993f90dffc7", # Caryatid
                "23b7487c-7093-47ae-a6e9-d3911ad58c5a", # Corporate War
                "92725a30-5f2a-439e-a5e1-4c818780ed1c"] # Mystery Box
   if not ds: ds = "corp"
   me.setGlobalVariable('ds', ds) 
   me.counters['Bit Pool'].value = 50
   me.counters['Max Hand Size'].value = 5
   me.counters['Tags'].value = 1
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 10
   me.Actions = 15
   for idx in range(len(testcards)):
      test = table.create(testcards[idx], (70 * idx) - 150, 0, 1, True)
      TypeCard[test] = test.Type
      KeywordCard[test] = getKeywords(test)
      CostCard[test] = test.Cost
      #random = rnd(10,500)
      if test.Type == 'Ice' or test.Type == 'Agenda' or test.Type == 'Node':
         test.isFaceUp = False
         test.markers[Not_rezzed] += 1
   
def atTurnStartEndEffects(Time = 'Start'): # Function which triggers card effects at the start or end of the turn.
   if not Automations['Start/End-of-Turn']: return
   TitleDone = False
   for card in table:
      Autoscripts = card.AutoScript.split('||')
      for AutoScript in Autoscripts:
         effect = re.search(r'atTurn(Start|End):([A-Z][A-Za-z]+)([0-9]+)([A-Za-z0-9 ]+)(.*)', AutoScript)
         if card.owner != me or not effect: continue
         if effect.group(1) != Time: continue # If it's a start-of-turn effect and we're at the end, or vice-versa, do nothing.
         if effect.group(5) and re.search(r'isOptional', effect.group(5)) and not confirm("{} can have the following optional ability activated at the start of your turn:\n\n[ {} {} {} ]\n\nDo you want to activate it?".format(card.name, effect.group(2), effect.group(3),effect.group(4))): continue
         if not TitleDone: notify(":::{}'s {}-of-Turn Effects:::".format(me,effect.group(1)))
         TitleDone = True
         effectNR = num(effect.group(3))
         passedScript = '{}'.format(effect.group(0))
         announceText = "{}:".format(card)
         if effect.group(2) == 'Gain' or effect.group(2) == 'Lose':
            GainX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Transfer':
            TransferX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Draw':
            DrawX(passedScript, announceText, card, notification = 'Automatic')
         if effect.group(2) == 'Refill':
            TokensX(passedScript, announceText, card, notification = 'Automatic')
   if me.counters['Bit Pool'].value < 0: 
      notify(":::Warning::: {}'s {}-of-turn effects cost more Bits than they had in their Bit Pool!".format(me,effect.group(1)))
   if ds == 'corp' and Time =='Start': draw(me.piles['R&D/Stack'])
   if TitleDone: notify(":::--------------------------:::".format(me))
