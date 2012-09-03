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
# This file contains the basic table actions in ANR. They are the ones the player calls when they use an action in the menu.
# Many of them are also called from the autoscripts.
###=================================================================================================================###
    
import re         
#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------
ds = None
identName = None

ModifyDraw = 0 #if True the audraw should warn the player to look at r&D instead 

DifficultyLevels = { }

installedCount = {} # A dictionary which keeps track how many of each card type have been installed by the player.

MemoryRequirements = {}
InstallationCosts = {}
maxClicks = 3
scoredAgendas = 0
currClicks = 0

DMGwarn = True # A boolean varialbe to track whether we've warned the player about doing automatic damage.
Dummywarn = True # Much like above, but it serves to remind the player not to trash some cards.
DummyTrashWarn = True
PriorityInform = True # Explains what the "prioritize card" action does.
ExposeTargetsWarn = True # A boolean variable that reminds the player to select multiple targets to expose for used by specific cards like Encryption Breakthrough
RevealandShuffleWarn = True # Similar to above.
newturn = True #We use this variable to track whether a player has yet to do anything this turn.
endofturn = False #We use this variable to know if the player is in the end-of-turn phase.
failedRequirement = True #A Global boolean that we set in case an Autoscript cost cannot be paid, so that we know to abort the rest of the script.
AfterRunInf = True # A warning to remind players that some actions have effects that need to be activated after a run.
AfterTraceInf = True # Similar to above
lastKnownNrClicks = 0 # A Variable keeping track of what the engine thinks our action counter should be, in case we change it manually.


#---------------------------------------------------------------------------
# Card Placement
#---------------------------------------------------------------------------

def placeCard(card, action = 'install'):
   if debugVerbosity >= 1: notify(">>> placeCard(){}".format(extraASDebug())) #Debug
   global installedCount
   type = card.Type
   if action != 'install' and type == 'Agenda':
      if ds == 'corp': type == 'scoredAgenda'
      else: type == 'liberatedAgenda'
   if debugVerbosity >= 3: notify("### Setting installedCount. Type is: {}".format(type)) #Debug
   if installedCount.get(type,None) == None: installedCount[type] = 0
   else: installedCount[type] += 1
   if debugVerbosity >= 2: notify("### installedCount is: {}. Setting loops...".format(installedCount[type])) #Debug
   loopsNR = installedCount[type] / (place[type][3]) 
   loopback = place[type][3] * loopsNR 
   if loopsNR and place[type][3] != 1: offset = 15 * (loopsNR % 3) # This means that in one loop the offset is going to be 0 and in another 15.
   else: offset = 0
   if debugVerbosity >= 3: notify("### installedCount[type] is: {}.\nLoopsNR is: {}.\nLoopback is: {}\nOffset is: {}".format(installedCount[type],offset, loopback, offset)) #Debug
   card.moveToTable(place[type][0] + (((cwidth(card,0) + place[type][2]) * (installedCount[type] - loopback)) + offset) * place[type][4],place[type][1]) 
   # To explain the above, we place the card at: Its original location
   #                                             + the width of the card
   #                                             + a predefined distance from each other times the number of other cards of the same type
   #                                             + the special offset in case we've done one or more loops
   #                                             And all of the above, multiplied by +1/-1 (place[type][4]) in order to direct the cards towards the left or the right
   #                                             And finally, the Y axis is always the same in ANR.
   if type == 'Agenda' or type == 'Upgrade' or type == 'Asset': # camouflage until I create function to install them on specific Server, via targeting.
      installedCount['Agenda'] = installedCount[type]
      installedCount['Asset'] = installedCount[type]
      installedCount['Upgrade'] = installedCount[type]
   if debugVerbosity >= 3: notify("<<< placeCard()") #Debug
   
#---------------------------------------------------------------------------
# Clicks indication
#---------------------------------------------------------------------------

def useClick(group = table, x=0, y=0, count = 1):
   if debugVerbosity >= 1: notify(">>> useClick(){}".format(extraASDebug())) #Debug
   global currClicks, lastKnownNrClicks
   mute()
   extraText = ''
   if count == 0: return '{} takes a free action'.format(me)
   clicksReduce = findCounterPrevention(me.Clicks, 'Clicks', me)
   if clicksReduce: notify(":::WARNING::: {} had to forfeit their next {} clicks".format(me, clicksReduce))
   me.Clicks -= clicksReduce
   if me.Clicks < count: 
      if not confirm("You do not have enough clicks left to take this action. Are you sure you want to continue?"): return 'ABORT'
      else: extraText = ' (Exceeding Max!)'
   currClicks += count + lastKnownNrClicks - me.Clicks# If the player modified their click counter manually, the last two will increase/decreate our current click accordingly.
   me.Clicks -= count
   lastKnownNrClicks = me.Clicks
   if debugVerbosity >= 3: notify("<<< useClick") #Debug
   if count == 2: return "{} {} {} uses Double Click #{} and #{}{}".format(uniClick(),uniClick(),me,currClicks - 1, currClicks,extraText)
   elif count == 3: return "{} {} {} {} uses Triple Click #{}, #{} and #{}{}".format(uniClick(),uniClick(),uniClick(),me,currClicks - 2, currClicks - 1, currClicks,extraText)
   else: return "{} {} uses Click #{}{}".format(uniClick(),me,currClicks,extraText)

def modClicks(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> modClicks(){}".format(extraASDebug())) #Debug
   global maxClicks
   mute()
   bkup = maxClicks
   maxClicks = askInteger("What is your current maximum Clicks per turn?", maxClicks)
   if maxClicks == None: maxClicks = bkup # In case the player closes the window, we restore their previous max.
   else: notify("{} has set their Max Clicks to {} per turn".format(me,maxClicks))
   
#---------------------------------------------------------------------------
# Start/End of turn
#---------------------------------------------------------------------------   
def goToEndTurn(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> goToEndTurn(){}".format(extraASDebug())) #Debug
   mute()
   global endofturn, currClicks, newturn
   if ds == None:
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   if getGlobalVariable('status') == 'running': jackOut() # If the player forgot to end the run, we do it for them now.
   if me.Clicks > 0: # If the player has not used all their clicks for this turn, remind them, just in case.
      if debugVerbosity <= 0 and not confirm("You have not taken all your clicks for this turn, are you sure you want to declare end of turn"): return
   if len(me.hand) > currentHandSize(): #If the player is holding more cards than their hand max. remind them that they need to discard some 
                                        # and put them in the end of turn to allow them to do so.
      if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
         if debugVerbosity <= 0 and not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
         else: notify(":::Warning::: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
      else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
         if ds == "corp": notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
         else: notify ("Runner {} is rebooting all systems for the day.".format(me))
         if debugVerbosity <= 0: confirm(':::Warning:::\n\n You have more card in your hand than your current hand size maximum of {}. Please discard enough and then use the "Declare End of Turn" action again.'.format(currentHandSize()))
         endofturn = True
         return
   endofturn = False
   newturn = False
   currClicks = 0
   clearAll() # Just in case the player has forgotten to remove their temp markers.
   atTimedEffects('End')
   if ds == "corp": notify ("=> {} ({}) has reached CoB (Close of Business hours).".format(identName, me))
   else: notify ("=> {} ({}) has gone to sleep for the day.".format(identName,me))

def goToSot (group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> goToSot(){}".format(extraASDebug())) #Debug
   global newturn, endofturn, lastKnownNrClicks, currClicks
   mute()
   clearNoise()
   if endofturn or currClicks or newturn:
      if debugVerbosity <= 0 and not confirm("You have not yet properly ended you previous turn. You need to use F12 after you've finished all your clicks.\n\nAre you sure you want to continue?"): return
      else: 
         if len(me.hand) > currentHandSize(): # Just made sure to notify of any shenanigans
            notify(":::Warning::: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
         else: notify(":::Warning::: {} has skipped their End-of-Turn phase".format(me))
         endofturn = False
   if ds == None:
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   currClicks = 0 # We wipe it again just in case they ended their last turn badly but insist on going through the next one.
   clicksReduce = findCounterPrevention(maxClicks, 'Clicks', me) # Checking if the player has any effects which force them to forfeit clicks.
   if clicksReduce: extraTXT = " ({} forfeited)".format(clicksReduce)
   else: extraTXT = ''
   if me.Clicks < 0: 
      if debugVerbosity <= 0 and not confirm("Your clicks were negative from last turn. Was this a result of a penalty you suffered from a card?"): 
         me.Clicks = maxClicks - clicksReduce # If the player did not have a penalty, then we assume those were extra clicks granted by some card effect, so we make sure they have their full maximum
      else: 
         me.Clicks += maxClicks - clicksReduce # If it was a penalty, then it remains with them for this round, which means they have less clicks to use.
         notify("{} is starting with {} less clicks this turn, due to a penalty from a previous turn.")
   else: me.Clicks = maxClicks - clicksReduce
   lastKnownNrClicks = me.Clicks
   myCards = (card for card in table if card.controller == me and card.owner == me)
   for card in myCards: 
      if card in Stored_Type and Stored_Type[card] != 'ICE': card.orientation &= ~Rot90 # Refresh all cards which can be used once a turn.
   newturn = True
   atTimedEffects('Start') # Check all our cards to see if there's any Start of Turn effects active.
   if ds == "corp": notify("=> The offices of {} ({}) are now open for business. They have {} clicks for this turn{}.".format(identName,me,me.Clicks,extraTXT))
   else: notify ("=> {} ({}) has woken up. They have {} clicks for this turn{}.".format(identName,me,me.Clicks,extraTXT))

#------------------------------------------------------------------------------
# Game Setup
#------------------------------------------------------------------------------

def createStartingCards():
   if debugVerbosity >= 1: notify(">>> createStartingCards(){}".format(extraASDebug())) #Debug
   if ds == "corp":
      traceCard = table.create("eb7e719e-007b-4fab-973c-3fe228c6ce20", 510, 200, 1, True) #The Trace card
      storeSpecial(traceCard)
      HQ = table.create("81cba950-9703-424f-9a6f-af02e0203762", 0, 0, 1, True)
      HQ.moveToTable(125, 185) # MoveToTable is accurate. Table.create isn't.
      storeSpecial(HQ)
      RD = table.create("fbb865c9-fccc-4372-9618-ae83a47101a2", 0, 0, 1, True)
      RD.moveToTable(245, 185)
      storeSpecial(RD)
      ARC = table.create("47597fa5-cc0c-4451-943b-9a14417c2007", 0, 0, 1, True)
      ARC.moveToTable(363, 185)
      storeSpecial(ARC)
      AV = table.create("23473bd3-f7a5-40be-8c66-7d35796b6031", 0, 0, 1, True) # The Virus Scan card.
      AV.moveToTable(510, 127)
      storeSpecial(AV)
   else:
      traceCard = table.create("eb7e719e-007b-4fab-973c-3fe228c6ce20", 566, -323, 1, True) #The Trace card
      traceCard.moveToTable(566, -323) # Otherwise it's bugging out
      storeSpecial(traceCard)
      TC = table.create("71a89203-94cd-42cd-b9a8-15377caf4437", 471, -325, 1, True) # The Technical Difficulties card.
      TC.moveToTable(471, -325) # It's never creating them in the right place. Move is accurate.
      storeSpecial(TC)   
 
def intJackin(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> intJackin(){}".format(extraASDebug())) #Debug
   global ds, maxClicks
   mute()
   if ds and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
   ds = None
   if not table.isTwoSided() and not confirm(":::WARNING::: This game is designed to be played on a two-sided table. Things will be extremely uncomfortable otherwise!! Please start a new game and makde sure the  the appropriate button is checked. Are you sure you want to continue?"): return
   chooseSide()
   #for type in Automations: switchAutomation(type,'Announce') # Too much spam.
   deck = me.piles['R&D/Stack']
   if len(deck) == 0:
      whisper ("Please load a deck first!")
      return
   resetAll()
   for card in me.hand:
      if card.Type != 'Identity': 
         whisper(":::Warning::: You are not supposed to have any non-Identity cards in your hand when you start the game")
         card.moveToBottom(me.piles['R&D/Stack'])
         continue
      else: 
         ds = card.Side
         storeSpecial(card)
         me.setGlobalVariable('ds', ds)
   if not ds: 
      confirm("You need to have your identity card in your hand when you try to setup the game. If you have it in your deck, please look for it and put it in your hand before running this function again")
      return
   if (ds == 'corp' and me.hasInvertedTable()) or (ds == 'runner' and not me.hasInvertedTable()):
      if not confirm(":::ERROR::: Due to engine limitations, the corp player must always be player [A] in order to properly utilize the board. Please start a new game and make sure you've set the corp to be player [A] in the lobby. Are you sure you want to continue?"): return   
   deckStatus = checkDeckNoLimit(deck)
   if not deckStatus[0]:
      if not confirm("We have found illegal cards in your deck. Bypass?"): return
      else: notify("{} has chosen to proceed with an illegal deck.".format(me))
   else: identity = deckStatus[1] # For code readability
   if ds == "corp":
      identity.moveToTable(125, 240)
      rnd(1,10) # Allow time for the ident to be recognised
      maxClicks = 3
      me.MU = 0
      notify("{} is the CEO of the {} Corporation".format(me,identity))
   else:
      identity.moveToTable(105, -345)
      rnd(1,10)  # Allow time for the ident to be recognised
      maxClicks = 4
      me.MU = 4
      BL = num(identity.Cost)
      me.counters['Base Link'].value = BL
      notify("{} is representing the Runner {}. They start with {} {}".format(me,identity,BL,uniLink()))
   createStartingCards()
   shuffle(me.piles['R&D/Stack'])
   notify("{}'s {} is shuffled ".format(me,pileName(me.piles['R&D/Stack'])))
   drawMany(me.piles['R&D/Stack'], 5)
   shuffle(me.piles['R&D/Stack']) # And another one just to be sure

def checkDeckNoLimit(group):
   if debugVerbosity >= 1: notify(">>> checkDeckNoLimit(){}".format(extraASDebug())) #Debug
   if not ds:
      whisper ("Choose a side first.")
      return 
   notify (" -> Checking deck of {} ...".format(me))
   ok = True
   if debugVerbosity >= 5: notify("### About to fetch identity card") #Debug
   identity = getSpecial('Identity')
   loDeckCount = len(group)
   if debugVerbosity >= 5: notify("### About to check identity min deck size.") #Debug
   if loDeckCount < num(identity.Requirement): # For identities, .Requirement is the card minimum they have.
      ok = False
      notify ( ":::ERROR::: Only {} cards in {}'s Deck. {} Needed!".format(loDeckCount,me,num(identity.Requirement)))
   mute()
   loAP = 0.0
   loInf = 0
   loRunner = False
   trash = me.piles['Heap/Archives(Face-up)']
   if debugVerbosity >= 5: notify("### About to moving cards into trash") #Debug
   for card in group: card.moveTo(trash)
   if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.               
   if debugVerbosity >= 5: notify("### About to check each card in the deck") #Debug
   for card in trash: 
      #if ok == False: continue # If we've already found illegal cards, no sense in checking anymore. Will activate this after checking
      if card.Type == 'Agenda': 
         if ds == 'corp': loAP += num(card.Stat)
         else: 
            notify(":::ERROR::: Agendas found in {}'s Stack.".format(me))
            ok = False
      elif card.Type in CorporationCardTypes and identity.Faction in RunnerFactions:
         notify(":::ERROR::: Corporate cards found in {}'s Stack.".format(me))
         ok = False
      elif card.Type in RunnerCardTypes and identity.Faction in CorporateFactions:
         notify(":::ERROR::: Runner cards found in {}'s R&Ds.".format(me))
         ok = False
      if card.Influence and card.Faction != identity.Faction: loInf += num(card.Influence)
      else:
         if card.Type == 'Identity': 
            notify(":::ERROR::: Extra Identity Cards found in {}'s {}.".format(me, pileName(group)))
            ok = False
         elif card.Faction != identity.Faction:   
            notify(":::ERROR::: Faction-restricted card ({}) found in {}'s {}.".format(card, me, pileName(group)))
            ok = False
   if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.               
   for card in trash: card.moveToBottom(group) # We use a second loop because we do not want to pause after each check
   if ds == 'corp' and loAP/loDeckCount < 2.0/5.0:
      notify(":::ERROR::: Only {} Agenda Points in {}'s R&D.".format(loAP/1,me))
      ok = False
   if loInf > num(identity.Stat):
      notify(":::ERROR::: Too much rival faction influence in {}'s R&D. {} found with a max of {}".format(me, loInf, num(identity.Stat)))
      ok = False
   if ok: notify("-> Deck of {} is OK!".format(me))
   if debugVerbosity >= 3: notify("<<< checkDeckNoLimit() with return: {},{}.".format(ok,identity)) #Debug
   return (ok,identity)

def createRemoteServer(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> createSDF(){}".format(extraASDebug())) #Debug
   Server = table.create("d59fc50c-c727-4b69-83eb-36c475d60dcb", x, y - (40 * playerside), 1, False)
   placeCard(Server,'install')
   
#------------------------------------------------------------------------------
# Run...
#------------------------------------------------------------------------------
def intRun(aCost = 1, Name = 'R&D', silent = False):
   if debugVerbosity >= 1: notify(">>> intRun(){}".format(extraASDebug())) #Debug
   if ds != 'runner':  
      whisper(":::ERROR:::Corporations can't run!")
      return 'ABORT'
   if getGlobalVariable('status') == 'running':
      whisper(":::ERROR:::You are already jacked-in. Please end the previous run (press [Esc]) before starting a new one")
      return
   CounterHold = getSpecial('Counter Hold') # Old code from Netrunner. Not sure if the new one will do stuff like that
   #if findMarker(CounterHold,'Fang') or findMarker(CounterHold,'Rex') or findMarker(CounterHold,'Fragmentation Storm'): # These are counters which prevent the runner from running.
   #   notify(":::Warning:::{} attempted to run but was prevented by a resident Sentry effect in their Rig. They will have to remove all such effects before attempting a run".format(me))
   #   return 'ABORT'
   ClickCost = useClick(count = aCost)
   if ClickCost == 'ABORT': return 'ABORT'
   if not silent: notify ("{} to start a run on {}.".format(ClickCost,Name))
   targetPL = ofwhom('-ofOpponent')
   BadPub = targetPL.counters['Bad Publicity'].value
   enemyIdent = getSpecial('Identity',targetPL)
   myIdent = getSpecial('Identity',me)
   if BadPub > 0:
         myIdent.markers[mdict['BadPublicity']] += BadPub
         notify("--> The Bad Publicity of {} allows {} to secure {} for this run".format(enemyIdent,myIdent,uniCredit(BadPub)))
   setGlobalVariable('status','running')
   atTimedEffects('Run')

def runHQ(group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> runHQ(){}".format(extraASDebug())) #Debug
   intRun(1, "HQ")

def runRD(group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> runRD(){}".format(extraASDebug())) #Debug
   intRun(1, "R&D")

def runArchives(group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> runArchives(){}".format(extraASDebug())) #Debug
   intRun(1, "the Archives")

def runServer(group, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> runSDF(){}".format(extraASDebug())) #Debug
   intRun(1, "a remote server")

def jackOut(group=table,x=0,y=0, silent = False):
   if debugVerbosity >= 1: notify(">>> jackOut()") #Debug
   opponent = ofwhom('-ofOpponent') # First we check if our opponent is a runner or a corp.
   if ds == 'corp': targetPL = opponent
   else: targetPL = me
   enemyIdent = getSpecial('Identity',targetPL)
   myIdent = getSpecial('Identity',me)
   if getGlobalVariable('status') != 'running': # If the runner is not running at the moment, do nothing
      if targetPL != me: whisper("{} is not running at the moment.".format(targetPL))
      else: whisper("You are not currently jacked-in.")
   else: # Else announce they are jacked in and resolve all post-run effects.
      setGlobalVariable('status','idle')
      myIdent.markers[mdict['BadPublicity']] = 0
      if not silent:
         if targetPL != me: notify("{} has kicked {} out of their corporate grid".format(myIdent,enemyIdent))
         else: notify("{} has jacked out of the run".format(myIdent))
      atTimedEffects('JackOut')
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
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   dummyCard = getSpecial('Tracing') # Just a random card to pass to the next function. Can't be bothered to modify the function to not need this.
   reduction = reduceCost(dummyCard, 'DelTag', 2)
   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))
   if payCost(2 - reduction) == "ABORT": 
      me.Clicks += 1 # If the player didn't notice they didn't have enough credits, we give them back their click
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   me.counters['Tags'].value -= 1
   notify ("{} and pays {}{} to lose a tag.".format(ClickCost,uniCredit(2 - reduction),extraText))

#------------------------------------------------------------------------------
# Markers
#------------------------------------------------------------------------------
def intAddCredits ( card, count):
   if debugVerbosity >= 1: notify(">>> intAddCredits(){}".format(extraASDebug())) #Debug
   mute()
   if ( count > 0):
      card.markers[mdict['Credits']] += count
      if ( card.isFaceUp == True): notify("{} adds {} from the bank on {}.".format(me,uniCredit(count),card))
      else: notify("{} adds {} on a card.".format(me,uniCredit(count)))

def addCredits(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addCredits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many Credits?", 1)
   if count == None: return
   intAddCredits(card, count)
	
def remCredits(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> remCredits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Credits?", 1)
   if count == None: return
   if count > card.markers[mdict['Credits']]: count = card.markers[mdict['Credits']]
   card.markers[mdict['Credits']] -= count
   if card.isFaceUp == True: notify("{} removes {} from {}.".format(me,uniCredit(count),card))
   else: notify("{} removes {} from a card.".format(me,uniCredit(count)))

def remXCredits (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> remCredits2BP(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Credits?", 1)
   if count == None: return
   if count > card.markers[mdict['Credits']]: count = card.markers[mdict['Credits']]
   card.markers[mdict['Credits']] -= count
   me.counters['Credits'].value += count 
   if card.isFaceUp == True: notify("{} removes {} from {} to their Credit Pool.".format(me,uniCredit(count),card))
   else: notify("{} takes {} from a card to their Credit Pool.".format(me,uniCredit(count)))

def addPlusOne(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addPlusOne(){}".format(extraASDebug())) #Debug
   mute()
   if MinusOne in card.markers:
      card.markers[mdict['MinusOne']] -= 1
   else: 
      card.markers[mdict['PlusOne']] += 1
   notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> addMinusOne(){}".format(extraASDebug())) #Debug
   mute()
   if PlusOne in card.markers:
      card.markers[mdict['PlusOne']] -= 1
   else:
      card.markers[mdict['MinusOne']] += 1
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
# Advancing cards
#------------------------------------------------------------------------------
def advanceCardP(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> advanceCardP(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   reduction = reduceCost(card, 'Advancement', 1)
   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))
   if payCost(1 - reduction) == "ABORT": 
      me.Clicks += 1 # If the player didn't notice they didn't have enough credits, we give them back their click
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   card.markers[mdict['Advancement']] += 1
   if card.isFaceUp: notify("{} and paid {}{} to advance {}.".format(ClickCost,uniCredit(1 - reduction),extraText,card))
   else: notify("{} and paid {}{} to advance a card.".format(ClickCost,uniCredit(1 - reduction),extraText))

def addXadvancementCounter(card, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> addXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many counters?", 1)
   if count == None: return
   card.markers[mdict['Advancement']] += count
   if card.isFaceUp == True: notify("{} adds {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> delXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many counters?", 1)
   if count == None: return
   if count > card.markers[mdict['Advancement']]: count = card.markers[mdict['Advancement']]
   card.markers[mdict['Advancement']] -= count
   if card.isFaceUp == True: notify("{} removes {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def advanceCardM(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> advanceCardM(){}".format(extraASDebug())) #Debug
   mute()
   card.markers[mdict['Advancement']] -= 1
   if (card.isFaceUp == True): notify("{} removes 1 advancement counter on {}.".format(me,card))
   else: notify("{} removes 1 advancement counter on a card.".format(me))

#---------------------
# Tracing...
#----------------------

def inputTraceValue (card, x=0,y=0, limit = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> inputTraceValue(){}".format(extraASDebug())) #Debug
   mute()
   limitText = ''
   card = getSpecial('Tracing')   
   limit = num(limit) # Just in case
   if debugVerbosity >= 2: notify("### Trace Limit: {}".format(limit))
   if limit > 0: limitText = '\n\n(Max Trace Power: {})'.format(limit)
   if ds == 'corp': traceTXT = 'Trace'
   else: traceTXT = 'Link'
   TraceValue = askInteger("Increase {} Strentgh by how much?{}".format(traceTXT,limitText), 0)
   if TraceValue == None: 
      whisper(":::Warning::: Trace attempt aborted by player.")
      return 'ABORT'
   while limit > 0 and TraceValue > limit:
      TraceValue = askInteger("Please increase by equal to or less than the max trace power!\nIncrease Trace power by how much?{}".format(limitText), 0)
      if TraceValue == None: 
         whisper(":::Warning::: Trace attempt aborted by player.")
         return 'ABORT'
   while TraceValue > me.Credits and not confirm("You do not have enough bits to increase your Trace Strength by this amount. Continue anyway?"):
      TraceValue = askInteger("Increase {} Strength by how much?{}".format(traceTXT, limitText), 0)
      if TraceValue == None: 
         whisper(":::Warning::: Trace attempt aborted by player.")
         return 'ABORT'
   card.markers[mdict['Credits']] = TraceValue
   if not silent: 
      if ds == 'corp': notify("{} strengthens their Trace by {}.".format(me,TraceValue))
      else: notify("{} reinforces their {} by {}.".format(me,uniLink(),TraceValue))
	
#def revealTraceValue (card, x=0,y=0): # Obsolete in ANR
#   if debugVerbosity >= 1: notify(">>> revealTraceValue(){}".format(extraASDebug())) #Debug
#   mute()
#   global TraceValue
#   card = getSpecial('Tracing')
#   card.isFaceUp = True
#   card.markers[mdict['Credits']] = TraceValue
#   notify ( "{} reveals a Trace Value of {}.".format(me,TraceValue))
#   if TraceValue == 0: autoscriptOtherPlayers('clearTraceAttempt') # if the trace value is 0, then we consider the trace attempt as valid, so we call scripts triggering from that.
#   TraceValue = 0

def payTraceValue (card, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> payTraceValue(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   card = getSpecial('Tracing')
   reduction = reduceCost(card, 'Trace', card.markers[mdict['Credits']])
   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))
   if payCost(card.markers[mdict['Credits']] - reduction)  == 'ABORT': return
   notify ("{} pays the {}{} they used during this trace attempt.".format(me,uniCredit(card.markers[mdict['Credits']]),extraText))
   card.markers[mdict['Credits']] = 0
   autoscriptOtherPlayers('TraceAttempt',card)

def cancelTrace ( card, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> cancelTrace(){}".format(extraASDebug())) #Debug
   mute()
   TraceValue = 0
   card.markers[mdict['Credits']] = 0
   notify ("{} cancels the Trace.".format(me) )

#------------------------------------------------------------------------------
# Counter & Damage Functions
#-----------------------------------------------------------------------------

def payCost(count = 1, cost = 'not_free', counter = 'BP'): # A function that removed the cost provided from our credit pool, after checking that we have enough.
   if debugVerbosity >= 1: notify(">>> payCost(){}".format(extraASDebug())) #Debug
   if cost == 'free': return 'free'
   count = num(count)
   if count <= 0 : return 0# If the card has 0 cost, there's nothing to do.
   if counter == 'BP':
      if me.counters['Credits'].value < count and not confirm("You do not seem to have enough Credits in your pool to take this action. Are you sure you want to proceed? \
         \n(If you do, your Credit Pool will go to the negative. You will need to increase it manually as required.)"): return 'ABORT' # If we don't have enough Credits in the pool, we assume card effects or mistake and notify the player that they need to do things manually.
      me.counters['Credits'].value -= count
   elif counter == 'AP': # We can also take costs from other counters with this action.
      if me.counters['Agenda Points'].value < count and not confirm("You do not seem to have enough Agenda Points to take this action. Are you sure you want to proceed? \
         \n(If you do, your Agenda Points will go to the negative. You will need to increase them manually as required.)"): return 'ABORT'
      me.counters['Agenda Points'].value -= count
   return uniCredit(count)

def reduceCost(card, type = 'Rez', fullCost = 0):
   if debugVerbosity >= 1: notify(">>> reduceCost(). Action is: {}".format(type)) #Debug
   if fullCost == 0: return 0 # If there's no cost, there's no use checking the table.
   reduction = 0
   status = getGlobalVariable('status')
   ### First we check if the card has an innate reduction. 
   Autoscripts = Stored_AutoScripts[card].split('||') 
   if len(Autoscripts): 
      for autoS in Autoscripts:
         if not re.search(r'onPay', autoS): 
            if debugVerbosity >= 2: notify("### No onPay trigger found in {}!".format(autoS))         
            continue
         reductionSearch = re.search(r'Reduce([0-9]+)Cost({}|All)'.format(type), autoS)
         if debugVerbosity >= 2: #Debug
            if reductionSearch: notify("!!! self-reduce regex groups: {}".format(reductionSearch.groups()))
            else: notify("!!! No self-reduce regex Match!")
         oppponent = ofwhom('-ofOpponent')
         if re.search(r'ifNoisyOpponent', autoS) and oppponent.getGlobalVariable('wasNoisy') != '1': 
            if debugVerbosity >= 2: notify("### No required noisy bit found!")
            continue
         reduction += num(reductionSearch.group(1))
         fullCost -= 1
   elif debugVerbosity >= 2: notify("### No self-reducing autoscripts found!")
   ### Now we check if we're in a run and we have bad publicity credits to spend
   if status == 'running':
      myIdent = getSpecial('Identity',me)
      while fullCost > 0 and myIdent.markers[mdict['BadPublicity']] and myIdent.markers[mdict['BadPublicity']] > 0: 
         reduction += 1
         fullCost -= 1
         myIdent.markers[mdict['BadPublicity']] -= 1
         if fullCost == 0: break      
   ### Finally we go through the table and see if there's any cards providing cost reduction
   for c in table: # Then check if there's other cards in the table that reduce its costs.
      Autoscripts = c.AutoScript.split('||')
      if len(Autoscripts) == 0: continue
      for autoS in Autoscripts:
         if re.search(r'whileRunning', autoS) and status != 'running': continue # if the reduction is only during runs, and we're not in a run, bypass this effect
         if debugVerbosity >= 2: notify("### Checking {} with AS: {}".format(c, autoS)) #Debug
         reductionSearch = re.search(r'Reduce([0-9#]+)Cost({}|All)-for([A-Z][A-Za-z ]+)(-not[A-Za-z_& ]+)?'.format(type), autoS) 
         if debugVerbosity >= 2: #Debug
            if reductionSearch: notify("!!! Regex is {}".format(reductionSearch.groups()))
            else: notify("!!! No reduceCost regex Match!") 
         if re.search(r'excludeDummy', autoS) and c.highlight == DummyColor: continue 
         if c.controller == me and reductionSearch and c.isFaceUp: # If the above search matches (i.e. we have a card with reduction for Rez and a condition we continue to check if our card matches the condition)
            if debugVerbosity >= 3: notify("### Possible Match found in {}".format(c)) # Debug         
            if reductionSearch.group(4): 
               exclusion = re.search(r'-not([A-Za-z_& ]+)'.format(type), reductionSearch.group(4))
               if exclusion and (re.search(r'{}'.format(exclusion.group(1)), Stored_Type[card]) or re.search(r'{}'.format(exclusion.group(1)), Stored_Keywords[card])): continue
            if reductionSearch.group(3) == 'All' or re.search(r'{}'.format(reductionSearch.group(3)), Stored_Type[card]) or re.search(r'{}'.format(reductionSearch.group(3)), Stored_Keywords[card]): #Looking for the type of card being reduced into the properties of the card we're currently paying.
               if debugVerbosity >= 2: notify(" ### Search match! Group is {}".format(reductionSearch.group(1))) # Debug
               if re.search(r'onlyOnce',autoS) and oncePerTurn(c, silent = True, act = 'automatic') == 'ABORT': continue # if the card's effect has already been used, check the next one
               if reductionSearch.group(1) != '#':
                  reduction += num(reductionSearch.group(1)) # if there is a match, the total reduction for this card's cost is increased.
               else: 
                  while fullCost > 0 and c.markers[mdict['Credits']] > 0: 
                     reduction += 1
                     fullCost -= 1
                     c.markers[mdict['Credits']] -= 1
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
      else: card.moveTo(me.piles['Heap/Archives(Face-up)'])
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
      
def getCredit(group, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> getCredit(){}".format(extraASDebug())) #Debug
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   creditsReduce = findCounterPrevention(1, 'Credits', me)
   if creditsReduce: extraTXT = " ({} forfeited)".format(uniCredit(creditsReduce))
   else: extraTXT = ''
   notify ("{} and receives {}{}.".format(ClickCost,uniCredit(1 - creditsReduce),extraTXT))
   me.counters['Credits'].value += 1 - creditsReduce

def findDMGProtection(DMGdone, DMGtype, targetPL): # Find out if the player has any card preventing damage
   if debugVerbosity >= 1: notify(">>> findDMGProtection(){}".format(extraASDebug())) #Debug
   if not Automations['Damage Prevention']: return 0
   protectionFound = 0
   protectionType = 'protection{}DMG'.format(DMGtype) # This is the string key that we use in the mdict{} dictionary
   carsList = sortPriority([c for c in table
               if c.controller == targetPL
               and c.markers])
   for card in carsList: # First we check for complete damage protection (i.e. protection from all types), which is always temporary.
      if card.markers[mdict['protectionAllDMG']]:
         while DMGdone > 0 and card.markers[mdict['protectionAllDMG']] > 0: 
            protectionFound += 1 
            DMGdone -= 1
            card.markers[mdict['protectionAllDMG']] -= 1 
         if DMGdone == 0: break
   for card in carsList:
      if card.markers[mdict[protectionType]]:
         while DMGdone > 0 and card.markers[mdict[protectionType]] > 0: # For each point of damage we do.
            protectionFound += 1 # We increase the protection found by 1
            DMGdone -= 1 # We reduce how much damage we still need to prevent by 1
            card.markers[mdict[protectionType]] -= 1 # We reduce the card's damage protection counters by 1
         if DMGdone == 0: break # If we've found enough protection to alleviate all damage, stop the search.
   if DMGtype == 'Net' or DMGtype == 'Brain': altprotectionType = 'protectionNetBrainDMG' # To check for the combined Net & Brain protection counter as well.
   else: altprotectionType = None
   for card in carsList: # We check for the combined protections after we use the single protectors.
      if altprotectionType and card.markers[mdict[altprotectionType]]:
         while DMGdone > 0 and card.markers[mdict[altprotectionType]] > 0: 
            protectionFound += 1 #
            DMGdone -= 1 
            card.markers[mdict[altprotectionType]] -= 1 
         if DMGdone == 0: break 
   if debugVerbosity >= 3: notify("<<< findDMGProtection() by returning: {}".format(protectionFound))
   return protectionFound

def findEnhancements(Autoscript): #Find out if the player has any cards increasing damage dealt.
   if debugVerbosity >= 1: notify(">>> findEnhancements(){}".format(extraASDebug())) #Debug
   enhancer = 0
   DMGtype = re.search(r'\bInflict[0-9]+(Meat|Net|Brain)Damage', Autoscript)
   if DMGtype:
      enhancerMarker = 'enhanceDamage:{}'.format(DMGtype.group(1))
      if debugVerbosity >= 3: notify('#### encancerMarker: {}'.format(enhancerMarker))
      for card in table:
         if debugVerbosity >= 2: notify("### Checking {}".format(card)) #Debug
         cardENH = re.search(r'Enhance([0-9]+){}Damage'.format(DMGtype.group(1)), card.AutoScript)
         if card.controller == me and card.isFaceUp and cardENH: enhancer += num(cardENH.group(1))
         if card.controller == me and card.isFaceUp:
            foundMarker = findMarker(card, enhancerMarker)
            if foundMarker: 
               enhancer += card.markers[foundMarker]
               card.markers[foundMarker] = 0
   if debugVerbosity >= 3: notify("<<< findEnhancements() by returning: {}".format(enhancer))
   return enhancer

def findVirusProtection(card, targetPL, VirusInfected): # Find out if the player has any virus preventing counters.
   if debugVerbosity >= 1: notify(">>> findVirusProtection(){}".format(extraASDebug())) #Debug
   protectionFound = 0
   if card.markers[mdict['protectionVirus']]:
      while VirusInfected > 0 and card.markers[mdict['protectionVirus']] > 0: # For each virus infected...
         protectionFound += 1 # We increase the protection found by 1
         VirusInfected -= 1 # We reduce how much viruses we still need to prevent by 1
         card.markers[mdict['protectionVirus']] -= 1 # We reduce the card's virus protection counters by 1
   if debugVerbosity >= 3: notify("<<< findVirusProtection() by returning: {}".format(protectionFound))
   return protectionFound

def findCounterPrevention(count, counter, targetPL): # Find out if the player has any markers preventing them form gaining specific counters (Credits, Agenda Points etc)
   if debugVerbosity >= 1: notify(">>> findCounterPrevention(){}".format(extraASDebug())) #Debug
   preventionFound = 0
   forfeit = None
   preventionType = 'preventCounter:{}'.format(counter)
   forfeitType = 'forfeitCounter:{}'.format(counter)
   cardList = [c for c in table
               if c.controller == targetPL
               and c.markers]
   for card in sortPriority(cardList):
      foundMarker = findMarker(card, preventionType)
      if not foundMarker: foundMarker = findMarker(card, forfeitType)
      if foundMarker: # If we found a counter prevention marker of the specific type we're looking for...
         while count > 0 and card.markers[foundMarker] > 0: # For each point of damage we do.
            preventionFound += 1 # We increase the prevention found by 1
            count -= 1 # We reduce how much counter we still need to add by 1
            card.markers[foundMarker] -= 1 # We reduce the specific counter prevention counters by 1
         if count == 0: break # If we've found enough protection to alleviate all counters, stop the search.
   if debugVerbosity >= 3: notify("<<< findCounterPrevention() by returning: {}".format(preventionFound))
   return preventionFound   
#------------------------------------------------------------------------------
# Card Actions
#------------------------------------------------------------------------------
   
def scrAgenda(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> scrAgenda(){}".format(extraASDebug())) #Debug
   global scoredAgendas
   mute()
   cheapAgenda = False
   storeProperties(card)
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
   if ds == 'runner': agendaTxt = "liberate"
   else: agendaTxt = "score"
   if Stored_Type[card] == "Agenda":
      if ds == 'corp' and card.markers[mdict['Advancement']] < num(Stored_Cost[card]):
         if confirm("You have not advanced this agenda enough to score it. Bypass?"): 
            cheapAgenda = True
            currentAdv = card.markers[mdict['Advancement']]
         else: return
      elif not confirm("Do you want to {} agenda {}?".format(agendaTxt,card.name)): return
      card.isFaceUp = True
      if agendaTxt == 'score' and chkTargeting(card) == 'ABORT': 
         card.isFaceUp = False
         notify("{} cancels their action".format(me))
         return
      ap = num(fetchProperty(card,'Stat'))
      card.markers[mdict['Scored']] += 1
      apReduce = findCounterPrevention(ap, 'Agenda Points', me)
      if apReduce: extraTXT = " ({} forfeited)".format(apReduce)
      else: extraTXT = ''
      if debugVerbosity >= 2: notify("### About to Score")
      me.counters['Agenda Points'].value += ap - apReduce
      if ds == 'corp': card.moveToTable(495 + (scoredAgendas * 15), 8, False) # Location of the Agenda Scoring point for the Corp.
      else: card.moveToTable(336 + (scoredAgendas * 15), -206, False) # Location of the Agenda Scoring point for the Runner.
      scoredAgendas += 1
      notify("{} {}s {} and receives {} agenda point(s){}".format(me, agendaTxt, card, ap - apReduce,extraTXT))
      if cheapAgenda: notify(":::Warning:::{} did not have enough advance tokens ({} out of {})! ".format(card,currentAdv,card.Cost))
      executePlayScripts(card,agendaTxt)
      autoscriptOtherPlayers('Agenda'+agendaTxt.capitalize()+'d',card) # The autoscripts triggered by this effect are using AgendaLiberated and AgendaScored as the hook
      if me.counters['Agenda Points'].value >= 7 : notify("{} wins the game!".format(me))
      card.highlight = None # In case the card was highlighted as revealed, we remove that now.
      card.markers[mdict['Advancement']] = 0 # We only want to clear the advance counters after the automations, as they may still be used.
   else:
      whisper ("You can't score this card")

def scrTargetAgenda(group = table, x = 0, y = 0):
   cardList = [c for c in table if c.targetedBy and c.targetedBy == me]
   for card in cardList:
      storeProperties(card)
      if Stored_Type[card] == 'Agenda':
         if card.markers[mdict['Scored']] and card.markers[mdict['Scored']] > 0: whisper(":::ERROR::: This agenda has already been scored")
         else:
            scrAgenda(card)
            return
   notify("You need to target an unscored agenda in order to use this action")
         
def RDaccessX(group = table, x = 0, y = 0): # A function which looks at the top X cards of the corp's deck and then asks the runner what to do with each one.
   if debugVerbosity >= 1: notify(">>> RDaccessX(){}".format(extraASDebug())) #Debug
   mute()
   RDtop = []
   removedCards = 0
   if ds == 'corp': 
      whisper("This action is only for the use of the runner. Use the 'Look at top X cards' function on your R&D's context manu to access your own deck")
      return
   count = askInteger("How many cards are you accessing from the corporation's R&D?",1)
   if count == None: return
   targetPL = ofwhom('-ofOpponent')
   if debugVerbosity >= 3: notify("### Found opponent. Storing the top {} as a list".format(count)) #Debug
   RDtop = list(targetPL.piles['R&D/Stack'].top(count))
   if len(RDtop) == 0: 
      whisper("Corp's R&D is empty. You cannot take this action")
      return
   if debugVerbosity >= 4:
      for card in RDtop: notify("#### Card: {}".format(card))
   notify("{} is accessing the top {} cards of {}'s R&D".format(me,count,targetPL))
   cover = table.create("ac3a3d5d-7e3a-4742-b9b2-7f72596d9c1b",0,0,1,True) # Creating a dummy card to cover that player's archives in case they're empty
   cover.moveTo(targetPL.piles['Heap/Archives(Face-up)']) # Moving that dummy card on top of their archives
   for iter in range(len(RDtop)):
      if debugVerbosity >= 3: notify("### Moving card {}".format(iter)) #Debug
      RDtop[iter].moveToBottom(targetPL.piles['Heap/Archives(Face-up)'])
      if debugVerbosity >= 4: notify("#### Looping...")
      loopChk(RDtop[iter],'Type')
      if re.search(r'onAccess:Reveal',RDtop[iter].AutoScript):
         RDtop[iter].moveToTable(0, 0 + yaxisMove(RDtop[iter]), False)
         RDtop[iter].highlight = RevealedColor         
         confirm("Ambush! You have stumbled into a {}\
                \n(This card activates even on access from R&D.)\
              \n\nYour blunder has already triggered the alarms. Please wait until corporate OpSec has decided whether to use its effects or not, before pressing any button\
                  ".format(RDtop[iter].name))
      if debugVerbosity >= 4: notify("#### Storing...")
      storeProperties(RDtop[iter]) # Otherwise trying to trash the card will crash because of reduceCost()
      cType = RDtop[iter].Type
      cKeywords = RDtop[iter].Keywords
      cStat = RDtop[iter].Stat
      cCost = RDtop[iter].Cost
      cName = RDtop[iter].name
      cRules = RDtop[iter].Rules
      if debugVerbosity >= 4: notify("#### Finished Storing. About to move back...")
      RDtop[iter].moveTo(targetPL.piles['R&D/Stack'],iter - removedCards)
      if debugVerbosity >= 3: notify("### Stored properties. Checking type...") #Debug
      if cType == 'Agenda' or cType == 'Asset' or cType == 'Upgrade':
         if cType == 'Agenda': action1TXT = 'Liberate for {} Agenda Points'.format(cStat)
         else: action1TXT = 'Pay {} to Trash'.format(cStat)
         choice = 0
         while choice < 1 or choice > 3:
            choice = askInteger("Card {}: {}\
                               \nType: {}\
                               \nKeywords: {}\
                               \nCost: {}\
                             \n\nCard Text: {}\
                             \n\nWhat do you want to do with this card?\
                               \n   1: Leave where it is.\
                               \n   2: Force trash at no cost.\
                               \n   3: {}\
                             ".format(iter+1,cName,cType,cKeywords,cCost,cRules,action1TXT),3)
            if choice == None: choice = 1
      else:                    
         choice = 0
         while choice < 1 or choice > 2:
            choice = askInteger("Card {}: {}\
                               \nType: {}\
                               \nKeywords: {}\
                               \nCost: {}\
                             \n\nCard Text: {}\
                             \n\nWhat do you want to do with this card?\
                               \n   1: Leave where it is.\
                               \n   2: Force trash at no cost.\
                             ".format(iter+1,cName,cType,cKeywords,cCost,cRules),1)
            if choice == None: choice = 1
      if choice == 2: 
         RDtop[iter].moveTo(targetPL.piles['Heap/Archives(Face-up)'])
         loopChk(RDtop[iter],'Type')
         notify("{} {} {} at no cost".format(me,uniTrash(),RDtop[iter]))
         removedCards += 1
      elif choice == 3:
         if cType == 'Agenda':
            RDtop[iter].moveToTable(0,0)
            RDtop[iter].highlight = RevealedColor
            scrAgenda(RDtop[iter])
            removedCards += 1
         else: 
            reduction = reduceCost(RDtop[iter], 'Trash', num(cStat))
            rc = payCost(num(cStat) - reduction, "not free")
            if rc == "ABORT": continue # If the player couldn't pay to trash the card, we leave it where it is.
            RDtop[iter].moveTo(targetPL.piles['Heap/Archives(Face-up)'])
            loopChk(RDtop[iter],'Type')
            notify("{} paid {} to {} {}".format(me,uniCredit(cStat),uniTrash(),RDtop[iter]))            
      else: continue
   cover.moveTo(shared.exile) # now putting the cover card to the exile deck that nobody looks at.
   notify("{} has accessing {}'s R&D".format(me,targetPL))

def ARCscore(group, x=0,y=0):
   mute()
   if debugVerbosity >= 1: notify(">>> ARCscore(){}".format(extraASDebug())) #Debug
   removedCards = 0
   ARCHcards = []
   if ds == 'corp': 
      whisper("This action is only for the use of the runner.")
      return
   targetPL = ofwhom('-ofOpponent')
   if debugVerbosity >= 3: notify("### Found opponent.") #Debug
   ARC = targetPL.piles['Heap/Archives(Face-up)']
   for card in targetPL.piles['Archives(Hidden)']: card.moveTo(ARC) # When the runner accesses the archives, all  cards of the face up archives.
   if len(ARC) == 0: 
      whisper("Corp's Archives are empty. You cannot take this action")
      return
   rnd(10,100) # A small pause
   for card in ARC:
      if debugVerbosity >= 3: notify("### Checking: {}.".format(card)) #Debug
      if card.Type == 'Agenda':
         card.moveToTable(0,0)
         card.highlight = RevealedColor
         scrAgenda(card)
         if card.highlight == RevealedColor: card.moveTo(ARC) # If the runner opted not to score the agenda, put it back into the deck.
      
def isRezzable (card):
   if debugVerbosity >= 1: notify(">>> isRezzable(){}".format(extraASDebug())) #Debug
   mute()
   Type = Stored_Type[card]
   if Type == "ICE" or Type == "Asset" or Type == "Upgrade": return True
   else: return False

def intRez (card, cost = 'not free', x=0, y=0, silent = False):
   if debugVerbosity >= 1: notify(">>> intRez(){}".format(extraASDebug())) #Debug
   mute()
   extraText = ''
   rc = ''
   storeProperties(card)
   if card.isFaceUp: 
      whisper("you can't rez a rezzed card")
      return 'ABORT'
   if not isRezzable(card): 
      whisper("Not a rezzable card")
      return 'ABORT'
   if chkTargeting(card) == 'ABORT': 
      notify("{} cancels their action".format(me))
      return
   reduction = reduceCost(card, 'Rez', num(Stored_Cost[card]))
   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))
   rc = payCost(num(Stored_Cost[card]) - reduction, cost)
   if rc == "ABORT": return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == "free": extraText = " at no cost"
   elif rc != 0: rc = "for {}".format(rc)
   else: rc = ''
   card.isFaceUp = True
   if not silent:
      if card.Type == 'ICE': notify("{} has rezzed {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Asset': notify("{} has acquired {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Upgrade': notify("{} has installed {} {}{}.".format(me, card, rc, extraText))
   random = rnd(10,100) # Bug workaround.
   executePlayScripts(card,'rez')
    
def rezForFree (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rezForFree(){}".format(extraASDebug())) #Debug
   intRez(card, "free")

def derez(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> derez(){}".format(extraASDebug())) #Debug
   mute()
   storeProperties(card)
   if card.isFaceUp:
      if not isRezzable(card): 
         whisper ("Not a rezzable card")
         return 'ABORT'
      else:
         if not silent: notify("{} derezzed {}".format(me, card))
         card.markers[mdict['Credits']] = 0
         card.isFaceUp = False
         executePlayScripts(card,'derez')
   else:
      notify ( "you can't derez a unrezzed card")
      return 'ABORT'
      
def expose(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> expose(){}".format(extraASDebug())) #Debug
   if not card.isFaceUp:
      mute()
      if card.controller != me and confirm(":::WARNING:::Confirm:::\nYou are about to expose an opponent's card.\
                                            Do they have any reactions to this expose attempt?"): return 'ABORT'
      card.isFaceUp = True
      if card.highlight == None: card.highlight = RevealedColor # we don't want to accidentally wipe dummy card highlight.
      if not silent: notify("{} exposed {}".format(me, card))
   else:
      card.isFaceUp = False
      if card.highlight == RevealedColor: card.highlight = None
      if not silent: notify("{} hides {} once more again".format(me, card))

def rolld6(group = table, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> rolld6(){}".format(extraASDebug())) #Debug
   mute()
   n = rnd(1, 6)
   if not silent: notify("{} rolls {} on a 6-sided die.".format(me, n))
   return n

def selectAsTarget (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> selectAsTarget(){}".format(extraASDebug())) #Debug
   card.target(True)

def clear(card, x = 0, y = 0, silent = False):
   if debugVerbosity >= 1: notify(">>> clear() card: {}".format(card)) #Debug
   mute()
   if not silent: notify("{} clears {}.".format(me, card))
   if card.highlight != DummyColor or card.highlight != RevealedColor or card.highlight != InactiveColor :card.highlight = None
   card.markers[mdict['BaseLink']] = 0
   card.markers[mdict['PlusOne']] = 0
   card.markers[mdict['MinusOne']] = 0
   card.target(False)
   if debugVerbosity >= 3: notify("<<< clear()")
   
def clearAll(): # Just clears all the player's cards.
   if debugVerbosity >= 1: notify(">>> clearAll()") #Debug
   for card in table:
      if card.controller == me: clear(card,silent = True)
   if debugVerbosity >= 3: notify("<<< clearAll()")
   
def intTrashCard(card, stat, cost = "not free",  ClickCost = '', silent = False):
   if debugVerbosity >= 1: notify(">>> intTrashCard(){}".format(extraASDebug())) #Debug
   global trashEasterEggIDX, DummyTrashWarn
   mute()
   MUtext = ""
   rc = ''
   extraText = ''
   storeProperties(card)
   if ClickCost == '': 
      ClickCost = '{} '.format(me) # If not clicks were used, then just announce our name.
      goodGrammar = 'es' # LOL Grammar Nazi
   else: 
      ClickCost += ' and '
      goodGrammar = ''
   if UniCode: goodGrammar = ''
   cardowner = card.owner
   if Stored_Type[card] == "Tracing" or Stored_Type[card] == "Counter Hold" or Stored_Type[card] == "Server": 
      whisper("{}".format(trashEasterEgg[trashEasterEggIDX]))
      if trashEasterEggIDX < 7:
         trashEasterEggIDX += 1
         return 'ABORT'
      elif trashEasterEggIDX == 7: 
         card.moveToBottom(cardowner.piles['Heap/Archives(Face-up)'])
         trashEasterEggIDX = 0
         return
   if card.highlight == DummyColor and DummyTrashWarn and not silent and not confirm(":::Warning!:::\n\nYou are about to trash a dummy card. You will not be able to restore it without using the effect that created it originally.\n\nAre you sure you want to proceed? (This message will not appear again)"): 
      DummyTrashWarn = False
      return
   else: DummyTrashWarn = False
   reduction = reduceCost(card, 'Trash', num(stat)) # So as not to waste time.
   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))    
   rc = payCost(num(stat) - reduction, cost)
   if rc == "ABORT": return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == 0: 
      if ClickCost.endswith(' and'): ClickCost[:-len(' and')] # if we have no click cost, we don't need the connection.
   else: 
      ClickCost += "pays {} to".format(rc) # If we have Credit cost, append it to the Click cost to be announced.
      goodGrammar = ''
   if Stored_Type[card] == 'Event' or Stored_Type[card] == 'Operation': silent = True # These cards are already announced when played. No need to mention them a second time.
   if card.isFaceUp:
      MUtext = chkRAM(card, 'uninstall')    
      if rc == "free" and not silent: notify("{} {} {} at no cost{}.".format(me, uniTrash(), card, MUtext))
      elif not silent: notify("{} {}{} {}{}{}.".format(ClickCost, uniTrash(), goodGrammar, card, extraText, MUtext))
      if card.Type == 'Agenda' and card.markers[mdict['Scored']]: 
         me.counters['Agenda Points'].value -= num(card.Stat) # Trashing Agendas for any reason, now takes they value away as well.
         notify("--> {} loses {} Agenda Points".format(me, card.Stat))
      if card.highlight != RevealedColor: executePlayScripts(card,'trash') # We don't want to run automations on simply revealed cards.
      card.moveTo(cardowner.piles['Heap/Archives(Face-up)'])
   elif (ds == "runner" and card.controller == me) or (ds == "runner" and card.controller != me and cost == "not free") or (ds == "corp" and card.controller != me ): 
   #I'm the runner and I trash my cards, or an accessed card from the corp, or I 'm the corp and I trash a runner's card.
      card.moveTo(cardowner.piles['Heap/Archives(Face-up)'])
      if rc == "free" and not silent: notify ("{} {} {} at no cost.".format(me, uniTrash(), card))
      elif not silent: notify("{} {}{} {}{}.".format(ClickCost, uniTrash() , goodGrammar, card, extraText))
   else: #I'm the corp and I trash my own hidden cards or the runner and trash a hidden corp card without cost (e.g. randomly picking one from their hand)
      card.moveTo(cardowner.piles['Archives(Hidden)'])
      if rc == "free" and not silent: notify("{} {} a hidden card at no cost.".format(me, uniTrash()))
      elif not silent: notify("{} {}{} a hidden card.".format(ClickCost, uniTrash(), goodGrammar))
   if debugVerbosity >= 3: notify("<<< intTrashCard()")

def trashCard (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> trashCard(){}".format(extraASDebug())) #Debug
   if card.highlight == DummyColor: intTrashCard(card, card.Stat, "free") # lingering effects don't require cost to trash.
   else: intTrashCard(card, card.Stat)
        
def trashForFree (card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> trashForFree(){}".format(extraASDebug())) #Debug
   intTrashCard(card, card.Stat, "free")

def pay2AndTrash(card, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> pay2AndTrash(){}".format(extraASDebug())) #Debug
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   intTrashCard(card, 2, ClickCost = ClickCost)

def trashTargetFree(group, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> trashTargetFree(){}".format(extraASDebug())) #Debug
   targetCards = [c for c in table
                 if c.targetedBy
                 and c.targetedBy == me]
   if len(targetCards) == 0: return
   if not confirm("You are about to trash your opponent's cards. This may cause issue if your opponent is currently manipulating them\
             \nPlease ask your opponent to wait until the notification appears before doing anything else\
           \n\n:::Warning:::Confirm:::Also confirm that your opponent does not have any reaction to you trashing one his cards\
           \n\nProceed?"): return
   for card in targetCards: 
      storeProperties(card)
      intTrashCard(card, fetchProperty(card, 'Stat'), "free")

def trashTargetPaid(group, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> trashTargetFree(){}".format(extraASDebug())) #Debug
   targetCards = [c for c in table
                 if c.targetedBy
                 and c.targetedBy == me]
   if len(targetCards) == 0: return
   if not confirm("You are about to trash your opponent's cards. This may cause issue if your opponent is currently manipulating them\
             \nPlease ask your opponent to wait until the notification appears before doing anything else\
           \n\nProceed?"): return
   for card in targetCards:
      storeProperties(card)
      if ds == 'corp':
         if Stored_Type[card] == 'Resource':
            ClickCost = useClick()
            if not card.controller.Tags:
               whisper("You can only {} the runner's resources when they're tagged".format(uniTrash()))
               continue
            if ClickCost == 'ABORT': return
            intTrashCard(card, 2, ClickCost = ClickCost)
         else: whisper("Only resources can be trashed from the runner")
      else: 
         if Stored_Type[card] == 'Upgrade' or Stored_Type[card] == 'Asset':
            intTrashCard(card, fetchProperty(card, 'Stat')) # If we're a runner, trash with the cost of the card's trash.
         else: whisper("You can only pay to trash the Corp's Nodes and Upgrades".format(uniTrash()))
      
def exileCard(card, silent = False):
   if debugVerbosity >= 1: notify(">>> exileCard(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the shared pile and outside of view.
   mute()
   storeProperties(card)
   if Stored_Type[card] == "Tracing" or Stored_Type[card] == "Counter Hold" or Stored_Type[card] == "Server": 
      whisper("This kind of card cannot be exiled!")
      return 'ABORT'
   else:
      if card.isFaceUp: MUtext = chkRAM(card, 'uninstall')
      else: MUtext = ''
      executePlayScripts(card,'trash')
      card.moveTo(shared.exile)
   if not silent: notify("{} exiled {}{}.".format(me,card,MUtext))
   
   
def uninstall(card, x=0, y=0, destination = 'hand', silent = False):
   if debugVerbosity >= 1: notify(">>> uninstall(){}".format(extraASDebug())) #Debug
   # Returns an installed card into our hand.
   mute()
   storeProperties(card)
   if destination == 'R&D' or destination == 'Stack': group = me.piles['R&D/Stack']
   else: group = card.owner.hand
   #confirm("destination: {}".format(destination)) # Debug
   if Stored_Type[card] == "Tracing" or Stored_Type[card] == "Counter Hold" or Stored_Type[card] == "Server": 
      whisper("This kind of card cannot be uninstalled!")
      return 'ABORT'
   else: 
      if card.isFaceUp: MUtext = chkRAM(card, 'uninstall')
      else: MUtext = ''
      executePlayScripts(card,'uninstall')
      card.moveTo(group)
   if not silent: notify("{} uninstalled {}{}.".format(me,card,MUtext))

def possess(daemonCard, programCard, silent = False):
   if debugVerbosity >= 1: notify(">>> possess(){}".format(extraASDebug())) #Debug
   #This function takes as arguments 2 cards. A Daemon and a program requiring MUs, then assigns the program to the Daemon, restoring the used MUs to the player.
   count = num(programCard.properties["Requirement"])
   if count > daemonCard.markers[mdict['DaemonMU']]:
      whisper("{} does not have enough free MUs to possess {}.".format(daemonCard, programCard))
      return 'ABORT'
   elif programCard.markers[mdict['DaemonMU']]:
      whisper("{} is already possessed by a daemon.".format(programCard))
      return 'ABORT'
   else: 
      daemonCard.markers[mdict['DaemonMU']] -= count
      programCard.markers[mdict['DaemonMU']] += count
      programCard.owner.MU += count # We return the MUs the card would be otherwise using.
      if not silent: notify("{} installs {} into {}".format(me,programCard,daemonCard))

      
def useCard(card,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> useCard(){}".format(extraASDebug())) #Debug
   if card.highlight == None:
      card.highlight = SelectColor
      notify ( "{} uses the ability of {}.".format(me,card) )
   else:
      if card.highlight == DummyColor:
         whisper(":::WARNING::: This highlight signifies that this card is a lingering effect left behind from the original\
                \nYou cannot clear such cards, please use the trash action to remove them.")
         return
      notify("{} clears {}.".format(me, card))
      card.highlight = None
      card.target(False)

def prioritize(card,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> prioritize(){}".format(extraASDebug())) #Debug
   global PriorityInform
   if card.highlight == None:
      card.highlight = PriorityColor
      notify ("{} prioritizes {} for using counters automatically.".format(me,card))
      if PriorityInform: 
         confirm("This action prioritizes a card for when selecting which card will use its counters from automated effects\
                                \nSuch automated effects include losing counters from stealth cards for using noisy icebreakers, or preventing damage\
                              \n\nSelecting a card for priority gives it first order in the pick. So it will use its counters before any other card will\
                              \n\nThe second order of priority is targeting a card. A card that is targeted at the time of the effect, will lose its counters after all cards highlighted with priority have\
                              \n\nFinally, if any part of the effect is left requiring the use of counters, any card without priority or targeted will be used.\
                              \n\nKeep this in mind if you wish to fine tune which cards use their counter automatically first\
                                \n(This message will not appear again)")
         PriorityInform = False
   else:
      if card.highlight == DummyColor:
         confirm(":::ERROR::: This highlight signifies that this card is a lingering effect left behind from the original\
                \nYou cannot prioritize such cards as they would lose their highlight and thus create problems with automation.\
                \nIf you want one such card to use counter before others, simply target (shift+click) it for the duration of the effect.")
         return
      notify("{} clears {}'s priority.".format(me, card))
      card.highlight = None
      card.target(False)
      
def rulings(card, x = 0, y = 0):
   if debugVerbosity >= 1: notify(">>> rulings(){}".format(extraASDebug())) #Debug
   mute()
   if not card.isFaceUp: return
   #openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))
   openUrl('http://www.cardgamedb.com/index.php/netrunner/android-netrunner-card-search?text={}'.format(card.name)) # Errata is not filled in most card so this works better until then
   
def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   if debugVerbosity >= 1: notify(">>> inspectCard(){}".format(extraASDebug())) #Debug
   ASText = "This card has the following automations:"
   if re.search(r'onPlay', card.Autoscript): ASText += '\n * It will have an effect when coming into play from your hand.'
   if re.search(r'onScore', card.Autoscript): ASText += '\n * It will have an effect when being scored.'
   if re.search(r'onRez', card.Autoscript): ASText += '\n * It will have an effect when its being rezzed.'
   if re.search(r'whileRezzed', card.Autoscript): ASText += '\n * It will has a continous effect while in play.'
   if re.search(r'whileScored', card.Autoscript): ASText += '\n * It will has a continous effect while scored.'
   if re.search(r'atTurnStart', card.Autoscript): ASText += '\n * It will perform an automation at the start of your turn.'
   if re.search(r'atTurnEnd', card.Autoscript): ASText += '\n * It will perform an automation at the end of your turn.'
   if card.AutoAction != '': 
      if ASText == 'This card has the following automations:': ASText == '\nThis card will perform one or more automated clicks when you double click on it.'
      else: ASText += '\n\nThis card will also perform one or more automated clicks when you double click on it.'
   if ASText == 'This card has the following automations:': ASText = '\nThis card has no automations.'
   if card.name in automatedMarkers:
      ASText += '\n\nThis card can create markers, which also have automated effects.'
   if card.type == 'Tracing': confirm("This is your tracing card. Double click on it to start a trace. It will ask you for your power bid and then put the amount as bits token on it.\
                                   \n\nOnce both players have made their bid, double-click on it again to pay the amount. This will automatically use credits from cards that pay for tracing if you have any.\
                                   \n\nIf for some reason the trace is cancelled, use the cancel trace from the menu. This will not use any bits and will clear the card.")
   elif card.type == 'Server': confirm("These are your Servers. Start stacking your Ice above them and your Agendas, Upgrades and Nodes below them.\
                                     \nThey have no automated abilities")
   elif card.type == 'Counter Hold': confirm("This is your Counter Hold. This card stores all the beneficial and harmful counters you might accumulate over the course of the game.\
                                          \n\nIf you're playing a corp, Bad Publicity, viruses and other such tokens may be put here as well. By double clicking this card, you'll use three clicks to clean all viruses from your cards.\
                                          \nIf you're playing a runner, brain damage markers, tags and any other tokens the corp gives you will be put here. by double clicking this card, you'll be able to select one of the markers to remove by paying its cost.\
                                        \n\nTo remove any token manually, simply drag & drop it out of this card.")
   else:
      if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(card.AutoScript,card.AutoAction)
      else: finalTXT = "Card Text: {}\n\n{}Would you like to see the card's details online?".format(card.Rules,ASText)
      if confirm("{}".format(finalTXT)): rulings(card)
   
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def currentHandSize(player = me):
   if debugVerbosity >= 1: notify(">>> currentHandSizel(){}".format(extraASDebug())) #Debug
   specialCard = getSpecial('Counter Hold', player)
   if specialCard.markers[mdict['BrainDMG']]: currHandSize =  player.counters['Hand Size'].value - specialCard.markers[mdict['BrainDMG']]
   else: currHandSize = player.counters['Hand Size'].value
   return currHandSize

def intPlay(card, cost = 'not_free'):
   if debugVerbosity >= 1: notify(">>> intPlay(){}".format(extraASDebug())) #Debug
   extraText = ''
   mute() 
   chooseSide() # Just in case...
   storeProperties(card)
   random = rnd(10,100)
   if (card.Type == 'Operation' or card.Type == 'Event') and chkTargeting(card) == 'ABORT': return # If it's an Operation or Event and has targeting requirements, check with the user first.
   if re.search(r'Double', getKeywords(card)): NbReq = 2 # Some cards require two clicks to play. This variable is passed to the useClick() function.
   else: NbReq = 1 #In case it's not a "Double" card. Then it only uses one click to play.
   ClickCost = useClick(count = NbReq)
   if ClickCost == 'ABORT': return  #If the player didn't have enough clicks and opted not to proceed, do nothing.
   if checkUnique(card) == False: return #If the player has the unique card and opted not to trash it, do nothing.
   if not checkNotHardwareConsole(card): return	#If player already has a Console in play and doesnt want to play that card, do nothing.
   if card.Type == 'Event' or card.Type == 'Operation': action = 'Play'
   else: action = 'Install'
   MUtext = ''
   rc = ''
   if card.Type == 'Resource' and re.search(r'Hidden', getKeywords(card)): hiddenresource = 'yes'
   else: hiddenresource = 'no'
   if card.Type == 'ICE' or card.Type == 'Agenda' or card.Type == 'Asset' or card.Type == 'Upgrade':
      placeCard(card, action)
      if Stored_Type[card] == 'ICE': card.orientation ^= Rot90 # Ice are played sideways.
      #random = rnd(10,100) #Workaround
      notify("{} to install a card.".format(ClickCost))
      card.isFaceUp = False
   elif card.Type == 'Program' or card.Type == 'Event' or card.Type == 'Resource' or card.Type == 'Hardware':
      MUtext = chkRAM(card)
      if card.Type == 'Resource' and hiddenresource == 'yes':
         placeCard(card, action)
         executePlayScripts(card,action.lower())
         card.isFaceUp = False
         notify("{} to install a hidden resource.".format(ClickCost))
         return
      reduction = reduceCost(card, action, num(card.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
      if reduction: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.
      rc = payCost(num(card.Cost) - reduction, cost)
      if rc == "ABORT": 
         me.Clicks += NbReq # If the player didn't notice they didn't have enough credits, we give them back their click
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = ''
      placeCard(card, action)
      if card.Type == 'Program':
         for targetLookup in table: # We check if we're targeting a daemon to install the program in.
            if targetLookup.targetedBy and targetLookup.targetedBy == me and re.search(r'Daemon',getKeywords(targetLookup)) and possess(targetLookup, card, silent = True) != 'ABORT':
               MUtext = ", installing it into {}".format(targetLookup)
               break         
         notify("{}{} to install {}{}{}.".format(ClickCost, rc, card, extraText,MUtext))
      elif card.Type == 'Event': notify("{}{} to prep with {}{}.".format(ClickCost, rc, card, extraText))
      elif card.Type == 'Hardware': notify("{}{} to purchase {}{}{}.".format(ClickCost, rc, card, extraText,MUtext))
      elif card.Type == 'Resource' and hiddenresource == 'no': notify("{}{} to acquire {}{}{}.".format(ClickCost, rc, card, extraText,MUtext))
      else: notify("{}{} to play {}{}{}.".format(ClickCost, rc, card, extraText,MUtext))
   else:
      reduction = reduceCost(card, action, num(card.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
      if reduction: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.
      rc = payCost(num(card.Cost) - reduction, cost)
      if rc == "ABORT": 
         me.Clicks += NbReq # If the player didn't notice they didn't have enough credits, we give them back their click
         return # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": extraText = " at no cost"
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = '' # When the cast costs nothing, we don't include the cost.
      placeCard(card, action)
      if card.Type == 'Operation': notify("{}{} to initiate {}{}.".format(ClickCost, rc, card, extraText))
      else: notify("{}{} to play {}{}.".format(ClickCost, rc, card, extraText))
   executePlayScripts(card,action.lower())
   autoscriptOtherPlayers('Card'+action,card) # we tell the autoscriptotherplayers that we installed/played a card. (e.g. See Haas-Bioroid ability)
   if debugVerbosity >= 3: notify("<<< intPlay().action: {}\nAutoscriptedothers: {}".format(action,'Card'+action)) #Debug
   if debugVerbosity >= 1:
      if Stored_Type.get(card,None): notify("++++ Stored Type: {}".format(Stored_Type[card]))
      else: notify("++++ No Stored Type Found for {}".format(card))
      if Stored_Keywords.get(card,None): notify("++++ Stored Keywords: {}".format(Stored_Keywords[card]))
      else: notify("++++ No Stored Keywords Found for {}".format(card))
      if Stored_Cost.get(card,None): notify("++++ Stored Cost: {}".format(Stored_Cost[card]))
      else: notify("++++ No Stored Cost Found for {}".format(card))


def chkTargeting(card):
   if debugVerbosity >= 1: notify(">>> chkTargeting(){}".format(extraASDebug())) #Debug
   global ExposeTargetsWarn, RevealandShuffleWarn
   if re.search(r'Targeted', card.AutoScript) and findTarget(card.AutoScript) == [] and not re.search(r'isOptional', card.AutoScript) and not confirm("This card requires a valid target for it to work correctly.\
                                                                                                                                                      \nIf you proceed without a target, strange things might happen.\
                                                                                                                                                     \n\nProceed anyway?"): return 'ABORT'
   targetPL = ofwhom(card.Autoscript)                                                                                                                                                      
   if re.search(r'ifTagged', card.Autoscript) and targetPL.Tags == 0 and not re.search(r'isOptional', card.AutoScript): 
      whisper("{} must be tagged in order to use this card".format(targetPL))
      return 'ABORT'
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

def checkNotHardwareConsole (card):
   if debugVerbosity >= 1: notify(">>> checkNotHardwareConsole(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type != "Hardware" or not re.search(r'Console', getKeywords(card)): return True
   ExistingConsoles = [ c for c in table
         if c.owner == me and c.isFaceUp and re.search(r'Console', getKeywords(c)) ]
   if len(ExistingConsoles) != 0 and not confirm("You already have at least one console in play. Are you sure you want to install {}?\n\n(If you do, your installed Consoles will be automatically trashed at no cost)".format(card.name)): return False
   else: 
      for HWDeck in ExistingConsoles: trashForFree(HWDeck)
   if debugVerbosity >= 1: notify(">>> checkNotHardwareConsole()") #Debug
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
   card.moveTo(me.piles['Heap/Archives(Face-up)'])
   notify ("{} moves a card to their face-up Archives.".format(me))

def handDiscard(card):
   if debugVerbosity >= 1: notify(">>> handDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if ds == "runner": 
      card.moveTo(me.piles['Heap/Archives(Face-up)'])
      if endofturn: 
         if card.Type == 'Program': notify("{} has killed a hanging process.".format(me))
         elif card.Type == 'Event': notify("{} has thrown away some notes.".format(me))
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
      if ds == "runner": destination = player.piles['Heap/Archives(Face-up)']
      else: destination = player.piles['Archives(Hidden)']
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Discard how many cards?", 1)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your hand to complete this action. Will discard as many as possible")   
   for iter in range(count):
      if debugVerbosity >= 3: notify("#### : handRandomDiscard() iter: {}".format(iter + 1)) # Debug
      card = group.random()
      if card == None: return iter + 1 # If we have no more cards, then return how many we managed to discard.
      card.moveTo(destination)
      if not silent: notify("{} discards {} at random.".format(player,card))
   if debugVerbosity >= 2: notify("<<< handRandomDiscard() with return {}".format(iter + 1)) #Debug
   return iter + 1 #We need to increase the iter by 1 because it starts iterating from 0
    		
def showatrandom(group, count = 1, silent = False):
   if debugVerbosity >= 1: notify(">>> showatrandom(){}".format(extraASDebug())) #Debug
   mute()
   for iter in range(count):
      card = group.random()
      if card == None: 
         notify(":::Info:::{} has no more cards in their hand to reveal".format(me))
         break
      card.moveToTable(playerside * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card), False)
      card.highlight = RevealedColor
   if not silent: notify("{} reveals {} at random from their hand.".format(me,card))

def groupToDeck (group = me.hand, player = me, silent = False):
   if debugVerbosity >= 1: notify(">>> groupToDeck(){}".format(extraASDebug())) #Debug
   mute()
   deck = player.piles['R&D/Stack']
   count = len(group)
   for c in group: c.moveTo(deck)
   if not silent: notify ("{} moves their whole {} to their {}.".format(player,pileName(group),pileName(deck)))
   if debugVerbosity >= 3: notify("<<< groupToDeck() with return:\n{}\n{}\n{}".format(pileName(group),pileName(deck),count)) #Debug
   else: return(pileName(group),pileName(deck),count) # Return a tuple with the names of the groups.

def mulligan(group):
   if debugVerbosity >= 1: notify(">>> mulligan(){}".format(extraASDebug())) #Debug
   if not confirm("Are you sure you want to take a mulligan?"): return
   notify("{} is taking a Mulligan...".format(me))
   groupToDeck(group,silent = True)
   resetAll()
   for i in range(2): 
      shuffle(me.piles['R&D/Stack']) # We do a good shuffle this time.   
      rnd(1,10)
      whisper("Shuffling...")
   drawMany(me.piles['R&D/Stack'], 5)   
   if debugVerbosity >= 3: notify("<<< mulligan()") #Debug
   
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
   card = group.top()
   if ds == 'corp' and newturn: 
      card.moveTo(me.hand)
      notify("--> {} perform's the turn's mandatory draw.".format(me))
      newturn = False
   else:
      ClickCost = useClick()
      if ClickCost == 'ABORT': return
      card.moveTo(me.hand)
      notify("{} to draw a card.".format(ClickCost))
   storeProperties(card)

def drawMany(group, count = None, destination = None, silent = False):
   if debugVerbosity >= 1: notify(">>> drawMany(){}".format(extraASDebug())) #Debug
   if debugVerbosity >= 2: notify("source: {}".format(group.name))
   if debugVerbosity >= 2 and destination: notify("destination: {}".format(destination.name))
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize : 
      count = SSize
      whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   for c in group.top(count): 
      c.moveTo(destination)
      if debugVerbosity >= 1:
         if Stored_Type.get(c,None): notify("++++ Stored Type: {}".format(Stored_Type[c]))
         else: notify("++++ No Stored Type Found for {}".format(c))
         if Stored_Keywords.get(c,None): notify("++++ Stored Keywords: {}".format(Stored_Keywords[c]))
         else: notify("++++ No Stored Keywords Found for {}".format(c))
         if Stored_Cost.get(c,None): notify("++++ Stored Cost: {}".format(Stored_Cost[c]))
         else: notify("++++ No Stored Cost Found for {}".format(c))
      storeProperties(c)
   if not silent: notify("{} draws {} cards.".format(me, count))
   if debugVerbosity >= 3: notify("<<< drawMany() with return: {}".format(count))
   return count

def toarchives(group = me.piles['Archives(Hidden)']):
   if debugVerbosity >= 1: notify(">>> toarchives(){}".format(extraASDebug())) #Debug
   mute()
   Archives = me.piles['Heap/Archives(Face-up)']
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
   if ds == "runner": destination = me.piles['Heap/Archives(Face-up)']
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

