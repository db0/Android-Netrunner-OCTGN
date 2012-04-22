Advance = ("Advance", "73b8d1f2-cd54-41a9-b689-3726b7b86f4f")
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
Automation = False # If True, game will automatically trigger card effects when playing cards. Requires specific preparation in the sets.
                   # Starts False and is switched on automatically at Jack In
UniBits = True # If True, game will display bits as unicode characters ❶, ❷, ❿ etc

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

def useAction(group = table, x=0, y=0):
    mute()
    global newturn
    if me.Actions < 1: 
        if not confirm("You have no more actions left. Are you sure you want to continue?"): return 'ABORT'
    if ds == 'corp': act = 4 - me.Actions
    else: act = 5 - me.Actions
    notify("{} takes Action #{}".format(me,act))
    me.Actions -= 1

def goToEndTurn(group, x = 0, y = 0):
    mute()
    global endofturn
    if ( ds == "" ):
        whisper ("Please perform the game setup first (Ctrl+Shift+S)")
        return
    if me.Actions > 0: # If the player has not used all their actions for this turn, remind them, just in case.
        if not confirm("You have not taken all your actions for this turn, are you sure you want to declare end of turn"): return
    if len(me.hand) > me.counters['Max Hand Size'].value: #If the player is holding more cards than their hand max. remind them that they need to discard some 
                                                       # and put them in the end of turn to allow them to do so.
        if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
            if not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
            else: notify("Note: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),me.counters['Max Hand Size'].value))
        else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
            if (ds == "corp"): notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
            else: notify ("Runner {} is rebooting all systems for the day.".format(me))
            whisper('Note: You have more card in your hand than your current hand size maximum. Please discard enough and then use the "Declare End of Turn" action again.')
            endofturn = True
            return
    if (ds == "corp"): notify ("The Corporation of {} has reached CoB (Close of Business hours).".format(me))
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
                notify("Note: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),me.counters['Max Hand Size'].value))
            else: notify("Note: {} has skipped their End-of-Turn phase".format(me))
            endofturn = False
    if (ds == "" ):
        whisper ("Please perform the game setup first (Ctrl+Shift+S)")
        return
    if me.Actions < 0: 
        if not confirm("Your actions were negative from last turn. Was this a result of a penalty you suffered from a card?"): 
            me.Actions = maxActions # If the player did not have a penalty, then we assume those were extra actions granted by some card effect, so we make sure they have their full maximum
        else: 
            me.Actions += maxActions # If it was a penalty, then it remains with them for this round, which means they have less actions to use.
            notify("{} is starting with {} less actions this turn, due to a penalty from a previous turn. They have {} actions this turn".format(me,maxActions - me.Actions, me.Actions))
    else: me.Actions = maxActions
    if (ds == "corp"): notify ("The offices of {}'s Corporation are now open for business.".format(me))
    else: notify ("Runner {} has woken up".format(me))
    newturn = True

def modActions(group,x=0,y=0):
    global maxActions
    mute()
    if ds =="corp": maxActions = askInteger("What is your current maximum Actions per turn?", 3)
    else: maxActions = askInteger("What is your current maximum Actions per turn?", 4)
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

def switchUniBits(group,x=0,y=0,command = 'Off'):
    global UniBits
    if UniBits and command != 'On':
        whisper("Bits will now be displayed as normal numbers.".format(me))
        UniBits = False
    else:
        whisper("Bits will now be displayed as unicode.".format(me))
        UniBits = True
        
def create3DataForts(group):
	table.create("2a0b57ca-1714-4a70-88d7-25fdf795486f", 150, 160 * playerside, 1)
	table.create("181de100-c255-464f-a4ed-4ac8cd728c61", 300, 160 * playerside, 1)
	table.create("59665835-0b0c-4710-99f7-8b90377c35b7", 450, 160 * playerside, 1)

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
    ds = TopCard.Player
    TopCard.moveTo(me.piles['R&D/Stack'])
    if checkDeckNoLimit(stack) != 0: notify ("SHOULD RETURN")
    me.counters['Bit Pool'].value =5
    me.counters['Max Hand Size'].value =5
    me.counters['Tags'].value =0
    me.counters['Agenda Points'].value =0
    me.counters['Bad Publicity'].value =0
    if ds == "corp":
        me.counters['Actions'].value =3
        me.counters['Memory'].value =0
        maxActions = 3
        NameDeck = "R&D"
        create3DataForts(group)
        notify("{} is playing as Corporation".format(me))      
    else:
        me.counters['Actions'].value =4
        me.counters['Memory'].value =4
        maxActions = 4
        NameDeck = "Stack"
        notify("{} is playing as Runner".format(me))
    table.create("c0f18b5a-adcd-4efe-b3f8-7d72d1bd1db8", 0, 200 * playerside, 1 ) #trace card
    switchAutomation(group,x,y,'On')
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
def intRun(Name):
	notify ("{} declares a run on {}.".format(me,Name))

def runHQ(group, x=0,Y=0):
    if useAction() == 'ABORT': return
    if ds == "runner": intRun("HQ")

def runRD(group, x=0,Y=0):
    if useAction() == 'ABORT': return
    if ds == "runner": intRun("R&D")

def runArchives(group, x=0,Y=0):
    if useAction() == 'ABORT': return
    if ds == "runner": intRun ("the Archives")

def runSDF(group, x=0,Y=0):
    if useAction() == 'ABORT': return
    if ds == "runner": intRun("a subsidiary data fort")

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
    if useAction() == 'ABORT': return
    if payCost(2) == "ABORT": 
        me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
        return # If the player didn't have enough money to pay and aborted the function, then do nothing.
    me.counters['Tags'].value -= 1
    notify (" {} pays {} and looses 1 tag.".format(me,uniBit(2)))

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
	intAddBits ( card, count)
	
def remBits(card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many Bits?", 1)
	if ( count > card.markers[Bits]): count = card.markers[Bits]

	card.markers[Bits] -= count
	if ( card.isFaceUp == True): notify("{} removes {} from {}.".format(me,uniBit(count),card))
	else: notify("{} removes {} from a card.".format(me,uniBit(count)))

def remBits2BP (card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many Bits?", 1)
	if ( count > card.markers[Bits]): count = card.markers[Bits]

	card.markers[Bits] -= count
	me.counters['Bit Pool'].value += count 
	if ( card.isFaceUp == True): notify("{} removes {} from {} to their Bit Pool.".format(me,uniBit(count),card))
	else: notify("{} takes {} from a card to their Bit Pool.".format(me,uniBit(count)))

def addPlusOne(card, x = 0, y = 0):
	mute()
	card.markers[PlusOne] += 1
	notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
	mute()
	card.markers[MinusOne] += 1
	notify("{} adds one +1 marker on {}.".format(me,card))
#------------------------------------------------------------------------------
# advancing cards
#------------------------------------------------------------------------------
def advanceCardP(card, x = 0, y = 0):
    mute()
    if useAction() == 'ABORT': return
    if payCost(1) == "ABORT": 
        me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
        return # If the player didn't have enough money to pay and aborted the function, then do nothing.
    card.markers[Advance] += 1
    if ( card.isFaceUp == True): notify("{} paid 1 and advanced {}.".format(me,card))
    else: notify("{} paid {} and advanced a card.".format(me,uniBit(1)))

def addXadvancementCounter(card, x=0, y=0):
	mute()
	count = askInteger("Add how many counters?", 1)
	card.markers[Advance] += count
	if ( card.isFaceUp == True): notify("{} adds {} advancement counters on {}.".format(me,count,card))
	else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
	mute()
	count = askInteger("Remove how many counters?", 1)
	if ( count > card.markers[Advance] ): count=card.markers[Advance]
	card.markers[Advance] -= count
	if ( card.isFaceUp == True): notify("{} removes {} advancement counters on {}.".format(me,count,card))
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
    if (card.properties['Type'] <> "Tracing"): return
    TraceValue = askInteger("Bet How Many?", 0)
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
    if useAction() == 'ABORT': return
    notify ("{} Receives {}.".format(me,uniBit(1)))
    me.counters['Bit Pool'].value += 1
    
#------------------------------------------------------------------------------
# Other functions on card
#------------------------------------------------------------------------------

def payCost(count = 1, cost = 'not_free', notification = silent): # A function that removed the cost provided from our bit pool, after checking that we have enough.
   if cost == 'free': return 'free'
   count = num(count)
   if count == 0 : return 0# If the card has 0 cost, there's nothing to do.
   if me.counters['Bit Pool'].value < count: # If we don't have enough Bits in the pool, we assume card effects or mistake and notify the player that they need to do things manually.
      if not confirm("You do not seem to have enough Bits in your pool to take this action. Are you sure you want to proceed? \
      \n(If you do, your Bit Pool will go to the negative. You will need to increase it manually as required.)"): return 'ABORT'
      if notification == loud: notify("{} was supposed to pay {} but only has {} in their bit pool. They'll need to reduce the cost by {} with card effects.".format(me, uniBit(count), uniBit(me.counters['Bit Pool'].value), uniBit(count - me.counters['Bit Pool'].value)))   
      me.counters['Bit Pool'].value -= count 
   else: # Otherwise, just take the money out and inform that we did if we're "loud".
      me.counters['Bit Pool'].value -= count
      if notification == loud: notify("{} has paid {}. {} remaining.".format(me, uniBit(count), uniBit(me.counters['Bit Pool'].value)))  
   return count
   
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
    if card.markers[Not_rezzed] == 0: whisper("you can't rez a rezzed card")
    elif isRezzable(card) == -1: whisper("Not a rezzable card")
    else:
        rc = payCost(CostCard[card], cost, loud)
        if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
        elif rc == "free": extraText = " at no cost"
        card.isFaceUp = True
        card.markers[Not_rezzed] -= 1
        if card.Type == 'Ice': notify("{} has rezzed {}{}.".format(me, card, extraText))
        if card.Type == 'Node': notify("{} has acquired {}{}.".format(me, card, extraText))
        if card.Type == 'Upgrade': notify("{} has installed {}{}.".format(me, card, extraText))
        executeAutomations ( card, "rez" )

def rezForFree (card, x = 0, y = 0):
	intRez(card, "free")

def derez(card, x = 0, y = 0):
   if (card.markers[Not_rezzed] == 0):
	if ( isRezzable(card) == -1):
		whisper ("Not a rezzable card")
		return
	else:
      		mute()
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

def rolld6(group, x = 0, y = 0):
    mute()
    n = rnd(1, 6)
    notify("{} rolls {} on a 6-sided die.".format(me, n))

def selectAsTarget (card, x = 0, y = 0):
    card.target(True)

def clear(card, x = 0, y = 0):
    notify("{} clears {}.".format(me, card))
    card.highlight = None
    card.target(False)

def intTrashCard (card, stat, cost = "not free"):
    mute()
    MUtext = ""
    if card.Type == "Tracing": return
    cardowner = card.owner
    rc = payCost(stat, cost, loud)
    if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
    if card.isFaceUp:
        if num(card.properties["MU Required"]) > 0:
            cardowner.Memory += num(card.properties["MU Required"])
            MUtext = ", freeing up {} MUs".format(card.properties["MU Required"])
        if rc == "free" : notify("{} trashed {} at no cost{}.".format(me, card, MUtext))
        else: notify("{} trashed {}{}.".format(me, card, MUtext))
        executeAutomations (card, "trash")
        card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
    elif (ds == "runner" and cardowner == me) or (ds == "corp" and cardowner != me ): #I'm the runner and I trash my card or I 'm the corp and I trash a runner card
        card.moveTo(cardowner.piles['Trash/Archives(Face-up)'])
        if rc == "free" : notify ("{} trashed {} at no cost.".format(me,card))
        else: notify("{} trashed {}.".format(me, cost, card))
    else: #I'm the corp and I trash my card or I'm the runner and I trash a corp's card
        card.moveTo(cardowner.piles['Archives(Hidden)'])
        if rc == "free": notify("{} trashed a hidden card at no cost.".format(me))
        else: notify("{} trashed a hidden card.".format(me,cost))

def trashCard (card, x = 0, y = 0):
	intTrashCard(card, card.Stat)
        
def trashForFree (card, x = 0, y = 0):
	intTrashCard(card, card.Stat, "free")

def pay2AndTrash ( card, x=0, y=0):
    if useAction() == 'ABORT': return
    intTrashCard(card, 2)

def useCard(card,x=0,y=0):
    if card.highlight == None:
        card.highlight = SelectColor
        notify ( "{} uses the ability of {}.".format(me,card) )
    else:
        notify("{} clears {}.".format(me, card))
        card.highlight = None
        card.target(False)

#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------
def intPlay(card, cost = 'not_free'):
    global TypeCard, CostCard
    extraText = ''
    mute() 
    chooseSide() # Just in case...
    if useAction() == 'ABORT': return
    TypeCard[card] = card.Type
    CostCard[card] = card.Cost
    MUtext = ""
    if card.Type == 'Resource' and re.search(r'Hidden', card.Keywords): hiddenresource = 'yes'
    else: hiddenresource = 'no'
    if card.Type == 'Ice' or card.Type == 'Agenda' or card.Type == 'Node' or (card.Type == 'Upgrade' and not re.search(r'Region', card.Keywords)):
        card.moveToTable(-180, 160 * playerside - yaxisMove(card), True) # Agendas, Nodes and non-region Upgrades all are played to the same spot now.
        if TypeCard[card] == 'Ice': 
            card.orientation ^= Rot90
            card.moveToTable(-180, 65 * playerside - yaxisMove(card), True) # Ice are moved a bit more to the front and played sideways.
        card.markers[Not_rezzed] += 1
        notify("{} installs a card.".format(me))
    elif card.Type == 'Program' or card.Type == 'Prep' or card.Type == 'Resource' or card.Type == 'Hardware':
        if num(card.properties["MU Required"]) > 0:
            me.Memory -= num(card.properties["MU Required"])
            MUtext = ", using up {} MUs".format(card.properties["MU Required"])
        if card.Type == 'Resource' and hiddenresource == 'yes':
            card.moveToTable(-180, 230 * playerside - yaxisMove(card), True)
            notify("{} installs a card.".format(me))
            executeAutomations(card,"play")
            return
        rc = payCost(card.Cost, cost, loud)
        if rc == "ABORT": 
            me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
            return # If the player didn't have enough money to pay and aborted the function, then do nothing.
        elif rc == "free": extraText = " at no cost"
        if card.Type == 'Program':
            card.moveToTable(-150, 65 * playerside - yaxisMove(card), False)
            notify("{} has installed {}{}{}.".format(me, card, extraText,MUtext))
        elif card.Type == 'Prep':
            card.moveToTable(0, 0 - yaxisMove(card), False)
            notify("{} has prepped with {}{}.".format(me, card, extraText))
        elif card.Type == 'Hardware':
            card.moveToTable(-210, 160 * playerside - yaxisMove(card), False)
            notify("{} has purchased {}{}{}.".format(me, card, extraText,MUtext))
        elif card.Type == 'Resource' and hiddenresource == 'no':
            card.moveToTable(180, 240 * playerside - yaxisMove(card), False)
            notify("{} has acquired {}{}{}.".format(me, card, extraText,MUtext))
        else:
            card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
            notify("{} plays {}{}{}.".format(me, card, extraText,MUtext))
    else:
        rc = payCost(card.Cost, cost, loud)
        if rc == "ABORT": 
            me.Actions += 1 # If the player didn't notice they didn't have enough bits, we give them back their action
            return # If the player didn't have enough money to pay and aborted the function, then do nothing.
        elif rc == "free": extraText = " at no cost"
        if card.Type == 'Operation':
            card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
            notify("{} initiates {}{}.".format(me, card, extraText))
        elif card.Type == 'Upgrade' and re.search(r'Region', card.Keywords):
            card.moveToTable(-220, 240 * playerside - yaxisMove(card), False)
            notify("{} opened a base of operations in {}{}.".format(me, card, extraText))
        else:
            card.moveToTable(0, 0 * playerside - yaxisMove(card), False)
            notify("{} has played {}{}.".format(me, card, extraText))           
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

def handtoStack (group):
    mute()
    Stack = me.piles['R&D/Stack']
    for c in me.hand: c.moveTo(Stack)
    if ( ds == "runner"):
        nameHand = "Hand"
        nameStack = "Stack"
    else:
        nameHand = "HQ"
        nameStack = "R&D"
    notify ("{} moves {} to {}.".format(me,nameHand,nameStack))


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
        if useAction() == 'ABORT': return
        group[0].moveTo(me.hand)
        notify("{} draws a card.".format(me))

def drawManySilent(group, count):
	SSize = len(group)
	if SSize == 0: return 0
	mute()
	if ( count > SSize) : count=SSize
	for c in group.top(count): c.moveTo(me.hand)
	return count

def drawMany(group, count = None):
	SSize = len(group)
	if SSize == 0: return
	mute()
	if count == None: count = askInteger("Draw how many cards?", 5)
	if ( count > SSize) : count=SSize
	for c in group.top(count): c.moveTo(me.hand)

	notify("{} draws {} cards.".format(me, count))

def toarchives(group = me.piles['Archives(Hidden)']):
	mute()
	Archives = me.piles['Archives(Hidden)']
	for c in group: c.moveTo(Archives)
	#Archives.shuffle()
	notify ("{} moves Hidden Archives to Archives.".format(me))

def archivestoStack(group):
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
	notify ("{} moves {} to {}.".format(me,nameTrash,nameStack))

def mill(group):
	if len(group) == 0: return
	mute()
    	count = askInteger("Mill how many cards?", 1)
	if ( ds == "runner"):
    		for c in group.top(count): c.moveTo(me.piles['Archives(Hidden)'])
		nameStack = "Stack"
		nameTrash = "Trash"
	else:
		for c in group.top(count): c.moveTo(me.piles['Archives(Hidden)'])
		nameStack = "HQ"
		nameTrash = "Archives H"

    	notify("{} mills the top {} cards from {} to {}.".format(me, count,nameStack,nameTrash))

def moveXtopCardtoBottomStack(group):
	if len(group) == 0: return
	mute()
    	count = askInteger("Move how many cards?", 1)
	for c in group.top(count): c.moveToBottom(group)
	if ( ds == "runner"): nameStack = "Stack"
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
    elif re.search(r'autoAddMUAndBitsCounter', AutoScript): autoAddMUAndCounter(card,Param1,Param2)
    elif re.search(r'MUHandSizeBitsCounter', AutoScript): autoaddMUHandSizeBitsCounter(card,Param1,Param2)
    elif re.search(r'autoAddMU', AutoScript): autoAddMU(card,Param1,Param2)
    elif re.search(r'autoAddHandSize', AutoScript): autoAddHandSize(card,Param1,Param2)

def autoGainXDrawY ( card, Param1, Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	drawManySilent ( me.piles['R&D/Stack'], Param2)
	notify ( "--> {} gains {} bits and draws {} cards.".format(me,Param1,Param2) )

def autoGainX ( card, Param1,Param2 ):
	mute()
	me.counters['Bit Pool'].value += Param1
	notify ( "--> {} gains {} bits.".format(me,Param1) )

def autoDrawX ( card, Param1,Param2):
	mute()
	drawManySilent ( me.piles['R&D/Stack'], Param1)
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

def regexptst(card, x=0, y=0):
    s = re.match(r"(A)([0-9]+)(B)([0-9]+)(T)([01])", card.AutoScript)
    whisper("Actions {}, Bits {}".format(s.group(2), s.group(4)))

    sAddBits = re.search(r"(Gain)([0-9]+)(Bits)", card.AutoScript)
    sRemTags = re.search(r"(Rem)([0-9]+)(Tags)", card.AutoScript)
    whisper("Add {} Bits and {} Tags".format(sAddBits.group(2), sRemTags.group(2)))
    
