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
             virusButcherBoy = ("Boardwalk","5831fb18-7cdf-44d2-8685-bdd392bb9f1c"),
             virusCascade = ("Cascade","723a0cca-7a05-46a8-a681-6e06666042ee"),
             virusCockroach = ("Cockroach","cda4cfcb-6f2d-4a7f-acaf-d796b8d1edee"),
             virusGremlin = ("Gremlin","032d2efa-e722-4218-ba2b-699dc80f0b94"),
             virusThought = ("Thought","811b9153-93cb-4898-ad9f-68864452b9f4"),
             virusFait = ("Fait","72c89567-72aa-446d-a9ea-e158c22c113a"),
             virusBoardwalk = ("Boardwalk","8c48db01-4f12-4653-a31a-3d22e9f5b6e9"))
         
#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------
ds = ""
Automation = False # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
                   # Starts False and is switched on automatically at Jack In
StartAutomation = False # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
UniBits = True # If True, game will display bits as unicode characters ❶, ❷, ❿ etc

ModifyDraw = False #if True the audraw should warn the player to look at r&D instead 
TraceValue = 0

DifficultyLevels = { }

TypeCard = {}
CostCard = {}

MemoryRequirements = { }
InstallationCosts = { }
maxActions = 3
scoredAgendas = 0
playerside = None # Variable to keep track on which side each player is
playeraxis = None # Variable to keep track on which axis the player is

#---------------------------------------------------------------------------
# Constants
#---------------------------------------------------------------------------
import re

turns = [
	'Start of Game',
	"It is now Corporation's Turn",
	"It is now Runner's Turn",
	"It is now End of Turn"]

ScoredColor = "#00ff44"
SelectColor = "#009900"
MakeRunColor = "#ff0000"

newturn = True #We use this variable to track whether a player has yet to do anything this turn.
endofturn = False #We use this variable to know if the player is in the end-of-turn phase.

silent = 'silent'
loud = 'loud'
Xaxis = 'x'  # Same as above
Yaxis = 'y'	 # Same as above
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
    if len(me.hand) > me.counters['Max Hand Size'].value: #If the player is holding more cards than their hand max. remind them that they need to discard some 
                                                       # and put them in the end of turn to allow them to do so.
        if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
            if not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
            else: notify(":::Warning::: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),me.counters['Max Hand Size'].value))
        else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
            if ds == "corp": notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
            else: notify ("Runner {} is rebooting all systems for the day.".format(me))
            whisper(':::Warning::: You have more card in your hand than your current hand size maximum. Please discard enough and then use the "Declare End of Turn" action again.')
            endofturn = True
            return
    if ds == "corp": notify ("The Corporation of {} has reached CoB (Close of Business hours).".format(me))
    else: notify ("Runner {} has gone to sleep for the day.".format(me))
    endofturn = False
    newturn = False

def goToSot (group, x=0,y=0):
    global newturn, endofturn
    mute()
    if endofturn:
        if not confirm("You have not yet properly ended you previous turn. Are you sure you want to continue?"): return
        else: 
            if len(me.hand) > me.counters['Max Hand Size'].value: # Just made sure to notify of any shenanigans
                notify(":::Warning::: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),me.counters['Max Hand Size'].value))
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
    for card in myCards: card.orientation &= ~Rot90 # Refresh all cards which can be used once a turn.
    atTurnStartEffects() # Check all our cards to see if there's any Start of Turn effects active.
    if ds == "corp": notify("The offices of {}'s Corporation are now open for business.".format(me))
    else: notify ("Runner {} has woken up".format(me))
    newturn = True

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

def switchAutomation(group,x=0,y=0,command = 'Off'):
    global Automation
    if Automation and command != 'On':
        notify ("{}'s automations are OFF.".format(me))
        Automation = False
    else:
        notify ("{}'s automations are ON.".format(me))
        Automation = True

def switchStartAutomation(group,x=0,y=0,command = 'Off'):
    global StartAutomation
    if StartAutomation and command != 'On':
        notify ("{}'s Start-of-Turn automations are OFF.".format(me))
        StartAutomation = False
    else:
        notify ("{}'s Start-of-Turn automations are ON.".format(me))
        StartAutomation = True

def switchUniBits(group,x=0,y=0,command = 'Off'):
    global UniBits
    if UniBits and command != 'On':
        whisper("Bits and Actions will now be displayed as normal ASCII.".format(me))
        UniBits = False
    else:
        whisper("Bits and Actions will now be displayed as Unicode.".format(me))
        UniBits = True
        
def create3DataForts(group):
   table.create("2a0b57ca-1714-4a70-88d7-25fdf795486f", 150, 160 * playerside, 1)
   table.create("181de100-c255-464f-a4ed-4ac8cd728c61", 300, 160 * playerside, 1)
   table.create("59665835-0b0c-4710-99f7-8b90377c35b7", 450, 160 * playerside, 1)
   table.create("feaadfe5-63fc-443e-b829-b9f63c346d11", 0, 250 * playerside, 1) # The Antivirus card.

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
    me.setGlobalVariable(ds, ds)
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
        create3DataForts(group)
        notify("{} is playing as Corporation".format(me))      
    else:
        maxActions = 4
        me.Actions = maxActions
        me.Memory = 4
        NameDeck = "Stack"
        notify("{} is playing as Runner".format(me))
    table.create("c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8", 0, 155 * playerside, 1 ) #trace card
    switchAutomation(group,x,y,'On')
    switchStartAutomation(group,x,y,'On')
    shuffle(me.piles['R&D/Stack'])
    notify ("{}'s {} is shuffled ".format(me,NameDeck) )
    drawMany (me.piles['R&D/Stack'], 5) 

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
    if ds != "runner":
        whisper("Only runners can use this action")
        return
    if me.Tags < 1: 
        whisper("You don't have any tags")
        return
    ActionCost = useAction()
    if ActionCost == 'ABORT': return
    if payCost(2) == "ABORT": 
        me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
        return # If the player didn't have enough money to pay and aborted the function, then do nothing.
    me.counters['Tags'].value -= 1
    notify ("{} and pays {} to loose a tag.".format(ActionCost,uniBit(2)))

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
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   if payCost(1) == "ABORT": 
      me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   card.markers[Advance] += 1
   if card.isFaceUp: notify("{} and paid {} to advance {}.".format(ActionCost,uniBit(1),card))
   else: notify("{} and paid {} to advance a card.".format(ActionCost,uniBit(1)))

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

def inputTraceValue (card, x=0,y=0):
   mute()
   global TraceValue
   if card.properties['Type'] != "Tracing": return
   TraceValue = askInteger("Bet How Many?", 0)
   if TraceValue == None: 
      whisper(":::Warning::: Trace bid aborted by player.")
      return
   card.markers[Bits] = 0
   card.isFaceUp = False
   notify ("{} chose a Trace Value.".format(me))
   TypeCard[card] = "Tracing"
	
def revealTraceValue (card, x=0,y=0):
    mute()
    global TraceValue
    if ( TypeCard[card] <> "Tracing"): return
    mute()
    card.isFaceUp = True
    card.markers[Bits] = TraceValue
    notify ( "{} reveals a Trace Value of {}.".format(me,TraceValue))
    TraceValue = 0

def payTraceValue (card, x=0,y=0):
	if (card.properties['Type'] <> "Tracing"): return
	mute()
	me.counters['Bit Pool'].value -= card.markers[Bits]
	notify ("{} pays {} for the Trace Value.".format(me,uniBit(card.markers[Bits])))
	card.markers[Bits] = 0

def cancelTrace ( card, x=0,y=0):
    mute()
    card.isFaceUp = True
    TraceValue = 0
    card.markers[Bits] = 0
    notify ("{} cancels the Trace Value.".format(me) )

#------------------------------------------------------------------------------
# Other functions
#-----------------------------------------------------------------------------

def intdamageDiscard(group,x=0,y=0):
    mute()
    if len(group) == 0:
        notify ("{} cannot discard at random.".format(me))
    else:
        card = group.random()
        if ds == 'corp': card.moveTo(me.piles['Archives(Hidden)'])
        else: card.moveTo(me.piles['Trash/Archives(Face-up)'])
        notify("{} discards {} at random.".format(me,card))

def addBrainDmg(group, x = 0, y = 0):
    me.counters['Max Hand Size'].value -=1
    notify ("{} suffers 1 Brain Damage.".format(me) )
    intdamageDiscard(me.hand)


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
   if count == 0 : return 0# If the card has 0 cost, there's nothing to do.
   if counter == 'BP':
      if me.counters['Bit Pool'].value < count and not confirm("You do not seem to have enough Bits in your pool to take this action. Are you sure you want to proceed? \
         \n(If you do, your Bit Pool will go to the negative. You will need to increase it manually as required.)"): return 'ABORT' # If we don't have enough Bits in the pool, we assume card effects or mistake and notify the player that they need to do things manually.
      me.counters['Bit Pool'].value -= count
   elif counter == 'AP': # We can also take costs from other counters with this action.
      if me.counters['Agenda Points'].value < count and not confirm("You do not seem to have enough Agenda Points to take this action. Are you sure you want to proceed? \
         \n(If you do, your Agenda Points will go to the negative. You will need to increase them manually as required.)"): return 'ABORT'
      me.counters['Agenda Points'].value -= count
   return uniBit(count)
   
def scrAgenda(card, x = 0, y = 0):
    #if DifficultyLevels[card] >= 1:
    global TypeCard, scoredAgendas
    mute()
    if card.markers[Scored] > 0: 
        notify ("This agenda has already been scored")
        return
    if ds == 'runner' and card.Type != "Agenda" and not card.isFaceUp:
        card.isFaceUp = True
        random = rnd(100,1000) # Hack Workaround
        if card.Type != "Agenda":
            whisper ("You can only score Agendas")
            card.isFaceUp = False
            return
    if ds == 'runner': TypeCard[card] = card.Type
    if TypeCard[card] == "Agenda":
        if confirm("Do you want to score this agenda?") == True:
            card.isFaceUp = True
            ap = num(card.Stat)
            card.markers[Advance] = 0
            card.markers[Not_rezzed] = 0
            card.markers[Scored] += 1
            me.counters['Agenda Points'].value += ap
            card.moveToTable(-600 - scoredAgendas * cwidth(card) / 6, 60 - yaxisMove(card) + scoredAgendas * cheight(card) / 2 * playerside, False)
            scoredAgendas += 1
            if ds == "runner": agendaTxt = "liberates"
            else: agendaTxt = "scores"
            notify("{} {} {} and receives {} agenda point(s)".format(me, agendaTxt, card, ap))
            if me.counters['Agenda Points'].value >= 7 : notify("{} wins the game!".format(me))
            else: executeAutomations (card,agendaTxt)
    else:
        whisper ("You can't score this card")

def isRezzable (card):
	mute()
	Type = TypeCard[card]
	
	if ( Type == "Ice" or Type == "Node" or Type == "Upgrade"): return 0
	else: return -1

def intRez (card,cost = 'not free', x=0, y=0):
    mute()
    extraText = ''
    rc = ''
    if card.markers[Not_rezzed] == 0: whisper("you can't rez a rezzed card")
    elif isRezzable(card) == -1: whisper("Not a rezzable card")
    else:
        rc = payCost(CostCard[card], cost)
        if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
        elif rc == "free": extraText = " at no cost"
        elif rc != 0: rc = "for {}".format(rc)
        card.isFaceUp = True
        card.markers[Not_rezzed] -= 1
        if card.Type == 'Ice': notify("{} has rezzed {}{}{}.".format(me, card, rc, extraText))
        if card.Type == 'Node': notify("{} has acquired {}{}{}.".format(me, card, rc, extraText))
        if card.Type == 'Upgrade': notify("{} has installed {}{}{}.".format(me, card, rc, extraText))
        executeAutomations ( card, "rez" )

def rezForFree (card, x = 0, y = 0):
	intRez(card, "free")

def derez(card, x = 0, y = 0):
   mute()
   if card.markers[Not_rezzed] == 0:
      if isRezzable(card) == -1: whisper ("Not a rezzable card")
      else:
         card.markers[Bits] = 0
         card.markers[Not_rezzed] += 1
         notify("{} derezzed {}".format(me, card))
         executeAutomations ( card, "derez" )
   else:
      notify ( "you can't derez a unrezzed card")

def expose(card, x = 0, y = 0):
	if not card.isFaceUp:
		mute()
		card.isFaceUp = True
		notify("{} exposed {}".format(me, card))
	else:
		notify("You can't expose this card")

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
    card.target(False)

def intTrashCard (card, stat, cost = "not free",  ActionCost = ''):
    mute()
    MUtext = ""
    rc = ''
    if ActionCost == '': 
      ActionCost = '{} '.format(me) # If not actions were used, then just announce our name.
      goodGrammar = 'es' # LOL Grammar Nazi
    else: 
      ActionCost += ' and '
      goodGrammar = ''
    if card.Type == "Tracing": return
    cardowner = card.owner
    rc = payCost(stat, cost)
    if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
    elif rc == 0: 
      if ActionCost.endswith(' and'): ActionCost[:-len(' and')] # if we have no action cost, we don't need the connection.
    else: 
      ActionCost += "pays {} to".format(rc) # If we have Bit cost, append it to the Action cost to be announced.
      goodGrammar = ''
    if card.isFaceUp:
        if num(card.properties["MU Required"]) > 0:
            cardowner.Memory += num(card.properties["MU Required"])
            MUtext = ", freeing up {} MUs".format(card.properties["MU Required"])
        if rc == "free" : notify("{} trashed {} at no cost{}.".format(me, card, MUtext))
        else: notify("{} trash{} {}{}.".format(ActionCost, goodGrammar, card, MUtext))
        executeAutomations (card, "trash")
        card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
    elif (ds == "runner" and cardowner == me) or (ds == "corp" and cardowner != me ): #I'm the runner and I trash my card or I 'm the corp and I trash a runner card
        card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
        if rc == "free" : notify ("{} trashed {} at no cost.".format(me,card))
        else: notify("{} trash{} {}.".format(ActionCost, goodGrammar, card))
    else: #I'm the corp and I trash my card or I'm the runner and I trash a corp's card
        card.moveTo(cardowner.piles['Archives(Hidden)'])
        if rc == "free": notify("{} trashed a hidden card at no cost.".format(me))
        else: notify("{} trash{} a hidden card.".format(ActionCost, goodGrammar))

def trashCard (card, x = 0, y = 0):
	intTrashCard(card, card.Stat)
        
def trashForFree (card, x = 0, y = 0):
	intTrashCard(card, card.Stat, "free")

def pay2AndTrash(card, x=0, y=0):
   ActionCost = useAction()
   if ActionCost == 'ABORT': return
   intTrashCard(card, 2, ActionCost = ActionCost)

def useCard(card,x=0,y=0):
    if card.highlight == None:
        card.highlight = SelectColor
        notify ( "{} uses the ability of {}.".format(me,card) )
    else:
        notify("{} clears {}.".format(me, card))
        card.highlight = None
        card.target(False)

def rulings(card, x = 0, y = 0):
  mute()
  if not card.isFaceUp: return
  openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))

def checkNotHardwareDeck (card):
   mute()
   if card.Type != "Hardware" or not re.search(r'Deck', card.Keywords): return True
   ExistingDecks = [ c for c in table
         if c.owner == me and c.isFaceUp and re.search(r'Deck', c.Keywords) ]
   if len(ExistingDecks) != 0 and not confirm("You already have at least one hardware deck in play. Are you sure you want to install {}?\n\n(If you do, your installed Decks will be automatically trashed at no cost)".format(card.name)): return False
   else: 
      for HWDeck in ExistingDecks: trashForFree(HWDeck)
   return True   

def checkUnique (card):
   mute()
   if not re.search(r'Unique', card.Keywords): return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and c.name == card.name and re.search(r'Unique', c.Keywords) ]
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
   global TypeCard, CostCard
   extraText = ''
   mute() 
   chooseSide() # Just in case...
   if re.search(r'Double', card.Keywords): NbReq = 2 # Some cards require two actions to play. This variable is passed to the useAction() function.
   else: NbReq = 1 #In case it's not a "Double" card. Then it only uses one action to play.
   ActionCost = useAction(count = NbReq)
   if ActionCost == 'ABORT': return  #If the player didn't have enough actions and opted not to proceed, do nothing.
   if checkUnique(card) == False: return #If the player has the unique card and opted not to trash it, do nothing.
   if not checkNotHardwareDeck(card): return	#If player already has a deck in play and doesnt want to play that card, do nothing.
   TypeCard[card] = card.Type
   CostCard[card] = card.Cost
   MUtext = ''
   rc = ''
   if card.Type == 'Resource' and re.search(r'Hidden', card.Keywords): hiddenresource = 'yes'
   else: hiddenresource = 'no'
   if card.Type == 'Ice' or card.Type == 'Agenda' or card.Type == 'Node' or (card.Type == 'Upgrade' and not re.search(r'Region', card.Keywords)):
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
         executeAutomations(card,"play")
         return
      rc = payCost(card.Cost, cost)
      if rc == "ABORT": 
         me.Actions += NbReq # If the player didn't notice they didn't have enough bits, we give them back their action
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      if card.Type == 'Program':
         card.moveToTable(-150, 65 * playerside - yaxisMove(card), False)
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
      elif card.Type == 'Upgrade' and re.search(r'Region', card.Keywords):
         card.moveToTable(-220, 240 * playerside - yaxisMove(card), False)
         notify("{}{} to open a base of operations in {}{}.".format(ActionCost, rc, card, extraText))
      else:
         card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
         notify("{}{} to play {}{}.".format(ActionCost, rc, card, extraText))           
   executeAutomations(card,"play")

def playForFree(card, x = 0, y = 0):
	intPlay(card,"free")

def movetoTopOfStack (card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveTo(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to top of {}.".format(me,nameStack) )

def movetoBottomOfStack (card):
	mute()
	Stack = me.piles['R&D/Stack']
	card.moveToBottom(Stack)
	if ( ds == "runner"): nameStack = "Stack"
	else: nameStack = "R&D"

	notify ( "{} moves a card to Bottom of {}.".format(me,nameStack) )

def handtoArchives (card):
	if ds == "runner": return
	mute()
	card.moveTo(me.piles['Trash/Archives(Face-up)'])
	notify ("{} moves a card to their face-up Archives.".format(me))

def handDiscard (card):
    mute()
    if ds == "runner": 
        card.moveTo(me.piles['Trash/Archives(Face-up)'])
        if endofturn: 
            if card.Type == 'Program': notify("{} has killed a hanging process.".format(me))
            elif card.Type == 'Prep': notify("{} has thrown away some notes.".format(me))
            elif card.Type == 'Hardware': notify("{} has deleted some spam mail.".format(me))
            elif card.Type == 'Resource': notify("{} has reconfigured some net protocols.".format(me))
            else: notify("{} has power cycled some hardware.".format(me))
            if len(me.hand) == me.counters['Max Hand Size'].value: 
                notify("{} has now discarded down to their max handsize of {}".format(me, me.counters['Max Hand Size'].value))
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
            if len(me.hand) == me.counters['Max Hand Size'].value: 
                notify("{} has now discarded down to their max handsize of {}".format(me, me.counters['Max Hand Size'].value))
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
        notify("{} perform's the turn's mandatory draw.".format(me))
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
      notify ( "- Error: only {} cards in {}'s Deck.".format(loDeckCount,me) )
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
         notify("- Error: only {} Agenda Points in {}'s R&D.".format(loAP/1,me))
         ok = -1
      if loRunner == 1:
         notify("- Error: Runner Cards found in {}'s R&D.".format(me))
         ok = -1
   else:
      loCorp = 0
      for card in group:
         card.moveTo(me.piles['Trash/Archives(Face-up)'])
         if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
         if card.Player == "corp": loCorp = 1
         card.moveToBottom(group)

      if loCorp == 1:
         notify("- Error: Corp Cards found in {}'s Stack.".format(me))
         ok = -1
   if ok == 0: notify("-> Deck of {} OK !".format(me))
   return ok

#------------------------------------------------------------------------------
# Automations
#------------------------------------------------------------------------------
def executeAutomations(card,action = ''):
    if not Automation: return
    if not card.isFaceUp: return
    AutoScript = card.AutoScript
    if AutoScript == "": return
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
   
#------------------------------------------------------------------------------
# Autoactions
#------------------------------------------------------------------------------

def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if card.Autoscript == "": ASText = "\n\nThis card is not Auto-Scripted!"
   else: ASText = "\n\nThis card is Auto-Scripted:\n[{}]".format(card.AutoScript)
   confirm("{}".format(ASText))

def useAbility(card, x = 0, y = 0):
   mute()
   if not card.isFaceUp or card.markers[Not_rezzed]: # If card is face down assume they wanted to rez 
      intRez(card)
      return
   elif not Automation or card.AutoAction == "": 
      useCard(card) # If card is face up but has no autoscripts, or automation is disabled just notify that we're using an action.
      return
   elif re.search(r'{Custom:', card.AutoScript): 
      customScript(card) # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   ### Checking if card has multiple autoscript options and providing choice to player.
   Autoscripts = card.AutoAction.split('||')
   for autoS in Autoscripts: # Checking and removing any "WhileDeployed" actions.
      if re.search(r'WhileInstalled', autoS) or re.search(r'AtTurnStart', autoS): Autoscripts.remove(autoS)
   if len(Autoscripts) == 0:
      useCard(card) # If the card had only "WhileInstalled"  or AtTurnStart effect, just announce that it is being used.
      return      
   if len(Autoscripts) > 1: 
      abilConcat = "This card has multiple abilities.\nWhich one would you like to use?\n\n" # We start a concat which we use in our confirm window.
      for idx in range(len(Autoscripts)): # If a card has multiple abilities, we go through each of them to create a nicely written option for the player.
         #notify("Autoscripts {}".format(Autoscripts)) # Debug
         abilRegex = re.search(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):([A-Z][a-z ]+)([0-9]*)([A-Z][a-z ]+)-?([A-Za-z -{},]*)", Autoscripts[idx]) # This regexp returns 3-4 groups, which we then reformat and put in the confirm dialogue in a better readable format.
         #notify("abilRegex is {}".format(abilRegex.groups())) # Debug
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
      ### Checking if any of  card effects requires one or more targets first
      if re.search(r'Targeted', activeAutoscript) and not findTarget(activeAutoscript): return
   for activeAutoscript in selectedAutoscripts:
      targetC = findTarget(activeAutoscript)
      ### Warning the player in case we need to
      if chkWarn(activeAutoscript) == 'ABORT': return
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
            Bcost = payCost(actionCost.group(2))
            if Bcost == 'ABORT': # if they can't pay the cost afterall, we return them their actions and abort.
               me.Actions += num(actionCost.group(1))
               return
            if actionCost.group(1) != '0':
               if actionCost.group(3) != '0' or actionCost.group(4) != '0': announceText += ', '
               else: announceText += ' and '
            else: announceText += ' '
            announceText += 'pays {}'.format(actionCost.group(2))
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
      ### Calling the relevant function depending on if we're increasing our own counters, the hoard's or putting card markers.
      if re.search(r'\b(Gain|Loose)([0-9]+)', activeAutoscript): announceText = GainX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bReshuffle([A-Za-z& ]+)', activeAutoscript): 
         reshuffleTuple = ReshuffleX(activeAutoscript, announceText, card) # The reshuffleX() function is special because it returns a tuple.
         announceText = reshuffleTuple[0] # The first element of the tuple contains the announceText string
         X = reshuffleTuple[1] # The second element of the tuple contains the number of cards that were reshuffled from the hand in the deck.
      elif re.search(r'Roll([0-9]+)', activeAutoscript): 
         rollTuple = RollX(activeAutoscript, announceText, card) # Returns like reshuffleX()
         announceText = rollTuple[0] 
         X = rollTuple[1] 
      elif re.search(r'\b(Put|Remove|Refill|Use)([0-9]+)', activeAutoscript): announceText = TokensX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bTransfer([0-9]+)', activeAutoscript): announceText = TransferX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bDraw([0-9]+)', activeAutoscript): announceText = DrawX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bShuffle([A-Za-z& ]+)', activeAutoscript): announceText = ShuffleX(activeAutoscript, announceText, card, targetC, n = X)
      elif re.search(r'\bRun([A-Za-z& ]+)', activeAutoscript): announceText = RunX(activeAutoscript, announceText, card, targetC, n = X)
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
         executeAutomations (card, "trash")
         card.moveTo(card.owner.piles['Trash/Archives(Face-up)'])
      notify("{}.".format(announceText)) # Finally announce what the player just did by using the concatenated string.

def autoscriptCostUndo(card, Autoscript):
   whisper("--> Undoing action...")
   actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", Autoscript)
   me.Actions += num(actionCost.group(1))
   me.counters['Bit Pool'].value += num(actionCost.group(2))
   me.counters['Agenda Points'].value += num(actionCost.group(3))
   if re.search(r"T2:", Autoscript):
      random = rnd(10,5000) # A little wait...
      card.orientation = Rot0

def findTarget(Autoscript):
   return None # Not in use atm.
   
def chkWarn(Autoscript):
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
   return 'OK'

def GainX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0):
   gain = 0
   action = re.search(r'\b(Gain|Lose)([0-9]+)(Bits|Agenda Points|Actions|Bad Publicity|Tags)', Autoscript)
   gain += num(action.group(2))
   if action.group(1) == 'Lose': gain *= -1
   multiplier = per(Autoscript, card, n, targetCard) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if action.group(3) == 'Bits': card.owner.counters['Bit Pool'].value += gain * multiplier
   elif action.group(3) == 'Agenda Points': card.owner.counters['Agenda Points'].value += gain * multiplier
   elif action.group(3) == 'Actions': card.owner.Actions += gain * multiplier
   elif action.group(3) == 'Bad Publicity': card.owner.counters['Bad Publicity'].value += gain * multiplier
   elif action.group(3) == 'Tags': 
      card.owner.Tags += gain * multiplier
      if card.owner.Tags < 0: card.owner.Tags = 0
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   announceString = "{} {} {} {}".format(announceText, action.group(1).lower(), abs(gain * multiplier), action.group(3))
   if not manual and multiplier > 0: notify('--> {}.'.format(announceString))
   else: return announceString

def TransferX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0):
   breakadd = 1
   if not targetCard: targetCard = card # If there's been to target card given, assume the target is the card itself.
   action = re.search(r'\bTransfer([0-9]+)Bits?-to(Bit Pool|Discard)', Autoscript)
   if action.group(1) == '999':
      if targetCard.markers[Bits]: count = targetCard.markers[Bits]
      else: count = 0
   else: count = num(action.group(1))
   if targetCard.markers[Bits] < count: 
      if re.search(r'isCost', Autoscript):
         whisper("You must have at least {} Bits on the card to take this action".format(action.group(1)))
         return 'ABORT'
      elif targetCard.markers[Bits] == 0 and manual: 
         whisper("There was nothing to transfer.")
         return 'ABORT'
      elif targetCard.markers[Bits] == 0 and not manual: return 'ABORT'
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
   announceString = "{} transfer {} bits from {} to {}".format(announceText, transfer + breakadd, targetCard, destination)
   if not manual: notify('--> {}.'.format(announceString))
   else: return announceString   

def TokensX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0):
   if not targetCard: targetCard = card # If there's been to target card given, assume the target is the card itself.
   foundKey = False
   action = re.search(r'\b(Put|Remove|Refill|Use)([0-9]+)([A-Za-z]+)-?', Autoscript)
   #confirm("{}".format(action.group(3)))
   if action.group(3) in mdict: token = mdict[action.group(3)]
   else: # If the marker we're looking for it not defined, then either create a new one with a random color, or look for a token with the custom name we used above.
      if card.markers:
         for key in card.markers:
            if key[0] == action.group(3): 
               foundKey = True
               token = key
      if not foundKey: # If no key is found with the name we seek, then create a new one with a random colour.
         rndGUID = rnd(1,8)
         token = ("{}".format(action.group(3)),"00000000-0000-0000-0000-00000000000{}".format(rndGUID))
   #confirm("Bump")
   count = num(action.group(2))
   multiplier = per(Autoscript, card, n, targetCard, manual)
   if action.group(1) == 'Put': modtokens = count * multiplier
   elif action.group(1) == 'Refill': modtokens = count - targetCard.markers[token]
   elif action.group(1) == 'Use':
      if not targetCard.markers[token] or count > targetCard.markers[token]: 
         whisper("There's not enough counters left on the card to use this ability!")
         return 'ABORT'
      else: modtokens = -count * multiplier
   else: 
      if count == 999:
         if action.group(3) == 'Virus': pass # We deal with removal of viruses later.
         elif targetCard.markers[token]: count = targetCard.markers[token]
         else: 
            whisper("There was nothing to remove.")
            return 'ABORT'
      else: modtokens = -count * multiplier
   if action.group(3) == 'Virus' and count == 999:
      targetCard.markers[virusButcherBoy] = 0
      targetCard.markers[virusCascade] = 0
      targetCard.markers[virusCockroach] = 0
      targetCard.markers[virusGremlin] = 0
      targetCard.markers[virusThought] = 0
      targetCard.markers[virusFait] = 0
      targetCard.markers[virusBoardwalk] = 0
   else: targetCard.markers[token] += modtokens
   if action.group(1) == 'Refill': announceString = "{} {} to {} {}".format(announceText, action.group(1), abs(modtokens), action.group(3))
   elif re.search(r'\bRemove999Virus', Autoscript): announceString = "{} to clean all viruses from their corporate network".format(announceText)
   else: announceString = "{} {} {} {} counters on {}".format(announceText, action.group(1).lower(), abs(modtokens), action.group(3), targetCard)
   if not manual and multiplier > 0: notify('--> {}.'.format(announceString))
   else: return announceString
 
def DrawX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0): # Function for drawing X Cards from the house deck to your hand.
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
   multiplier = per(Autoscript, card, n, targetCard, manual)
   count = drawMany(source, draw * multiplier, destination, True)
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if targetPL == me: announceString = "{} {} {} cards from their {} to their {}".format(announceText, destiVerb, count, source.name, destination.name)
   else: announceString = "{} {} {} cards from {}'s {} to {}'s {}".format(announceText, destiVerb, count, targetPL, source.name, targetPL, destination.name)
   if not manual and multiplier > 0: notify('--> {}.'.format(announceString))
   else: return announceString

def ofwhom(Autoscript):
   if re.search(r'-ofOpponent', Autoscript):
      if len(players) > 1:
         for player in players:
            if player != me and player.getGlobalVariable(ds) != ds: 
               targetPL = player # Opponent needs to be not us, and of a different type. 
                                 # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
      else : 
         whisper("There's no Opponents! Selecting myself.")
         targetPL = me
   else: targetPL = me
   return targetPL
   
def ReshuffleX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0): # A Function for reshuffling a pile into the R&D/Stack
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
   announceString = "{} shuffle their {} to their {}".format(announceText, namestuple[0], namestuple[1])
   if not manual: notify('--> {}.'.format(announceString))
   else: return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0): # A Function for reshuffling a pile into the R&D/Stack
   mute()
   action = re.search(r'\bShuffle([A-Za-z& ]+)', Autoscript)
   targetPL = ofwhom(Autoscript)
   if action.group(1) == 'Trash': pile = targetPL.piles['Trash/Archives(Face-up)']
   elif action.group(1) == 'Stack': pile = targetPL.piles['R&D/Stack']
   elif action.group(1) == 'Hidden Archives': pile = targetPL.piles['Archives(Hidden)']
   shuffle(pile)
   if targetPL == me: announceString = "{} shuffle their {}".format(announceText, pile.name)
   else: announceString = "{} shuffle {}' {}".format(announceText, targetPL, pile.name)
   if not manual: notify('--> {}.'.format(announceString))
   else: return announceString
   
def RollX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0): # Function for drawing X Cards from the house deck to your hand.
   action = re.search(r'\bRoll([0-9]+)Dice', Autoscript)
   count = num(action.group(1))
   multiplier = per(Autoscript, card, n, targetCard, manual)
   d6 = rolld6(silent = True) # For now we always roll 1d6. If we ever have a autoaction which needs more then 1, I'll implement it.
   announceString = "{} roll {} on a die".format(announceText, d6)
   if not manual: notify('--> {}.'.format(announceString))
   else: return (announceString, d6)
   
def RunX(Autoscript, announceText, card, targetCard = None, manual = True, n = 0): # Function for drawing X Cards from the house deck to your hand.
   action = re.search(r'\bRun([A-Z][A-Za-z& ]+)', Autoscript)
   announceString = "{} start a run on {}".format(announceText, action.group(1))
   if not manual: notify('--> {}.'.format(announceString))
   else: return announceString

def per(Autoscript, card = None, count = 0, targetCard = None, manual = False): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   per = re.search(r'\b(per|upto)(Assigned|Target|Parent|Generated|Installed|Rezzed|Transferred|Bought)?([{A-Z][A-Za-z0-9,_ {}&]*)[-]?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable.
   if per: # If the  search was successful...
      if per.group(2) and per.group(2) == 'Target': useC = targetCard # If the effect is targeted, we need to use the target's attributes
      else: useC = card # If not, use our own.
      if per.group(3) == 'X': multiplier = count      
      elif per.group(3) == 'AdvancementMarker': multiplier = useC.markers[Advance]
      elif per.group(3) == 'BitMarker': multiplier = useC.markers[Bits]
      elif per.group(3) == 'GenericMarker': multiplier = useC.markers[Generic]
   else: multiplier = 1
   return multiplier
  
def customScript(card):
   useCard(card) # Not in use atm.
   
def TrialError(group, x=0, y=0):
   table.create("c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8", 0, 200 * playerside, 1 ) #trace card
   create3DataForts(group)
   
def atTurnStartEffects():
   if not StartAutomation: return
   TitleDone = False
   for card in table:
      effect = re.search(r'AtTurnStart:([A-Z][A-Za-z]+)([0-9]+)([A-Z][A-Za-z0-9 ]+)-?([A-Za-z0-9- {}$]*)', card.AutoScript)
      if card.owner != me or not effect: continue
      if effect.group(4) and re.search(r'isOptional', effect.group(4)) and not confirm("{} can have the following optional ability activated at the start of your turn:\n\n[ {} {} {} ]\n\nDo you want to activate it?".format(card.name, effect.group(1), effect.group(2),effect.group(3))): continue
      if not TitleDone: notify(":::{}'s Start of Turn Effects:::".format(me))
      TitleDone = True
      effectNR = num(effect.group(2))
      announceText = "{}:".format(card)
      if effect.group(1) == 'Gain' or effect.group(1) == 'Lose':
         GainX(card.AutoScript, announceText, card, manual = False)
      if effect.group(1) == 'Transfer':
         TransferX(card.AutoScript, announceText, card, manual = False)
      if effect.group(1) == 'Draw':
         DrawX(card.AutoScript, announceText, card, manual = False)
      if effect.group(1) == 'Refill':
         TokensX(card.AutoScript, announceText, card, manual = False)
   if me.counters['Bit Pool'].value < 0: 
      notify(":::Warning::: {}'s start of turn effects cost more Bits than they had in their Bit Pool!".format(me))
   if TitleDone: notify(":::--------------------------:::".format(me))
