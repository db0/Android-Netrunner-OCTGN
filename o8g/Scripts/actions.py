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
import collections
import time


#---------------------------------------------------------------------------
# Global variables
#---------------------------------------------------------------------------
identName = None # The name of our current identity
Identity = None
origController = {} # A dictionary which holds the original controller of cards who have temporary switched control to allow the opponent to manipulate them (usually during access)
ModifyDraw = 0 #if True the audraw should warn the player to look at r&D instead

gatheredCardList = False # A variable used in reduceCost to avoid scanning the table too many times.
costIncreasers = [] # used in reduceCost to store the cards that might hold potential cost-increasing effects. We store them globally so that we only scan the table once per execution
costReducers = [] # Same as above

installedCount = {} # A dictionary which keeps track how many of each card type have been installed by the player.

autoRezFlags = [] # A dictionary which holds cards that the corp has set to Auto Rez at the start of their turn.
currClicks = 0

PriorityInform = True # Explains what the "prioritize card" action does.
newturn = True #We use this variable to track whether a player has yet to do anything this turn.
endofturn = False #We use this variable to know if the player is in the end-of-turn phase.
lastKnownNrClicks = 0 # A Variable keeping track of what the engine thinks our action counter should be, in case we change it manually.

#---------------------------------------------------------------------------
# Clicks indication
#---------------------------------------------------------------------------

def useClick(group = table, x=0, y=0, count = 1, manual = False):
   debugNotify(">>> useClick(){}".format(extraASDebug())) #Debug
   global currClicks, lastKnownNrClicks
   mute()
   extraText = ''
   if count == 0: return '{} takes a free action'.format(me)
   if ds == 'runner' and re.search(r'running',getGlobalVariable('status')):
      if getGlobalVariable('SuccessfulRun') == 'True': jackOut() # If the runner has done a successful run but forgot to end it, then simply jack them out automatically.
      elif not confirm("You have not yet finished your previous run. Normally you're not allowed to use clicks during runs, are you sure you want to continue?\
                    \n\n(Pressing 'No' will abort this action and you can then Jack-out or finish the run succesfully with [ESC] or [F3] respectively"): return 'ABORT'
   clicksReduce = findCounterPrevention(me.Clicks, 'Clicks', me)
   if clicksReduce: notify(":::WARNING::: {} had to forfeit their next {} clicks".format(me, clicksReduce))
   me.Clicks -= clicksReduce
   if me.Clicks < count:
      if not confirm("You do not have enough clicks left to take this action. Are you sure you want to continue?\n\n(Did you remember to start your turn with [F1]?)"): return 'ABORT'
      else: extraText = ' (Exceeding Max!)'
   currClicks += count + lastKnownNrClicks - me.Clicks# If the player modified their click counter manually, the last two will increase/decreate our current click accordingly.
   me.Clicks -= count
   lastKnownNrClicks = me.Clicks
   #if not manual: clearLeftoverEvents() # We don't clear all event when manually dragging events to the table, or it will clear the one we just played as well. 
   # Removed above for speed. Now done only in turn end.
   debugNotify("<<< useClick", 3) #Debug
   if count == 2: return "{} {} {} uses Double Click #{} and #{}{}".format(uniClick(),uniClick(),me,currClicks - 1, currClicks,extraText)
   elif count == 3: return "{} {} {} {} uses Triple Click #{}, #{} and #{}{}".format(uniClick(),uniClick(),uniClick(),me,currClicks - 2, currClicks - 1, currClicks,extraText)
   else: return "{} {} uses Click #{}{}".format(uniClick(),me,currClicks,extraText)

def modClicks(group = table,x=0,y=0,targetPL = me, count = 1, action = 'interactive'):
   debugNotify(">>> modClicks() for {} with count {}".format(targetPL,count)) #Debug
   mute()
   loopWait = 0
   while getGlobalVariable('Max Clicks') == 'CHECKED OUT':
      rnd(1,10)
      if loopWait >= 3 and not count % 3: notify("=> {} is still checking Max Clicks...".format(me))
      loopWait += 1
      if loopWait == 15: 
         notify(":::ERROR::: cannot check out the max clicks variable. Try again later")
         return 'ABORT'
   maxClicksDict = eval(getGlobalVariable('Max Clicks'))
   debugNotify("maxClicksDict = {}".format(maxClicksDict))
   setGlobalVariable('Max Clicks','CHECKED OUT')
   if action == 'interactive': # If we're silent and at count 0, we're just looking to grab how many maxclicks we have at the end.
      count = askInteger("What is your new current maximum Clicks per turn?", maxClicksDict[targetPL._id])
      if count == None: return
      maxClicksDict[targetPL._id] = count
      notify("{} has set their Max Clicks to {} per turn".format(me,count))
   elif action == 'increment': maxClicksDict[targetPL._id] += count 
   elif action == 'set to': maxClicksDict[targetPL._id] = count
   if maxClicksDict.get(targetPL._id,'NULL') == 'NULL': # If the value has not been set, we reset it to avoid a crash.
      notify(":::WARNING::: {}'s Max Clicks were not set. Setting at the default value".format(targetPL))
      if targetPL.getGlobalVariable('ds') == 'corp': maxClicksDict[targetPL._id] = 3
      else: maxClicksDict[targetPL._id] = 4
   setGlobalVariable('Max Clicks',str(maxClicksDict)) 
   debugNotify("<<< modClicks() with return {}".format(maxClicksDict[targetPL._id])) #Debug
   return maxClicksDict[targetPL._id]

#---------------------------------------------------------------------------
# Start/End of turn
#---------------------------------------------------------------------------
def goToEndTurn(group, x = 0, y = 0):
   debugNotify(">>> goToEndTurn(){}".format(extraASDebug())) #Debug
   mute()
   global endofturn, currClicks, newturn
   if ds == None:
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   if re.search(r'running',getGlobalVariable('status')): jackOut() # If the player forgot to end the run, we do it for them now.
   if me.Clicks > 0: # If the player has not used all their clicks for this turn, remind them, just in case.
      if debugVerbosity <= 0 and not confirm("You have not taken all your clicks for this turn, are you sure you want to declare end of turn"): return
   if currentHandSize(me) < 0: 
      notify(":::Warning:::{} goes to sleep, never to wake up again (flatlined due to excessive brain damage.)".format(me)) #If the target does not have any more cards in their hand, inform they've flatlined.
      reportGame('Flatlined')
      return
   atTimedEffects('PreEnd')
   if len(me.hand) > currentHandSize(): #If the player is holding more cards than their hand max. remind them that they need to discard some
                                        # and put them in the end of turn to allow them to do so.
      if endofturn: #If the player has gone through the end of turn phase and still has more hands, allow them to continue but let everyone know.
         if debugVerbosity <= 0 and not confirm("You still hold more cards than your hand size maximum. Are you sure you want to proceed?"): return
         else: notify(":::Warning::: {} has ended their turn holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
      else: # If the player just ended their turn, give them a chance to discard down to their hand maximum.
         if ds == "corp": notify ("The Corporation of {} is performing an Internal Audit before CoB.".format(me))
         else: notify ("Runner {} is rebooting all systems for the day.".format(me))
         if debugVerbosity <= 0: information(':::Warning:::\n\n You have more card in your hand than your current hand size maximum of {}. Please discard enough and then use the "Declare End of Turn" action again.'.format(currentHandSize()))
         endofturn = True
         return
   playTurnEndSound()
   endofturn = False
   newturn = False
   currClicks = 0
   myCards = [card for card in table if card.controller == me and card.owner == me]
   for card in myCards: # We refresh once-per-turn cards to be used on the opponent's turn as well (e.g. Net Shield)
      if card._id in Stored_Type and fetchProperty(card, 'Type') != 'ICE': card.orientation &= ~Rot90
   clearRestrictionMarkers()
   atTimedEffects('End')
   clearAll() # Just in case the player has forgotten to remove their temp markers.
   announceEoT()
   opponent = ofwhom('onOpponent')
   opponent.setActivePlayer() # new in OCTGN 3.0.5.47

def goToSot (group, x=0,y=0):
   debugNotify(">>> goToSot(){}".format(extraASDebug())) #Debug
   global newturn, endofturn, lastKnownNrClicks, currClicks, turn
   mute()
   if endofturn or currClicks or newturn or me.Clicks != 0:
      if debugVerbosity <= 0 and not confirm("You have not yet properly ended you previous turn. You need to use F12 after you've finished all your clicks.\n\nAre you sure you want to continue?"): return
      else:
         if len(me.hand) > currentHandSize(): # Just made sure to notify of any shenanigans
            notify(":::Warning::: {} has skipped their End-of-Turn phase and they are holding more cards ({}) than their hand size maximum of {}".format(me,len(me.hand),currentHandSize()))
         else: notify(":::Warning::: {} has skipped their End-of-Turn phase".format(me))
         endofturn = False
   if ds == None:
      whisper ("Please perform the game setup first (Ctrl+Shift+S)")
      return
   if not me.isActivePlayer:
      if turn != 0 and not confirm("You opponent does not seem to have finished their turn properly with F12 yet. Continue?"): return
      else: me.setActivePlayer()
   playTurnStartSound()
   try: atTimedEffects('PreStart') # Trying to figure out where #275 is coming from
   except: notify(":::ERROR::: When executing PreStart scripts. Please report at: https://github.com/db0/Android-Netrunner-OCTGN/issues/275")
   currClicks = 0 # We wipe it again just in case they ended their last turn badly but insist on going through the next one.
   try: # Trying to figure out where #275 is coming from
      getMaxClicks = modClicks(action = 'chk')
      if getMaxClicks == 'ABORT': 
         if ds == 'corp': me.Clicks = 3
         else: me.Clicks = 4
      else: me.Clicks = getMaxClicks
   except: 
      notify(":::ERROR::: When setting max clicks. Please report at: https://github.com/db0/Android-Netrunner-OCTGN/issues/275")
      if ds == 'corp': me.Clicks = 3
      else: me.Clicks = 4      
   lastKnownNrClicks = me.Clicks
   try: # Trying to figure out where #275 is coming from
      myCards = [card for card in table if card.controller == me and card.owner == me]
      for card in myCards:
         if card._id in Stored_Type and fetchProperty(card, 'Type') != 'ICE': card.orientation &= ~Rot90 # Refresh all cards which can be used once a turn.
         if card.Name == '?' and card.owner == me and not card.isFaceUp:
            debugNotify("Peeking() at goToSot()")
            card.peek() # We also peek at all our facedown cards which the runner accessed last turn (because they left them unpeeked)
   except: notify(":::ERROR::: When trying to refresh cards. Please report at: https://github.com/db0/Android-Netrunner-OCTGN/issues/275")
   clearRestrictionMarkers()
   remoteServers = (card for card in table if card.Name == 'Remote Server' and card.controller != me)
   for card in remoteServers: remoteCall(card.controller,'passCardControl',[card,me]) 
   # At the start of each player's turn, we swap the ownership of all remote server, to allow them to double-click them (If they're a runner) or manipulate them (if they're a corp)
   # We do not use grabCardControl as that may take a while, as it's waiting for control change to resolve.                                                                                    
   newturn = True
   turn += 1
   autoRez()
   clearAllNewCards()
   if ds == 'runner':
      setGlobalVariable('Remote Run','False')
      setGlobalVariable('Central Run','False')
   atTimedEffects('Start') # Check all our cards to see if there's any Start of Turn effects active.
   announceSoT()
   opponent = ofwhom('onOpponent')

def autoRez():
   # A function which rezzes all cards which have been flagged to be auto-rezzed at the start of the turn.
   debugNotify(">>> autoRez()") #Debug
   mute()
   global autoRezFlags
   for cID in autoRezFlags:
      card = Card(cID)
      whisper("--- Attempting to Auto Rez {}".format(fetchProperty(card, 'Name')))
      if intRez(card, silentCost = True) == 'ABORT': whisper(":::WARNING::: Could not rez {} automatically. Ignoring".format(fetchProperty(card, 'Name')))
   del autoRezFlags[:]
   debugNotify("<<< autoRez()", 3) #Debug
#------------------------------------------------------------------------------
# Game Setup
#------------------------------------------------------------------------------

def createStartingCards():
   try:
      debugNotify(">>> createStartingCards()") #Debug
      if ds == "corp":
         if debugVerbosity >= 5: information("Creating Trace Card")
         traceCard = table.create("eb7e719e-007b-4fab-973c-3fe228c6ce20", (569 * flipBoard) + flipModX, (163 * flipBoard) + flipModY, 1, True) #The Trace card
         storeSpecial(traceCard)
         if debugVerbosity >= 5: information("Creating HQ")
         HQ = table.create("81cba950-9703-424f-9a6f-af02e0203762", (169 * flipBoard) + flipModX, (188 * flipBoard) + flipModY, 1, True)
         storeSpecial(HQ) # We pass control of the centrals to the runner, so that they can double click them to start runs
         HQ.setController(findOpponent())
         if debugVerbosity >= 5: information("Creating R&D")
         RD = table.create("fbb865c9-fccc-4372-9618-ae83a47101a2", (277 * flipBoard) + flipModX, (188 * flipBoard) + flipModY, 1, True)
         storeSpecial(RD)
         RD.setController(findOpponent())
         if debugVerbosity >= 5: information("Creating Archives")
         ARC = table.create("47597fa5-cc0c-4451-943b-9a14417c2007", (382 * flipBoard) + flipModX, (188 * flipBoard) + flipModY, 1, True)
         storeSpecial(ARC)
         ARC.setController(findOpponent())
         if debugVerbosity >= 5: information("Creating Virus Scan")
         AV = table.create("23473bd3-f7a5-40be-8c66-7d35796b6031", (478 * flipBoard) + flipModX, (165 * flipBoard) + flipModY, 1, True) # The Virus Scan card.
         storeSpecial(AV)
         try:
            BTN = table.create("fb146e53-714b-4b29-861a-d58ca9840c00", (638 * flipBoard) + flipModX, (25 * flipBoard) + flipModY, 1, True) # The No Rez Button
            BTN = table.create("e904542b-83db-4022-9e8e-9369fe7bc761", (638 * flipBoard) + flipModX, (95 * flipBoard) + flipModY, 1, True) # The OK Button
            BTN = table.create("0887f64f-4fe8-4a5b-9d41-77408fe0224b", (638 * flipBoard) + flipModX, (165 * flipBoard) + flipModY, 1, True) # The Wait Button
         except: delayed_whisper("!!!ERROR!!! In createStartingCards()\n!!! Please Install Markers Set v2.2.1+ !!!")
      else:
         if debugVerbosity >= 5: information("Creating Trace Card")
         traceCard = table.create("eb7e719e-007b-4fab-973c-3fe228c6ce20", (342 * flipBoard) + flipModX, (-331 * flipBoard) + flipModY, 1, True) #The Trace card
         storeSpecial(traceCard)
         #TC = table.create("71a89203-94cd-42cd-b9a8-15377caf4437", 471, -325, 1, True) # The Technical Difficulties card.
         #TC.moveToTable(471, -325) # It's never creating them in the right place. Move is accurate.
         #storeSpecial(TC)
         try:
            BTN = table.create("33ac6951-93ec-4034-9578-0d7dcc77c3f8", (638 * flipBoard) + flipModX, (-80 * flipBoard) + flipModY, 1, True) # The Access Imminent Button
            BTN = table.create("e904542b-83db-4022-9e8e-9369fe7bc761", (638 * flipBoard) + flipModX, (-150 * flipBoard) + flipModY, 1, True) # The OK Button
            BTN = table.create("0887f64f-4fe8-4a5b-9d41-77408fe0224b", (638 * flipBoard) + flipModX, (-220 * flipBoard) + flipModY, 1, True) # The Wait Button
         except: delayed_whisper("!!!ERROR!!! In createStartingCards()\n!!! Please Install Markers Set v2.2.1+ !!!")
   except: notify("!!!ERROR!!! {} - In createStartingCards()\n!!! PLEASE INSTALL MARKERS SET FILE !!!".format(me))


def intJackin(group = table, x = 0, y = 0, manual = False):
   debugNotify(">>> intJackin(){}".format(extraASDebug())) #Debug
   mute()
   if not Identity:
      information("::: ERROR::: No identify found! Please load a deck which contains an identity card.")
      return
   else:
      if Identity.group == table and not manual and not confirm("Are you sure you want to setup for a new game? (This action should only be done after a table reset)"): return
   #for type in Automations: switchAutomation(type,'Announce') # Too much spam.
   deck = me.piles['R&D/Stack']
   debugNotify("Checking Deck", 3)
   if len(deck) == 0:
      whisper ("Please load a deck first!")
      return
   debugNotify("Placing Identity", 3)
   debugNotify("Identity is: {}".format(Identity), 3)
   if ds == "corp":
      Identity.moveToTable((169 * flipBoard) + flipModX, (255 * flipBoard) + flipModY)
      rnd(1,10) # Allow time for the ident to be recognised
      modClicks(count = 3, action = 'set to')
      me.MU = 0
      notify("{} is the CEO of the {} Corporation".format(me,Identity))
   else:
      Identity.moveToTable((106 * flipBoard) + flipModX, (-331 * flipBoard) + flipModY)
      rnd(1,10)  # Allow time for the ident to be recognised
      modClicks(count = 4, action = 'set to')
      me.MU = 4
      BL = num(Identity.Cost)
      me.counters['Base Link'].value = BL
      notify("{} is representing the Runner {}. They start with {} {}".format(me,Identity,BL,uniLink()))
   debugNotify("Creating Starting Cards", 3)
   createStartingCards()
   debugNotify("Shuffling Deck", 3)
   shuffle(me.piles['R&D/Stack'])
   debugNotify("Drawing 5 Cards", 3)
   notify("{}'s {} is shuffled ".format(me,pileName(me.piles['R&D/Stack'])))
   drawMany(me.piles['R&D/Stack'], 5)
   debugNotify("Reshuffling Deck", 3)
   shuffle(me.piles['R&D/Stack']) # And another one just to be sure
   executePlayScripts(Identity,'STARTUP')
   initGame()
   setleague(manual = False) # Check if this is a league match
   announceSupercharge()

def createRemoteServer(group,x=0,y=0):
   debugNotify(">>> createSDF(){}".format(extraASDebug())) #Debug
   Server = table.create("d59fc50c-c727-4b69-83eb-36c475d60dcb", x, y - (40 * playerside), 1, False)
   placeCard(Server,'INSTALL')

#------------------------------------------------------------------------------
# Run...
#------------------------------------------------------------------------------
def intRun(aCost = 1, Name = 'R&D', silent = False):
   debugNotify(">>> intRun(). Current status:{}".format(getGlobalVariable('status'))) #Debug
   if ds != 'runner':
      whisper(":::ERROR:::Corporations can't run!")
      return 'ABORT'
   if re.search(r'running',getGlobalVariable('status')):
      whisper(":::ERROR:::You are already jacked-in. Please end the previous run (press [Esc] or [F3]) before starting a new one")
      return
   targetPL = findOpponent()
   BadPub = targetPL.counters['Bad Publicity'].value
   enemyIdent = getSpecial('Identity',targetPL)
   myIdent = getSpecial('Identity',me)
   abortArrow = False
   ### Custom Run Prevention Cards ###
   if enemyIdent.Subtitle == "Replicating Perfection":
      debugNotify("Checking Jinteki: Replicating Perfection restriction")
      if getGlobalVariable('Central Run') == 'False' and Name == 'Remote': 
         whisper(":::ERROR::: Your opponent is playing {}:{}. You cannot run a remote server until you've first run on a central server".format(enemyIdent,enemyIdent.Subtitle))
         return 'ABORT'
   for c in table:
      if c.name == 'Enhanced Login Protocol' and c.orientation != Rot90 and not silent: # For cards which increase the action cost, we need to check manually before the run. We don't do it when silent since that signifies a scripted run (i.e. card effect)
         aCost += 1
         c.orientation = Rot90
   ClickCost = useClick(count = aCost)
   if ClickCost == 'ABORT': return 'ABORT'
   playRunStartSound()
   if Name == 'Archives': announceTXT = 'the Archives'
   elif Name == 'Remote': announceTXT = 'a remote server'
   else: announceTXT = Name
   if not silent: notify ("{} to start a run on {}.".format(ClickCost,announceTXT))
   #barNotifyAll('#000000',"{} starts a run on {}.".format(fetchRunnerPL(),announceTXT))
   debugNotify("Setting bad publicity", 2)
   if BadPub > 0:
         myIdent.markers[mdict['BadPublicity']] += BadPub
         notify("--> The Bad Publicity of {} allows {} to secure {} for this run".format(enemyIdent,myIdent,uniCredit(BadPub)))
   debugNotify("Painting run Arrow", 2)
   if Name != 'Remote':
      targetServer = getSpecial(Name,enemyIdent.controller)
      if not targetServer: abortArrow = True # If for some reason we can't find the relevant central server card (e.g. during debug), we abort gracefully
      setGlobalVariable('Central Run','True')
   else:
      targetRemote = findTarget("Targeted-atRemote Server-isMutedTarget") # We try to see if the player had a remote targeted, if so we make it the target.
      if len(targetRemote) > 0: targetServer = targetRemote[0] # If there's no remote targeted, we paint no arrow.
      else: abortArrow = True # If we cannot figure out which remote the runner is running on,
      setGlobalVariable('Remote Run','True')
   if not abortArrow:
      targetServer.target(False)
      myIdent.arrow(targetServer, True)
   setGlobalVariable('status','running{}'.format(Name))
   atTimedEffects('Run')

def runHQ(group, x=0,y=0):
   debugNotify(">>> runHQ(){}".format(extraASDebug())) #Debug
   intRun(1, "HQ")

def runRD(group, x=0,y=0):
   debugNotify(">>> runRD(){}".format(extraASDebug())) #Debug
   intRun(1, "R&D")

def runArchives(group, x=0,y=0):
   debugNotify(">>> runArchives(){}".format(extraASDebug())) #Debug
   intRun(1, "Archives")

def runServer(group, x=0,y=0):
   debugNotify(">>> runSDF(){}".format(extraASDebug())) #Debug
   intRun(1, "Remote")

def jackOut(group=table,x=0,y=0, silent = False):
   mute()
   debugNotify(">>> jackOut(). Current status:{}".format(getGlobalVariable('status'))) #Debug
   opponent = ofwhom('-ofOpponent') # First we check if our opponent is a runner or a corp.
   if ds == 'corp': targetPL = opponent
   else: targetPL = me
   enemyIdent = getSpecial('Identity',targetPL)
   myIdent = getSpecial('Identity',me)
   runTargetRegex = re.search(r'running([A-Za-z&]+)',getGlobalVariable('status'))
   if not runTargetRegex: # If the runner is not running at the moment, do nothing
      if targetPL != me: whisper("{} is not running at the moment.".format(targetPL))
      else: whisper("You are not currently jacked-in.")
   else: # Else announce they are jacked in and resolve all post-run effects.
      runTarget = runTargetRegex.group(1) # If the runner is not feinting, then extract the target from the shared variable
      if ds == 'runner' : myIdent.markers[mdict['BadPublicity']] = 0 #If we're the runner, then remove out remaining bad publicity tokens
      else: 
         grabCardControl(enemyIdent) # Taking control to avoid errors.
         enemyIdent.markers[mdict['BadPublicity']] = 0 # If we're not the runner, then find the runners and remove any bad publicity tokens
         passCardControl(enemyIdent,enemyIdent.owner)
      if getGlobalVariable('SuccessfulRun') == 'False': playRunUnsuccesfulSound()
      atTimedEffects('JackOut') # If this was a simple jack-out, then make the end-of-run effects trigger only jack-out effects
      setGlobalVariable('status','idle') # Clear the run variable
      setGlobalVariable('feintTarget','None') # Clear any feinted targets
      setGlobalVariable('SuccessfulRun','False') # Set the variable which tells the code if the run was successful or not, to false.
      setGlobalVariable('Access','DENIED')
      setGlobalVariable('accessAttempts','0')
      debugNotify("About to announce end of Run", 2) #Debug
      if not silent: # Announce the end of run from the perspective of each player.
         if targetPL != me: 
            notify("{} has kicked {} out of their corporate grid".format(myIdent,enemyIdent))
            playCorpEndSound()
         else: notify("{} has jacked out of their run on the {} server".format(myIdent,runTarget))
      #barNotifyAll('#000000',"{} has jacked out.".format(fetchRunnerPL()))
      clearAll(True, True) # On jack out we clear all player's counters, but don't discard cards from the table.
   debugNotify("<<< jackOut()", 3) # Debug

def runSuccess(group=table,x=0,y=0, silent = False, ShardSuccess = False):
   mute()
   debugNotify(">>> runSuccess(). Current status:{}".format(getGlobalVariable('status'))) #Debug
   opponent = ofwhom('-ofOpponent') # First we check if our opponent is a runner or a corp.
   if ds == 'corp': 
      if re.search(r'running',getGlobalVariable('status')):
         notify("{} acknowledges a successful run.".format(me))
         setGlobalVariable('Access','GRANTED')
      else: whisper("Nobody is running your servers at the moment!")
   else:
      runTargetRegex = re.search(r'running([A-Za-z&]+)',getGlobalVariable('status'))
      if not runTargetRegex: # If the runner is not running at the moment, do nothing
         whisper(":::Error::: You are not currently jacked-in.")
      elif getGlobalVariable('SuccessfulRun') == 'True' or getGlobalVariable('SuccessfulRun') == 'Null':
         whisper(":::Error::: You have already completed this run. Jacking out instead...")
         jackOut()
      elif not ShardSuccess and getGlobalVariable('Access') == 'DENIED' and num(getGlobalVariable('accessAttempts')) == 0 and getGlobalVariable('Quick Access') != 'Fucking':
         BUTTON_Access() # The first time a player tries to succeed the run, we press the button for them
      elif not ShardSuccess and getGlobalVariable('Quick Access') == 'False' and getGlobalVariable('Access') == 'DENIED' and (num(getGlobalVariable('accessAttempts')) < 3 or (num(getGlobalVariable('accessAttempts')) >= 3 and not confirm("Corp has not yet acknowledged your successful run. Bypass their reaction window?"))):
         notify(":::WARNING::: {} is about to access the server and is waiting for final corporation reacts.\n(Corp must now press the [OK] button F3 to acknowledge the access.)".format(me))
         setGlobalVariable('accessAttempts',str(num(getGlobalVariable('accessAttempts')) + 1))
         return 'DENIED'
      else:
         blockSuccess = False
         for c in table: 
            if c.name == 'Crisium Grid': # Here we basically tell the system that if Crisium Grid has been used,don't set the run as succesful
               blockSuccessMarker = findMarker(c, 'Enabled')
               if blockSuccessMarker:
                  c.markers[blockSuccessMarker] = 0
                  blockSuccess = True
                  setGlobalVariable('SuccessfulRun','Null')
                  notify(":> {} sets the run to a null state.".format(c))
                  break
         if not blockSuccess: 
            setGlobalVariable('SuccessfulRun','True')
         if getGlobalVariable('feintTarget') != 'None': runTarget = getGlobalVariable('feintTarget') #If the runner is feinting, now change the target server to the right one
         else: runTarget = runTargetRegex.group(1) # If the runner is not feinting, then extract the target from the shared variable
         atTimedEffects('SuccessfulRun',ShardSuccess)
         notify("{} has successfully run the {} server".format(identName,runTarget))
         #barNotifyAll('#000000',"{} has run succesfully.".format(fetchRunnerPL()))
         if runTarget == 'Remote': setGlobalVariable('Remote Run','Success')
         else: setGlobalVariable('Central Run','Success')
   debugNotify("<<< runSuccess()", 3) # Debug
#------------------------------------------------------------------------------
# Tags...
#------------------------------------------------------------------------------
def pay2andDelTag(group, x = 0, y = 0):
   debugNotify(">>> pay2andDelTag(){}".format(extraASDebug())) #Debug
   mute()
   if ds != "runner":
      whisper("Only runners can use this action")
      return
   if me.Tags < 1:
      whisper("You don't have any tags")
      return
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   playRemoveTagSound()
   dummyCard = getSpecial('Tracing') # Just a random card to pass to the next function. Can't be bothered to modify the function to not need this.
   reduction = reduceCost(dummyCard, 'DELTAG', 2)
   if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))
   elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
   else: extraText = ''
   if payCost(2 - reduction) == "ABORT":
      me.Clicks += 1 # If the player didn't notice they didn't have enough credits, we give them back their click
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   me.counters['Tags'].value -= 1
   notify ("{} and pays {}{} to lose a tag.".format(ClickCost,uniCredit(2 - reduction),extraText))

#------------------------------------------------------------------------------
# Markers
#------------------------------------------------------------------------------
def intAddCredits ( card, count):
   debugNotify(">>> intAddCredits(){}".format(extraASDebug())) #Debug
   mute()
   if ( count > 0):
      card.markers[mdict['Credits']] += count
      if ( card.isFaceUp == True): notify("{} adds {} from the bank on {}.".format(me,uniCredit(count),card))
      else: notify("{} adds {} on a card.".format(me,uniCredit(count)))

def addCredits(card, x = 0, y = 0):
   debugNotify(">>> addCredits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many Credits?", 1)
   if count == None: return
   intAddCredits(card, count)

def remCredits(card, x = 0, y = 0):
   debugNotify(">>> remCredits(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Credits?", 1)
   if count == None: return
   if count > card.markers[mdict['Credits']]: count = card.markers[mdict['Credits']]
   card.markers[mdict['Credits']] -= count
   if card.isFaceUp == True: notify("{} removes {} from {}.".format(me,uniCredit(count),card))
   else: notify("{} removes {} from a card.".format(me,uniCredit(count)))

def remXCredits (card, x = 0, y = 0):
   debugNotify(">>> remCredits2BP(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many Credits?", 1)
   if count == None: return
   if count > card.markers[mdict['Credits']]: count = card.markers[mdict['Credits']]
   card.markers[mdict['Credits']] -= count
   me.counters['Credits'].value += count
   if card.isFaceUp == True: notify("{} removes {} from {} to their Credit Pool.".format(me,uniCredit(count),card))
   else: notify("{} takes {} from a card to their Credit Pool.".format(me,uniCredit(count)))

def addPlusOne(card, x = 0, y = 0):
   debugNotify(">>> addPlusOne(){}".format(extraASDebug())) #Debug
   mute()
   if mdict['MinusOne'] in card.markers:
      card.markers[mdict['MinusOne']] -= 1
   else:
      card.markers[mdict['PlusOne']] += 1
   notify("{} adds one +1 marker on {}.".format(me,card))

def addMinusOne(card, x = 0, y = 0):
   debugNotify(">>> addMinusOne(){}".format(extraASDebug())) #Debug
   mute()
   if mdict['PlusOne'] in card.markers:
      card.markers[mdict['PlusOne']] -= 1
   else:
      card.markers[mdict['MinusOne']] += 1
   notify("{} adds one -1 marker on {}.".format(me,card))

def addPlusOnePerm(card, x = 0, y = 0):
   debugNotify(">>> addPlusOnePerm(){}".format(extraASDebug())) #Debug
   mute()
   card.markers[mdict['PlusOnePerm']] += 1
   notify("{} adds one Permanent +1 marker on {}.".format(me,card))

def addMarker(cards, x = 0, y = 0): # A simple function to manually add any of the available markers.
   debugNotify(">>> addMarker(){}".format(extraASDebug())) #Debug
   mute()
   marker, quantity = askMarker() # Ask the player how many of the same type they want.
   if quantity == 0: return
   for card in cards: # Then go through their cards and add those markers to each.
      card.markers[marker] += quantity
      notify("{} adds {} {} counter to {}.".format(me, quantity, marker[0], card))

def addVirusCounter(card, x = 0, y = 0):
   card.markers[mdict['Virus']] += 1

def addPowerCounter(card, x = 0, y = 0):
   card.markers[mdict['Power']] += 1

def addAgendaCounter(card, x = 0, y = 0):
   card.markers[mdict['Agenda']] += 1
#------------------------------------------------------------------------------
# Advancing cards
#------------------------------------------------------------------------------
def advanceCardP(card, x = 0, y = 0):
   debugNotify(">>> advanceCardP(){}".format(extraASDebug())) #Debug
   mute()
   update()
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   reduction = reduceCost(card, 'ADVANCEMENT', 1)
   if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))
   elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
   else: extraText = ''
   if payCost(1 - reduction) == "ABORT":
      me.Clicks += 1 # If the player didn't notice they didn't have enough credits, we give them back their click
      return # If the player didn't have enough money to pay and aborted the function, then do nothing.
   card.markers[mdict['Advancement']] += 1
   remoteCall(findOpponent(),'playSound',['Advance-Card']) # Attempt to fix lag
   #playSound('Advance-Card')
   if card.isFaceUp: notify("{} and paid {}{} to advance {}.".format(ClickCost,uniCredit(1 - reduction),extraText,card))
   else: notify("{} and paid {}{} to advance a card.".format(ClickCost,uniCredit(1 - reduction),extraText))

def addXadvancementCounter(card, x=0, y=0):
   debugNotify(">>> addXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Add how many counters?", 1)
   if count == None: return
   card.markers[mdict['Advancement']] += count
   if card.isFaceUp == True: notify("{} adds {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def delXadvancementCounter(card, x = 0, y = 0):
   debugNotify(">>> delXadvancementCounter(){}".format(extraASDebug())) #Debug
   mute()
   count = askInteger("Remove how many counters?", 1)
   if count == None: return
   if count > card.markers[mdict['Advancement']]: count = card.markers[mdict['Advancement']]
   card.markers[mdict['Advancement']] -= count
   if card.isFaceUp == True: notify("{} removes {} advancement counters on {}.".format(me,count,card))
   else: notify("{} adds {} advancement counters on a card.".format(me,count))

def advanceCardM(card, x = 0, y = 0):
   debugNotify(">>> advanceCardM(){}".format(extraASDebug())) #Debug
   mute()
   card.markers[mdict['Advancement']] -= 1
   if (card.isFaceUp == True): notify("{} removes 1 advancement counter on {}.".format(me,card))
   else: notify("{} removes 1 advancement counter on a card.".format(me))

#---------------------
# Tracing...
#----------------------

def inputTraceValue (card, x=0,y=0, limit = 0, silent = False):
   debugNotify(">>> inputTraceValue(){}".format(extraASDebug())) #Debug
   mute()
   limitText = ''
   card = getSpecial('Tracing')
   limit = num(limit) # Just in case
   debugNotify("Trace Limit: {}".format(limit), 2)
   if limit > 0: limitText = '\n\n(Max Trace Power: {})'.format(limit)
   if ds == 'corp': traceTXT = 'Trace'
   else: traceTXT = 'Link'
   if ds == 'corp': 
      barNotifyAll('#000000',"{} is initiating a trace...".format(me))
      playTraceStartSound()
   else: barNotifyAll('#000000',"{} is working on their base link".format(me))
   TraceValue = askInteger("Increase {} Strength by how much?{}".format(traceTXT,limitText), 0)
   if TraceValue == None:
      whisper(":::Warning::: Trace attempt aborted by player.")
      return 'ABORT'
   while limit > 0 and TraceValue > limit:
      TraceValue = askInteger("Please increase by equal to or less than the max trace power!\nIncrease Trace power by how much?{}".format(limitText), 0)
      if TraceValue == None:
         whisper(":::Warning::: Trace attempt aborted by player.")
         return 'ABORT'
   while TraceValue - reduceCost(card, 'TRACE', TraceValue, dryRun = True) > me.Credits and not confirm("You do not seem to have enough bits to increase your Trace Strength by this amount. Continue anyway?"):
      TraceValue = askInteger("Increase {} Strength by how much?{}".format(traceTXT, limitText), 0)
      if TraceValue == None:
         whisper(":::Warning::: Trace attempt aborted by player.")
         return 'ABORT'
   reduction = reduceCost(card, 'TRACE', TraceValue)
   if reduction > 0: extraText = " (Cost reduced by {})".format(uniCredit(reduction))
   elif reduction < 0: extraText = " (Cost increased by {})".format(uniCredit(abs(reduction)))
   else: extraText = ''
   if payCost(TraceValue - reduction)  == 'ABORT': return
   #card.markers[mdict['Credits']] = TraceValue
   if ds == 'corp':
      if not silent: notify("{} starts a trace with a base strength of 0 reinforced by {}{}.".format(me,TraceValue,extraText))
      setGlobalVariable('CorpTraceValue',str(TraceValue))
      OpponentTrace = getSpecial('Tracing',ofwhom('ofOpponent'))
      OpponentTrace.highlight = EmergencyColor
      autoscriptOtherPlayers('InitiatedTrace', card)
   else:
      if not silent: notify("{} reinforces their {} by {} for a total of {}{}.".format(me,uniLink(),TraceValue, TraceValue + me.counters['Base Link'].value,extraText))
      CorpTraceValue = num(getGlobalVariable('CorpTraceValue'))
      currentTraceEffectTuple = eval(getGlobalVariable('CurrentTraceEffect'))
      debugNotify("currentTraceEffectTuple = {}".format(currentTraceEffectTuple), 2)
      if CorpTraceValue > TraceValue + me.counters['Base Link'].value:
         notify("-- {} has been traced".format(identName))
         playTraceLostSound()
         autoscriptOtherPlayers('UnavoidedTrace', card)
         try:
            if currentTraceEffectTuple[1] != 'None':
               debugNotify("Found currentTraceEffectTuple")
               executePostEffects(Card(currentTraceEffectTuple[0]),currentTraceEffectTuple[1], count = CorpTraceValue - TraceValue - me.counters['Base Link'].value) # We sent this function the card which triggered the trace, and the effect which was triggered.
         except: 
            debugNotify("currentTraceEffectTuple == None")
            pass # If it's an exception it means our tuple does not exist, so there's no current trace effects. Manual use of the trace card?
      else:
         notify("-- {} has eluded the trace".format(identName))
         playTraceAvoidedSound()
         autoscriptOtherPlayers('EludedTrace', card)
         try:
            if currentTraceEffectTuple[2] != 'None':
               executePostEffects(Card(currentTraceEffectTuple[0]),currentTraceEffectTuple[2]) # We sent this function the card which triggered the trace, and the effect which was triggered.
         except: pass # If it's an exception it means our tuple does not exist, so there's no current trace effects. Manual use of the trace card?
      setGlobalVariable('CurrentTraceEffect','None') # Once we're done with the current effects of the trace, we clear the CurrentTraceEffect global variable
      setGlobalVariable('CorpTraceValue','None') # And the corp's trace value
      card.highlight = None
   return TraceValue

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

#def payTraceValue (card, x=0,y=0):
#   if debugVerbosity >= 1: notify(">>> payTraceValue(){}".format(extraASDebug())) #Debug
#   mute()
#   extraText = ''
#   card = getSpecial('Tracing')
#   reduction = reduceCost(card, 'TRACE', card.markers[mdict['Credits']])
#   if reduction: extraText = " (reduced by {})".format(uniCredit(reduction))
#   if payCost(card.markers[mdict['Credits']] - reduction)  == 'ABORT': return
#   notify ("{} pays the {}{} they used during this trace attempt.".format(me,uniCredit(card.markers[mdict['Credits']]),extraText))
#   card.markers[mdict['Credits']] = 0
#   autoscriptOtherPlayers('TraceAttempt',card)

def cancelTrace ( card, x=0,y=0):
   debugNotify(">>> cancelTrace(){}".format(extraASDebug())) #Debug
   mute()
   TraceValue = 0
   card.markers[mdict['Credits']] = 0
   notify ("{} cancels the Trace.".format(me) )

#------------------------------------------------------------------------------
# Counter & Damage Functions
#-----------------------------------------------------------------------------

def payCost(count = 1, cost = 'not free', counter = 'BP', silentCost = False): # A function that removed the cost provided from our credit pool, after checking that we have enough.
   debugNotify(">>> payCost(){}".format(extraASDebug())) #Debug
   if cost != 'not free': return 'free'
   count = num(count)
   if count <= 0 : return 0# If the card has 0 cost, there's nothing to do.
   if counter == 'BP':
      if me.counters['Credits'].value < count:
         if silentCost: return 'ABORT'
         if not confirm("You do not seem to have enough Credits in your pool to take this action. Are you sure you want to proceed? \
                      \n(If you do, your Credit Pool will go to the negative. You will need to increase it manually as required.)"): return 'ABORT' # If we don't have enough Credits in the pool, we assume card effects or mistake and notify the player that they need to do things manually.
      me.counters['Credits'].value -= count
   elif counter == 'AP': # We can also take costs from other counters with this action.
      if me.counters['Agenda Points'].value < count and not confirm("You do not seem to have enough Agenda Points to take this action. Are you sure you want to proceed? \
         \n(If you do, your Agenda Points will go to the negative. You will need to increase them manually as required.)"): return 'ABORT'
      me.counters['Agenda Points'].value -= count
   return "{} (remaining bank: {})".format(uniCredit(count),uniCredit(me.Credits))

def findExtraCosts(card, action = 'REZ'):
   # Some hardcoded effects that increase the cost of a card.
   debugNotify(">>> findExtraCosts(). Action is: {}.".format(action)) #Debug
   increase = 0
   for marker in card.markers:
      if re.search(r'Cortez Chip',marker[0]) and action == 'REZ': increase += 2 * card.markers[marker]
   debugNotify("<<< findExtraCosts(). Increase: {}.".format(increase), 3) #Debug
   return increase

def reduceCost(card, action = 'REZ', fullCost = 0, dryRun = False, reversePlayer = False): 
   # reversePlayer is a variable that holds if we're looking for cost reducing effects affecting our opponent, rather than the one running the script.
   global costReducers,costIncreasers
   type = action.capitalize()
   debugNotify(">>> reduceCost(). Action is: {}. FullCost = {}".format(type,fullCost)) #Debug
   #if fullCost == 0: return 0 # Not used as we now have actions which also increase costs
   fullCost = abs(fullCost)
   reduction = 0
   status = getGlobalVariable('status')
   debugNotify("Status: {}".format(status), 3)
   ### First we check if the card has an innate reduction.
   Autoscripts = fetchProperty(card, 'AutoScripts').split('||')
   if len(Autoscripts):
      debugNotify("Checking for onPay reductions")
      for autoS in Autoscripts:
         if not re.search(r'onPay', autoS):
            debugNotify("No onPay trigger found in {}!".format(autoS), 2)
            continue
         reductionSearch = re.search(r'Reduce([0-9]+)Cost({}|All)'.format(type), autoS)
         if debugVerbosity >= 2: #Debug
            if reductionSearch: notify("!!! self-reduce regex groups: {}".format(reductionSearch.groups()))
            else: notify("!!! No self-reduce regex Match!")
         oppponent = ofwhom('-ofOpponent')
         if re.search(r'ifNoisyOpponent', autoS) and oppponent.getGlobalVariable('wasNoisy') != '1':
            debugNotify("No required noisy bit found!", 2)
            continue
         count = num(reductionSearch.group(1))
         targetCards = findTarget(autoS,card = card)
         multiplier = per(autoS, card, 0, targetCards)
         reduction += (count * multiplier)
         fullCost -= (count * multiplier)
         if count * multiplier > 0 and not dryRun: notify("-- {}'s full cost is reduced by {}".format(card,count * multiplier))
   else:
      debugNotify("No self-reducing autoscripts found!", 2)
   ### First we go through the table and gather any cards providing potential cost reduction
   if not gatheredCardList: # A global variable set during access of card use, that stores if we've scanned the tables for cards which reduce costs, so that we don't have to do it again.
      debugNotify("No gatheredCardList. About to Scan table cards.")
      del costReducers[:]
      del costIncreasers[:]
      RC_cardList = sortPriority([c for c in table
                              if c.isFaceUp
                              and c.highlight != RevealedColor
                              and c.highlight != StealthColor # Cards reserved for stealth do not give the credits elsewhere. Stealth cards like dagger use those credits via TokensX
                              and c.highlight != InactiveColor])
      reductionRegex = re.compile(r'(Reduce|Increase)([0-9#XS]+)Cost({}|All)-affects([A-Z][A-Za-z ]+)(-not[A-Za-z_& ]+)?'.format(type)) # Doing this now, to reduce load.
      for c in RC_cardList: # Then check if there's other cards in the table that reduce its costs.
         debugNotify("Scanning {}".format(c), 2) #Debug
         if c.Type == 'Identity' and c.Side == 'runner' and chkCerebralStatic(): continue # If Cerebral Static is still active, we abort the scripts.
         Autoscripts = CardsAS.get(c.model,'').split('||')
         if len(Autoscripts) == 0: 
            debugNotify("No AS found. Continuing")
            continue
         for autoS in Autoscripts:
            debugNotify("AS: {}".format(autoS), 2) #Debug
            if not chkRunningStatus(autoS): 
               debugNotify("Rejecting because not running")
               continue # if the reduction is only during runs, and we're not in a run, bypass this effect
            if not chkPlayer(autoS, origController.get(c._id,c.controller), False, reversePlayerChk = reversePlayer): 
               debugNotify("Rejecting because player does not match")
               continue
            reductionSearch = reductionRegex.search(autoS)
            if debugVerbosity >= 2: #Debug
               if reductionSearch: notify("!!! Regex is {}".format(reductionSearch.groups()))
               else: notify("!!! No reduceCost regex Match!")
            if re.search(r'excludeDummy', autoS) and c.highlight == DummyColor: continue
            if re.search(r'ifInstalled',autoS) and (card.group != table or card.highlight == RevealedColor): continue
            if reductionSearch: # If the above search matches (i.e. we have a card with reduction for Rez and a condition we continue to check if our card matches the condition)
               if reductionSearch.group(1) == 'Reduce':
                  debugNotify("Adding {} to cost reducers".format(c))
                  costReducers.append((c,reductionSearch,autoS)) # We put the costReducers in a different list, as we want it to be checked after all the increasers are checked
               else:
                  debugNotify("Adding {} to cost Increasers".format(c))
                  costIncreasers.append((c,reductionSearch,autoS)) # Cost increasing cards go into the main list we'll check in a bit, as we need to check them first.
                  # In each entry we store a tuple of the card object and the search result for its cost modifying abilities, so that we don't regex again later.
   else: debugNotify("gatheredCardList = {}".format(gatheredCardList))
   ### Now we check if any cards increase costs first since those costs can be later reduced via BP or other cards.
   for cTuple in costIncreasers:  
      debugNotify("Checking next cTuple", 4) #Debug
      c = cTuple[0]
      reductionSearch = cTuple[1]
      autoS = cTuple[2]
      debugNotify("cTuple[0] (i.e. card) is: {}".format(c), 2) #Debug
      debugNotify("cTuple[2] (i.e. autoS) is: {}".format(autoS), 4) #Debug
      if reductionSearch.group(4) == 'All' or checkCardRestrictions(gatherCardProperties(card), prepareRestrictions(autoS,seek = 'reduce')):
         debugNotify(" ### Search match! Increase Value is {}".format(reductionSearch.group(2)), 3) # Debug
         if not checkSpecialRestrictions(autoS,card): continue # Check if the card who's cost we're reducing matches the special restrictions of the autoscript
         if re.search(r'ifHosted',autoS): 
            c = fetchHost(card)
            if not c: continue # If we're only reducing cost for hosted cards and it isn't one, we do nothing.
         if re.search(r'onlyOnce',autoS):
            if dryRun: # For dry Runs we do not want to add the "Activated" token on the card.
               if oncePerTurn(c, act = 'dryRun') == 'ABORT': continue
            else:
               if oncePerTurn(c, act = 'automatic') == 'ABORT': continue # if the card's effect has already been used, check the next one
         if reductionSearch.group(2) == '#':
            markersCount = c.markers[mdict['Credits']]
            markersRemoved = 0
            while markersCount > 0:
               debugNotify("Increasing Cost with and Markers from {}".format(c), 2) # Debug
               reduction -= 1
               fullCost += 1
               markersCount -= 1
               markersRemoved += 1
            if not dryRun and markersRemoved != 0:
               c.markers[mdict['Credits']] -= markersRemoved # If we have a dryRun, we don't remove any tokens.
               notify(" -- {} credits are used from {}".format(markersRemoved,c))
         elif reductionSearch.group(2) == 'X':
            markerName = re.search(r'-perMarker{([\w ]+)}', autoS)
            try:
               marker = findMarker(c, markerName.group(1))
               if marker:
                  for iter in range(c.markers[marker]):
                     reduction -= 1
                     fullCost += 1
            except: notify("!!!ERROR!!! ReduceXCost - Bad Script")
         elif reductionSearch.group(2) == 'S': # 'S' Stands for Special (i.e. custom effects)
            if c.name == 'Running Interference':
               if card.Type == 'ICE':  
                  reduction -= num(card.Cost)
                  fullCost += num(card.Cost)
         else:
            for iter in range(num(reductionSearch.group(2))):  # if there is a match, the total reduction for this card's cost is increased.
               reduction -= 1
               fullCost += 1
   ### We now check for cards which reduce costs universally and as a constant effect               
   for cTuple in costReducers: 
      debugNotify("Checking next cTuple", 4) #Debug
      c = cTuple[0]
      reductionSearch = cTuple[1]
      autoS = cTuple[2]
      debugNotify("cTuple[0] (i.e. card) is: {}".format(c), 2) #Debug
      debugNotify("cTuple[2] (i.e. autoS) is: {}".format(autoS), 4) #Debug
      if reductionSearch.group(4) == 'All' or checkCardRestrictions(gatherCardProperties(card), prepareRestrictions(autoS,seek = 'reduce')):
         debugNotify(" ### Search match! Reduction Value is {}".format(reductionSearch.group(2)), 3) # Debug
         if not checkSpecialRestrictions(autoS,card): continue # Check if the card who's cost we're reducing matches the special restrictions of the autoscript
         if re.search(r'ifHosted',autoS): 
            c = fetchHost(card)
            if not c: continue # If we're only reducing cost for hosted cards and it isn't one, we do nothing.
         if re.search(r'onlyOnce',autoS):
            if dryRun: # For dry Runs we do not want to add the "Activated" token on the card.
               if oncePerTurn(c, act = 'dryRun') == 'ABORT': continue
            else:
               if oncePerTurn(c, act = 'automatic') == 'ABORT': continue # if the card's effect has already been used, check the next one
         if reductionSearch.group(2) == '#' and c.highlight == PriorityColor: # We also check if we have any recurring credits to spend on cards which the player has prioritized. Those will spend before BP.
            markersCount = c.markers[mdict['Credits']]
            markersRemoved = 0
            while markersCount > 0:
               debugNotify("Reducing Cost with and Markers from {}".format(c), 2) # Debug
               if fullCost > 0:
                  reduction += 1
                  fullCost -= 1
                  markersCount -= 1
                  markersRemoved += 1
               else: break
            if not dryRun and markersRemoved != 0:
               c.markers[mdict['Credits']] -= markersRemoved # If we have a dryRun, we don't remove any tokens.
               notify(" -- {} credits are used from {}".format(markersRemoved,c))
         elif reductionSearch.group(2) == 'X':
            markerName = re.search(r'-perMarker{([\w ]+)}', autoS)
            try:
               marker = findMarker(c, markerName.group(1))
               if marker:
                  for iter in range(c.markers[marker]):
                     if fullCost > 0:
                        reduction += 1
                        fullCost -= 1
            except: notify("!!!ERROR!!! ReduceXCost - Bad Script")
         else:
            for iter in range(num(reductionSearch.group(2))):  # if there is a match, the total reduction for this card's cost is increased.
               if fullCost > 0:
                  reduction += 1
                  fullCost -= 1
   ### Now we check if we're in a run and we have bad publicity credits to spend on reducing costs, since we want to spend that first usually.
   if re.search(r'running',status) and fullCost > 0:
      debugNotify("Checking for running reductions")
      if type == 'Force': myIdent = getSpecial('Identity',ofwhom('-ofOpponent'))
      else: myIdent = getSpecial('Identity',me)
      if myIdent.markers[mdict['BadPublicity']]:
         usedBP = 0
         BPcount = myIdent.markers[mdict['BadPublicity']]
         debugNotify("BPcount = {}".format(BPcount), 2)
         while fullCost > 0 and BPcount > 0:
            reduction += 1
            fullCost -= 1
            usedBP += 1
            BPcount -= 1
            if fullCost == 0: break
         if not dryRun and usedBP != 0:
            myIdent.markers[mdict['BadPublicity']] -= usedBP
            notify(" -- {} spends {} Bad Publicity credits".format(myIdent,usedBP))
   for cTuple in costReducers: # Finally we check for cards which also reduce costs by spending credits on themselves (since we only want to remove those as a last resort.)
      debugNotify("Checking next cTuple", 4) #Debug
      c = cTuple[0]
      reductionSearch = cTuple[1]
      autoS = cTuple[2]
      debugNotify("cTuple[0] (i.e. card) is: {}".format(c.name)) #Debug
      debugNotify("cTuple[2] (i.e. autoS) is: {}".format(autoS), 4) #Debug
      if reductionSearch.group(4) == 'All' or checkCardRestrictions(gatherCardProperties(card), prepareRestrictions(autoS,seek = 'reduce')):
         debugNotify(" ### Search match! Reduction Value is {}".format(reductionSearch.group(2)), 3) # Debug
         if not checkSpecialRestrictions(autoS,card): continue # Check if the card who's cost we're reducing matches the special restrictions of the autoscript
         if re.search(r'ifHosted',autoS): 
            c = fetchHost(card)
            if not c: continue # If we're only reducing cost for hosted cards and it isn't one, we do nothing.
         if re.search(r'onlyOnce',autoS):
            if dryRun: # For dry Runs we do not want to add the "Activated" token on the card.
               if oncePerTurn(c, act = 'dryRun') == 'ABORT': continue
            else:
               if oncePerTurn(c, act = 'automatic') == 'ABORT': continue # if the card's effect has already been used, check the next one
         if reductionSearch.group(2) == '#':
            markersCount = c.markers[mdict['Credits']]
            markersRemoved = 0
            while markersCount > 0:
               debugNotify("Reducing Cost with and Markers from {}".format(c), 2) # Debug
               if fullCost > 0:
                  reduction += 1
                  fullCost -= 1
                  markersCount -= 1
                  markersRemoved += 1
               else: break
            if not dryRun and markersRemoved != 0:
               c.markers[mdict['Credits']] -= markersRemoved # If we have a dryRun, we don't remove any tokens.
               notify(" -- {} credits are used from {}".format(markersRemoved,c))
            if not dryRun and re.search(r'trashCost-ifEmpty', autoS) and not c.markers[mdict["Credit"]]:
               debugNotify("{} has with trashCost".format(c), 3)
               intTrashCard(c, c.Stat, cost = "free", silent = True)
               notify("-- {} {} {} because it was empty".format(me,uniTrash(),c))
               #ModifyStatus('TrashMyself', c.controller.name, card, notification = 'Quick') # If the modulator -trashCost is there, the card trashes itself in order to use it's damage prevention ability
   debugNotify("<<< reduceCost() with return {}".format(reduction))
   return reduction

def intdamageDiscard(count = 1):
   debugNotify(">>> intdamageDiscard()") #Debug
   mute()
   for DMGpt in range(count): #Start applying the damage
      notify("+++ Applying damage {} of {}...".format(DMGpt+1,count))
      if len(me.hand) == 0:
         notify ("{} has flatlined.".format(me))
         reportGame('Flatlined')
         break
      else:
         card = me.hand.random()
         if ds == 'corp': card.moveTo(me.piles['Archives(Hidden)']) # For testing.
         else: card.moveTo(me.piles['Heap/Archives(Face-up)'])
         notify("--DMG: {} discarded.".format(card))

def addBrainDmg(group, x = 0, y = 0):
   mute()
   debugNotify(">>> addBrainDmg()") #Debug
   enhancer = findEnhancements("Inflict1BrainDamage")
   DMG = 1 + enhancer
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(DMG, 'Brain', me): # If we find any defense against it, inform that it was prevented
      notify ("{} prevents 1 Brain Damage.".format(me))
   else:
      applyBrainDmg()
      notify ("{} suffers 1 Brain Damage.".format(me))
      finalDMG = DMG - chkDmgSpecialEffects('Brain', DMG)[0]
      intdamageDiscard(finalDMG)
      #intdamageDiscard(me.hand)    
      playDMGSound('Brain')
      autoscriptOtherPlayers('BrainDMGInflicted',getSpecial('Identity',fetchRunnerPL()))
   debugNotify("<<< addBrainDmg()") #Debug

def applyBrainDmg(player = me, count = 1):
   debugNotify(">>> applyBrainDmg(){}".format(extraASDebug())) #Debug
   specialCard = getSpecial('Identity', player)
   specialCard.markers[mdict['BrainDMG']] += count

def addMeatDmg(group, x = 0, y = 0):
   mute()
   debugNotify(">>> addMeatDmg(){}".format(extraASDebug())) #Debug
   enhancer = findEnhancements("Inflict1MeatDamage")
   DMG = 1 + enhancer
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(DMG, 'Meat', me):
      notify ("{} prevents 1 Meat Damage.".format(me))
   else:
      notify ("{} suffers 1 Meat Damage.".format(me))
      finalDMG = DMG - chkDmgSpecialEffects('Meat', DMG)[0]
      intdamageDiscard(finalDMG)
      #intdamageDiscard(me.hand)
      playDMGSound('Meat')
      autoscriptOtherPlayers('MeatDMGInflicted',getSpecial('Identity',fetchRunnerPL()))

def addNetDmg(group, x = 0, y = 0):
   mute()
   debugNotify(">>> addNetDmg(){}".format(extraASDebug())) #Debug
   enhancer = findEnhancements("Inflict1MeatDamage")
   DMG = 1 + enhancer
   if Automations['Damage Prevention'] and confirm("Is this damage preventable?") and findDMGProtection(DMG, 'Net', me):
      notify ("{} prevents 1 Net Damage.".format(me))
   else:
      notify ("{} suffers 1 Net Damage.".format(me))
      finalDMG = DMG - chkDmgSpecialEffects('Net', DMG)[0]
      intdamageDiscard(finalDMG)
      #intdamageDiscard(me.hand)
      playDMGSound('Net')
      autoscriptOtherPlayers('NetDMGInflicted',getSpecial('Identity',fetchRunnerPL()))

def getCredit(group, x = 0, y = 0):
   debugNotify(">>> getCredit(){}".format(extraASDebug())) #Debug
   mute()
   update()
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   creditsReduce = findCounterPrevention(1, 'Credits', me)
   if creditsReduce: extraTXT = " ({} forfeited)".format(uniCredit(creditsReduce))
   else: extraTXT = ''
   notify ("{} and receives {}{}.".format(ClickCost,uniCredit(1 - creditsReduce),extraTXT))
   me.counters['Credits'].value += 1 - creditsReduce
   debugNotify("About to autoscript other players")
   playClickCreditSound()
   autoscriptOtherPlayers('CreditClicked', Identity)

def findDMGProtection(DMGdone, DMGtype, targetPL): # Find out if the player has any card preventing damage
   debugNotify(">>> findDMGProtection() with DMGtype: {}".format(DMGtype)) #Debug
   if not Automations['Damage Prevention']: return 0
   protectionFound = 0
   protectionType = 'protection{}DMG'.format(DMGtype) # This is the string key that we use in the mdict{} dictionary
   for card in table: # First we check if we have some emergency protection cards.
      debugNotify("Checking {} for emergency protection".format(card))
      for autoS in CardsAS.get(card.model,'').split('||'):
         debugNotify("Checking autoS = {} ".format(autoS),4)
         if card.controller == targetPL and re.search(r'onDamage', autoS):
            availablePrevRegex = re.search(r'protection(Meat|Net|Brain|NetBrain|All)DMG', autoS)
            debugNotify("availablePrevRegex = {} ".format(availablePrevRegex.groups()))
            if availablePrevRegex and (re.search(r'{}'.format(DMGtype),availablePrevRegex.group(1)) or availablePrevRegex.group(1) == 'All'):
               if re.search(r'onlyOnce',autoS) and card.orientation == Rot90: continue # If the card has a once per-turn ability which has been used, ignore it
               if (re.search(r'excludeDummy',autoS) or re.search(r'CreateDummy',autoS)) and card.highlight == DummyColor: continue
               if targetPL == me:
                  if confirm("You control a {} which can prevent some of the damage you're about to suffer. Do you want to activate it now?".format(fetchProperty(card, 'name'))):
                     splitScripts = autoS.split("$$")
                     for passedScript in splitScripts: X = redirect(passedScript, card, announceText = None, notificationType = 'Quick', X = 0)
                     if re.search(r'onlyOnce',autoS): card.orientation = Rot90
               else:
                  notify(":::NOTICE::: {} is about to inflict {} Damage. {} can now use their damage prevention effects such as {}.".format(me,DMGtype,targetPL,card))
                  pingCount = 0 
                  while not confirm("{} controls a {} which can prevent some of the damage you're about to inflict to them. Please wait until they decide to use it.\
                                  \n\nHas the runner  decided whether or not to the effects of their damage prevention card?\
                                    \n(Pressing 'No' will send a ping to the runner  player to remind him to take action)".format(targetPL.name,fetchProperty(card, 'name'))):
                        pingCount += 1
                        if pingCount > 2 and confirm("You've tried to ping your opponent {} times already. Do you perhaps want to abort this script?".format(pingCount)): return 'ABORT'
                        rnd(1,1000)
                        notify(":::NOTICE::: {} is still waiting for {} to decide whether to use {} or not".format(me,targetPL,card))
   cardList = sortPriority([c for c in table
               if c.controller == targetPL
               and c.markers])
   for card in cardList: # First we check for complete damage protection (i.e. protection from all types), which is always temporary.
      if card.markers[mdict['protectionAllDMG']]:
         if card.markers[mdict['protectionAllDMG']] == 100: # If we have 100 markers of damage prevention, the card is trying to prevent all Damage.
            protectionFound += DMGdone
            DMGdone = 0
            card.markers[mdict['protectionAllDMG']] = 0
         else:
            while DMGdone > 0 and card.markers[mdict['protectionAllDMG']] > 0:
               protectionFound += 1
               DMGdone -= 1
               card.markers[mdict['protectionAllDMG']] -= 1
         for autoS in CardsAS.get(card.model,'').split('||'):
            if re.search(r'trashCost', autoS) and re.search(re.escape(protectionType), autoS) and not (re.search(r'CreateDummy', autoS) and card.highlight != DummyColor):
               if not (re.search(r'trashCost-ifEmpty', autoS) and card.markers[mdict[protectionType]] > 0):
                  debugNotify("{} has with trashCost".format(card), 3)
                  ModifyStatus('TrashMyself', targetPL.name, card, notification = 'Quick') # If the modulator -trashCost is there, the card trashes itself in order to use it's damage prevention ability
         if DMGdone == 0: break
   for card in cardList:
      if card.markers[mdict[protectionType]]:
         if card.markers[mdict[protectionType]] == 100: # If we have 100 markers of damage prevention, the card is trying to prevent all Damage.
            protectionFound += DMGdone
            DMGdone = 0
            card.markers[mdict[protectionType]] = 0
         else:
            while DMGdone > 0 and card.markers[mdict[protectionType]] > 0: # For each point of damage we do.
               protectionFound += 1 # We increase the protection found by 1
               DMGdone -= 1 # We reduce how much damage we still need to prevent by 1
               card.markers[mdict[protectionType]] -= 1 # We reduce the card's damage protection counters by 1
         debugNotify("Checking if card has a trashCost")
         for autoS in CardsAS.get(card.model,'').split('||'):
            if re.search(r'trashCost', autoS) and re.search(re.escape(protectionType), autoS) and not (re.search(r'CreateDummy', autoS) and card.highlight != DummyColor):
               debugNotify("Card has a trashcost")
               if not (re.search(r'trashCost-ifEmpty', autoS) and card.markers[mdict[protectionType]] > 0):
                  ModifyStatus('TrashMyself', targetPL.name, card, notification = 'Quick') # If the modulator -trashCost is there, the card trashes itself in order to use it's damage prevention ability
         if DMGdone == 0: break # If we've found enough protection to alleviate all damage, stop the search.
   if DMGtype == 'Net' or DMGtype == 'Brain': altprotectionType = 'protectionNetBrainDMG' # To check for the combined Net & Brain protection counter as well.
   else: altprotectionType = None
   for card in cardList: # We check for the combined protections after we use the single protectors.
      if altprotectionType and card.markers[mdict[altprotectionType]]:
         if card.markers[mdict[altprotectionType]] == 100: # If we have 100 markers of damage prevention, the card is trying to prevent all Damage.
            protectionFound += DMGdone
            DMGdone = 0
            card.markers[mdict[altprotectionType]] = 0
         else:
            while DMGdone > 0 and card.markers[mdict[altprotectionType]] > 0:
               protectionFound += 1 #
               DMGdone -= 1
               card.markers[mdict[altprotectionType]] -= 1
               
         for autoS in CardsAS.get(card.model,'').split('||'):
            if re.search(r'trashCost', autoS) and re.search(re.escape(protectionType), autoS) and not (re.search(r'CreateDummy', autoS) and card.highlight != DummyColor):
               if not (re.search(r'trashCost-ifEmpty', autoS) and card.markers[mdict[protectionType]] > 0):     
                  ModifyStatus('TrashMyself', targetPL.name, card, notification = 'Quick') # If the modulator -trashCost is there, the card trashes itself in order to use it's damage prevention ability
         if DMGdone == 0: break
   debugNotify("<<< findDMGProtection() by returning: {}".format(protectionFound), 3)
   return protectionFound

def findEnhancements(Autoscript): #Find out if the player has any cards increasing damage dealt.
   debugNotify(">>> findEnhancements(){}".format(extraASDebug())) #Debug
   enhancer = 0
   DMGtype = re.search(r'\bInflict[0-9]+(Meat|Net|Brain)Damage', Autoscript)
   if DMGtype:
      for card in table:
         if card.controller == me and card.isFaceUp:
            debugNotify("Checking {}".format(card), 2) #Debug
            Autoscripts = CardsAS.get(card.model,'').split('||')
            for autoS in Autoscripts:
               if re.search(r'-isScored', autoS) and card.controller.getGlobalVariable('ds') != 'corp': continue
               cardENH = re.search(r'Enhance([0-9]+){}Damage'.format(DMGtype.group(1)), autoS)
               if cardENH: enhancer += num(cardENH.group(1))
               enhancerMarker = 'enhanceDamage:{}'.format(DMGtype.group(1))
               debugNotify(' encancerMarker: {}'.format(enhancerMarker), 3)
               foundMarker = findMarker(card, enhancerMarker)
               if foundMarker:
                  enhancer += card.markers[foundMarker]
                  card.markers[foundMarker] = 0
   debugNotify("<<< findEnhancements() by returning: {}".format(enhancer), 3)
   return enhancer

def findVirusProtection(card, targetPL, VirusInfected): # Find out if the player has any virus preventing counters.
   debugNotify(">>> findVirusProtection(){}".format(extraASDebug())) #Debug
   protectionFound = 0
   if card.markers[mdict['protectionVirus']]:
      while VirusInfected > 0 and card.markers[mdict['protectionVirus']] > 0: # For each virus infected...
         protectionFound += 1 # We increase the protection found by 1
         VirusInfected -= 1 # We reduce how much viruses we still need to prevent by 1
         card.markers[mdict['protectionVirus']] -= 1 # We reduce the card's virus protection counters by 1
   debugNotify("<<< findVirusProtection() by returning: {}".format(protectionFound), 3)
   return protectionFound

def findCounterPrevention(count, counter, targetPL): # Find out if the player has any markers preventing them form gaining specific counters (Credits, Agenda Points etc)
   debugNotify(">>> findCounterPrevention() for {}. Return immediately <<<".format(counter)) #Debug
   return 0
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
   debugNotify("<<< findCounterPrevention() by returning: {}".format(preventionFound), 3)
   return preventionFound
#------------------------------------------------------------------------------
# Card Actions
#------------------------------------------------------------------------------

def scrAgenda(card, x = 0, y = 0,silent = False, forced = False):
   debugNotify(">>> scrAgenda(){}".format(extraASDebug())) #Debug
   #global scoredAgendas
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
   if ds == 'runner': agendaTxt = 'LIBERATE'
   else: agendaTxt = 'SCORE'
   if fetchProperty(card, 'Type') == "Agenda":
      if ds == 'corp' and card.markers[mdict['Advancement']] < findAgendaRequirement(card) and not forced:
         if confirm("You have not advanced this agenda enough to score it. Bypass?"):
            cheapAgenda = True
            currentAdv = card.markers[mdict['Advancement']]
         else: return
      elif not silent and not confirm("Do you want to {} agenda {}?".format(agendaTxt.lower(),fetchProperty(card, 'name'))): return
      grabCardControl(card) # Taking control of the agenda for the one that scored it.
      card.isFaceUp = True
      if agendaTxt == 'SCORE' and chkTargeting(card) == 'ABORT':
         card.isFaceUp = False
         notify("{} cancels their action".format(me))
         return
      ap = num(fetchProperty(card,'Stat'))
      card.markers[mdict['Scored']] += 1
      apReduce = findCounterPrevention(ap, 'Agenda Points', me)
      if apReduce: extraTXT = " ({} forfeited)".format(apReduce)
      else: extraTXT = ''
      debugNotify("About to Score", 2)
      me.counters['Agenda Points'].value += ap - apReduce
      placeCard(card, action = 'SCORE')
      notify("{} {}s {} and receives {} agenda point(s){}".format(me, agendaTxt.lower(), card, ap - apReduce,extraTXT))
      if cheapAgenda: notify(":::Warning:::{} did not have enough advance tokens ({} out of {})! ".format(card,currentAdv,card.Cost))
      playScoreAgendaSound(card)
      executePlayScripts(card,agendaTxt)
      autoscriptOtherPlayers('Agenda'+agendaTxt.capitalize()+'d',card) # The autoscripts triggered by this effect are using AgendaLiberated and AgendaScored as the hook
      if me.counters['Agenda Points'].value >= 7 or (getSpecial('Identity',fetchCorpPL()).name == "Harmony Medtech" and me.counters['Agenda Points'].value >= 6):
         notify("{} wins the game!".format(me))
         reportGame()
      clearCurrents(agendaTxt) # We check to see if there's any currents to clear.
      card.highlight = None # In case the card was highlighted as revealed, we remove that now.
      card.markers[mdict['Advancement']] = 0 # We only want to clear the advance counters after the automations, as they may still be used.
   else:
      whisper ("You can't score this card")

def scrTargetAgenda(group = table, x = 0, y = 0):
   cardList = [c for c in table if c.targetedBy and c.targetedBy == me]
   for card in cardList:
      storeProperties(card)
      if fetchProperty(card, 'Type') == 'Agenda':
         if card.markers[mdict['Scored']] and card.markers[mdict['Scored']] > 0: whisper(":::ERROR::: This agenda has already been scored")
         else:
            scrAgenda(card)
            return
   notify("You need to target an unscored agenda in order to use this action")

def accessTarget(group = table, x = 0, y = 0, noQuestionsAsked = False):
   debugNotify(">>> accessTarget()") #Debug
   mute()
   global origController
   targetPL = ofwhom('-ofOpponent')
   if getGlobalVariable('SuccessfulRun') != 'True' and not noQuestionsAsked:
      if not re.search(r'running',getGlobalVariable('status')) and not confirm("You're not currently running. Are you sure you're allowed to access this card?"): return
      if runSuccess() == 'DENIED': return # If the player is trying to access, then we assume the run was a success.
   cardList = [c for c in table
               if c.targetedBy
               and c.targetedBy == me
               and c.controller == targetPL
               and not c.markers[mdict['Scored']]
               and not c.markers[mdict['ScorePenalty']]
               and c.Type != 'Server'
               and c.Type != 'ICE' # To prevent mistakes
               and not (c.orientation == Rot90 and not c.isFaceUp)
               and c.Type != 'Remote Server']
   for card in cardList:
      origController[card._id] = card.controller # We store the card's original controller to know against whom to check for scripts (e.g. when accessing a rezzed encryption protocol)
      grabCardControl(card)
      cFaceD = False
      if not card.isFaceUp:
         card.isFaceUp = True
         rnd(1,100) # Bigger delay, in case the lag makes the card take too long to read.
         cFaceD = True
         card.highlight = InactiveColor
      storeProperties(card)
      Autoscripts = CardsAS.get(card.model,'').split('||')
      for autoS in Autoscripts:
         if re.search(r'onAccess:',autoS):
            debugNotify(" accessRegex found!")
            if re.search(r'-ifNotInstalled',autoS): continue # -ifNotInstalled effects don't work with the Access Card shortcut.
            notify("{} has just accessed a {}!".format(me,card.name))
            debugNotify("Doing Remote Call with player = {}. card = {}, autoS = {}".format(me,card,autoS))
            remoteCall(card.owner, 'remoteAutoscript', [card,autoS])
            if re.search(r'-pauseRunner',autoS): # If the -pauseRunner modulator exists, we need to prevent the runner form trashing or scoring cards, as the amount of advancement tokens they have will be wiped and those may be important for the ambush effect.
               passCardControl(card,card.owner) # We pass control back to the original owner in case of a trap, to allow them to manipulate their own card (e.g. Toshiyuki Sakai)
               while not confirm("Ambush! You have stumbled into a {}\
                               \n(This card activates even when inactive. You need to wait for the corporation now.)\
                             \n\nHas the corporation decided whether or not to the effects of this ambush?\
                               \n(Pressing 'No' will send a ping to the corporation player to remind him to take action)\
                                 ".format(card.name)):
                  rnd(1,1000)
                  notify(":::NOTICE::: {} is still waiting for {} to decide whether to use {} or not".format(me,card.owner,card))
      if card.group != table: whisper(":::Access Aborted::: Card has left the table!")
      else:
         grabCardControl(card) # If the card is still in the table after any trap option resolves...
         if card.Type == 'ICE':
            cStatTXT = '\nStrength: {}.'.format(card.Stat)
         elif card.Type == 'Asset' or card.Type == 'Upgrade':
            cStatTXT = '\nTrash Cost: {}.'.format(card.Stat)
         elif card.Type == 'Agenda':
            cStatTXT = '\nAgenda Points: {}.'.format(card.Stat)
         else: cStatTXT = ''
         title = "Card: {}.\
                \nType: {}.\
                \nKeywords: {}.\
                \nCost: {}.\
                  {}\n\nCard Text: {}\
              \n\nWhat do you want to do with this card?".format(fetchProperty(card, 'name'),fetchProperty(card, 'Type'),fetchProperty(card, 'Keywords'),fetchProperty(card, 'Cost'),cStatTXT,fetchProperty(card, 'Rules'))
         if card.Type == 'Agenda' or card.Type == 'Asset' or card.Type == 'Upgrade':
            if card.Type == 'Agenda': action1TXT = 'Liberate for {} Agenda Points.'.format(card.Stat)
            else:
               reduction = reduceCost(card, 'TRASH', num(card.Stat), dryRun = True)
               if reduction > 0:
                  extraText = " ({} - {})".format(card.Stat,reduction)
                  extraText2 = " (reduced by {})".format(uniCredit(reduction))
               elif reduction < 0:
                  extraText = " ({} + {})".format(card.Stat,abs(reduction))
                  extraText2 = " (increased by {})".format(uniCredit(abs(reduction)))
               else:
                  extraText = ''
                  extraText2 = '' # I only set this here, even though it's used in line 1190 later, because to reach that part, it will have to pass through this if clause always.
               action1TXT = 'Pay {}{} to Trash.'.format(num(card.Stat) - reduction,extraText)
            options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)",action1TXT]
         else:
            options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)"]
         choice = SingleChoice(title, options, 'button')
         if choice == None: choice = 0
         if choice == 1:
            sendToTrash(card)
            notify("{} {} {} at no cost".format(me,uniTrash(),card))
         elif choice == 2:
            if card.Type == 'Agenda':
               scrAgenda(card,silent = True)
            else:
               reduction = reduceCost(card, 'TRASH', num(card.Stat))
               rc = payCost(num(card.Stat) - reduction, "not free")
               if rc == "ABORT": pass # If the player couldn't pay to trash the card, we leave it where it is.
               sendToTrash(card)
               notify("{} paid {}{} to {} {}".format(me,uniCredit(num(card.Stat) - reduction),extraText2,uniTrash(),card))
         else: pass
         if cFaceD and card.group == table and not card.markers[mdict['Scored']] and not card.markers[mdict['ScorePenalty']]: card.isFaceUp = False
         card.highlight = None
         if card.group == table and not card.markers[mdict['Scored']] and not card.markers[mdict['ScorePenalty']]: 
            passCardControl(card,card.owner) # We pass control back to the corp, but only if we didn't steal the card.
            try: del origController[card._id] # We use a try: just in case...
            except: pass

def RDaccessX(group = table, x = 0, y = 0,count = None): # A function which looks at the top X cards of the corp's deck and then asks the runner what to do with each one.
   debugNotify(">>> RDaccessX()") #Debug
   mute()
   global gatheredCardList, origController
   RDtop = []
   removedCards = 0
   if ds == 'corp' and len(players) != 1:
      whisper("This action is only for the use of the runner. Use the 'Look at top X cards' function on your R&D's context manu to access your own deck")
      return
   pauseRecovery = eval(getGlobalVariable('Paused Runner'))
   if pauseRecovery and pauseRecovery[0] == 'R&D':
      #confirm('{}'.format(pauseRecovery))
      barNotifyAll('#000000',"{} is resuming R&D Access".format(me))   
      skipIter = pauseRecovery[1] # This is the iter at which we'll resume from
      count = pauseRecovery[2] # The count of cards is what the previous access was, minus any removed cards (e.g.trashed ones)
   else:
      barNotifyAll('#000000',"{} is initiating R&D Access".format(me))
      if not count: count = askInteger("How many files are you able to access from the corporation's R&D?",1)
      if count == None: return
      skipIter = -1 # We only using this variable if we're resuming from a paused R&D access.
      playAccessSound('RD')
   targetPL = ofwhom('-ofOpponent')
   grabPileControl(targetPL.piles['R&D/Stack'])
   debugNotify("Found opponent. Storing the top {} as a list".format(count), 3) #Debug
   RDtop = list(targetPL.piles['R&D/Stack'].top(count))
   if len(RDtop) == 0:
      whisper("Corp's R&D is empty. You cannot take this action")
      return
   if debugVerbosity >= 4:
      for card in RDtop: notify(" Card: {}".format(card))
   notify("{} is accessing the top {} cards of {}'s R&D".format(me,count,targetPL))
   for iter in range(len(RDtop)):
      if iter <= skipIter: continue
      debugNotify("Moving card {}".format(iter), 3) #Debug
      notify(" -- {} is now accessing the {} card".format(me,numOrder(iter)))
      origController[RDtop[iter]._id] = targetPL # We store the card's original controller to know against whom to check for scripts (e.g. when accessing a rezzed encryption protocol)
      RDtop[iter].moveToBottom(me.ScriptingPile)
      storeProperties(RDtop[iter])
      debugNotify(" Looping...", 4)
      loopChk(RDtop[iter],'Type')
      Autoscripts = CardsAS.get(RDtop[iter].model,'').split('||')
      debugNotify("Grabbed AutoScripts", 4)
      for autoS in Autoscripts:
         if re.search(r'onAccess:',autoS):
            if re.search(r'-ifInstalled',autoS): continue # -ifInstalled cards work only while on the table.
            if re.search(r'-ifNotAccessedInRD',autoS): continue # -ifNotInRD cards work only while not accessed from R&D.
            debugNotify(" accessRegex found!")
            notify("{} has just accessed {}!".format(me,RDtop[iter].name))
            remoteCall(RDtop[iter].owner, 'remoteAutoscript', [RDtop[iter],autoS])
            if re.search(r'-pauseRunner',autoS): 
               notify(":::WARNING::: {} has stumbled onto {}. Once the effects of this card are complete, they need to press Ctrl+A to continue their access from where they left it.\nThey have seen {} out of {} cards until now.".format(me,RDtop[iter].name,iter + 1, count))
               RDtop[iter].moveTo(targetPL.piles['R&D/Stack'],iter - removedCards)
               passPileControl(targetPL.piles['R&D/Stack'],targetPL)
               gatheredCardList = False  # We set this variable to False, so that reduceCost() calls from other functions can start scanning the table again.
               setGlobalVariable('Paused Runner',str(['R&D',iter - removedCards,count - removedCards]))
               return
      debugNotify(" Storing...", 4)
      cType = RDtop[iter].Type
      cKeywords = RDtop[iter].Keywords
      cStat = RDtop[iter].Stat
      cCost = RDtop[iter].Cost
      cName = RDtop[iter].name
      cRules = RDtop[iter].Rules
      debugNotify("Stored properties. Checking type...", 3) #Debug
      if cType == 'ICE':
         cStatTXT = '\nStrength: {}.'.format(cStat)
      elif cType == 'Asset' or cType == 'Upgrade':
         cStatTXT = '\nTrash Cost: {}.'.format(cStat)
      elif cType == 'Agenda':
         cStatTXT = '\nAgenda Points: {}.'.format(cStat)
      else: cStatTXT = ''
      title = "Card: {}.\
             \nType: {}.\
             \nKeywords: {}.\
             \nCost: {}.\
               {}\n\nCard Text: {}\
           \n\nWhat do you want to do with this card?".format(cName,cType,cKeywords,cCost,cStatTXT,cRules)
      if cType == 'Agenda' or cType == 'Asset' or cType == 'Upgrade':
         if cType == 'Agenda': action1TXT = 'Liberate for {} Agenda Points.'.format(cStat)
         else:
            reduction = reduceCost(RDtop[iter], 'TRASH', num(cStat), dryRun = True)
            gatheredCardList = True # We set this variable to True, to tell future reducecosts in this execution, not to scan the table a second time.
            if reduction > 0:
               extraText = " ({} - {})".format(cStat,reduction)
               extraText2 = " (reduced by {})".format(uniCredit(reduction))
            elif reduction < 0:
               extraText = " ({} + {})".format(cStat,abs(reduction))
               extraText2 = " (increased by {})".format(uniCredit(reduction))
            else:
               extraText = ''
               extraText2 = ''
            action1TXT = 'Pay {}{} to Trash.'.format(num(cStat) - reduction,extraText)
         options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)",action1TXT]
      else:
         options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)"]
      choice = SingleChoice(title, options, 'button')
      if choice == None: choice = 0
      if choice == 1:
         sendToTrash(RDtop[iter])
         loopChk(RDtop[iter],'Type')
         notify("{} {} {} at no cost".format(me,uniTrash(),RDtop[iter]))
         removedCards += 1
      elif choice == 2:
         if cType == 'Agenda':
            RDtop[iter].moveToTable(0,0)
            RDtop[iter].highlight = RevealedColor
            scrAgenda(RDtop[iter],silent = True)
            removedCards += 1
         else:
            reduction = reduceCost(RDtop[iter], 'TRASH', num(cStat))
            rc = payCost(num(cStat) - reduction, "not free")
            if rc == "ABORT": continue # If the player couldn't pay to trash the card, we leave it where it is.
            sendToTrash(RDtop[iter])
            loopChk(RDtop[iter],'Type')
            notify("{} paid {}{} to {} {}".format(me,uniCredit(num(cStat) - reduction),extraText2,uniTrash(),RDtop[iter]))
            removedCards += 1
      else: 
         debugNotify("Selected doing nothing. About to move back...", 4)
         RDtop[iter].moveTo(targetPL.piles['R&D/Stack'],iter - removedCards)
      try: del origController[RDtop[iter]._id] # We use a try: just in case...
      except: pass         
   notify("{} has finished accessing {}'s R&D".format(me,targetPL))
   passPileControl(targetPL.piles['R&D/Stack'],targetPL)
   gatheredCardList = False  # We set this variable to False, so that reduceCost() calls from other functions can start scanning the table again.
   setGlobalVariable('Paused Runner','False')
   debugNotify("<<< RDaccessX()", 3)
   
def ARCscore(group=table, x=0,y=0):
   mute()
   global origController
   debugNotify(">>> ARCscore(){}".format(extraASDebug())) #Debug
   removedCards = 0
   ARCHcards = []
   if ds == 'corp':
      whisper("This action is only for the use of the runner.")
      return
   targetPL = ofwhom('-ofOpponent')
   debugNotify("Found opponent.", 3) #Debug
   ARC = targetPL.piles['Heap/Archives(Face-up)']
   grabPileControl(ARC)
   grabPileControl(targetPL.piles['Archives(Hidden)'])
   for card in targetPL.piles['Archives(Hidden)']: card.moveTo(ARC) # When the runner accesses the archives, all  cards of the face up archives.
   passPileControl(targetPL.piles['Archives(Hidden)'],targetPL)
   if len(ARC) == 0:
      whisper("Corp's Archives are empty. You cannot take this action")
      return
   playAccessSound('Archives')
   rnd(10,100) # A small pause
   agendaFound = False
   for card in ARC:
      debugNotify("Checking: {}.".format(card), 3) #Debug
      origController[card._id] = targetPL # We store the card's original controller to know against whom to check for scripts (e.g. when accessing a rezzed encryption protocol)
      if card.Type == 'Agenda' and not re.search(r'-disableAutoStealingInArchives',CardsAS.get(card.model,'')): 
         agendaFound = True
         card.moveToTable(0,0)
         card.highlight = RevealedColor
         scrAgenda(card) # We don't want it silent, as it needs to ask the runner to score, in case of agendas like Fetal AI for which they have to pay as well.
         if card.highlight == RevealedColor: card.moveTo(ARC) # If the runner opted not to score the agenda, put it back into the deck.
      Autoscripts = CardsAS.get(card.model,'').split('||')
      debugNotify("Grabbed AutoScripts", 4)
      for autoS in Autoscripts:
         if chkModulator(card, 'worksInArchives', 'onAccess'):
            debugNotify("-worksInArchives accessRegex found!")
            notify("{} has just accessed a {}!".format(me,card.name))
            remoteCall(card.owner, 'remoteAutoscript', [card,autoS])
      try: del origController[card._id] # We use a try: just in case...
      except: pass
   if not agendaFound: notify("{} has rumaged through {}'s archives but found no Agendas".format(Identity,targetPL))
   passPileControl(ARC,targetPL)
   debugNotify("<<< ARCscore()")

def HQaccess(group=table, x=0,y=0, silent = False, directTargets = None):
   mute()
   global origController
   debugNotify(">>> HQAccess(){}".format(extraASDebug())) #Debug
   if ds == 'corp' and len(players) != 1:
      whisper("This action is only for the use of the runner.")
      return
   targetPL = ofwhom('-ofOpponent')
   debugNotify("Found opponent.", 3) #Debug
   grabPileControl(targetPL.hand)
   revealedCards = [c for c in table if c.highlight == RevealedColor]
   if len(revealedCards): # Checking if we're continuing from a Paused HQ Access.
      barNotifyAll('#000000',"{} is resuming their HQ Access".format(me))      
   elif getGlobalVariable('Paused Runner') != 'False':
      # If the pause variable is still active, it means the last access was paused by there were no other cards to resume, so we just clear the variable.
      setGlobalVariable('Paused Runner','False')
      return
   elif directTargets != None: # This means that we passed direct cards to access (e.g. Kitsune)
      barNotifyAll('#000000',"{} is initiating HQ Access".format(me))
      playAccessSound('HQ')
      showDirect(directTargets)      
      revealedCards = directTargets
   else:
      if not silent and not confirm("You are about to access a random card from the corp's HQ.\
                                   \nPlease make sure your opponent is not manipulating their hand, and does not have a way to cancel this effect before continuing\
                                 \n\nProceed?"): return
      barNotifyAll('#000000',"{} is initiating HQ Access".format(me))
      count = askInteger("How many files are you able to access from the corporation's HQ?",1)
      if count == None: return
      playAccessSound('HQ')
      revealedCards = showatrandom(count = count, targetPL = targetPL, covered = True)
   for revealedCard in revealedCards:
      loopChk(revealedCard)
      origController[revealedCard._id] = targetPL # We store the card's original controller to know against whom to check for scripts (e.g. when accessing a rezzed encryption protocol)
      #storeProperties(revealedCard) # So as not to crash reduceCost() later
      revealedCard.sendToFront() # We send our currently accessed card to the front, so that the corp can see it. The rest are covered up.
      accessRegex = re.search(r'onAccess:([^|]+)',CardsAS.get(revealedCard.model,''))
      if accessRegex:
         debugNotify(" accessRegex found! {}".format(accessRegex.group(1)), 2)
         notify("{} has just accessed a {}!".format(me,revealedCard))
      Autoscripts = CardsAS.get(revealedCard.model,'').split('||')
      for autoS in Autoscripts:
         if re.search(r'onAccess:',autoS):
            if re.search(r'-ifInstalled',autoS): continue # -ifInstalled cards work only while on the table.
            debugNotify(" accessRegex found!")
            notify("{} has just accessed a {}!".format(me,revealedCard.name))
            remoteCall(revealedCard.owner, 'remoteAutoscript', [revealedCard,autoS])
            if re.search(r'-pauseRunner',autoS): 
               notify(":::WARNING::: {} has stumbled onto {}. Once the effects of this card are complete, they need to press Ctrl+Q to continue their access from where they left it.".format(me,revealedCard.name))
               revealedCard.moveTo(targetPL.hand) # We return it to the player's hand because the effect will decide where it goes afterwards
               if not len([c for c in table if c.highlight == RevealedColor]): clearCovers() # If we have no leftover cards to access after a
               passPileControl(targetPL.hand,targetPL)
               setGlobalVariable('Paused Runner',str(['HQ']))
               return
      debugNotify("Not a Trap.", 2) #Debug
      if revealedCard.Type == 'ICE':
         cStatTXT = '\nStrength: {}.'.format(revealedCard.Stat)
      elif revealedCard.Type == 'Asset' or revealedCard.Type == 'Upgrade':
         cStatTXT = '\nTrash Cost: {}.'.format(revealedCard.Stat)
      elif revealedCard.Type == 'Agenda':
         cStatTXT = '\nAgenda Points: {}.'.format(revealedCard.Stat)
      else: cStatTXT = ''
      debugNotify("Crafting Title", 2) #Debug
      title = "Card: {}.\
             \nType: {}.\
             \nKeywords: {}.\
             \nCost: {}.\
               {}\n\nCard Text: {}\
           \n\nWhat do you want to do with this card?".format(revealedCard.Name,revealedCard.Type,revealedCard.Keywords,revealedCard.Cost,cStatTXT,revealedCard.Rules)
      if revealedCard.Type == 'Agenda' or revealedCard.Type == 'Asset' or revealedCard.Type == 'Upgrade':
         if revealedCard.Type == 'Agenda': action1TXT = 'Liberate for {} Agenda Points.'.format(revealedCard.Stat)
         else:
            reduction = reduceCost(revealedCard, 'TRASH', num(revealedCard.Stat), dryRun = True)
            if reduction > 0:
               extraText = " ({} - {})".format(revealedCard.Stat,reduction)
               extraText2 = " (reduced by {})".format(uniCredit(reduction))
            elif reduction < 0:
               extraText = " ({} + {})".format(revealedCard.Stat,abs(reduction))
               extraText2 = " (increased by {})".format(uniCredit(abs(reduction)))
            else:
               extraText = ''
               extraText2 = ''
            action1TXT = 'Pay {}{} to Trash.'.format(num(revealedCard.Stat) - reduction,extraText)
         options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)",action1TXT]
      else:
         options = ["Leave where it is.","Force trash at no cost.\n(Only through card effects)"]
      debugNotify("Opening Choice Window", 2) #Debug
      choice = SingleChoice(title, options, 'button')
      if choice == None: choice = 0
      if choice == 1:
         sendToTrash(revealedCard)
         loopChk(revealedCard,'Type')
         notify("{} {} {} at no cost".format(me,uniTrash(),revealedCard))
      elif choice == 2:
         if revealedCard.Type == 'Agenda':
            scrAgenda(revealedCard,silent = True)
         else:
            reduction = reduceCost(revealedCard, 'TRASH', num(revealedCard.Stat))
            rc = payCost(num(revealedCard.Stat) - reduction, "not free")
            if rc == "ABORT": revealedCard.moveTo(targetPL.hand) # If the player couldn't pay to trash the card, we leave it where it is.
            sendToTrash(revealedCard)
            loopChk(revealedCard,'Type')
            notify("{} paid {}{} to {} {}".format(me,uniCredit(num(revealedCard.Stat) - reduction),extraText2,uniTrash(),revealedCard))
      else: revealedCard.moveTo(targetPL.hand)
      try: del origController[revealedCard._id] # We use a try: just in case...
      except: pass
   rnd(1,10) # a little pause
   for c in revealedCards: c.highlight = None # We make sure no card remains highlighted for some reason.
   passPileControl(targetPL.hand,targetPL)
   setGlobalVariable('Paused Runner','False')
   clearCovers() # Finally we clear any remaining cover cards.
   debugNotify("<<< HQAccess()", 3)
   
def isRezzable (card):
   debugNotify(">>> isRezzable(){}".format(extraASDebug())) #Debug
   mute()
   Type = fetchProperty(card, 'Type')
   if Type == "ICE" or Type == "Asset" or Type == "Upgrade" or Type == "Agenda": return True
   else: return False

def intRez (card, x=0, y=0, cost = 'not free', silent = False, silentCost = False, preReduction = 0):
   debugNotify(">>> intRez(){}".format(extraASDebug())) #Debug
   mute()
   rc = ''
   storeProperties(card)
   if card.isFaceUp:
      whisper("you can't rez a rezzed card")
      return 'ABORT'
   if not isRezzable(card):
      whisper("Not a rezzable card")
      return 'ABORT'
   if not checkUnique(card): return 'ABORT' #If the player has the unique card rezzed and opted not to trash it, do nothing.
   if chkTargeting(card) == 'ABORT':
      notify("{} cancels their action".format(me))
      return 'ABORT'
   if fetchProperty(card, 'Name') == 'IQ': cardCost = len(me.hand) # Special code to allow IQ to work
   else: cardCost = num(fetchProperty(card, 'Cost'))
   if cost != 'free': reduction = reduceCost(card, 'REZ', cardCost) + preReduction
   else: reduction = preReduction
   if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))
   elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
   else: extraText = ''
   increase = findExtraCosts(card, 'REZ')
   rc = payCost(cardCost - reduction + increase, cost, silentCost = silentCost)
   if rc == "ABORT": return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == "free": extraText = " at no cost"
   elif rc != 0: rc = "for {}".format(rc)
   else: rc = ''
   card.isFaceUp = True
   if not silent:
      if card.Type == 'ICE': notify("{} has rezzed {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Asset': notify("{} has acquired {} {}{}.".format(me, card, rc, extraText))
      if card.Type == 'Upgrade': notify("{} has installed {} {}{}.".format(me, card, rc, extraText))
   playRezSound(card)
   update() # Bug workaround.
   executePlayScripts(card,'REZ')
   autoscriptOtherPlayers('CardRezzed',card)

def rezForFree(card, x = 0, y = 0):
   debugNotify(">>> rezForFree(){}".format(extraASDebug())) #Debug
   intRez(card, cost = 'free')

def flagAutoRez(card, x = 0, y = 0):
   global autoRezFlags
   storeProperties(card)
   if card.isFaceUp:
      whisper("you can't rez a rezzed card")
      return 'ABORT'
   if not isRezzable(card):
      whisper("Not a rezzable card")
      return 'ABORT'
   if card._id in autoRezFlags:
      autoRezFlags.remove(card._id)
      whisper("--- {} will not attempt to rez at the start of your turn".format(fetchProperty(card, 'Name')))
   else:
      autoRezFlags.append(card._id)
      whisper("--- {} has been flagged to automatically rez at the start of your turn".format(fetchProperty(card, 'Name')))

def derez(card, x = 0, y = 0, silent = False):
   debugNotify(">>> derez(){}".format(extraASDebug())) #Debug
   mute()
   storeProperties(card)
   if card.isFaceUp:
      if not isRezzable(card):
         whisper ("Not a rezzable card")
         return 'ABORT'
      else:
         if not silent: notify("{} derezzed {}".format(me, card))
         card.markers[mdict['Credits']] = 0
         playDerezSound(card)
         executePlayScripts(card,'DEREZ')
         autoscriptOtherPlayers('CardDerezzed',card)
         card.isFaceUp = False
         if card.owner == me:
            if debugVerbosity >= 0 and not confirm("Peek at card?"): return
            card.peek()
   else:
      notify ( "you can't derez a unrezzed card")
      return 'ABORT'

def expose(card, x = 0, y = 0, silent = False):
   debugNotify(">>> expose(){}".format(extraASDebug())) #Debug
   if not card.isFaceUp:
      mute()
      if card.controller != me: notify("{} attempts to expose target card.".format(me)) # When the opponent exposes, we don't actually go through with it, to avoid mistakes.
      else:
         card.isFaceUp = True
         if card.highlight == None: card.highlight = RevealedColor # we don't want to accidentally wipe dummy card highlight.
         if not silent: notify("{} exposed {}".format(me, card))
   else:
      card.isFaceUp = False
      debugNotify("Peeking() at expose()")
      card.peek()
      if card.highlight == RevealedColor: card.highlight = None
      if not silent: notify("{} hides {} once more again".format(me, card))

def rolld6(group = table, x = 0, y = 0, silent = False):
   debugNotify(">>> rolld6(){}".format(extraASDebug())) #Debug
   mute()
   n = rnd(1, 6)
   if not silent: notify("{} rolls {} on a 6-sided die.".format(me, n))
   return n

def selectAsTarget (card, x = 0, y = 0):
   debugNotify(">>> selectAsTarget(){}".format(extraASDebug())) #Debug
   card.target(True)

def clear(card, x = 0, y = 0, silent = False):
   debugNotify(">>> clear() card: {}".format(card), ) #Debug
   mute()
   if not silent: notify("{} clears {}.".format(me, card))
   if card.highlight != DummyColor and card.highlight != RevealedColor and card.highlight != NewCardColor and card.highlight != InactiveColor and card.highlight != StealthColor and card.highlight != PriorityColor: 
      debugNotify("Clearing {} Highlight for {}".format(card.highlight,card))
      card.highlight = None
   card.markers[mdict['BaseLink']] = 0
   card.markers[mdict['PlusOne']] = 0
   card.markers[mdict['MinusOne']] = 0
   card.target(False)
   debugNotify("<<< clear()", 3)

def clearAll(markersOnly = False, allPlayers = False): # Just clears all the player's cards.
   debugNotify(">>> clearAll()") #Debug
   if allPlayers: 
      for player in getPlayers():
         if player != me: remoteCall(player,'clearAll',[markersOnly, False])
   for card in table:
      if card.controller == me: 
         if card.name == 'Trace': card.highlight = None # We clear the card in case a tracing is pending that was not done.
         clear(card,silent = True)
         if card.owner == me and card.Type == 'Identity' and Stored_Type.get(card._id,'NULL') == 'NULL':
            delayed_whisper(":::DEBUG::: Identity was NULL. Re-storing as an attempt to fix")
            storeProperties(card, True)
   if not markersOnly: clearLeftoverEvents()
   debugNotify("<<< clearAll()", 3)

def clearAllNewCards(remoted = False): # Clears all highlights from new cards.
   debugNotify(">>> clearAllNewCards(){}".format(extraASDebug())) #Debug
   if not remoted:
      for player in getPlayers():
         if player != me: remoteCall(player,'clearAllNewCards',[True])
   for card in table:
      if card.highlight == NewCardColor and card.controller == me: 
         debugNotify("Clearing New card {}".format(card))
         card.highlight = None  
   debugNotify(">>> clearAllNewCards(){}".format(extraASDebug())) #Debug
   
def intTrashCard(card, stat, cost = "not free",  ClickCost = '', silent = False):
   debugNotify(">>> intTrashCard(){}".format(extraASDebug())) #Debug
   global trashEasterEggIDX
   mute()
   MUtext = ""
   rc = ''
   storeProperties(card)
   if card.group.name == 'Heap/Archives(Face-up)' or card.group.name == 'Archives(Hidden)': # If the card is already trashed (say from a previous script), we don't want to try and trash it again
      return # We don't return abort, otherwise scripts will stop executing (e.g. see using Fairy to break two subroutines)
   if card.markers[mdict['Scored']] or card.markers[mdict['ScorePenalty']]: 
      exileCard(card) # If the card is scored, then card effects don't trash it, but rather remove it from play (Otherwise the runner could score it again)
      return
   if ClickCost == '':
      ClickCost = '{} '.format(me) # If not clicks were used, then just announce our name.
      goodGrammar = 'es' # LOL Grammar Nazi
   else:
      ClickCost += ' and '
      goodGrammar = ''
   if UniCode: goodGrammar = ''
   cardowner = card.owner
   if fetchProperty(card, 'Type') == "Tracing" or fetchProperty(card, 'Type') == "Counter Hold" or (fetchProperty(card, 'Type') == "Server" and fetchProperty(card, 'name') != "Remote Server"):
      whisper("{}".format(trashEasterEgg[trashEasterEggIDX]))
      if trashEasterEggIDX < 7:
         trashEasterEggIDX += 1
         return 'ABORT'
      elif trashEasterEggIDX == 7:
         card.moveToBottom(cardowner.piles['Heap/Archives(Face-up)'])
         trashEasterEggIDX = 0
         return 'ABORT'
   if card.highlight == DummyColor and getSetting('DummyTrashWarn',True) and not silent and not confirm(":::Warning!:::\n\nYou are about to trash a dummy card. You will not be able to restore it without using the effect that created it originally.\n\nAre you sure you want to proceed? (This message will not appear again)"):
      setSetting('DummyTrashWarn',False)
      return
   else: setSetting('DummyTrashWarn',False)
   if cost != 'free': reduction = reduceCost(card, 'TRASH', num(stat)) # So as not to waste time.
   else: reduction = 0
   if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))
   elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
   else: extraText = ''
   rc = payCost(num(stat) - reduction, cost)
   if rc == "ABORT": return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
   elif rc == 0:
      if ClickCost.endswith(' and'): ClickCost[:-len(' and')] # if we have no click cost, we don't need the connection.
   else:
      ClickCost += "pays {} to".format(rc) # If we have Credit cost, append it to the Click cost to be announced.
      goodGrammar = ''
   if fetchProperty(card, 'Type') == 'Event' or fetchProperty(card, 'Type') == 'Operation': silent = True # These cards are already announced when played. No need to mention them a second time.
   if card.isFaceUp:
      MUtext = chkRAM(card, 'UNINSTALL')
      if rc == "free" and not silent:
         debugNotify("About to trash card for free. Cost = {}".format(cost), 2)
         if cost == "host removed": notify("{} {} {} because its host has been removed from play{}.".format(card.owner, uniTrash(), card, MUtext))
         else: notify("{} {} {} at no cost{}.".format(me, uniTrash(), card, MUtext))
      elif not silent: notify("{} {}{} {}{}{}.".format(ClickCost, uniTrash(), goodGrammar, card, extraText, MUtext))
      sendToTrash(card)
   elif (ds == "runner" and card.controller == me) or (ds == "runner" and card.controller != me and cost == "not free") or (ds == "corp" and card.controller != me ):
   #I'm the runner and I trash my cards, or an accessed card from the corp, or I 'm the corp and I trash a runner's card, then the card will go to the open archives
      sendToTrash(card)
      if rc == "free" and not silent:
         if card.highlight == DummyColor: notify ("{} clears {}'s lingering effects.".format(me, card)) # In case the card is a dummy card, we change the notification slightly.
         else: notify ("{} {} {}{} at no cost.".format(me, uniTrash(), card, extraText))
      elif not silent: notify("{} {}{} {}{}.".format(ClickCost, uniTrash() , goodGrammar, card, extraText))
   else: #I'm the corp and I trash my own hidden cards or the runner and trash a hidden corp card without cost (e.g. randomly picking one from their hand)
      sendToTrash(card, cardowner.piles['Archives(Hidden)'])
      if rc == "free" and not silent: notify("{} {} a hidden card at no cost.".format(me, uniTrash()))
      elif not silent: notify("{} {}{} a hidden card.".format(ClickCost, uniTrash(), goodGrammar))
   debugNotify("<<< intTrashCard()", 3)

def trashCard (card, x = 0, y = 0):
   debugNotify(">>> trashCard(){}".format(extraASDebug())) #Debug
   if card.highlight == DummyColor: intTrashCard(card, card.Stat, "free") # lingering effects don't require cost to trash.
   else: intTrashCard(card, card.Stat)

def trashForFree (card, x = 0, y = 0):
   debugNotify(">>> trashForFree(){}".format(extraASDebug())) #Debug
   intTrashCard(card, card.Stat, "free")

def pay2AndTrash(card, x=0, y=0):
   debugNotify(">>> pay2AndTrash(){}".format(extraASDebug())) #Debug
   ClickCost = useClick()
   if ClickCost == 'ABORT': return
   intTrashCard(card, 2, ClickCost = ClickCost)

def trashTargetFree(group, x=0, y=0):
   debugNotify(">>> trashTargetFree(){}".format(extraASDebug())) #Debug
   targetCards = [c for c in table
                 if c.targetedBy
                 and c.targetedBy == me]
   if len(targetCards) == 0: return
   for card in targetCards:
      storeProperties(card)
      intTrashCard(card, fetchProperty(card, 'Stat'), "free")

def trashTargetPaid(group, x=0, y=0):
   debugNotify(">>> trashTargetFree(){}".format(extraASDebug())) #Debug
   targetCards = [c for c in table
                 if c.targetedBy
                 and c.targetedBy == me]
   if len(targetCards) == 0: return
### I think the below is not necessary from experience ###
#   if not confirm("You are about to trash your opponent's cards. This may cause issue if your opponent is currently manipulating them\
#             \nPlease ask your opponent to wait until the notification appears before doing anything else\
#           \n\nProceed?"): return
   for card in targetCards:
      storeProperties(card)
      cardType = fetchProperty(card, 'Type')
      if ds == 'corp':
         if cardType != 'Resource' and not confirm("Only resources can be trashed from the runner.\n\nBypass Restriction?"): continue
         if not card.controller.Tags and not confirm("You can only Trash the runner's resources when they're tagged\n\nBypass Restriction?"): continue
         ClickCost = useClick()
         if ClickCost == 'ABORT': return
         intTrashCard(card, 2, ClickCost = ClickCost)
      else:
         if cardType != 'Upgrade' and cardType != 'Asset' and not confirm("You can normally only pay to trash the Corp's Nodes and Upgrades.\n\nBypass Restriction?"): continue
         intTrashCard(card, fetchProperty(card, 'Stat')) # If we're a runner, trash with the cost of the card's trash.

def exileCard(card, silent = False):
   debugNotify(">>> exileCard(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the shared pile and outside of view.
   mute()
   storeProperties(card)
   if fetchProperty(card, 'Type') == "Tracing" or fetchProperty(card, 'Type') == "Counter Hold" or fetchProperty(card, 'Type') == "Server":
      whisper("This kind of card cannot be exiled!")
      return 'ABORT'
   else:
      if card.isFaceUp: MUtext = chkRAM(card, 'UNINSTALL')
      else: MUtext = ''
      if card.markers[mdict['Scored']]:
         if card.Type == 'Agenda': APloss = num(card.Stat)
         else: APloss = card.markers[mdict['Scored']] # If we're trashing a card that's not an agenda but nevertheless counts as one, the amount of scored counters are the AP it provides.
         me.counters['Agenda Points'].value -= APloss # Trashing Agendas for any reason, now takes they value away as well.
         notify("--> {} loses {} Agenda Points".format(me, APloss))
      if card.markers[mdict['ScorePenalty']]: # A card with Score Penalty counters was giving us minus agenda points. By exiling it, we recover those points.
         if card.Type == 'Agenda': APgain = num(card.Stat)
         else: APgain = card.markers[mdict['ScorePenalty']]
         me.counters['Agenda Points'].value += APgain 
         notify("--> {} recovers {} Agenda Points".format(me, APgain))
         if me.counters['Agenda Points'].value >= 7 or (getSpecial('Identity',fetchCorpPL()).name == "Harmony Medtech" and me.counters['Agenda Points'].value >= 6):
            notify("{} wins the game!".format(me))
            reportGame() # If we removed agenda points penalty (e.g. Data Dealer a Shi.Kyu) and that made us reach 7 agenda points, we can win the game at this point.
      executePlayScripts(card,'TRASH') # We don't want to run automations on simply revealed cards.
      clearAttachLinks(card)
      changeCardGroup(card,card.owner.piles['Removed from Game'])
   if not silent: notify("{} exiled {}{}.".format(me,card,MUtext))

def uninstall(card, x=0, y=0, destination = 'hand', silent = False):
   debugNotify(">>> uninstall(){}".format(extraASDebug())) #Debug
   # Returns an installed card into our hand.
   mute()
   storeProperties(card)
   if destination == 'R&D' or destination == 'Stack': group = card.owner.piles['R&D/Stack']
   else: group = card.owner.hand
   #confirm("destination: {}".format(destination)) # Debug
   if fetchProperty(card, 'Type') == "Tracing" or fetchProperty(card, 'Type') == "Counter Hold" or (fetchProperty(card, 'Type') == "Server" and fetchProperty(card, 'name') != "Remote Server"):
      whisper("This kind of card cannot be uninstalled!")
      return 'ABORT'
   else:
      if card.isFaceUp: MUtext = chkRAM(card, 'UNINSTALL')
      else: MUtext = ''
      executePlayScripts(card,'UNINSTALL')
      autoscriptOtherPlayers('CardUninstalled',card)
      clearAttachLinks(card)
      card.moveTo(group)
   if not silent: notify("{} uninstalled {}{}.".format(me,card,MUtext))

def useCard(card,x=0,y=0):
   debugNotify(">>> useCard(){}".format(extraASDebug())) #Debug
   if card.highlight == None or card.highlight == NewCardColor:
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
   debugNotify(">>> prioritize(){}".format(extraASDebug())) #Debug
   if card.highlight == None:
      card.highlight = PriorityColor
      notify ("{} prioritizes {} for using counters automatically.".format(me,card))
      if getSetting('PriorityInform',True):
         information("This action prioritizes a card for when selecting which card will use its counters from automated effects\
                    \nSuch automated effects include losing counters from stealth cards for using noisy icebreakers, or preventing damage\
                  \n\nSelecting a card for priority gives it first order in the pick. So it will use its counters before any other card will\
                  \n\nThe second order of priority is targeting a card. A card that is targeted at the time of the effect, will lose its counters after all cards highlighted with priority have\
                  \n\nFinally, if any part of the effect is left requiring the use of counters, any card without priority or targeted will be used.\
                  \n\nKeep this in mind if you wish to fine tune which cards use their counter automatically first\
                    \n(This message will not appear again)")
         setSetting('PriorityInform',False)
   else:
      if card.highlight == DummyColor:
         information(":::ERROR::: This highlight signifies that this card is a lingering effect left behind from the original\
                \nYou cannot prioritize such cards as they would lose their highlight and thus create problems with automation.\
                \nIf you want one such card to use counter before others, simply target (shift+click) it for the duration of the effect.")
         return
      notify("{} clears {}'s priority.".format(me, card))
      card.highlight = None
      card.target(False)

def stealthReserve(card,x=0,y=0):
   debugNotify(">>> prioritize(){}".format(extraASDebug())) #Debug
   if card.highlight == None:
      card.highlight = StealthColor
      notify ("{} reserves credits on {} for stealth cards.".format(me,card))
   else:
      if card.highlight == DummyColor:
         information(":::ERROR::: This highlight signifies that this card is a lingering effect left behind from the original\
                \nYou cannot reserve such cards for stealth as they would lose their highlight and thus create problems with automation.\
                \nIf you want one such card to use counter before others, simply target (shift+click) it for the duration of the effect.")
         return
      notify("{} clears {}'s stealth reservation.".format(me, card))
      card.highlight = None
      card.target(False)
      
def rulings(card, x = 0, y = 0):
   debugNotify(">>> rulings(){}".format(extraASDebug())) #Debug
   mute()
   #if not card.isFaceUp: return
   #openUrl('http://www.netrunneronline.com/cards/{}/'.format(card.Errata))
   if card.Subtitle != '': subTXT = ':' + card.Subtitle
   else: subTXT = ''
   openUrl('http://netrunnerdb.com/find/?q={}{}'.format(fetchProperty(card, 'name'),subTXT)) # Errata is not filled in most card so this works better until then

def inspectCard(card, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectCard(){}".format(extraASDebug())) #Debug
   ASText = "This card has the following automations:"
   if re.search(r'onPlay', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will have an effect when coming into play from your hand.'
   if re.search(r'onScore', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will have an effect when being scored.'
   if re.search(r'onRez', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will have an effect when its being rezzed.'
   if re.search(r'onInstall', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will have an effect when its being installed.'
   if re.search(r'whileRezzed', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will has a continous effect while in play.'
   if re.search(r'whileScored', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will has a continous effect while scored.'
   if re.search(r'whileRunning', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will has a continous effect while running.'
   if re.search(r'atTurnStart', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will perform an automation at the start of your turn.'
   if re.search(r'atTurnEnd', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will perform an automation at the end of your turn.'
   if re.search(r'atRunStart', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will perform an automation at the start of your run.'
   if re.search(r'atJackOut', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will perform an automation at the end of a run.'
   if re.search(r'onAccess', Stored_AutoScripts.get(card._id,'')): ASText += '\n * It will perform an automation when the runner accesses it.'
   if CardsAA.get(card.model,'') != '' or Stored_AutoActions.get(card._id,'') != '':
      debugNotify("We have AutoActions", 2) #Debug
      if ASText == 'This card has the following automations:': ASText = '\nThis card will perform one or more automated actions when you double click on it.'
      else: ASText += '\n\nThis card will also perform one or more automated actions when you double click on it.'
   if ASText == 'This card has the following automations:': ASText = '\nThis card has no automations.'
   #if fetchProperty(card, 'name') in automatedMarkers:
   #   ASText += '\n\nThis card can create markers, which also have automated effects.'
   if card.type == 'Tracing': information("This is your tracing card. Double click on it to reinforce your trace or base link.\
                                         \nIt will ask you for your bid and then take the same amount of credits from your bank automatically")
   elif card.type == 'Server': information("These are your Servers. Start stacking your Ice above them and your Agendas, Upgrades and Nodes below them.\
                                     \nThey have no automated abilities so remember to manually pay credits for every ICE you install after the first!")
   elif card.type == 'Counter Hold': information("This is your Counter Hold. This card stores all the beneficial and harmful counters you might accumulate over the course of the game.\
                                          \n\nIf you're playing a corp, Bad Publicity, viruses and other such tokens may be put here as well. By double clicking this card, you'll use three clicks to clean all viruses from your cards.\
                                          \nIf you're playing a runner, brain damage markers, tags and any other tokens the corp gives you will be put here. by double clicking this card, you'll be able to select one of the markers to remove by paying its cost.\
                                        \n\nTo remove any token manually, simply drag & drop it out of this card.")
   elif card.type == 'Button': information("This is a button to help you quickly shout announcements to your opponent.\
                                          \nTo use a card button just double click on it.\
                                        \n\nThe Various buttons are: \
                                        \n\n* 'Access Imminent': Use this before you press F3 for a successful run, if you want to give the corporation an opportunity to rez upgrades/assets or use paid abilities\
                                        \n\n* 'No Rez': Use this as a corp to inform the runner you're not rezzing the currently approached ICE.\
                                        \n\n* 'Wait': Use this if you want to stop the opponent while you play reactions.\
                                        \n\n* 'OK': Use this to inform your opponent you have no more reactions to play.")
   else:
      if debugVerbosity > 0: finalTXT = 'AutoScript: {}\n\n AutoAction: {}'.format(CardsAS.get(card.model,''),CardsAA.get(card.model,''))
      else: finalTXT = "Card Text: {}\n\n{}\n\nWould you like to see the card's details online?".format(card.Rules,ASText)
      if confirm("{}".format(finalTXT)): rulings(card)

def inspectTargetCard(group, x = 0, y = 0): # This function shows the player the card text, to allow for easy reading until High Quality scans are procured.
   debugNotify(">>> inspectTargetCard(){}".format(extraASDebug())) #Debug
   for card in table:
      if card.targetedBy and card.targetedBy == me: inspectCard(card)
      
#------------------------------------------------------------------------------
# Hand Actions
#------------------------------------------------------------------------------

def currentHandSize(player = me):
   debugNotify(">>> currentHandSizel(){}".format(extraASDebug())) #Debug
   specialCard = getSpecial('Identity', player)
   if specialCard.markers[mdict['BrainDMG']]: currHandSize =  player.counters['Hand Size'].value - specialCard.markers[mdict['BrainDMG']]
   else: currHandSize = player.counters['Hand Size'].value
   return currHandSize

def intPlay(card, cost = 'not free', scripted = False, preReduction = 0, retainPos = False):
   debugNotify(">>> intPlay(){}".format(extraASDebug())) #Debug
   global gatheredCardList
   gatheredCardList = False # We reset this variable because we can call intPlay from other scripts. And at that point we want to re-scan the table.
   extraText = '' # We set this here, because the if clause that may modify this variable will not be reached in all cases. So we need to set it to null here to avoid a python error later.
   mute()
   chooseSide() # Just in case...
   if not scripted: whisper("+++ Processing. Please Hold...")
   storeProperties(card)
   recalcMU()
   update()
   if not checkNotHardwareConsole(card, manual = retainPos): return	#If player already has a Console in play and doesnt want to play that card, do nothing.
   if card.Type != 'ICE' and card.Type != 'Agenda' and card.Type != 'Upgrade' and card.Type != 'Asset': # We only check for uniqueness on install, against cards that install face-up
      if not checkUnique(card, manual = retainPos): return #If the player has the unique card and opted not to trash it, do nothing.
   if card.Type == 'Program' and me.MU - num(fetchProperty(card,'Requirement')) < 0 and not confirm("It appears as if you're about to run out of MU if you install this card (We haven't checked for daemon hosting yet though). Proceed anyway?"): return
   if scripted: NbReq = 0
   elif re.search(r'Double', getKeywords(card)) and not chkDoublePrevention():
      NbReq = 2 # Some cards require two clicks to play. This variable is passed to the useClick() function.
   else: NbReq = 1 #In case it's not a "Double" card. Then it only uses one click to play.
   ClickCost = useClick(count = NbReq, manual = retainPos)
   if ClickCost == 'ABORT': 
      if retainPos: card.moveTo(me.hand)
      return  #If the player didn't have enough clicks and opted not to proceed, do nothing.
   if (card.Type == 'Operation' or card.Type == 'Event') and chkTargeting(card) == 'ABORT': 
      me.Clicks += NbReq # We return any used clicks in case of aborting due to missing target
      card.moveTo(me.hand)
      return 'ABORT'# If it's an Operation or Event and has targeting requirements, check with the user first.
   host = chkHostType(card)
   debugNotify("host received: {}".format(host), 4)
   if host:
      try:
         if host == 'ABORT':
            me.Clicks += NbReq
            if retainPos: card.moveTo(me.hand)
            return 'ABORT'
      except: # If there's an exception, it means that the host is a card object which cannot be compared to a string
         debugNotify("Found Host", 2)
         hostTXT = ' on {}'.format(host) # If the card requires a valid host and we found one, we will mention it later.
   else:
      debugNotify("No Host Requirement", 2)
      hostTXT = ''
   debugNotify("Finished Checking Host Requirements", 2)
   if card.Type == 'Event' or card.Type == 'Operation': action = 'PLAY'
   else: action = 'INSTALL'
   MUtext = ''
   rc = ''
   if card.Type == 'Resource' and re.search(r'Hidden', getKeywords(card)): hiddenresource = 'yes'
   else: hiddenresource = 'no'
   expectedCost = num(card.Cost) - preReduction
   if expectedCost < 0: expectedCost = 0
   if card.Type == 'ICE' or card.Type == 'Agenda' or card.Type == 'Asset' or card.Type == 'Upgrade':
      placeCard(card, action, retainPos = retainPos)
      if fetchProperty(card, 'Type') == 'ICE': card.orientation ^= Rot90 # Ice are played sideways.
      notify("{} to install a card.".format(ClickCost))
      #card.isFaceUp = False # Now Handled by placeCard()
   elif card.Type == 'Program' or card.Type == 'Event' or card.Type == 'Resource' or card.Type == 'Hardware':
      MUtext = chkRAM(card)
      if card.Type == 'Resource' and hiddenresource == 'yes':
         placeCard(card, action, retainPos = retainPos)
         executePlayScripts(card,action)
         card.isFaceUp = False
         notify("{} to install a hidden resource.".format(ClickCost))
         return
      if cost == 'not free': # If the cost is not free, then we check for cost reductors/increasers and do a dryrun to gather how much the reduction is going to be.
         reduction = reduceCost(card, action, expectedCost, dryRun = True) #Checking to see if the cost is going to be reduced by cards we have in play.
         if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.
         elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: reduction = 0
      rc = payCost(expectedCost - reduction, cost)
      if rc == "ABORT":
         me.Clicks += NbReq # If the player didn't notice they didn't have enough credits, we give them back their click
         if retainPos: card.moveTo(me.hand)
         return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": 
         extraText = " at no cost"
         rc = ''
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = ''
      if cost == 'not free': reduction = reduceCost(card, action, expectedCost) # Now we go ahead and actually remove any markers from cards
      placeCard(card, action, retainPos = retainPos)
      if card.Type == 'Program':
         for targetLookup in table: # We check if we're targeting a daemon to install the program in.
            if targetLookup.targetedBy and targetLookup.targetedBy == me and (re.search(r'Daemon',getKeywords(targetLookup)) or re.search(r'CountsAsDaemon', CardsAS.get(targetLookup.model,''))) and possess(targetLookup, card, silent = True) != 'ABORT':
               MUtext = ", installing it into {}".format(targetLookup)
               break
         notify("{}{} to install {}{}{}{}.".format(ClickCost, rc, card, hostTXT, extraText,MUtext))
      elif card.Type == 'Event': notify("{}{} to prep with {}{}.".format(ClickCost, rc, card, extraText))
      elif card.Type == 'Hardware': notify("{}{} to setup {}{}{}{}.".format(ClickCost, rc, card, hostTXT, extraText,MUtext))
      elif card.Type == 'Resource' and hiddenresource == 'no': notify("{}{} to acquire {}{}{}{}.".format(ClickCost, rc, card, hostTXT, extraText,MUtext))
      else: notify("{}{} to play {}{}{}.".format(ClickCost, rc, card, extraText,MUtext))
   else:
      if cost == 'not free': 
         reduction = reduceCost(card, action, expectedCost, dryRun = True) #Checking to see if the cost is going to be reduced by cards we have in play.
         if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.
         elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: reduction = 0
      rc = payCost(expectedCost - reduction, cost)
      if rc == "ABORT":
         me.Clicks += NbReq # If the player didn't notice they didn't have enough credits, we give them back their click
         if retainPos: card.moveTo(me.hand)
         return 'ABORT' # If the player didn't have enough money to pay and aborted the function, then do nothing.
      elif rc == "free": 
         extraText = " at no cost"
         rc = ''
      elif rc != 0: rc = " and pays {}".format(rc)
      else: rc = '' # When the cast costs nothing, we don't include the cost.
      if cost == 'not free': reduction = reduceCost(card, action, expectedCost)
      placeCard(card, action, retainPos = retainPos)
      if card.Type == 'Operation': notify("{}{} to initiate {}{}.".format(ClickCost, rc, card, extraText))
      else: notify("{}{} to play {}{}.".format(ClickCost, rc, card, extraText))
   if re.search('Current',getKeywords(card)): clearCurrents(card = card) # If the card just played was a current, we clear all other currents on the table.
   playInstallSound(card)
   card.highlight = NewCardColor # We give all new cards an orange highlight to make them easiet to see.
   playEvOpSound(card)
   executePlayScripts(card,action)
   autoscriptOtherPlayers('Card'+action.capitalize(),card) # we tell the autoscriptotherplayers that we installed/played a card. (e.g. See Haas-Bioroid ability)
   if debugVerbosity >= 3: notify("<<< intPlay().action: {}\nAutoscriptedothers: {}".format(action,'Card'+action.capitalize())) #Debug
   if debugVerbosity >= 1:
      if Stored_Type.get(card._id,None): notify("++++ Stored Type: {}".format(fetchProperty(card, 'Type')))
      else: notify("++++ No Stored Type Found for {}".format(card))
      if Stored_Keywords.get(card._id,None): notify("++++ Stored Keywords: {}".format(fetchProperty(card, 'Keywords')))
      else: notify("++++ No Stored Keywords Found for {}".format(card))
      if Stored_Cost.get(card._id,None): notify("++++ Stored Cost: {}".format(fetchProperty(card, 'Cost')))
      else: notify("++++ No Stored Cost Found for {}".format(card))

def playForFree(card, x = 0, y = 0):
   debugNotify(">>> playForFree(){}".format(extraASDebug())) #Debug
   intPlay(card,"free")

def movetoTopOfStack(card):
   debugNotify(">>> movetoTopOfStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   card.moveTo(deck)
   notify ("{} moves a card to top of their {}.".format(me,pileName(deck)))

def movetoBottomOfStack(card, silent = False):
   debugNotify(">>> movetoBottomOfStack(){}".format(extraASDebug())) #Debug
   # Puts the removed card in the shared pile and outside of view.
   mute()
   storeProperties(card)
   if fetchProperty(card, 'Type') == "Tracing" or fetchProperty(card, 'Type') == "Counter Hold" or fetchProperty(card, 'Type') == "Server":
      whisper("This kind of card cannot be removed from the table!")
      return 'ABORT'
   else:
      if card.isFaceUp and card.group == table: MUtext = chkRAM(card, 'UNINSTALL')
      else: MUtext = ''
      clearAttachLinks(card)
      changeCardGroup(card,card.owner.piles['R&D/Stack'],True)
   if not silent: notify("{} sent {} to the bottom of {}{}.".format(me,card,pileName(card.owner.piles['R&D/Stack']),MUtext))
   
def handtoArchives(card):
   debugNotify(">>> handtoArchives(){}".format(extraASDebug())) #Debug
   if ds == "runner": return
   mute()
   card.moveTo(me.piles['Heap/Archives(Face-up)'])
   notify ("{} moves a card to their face-up Archives.".format(me))

def handDiscard(card, scripted = False):
   debugNotify(">>> handDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if not scripted: playDiscardHandCardSound()
   if ds == "runner":
      card.moveTo(me.piles['Heap/Archives(Face-up)'])
      if endofturn:
         if card.Type == 'Program': notify("{} has killed a hanging process ({}).".format(me,card))
         elif card.Type == 'Event': notify("{} has thrown away some notes ({}).".format(me,card))
         elif card.Type == 'Hardware': notify("{} has deleted some spam mail ({}).".format(me,card))
         elif card.Type == 'Resource': notify("{} has reconfigured some net protocols ({}).".format(me,card))
         else: notify("{} has power cycled some hardware.".format(me))
         if len(me.hand) == currentHandSize():
            notify("{} has now discarded down to their max handsize of {}".format(me, currentHandSize()))
            goToEndTurn(table, 0, 0)
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
            goToEndTurn(table, 0, 0)
      else: notify("{} discards a card.".format(me))

def handRandomDiscard(group = None, count = None, player = None, destination = None, silent = False):
   debugNotify(">>> handRandomDiscard(){}".format(extraASDebug())) #Debug
   mute()
   if not player: player = me
   if not group: group = me.hand
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
      debugNotify(" : handRandomDiscard() iter: {}".format(iter + 1), 3) # Debug
      card = group.random()
      if card == None: return iter + 1 # If we have no more cards, then return how many we managed to discard.
      card.moveTo(destination)
      if not silent: notify("{} discards {} at random.".format(player,card))
   debugNotify("<<< handRandomDiscard() with return {}".format(iter + 1), 2) #Debug
   return iter + 1 #We need to increase the iter by 1 because it starts iterating from 0

def showatrandom(group = None, count = 1, targetPL = None, silent = False, covered = False):
   debugNotify(">>> showatrandom(){}".format(extraASDebug())) #Debug
   mute()
   shownCards = []
   side = 1
   if not targetPL: targetPL = me
   if not group: group = targetPL.hand
   if targetPL != me: side = -1
   if len(group) == 0:
      whisper(":::WARNING::: {} had no cards in their hand!".format(targetPL))
      return shownCards
   elif count > len(group):
      whisper(":::WARNING::: {} has only {} cards in their hand.".format(targetPL,len(group)))
      count = len(group)
   # if group == targetPL.hand: # Disabling because it seems buggy and slow.
      # for c in group:  c.moveTo(targetPL.ScriptingPile)        
      # targetPL.ScriptingPile.shuffle()
      # for c in targetPL.ScriptingPile: c.moveTo(targetPL.hand)
   for iter in range(count):
      card = group.random()
      if card.controller != me: # If we're revealing a card from another player's hand, we grab its properties before we put it on the table, as as not to give away if we're scanning it right now or not.
         card.isFaceUp = True
         storeProperties(card, forced = False)
      time.sleep(1)
      if card == None:
         notify(":::Info:::{} has no more cards in their hand to reveal".format(targetPL))
         break
      if covered:
         cover = table.create("ac3a3d5d-7e3a-4742-b9b2-7f72596d9c1b",playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side,1,False)
         cover.moveToTable(playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side,False)
      card.moveToTable(playerside * side * iter * cwidth(card) - (count * cwidth(card) / 2), 0 - yaxisMove(card) * side, False)
      card.highlight = RevealedColor
      card.sendToBack()
      if not covered: loopChk(card) # A small delay to make sure we grab the card's name to announce
      shownCards.append(card) # We put the revealed cards in a list to return to other functions that call us
   if not silent: notify("{} reveals {} at random from their hand.".format(targetPL,card))
   debugNotify("<<< showatrandom() with return {}".format(card), 2) #Debug
   return shownCards

def showDirect(cardList):
   debugNotify(">>> showDirect(){}".format(extraASDebug())) #Debug
   mute()
   if cardList[0].owner != me: side = -1
   else: side = 1
   for iter in range(len(cardList)):
      card = cardList[iter]
      card.moveToTable(playerside * side * iter * cwidth(card) - (len(cardList) * cwidth(card) / 2), 0 - yaxisMove(card) * side, False)
      card.highlight = RevealedColor
      card.sendToBack()
      storeProperties(card, forced = False)
      loopChk(card) # A small delay to make sure we grab the card's name to announce
   debugNotify("<<< showDirect()") #Debug

def groupToDeck (group = me.hand, player = me, silent = False):
   debugNotify(">>> groupToDeck(){}".format(extraASDebug())) #Debug
   mute()
   deck = player.piles['R&D/Stack']
   count = len(group)
   for c in group: c.moveTo(deck)
   if not silent: notify ("{} moves their whole {} to their {}.".format(player,pileName(group),pileName(deck)))
   if debugVerbosity >= 3: notify("<<< groupToDeck() with return:\n{}\n{}\n{}".format(pileName(group),pileName(deck),count)) #Debug
   else: return(pileName(group),pileName(deck),count) # Return a tuple with the names of the groups.

def mulligan(group):
   debugNotify(">>> mulligan(){}".format(extraASDebug())) #Debug
   if not confirm("Are you sure you want to take a mulligan?"): return
   notify("{} is taking a Mulligan...".format(me))
   groupToDeck(group,silent = True)
   resetAll()
   for i in range(1):
      rnd(1,10)
      shuffle(me.piles['R&D/Stack']) # We do a good shuffle this time.
      whisper("Shuffling...")
   drawMany(me.piles['R&D/Stack'], 5)
   executePlayScripts(Identity,'MULLIGAN')
   debugNotify("<<< mulligan()", 3) #Debug

#------------------------------------------------------------------------------
# Pile Actions
#------------------------------------------------------------------------------
def shuffle(group):
   debugNotify(">>> shuffle(){}".format(extraASDebug())) #Debug
   group.shuffle()

def draw(group):
   debugNotify(">>> draw(){}".format(extraASDebug())) #Debug
   global newturn
   mute()
   if len(group) == 0:
      if ds == 'corp':
         notify(":::ATTENTION::: {} cannot draw another card. {} loses the game!".format(me,me))
         reportGame('DeckDefeat')
      else:
         whisper(":::ERROR::: No more cards in your stack")
      return
   card = group.top()
   if ds == 'corp' and newturn: notify("--> {} performs the turn's mandatory draw.".format(me))
   else:
      ClickCost = useClick()
      if ClickCost == 'ABORT': return
      notify("{} to draw a card.".format(ClickCost))
      playClickDrawSound()
   changeCardGroup(card,me.hand)      
   dailyList = [card]
   dailyBusiness = chkDailyBusinessShows() # Due to its automated wording, I have to hardcode this on every card draw.
   if dailyBusiness:
      for c in group.top(dailyBusiness):
         dailyList.append(c)
         changeCardGroup(c,me.hand)
      for iter in range(dailyBusiness):
         returnedCard = askCard(dailyList)
         returnedCard.moveToBottom(group)
   if not (ds == 'corp' and newturn): autoscriptOtherPlayers('CardDrawnClicked',card)
   if ds == 'corp' and newturn: newturn = False # Need to do this later so as not to trigger autoscripts from the mnandatory draw.
   if len(group) <= 3 and ds == 'corp': notify(":::WARNING::: {} is about to be decked! R&D down to {} cards.".format(me,len(group)))
   storeProperties(card)

def drawMany(group, count = None, destination = None, silent = False):
   debugNotify(">>> drawMany(){}".format(extraASDebug())) #Debug
   debugNotify("source: {}".format(group.name), 2)
   if destination: debugNotify("destination: {}".format(destination.name), 2)
   mute()
   if destination == None: destination = me.hand
   SSize = len(group)
   if SSize == 0: return 0
   if count == None: count = askInteger("Draw how many cards?", 5)
   if count == None: return 0
   if count > SSize:
      if group.player == me and group == me.piles['R&D/Stack'] and destination == me.hand and ds == 'corp':
         if confirm("You do not have enough cards in your R&D to draw. Continuing with this action will lose you the game. Proceed?"):
            notify(":::ATTENTION::: {} cannot draw the full amount of cards. {} loses the game!".format(me,me))
            reportGame('DeckDefeat')
            return count
         else: 
            notify(":::WARNING::: {} canceled the card draw effect to avoid decking themselves".format(me))
            return 0
      else: 
         count = SSize
         whisper("You do not have enough cards in your deck to complete this action. Will draw as many as possible")
   if destination == me.hand and group == me.piles['R&D/Stack']: # Due to its automated wording, I have to hardcode this on every card draw.
      dailyList = []
      dailyBusiness = chkDailyBusinessShows() 
   else: dailyBusiness = 0
   for c in group.top(count):
      if dailyBusiness:
         dailyList.append(c)
      changeCardGroup(c,destination)
      #c.moveTo(destination)
   if dailyBusiness:
      for c in group.top(dailyBusiness):
         dailyList.append(c)
         changeCardGroup(c,destination)
      for iter in range(dailyBusiness):
         returnedCard = askCard(dailyList)
         returnedCard.moveToBottom(group)
   if not silent: notify("{} draws {} cards.".format(me, count))
   if len(group) <= 3 and group.player.getGlobalVariable('ds') == 'corp': notify(":::WARNING::: {} is about to be decked! R&D down to {} cards.".format(group.player,len(group)))
   debugNotify("<<< drawMany() with return: {}".format(count), 3)
   return count

def chkDailyBusinessShows():
   found = 0
   for c in table:
      if c.name == "Daily Business Show" and c.controller == me and c.orientation == Rot0:
         found += 1
         c.orientation = Rot90
   return found
def toarchives(group = me.piles['Archives(Hidden)']):
   debugNotify(">>> toarchives(){}".format(extraASDebug())) #Debug
   mute()
   Archives = me.piles['Heap/Archives(Face-up)']
   for c in group: c.moveTo(Archives)
   #Archives.shuffle()
   notify ("{} moves Hidden Archives to their Face-Up Archives.".format(me))

def archivestoStack(group, silent = False):
   debugNotify(">>> archivestoStack(){}".format(extraASDebug())) #Debug
   mute()
   deck = me.piles['R&D/Stack']
   for c in group: c.moveTo(deck)
   #Archives.shuffle()
   if not silent: notify ("{} moves their {} to {}.".format(me,pileName(group),pileName(deck)))
   else: return(pileName(group),pileName(deck))

def mill(group):
   debugNotify(">>> mill(){}".format(extraASDebug())) #Debug
   if len(group) == 0: return
   mute()
   count = askInteger("Mill how many cards?", 1)
   if count == None: return
   if ds == "runner": destination = me.piles['Heap/Archives(Face-up)']
   else: destination = me.piles['Archives(Hidden)']
   for c in group.top(count): c.moveTo(destination)
   notify("{} mills the top {} cards from their {} to {}.".format(me, count,pileName(group),pileName(destination)))

def moveXtopCardtoBottomStack(group):
   debugNotify(">>> moveXtopCardtoBottomStack(){}".format(extraASDebug())) #Debug
   mute()
   if len(group) == 0: return
   count = askInteger("Move how many cards?", 1)
   if count == None: return
   for c in group.top(count): c.moveToBottom(group)
   notify("{} moves the top {} cards from their {} to the bottom of {}.".format(me, count,pileName(group),pileName(group)))

