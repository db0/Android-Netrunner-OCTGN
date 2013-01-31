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
               'Damage'                 : True}

UniCode = True # If True, game will display credits, clicks, trash, memory as unicode characters

debugVerbosity = -1 # At -1, means no debugging messages display

startupMsg = False # Used to check if the player has checked for the latest version of the game.

gameGUID = None # A Unique Game ID that is fetched during game launch.
#totalInfluence = 0 # Used when reporting online
#gameEnded = False # A variable keeping track if the players have submitted the results of the current game already.
turn = 0 # used during game reporting to report how many turns the game lasted

CardsAA = {} # Dictionary holding all the AutoAction scripts for all cards
CardsAS = {} # Dictionary holding all the AutoScript scripts for all cards

#---------------------------------------------------------------------------
# Generic Netrunner functions
#---------------------------------------------------------------------------
def uniCredit(count):
   if debugVerbosity >= 1: notify(">>> uniCredit(){}".format(extraASDebug())) #Debug
   count = num(count)
   if UniCode: return "{} ¥".format(count)
   else: 
      if count == 1: grammar = 's'
      else: grammar =''
      return "{} Credit{}".format(count,grammar)
 
def uniRecurring(count):
   if debugVerbosity >= 1: notify(">>> uniRecurring(){}".format(extraASDebug())) #Debug
   count = num(count)
   if UniCode: return "{} £".format(count)
   else: 
      if count == 1: grammar = 's'
      else: grammar =''
      return "{} Recurring Credit{}".format(count,grammar)
 
def uniClick():
   if debugVerbosity >= 1: notify(">>> uniClick(){}".format(extraASDebug())) #Debug
   if UniCode: return ' ⌚'
   else: return '(/)'

def uniTrash():
   if debugVerbosity >= 1: notify(">>> uniTrash(){}".format(extraASDebug())) #Debug
   if UniCode: return '⏏'
   else: return 'Trash'

def uniMU(count = 1):
   if debugVerbosity >= 1: notify(">>> uniMU(){}".format(extraASDebug())) #Debug
   if UniCode: 
      if num(count) == 1: return '⎗'
      elif num(count) == 2:  return '⎘'
      else: return '{} MU'.format(count)
   else: return '{} MU'.format(count)
   
def uniLink():
   if debugVerbosity >= 1: notify(">>> uniLink(){}".format(extraASDebug())) #Debug
   if UniCode: return '⎙'
   else: return 'Base Link'

def uniSubroutine():
   if debugVerbosity >= 1: notify(">>> uniLink(){}".format(extraASDebug())) #Debug
   if UniCode: return '⏎'
   else: return '[Subroutine]'

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
      if debugVerbosity >= 3: notify("### Key: {}\nmarkerDesc: {}".format(key[0],markerDesc)) # Debug
      if re.search(r'{}'.format(markerDesc),key[0]) or markerDesc == key[0]:
         foundKey = key
         if debugVerbosity >= 2: notify("### Found {} on {}".format(key[0],card))
         break
   if debugVerbosity >= 3: notify("<<< findMarker() by returning: {}".format(foundKey))
   return foundKey
   
def getKeywords(card): # A function which combines the existing card keywords, with markers which give it extra ones.
   if debugVerbosity >= 1: notify(">>> getKeywords(){}".format(extraASDebug())) #Debug
   global Stored_Keywords
   #confirm("getKeywords") # Debug
   keywordsList = []
   cKeywords = fetchProperty(card, 'Keywords')
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
   if debugVerbosity >= 3: notify("<<< getKeywords() by returning: {}.".format(keywords[:-1]))
   return keywords[:-1] # We need to remove the trailing dash '-'
   
def pileName(group):
   if debugVerbosity >= 1: notify(">>> pileName(){}".format(extraASDebug())) #Debug   
   if debugVerbosity >= 2: notify(">>> pile player: {}".format(group.player)) #Debug   
   if group.name == 'Heap/Archives(Face-up)':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'Face-up Archives'
      else: name = 'Heap'
   elif group.name == 'R&D/Stack':
      if group.player.getGlobalVariable('ds') == 'corp': name = 'R&D'
      else: name = 'Stack'
   elif group.name == 'Archives(Hidden)': name = 'Hidden Archives'
   else:
      if group.player.getGlobalVariable('ds') == 'corp': name = 'HQ'
      else: name = 'Grip'
   if debugVerbosity >= 3: notify("<<< pileName() by returning: {}".format(name))
   return name

def clearNoise(): # Clears all player's noisy bits. I.e. nobody is considered to have been noisy this turn.
   if debugVerbosity >= 1: notify(">>> clearNoise()") #Debug
   for player in players: player.setGlobalVariable('wasNoisy', '0') 
   if debugVerbosity >= 3: notify("<<< clearNoise()") #Debug

def storeSpecial(card): 
# Function stores into a shared variable some special cards that other players might look up.
   try:
      if debugVerbosity >= 1: notify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
      storeProperties(card, True)
      specialCards = eval(me.getGlobalVariable('specialCards'))
      specialCards[card.Type] = card._id
      me.setGlobalVariable('specialCards', str(specialCards))
   except: notify("!!!ERROR!!! In storeSpecial()")

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   if debugVerbosity >= 1: notify(">>> getSpecial() for player: {}".format(me.name)) #Debug
   specialCards = eval(player.getGlobalVariable('specialCards'))
   card = Card(specialCards[cardType])
   if debugVerbosity >= 2: notify("### Stored_Type = {}".format(Stored_Type.get(card._id,'NULL')))
   if Stored_Type.get(card._id,'NULL') == 'NULL':
      if card.owner == me: delayed_whisper(":::DEBUG::: {} was NULL. Re-storing as an attempt to fix".format(cardType))
      if debugVerbosity >= 1: notify("### card ID = {}".format(card._id))
      if debugVerbosity >= 1: notify("### Stored Type = {}".format(Stored_Type.get(card._id,'NULL')))
      storeProperties(card, True)
   if debugVerbosity >= 3: notify("<<< getSpecial() by returning: {}".format(card))
   return card

def chkRAM(card, action = 'INSTALL', silent = False):
   if debugVerbosity >= 1: notify(">>> chkRAM(){}".format(extraASDebug())) #Debug
   MUreq = num(fetchProperty(card,'Requirement'))
   if (MUreq > 0
         and not (card.markers[mdict['DaemonMU']] and not re.search(r'Daemon',getKeywords(card)))
         and not findMarker(card,'Daemon Hosted MU')
         and card.highlight != InactiveColor 
         and card.highlight != RevealedColor):
      if action == 'INSTALL':
         card.owner.MU -= MUreq
         MUtext = ", using up  {}".format(uniMU(MUreq))
      elif action == 'UNINSTALL':
         card.owner.MU += MUreq
         MUtext = ", freeing up  {}".format(uniMU(MUreq))
   else: MUtext = ''
   if card.owner.MU < 0 and not silent: 
      notify(":::Warning:::{}'s programs require more memory than he has available. They must trash enough programs to bring their available Memory to at least 0".format(card.controller))
      information(":::ATTENTION:::\n\nYou are now using more MUs than you have available memory!\
                  \nYou need to trash enough programs to bring your Memory to 0 or higher")
   if debugVerbosity >= 3: notify("<<< chkRAM() by returning: {}".format(MUtext))
   return MUtext

def scanTable(group = table, x=0,y=0):
   if debugVerbosity >= 1: notify(">>> scanTable(){}".format(extraASDebug())) #Debug
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   if not confirm("This action will clear the internal variables and re-scan all cards in the table to fix them.\
                 \nThis action should only be used as a last-ditch effort to fix some weird behaviour in the game (e.g. treating an Ice like Agenda, or something silly like that)\
               \n\nHowever this may take some time, depending on your PC power.\
                 \nAre you sure you want to proceed?"): return
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
 
def checkUnique (card):
   if debugVerbosity >= 1: notify(">>> checkUnique(){}".format(extraASDebug())) #Debug
   mute()
   if not re.search(r'Unique', getKeywords(card)): 
      if debugVerbosity >= 3: notify("<<< checkUnique() - Not a unique card") #Debug
      return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and fetchProperty(c, 'name') == fetchProperty(card, 'name') and re.search(r'Unique', getKeywords(c)) ]
   if len(ExistingUniques) != 0 and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be Trashed at no cost)".format(fetchProperty(card, 'name'))) : return False
   else:
      for uniqueC in ExistingUniques: trashForFree(uniqueC)
   if debugVerbosity >= 3: notify("<<< checkUnique() - Returning True") #Debug
   return True   
   
def clearAttachLinks(card):
# This function takes care to discard any attachments of a card that left play
# It also clear the card from the host dictionary, if it was itself attached to another card
# If the card was hosted by a Daemon, it also returns the free MU token to that daemon
   if debugVerbosity >= 1: notify(">>> clearAttachLinks()") #Debug
   hostCards = eval(getGlobalVariable('Host Cards'))
   cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
   if cardAttachementsNR >= 1:
      hostCardSnapshot = dict(hostCards)
      for attachment in hostCardSnapshot:
         if hostCardSnapshot[attachment] == card._id:
            if Card(attachment) in table: intTrashCard(Card(attachment),0,cost = "host removed")
            del hostCards[attachment]
   if debugVerbosity >= 2: notify("### Checking if the card is attached to unlink.")      
   if hostCards.has_key(card._id):
      hostCard = Card(hostCards[card._id])
      if re.search(r'Daemon',getKeywords(hostCard)) and hostCard.group == table: 
         if card.markers[mdict['DaemonMU']] and not re.search(r'Daemon',getKeywords(card)):
            hostCard.markers[mdict['DaemonMU']] += card.markers[mdict['DaemonMU']] # If the card was hosted by a Daemon, we return any Daemon MU's used.
         DaemonHosted = findMarker(card,'Daemon Hosted MU')
         if DaemonHosted: # if the card just removed was a daemon hosted by a daemon, then it's going to have a different kind of token.
            hostCard.markers[mdict['DaemonMU']] += card.markers[DaemonHosted] # If the card was hosted by a Daemon, we return any Daemon MU's used.
      del hostCards[card._id] # If the card was an attachment, delete the link
   setGlobalVariable('Host Cards',str(hostCards))
   if debugVerbosity >= 3: notify("<<< clearAttachLinks()") #Debug   
 
def resetAll(): # Clears all the global variables in order to start a new game.
   if debugVerbosity >= 1: notify(">>> resetAll(){}".format(extraASDebug())) #Debug
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   global installedCount, debugVerbosity,newturn,endofturn, currClicks, turn
   mute()
   me.counters['Credits'].value = 5
   me.counters['Hand Size'].value = 5
   me.counters['Tags'].value = 0
   me.counters['Agenda Points'].value = 0
   me.counters['Bad Publicity'].value = 0
   Stored_Type.clear()
   Stored_Cost.clear()
   Stored_Keywords.clear()
   Stored_AutoActions.clear()
   Stored_AutoScripts.clear()
   installedCount.clear()
   setGlobalVariable('CurrentTraceEffect','None')
   setGlobalVariable('CorpTraceValue','None')
   newturn = False 
   endofturn = False
   currClicks = 0
   turn = 0
   ShowDicts()
   if len(players) > 1: debugVerbosity = -1 # Reset means normal game.
   elif debugVerbosity != -1 and confirm("Reset Debug Verbosity?"): debugVerbosity = -1    
   if debugVerbosity >= 1: notify("<<< resetAll()") #Debug
#------------------------------------------------------------------------------
# Switches
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

def switchTriggersAutomation(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchTriggersAutomation(){}".format(extraASDebug())) #Debug
   switchAutomation('Triggers')
   
def switchWinForms(group,x=0,y=0):
   if debugVerbosity >= 1: notify(">>> switchWinForms(){}".format(extraASDebug())) #Debug
   switchAutomation('WinForms')
   
def switchUniCode(group,x=0,y=0,command = 'Off'):
   if debugVerbosity >= 1: notify(">>> switchUniCode(){}".format(extraASDebug())) #Debug
   global UniCode
   if UniCode and command != 'On':
      whisper("Credits and Clicks will now be displayed as normal ASCII.".format(me))
      UniCode = False
   else:
      whisper("Credits and Clicks will now be displayed as Unicode.".format(me))
      UniCode = True

def ImAProAtThis(group = table, x=0, y=0):
   if debugVerbosity >= 1: notify(">>> ImAProAtThis(){}".format(extraASDebug())) #Debug
   global DMGwarn, Dummywarn, DummyTrashWarn, ExposeTargetsWarn, RevealandShuffleWarn, PriorityInform, AfterRunInf, AfterTraceInf
   DMGwarn = False 
   Dummywarn = False 
   ExposeTargetsWarn = False
   RevealandShuffleWarn = False
   DummyTrashWarn = False
   PriorityInform = False
   AfterRunInf = False
   AfterTraceInf = False
   whisper("-- All Newbie warnings have been disabled. Play safe.")

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
#  Online Functions
#------------------------------------------------------------------------------

def versionCheck():
   if debugVerbosity >= 1: notify(">>> versionCheck()") #Debug
   global startupMsg
   me.setGlobalVariable('gameVersion',gameVersion)
   if not startupMsg:
      (url, code) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/current_version.txt')
      if debugVerbosity >= 2: notify("### url:{}, code: {}".format(url,code)) #Debug
      if code != 200 or not url:
         whisper(":::WARNING::: Cannot check version at the moment.")
         return
      detailsplit = url.split('||')
      currentVers = detailsplit[0].split('.')
      installedVers = gameVersion.split('.')
      if debugVerbosity >= 2: notify("### Finished version split. About to check") #Debug
      if len(installedVers) < 3:
         whisper("Your game definition does not follow the correct version conventions. It is most likely outdated or modified from its official release.")
         startupMsg = True
      elif (num(currentVers[0]) > num(installedVers[0]) or 
           (num(currentVers[0]) == num(installedVers[0]) and num(currentVers[1]) > num(installedVers[1])) or 
           (num(currentVers[0]) == num(installedVers[0]) and num(currentVers[1]) == num(installedVers[1]) and num(currentVers[2]) > num(installedVers[2]))):
         notify("{}'s game definition ({}) is out-of-date!".format(me, gameVersion))
         if confirm("There is a new game definition available!\nYour version: {}.\nCurrent version: {}\n{}\
                     {}\
                 \n\nDo you want to be redirected to download the latest version?.\
                   \n(You'll have to download the game definition, any patch for the current version and the markers if they're newer than what you have installed)\
                     ".format(gameVersion, detailsplit[0],detailsplit[2],detailsplit[1])):
            openUrl('http://octgn.gamersjudgement.com/viewtopic.php?f=52&t=494')
         startupMsg = True
      if debugVerbosity >= 2: notify("### Finished version check. Seeing if I should MOTD.") #Debug
      if not startupMsg: MOTD() # If we didn't give out any other message , we give out the MOTD instead.
      startupMsg = True
   if debugVerbosity >= 3: notify("<<< versionCheck()") #Debug
      
      
def MOTD():
   if debugVerbosity >= 1: notify(">>> MOTD()") #Debug
   (MOTDurl, MOTDcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/MOTD.txt')
   (DYKurl, DYKcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/DidYouKnow.txt')
   if (MOTDcode != 200 or not MOTDurl) or (DYKcode !=200 or not DYKurl):
      whisper(":::WARNING::: Cannot fetch MOTD or DYK info at the moment.")
      return
   DYKlist = DYKurl.split('||')
   DYKrnd = rnd(0,len(DYKlist)-1)
   while MOTDdisplay(MOTDurl,DYKlist[DYKrnd]) == 'MORE': 
      MOTDurl = '' # We don't want to spam the MOTD for the further notifications
      DYKrnd += 1
      if DYKrnd == len(DYKlist): DYKrnd = 0
   if debugVerbosity >= 3: notify("<<< MOTD()") #Debug
   
def MOTDdisplay(MOTD,DYK):
   if debugVerbosity >= 1: notify(">>> MOTDdisplay()") #Debug
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
   if debugVerbosity >= 1: notify(">>> initGame()") #Debug
   if getGlobalVariable('gameGUID') != 'None': return #If we've already grabbed a GUID, then just use that.
   (gameInit, initCode) = webRead('http://84.205.248.92/slaghund/init.slag')
   if initCode != 200:
      #whisper("Cannot grab GameGUID at the moment!") # Maybe no need to inform players yet.
      return
   if debugVerbosity >= 2: notify("### {}".format(gameInit)) #Debug
   GUIDregex = re.search(r'([0-9a-f-]{36}).*?',gameInit)
   if GUIDregex: setGlobalVariable('gameGUID',GUIDregex.group(1))
   else: setGlobalVariable('gameGUID','None') #If for some reason the page does not return a propert GUID, we won't record this game.
   setGlobalVariable('gameEnded','False')
   if debugVerbosity >= 3: notify("<<< initGame()") #Debug
   
def reportGame(result = 'AgendaVictory'): # This submits the game results online.
   delayed_whisper("Please wait. Submitting Game Stats...")     
   if debugVerbosity >= 1: notify(">>> reportGame()") #Debug
   GUID = getGlobalVariable('gameGUID')
   if GUID == 'None' and debugVerbosity < 0: return # If we don't have a GUID, we can't submit. But if we're debugging, we go through.
   gameEnded = getGlobalVariable('gameEnded')
   if gameEnded == 'True':
     if not confirm("Your game already seems to have finished once before. Do you want to change the results to '{}' for {}?".format(result,me.name)): return
   #LEAGUE = fetchLeagues()
   LEAGUE = '' #Disabled as I don't think I need this part of the code anymore.
   PLAYER = me.name # Seeting some variables for readability in the URL
   id = getSpecial('Identity',me)
   IDENTITY = id.Subtitle
   RESULT = result
   GNAME = currentGameName()
   if result == 'Flatlined' or result == 'Conceded' or result == 'DeckDefeat': WIN = 0
   else: WIN = 1
   SCORE = me.counters['Agenda Points'].value
   deckStats = eval(me.getGlobalVariable('Deck Stats'))
   if debugVerbosity >= 2: notify("### Retrieved deckStats ") #Debug
   if debugVerbosity >= 2: notify("### deckStats = {}".format(deckStats)) #Debug
   INFLUENCE = deckStats[0]
   CARDSNR = deckStats[1]
   AGENDASNR = deckStats[2]
   TURNS = turn
   VERSION = gameVersion
   if debugVerbosity >= 2: notify("### About to report player results online.") #Debug
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
   E_IDENTITY = enemyIdent.Subtitle
   if debugVerbosity >= 2: notify("### Enemy Identity Name: {}".format(E_IDENTITY)) #Debug
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
   else: 
      E_RESULT = 'Unknown'
      E_WIN = 0
   E_SCORE = enemyPL.counters['Agenda Points'].value
   if debugVerbosity >= 2: notify("### About to retrieve E_deckStats") #Debug
   E_deckStats = eval(enemyPL.getGlobalVariable('Deck Stats'))
   if debugVerbosity >= 2: notify("### E_deckStats = {}".format(E_deckStats)) #Debug
   E_INFLUENCE = E_deckStats[0]
   E_CARDSNR = E_deckStats[1]
   E_AGENDASNR = E_deckStats[2]
   if ds == 'corp': E_TURNS = turn - 1 # If we're a corp, the opponent has played one less turn than we have.
   else: E_TURNS = turn # If we're the runner, the opponent has played one more turn than we have.
   E_VERSION = enemyPL.getGlobalVariable('gameVersion')
   if debugVerbosity >= 2: notify("### About to report enemy results online.") #Debug
   if debugVerbosity < 1: # We only submit stats if we're not debugging
      (EreportTXT, EreportCode) = webRead('http://84.205.248.92/slaghund/game.slag?g={}&u={}&id={}&r={}&s={}&i={}&t={}&cnr={}&anr={}&v={}&w={}&lid={}&gname={}'.format(GUID,ENEMY,E_IDENTITY,E_RESULT,E_SCORE,E_INFLUENCE,E_TURNS,E_CARDSNR,E_AGENDASNR,E_VERSION,E_WIN,LEAGUE,GNAME),10000)
   setGlobalVariable('gameEnded','True')
   if debugVerbosity >= 3: notify("<<< reportGame()") #Debug

def fetchLeagues():
   if debugVerbosity >= 1: notify(">>> fetchLeagues()") #Debug
   #return '' ### Code still WiP! Remove this at 1.1.16
   (LeagueTXT, LeagueCode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/Leagues.txt')
   if LeagueCode != 200 or not LeagueTXT:
      whisper(":::WARNING::: Cannot check League Details online.")
      return ''
   if LeagueTXT == "No Leagues Ongoing": return
   leaguesSplit = LeagueTXT.split('-----') # Five dashes separate on league from another
   opponent = ofwhom('onOpponent')
   for league in leaguesSplit:
      leagueMatches = league.split('\n')
      if debugVerbosity >= 4: notify("### League Linebreak Splits: {}".format(leagueMatches))
      for matchup in leagueMatches:
         if re.search(r'{}'.format(me.name),matchup, re.IGNORECASE) and re.search(r'{}'.format(opponent.name),matchup, re.IGNORECASE): #Check if the player's name exists in the league
            leagueDetails = league.split('=====') # Five equals separate the league name from its participants
            timeDetails = leagueDetails[1].strip() # We grab the time after which the matchup are not valid anymore.
            endTimes = timeDetails.split('.')
            currenttime = time.gmtime(time.time())
            if debugVerbosity >= 2: notify("### Current Time:{}\n### End Times:{}".format(currenttime,endTimes)) #Debug
            if endTimes[0] >= currenttime[0] and endTimes[1] >= currenttime[1] and endTimes[2] >= currenttime[2] and endTimes[3] >= currenttime[3] and endTimes[4] >= currenttime[4]:          
               if confirm("Was this a match for the {} League?".format(leagueDetails[0])):
                  return leagueDetails[0] # If we matched a league, the return the first entry in the list, which is the league name.
   return '' # If we still haven't found a league name, it means the player is not listed as taking part in a league.
   
def fetchCardScripts(group = table, x=0, y=0): # Creates 2 dictionaries with all scripts for all cards stored, based on a web URL or the local version if that doesn't exist.
   if debugVerbosity >= 1: notify(">>> fetchCardScripts()") #Debug
   global CardsAA, CardsAS # Global dictionaries holding Card AutoActions and Card AutoScripts for all cards.
   whisper("+++ Fetching fresh scripts. Please Wait...")
   if (len(players) > 1 or debugVerbosity == 0) and me.name != 'dbzer0': # I put my debug account to always use local scripts.
      try: (ScriptsDownload, code) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/scripts/CardScripts.py',5000)
      except: 
         if debugVerbosity >= 0: notify("Timeout Error when trying to download scripts")
         code = ScriptsDownload = None
   else: # If we have only one player, we assume it's a debug game and load scripts from local to save time.
      if debugVerbosity >= 0: notify("Skipping Scripts Download for faster debug")
      code = 0
      ScriptsDownload = None
   if debugVerbosity >= 4: notify("### code:{}, text: {}".format(code, ScriptsDownload)) #Debug
   if code != 200 or not ScriptsDownload or (ScriptsDownload and not re.search(r'ANR CARD SCRIPTS', ScriptsDownload)) or debugVerbosity >= 0: 
      whisper(":::WARNING::: Cannot download card scripts at the moment. Will use localy stored ones.")
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
      if debugVerbosity >= 2: notify(Split_Details[0].strip()) # If it's the card name, notify us of it.
      Split_Scripts = Split_Details[2].split('+++++') # List item [1] always holds the two scripts. AutoScripts and AutoActions.
      CardsAS[Split_Details[1].strip()] = Split_Scripts[0].strip()
      CardsAA[Split_Details[1].strip()] = Split_Scripts[1].strip()
   if turn > 0: whisper("+++ All card scripts refreshed!")
   if debugVerbosity >= 4: # Debug
      notify("CardsAS Dict:\n{}".format(str(CardsAS)))
      notify("CardsAA Dict:\n{}".format(str(CardsAA))) 
   if debugVerbosity >= 3: notify("<<< fetchCardScripts()") #Debug

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
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         ImAProAtThis() # At debug level 1, we also disable all warnings
      elif debugVerbosity == 1: debugVerbosity = 2
      elif debugVerbosity == 2: debugVerbosity = 3
      elif debugVerbosity == 3: debugVerbosity = 4
      else: debugVerbosity = 0
      notify("Debug verbosity is now: {}".format(debugVerbosity))
      if ds == "corp": 
         notify("Runner now")
         ds = "runner"
      else: 
         ds = "corp"
         notify("Corp Now")
      return
   if me.name == 'db0' or me.name == 'dbzer0': 
      debugVerbosity = 0
      fetchCardScripts()
   if not (len(players) == 1 or debugVerbosity >= 0): 
      whisper("This function is only for development purposes")
      return
   ######## Testing Corner ########
   if ds == "corp": 
      notify("Runner now")
      ds = "runner"
   else: 
      ds = "corp"
      notify("Corp Now")
   ###### End Testing Corner ######
   testcards = ["bc0f047c-01b1-427f-a439-d451eda02039", #Corporate Retreat
                "bc0f047c-01b1-427f-a439-d451eda01004", #Stimhack
                "bc0f047c-01b1-427f-a439-d451eda02025", #Compromised Employee
                "bc0f047c-01b1-427f-a439-d451eda02032", #Fetal AI
                "bc0f047c-01b1-427f-a439-d451eda02026", #Notoriety
                "bc0f047c-01b1-427f-a439-d451eda02002", #Spinal Modem
                "bc0f047c-01b1-427f-a439-d451eda02021", #Vamp
                "bc0f047c-01b1-427f-a439-d451eda02033", #Trick of Light
                "bc0f047c-01b1-427f-a439-d451eda02030"] #Sherlock
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
   notify("### Variables Reset") #Debug   
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      notify("### Playerside not chosen yet. Doing now") #Debug   
      chooseSide()
      notify("### About to create starting cards.") #Debug   
      createStartingCards()
   notify("<<< TrialError()") #Debug
   if confirm("Spawn Test Cards?"):
      for idx in range(len(testcards)):
         test = table.create(testcards[idx], (70 * idx) - 150, 0, 1, True)
         storeProperties(test)
         if test.Type == 'ICE' or test.Type == 'Agenda' or test.Type == 'Asset': test.isFaceUp = False


def ShowDicts():
   if debugVerbosity < 0: return
   notify("Stored_Types:\n {}".format(str(Stored_Type)))
   notify("Stored_Costs:\n {}".format(str(Stored_Cost)))
   notify("Stored_Keywords: {}".format(str(Stored_Keywords)))
   if debugVerbosity >= 4: notify("Stored_AA: {}".format(str(Stored_AutoActions)))
   if debugVerbosity >= 4: notify("Stored_AS: {}".format(str(Stored_AutoScripts)))
   notify("installedCounts: {}".format(str(installedCount)))

def DebugCard(card, x=0, y=0):
   whisper("Stored Card Properties\
          \n----------------------\
          \nType: {}\
          \nKeywords: {}\
          \nCost: {}\
          \nCard ID: {}\
          \n----------------------\
          ".format(Stored_Type.get(card._id,'NULL'), Stored_Keywords.get(card._id,'NULL'), Stored_Cost.get(card._id,'NULL'),card._id))
   if debugVerbosity >= 4: 
      #notify("Stored_AS: {}".format(str(Stored_AutoScripts)))
      notify("Downloaded AA: {}".format(str(CardsAA)))
      notify("Card's AA: {}".format(CardsAA.get(card.model,'???')))
   storeProperties(card, True)
   if Stored_Type.get(card._id,'?') != 'ICE': card.orientation = Rot0
   
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
      
