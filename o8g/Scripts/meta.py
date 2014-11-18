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
# This file contains scripts which are not used to play the actual game, but is rather related to the rules of engine
# * [Generic Netrunner] functions are not doing something in the game by themselves but called often by the functions that do.
# * In the [Switches] section are the scripts which controls what automations are active.
# * [Help] functions spawn tokens on the table with succint information on how to play the game.
# * [Button] functions are trigered either from the menu or from the button cards on the table, and announce a specific message each.
# * [Debug] if for helping the developers fix bugs
# * [Online Functions] is everything which connects to online files for some purpose, such as checking the game version or displaying a message of the day
###=================================================================================================================###
import re, time
#import sys # Testing
#import dateutil # Testing
#import elementtree # Testing
#import decimal # Testing

try:
    import os
    if os.environ['RUNNING_TEST_SUITE'] == 'TRUE':
        me = object
        table = object
except ImportError:
    pass

Automations = {'Play, Score and Rez'    : True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'Start/End-of-Turn'      : True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.
               'Damage Prevention'      : True, # If True, game will automatically use damage prevention counters from card they control.
               'Triggers'               : True, # If True, game will search the table for triggers based on player's actions, such as installing a card, or trashing one.
               'WinForms'               : True, # If True, game will use the custom Windows Forms for displaying multiple-choice menus and information pop-ups
               'Quick Access'           : False,# If True, game will enable quick access
               'Damage'                 : True}

UniCode = True # If True, game will display credits, clicks, trash, memory as unicode characters

debugVerbosity = -1 # At -1, means no debugging messages display

startupMsg = False # Used to check if the player has checked for the latest version of the game.

gameGUID = None # A Unique Game ID that is fetched during game launch.
#totalInfluence = 0 # Used when reporting online
#gameEnded = False # A variable keeping track if the players have submitted the results of the current game already.
turn = 0 # used during game reporting to report how many turns the game lasted
AccessBtnNextChoice = 0
askedQA = False

CardsAA = {} # Dictionary holding all the AutoAction scripts for all cards
CardsAS = {} # Dictionary holding all the AutoScript scripts for all cards


#---------------------------------------------------------------------------
# Generic Netrunner functions
#---------------------------------------------------------------------------
def uniCredit(count):
   debugNotify(">>> uniCredit(){}".format(extraASDebug())) #Debug
   count = num(count)
   if UniCode: return "{} ¥".format(count)
   else: 
      if count == 1: grammar = 's'
      else: grammar =''
      return "{} Credit{}".format(count,grammar)
 
def uniRecurring(count):
   debugNotify(">>> uniRecurring(){}".format(extraASDebug())) #Debug
   count = num(count)
   if UniCode: return "{} £".format(count)
   else: 
      if count == 1: grammar = 's'
      else: grammar =''
      return "{} Recurring Credit{}".format(count,grammar)
 
def uniClick():
   debugNotify(">>> uniClick(){}".format(extraASDebug())) #Debug
   if UniCode: return ' ⌚'
   else: return '(/)'

def uniTrash():
   debugNotify(">>> uniTrash(){}".format(extraASDebug())) #Debug
   if UniCode: return '⏏'
   else: return 'Trash'

def uniMU(count = 1):
   debugNotify(">>> uniMU(){}".format(extraASDebug())) #Debug
   if UniCode: 
      if num(count) == 1: return '⎗'
      elif num(count) == 2:  return '⎘'
      else: return '{} MU'.format(count)
   else: return '{} MU'.format(count)
   
def uniLink():
   debugNotify(">>> uniLink(){}".format(extraASDebug())) #Debug
   if UniCode: return '⎙'
   else: return 'Base Link'

def uniSubroutine():
   debugNotify(">>> uniLink(){}".format(extraASDebug())) #Debug
   if UniCode: return '⏎'
   else: return '[Subroutine]'

def chooseWell(limit, choiceText, default = None):
   debugNotify(">>> chooseWell(){}".format(extraASDebug())) #Debug
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
   debugNotify(">>> findMarker() on {} with markerDesc = {}".format(card,markerDesc)) #Debug
   foundKey = None
   if markerDesc in mdict: markerDesc = mdict[markerDesc][0] # If the marker description is the code of a known marker, then we need to grab the actual name of that.
   for key in card.markers:
      debugNotify("Key: {}\nmarkerDesc: {}".format(key[0],markerDesc), 3) # Debug
      if re.search(r'{}'.format(markerDesc),key[0]) or markerDesc == key[0]:
         foundKey = key
         debugNotify("Found {} on {}".format(key[0],card), 2)
         break
   debugNotify("<<< findMarker() by returning: {}".format(foundKey), 3)
   return foundKey
   
def getKeywords(card): # A function which combines the existing card keywords, with markers which give it extra ones.
   debugNotify(">>> getKeywords(){}".format(extraASDebug())) #Debug
   global Stored_Keywords
   #confirm("getKeywords") # Debug
   keywordsList = []
   cKeywords = card.Keywords # First we try a normal grab, if the card properties cannot be read, then we flip face up.
   if cKeywords == '?': cKeywords = fetchProperty(card, 'Keywords')
   strippedKeywordsList = cKeywords.split('-')
   for cardKW in strippedKeywordsList:
      strippedKW = cardKW.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
      if strippedKW: keywordsList.append(strippedKW) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.   
   if card.markers:
      for key in card.markers:
         markerKeyword = re.search('Keyword:([\w ]+)',key[0])
         if markerKeyword:
            #confirm("marker found: {}\n key: {}".format(markerKeyword.groups(),key[0])) # Debug
            #if markerKeyword.group(1) == 'Barrier' or markerKeyword.group(1) == 'Sentry' or markerKeyword.group(1) == 'Code Gate': #These keywords are mutually exclusive. An Ice can't be more than 1 of these
               #if 'Barrier' in keywordsList: keywordsList.remove('Barrier') # It seems in ANR, they are not so mutually exclusive. See: Tinkering
               #if 'Sentry' in keywordsList: keywordsList.remove('Sentry') 
               #if 'Code Gate' in keywordsList: keywordsList.remove('Code Gate')
            if re.search(r'Breaker',markerKeyword.group(1)):
               if 'Barrier Breaker' in keywordsList: keywordsList.remove('Barrier Breaker')
               if 'Sentry Breaker' in keywordsList: keywordsList.remove('Sentry Breaker')
               if 'Code Gate Breaker' in keywordsList: keywordsList.remove('Code Gate Breaker')
            keywordsList.append(markerKeyword.group(1))
   keywords = ''
   for KW in keywordsList:
      keywords += '{}-'.format(KW)
   Stored_Keywords[card._id] = keywords[:-1] # We also update the global variable for this card, which is used by many functions.
   debugNotify("<<< getKeywords() by returning: {}.".format(keywords[:-1]), 3)
   return keywords[:-1] # We need to remove the trailing dash '-'
   
def pileName(group):
   debugNotify(">>> pileName()") #Debug
   debugNotify("pile name {}".format(group.name), 2) #Debug   
   debugNotify("pile player: {}".format(group.player), 2) #Debug
   if group.name == 'Table': name = 'Table'
   elif group.name == 'Heap/Archives(Face-up)':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'Face-up Archives'
      else: name = 'Heap'
   elif group.name == 'R&D/Stack':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'R&D'
      else: name = 'Stack'
   elif group.name == 'Archives(Hidden)': name = 'Hidden Archives'
   else:
      if group.player.getGlobalVariable('ds') == 'corp': name = 'HQ'
      else: name = 'Grip'
   debugNotify("<<< pileName() by returning: {}".format(name), 3)
   return name

def clearNoise(): # Clears all player's noisy bits. I.e. nobody is considered to have been noisy this turn.
   debugNotify(">>> clearNoise()") #Debug
   for player in players: player.setGlobalVariable('wasNoisy', '0') 
   debugNotify("<<< clearNoise()", 3) #Debug

def storeSpecial(card): 
# Function stores into a shared variable some special cards that other players might look up.
   try:
      debugNotify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
      storeProperties(card, True)
      specialCards = eval(me.getGlobalVariable('specialCards'))
      if card.name == 'HQ' or card.name == 'R&D' or card.name == 'Archives':
         specialCards[card.name] = card._id # The central servers we find via name
      else: specialCards[card.Type] = card._id
      me.setGlobalVariable('specialCards', str(specialCards))
   except: notify("!!!ERROR!!! In storeSpecial()")

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   debugNotify(">>> getSpecial() for player: {}".format(me.name)) #Debug
   specialCards = eval(player.getGlobalVariable('specialCards'))
   cardID = specialCards.get(cardType,None)
   if not cardID: 
      debugNotify("No special card of type {} found".format(cardType),2)
      card = None
   else:
      card = Card(specialCards[cardType])
      debugNotify("Stored_Type = {}".format(Stored_Type.get(card._id,'NULL')), 2)
      if Stored_Type.get(card._id,'NULL') == 'NULL':
         #if card.owner == me: delayed_whisper(":::DEBUG::: {} was NULL. Re-storing as an attempt to fix".format(cardType)) # Debug
         debugNotify("card ID = {}".format(card._id))
         debugNotify("Stored Type = {}".format(Stored_Type.get(card._id,'NULL')))
         storeProperties(card, True)
   debugNotify("<<< getSpecial() by returning: {}".format(card), 3)
   return card

def chkRAM(card, action = 'INSTALL', silent = False):
   debugNotify(">>> chkRAM(){}".format(extraASDebug())) #Debug
   MUreq = num(fetchProperty(card,'Requirement'))
   hostCards = eval(getGlobalVariable('Host Cards'))
   if hostCards.has_key(card._id): hostC = Card(hostCards[card._id])
   else: hostC = None
   if (MUreq > 0
         and not (card.markers[mdict['DaemonMU']] and not re.search(r'Daemon',getKeywords(card)))
         and not findMarker(card,'Daemon Hosted MU')
         and not (card.markers[mdict['Cloud']] and card.markers[mdict['Cloud']] >= 1) # If the card is already in the cloud, we do not want to modify the player's MUs
         and not (hostC and findMarker(card, '{} Hosted'.format(hostC.name)) and hostC.name != "Scheherazade") # No idea if this will work.
         and card.highlight != InactiveColor 
         and card.highlight != RevealedColor):
      if action == 'INSTALL':
         #card.owner.MU -= MUreq
         chkCloud(card)
         update()
         if not card.markers[mdict['Cloud']]:
            MUtext = ", using up  {}".format(uniMU(MUreq))
         else: MUtext = ''
      elif action == 'UNINSTALL':
         #card.owner.MU += MUreq
         MUtext = ", freeing up  {}".format(uniMU(MUreq))
   else: MUtext = ''
   #if card.owner.MU < 0 and not silent: 
      #notify(":::Warning:::{}'s programs require more memory than they have available. They must trash enough programs to bring their available Memory to at least 0".format(card.controller))
      #information(":::ATTENTION:::\n\nYou are now using more MUs than you have available memory!\
                  #\nYou need to trash enough programs to bring your Memory to 0 or higher")
   debugNotify("<<< chkRAM() by returning: {}".format(MUtext), 3)
   return MUtext

def recalcMU(): # Changing how MUs are tracked just for Ekomind...
   mute()
   baseMU = 4
   addedMU = 0
   paidMU = 0
   for card in table:
      if card.controller == me and ds == 'runner' and card.highlight != InactiveColor and card.highlight != DummyColor and card.highlight != RevealedColor:
         Autoscripts = CardsAS.get(card.model,'').split('||')
         for autoS in Autoscripts: 
            setMU = re.search(r'whileInPlay:SetTo([0-9]|Special)MU',autoS)
            if setMU:
               if setMU.group(1) == 'Special':
                  if card.name == 'Ekomind': 
                     baseMU = len(me.hand)
                     #notify("setting MU to {} from {}".format(len(me.hand),card)) #Debug
               else: baseMU = num(setMU.group(1))
   for card in table:
      if card.controller == me and ds == 'runner':
         Autoscripts = CardsAS.get(card.model,'').split('||')
         for autoS in Autoscripts: 
            extraMU = re.search(r'whileInPlay:Provide([0-9])MU',autoS)
            if extraMU: 
               addedMU += num(extraMU.group(1))
               #notify("found {} extra MU on {}".format(extraMU.group(1),card)) #Debug
   for card in table:
      if card.controller == me and ds == 'runner' and fetchProperty(card,'Type') == 'Program':
         MUreq = num(fetchProperty(card,'Requirement'))
         hostCards = eval(getGlobalVariable('Host Cards'))
         if hostCards.has_key(card._id): hostC = Card(hostCards[card._id])
         else: hostC = None
         if (MUreq > 0
               and not (card.markers[mdict['DaemonMU']] and not re.search(r'Daemon',getKeywords(card)))
               and not findMarker(card,'Daemon Hosted MU')
               and not (card.markers[mdict['Cloud']] and card.markers[mdict['Cloud']] >= 1) # If the card is already in the cloud, we do not want to modify the player's MUs
               and not (hostC and findMarker(card, '{} Hosted'.format(hostC.name)) and hostC.name != "Scheherazade") # No idea if this will work.
               and card.highlight != InactiveColor 
               and card.highlight != RevealedColor): 
            paidMU += MUreq
            chkCloud(card)
            #notify("paying {} MU for {}".format(MUreq,card)) #Debug               
   #confirm('baseMU = {}, addedMU = {}, MUreq = {} '.format(baseMU,addedMU,MUreq)) # Debug
   me.MU = baseMU + addedMU - paidMU
   if me.MU < 0: notify(":::WARNING::: {} is currently exceeding their available Memory Units".format(me))
   
   
def chkCloud(cloudCard = None): # A function which checks the table for cards which can be put in the cloud and thus return their used MUs
   debugNotify(">>> chkCloud(){}".format(extraASDebug())) #Debug
   if not cloudCard: cards = [c for c in table if c.Type == 'Program']
   else: cards = [cloudCard] # If we passed a card as a variable, we just check the cloud status of that card
   for card in cards:
      #notify("Cloud Checking {} with AS = {}".format(card,fetchProperty(card, 'AutoScripts'))) #Debug
      cloudRegex = re.search(r'Cloud([0-9]+)Link',fetchProperty(card, 'AutoScripts'))
      if cloudRegex:
         linkRequired = num(cloudRegex.group(1))
         #notify("Found Cloud Regex on {}. linkRequired = {}".format(linkRequired,card)) #Debug
         if linkRequired <= card.controller.counters['Base Link'].value and not card.markers[mdict['Cloud']]:
            card.markers[mdict['Cloud']] = 1
            card.controller.MU += num(card.Requirement)
            notify("-- {}'s {} has been enabled for cloud computing".format(me,card))            
         if linkRequired > card.controller.counters['Base Link'].value and card.markers[mdict['Cloud']] and card.markers[mdict['Cloud']] >= 1:
            card.markers[mdict['Cloud']] = 0
            card.controller.MU -= num(card.Requirement)
            notify("-- {}'s {} has lost connection to the cloud.".format(me,card))
            if card.controller.MU < 0: 
               notify(":::Warning:::{}'s loss of cloud connection means that their programs require more memory than they have available. They must trash enough programs to bring their available Memory to at least 0".format(card.controller))
   debugNotify("<<< chkCloud()", 3)
            
   
def chkHostType(card, seek = 'Targeted', caissa = False):
   debugNotify(">>> chkHostType(){}".format(extraASDebug())) #Debug
   # Checks if the card needs to have a special host targeted before it can come in play.
   if caissa: hostType = re.search(r'CaissaPlace:([A-Za-z1-9:_ -]+)', fetchProperty(card, 'AutoScripts'))
   else: hostType = re.search(r'Placement:([A-Za-z1-9:_ -]+)', fetchProperty(card, 'AutoScripts'))
   if hostType:
      debugNotify("hostType: {}.".format(hostType.group(1)), 2) #Debug
      if hostType.group(1) == 'ICE': host = findTarget('{}-isICE-choose1'.format(seek))
      else: host = findTarget('{}-at{}-choose1'.format(seek,hostType.group(1)),card = card)
      if len(host) == 0:
         delayed_whisper("ABORTING!")
         result = 'ABORT'
      else: result = host[0] # If a propert host is targeted, then we return it to the calling function. We always return just the first result.
   else: result = None
   debugNotify("<<< chkHostType() with result {}".format(result), 3)
   return result
   
def chkDoublePrevention():
   # This function checks for various cards which, if present prevent extra costs from double cards.
   debugNotify(">>> chkDoublePrevention(){}".format(extraASDebug())) #Debug
   fullCostPrev = False
   for c in table: 
      if fullCostPrev: break # If we already prevented the full cost, let's break out of the loop.
      if c.name == 'Starlight Crusade Funding' and c.controller == me: 
         notify("--> {} has allowed {} to ignore the additional costs".format(c,me))
         fullCostPrev = True
   debugNotify("<<< chkDoublePrevention() with fullCostPrev = {}".format(fullCostPrev)) #Debug
   return fullCostPrev
 
def scanTable(group = table, x=0,y=0):
   debugNotify(">>> scanTable(){}".format(extraASDebug())) #Debug
   global Stored_Name, Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   if not confirm("This action will clear the internal variables and re-scan all cards in the table to fix them.\
                 \nThis action should only be used as a last-ditch effort to fix some weird behaviour in the game (e.g. treating an Ice like Agenda, or something silly like that)\
               \n\nHowever this may take some time, depending on your PC power.\
                 \nAre you sure you want to proceed?"): return
   Stored_Name.clear()
   Stored_Type.clear()
   Stored_Cost.clear()
   Stored_Keywords.clear()
   Stored_AutoActions.clear()
   Stored_AutoScripts.clear()
   cardList = [card for card in table]
   iter = 0
   for c in cardList:
      if iter % 10 == 0: whisper("Working({}/{} done)...".format(iter, len(cardList)))
      storeProperties(c)
      iter += 1
   for c in me.hand: storeProperties(c)
   notify("{} has re-scanned the table and refreshed their internal variables.".format(me))
 
def checkUnique (card, manual = False):
   debugNotify(">>> checkUnique(){}".format(extraASDebug())) #Debug
   mute()
   if not re.search(r'Unique', getKeywords(card)): 
      debugNotify("<<< checkUnique() - Not a unique card", 3) #Debug
      return True #If the played card isn't unique do nothing.
   cName = fetchProperty(card, 'name')
   ExistingUniques = [ c for c in table
                       if c.owner == me 
                       and c.controller == me 
                       and c.isFaceUp 
                       and c.name == cName ]
   if ((not manual and len(ExistingUniques) != 0) or (manual and len(ExistingUniques) != 1)) and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be Trashed at no cost)".format(fetchProperty(card, 'name'))) : return False
   else:
      count = len(ExistingUniques)
      for uniqueC in ExistingUniques: 
         if manual and count == 1: break # If it's a manual, the new unique card is already on the table, so we do not want to trash it as well.
         trashForFree(uniqueC)
         count -= 1
   debugNotify("<<< checkUnique() - Returning True", 3) #Debug
   return True   

def chkTargeting(card):
   debugNotify(">>> chkTargeting(){}".format(extraASDebug())) #Debug
   for autoS in CardsAS.get(card.model,'').split('||'):
      if (re.search(r'on(Rez|Play|Install)[^|]+(?<!Auto)Targeted', autoS)
            and len(findTarget(autoS)) == 0
            and not re.search(r'isOptional', autoS)
            and not confirm("This card requires a valid target for it to work correctly.\
                           \nIf you proceed without a target, strange things might happen.\
                         \n\nProceed anyway?")):
         return 'ABORT'
   if ds == 'corp': runnerPL = findOpponent()
   else: runnerPL = me
   if re.search(r'ifTagged', CardsAS.get(card.model,'')) and runnerPL.Tags == 0 and not re.search(r'isOptional', CardsAS.get(card.model,'')) and not re.search(r'doesNotBlock', CardsAS.get(card.model,'')):
      whisper("{} must be tagged in order to use this card".format(runnerPL))
      return 'ABORT'
   if re.search(r'isExposeTarget', CardsAS.get(card.model,'')) and getSetting('ExposeTargetsWarn',True):
      if confirm("This card will automatically provide a bonus depending on how many non-exposed derezzed cards you've selected.\
                \nMake sure you've selected all the cards you wish to expose and have peeked at them before taking this action\
                \nSince this is the first time you take this action, you have the opportunity now to abort and select your targets before traying it again.\
              \n\nDo you want to abort this action?\
                \n(This message will not appear again)"):
         setSetting('ExposeTargetsWarn',False)
         return 'ABORT'
      else: setSetting('ExposeTargetsWarn',False) # Whatever happens, we don't show this message again.
   if re.search(r'Reveal&Shuffle', CardsAS.get(card.model,'')) and getSetting('RevealandShuffleWarn',True):
      if confirm("This card will automatically provide a bonus depending on how many cards you selected to reveal (i.e. place on the table) from your hand.\
                \nMake sure you've selected all the cards (of any specific type required) you wish to reveal to the other players\
                \nSince this is the first time you take this action, you have the opportunity now to abort and select your targets before trying it again.\
              \n\nDo you want to abort this action?\
                \n(This message will not appear again)"):
         setSetting('RevealandShuffleWarn',False)
         return 'ABORT'
      else: setSetting('RevealandShuffleWarn',False) # Whatever happens, we don't show this message again.
   if re.search(r'HandTarget', CardsAS.get(card.model,'')) or re.search(r'HandTarget', CardsAA.get(card.model,'')):
      hasTarget = False
      for c in me.hand:
         if c.targetedBy and c.targetedBy == me: hasTarget = True
      if not hasTarget:
         whisper(":::Warning::: This card effect requires that you have one of more cards targeted from your hand. Aborting!")
         return 'ABORT'

def checkNotHardwareConsole (card, manual = False):
   debugNotify(">>> checkNotHardwareConsole(){}".format(extraASDebug())) #Debug
   mute()
   if card.Type != "Hardware" or not re.search(r'Console', getKeywords(card)): return True
   ExistingConsoles = [ c for c in table
         if c.owner == me and c.isFaceUp and re.search(r'Console', getKeywords(c)) ]
   if ((not manual and len(ExistingConsoles) != 0) or (manual and len(ExistingConsoles) != 1)) and not confirm("You already have at least one console in play and you're not normally allowed to install a second. Are you sure you want to install {}?".format(fetchProperty(card, 'name'))): return False
   #else:
      #for HWDeck in ExistingConsoles: trashForFree(HWDeck)
   debugNotify(">>> checkNotHardwareConsole()") #Debug
   return True   
   
def chkTags():
# A function which checks if the runner has any tags and puts a tag marker on the runner ID in that case.
   if ds == 'runner': 
      ID = Identity
      player = me
   else: 
      player = findOpponent()
      ID = getSpecial('Identity',player)
   remoteCall(player,'syncTags',[]) # We send the tag update as a remote call, so as not to get complaints from OCTGN
   if player.Tags: return True      
   else: return False
      
def syncTags():
   mute()
   ID = getSpecial('Identity',me)
   if me.Tags: ID.markers[mdict['Tag']] = me.Tags
   else: ID.markers[mdict['Tag']] = 0

def fetchRunnerPL():
   if ds == 'runner': return me
   else: return findOpponent()
   
def fetchCorpPL():
   if ds == 'corp': return me
   else: return findOpponent()
   
def clearAttachLinks(card):
# This function takes care to discard any attachments of a card that left play
# It also clear the card from the host dictionary, if it was itself attached to another card
# If the card was hosted by a Daemon, it also returns the free MU token to that daemon
   debugNotify(">>> clearAttachLinks()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
   if cardAttachementsNR >= 1:
      hostCardSnapshot = dict(hostCards)
      for attachment in hostCardSnapshot:
         if hostCardSnapshot[attachment] == card._id:
            if Card(attachment) in table: intTrashCard(Card(attachment),0,cost = "host removed")
            del hostCards[attachment]
      setGlobalVariable('Host Cards',str(hostCards))
   unlinkHosts(card)
   debugNotify("<<< clearAttachLinks()", 3) #Debug   

def unlinkHosts(card): #Checking if the card is attached to unlink.
   debugNotify(">>> returnHostTokens()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   if hostCards.has_key(card._id):
      hostCard = Card(hostCards[card._id])
      if (re.search(r'Daemon',getKeywords(hostCard)) or re.search(r'CountsAsDaemon', CardsAS.get(hostCard.model,''))) and hostCard.group == table: 
         if card.markers[mdict['DaemonMU']] and not re.search(r'Daemon',getKeywords(card)):
            hostCard.markers[mdict['DaemonMU']] += card.markers[mdict['DaemonMU']] # If the card was hosted by a Daemon, we return any Daemon MU's used.
         DaemonHosted = findMarker(card,'Daemon Hosted MU')
         if DaemonHosted: # if the card just removed was a daemon hosted by a daemon, then it's going to have a different kind of token.
            hostCard.markers[mdict['DaemonMU']] += card.markers[DaemonHosted] # If the card was hosted by a Daemon, we return any Daemon MU's used.
      customMU = findMarker(card, '{} Hosted'.format(hostCard.name)) 
      debugNotify("customMU = {}".format(customMU))
      if customMU and hostCard.group == table: # If the card has a custom hosting marker (e.g. Dinosaurus)
         hostCard.markers[customMU] += 1 # Then we return the custom hosting marker to its original card to signifiy it's free to host another program.
         card.markers[customMU] -= 1
      del hostCards[card._id] # If the card was an attachment, delete the link
      setGlobalVariable('Host Cards',str(hostCards)) # We need to store again before orgAttachments takes over
      if not re.search(r'Daemon',getKeywords(hostCard)) and not customMU: 
         orgAttachments(hostCard) # Reorganize the attachments if the parent is not a daemon-type card.
   debugNotify("<<< returnHostTokens()", 3) #Debug   
   
def sendToTrash(card, pile = None): # A function which takes care of sending a card to the right trash pile and running the appropriate scripts. Doesn't handle costs.
   debugNotify(">>> sendToTrash()") #Debug   
   if pile == None: pile = card.owner.piles['Heap/Archives(Face-up)'] # I can't pass it as a function variable. OCTGN doesn't like it.
   debugNotify("Target Pile: {}'s {}".format(pile.player,pile.name))
   debugNotify("sendToTrash says previous group = {} and highlight = {}".format(card.group.name,card.highlight))
   if pile.controller != me:
      debugNotify("We don't control the discard pile. Taking it over.")
      grabPileControl(pile)
   if card.controller != me and card.group == table: grabCardControl(card) # We take control of the card in order to avoid errors
   if card.group == table: 
      if card.highlight != DummyColor: playTrashSound(card) # We don't want the trash sound for resident effects.
      autoscriptOtherPlayers('CardTrashed',card)
   if card.group == table or chkModulator(card, 'runTrashScriptWhileInactive', 'onTrash'): 
      executePlayScripts(card,'TRASH') # We don't want to run automations on simply revealed cards, but some of them will like Director Haas.
   clearAttachLinks(card)
   if chkModulator(card, 'preventTrash', 'onTrash'): # IF the card has the preventTrash modulator, it's not supposed to be trashed.
      if chkModulator(card, 'ifAccessed', 'onTrash') and ds != 'runner': card.moveTo(pile) # Unless it only has that modulator active during runner access. Then when the corp trashes it, it should trash normally.
   else: card.moveTo(pile)
   if pile.player != pile.controller: remoteCall(pile.controller,'passPileControl',[pile,pile.player])
   update()
   debugNotify("<<< sendToTrash()", 3) #Debug   
   
def findAgendaRequirement(card):
   mute()
   debugNotify(">>> findAgendaRequirement() for card: {}".format(card)) #Debug
   AdvanceReq = num(fetchProperty(card, 'Cost'))
   for c in table:
      debugNotify("Checking {} for Agenda cost mods".format(c))
      for autoS in CardsAS.get(c.model,'').split('||'):
         if re.search(r'whileInPlay', autoS) or ((re.search(r'whileScored', autoS) or re.search(r'whileLiberated', autoS)) and c.markers[mdict['Scored']]):
            advanceModRegex = re.search(r'(Increase|Decrease)([0-9])Advancement', autoS)
            if advanceModRegex:
               debugNotify("We have a advanceModRegex")
               if c.isFaceUp and not checkCardRestrictions(gatherCardProperties(card), prepareRestrictions(autoS, 'reduce')): continue 
               debugNotify("advanceModRegex = {} ".format(advanceModRegex.groups()))
               if re.search(r'onlyOnce',autoS) and c.orientation == Rot90: continue # If the card has a once per-turn ability which has been used, ignore it
               if (re.search(r'excludeDummy',autoS) or re.search(r'CreateDummy',autoS)) and c.highlight == DummyColor: continue
               advanceMod = num(advanceModRegex.group(2)) * {'Decrease': -1}.get(advanceModRegex.group(1),1) * per(autoS, c, 0, findTarget(autoS, card = card))
               debugNotify("advanceMod = {}".format(advanceMod))
               AdvanceReq += advanceMod
               if advanceMod: 
                  delayed_whisper("-- {} {}s advance requirement by {}".format(c,advanceModRegex.group(1),advanceMod))
   debugNotify("<<< findAgendaRequirement() with return {}".format(AdvanceReq)) #Debug
   return AdvanceReq
   
def resetAll(): # Clears all the global variables in order to start a new game.
   global Stored_Name, Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   global installedCount, debugVerbosity, newturn,endofturn, currClicks, turn, autoRezFlags
   debugNotify(">>> resetAll(){}".format(extraASDebug())) #Debug
   mute()
   if len(table) > 0: return # This function should only ever run after game start or reset. We abort in case it's a reconnect.
   me.counters['Credits'].value = 5
   me.counters['Hand Size'].value = 5
   me.counters['Tags'].value = 0
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 0
   Stored_Name.clear()
   Stored_Type.clear()
   Stored_Cost.clear()
   Stored_Keywords.clear()
   Stored_AutoActions.clear()
   Stored_AutoScripts.clear()
   installedCount.clear()
   setGlobalVariable('CurrentTraceEffect','None')
   setGlobalVariable('CorpTraceValue','None')
   setGlobalVariable('League','')
   setGlobalVariable('Access','DENIED')
   setGlobalVariable('accessAttempts','0')
   newturn = False 
   endofturn = False
   currClicks = 0
   turn = 0
   del autoRezFlags[:]
   ShowDicts()
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1    
   debugNotify("<<< resetAll()") #Debug   
   
def checkQuickAccess():
   debugNotify(">>> checkQuickAccess()") #Debug   
   #if len(players) == 1: 
      #notify(">>> checkQuickAccess") # Debug
      #notify("## currentGameName = {}".format(currentGameName())) # Debug
   if len(players) == 1 or re.search(r'(\[Quick Access\]|\[QA\]|\[FQA\])',currentGameName()):
      #if len(players) == 1: notify("## About to get QuickAccessInfo Setting") # Debug
      if getSetting('QuickAccessInfo',True):
         information(":::INFO::: You have joined a [Quick Access] game for the first time.\
                 \n\n'[Quick Access]' or '[QA]' games allow the runners to access servers without needing a confirmation from the corp that it's OK to access (i.e. using the OK button or F3)\
                    \nAs such the game expects the runner to make use of the 'Access Imminent' button before pressing F3 to allow the corporation a chance to react.\
                  \n\nThe mode was made to facilitate faster play on behalf of the runner. Please run responsibly.")
         setSetting('QuickAccessInfo',False)
      #if len(players) == 1: notify("## About to switchQuickAccess()") # Debug
      switchQuickAccess(forced = True)
   debugNotify("<<< checkQuickAccess()") #Debug   
      
def clearLeftoverEvents():
   debugNotify(">>> clearLeftoverEvents()") #Debug   
   debugNotify("About to clear all events from table")
   hostCards = eval(getGlobalVariable('Host Cards'))
   for card in table: # We discard all events on the table when the player tries to use another click.
      debugNotify("Processing {}".format(card))
      debugNotify("hostCards eval = {}".format(hostCards))
      if card.isFaceUp and (card.Type == 'Operation' or card.Type == 'Event') and not re.search('Current',getKeywords(card)) and card.highlight != DummyColor and card.highlight != RevealedColor and card.highlight != InactiveColor and not card.markers[mdict['Scored']] and not hostCards.has_key(card._id): # We do not trash "scored" events (e.g. see Notoriety) or cards hosted on others card (e.g. see Oversight AI)
         intTrashCard(card,0,"free") # Clearing all Events and operations for players who keep forgeting to clear them.   
   debugNotify("<<< clearLeftoverEvents()") #Debug   

def clearCurrents(type = None,card = None):
   debugNotify(">>> clearCurrents(){}".format(extraASDebug())) #Debug
   mute()
   for c in table:
      if re.search('Current',getKeywords(c)):
         if card and card == c: continue # if a card variable has been passed, it's a newly placed current, which we don't want to trash.
         if not type: 
            intTrashCard(c, c.Stat, "free")
            notify(":> {} replaces the {} current".format(me,c))
         elif type == 'LIBERATE' and c.Side == 'corp': 
            intTrashCard(c, c.Stat, "free")
            notify(":> {} fizzles out as {} liberates an agenda".format(c,me))
         elif type == 'SCORE' and c.Side == 'runner': 
            intTrashCard(c, c.Stat, "free")
            notify(":> {} scores their agenda and {} fades out".format(me,c))
            
def chkCerebralStatic():
   CS = None
   for card in table:
      if card.name == "Cerebral Static": CS = card
   return CS
#---------------------------------------------------------------------------
# Card Placement
#---------------------------------------------------------------------------

def placeCard(card, action = 'INSTALL', hostCard = None, type = None, retainPos = False):
   debugNotify(">>> placeCard() with action: {}".format(action)) #Debug
   if not hostCard:
      hostCard = chkHostType(card, seek = 'DemiAutoTargeted')
      if hostCard:
         try:
            if hostCard == 'ABORT': 
               delayed_whisper(":::ERROR::: No Valid Host Targeted! Aborting Placement.") # We can pass a host from a previous function (e.g. see Personal Workshop)
               return 'ABORT'
         except: pass
   if hostCard: hostMe(card,hostCard)
   else:
      global installedCount
      if not type: 
         type = fetchProperty(card, 'Type') # We can pass the type of card as a varialbe. This way we can pass one card as another.
         if action != 'INSTALL' and type == 'Agenda':
            if ds == 'corp': type = 'scoredAgenda'
            else: type = 'liberatedAgenda'
         if action == 'INSTALL' and re.search(r'Console',card.Keywords): type = 'Console'
      if action == 'INSTALL' and type in CorporationCardTypes: CfaceDown = True
      else: CfaceDown = False
      debugNotify("Setting installedCount. Type is: {}, CfaceDown: {}".format(type, str(CfaceDown)), 3) #Debug
      if installedCount.get(type,None) == None: installedCount[type] = 0
      else: installedCount[type] += 1
      debugNotify("installedCount is: {}. Setting loops...".format(installedCount[type]), 2) #Debug
      loopsNR = installedCount[type] / (place[type][3]) 
      loopback = place[type][3] * loopsNR 
      if loopsNR and place[type][3] != 1: offset = 15 * (loopsNR % 3) # This means that in one loop the offset is going to be 0 and in another 15.
      else: offset = 0
      debugNotify("installedCount[type] is: {}.\nLoopsNR is: {}.\nLoopback is: {}\nOffset is: {}".format(installedCount[type],offset, loopback, offset), 3) #Debug
      #if not retainPos: card.moveToTable(((place[type][0] + (((cwidth(card,0) + place[type][2]) * (installedCount[type] - loopback)) + offset) * place[type][4]) * flipBoard) + flipModX,(place[type][1] * flipBoard) + flipModY,CfaceDown) 
      if not retainPos: placeOnTable(card,((place[type][0] + (((cwidth(card,0) + place[type][2]) * (installedCount[type] - loopback)) + offset) * place[type][4]) * flipBoard) + flipModX,(place[type][1] * flipBoard) + flipModY,CfaceDown) 
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
      if not card.isFaceUp: 
         debugNotify("Peeking() at placeCard()")
         card.peek() # Added in octgn 3.0.5.47
   debugNotify("<<< placeCard()", 3) #Debug

def hostMe(card,hostCard):
   debugNotify(">>> hostMe()") #Debug
   unlinkHosts(card) # First we make sure we clear any previous hosting and return any markers to their right place.
   hostCards = eval(getGlobalVariable('Host Cards'))
   hostCards[card._id] = hostCard._id
   setGlobalVariable('Host Cards',str(hostCards))
   orgAttachments(hostCard)
   debugNotify("<<< hostMe()") #Debug

def orgAttachments(card):
# This function takes all the cards attached to the current card and re-places them so that they are all visible
# xAlg, yAlg are the algorithsm which decide how the card is placed relative to its host and the other hosted cards. They are always multiplied by attNR
   debugNotify(">>> orgAttachments()") #Debug
   attNR = 1
   debugNotify(" Card Name : {}".format(card.name), 4)
   if specialHostPlacementAlgs.has_key(card.name):
      debugNotify("Found specialHostPlacementAlgs", 3)
      xAlg = specialHostPlacementAlgs[card.name][0]
      yAlg = specialHostPlacementAlgs[card.name][1]
      debugNotify("Found Special Placement Algs. xAlg = {}, yAlg = {}".format(xAlg,yAlg), 2)
   else: 
      debugNotify("No specialHostPlacementAlgs", 3)
      xAlg = 0 # The Default placement on the X axis, is to place the attachments at the same X as their parent
      if card.controller == me: sideOffset = playerside # If it's our card, we need to assign it towards our side
      else: sideOffset = playerside * -1 # Otherwise we assign it towards the opponent's side
      yAlg =  -(cwidth(card) / 4 * sideOffset) # Defaults
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachements = [Card(att_id) for att_id in hostCards if hostCards[att_id] == card._id]
   x,y = card.position
   for attachment in cardAttachements:
      debugNotify("Checking group of {}".format(attachment))
      debugNotify("group name = {}".format(attachment.group.name))
      if attachment.owner.getGlobalVariable('ds') == 'corp' and pileName(attachment.group) in ['R&D','Face-up Archives','HQ'] and attachment.Type != 'Operation':
         debugNotify("card is faceDown")
         cFaceDown = True
      else: 
         debugNotify("attachment.isFaceUp = {}".format(attachment.isFaceUp))
         cFaceDown = False # If we're moving corp cards to the table, we generally move them face down
      placeOnTable(attachment,x + ((xAlg * attNR) * flipBoard), y + ((yAlg * attNR) * flipBoard),cFaceDown)
      if cFaceDown and attachment.owner == me: 
         debugNotify("Peeking() at orgAttachments()")
         attachment.peek() # If we moved our own card facedown to the table, we peek at it.
      if fetchProperty(attachment, 'Type') == 'ICE': attachment.orientation = Rot90 # If we just moved an ICE to the table, we make sure it's turned sideways.
      indexSet(attachment,len(cardAttachements) - attNR) # This whole thing has become unnecessary complicated because sendToBack() does not work reliably
      debugNotify("{} index = {}".format(attachment,attachment.getIndex), 4) # Debug
      attNR += 1
      debugNotify("Moving {}, Iter = {}".format(attachment,attNR), 4)
   indexSet(card,'front') # Because things don't work as they should :(
   if debugVerbosity >= 4: # Checking Final Indices
      for attachment in cardAttachements: notify("{} index = {}".format(attachment,attachment.getIndex)) # Debug
   debugNotify("<<< orgAttachments()", 3) #Debug      

def possess(daemonCard, programCard, silent = False, force = False):
   debugNotify(">>> possess(){}".format(extraASDebug())) #Debug
   #This function takes as arguments 2 cards. A Daemon and a program requiring MUs, then assigns the program to the Daemon, restoring the used MUs to the player.
   hostType = re.search(r'Placement:([A-Za-z1-9:_ -]+)', fetchProperty(programCard, 'AutoScripts'))
   if hostType and not re.search(r'Daemon',hostType.group(1)):
      delayed_whisper("This card cannot be hosted on a Daemon as it needs a special host type")
      return 'ABORT'
   count = num(programCard.properties["Requirement"])
   debugNotify("Looking for custom hosting marker", 2)
   customHostMarker = findMarker(daemonCard, '{} Hosted'.format(daemonCard.name)) # We check if the card has a custom hosting marker which we use when the hosting is forced
   debugNotify("Custom hosting marker: {}".format(customHostMarker), 2)
   hostCards = eval(getGlobalVariable('Host Cards'))   
   if not force and (count > daemonCard.markers[mdict['DaemonMU']] and not customHostMarker):
      delayed_whisper(":::ERROR::: {} has already hosted the maximum amount of programs it can hold.".format(daemonCard))
      return 'ABORT'
   elif force and not customHostMarker: # .get didn't work on card.markers[] :-(
      delayed_whisper(":::ERROR::: {} has already hosted the maximum amount of programs it can hold.".format(daemonCard))
      return 'ABORT'
   elif hostCards.has_key(programCard._id):
      delayed_whisper(":::ERROR::: {} is already hosted in {}.".format(programCard,Card(hostCards[programCard._id])))
      return 'ABORT'
   else:
      debugNotify("We have a valid daemon host", 2) #Debug
      hostCards[programCard._id] = daemonCard._id
      setGlobalVariable('Host Cards',str(hostCards))
      if not customHostMarker:
         daemonCard.markers[mdict['DaemonMU']] -= count
         if re.search(r'Daemon',fetchProperty(programCard, 'Keywords')): # If it's a daemon, we do not want to give it the same daemon token, as that's going to be reused for other programs and we do not want that.
            TokensX('Put{}Daemon Hosted MU-isSilent'.format(count), '', programCard)
         else: programCard.markers[mdict['DaemonMU']] += count
      else:
         daemonCard.markers[customHostMarker] -= 1 # If this a forced host, the host should have a special counter on top of it...
         programCard.markers[customHostMarker] += 1 # ...that we move to the hosted program to signify it's hosted
         Autoscripts = CardsAS.get(daemonCard.model,'').split('||')
         debugNotify("Daemon Autoscripts found = {}".format(Autoscripts))
         for autoS in Autoscripts:
            markersRegex = re.search(r'onHost:(.*)',autoS)            
            if markersRegex:
               debugNotify("markersRegex groups = {}".format(markersRegex.groups()))
               for autoS in markersRegex.group(1).split('$$'):
                  redirect(autoS, programCard, announceText = None, notificationType = 'Quick', X = 0)
                  #TokensX(markersRegex.group(1),'',programCard)
            else: debugNotify("No onHost scripts found in {}".format(autoS))
      if customHostMarker and customHostMarker[0] == 'Scheherazade Hosted': pass
      else: programCard.owner.MU += count # We return the MUs the card would be otherwise using.
      if not silent: notify("{} installs {} into {}".format(me,programCard,daemonCard))
   debugNotify("<<< possess()", 3) #Debug   
   
def chkDmgSpecialEffects(dmgType, count):
# This function checks for special card effects on the table that hijack normal damage effects and do something extra or differently
# At the moment it's used for the two Chronos Protocol IDs.
   debugNotify(">>> chkDmgSpecialEffects()") #Debug
   usedDMG = 0
   replaceDMGAnnounce = False
   for card in table:
      if card.controller == me and card.model == 'bc0f047c-01b1-427f-a439-d451eda05022' and dmgType == 'Net' and re.search(r'running',getGlobalVariable('status')):
         if confirm("Do you want to pay 2 credits to use {}'s ability to turn this {} Net damage into Brain Damage?\n\n(Unfortunately, OCTGN is not aware where {} is placed. If he's not in the right server, just press No.".format(card.name,count,card.name)):
            if payCost(2, 'not free') != "ABORT":
               usedDMG = count # After this, we don't want any autoscripts to be doing any more damage
               InflictX('Inflict1BrainDamage-onOpponent', '', card)
               notify("--> {} activates {} to turn all their Net Damage into 1 Brain damage".format(me,card))
               replaceDMGAnnounce = True
      if card.name == 'Chronos Protocol':
         if card.Faction == 'Jinteki' and dmgType == 'Net' and oncePerTurn(card, silent = True, act = 'automatic') != 'ABORT':
            if card.controller == me: JintekiCP(card,count)
            else: remoteCall(card.controller,'JintekiCP',[card,count]) # It needs to be the Jinteki player who selects the card.
            usedDMG = count # After this, we don't want any autoscripts to be doing any more damage
         if card.Faction == 'Haas-Bioroid' and dmgType == 'Brain':
            remoteCall(fetchRunnerPL(),'HasbroCP',[card,count])
            usedDMG = count # After this, we don't want any autoscripts to be doing any more damage
   debugNotify("<<< chkDmgSpecialEffects() with return {}".format(usedDMG)) #Debug
   return (usedDMG,replaceDMGAnnounce)

def JintekiCP(card,count): # Function which takes care that the Jinteki Chronos Protocol ID properly asks the Jinteki player for the choice before doing more damage.
   debugNotify(">>> JintekiCP()") #Debug
   mute()
   targetPL = findOpponent()
   if not len(targetPL.hand): remoteCall(targetPL, 'intdamageDiscard',[count]) # If their hand is empty we need to flatline them
   else:
      grabPileControl(targetPL.hand)
      #targetPL.hand.setVisibility('all')
      #update()
      handList = [c for c in targetPL.hand]
      for c in handList: c.moveToTable(0,0)
      for c in handList: loopChk(c,'Type') # Make sure we can see each card's details
      choice = SingleChoice("Choose a card to trash for your first Net Damage", makeChoiceListfromCardList(handList))
      if choice != None: # If the player cancels the choice for some reason, abort the rest of the damage.
         sendToTrash(handList[choice])
         notify("=> {} uses {}'s ability to trash {} with the first net damage".format(me,card,handList[choice]))
      for c in handList: c.moveTo(targetPL.hand)
      passPileControl(targetPL.hand,targetPL)
      #remoteCall(targetPL,'grabVisibility',[targetPL.hand])
      if choice != None: 
         if count - 1: remoteCall(targetPL, 'intdamageDiscard',[count - 1]) # If there's any leftover damage, we inflict it now.
   debugNotify("<<< JintekiCP()") #Debug
   
def HasbroCP(card,count): # A Function called remotely for the runner player which takes care to wipe all cards of the same type as the one trashed from the game.
   debugNotify(">>> HasbroCP()") #Debug
   mute()
   for iter in range(count):
      exiledC = me.hand.random()
      exiledC.moveTo(me.piles['Removed from Game'])
      notify("--DMG: {} is removed from the game due to {}!".format(exiledC,card))
      #me.piles['R&D/Stack'].setVisibility('me')
      for c in me.piles['R&D/Stack']: c.peek()
      for c in me.piles['R&D/Stack']:
         loopChk(c,'Name')
         #notify("### {} c.model == {}".format(c.Name,c.model))
         if c.Name == exiledC.Name: 
            c.moveTo(me.piles['Removed from Game'])
            notify("=> Extra {} scrubbed from Stack".format(exiledC))
      #me.piles['R&D/Stack'].setVisibility('none')      
      shuffle(me.piles['R&D/Stack'])
      for c in me.piles['Heap/Archives(Face-up)']:
         if c.model == exiledC.model: 
            c.moveTo(me.piles['Removed from Game'])      
            notify("=> Extra {} scrubbed from Heap".format(exiledC))
      for c in table:
         if c.model == exiledC.model and not c.markers[mdict['Scored']] and not c.markers[mdict['ScorePenalty']] and c.highlight != DummyColor: # Scored cards like Notoriety are not removed, nor are resident effects.
            exileCard(c, True)
            notify("=> Extra {} scrubbed from the table".format(exiledC))
      for c in me.hand:
         if c.model == exiledC.model: 
            c.moveTo(me.piles['Removed from Game'])      
            notify("=> Extra {} scrubbed from Grip".format(exiledC))
   debugNotify("<<< HasbroCP()") #Debug
#------------------------------------------------------------------------------
# Switches
#------------------------------------------------------------------------------

def switchAutomation(type,command = 'Off'):
   debugNotify(">>> switchAutomation(){}".format(extraASDebug())) #Debug
   global Automations
   if (Automations[type] and command == 'Off') or (not Automations[type] and command == 'Announce'):
      notify ("--> {}'s {} automations are OFF.".format(me,type))
      if command != 'Announce': Automations[type] = False
   else:
      notify ("--> {}'s {} automations are ON.".format(me,type))
      if command != 'Announce': Automations[type] = True
   
def switchPlayAutomation(group,x=0,y=0):
   debugNotify(">>> switchPlayAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Play, Score and Rez')
   
def switchStartEndAutomation(group,x=0,y=0):
   debugNotify(">>> switchStartEndAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Start/End-of-Turn')

def switchDMGAutomation(group,x=0,y=0):
   debugNotify(">>> switchDMGAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Damage')

def switchPreventDMGAutomation(group,x=0,y=0):
   debugNotify(">>> switchDMGAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Damage Prevention')

def switchTriggersAutomation(group,x=0,y=0):
   debugNotify(">>> switchTriggersAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Triggers')
   
def switchWinForms(group,x=0,y=0):
   debugNotify(">>> switchWinForms(){}".format(extraASDebug())) #Debug
   switchAutomation('WinForms')
   
def switchUniCode(group,x=0,y=0,command = 'Off'):
   debugNotify(">>> switchUniCode(){}".format(extraASDebug())) #Debug
   global UniCode
   if UniCode and command != 'On':
      whisper("Credits and Clicks will now be displayed as normal ASCII.".format(me))
      UniCode = False
   else:
      whisper("Credits and Clicks will now be displayed as Unicode.".format(me))
      UniCode = True

def switchSounds(group,x=0,y=0):
   debugNotify(">>> switchSounds(){}".format(extraASDebug())) #Debug
   if getSetting('Sounds', True):
      setSetting('Sounds', False)
      whisper("Sound effects have been switched off")
   else:
      setSetting('Sounds', True)
      whisper("Sound effects have been switched on")
        
def switchQuickAccess(group = table,x=0,y=0,forced = False, remoted = False):
   #if len(players) == 1: notify(">>> switchQuickAccess()") # Debug
   debugNotify(">>> switchQuickAccess(){}".format(extraASDebug())) #Debug
   global askedQA
   QAgame = re.search(r'(\[Quick Access\]|\[QA\]|\[FQA\])',currentGameName()) # If the game has [Quick Access] in the title, we don't allow to turn QA off.
   if not forced and QAgame:
      whisper(":::ERROR::: Sorry, you cannot cancel Quick Access in a [Quick Access] game.")
   elif not forced and ds == None:
      whisper(":::ERROR::: Please load a deck first.")
   else:
      QA = getGlobalVariable('Quick Access')
      if ds == 'corp' or forced or len(players) == 1: # Checking that this is not a single-player game to avoid an infinite loop
         if QA == 'False':
            if remoted and not confirm("The runner would like to turn Quick Access on (i.e. not requiring corp confirmation before accessing a server). Do you accept?"): 
               notify(":::INFO::: {} rejected the request to activate Quick Access!".format(me))
            elif re.search(r'\[FQA\]',currentGameName()): 
               setGlobalVariable('Quick Access','Fucking')
               if QAgame: barNotifyAll("#009900",":::INFO::: This is a [Fucking Quick Access] Game!") 
            else: 
               setGlobalVariable('Quick Access','True')
               if QAgame: barNotifyAll("#009900",":::INFO::: This is a [Quick Access] Game!") 
               else: barNotifyAll("#009900",":::INFO::: Quick Access has been activated!")
         else: 
            if remoted and not confirm("The runner would like to turn Quick Access off. Accept?"): 
               notify(":::INFO::: {} rejected the request to disable Quick Access!".format(me))
               return
            setGlobalVariable('Quick Access','False')
            barNotifyAll("#009900",":::INFO::: Quick Access has been disabled!")
      else:
         if askedQA: whisper(":::ERROR::: You've already asked the corp to enable QA once already. Please don't spam them.")
         else:
            whisper(":::INFO::: Asking for corporation confirmation to activate Quick Access...")
            targetPL = findOpponent()
            if targetPL != me: remoteCall(targetPL,'remoteAskQA',[]) # Checking player just in case we end up in an infinite loop.
            askedQA = True # The runner can only ask once for QA in order not to spam the corp
            
def remoteAskQA():
   mute()
   switchQuickAccess(remoted = True)
   
def addGroupVisibility(group,player):
   mute()
   if group.controller != me: 
      remoteCall(group.controller,'addGroupVisibility',[group,player])
   else:    
      debugNotify("{} giving {} visibility to {}. Current Controller == {}".format(me,group.name,player,group.controller))
      group.addViewer(player)
   update()
   debugNotify("<<< addGroupVisibility. {} Viewers == {}".format(group,[pl.name for pl in group.viewers]))
   
def delGroupVisibility(group,player):
   mute()
   if group.controller != me: remoteCall(group.controller,'delGroupVisibility',[group,player])
   else: group.removeViewer(player)
   update()
   debugNotify("<<< delGroupVisibility. {} Viewers == {}".format(group,[pl.name for pl in group.viewers]))

def modGroupVisibility(group,setting):
   mute()
   if group.controller != me: 
      remoteCall(group.controller,'modGroupVisibility',[group,setting])
   else:    
      debugNotify("{} setting {} visibility to {}. Current Controller == {}".format(me,group.name,setting,group.controller))
      group.setVisibility(setting)
   update()
   debugNotify("<<< modGroupVisibility. {} group.visibility == {}".format(group,group.visibility))

   
#------------------------------------------------------------------------------
# Help functions
#------------------------------------------------------------------------------

def HELP_TurnStructure(group,x=0,y=0):
   table.create('8b4f0c4d-4e4a-4d7f-890d-936ef37c8600', x, y, 1)
def HELP_CorpActions(group,x=0,y=0):
   table.create('881ccfad-0da9-4ca8-82e6-29c524f15a7c', x, y, 1)
def HELP_RunnerActions(group,x=0,y=0):
   table.create('6b3c394a-411f-4a1c-b529-9a8772a96db9', x, y, 1)
def HELP_RunAnatomy(group,x=0,y=0):
   table.create('db60308d-0d0e-4891-9954-7c600a7389e1', x, y, 1)
def HELP_RunStructure(group,x=0,y=0):
   table.create('51c3a293-3923-49ee-8c6f-b8c41aaba5f3', x, y, 1)


#------------------------------------------------------------------------------
# Button functions
#------------------------------------------------------------------------------

def BUTTON_Access(group = None,x=0,y=0):
   global AccessBtnNextChoice # Using a global var to avoid running the slow random function
   mute()
   if num(getGlobalVariable('accessAttempts')) == 0:
      AccessMsgs = ["--- Alert: Unauthorized Access Imminent!", 
                    "--- Alert: Runner entry detected!",
                    "--- Alert: Firewalls breached!",
                    "--- Alert: Intrusion in progress!"]
      #AccessTXT = AccessMsgs[rnd(0,len(AccessMsgs) - 1)]
      AccessTXT = AccessMsgs[AccessBtnNextChoice]
      AccessBtnNextChoice += 1
      if AccessBtnNextChoice >= len(AccessMsgs): AccessBtnNextChoice = 0
      notify(AccessTXT + "\n-- {} is about to gain access. Corporate React?".format(me))
      setGlobalVariable('accessAttempts',str(num(getGlobalVariable('accessAttempts')) + 1))  # The runner using the Button counts for an access Attempt. After 3 of them, the runner can bypass an unresponsive corp.
      playButtonSound('Access')
   else: runSuccess()

def BUTTON_NoRez(group = None,x=0,y=0):  
   notify("--- {} does not rez approached ICE".format(me))
   playButtonSound('NoRez')

def BUTTON_OK(group = None,x=0,y=0):
   notify("--- {} has no further reactions.".format(me))
   if re.search(r'running',getGlobalVariable('status')) and ds == 'corp': 
      setGlobalVariable('Access','GRANTED')
      notify("--- ACCESS GRANTED ---")
   playButtonSound('OK')

def BUTTON_Wait(group = None,x=0,y=0):  
   notify("--- Wait! {} wants to react.".format(me))
   playButtonSound('Wait')
#------------------------------------------------------------------------------
#  Online Functions
#------------------------------------------------------------------------------

def versionCheck():
   debugNotify(">>> versionCheck()") #Debug
   global startupMsg
   me.setGlobalVariable('gameVersion',gameVersion)
   if not startupMsg: MOTD() # If we didn't give out any other message , we give out the MOTD instead.
   startupMsg = True
   ### Below code Not needed anymore in 3.1.x
   # if not startupMsg:
      # (url, code) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/current_version.txt')
      # debugNotify("url:{}, code: {}".format(url,code), 2) #Debug
      # if code != 200 or not url:
         # whisper(":::WARNING::: Cannot check version at the moment.")
         # return
      # detailsplit = url.split('||')
      # currentVers = detailsplit[0].split('.')
      # installedVers = gameVersion.split('.')
      # debugNotify("Finished version split. About to check", 2) #Debug
      # if len(installedVers) < 3:
         # whisper("Your game definition does not follow the correct version conventions. It is most likely outdated or modified from its official release.")
         # startupMsg = True
      # elif (num(currentVers[0]) > num(installedVers[0]) or 
           # (num(currentVers[0]) == num(installedVers[0]) and num(currentVers[1]) > num(installedVers[1])) or 
           # (num(currentVers[0]) == num(installedVers[0]) and num(currentVers[1]) == num(installedVers[1]) and num(currentVers[2]) > num(installedVers[2]))):
         # notify("{}'s game definition ({}) is out-of-date!".format(me, gameVersion))
         # if confirm("There is a new game definition available!\nYour version: {}.\nCurrent version: {}\n{}\
                     # {}\
                 # \n\nDo you want to be redirected to download the latest version?.\
                   # \n(You'll have to download the game definition, any patch for the current version and the markers if they're newer than what you have installed)\
                     # ".format(gameVersion, detailsplit[0],detailsplit[2],detailsplit[1])):
            # openUrl('http://octgn.gamersjudgement.com/viewtopic.php?f=52&t=494')
         # startupMsg = True
      # debugNotify("Finished version check. Seeing if I should MOTD.", 2) #Debug
   debugNotify("<<< versionCheck()", 3) #Debug
      
      
def MOTD():
   debugNotify(">>> MOTD()") #Debug
   #if me.name == 'db0' or me.name == 'dbzer0': return #I can't be bollocksed
   (MOTDurl, MOTDcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/MOTD.txt',3000)
   if MOTDcode != 200 or not MOTDurl:
      whisper(":::WARNING::: Cannot fetch MOTD info at the moment.")
      return
   if getSetting('MOTD', 'UNSET') != MOTDurl: # If we've already shown the player the MOTD already, we don't do it again.
      setSetting('MOTD', MOTDurl) # We store the current MOTD so that we can check next time if it's the same.
      (DYKurl, DYKcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/DidYouKnow.txt',3000)
      if DYKcode !=200 or not DYKurl:
         whisper(":::WARNING::: Cannot fetch DYK info at the moment.")
         return
      DYKlist = DYKurl.split('||')
      DYKrnd = rnd(0,len(DYKlist)-1)
      while MOTDdisplay(MOTDurl,DYKlist[DYKrnd]) == 'MORE': 
         MOTDurl = '' # We don't want to spam the MOTD for the further notifications
         DYKrnd += 1
         if DYKrnd == len(DYKlist): DYKrnd = 0
   debugNotify("<<< MOTD()", 3) #Debug
   
def MOTDdisplay(MOTD,DYK):
   debugNotify(">>> MOTDdisplay()") #Debug
   if re.search(r'http',MOTD): # If the MOTD has a link, then we do not sho DYKs, so that they have a chance to follow the URL
      MOTDweb = MOTD.split('&&')      
      if confirm("{}".format(MOTDweb[0])): openUrl(MOTDweb[1].strip())
   elif re.search(r'http',DYK):
      DYKweb = DYK.split('&&')
      if confirm("{}\
              \n\nDid You Know?:\
                \n------------------\
                \n{}".format(MOTD,DYKweb[0])):
         openUrl(DYKweb[1].strip())
   elif confirm("{}\
              \n\nDid You Know?:\
                \n-------------------\
                \n{}\
                \n-------------------\
              \n\nWould you like to see the next tip?".format(MOTD,DYK)): return 'MORE'
   return 'STOP'

def initGame(): # A function which prepares the game for online submition
   debugNotify(">>> initGame()") #Debug
   if getGlobalVariable('gameGUID') != 'None': return #If we've already grabbed a GUID, then just use that.
   (gameInit, initCode) = webRead('http://84.205.248.92/slaghund/init.slag',3000)
   if initCode != 200:
      #whisper("Cannot grab GameGUID at the moment!") # Maybe no need to inform players yet.
      return
   debugNotify("{}".format(gameInit), 2) #Debug
   GUIDregex = re.search(r'([0-9a-f-]{36}).*?',gameInit)
   if GUIDregex: setGlobalVariable('gameGUID',GUIDregex.group(1))
   else: setGlobalVariable('gameGUID','None') #If for some reason the page does not return a propert GUID, we won't record this game.
   setGlobalVariable('gameEnded','False')
   debugNotify("<<< initGame()", 3) #Debug
   
def reportGame(result = 'AgendaVictory'): # This submits the game results online.
   delayed_whisper("Please wait. Submitting Game Stats...")     
   debugNotify(">>> reportGame()") #Debug
   GUID = getGlobalVariable('gameGUID')
   if GUID == 'None' and debugVerbosity < 0: return # If we don't have a GUID, we can't submit. But if we're debugging, we go through.
   gameEnded = getGlobalVariable('gameEnded')
   if gameEnded == 'True':
     if not confirm("Your game already seems to have finished once before. Do you want to change the results to '{}' for {}?".format(result,me.name)): return
   playGameEndSound(result)
   PLAYER = me.name # Seeting some variables for readability in the URL
   id = getSpecial('Identity',me)
   IDENTITY = id.Subtitle.replace(',','').replace('.','').replace('#','').replace('@','').replace('#','')
   RESULT = result
   GNAME = currentGameName()
   LEAGUE = getGlobalVariable('League')
   if result == 'Flatlined' or result == 'Conceded' or result == 'DeckDefeat' or result == 'AgendaDefeat': WIN = 0
   else: WIN = 1
   SCORE = me.counters['Agenda Points'].value
   deckStats = eval(me.getGlobalVariable('Deck Stats'))
   debugNotify("Retrieved deckStats ", 2) #Debug
   debugNotify("deckStats = {}".format(deckStats), 2) #Debug
   INFLUENCE = deckStats[0]
   CARDSNR = deckStats[1]
   AGENDASNR = deckStats[2]
   TURNS = turn
   VERSION = gameVersion
   debugNotify("About to report player results online.", 2) #Debug
   if (turn < 1 or len(players) == 1) and debugVerbosity < 1:
      notify(":::ATTENTION:::Game stats submit aborted due to number of players ( less than 2 ) or turns played (less than 1)")
      return # You can never win before the first turn is finished and we don't want to submit stats when there's only one player.
   if debugVerbosity < 1: # We only submit stats if we're not in debug mode
      (reportTXT, reportCode) = webRead('http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}'.format(GUID,PLAYER,IDENTITY,RESULT,SCORE,INFLUENCE,TURNS,CARDSNR,AGENDASNR,VERSION,WIN,LEAGUE,GNAME),10000)
   else: 
      if confirm('Report URL: http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}\n\nSubmit?'.format(GUID,PLAYER,IDENTITY,RESULT,SCORE,INFLUENCE,TURNS,CARDSNR,AGENDASNR,VERSION,WIN,LEAGUE,GNAME)):
         (reportTXT, reportCode) = webRead('http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}'.format(GUID,PLAYER,IDENTITY,RESULT,SCORE,INFLUENCE,TURNS,CARDSNR,AGENDASNR,VERSION,WIN,LEAGUE,GNAME),10000)
         notify('Report URL: http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}\n\nSubmit?'.format(GUID,PLAYER,IDENTITY,RESULT,SCORE,INFLUENCE,TURNS,CARDSNR,AGENDASNR,VERSION,WIN,LEAGUE,GNAME))
   try:
      if reportTXT != "Updating result...Ok!" and debugVerbosity >=0: whisper("Failed to submit match results") 
   except: pass
   # The victorious player also reports for their enemy
   enemyPL = ofwhom('-ofOpponent')
   ENEMY = enemyPL.name
   enemyIdent = getSpecial('Identity',enemyPL)
   E_IDENTITY = enemyIdent.Subtitle.replace(',','').replace('.','').replace('#','').replace('@','').replace('#','')
   debugNotify("Enemy Identity Name: {}".format(E_IDENTITY), 2) #Debug
   if result == 'FlatlineVictory': 
      E_RESULT = 'Flatlined'
      E_WIN = 0
   elif result == 'Flatlined': 
      E_RESULT = 'FlatlineVictory'
      E_WIN = 1
   elif result == 'Conceded': 
      E_RESULT = 'ConcedeVictory'
      E_WIN = 1  
   elif result == 'DeckDefeat': 
      E_RESULT = 'DeckVictory'
      E_WIN = 1  
   elif result == 'AgendaVictory': 
      E_RESULT = 'AgendaDefeat'
      E_WIN = 0
   elif result == 'AgendaDefeat': 
      E_RESULT = 'AgendaVictory'
      E_WIN = 1
   else: 
      E_RESULT = 'Unknown'
      E_WIN = 0
   E_SCORE = enemyPL.counters['Agenda Points'].value
   debugNotify("About to retrieve E_deckStats", 2) #Debug
   E_deckStats = eval(enemyPL.getGlobalVariable('Deck Stats'))
   debugNotify("E_deckStats = {}".format(E_deckStats), 2) #Debug
   E_INFLUENCE = E_deckStats[0]
   E_CARDSNR = E_deckStats[1]
   E_AGENDASNR = E_deckStats[2]
   if ds == 'corp': E_TURNS = turn - 1 # If we're a corp, the opponent has played one less turn than we have.
   else: E_TURNS = turn # If we're the runner, the opponent has played one more turn than we have.
   debugNotify("About to report enemy results online.", 2) #Debug
   if debugVerbosity < 1: # We only submit stats if we're not debugging
      (EreportTXT, EreportCode) = webRead('http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}'.format(GUID,ENEMY,E_IDENTITY,E_RESULT,E_SCORE,E_INFLUENCE,E_TURNS,E_CARDSNR,E_AGENDASNR,VERSION,E_WIN,LEAGUE,GNAME),10000)
   setGlobalVariable('gameEnded','True')
   notify("Thanks for playing. Please submit any bugs or feature requests on github.\n-- https://github.com/db0/Android-Netrunner-OCTGN/issues")
   notify("   \n =+= Please consider supporting the development of this plugin\n =+= http://www.patreon.com/db0\n")
   debugNotify("<<< reportGame()", 3) #Debug

def setleague(group = table, x=0,y=0, manual = True):
   debugNotify(">>> setleague()") #Debug
   mute()
   league = getGlobalVariable('League')
   origLeague = league
   debugNotify("global var = {}".format(league))
   if league == '': # If there is no league set, we attempt to find out the league name from the game name
      for leagueTag in knownLeagues:
         if re.search(r'{}'.format(leagueTag),currentGameName()): league = leagueTag
   debugNotify("League after automatic check: {}".format(league))
   if manual:
      if not confirm("Do you want to set this match to count for an active league\n(Pressing 'No' will unset this match from all leagues)"): league = ''
      else:
         choice = SingleChoice('Please Select One the Active Leagues', [knownLeagues[leagueTag] for leagueTag in knownLeagues])
         if choice != None: league = [leagueTag for leagueTag in knownLeagues][choice]
   debugNotify("League after manual check: {}".format(league))
   debugNotify("Comparing with origLeague: {}".format(origLeague))
   if origLeague != league:
      if manual: 
         if league ==  '': notify("{} sets this match as casual".format(me))
         else: notify("{} sets this match to count for the {}".format(me,knownLeagues[league]))
      elif league != '': notify(":::LEAGUE::: This match will be recorded for the the {}. (press Ctrl+Alt+L to unset)".format(knownLeagues[league]))
   elif manual: 
         if league == '': delayed_whisper("Game is already casual.")
         else: delayed_whisper("Game already counts for the {}".format(me,knownLeagues[league]))
   setGlobalVariable('League',league)
   debugNotify(">>> setleague() with league: {}".format(league)) #Debug
         
def fetchCardScripts(group = table, x=0, y=0, silent = False): # Creates 2 dictionaries with all scripts for all cards stored, based on a web URL or the local version if that doesn't exist.
   debugNotify(">>> fetchCardScripts()") #Debug
   global CardsAA, CardsAS # Global dictionaries holding Card AutoActions and Card AutoScripts for all cards.
   if not silent: whisper("+++ Fetching fresh scripts. Please Wait...")
   if (len(players) > 1 or debugVerbosity == 0) and me.name != 'dbzer0' and not silent: # I put my debug account to always use local scripts.
      try: (ScriptsDownload, code) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/o8g/Scripts/CardScripts.py',5000)
      except: 
         debugNotify("Timeout Error when trying to download scripts", 0)
         code = ScriptsDownload = None
   else: # If we have only one player, we assume it's a debug game and load scripts from local to save time.
      debugNotify("Skipping Scripts Download for faster debug", 0)
      code = 0
      ScriptsDownload = None
   debugNotify("code:{}, text: {}".format(code, ScriptsDownload), 4) #Debug
   if code != 200 or not ScriptsDownload or (ScriptsDownload and not re.search(r'ANR CARD SCRIPTS', ScriptsDownload)) or debugVerbosity >= 0: 
      whisper(":::WARNING::: Cannot download card scripts at the moment. Will use locally stored ones.")
      Split_Main = ScriptsLocal.split('=====') # Split_Main is separating the file description from the rest of the code
   else: 
      #WHAT THE FUUUUUCK? Why does it gives me a "value cannot be null" when it doesn't even come into this path with a broken connection?!
      #WHY DOES IT WORK IF I COMMENT THE NEXT LINE. THIS MAKES NO SENSE AAAARGH!
      #ScriptsLocal = ScriptsDownload #If we found the scripts online, then we use those for our scripts
      Split_Main = ScriptsDownload.split('=====')
   if debugVerbosity >= 5:  #Debug
      notify(Split_Main[1])
      notify('=====')
   Split_Cards = Split_Main[1].split('.....') # Split Cards is making a list of a different cards
   if debugVerbosity >= 5: #Debug
      notify(Split_Cards[0]) 
      notify('.....')
   for Full_Card_String in Split_Cards:
      if re.search(r'ENDSCRIPTS',Full_Card_String): break # If we have this string in the Card Details, it means we have no more scripts to load.
      Split_Details = Full_Card_String.split('-----') # Split Details is splitting the card name from its scripts
      if debugVerbosity >= 5:  #Debug
         notify(Split_Details[0])
         notify('-----')
      # A split from the Full_Card_String always should result in a list with 2 entries.
      debugNotify(Split_Details[0].strip(), 2) # If it's the card name, notify us of it.
      Split_Scripts = Split_Details[2].split('+++++') # List item [1] always holds the two scripts. AutoScripts and AutoActions.
      CardsAS[Split_Details[1].strip()] = Split_Scripts[0].strip()
      CardsAA[Split_Details[1].strip()] = Split_Scripts[1].strip()
   if turn > 0: whisper("+++ All card scripts refreshed!")
   if debugVerbosity >= 4: # Debug
      notify("CardsAS Dict:\n{}".format(str(CardsAS)))
      notify("CardsAA Dict:\n{}".format(str(CardsAA))) 
   debugNotify("<<< fetchCardScripts()", 3) #Debug

def concede(group=table,x=0,y=0):
   mute()
   if confirm("Are you sure you want to concede this game?"): 
      reportGame('Conceded')
      notify("{} has conceded the game".format(me))
   else: 
      notify("{} was about to concede the game, but thought better of it...".format(me))
#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global ds, debugVerbosity
   mute()
   #test()
   delayed_whisper("## Checking Debug Verbosity")
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      whisper("Debug verbosity is now: {}".format(debugVerbosity))
      return
   delayed_whisper("## Checking my Name")
   if me.name == 'db0' or me.name == 'dbzer0' or me.name == 'null': 
      debugVerbosity = 0
      fetchCardScripts()
   delayed_whisper("## Checking players array size")
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   ######## Testing Corner ########
   #testHandRandom()
   ###### End Testing Corner ######
   delayed_whisper("## Defining Test Cards")
   testcards = [
                "bc0f047c-01b1-427f-a439-d451eda04061", 
                "bc0f047c-01b1-427f-a439-d451eda04062",
                # "bc0f047c-01b1-427f-a439-d451eda04063",
                # "bc0f047c-01b1-427f-a439-d451eda04064",
                # "bc0f047c-01b1-427f-a439-d451eda04065",
                #"bc0f047c-01b1-427f-a439-d451eda04066",
                #"bc0f047c-01b1-427f-a439-d451eda04067",
                #"bc0f047c-01b1-427f-a439-d451eda04068",
                "bc0f047c-01b1-427f-a439-d451eda04069",
                #"bc0f047c-01b1-427f-a439-d451eda04070",
                #"bc0f047c-01b1-427f-a439-d451eda04071",
                #"bc0f047c-01b1-427f-a439-d451eda04072",
                "bc0f047c-01b1-427f-a439-d451eda04073",
                #"bc0f047c-01b1-427f-a439-d451eda04074",
                #"bc0f047c-01b1-427f-a439-d451eda04075",
                #"bc0f047c-01b1-427f-a439-d451eda04076",
                #"bc0f047c-01b1-427f-a439-d451eda04077",
                #"bc0f047c-01b1-427f-a439-d451eda04078",
                "bc0f047c-01b1-427f-a439-d451eda04079",
                "bc0f047c-01b1-427f-a439-d451eda04058",
                "bc0f047c-01b1-427f-a439-d451eda04080"
                ] 
   if not ds: 
      if confirm("corp?"): ds = "corp"
      else: ds = "runner"
   me.setGlobalVariable('ds', ds) 
   me.counters['Credits'].value = 50
   me.counters['Hand Size'].value = 5
   me.counters['Tags'].value = 1
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 10
   me.Clicks = 15
   notify("Variables Reset") #Debug   
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      notify("Playerside not chosen yet. Doing now") #Debug   
      chooseSide()
      notify("About to create starting cards.") #Debug   
      createStartingCards()
   notify("<<< TrialError()") #Debug
   # if debugVerbosity >= 0 and confirm("Spawn Test Cards?"):
      # for idx in range(len(testcards)):
         # test = table.create(testcards[idx], (70 * idx) - 650, 0, 1, True)
         # storeProperties(test)
         # if test.Type == 'ICE' or test.Type == 'Agenda' or test.Type == 'Asset': test.isFaceUp = False

def debugChangeSides(group=table,x=0,y=0):
   global ds
   if debugVerbosity >=0:
      delayed_whisper("## Changing side")
      if ds == "corp": 
         notify("Runner now")
         ds = "runner"
         me.setGlobalVariable('ds','runner')
      else: 
         ds = "corp"
         me.setGlobalVariable('ds','corp')
         notify("Corp Now")
   else: whisper("Sorry, development purposes only")


def ShowDicts():
   if debugVerbosity < 0: return
   notify("Stored_Names:\n {}".format(str(Stored_Name)))
   notify("Stored_Types:\n {}".format(str(Stored_Type)))
   notify("Stored_Costs:\n {}".format(str(Stored_Cost)))
   notify("Stored_Keywords: {}".format(str(Stored_Keywords)))
   debugNotify("Stored_AA: {}".format(str(Stored_AutoActions)), 4)
   debugNotify("Stored_AS: {}".format(str(Stored_AutoScripts)), 4)
   notify("installedCounts: {}".format(str(installedCount)))

def DebugCard(card, x=0, y=0):
   whisper("Stored Card Properties\
          \n----------------------\
          \nStored Name: {}\
          \nPrinted Name: {}\
          \nStored Type: {}\
          \nPrinted Type: {}\
          \nStored Keywords: {}\
          \nPrinted Keywords: {}\
          \nCost: {}\
          \nCard ID: {}\
          \n----------------------\
          ".format(Stored_Name.get(card._id,'NULL'), card.Name, Stored_Type.get(card._id,'NULL'), card.Type, Stored_Keywords.get(card._id,'NULL'), card.Keywords, Stored_Cost.get(card._id,'NULL'),card._id))
   if debugVerbosity >= 4: 
      #notify("Stored_AS: {}".format(str(Stored_AutoScripts)))
      notify("Downloaded AA: {}".format(str(CardsAA)))
      notify("Card's AA: {}".format(CardsAA.get(card.model,'???')))
   storeProperties(card, True)
   if Stored_Type.get(card._id,'?') != 'ICE': card.orientation = Rot0

def addC(cardModel,count = 1): # Quick function to add custom cards on the table depending on their GUID
# Use the following to spawn a card
# remoteCall(me,'addC',['<cardGUID>'])
   card = table.create(cardModel, 0,0, count, True)
   storeProperties(card)
   if card.Type == 'ICE' or card.Type == 'Agenda' or card.Type == 'Asset': card.isFaceUp = False   
   
def extraASDebug(Autoscript = None):
   if Autoscript and debugVerbosity >= 3: return ". Autoscript:{}".format(Autoscript)
   else: return ''

def ShowPos(group, x=0,y=0):
   if debugVerbosity >= 1: 
      notify('x={}, y={}'.format(x,y))
      
def ShowPosC(card, x=0,y=0):
   if debugVerbosity >= 1: 
      notify(">>> ShowPosC(){}".format(extraASDebug())) #Debug
      x,y = card.position
      notify('card x={}, y={}'.format(x,y))      

   
def testHandRandom():
   if confirm("Run Hand random alg?"):
      randomsList = []
      notify("About to fill list")
      for iter in range(len(me.hand)): randomsList.append(0)
      notify("about to iter 100")
      for i in range(500):
         c = me.hand.random()
         for iter in range(len(me.hand)):            
            if c == me.hand[iter]: 
               randomsList[iter] += 1
               break
      notify("randomsList: {}".format(randomsList))

def echoScripts():
   notify(ScriptsLocal)