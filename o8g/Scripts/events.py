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

flipBoard = 1 # If True, it signifies that the table board has been flipped because the runner is on the side A
ds = None # The side of the player. 'runner' or 'corp'
flipModX = 0
flipModY = 0

def chkTwoSided():
   mute()
   if not table.isTwoSided(): information(":::WARNING::: This game is designed to be played on a two-sided table. Things will be extremely uncomfortable otherwise!! Please start a new game and make sure  the appropriate button is checked")
   fetchCardScripts() # We only download the scripts at the very first setup of each play session.
   versionCheck()
   prepPatronLists()
   checkQuickAccess()

def checkDeck(player,groups):
   debugNotify(">>> checkDeck(){}".format(extraASDebug())) #Debug
   #confirm("raw groups = {}".format(groups))
   #confirm("group names= {}".format([g.name for g in groups]))
   if player != me: return # We only want the owner of to run this script
   mute()
   global totalInfluence, Identity, ds
   notify (" -> Checking deck of {} ...".format(me))
   ok = True
   group = me.piles['R&D/Stack']
   ds = None
   for card in me.hand:
      if card.Type != 'Identity':
         whisper(":::Warning::: You are not supposed to have any non-Identity cards in your hand when you start the game")
         card.moveToBottom(me.piles['R&D/Stack'])
         continue
      else:
         ds = card.Side.lower()
         me.setGlobalVariable('ds', ds)
         storeSpecial(card)
         Identity = card
   debugNotify("About to fetch Identity card", 4) #Debug
   if not Identity: 
      delayed_whisper(":::ERROR::: Please Reset and load a deck with an Identity included. Aborting!")
      return
   loDeckCount = len(group)
   debugNotify("About to check Identity min deck size.", 4) #Debug
   if loDeckCount < num(Identity.Requirement): # For identities, .Requirement is the card minimum they have.
      ok = False
      notify ( ":::ERROR::: Only {} cards in {}'s Deck. {} Needed!".format(loDeckCount,me,num(Identity.Requirement)))
   mute()
   loAP = 0
   loInf = 0
   loRunner = False
   agendasCount = 0
   #debugNotify("About to move cards into me.ScriptingPile", 4) #Debug
   debugNotify("About to get visibility", 4) #Debug
   group.setVisibility('me')
   #for card in group: card.moveTo(me.ScriptingPile)
   #if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
   debugNotify("About to check each card in the deck", 4) #Debug
   counts = collections.defaultdict(int)
   CardLimit = {}
   professorsRig = [] # This is used by "The Professor" to avoid counting influence for the first instance of a program.
   for card in group:
      #setAwareness(card)
      counts[card.name] += 1
      if counts[card.name] > 3:
         notify(":::ERROR::: Only 3 copies of {} allowed.".format(card.name))
         ok = False
      if card.Type == 'Agenda':
         if ds == 'corp':
            loAP += num(card.Stat)
            agendasCount += 1
         else:
            notify(":::ERROR::: Agendas found in {}'s Stack.".format(me))
            ok = False
      elif card.Type in CorporationCardTypes and Identity.Faction in RunnerFactions:
         notify(":::ERROR::: Corporate cards found in {}'s Stack.".format(me))
         ok = False
      elif card.Type in RunnerCardTypes and Identity.Faction in CorporateFactions:
         notify(":::ERROR::: Runner cards found in {}'s R&Ds.".format(me))
         ok = False
      if num(card.Influence) and card.Faction != Identity.Faction:
         if Identity.model == 'bc0f047c-01b1-427f-a439-d451eda03029' and card.Type == 'Program' and card.model not in professorsRig:
            debugNotify("adding {} to prof. rig. card type = {}".format(card,card.Type))
            professorsRig.append(card.model) # First instance of a card is free of influence costs.
         else: 
            debugNotify("adding influence of {}. card type = {}".format(card,card.Type))
            loInf += num(card.Influence)
      else:
         if card.Type == 'Identity':
            notify(":::ERROR::: Extra Identity Cards found in {}'s {}.".format(me, pileName(group)))
            ok = False
         elif card.Faction != Identity.Faction and card.Faction != 'Neutral' and Identity.Faction != 'Neutral':
            notify(":::ERROR::: Faction-restricted card ({}) found in {}'s {}.".format(fetchProperty(card, 'name'), me, pileName(group)))
            ok = False
      if Identity.model == 'bc0f047c-01b1-427f-a439-d451eda00000' and card.Faction == 'Criminal':
         notify(":::ERROR::: Criminal cards found in a {} deck".format(Identity))
         ok = False
      if Identity.model == 'bc0f047c-01b1-427f-a439-d451eda03002' and card.Faction == 'Jinteki':
         notify(":::ERROR::: Jinteki cards found in a {} deck".format(Identity))
         ok = False
      if card.model in LimitedCard:
         if card.model not in CardLimit: CardLimit[card.model] = 1
         else: CardLimit[card.model] += 1
         if CardLimit[card.model] > 1: 
            notify(":::ERROR::: Duplicate Limited card ({}) found in {}'s {}.".format(card,me,pileName(group)))
            ok = False
   #if len(players) > 1: random = rnd(1,100) # Fix for multiplayer only. Makes Singleplayer setup very slow otherwise.
   #for card in me.ScriptingPile: card.moveToBottom(group) # We use a second loop because we do not want to pause after each check
   group.setVisibility('None')
   if ds == 'corp':
      requiredAP = 2 + 2 * int(loDeckCount / 5)
      if loAP not in (requiredAP, requiredAP + 1):
         notify(":::ERROR::: {} cards requires {} or {} Agenda Points, found {}.".format(loDeckCount, requiredAP, requiredAP + 1, loAP))
         ok = False
   if loInf > num(Identity.Stat) and Identity.Faction != 'Neutral':
      notify(":::ERROR::: Too much rival faction influence in {}'s R&D. {} found with a max of {}".format(me, loInf, num(Identity.Stat)))
      ok = False
   deckStats = (loInf,loDeckCount,agendasCount) # The deck stats is a tuple that we stored shared, and stores how much influence is in the player's deck, how many cards it has and how many agendas
   me.setGlobalVariable('Deck Stats',str(deckStats))
   debugNotify("Total Influence used: {} (Influence string stored is: {}".format(loInf, me.getGlobalVariable('Influence')), 2) #Debug
   if ok: notify("-> Deck of {} is OK!".format(me))
   else: 
      notify("-> Deck of {} is _NOT_ OK!".format(me))
      information("We have found illegal cards in your deck. Please load a legal deck!")
   debugNotify("<<< checkDeckNoLimit()") #Debug
   chkSideFlip()
  
def chkSideFlip(forced = False):
   mute()
   debugNotify(">>> chkSideFlip()")
   debugNotify("Checking Identity", 3)
   if not ds:
      information(":::ERROR::: No Identity found! Please load a deck which contains an Identity card before proceeding to setup.")
      return
   chooseSide()
   debugNotify("Checking side Flip", 3)
   if (ds == 'corp' and me.hasInvertedTable()) or (ds == 'runner' and not me.hasInvertedTable()): setGlobalVariable('boardFlipState','True')
   elif flipBoard == -1: setGlobalVariable('boardFlipState','False')
   else: debugNotify("Leaving Board as is")

def parseNewCounters(player,counter,oldValue):
   mute()
   debugNotify(">>> parseNewCounters() for player {} with counter {}. Old Value = {}".format(player,counter.name,oldValue))
   if counter.name == 'Tags' and player == me: chkTags()
   if counter.name == 'Bad Publicity' and oldValue < counter.value:
      if player == me: playSound('Gain-Bad_Publicity')
      for c in table: # Looking for cards which trigger off the corp gaining Bad Publicity
         if c.name == "Raymond Flint" and c.controller == me:
            if confirm("Do you want to activate Raymont Flint's ability at this point?\n\n(Make sure your opponent does not have a way to cancel this effect before continuing)"):
               HQaccess(silent = True)
   debugNotify("<<< parseNewCounters()")

def checkMovedCard(player,card,fromGroup,toGroup,oldIndex,index,oldX,oldY,x,y,isScriptMove,highlight = None,markers = None):
   mute()
   debugNotify("isScriptMove = {}".format(isScriptMove))
   if toGroup != me.piles['R&D/Stack'] and card.owner == me: superCharge(card) # First we check if we should supercharge the card, but only if the card is still on the same group at the time of execution.  
   if fromGroup == me.piles['R&D/Stack'] and toGroup == me.hand and ds == 'corp': # Code to store cards drawn by the corp to be exposed later by Bug
      if len([c for c in table if c.name == 'Bug']): setGlobalVariable('Bug Memory',card.name)
   if ds == 'runner' and card.controller == me and fromGroup != toGroup: recalcMU() # Any time a card enters or leaves the table, we recalculate MUs, just in case.
   if isScriptMove: return # If the card move happened via a script, then all further automations should have happened already.
   if fromGroup == me.hand and toGroup == table: 
      if card.Type == 'Identity': intJackin(manual = True)
      else: 
         if not card.isFaceUp: card.peek()
         if not re.search(r'onDragDrop:IgnoreCosts', CardsAS.get(card.model,'')): 
            intPlay(card, retainPos = True)
         elif re.search(r'onDragDrop:IgnoreCosts-isSourceShard', CardsAS.get(card.model,'')):
            notify("-- {} has discovered an {} instead of accessing cards".format(me,card))
            runSuccess(ShardSuccess = True)
   elif fromGroup != table and toGroup == table and card.owner == me: # If the player moves a card into the table from Deck or Trash, we assume they are installing it for free.
      if not card.isFaceUp: card.peek()
      if confirm("Play this card from {} for free?".format(pileName(fromGroup))):
         intPlay(card, cost = 'free', scripted = True, retainPos = True)
   elif fromGroup == table and toGroup != table and card.owner == me: # If the player dragged a card manually from the table to their discard pile...
      if card.isFaceUp and card.Type == 'Program': 
         chkRAM(card, 'UNINSTALL')
         notify(":> {} frees up {} MU".format(player,card.Requirement))
      if toGroup == player.piles['Archives(Hidden)'] or toGroup == player.piles['Heap/Archives(Face-up)']:
         if ds == 'runner': sendToTrash(card, player.piles['Heap/Archives(Face-up)']) # The runner cards always go to face-up archives
         else: sendToTrash(card, toGroup)
      else: 
         executePlayScripts(card,'UNINSTALL')
         autoscriptOtherPlayers('CardUninstalled',card)
         clearAttachLinks(card) # If the card was manually uninstalled or moved elsewhere than trash, then we simply take care of the MU and the attachments
   elif fromGroup == table and toGroup == table and card.owner == me: 
      orgAttachments(card)
      
def checkGlobalVars(name,oldValue,value):
   mute()
   if name == 'boardFlipState': checkBoardFlip(name,oldValue,value)
   if name == 'accessAttempts': checkAccessAttempts(name,oldValue,value)

def checkBoardFlip(name,oldValue,value):   
   global flipBoard, flipModX, flipModY
   if value == 'True':
      debugNotify("Flipping Board")
      flipBoard = -1
      flipModX = -61
      flipModY = -77
      table.setBoardImage("table\\Tabletop_flipped.png")
   else:
      debugNotify("Restoring Board Orientation")
      flipBoard = 1
      flipModX = 0
      flipModY = 0
      table.setBoardImage("table\\Tabletop.png") # If they had already reversed the table before, we set it back proper again   

def checkAccessAttempts(name,oldValue,value):
   if ds == 'corp' and num(value) >= 3:
      if confirm("The runner is currently waiting for final corporate reactions before proceeding to access the server. Do you have any cards to rez or paid abilities to use at this moment?"):
         notify(":::WARNING::: The Corporation delays access while they deliberate which reacts to trigger...")
      else: runSuccess()
         
def reconnectMe(group=table, x=0,y=0):
   reconnect()
   
def reconnect():
# An event which takes care to properly reset all the player variables after they reconnect to the game.
   global identName, Identity, lastKnownNrClicks, PriorityInform, ds
   fetchCardScripts(silent = True)
   for card in me.hand: storeProperties(card)
   for card in table:
      storeProperties(card)
      if card.Type == 'Identity' and card.owner == me:
         identName = card.name # The name of our current identity
         Identity = card
         ds = card.Side.lower()
      if card.Type == 'ICE': card.orientation = Rot90         
   lastKnownNrClicks = me.Clicks
   PriorityInform = False # Explains what the "prioritize card" action does.
   chkSideFlip()
   notify("::> {} has reconnected to the session!".format(me))
   