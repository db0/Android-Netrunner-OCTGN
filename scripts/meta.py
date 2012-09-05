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
###=================================================================================================================###
import re

Automations = {'Play, Score and Rez'    : True, # If True, game will automatically trigger card effects when playing or double-clicking on cards. Requires specific preparation in the sets.
               'Start/End-of-Turn'      : True, # If True, game will automatically trigger effects happening at the start of the player's turn, from cards they control.                
               'Damage Prevention'      : True, # If True, game will automatically use damage prevention counters from card they control.                
               'Triggers'               : True, # If True, game will search the table for triggers based on player's actions, such as installing a card, or trashing one.
               'Damage'                 : True}

UniCode = True # If True, game will display credits, clicks, trash, memory as unicode characters

debugVerbosity = -1 # At -1, means no debugging messages display

startupMsg = False # Used to check if the player has checked for the latest version of the game.

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
   strippedKeywordsList = card.Keywords.split('-')
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
   Stored_Keywords[card] = keywords[:-1] # We also update the global variable for this card, which is used by many functions.
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
   if debugVerbosity >= 1: notify(">>> storeSpecial(){}".format(extraASDebug())) #Debug
   storeProperties(card)
   specialCards = eval(me.getGlobalVariable('specialCards'))
   specialCards[card.Type] = card._id
   me.setGlobalVariable('specialCards', str(specialCards))

def getSpecial(cardType,player = me):
# Functions takes as argument the name of a special card, and the player to whom it belongs, and returns the card object.
   if debugVerbosity >= 1: notify(">>> getSpecial(){}".format(extraASDebug())) #Debug
   specialCards = eval(player.getGlobalVariable('specialCards'))
   if debugVerbosity >= 3: notify("<<< getSpecial() by returning: {}".format(Card(specialCards[cardType])))
   return Card(specialCards[cardType])

def chkRAM(card, action = 'INSTALL', silent = False):
   if debugVerbosity >= 1: notify(">>> chkRAM(){}".format(extraASDebug())) #Debug
   MUreq = num(fetchProperty(card,'Requirement'))
   if MUreq > 0 and not card.markers[mdict['DaemonMU']] and card.highlight != InactiveColor and card.highlight != RevealedColor:
      if action == 'INSTALL':
         card.controller.MU -= MUreq
         MUtext = ", using up  {}".format(uniMU(MUreq))
      elif action == 'UNINSTALL':
         card.controller.MU += MUreq
         MUtext = ", freeing up  {}".format(uniMU(MUreq))
   else: MUtext = ''
   if card.controller.MU < 0 and not silent: notify(":::Warning:::{}'s programs require more memory than he has available. They must trash enough programs to bring their available Memory to at least 0".format(card.controller))
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
   if not re.search(r'Unique', getKeywords(card)): return True #If the played card isn't unique do nothing.
   ExistingUniques = [ c for c in table
         if c.owner == me and c.isFaceUp and c.name == card.name and re.search(r'Unique', getKeywords(c)) ]
   if len(ExistingUniques) != 0 and not confirm("This unique card is already in play. Are you sure you want to play {}?\n\n(If you do, your existing unique card will be {} at no cost)".format(card.name,uniTrash())) : return False
   else:
      for uniqueC in ExistingUniques: trashForFree(uniqueC)
   return True   
 
def resetAll(): # Clears all the global variables in order to start a new game.
   if debugVerbosity >= 1: notify(">>> resetAll(){}".format(extraASDebug())) #Debug
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   global installedCount, debugVerbosity,newturn,endofturn, currClicks
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
   newturn = False 
   endofturn = False
   currClicks = 0
   ShowDicts()
   debugVerbosity = -1 # Reset means normal game.
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
# Version checking and MOTD
#------------------------------------------------------------------------------

def versionCheck():
   if debugVerbosity >= 1: notify(">>> versionCheck()") #Debug
   global startupMsg
   if not startupMsg:
      (url, code) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/current_version.txt')
      if code != 200:
         whisper("Cannot check version page at the moment.")
         return
      detailsplit = url.split('||')
      currentVers = detailsplit[0].split('.')
      installedVers = gameVersion.split('.')
      if len(installedVers) < 3:
         whisper("Your game definition does not follow the correct version conventions. It is most likely outdated or modified from its official release.")
         startupMsg = True
      elif currentVers[0] != installedVers[0] or currentVers[1] != installedVers[1] or currentVers[2] != installedVers[2]:
         notify("{}'s game definition ({}) is out-of-date!".format(me, gameVersion))
         if confirm("There is a new game definition available!\nYour version: {}.\nCurrent version: {}\
                     {}\
                 \n\nDo you want to be redirected to download the latest version?.\
                   \n(You'll have to download the game definition, any patch for the current version and the markers if they're newer than what you have installed)\
                     ".format(gameVersion, detailsplit[0],detailsplit[2],detailsplit[1])):
            openUrl('https://github.com/db0/Android-Netrunner-OCTGN/downloads')
         startupMsg = True
      elif len(currentVers) == 4:
         if len(installedVers) < 4: emergencyV = True 
         elif currentVers[3] != installedVers[3]: emergencyV = True 
         else: emergencyV = False
         if emergencyV and confirm("There is an emergency fix available for your current version!\nYour version: {}.\nCurrent version: {}.\
                                    {}\
                                \n\nDo you want to be redirected to download the latest version?.\
                                  \n(An emergency update probably means there's a significant bug left in the engine. We strongly suggest you update before proceeding.)\
                                    ".format(gameVersion, detailsplit[0],detailsplit[1])): 
            openUrl('https://github.com/db0/Android-Netrunner-OCTGN/downloads')
         startupMsg = True
      if not startupMsg: MOTD() # If we didn't give out any other message , we give out the MOTD instead.
      startupMsg = True
   if debugVerbosity >= 3: notify("<<< versionCheck()") #Debug
      
      
def MOTD():
   if debugVerbosity >= 1: notify(">>> MOTD()") #Debug
   (MOTDurl, MOTDcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/MOTD.txt')
   (DYKurl, DYKcode) = webRead('https://raw.github.com/db0/Android-Netrunner-OCTGN/master/DidYouKnow.txt')
   if MOTDcode != 200 or DYKcode !=200:
      whisper("Cannot check MOTD or DYK page at the moment.")
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
   
#------------------------------------------------------------------------------
# Debugging
#------------------------------------------------------------------------------
   
def TrialError(group, x=0, y=0): # Debugging
   global ds, debugVerbosity
   mute()
   ######## Testing Corner ########
   #for hook in regexHooks: notify("regex for {} is {}".format(hook, regexHooks[hook]))
   #if regexHooks['GainX'].search('TrashMyself'): confirm("Found!")
   #else: confirm("Not Found :(")
   ###### End Testing Corner ######
   if debugVerbosity >=0: 
      if debugVerbosity == 0: 
         debugVerbosity = 1
         ImAProAtThis() # At debug level 1, we also disable all warnings
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
   testcards = ["bc0f047c-01b1-427f-a439-d451eda01018", #Account Siphon
                "bc0f047c-01b1-427f-a439-d451eda01030", #Crash Space
                "bc0f047c-01b1-427f-a439-d451eda01056", #Adonis Campaign
                "bc0f047c-01b1-427f-a439-d451eda01081", #AstroScript Pilot Program
                "bc0f047c-01b1-427f-a439-d451eda01057", #Aggressive Secretary
                "bc0f047c-01b1-427f-a439-d451eda01029", #Bank Job
                "bc0f047c-01b1-427f-a439-d451eda01052", #Access to Globalsec
                "bc0f047c-01b1-427f-a439-d451eda01060", #Shipment from Mirrormorph
                "bc0f047c-01b1-427f-a439-d451eda01031"] #Data Dealer # Checking to see if the targeting works.
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
   if not playerside:  # If we've already run this command once, don't recreate the cards.
      chooseSide()
      createStartingCards()
#   for idx in range(len(testcards)):
#      test = table.create(testcards[idx], (70 * idx) - 150, 0, 1, True)
#      storeProperties(test)
#      if test.Type == 'ICE' or test.Type == 'Agenda' or test.Type == 'Asset': test.isFaceUp = False


def ShowDicts():
   if debugVerbosity < 0: return
   notify("Stored_Types:\n {}".format(str(Stored_Type)))
   notify("Stored_Costs:\n {}".format(str(Stored_Cost)))
   notify("Stored_Keywords: {}".format(str(Stored_Keywords)))
   notify("Stored_AA: {}".format(str(Stored_AutoActions)))
   notify("Stored_AS: {}".format(str(Stored_AutoScripts)))
   notify("installedCounts: {}".format(str(installedCount)))

def DebugCard(card, x=0, y=0):
   whisper("Stored Card Properties\
          \n----------------------\
          \nType: {}\
          \nKeywords: {}\
          \nCost: {}\
          \nCard ID: {}\
          \n----------------------\
          ".format(Stored_Type[card], Stored_Keywords[card], Stored_Cost[card],card._id))
   storeProperties(card)
   
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