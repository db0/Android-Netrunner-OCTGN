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
# This file contains the autoscripting of the game. These are the actions that trigger automatically
#  when the player plays a card, double-clicks on one, or goes to Start/End ot Turn/Run
# * [Play/Score/Rez/Trash trigger] is basically used when the a card enters or exist play in some way 
# * [Card Use trigger] is used when a card is being used while on the table. I.e. being double-clicked.
# * [Other Player trigger] is used when another player plays a card or uses an action. The other player basically do your card effect for you
# * [Start/End of Turn/Run trigger] is called at the start/end of turns or runs actions.
# * [Core Commands] is the primary place where all the autoscripting magic happens.
# * [Helper Commands] are usually shared by many Core Commands, or maybe used many times in one of them.
###=================================================================================================================###

import re

secretCred = None # Used to allow the player to spend credits in secret for some card abilities (e.g. Snowflake)
failedRequirement = True # A Global boolean that we set in case an Autoscript cost cannot be paid, so that we know to abort the rest of the script.
EscherUse = 0

#------------------------------------------------------------------------------
# Play/Score/Rez/Trash trigger
#------------------------------------------------------------------------------

def executePlayScripts(card, action):
   action = action.upper() # Just in case we passed the wrong case
   debugNotify(">>> executePlayScripts() for {} with action: {}".format(card,action)) #Debug
   debugNotify("AS dict entry = {}".format(CardsAS.get(card.model,'NULL')),4)
   debugNotify("card.model = {}".format(card.model),4)
   global failedRequirement
   if not Automations['Play, Score and Rez']: 
      debugNotify("Exiting because automations are off", 2)
      return
   if CardsAS.get(card.model,'NULL') == 'NULL': 
      debugNotify("Exiting because card has no autoscripts", 2)
      return
   failedRequirement = False
   X = 0
   Autoscripts = CardsAS.get(card.model,'').split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
   autoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
   for autoS in autoScriptsSnapshot: # Checking and removing any scripts which are not parsed at this point.
      if (autoS == '' or 
          re.search(r'atTurn(Start|End)', autoS) or 
          re.search(r'atRunStart', autoS) or 
          re.search(r'Reduce[0-9#X]Cost', autoS) or 
          re.search(r'whileRunning', autoS) or 
          re.search(r'atJackOut', autoS) or 
          re.search(r'atSuccessfulRun', autoS) or 
          re.search(r'onAccess', autoS) or 
          re.search(r'onHost', autoS) or 
          re.search(r'Placement', autoS) or 
          re.search(r'CaissaPlace', autoS) or 
          re.search(r'whileInPlay', autoS) or 
          re.search(r'onDragDrop', autoS) or 
          re.search(r'ConstantAbility', autoS) or 
          re.search(r'onPay', autoS) or # onPay effects are only useful before we go to the autoscripts, for the cost reduction.
          re.search(r'triggerNoisy', autoS) or # Trigger Noisy are used automatically during action use.
          re.search(r'-isTrigger', autoS)): Autoscripts.remove(autoS)
      elif re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'CustomScript', autoS): 
         CustomScript(card,action)
         Autoscripts.remove(autoS)
   if len(Autoscripts) == 0: return
   if debugVerbosity >= 2: notify ('Looking for multiple choice options') # Debug
   if action == 'PLAY': trigger = 'onPlay' # We figure out what can be the possible multiple choice trigger
   elif action == 'REZ': trigger = 'onRez'
   elif action == 'INSTALL': trigger = 'onInstall'
   elif action == 'SCORE': trigger = 'onScore'
   elif action == 'TRASH': trigger = 'onTrash'
   else: trigger = 'N/A'
   if debugVerbosity >= 2: notify ('trigger = {}'.format(trigger)) # Debug
   if trigger != 'N/A': # If there's a possibility of a multiple choice trigger, we do the check
      TriggersFound = [] # A List which will hold any valid abilities for this trigger
      for autoS in Autoscripts:
         if re.search(r'{}:'.format(trigger),autoS): # If the script has the appropriate trigger, we put it into the list.
            TriggersFound.append(autoS)
      if debugVerbosity >= 2: notify ('TriggersFound = {}'.format(TriggersFound)) # Debug
      if len(TriggersFound) > 1: # If we have more than one option for this trigger, we need to ask the player for which to use.
         if Automations['WinForms']: ChoiceTXT = "This card has multiple abilities that can trigger at this point.\nSelect the ones you would like to use."
         else: ChoiceTXT = "This card has multiple abilities that can trigger at this point.\nType the number of the one you would like to use."
         triggerInstructions = re.search(r'{}\[(.*?)\]'.format(trigger),card.Instructions) # If the card has multiple options, it should also have some card instructions to have nice menu options.
         if not triggerInstructions and debugVerbosity >= 1: notify("## Oops! No multiple choice instructions found and I expected some. Will crash prolly.") # Debug
         cardInstructions = triggerInstructions.group(1).split('|-|') # We instructions for trigger have a slightly different split, so as not to conflict with the instructions from AutoActions.
         choices = cardInstructions
         abilChoice = SingleChoice(ChoiceTXT, choices, type = 'button')
         if abilChoice == 'ABORT' or abilChoice == None: return # If the player closed the window, or pressed Cancel, abort.
         TriggersFound.pop(abilChoice) # What we do now, is we remove the choice we made, from the list of possible choices. We remove it because then we will remove all the other options from the main list "Autoscripts"
         for unchosenOption in TriggersFound:
            if debugVerbosity >= 4: notify (' Removing unused option: {}'.format(unchosenOption)) # Debug
            Autoscripts.remove(unchosenOption)
         if debugVerbosity >= 2: notify ('Final Autoscripts after choices: {}'.format(Autoscripts)) # Debug
   for autoS in Autoscripts:
      debugNotify("First Processing: {}".format(autoS), 2) # Debug
      effectType = re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', autoS)
      if not effectType:
         debugNotify("no regeX match for playscripts. aborting",4)
         continue
      else: debugNotify("effectType.group(1)= {}".format(effectType.group(1)),4)
      if ((effectType.group(1) == 'onRez' and action != 'REZ') or # We don't want onPlay effects to activate onTrash for example.
          (effectType.group(1) == 'onPlay' and action != 'PLAY') or
          (effectType.group(1) == 'onInstall' and action != 'INSTALL') or
          (effectType.group(1) == 'onScore' and action != 'SCORE') or
          (effectType.group(1) == 'onStartup' and action != 'STARTUP') or
          (effectType.group(1) == 'onMulligan' and action != 'MULLIGAN') or
          (effectType.group(1) == 'whileScored' and ds != 'corp') or
          (effectType.group(1) == 'whileLiberated' and ds != 'runner') or
          (effectType.group(1) == 'onDamage' and action != 'DAMAGE') or
          (effectType.group(1) == 'onLiberation' and action != 'LIBERATE') or
          (effectType.group(1) == 'onTrash' and action != 'TRASH' and action!= 'UNINSTALL' and action != 'DEREZ') or
          (effectType.group(1) == 'onDerez' and action != 'DEREZ')): 
         debugNotify("Rejected {} because {} does not fit with {}".format(autoS,effectType.group(1),action))
         continue 
      if re.search(r'-isOptional', autoS):
         if not confirm("This card has an optional ability you can activate at this point. Do you want to do so?"): 
            notify("{} opts not to activate {}'s optional ability".format(me,card))
            return 'ABORT'
         else: notify("{} activates {}'s optional ability".format(me,card))
      selectedAutoscripts = autoS.split('$$')
      if debugVerbosity >= 2: notify ('selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for activeAutoscript in selectedAutoscripts:
         debugNotify("Second Processing: {}".format(activeAutoscript), 2) # Debug
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         if not ifHave(activeAutoscript): continue # If the script requires the playet to have a specific counter value and they don't, do nothing.
         if not ifVarSet(activeAutoscript): continue # If the script requires a shared AutoScript variable to be set to a specific value.
         if not checkOrigSpecialRestrictions(activeAutoscript,card): continue  
         if not chkRunStatus(activeAutoscript): continue
         if re.search(r'-ifAccessed', activeAutoscript) and ds != 'runner': 
            debugNotify("!!! Failing script because card is not being accessed")
            continue # These scripts are only supposed to fire from the runner (when they access a card)         
         if re.search(r'-ifActive', activeAutoscript):
            if card.highlight == InactiveColor or card.highlight == RevealedColor or card.group.name != 'Table':
               debugNotify("!!! Failing script because card is inactive. highlight == {}. group.name == {}".format(card.highlight,card.group.name))
               continue 
            else: debugNotify("Succeeded for -ifActive. highlight == {}. group.name == {}".format(card.highlight,card.group.name))
         else: debugNotify("No -ifActive Modulator")
         if re.search(r'-ifScored', activeAutoscript) and not card.markers[mdict['Scored']] and not card.markers[mdict['ScorePenalty']]:
            debugNotify("!!! Failing script because card is not scored")
            continue 
         if re.search(r'-ifUnscored', activeAutoscript) and (card.markers[mdict['Scored']] or card.markers[mdict['ScorePenalty']]):
            debugNotify("!!! Failing script because card is scored")
            continue 
         if re.search(r':Pass\b', activeAutoscript): continue # Pass is a simple command of doing nothing ^_^
         effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\|:,<>+ -]*)', activeAutoscript)
         if not effect: 
            whisper(":::ERROR::: In AutoScript: {}".format(activeAutoscript))
            continue
         debugNotify('effects: {}'.format(effect.groups()), 2) #Debug
         if effectType.group(1) == 'whileRezzed' or effectType.group(1) == 'whileInstalled' or effectType.group(1) == 'whileScored' or effectType.group(1) == 'whileLiberated':
            if action == 'STARTUP' or action == 'MULLIGAN': 
               debugNotify("Aborting while(Rezzed|Scored|etc) because we're on statup/mulligan")
               continue # We don't want to run whileRezzed events during startup
            else: debugNotify("not on statup/mulligan. proceeding")
            if effect.group(1) != 'Gain' and effect.group(1) != 'Lose': continue # The only things that whileRezzed and whileScored affect in execute Automations is GainX scripts (for now). All else is onTrash, onPlay etc
            if action == 'DEREZ' or ((action == 'TRASH' or action == 'UNINSTALL') and card.highlight != InactiveColor and card.highlight != RevealedColor): Removal = True
            else: Removal = False
         #elif action == 'DEREZ' or action == 'TRASH': continue # If it's just a one-off event, and we're trashing it, then do nothing.
         else: Removal = False
         targetC = findTarget(activeAutoscript)
         targetPL = ofwhom(activeAutoscript,card.owner) # So that we know to announce the right person the effect, affects.
         announceText = "{} uses {}'s ability to".format(targetPL,card)
         debugNotify(" targetC: {}".format(targetC), 3) # Debug
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
            debugNotify("passedscript: {}".format(passedScript), 2) # Debug
            gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Quick', n = X, actionType = action)
            if gainTuple == 'ABORT': return
            X = gainTuple[1] 
         else: 
            passedScript = effect.group(0)
            debugNotify("passedscript: {}".format(passedScript), 2) # Debug
            if regexHooks['CreateDummy'].search(passedScript): 
               if CreateDummy(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['DrawX'].search(passedScript): 
               if DrawX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['TokensX'].search(passedScript): 
               if TokensX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['RollX'].search(passedScript): 
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if rollTuple == 'ABORT': return
               X = rollTuple[1] 
            elif regexHooks['RequestInt'].search(passedScript): 
               numberTuple = RequestInt(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if numberTuple == 'ABORT': return
               X = numberTuple[1] 
            elif regexHooks['DiscardX'].search(passedScript): 
               discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if discardTuple == 'ABORT': return
               X = discardTuple[1] 
            elif regexHooks['RunX'].search(passedScript): 
               if RunX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['TraceX'].search(passedScript): 
               if TraceX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['PsiX'].search(passedScript): 
               if PsiX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['ReshuffleX'].search(passedScript): 
               reshuffleTuple = ReshuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if reshuffleTuple == 'ABORT': return
               X = reshuffleTuple[1]
            elif regexHooks['ShuffleX'].search(passedScript): 
               if ShuffleX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['ChooseKeyword'].search(passedScript): 
               if ChooseKeyword(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['InflictX'].search(passedScript): 
               if InflictX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['SetVarX'].search(passedScript): 
               if SetVarX(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['RetrieveX'].search(passedScript): 
               retrieveTuple = RetrieveX(passedScript, announceText, card, targetC, notification = 'Quick', n = X)
               if retrieveTuple == 'ABORT': return # Retrieve also returns the cards it found in a tuple. But we're not using those here.
               X = len(retrieveTuple[1])
            elif regexHooks['ModifyStatus'].search(passedScript): 
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
            elif regexHooks['UseCustomAbility'].search(passedScript):
               if UseCustomAbility(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': break
         if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
         debugNotify("Loop for scipt {} finished".format(passedScript), 2)

#------------------------------------------------------------------------------
# Card Use trigger
#------------------------------------------------------------------------------

def useAbility(card, x = 0, y = 0): # The start of autoscript activation.
   debugNotify(">>> useAbility(){}".format(extraASDebug())) #Debug
   mute()
   update() # Make sure all other effects have finished resolving.
   global failedRequirement,gatheredCardList
   AutoscriptsList = [] # An empty list which we'll put the AutoActions to execute.
   storeProperties(card) # Just in case
   failedRequirement = False # We set it to false when we start a new autoscript.
   debugNotify("Checking if Tracing card...", 4)
   if card.Type == 'Button': # The Special button cards.
      if card.name == 'Access Imminent': BUTTON_Access()
      elif card.name == 'No Rez': BUTTON_NoRez()
      elif card.name == 'Wait!': BUTTON_Wait()
      elif card.name == 'Start Turn': goToSot(0)
      elif card.name == 'End Turn': goToEndTurn(0)
      elif card.name == 'Grant Access': runSuccess(0)
      else:
          debugNotify("## Unknown button pressed, treating as OK",4)
          BUTTON_OK()
      return
   if (card._id in Stored_Type and fetchProperty(card, 'Type') == 'Tracing') or card.model == 'eb7e719e-007b-4fab-973c-3fe228c6ce20': # If the player double clicks on the Tracing card...
      debugNotify("+++ Confirmed tacting card. Checking Status...", 5)
      if card.isFaceUp and not card.markers[mdict['Credits']]: inputTraceValue(card, limit = 0)
      elif card.isFaceUp and card.markers[mdict['Credits']]: payTraceValue(card)
      elif not card.isFaceUp: card.isFaceUp = True
      return
   debugNotify("Not a tracing card. Checking highlight...", 4)
   if markerScripts(card): return # If there's a special marker, it means the card triggers to do something else with the default action
   if card.highlight == InactiveColor:
      accessRegex = re.search(r'onAccess:([^|]+)',CardsAS.get(card.model,''))
      if not accessRegex:
         whisper("You cannot use inactive cards. Please use the relevant card abilities to clear them first. Aborting")
         return
   if card.type == 'Identity' and card.Side == 'runner' and chkCerebralStatic(): 
         whisper("You cannot use your ID's ability because {} is active. Aborting!".format(chkCerebralStatic()))
         return
   debugNotify("Finished storing CardsAA.get(card.model,'')s. Checking Rez status", 4)
   if not card.isFaceUp:
      if re.search(r'onAccess',fetchProperty(card, 'AutoActions')) and confirm("This card has an ability that can be activated even when unrezzed. Would you like to activate that now?"): card.isFaceUp = True # Activating an on-access ability requires the card to be exposed, it it's no already.
      elif re.search(r'Hidden',fetchProperty(card, 'Keywords')): card.isFaceUp # If the card is a hidden resource, just turn it face up for its imminent use.
      elif fetchProperty(card, 'Type') == 'Agenda': 
         scrAgenda(card) # If the player double-clicks on an Agenda card, assume they wanted to Score it.
         return
      else: 
         intRez(card) # If card is face down or not rezzed assume they wanted to rez       
         return
   debugNotify("Card not unrezzed. Checking for automations switch...", 4)
   if not Automations['Play, Score and Rez'] or fetchProperty(card, 'AutoActions') == '':
      debugNotify("Going to useCard() because AA = {}".format(fetchProperty(card, 'AutoActions')))
      useCard(card) # If card is face up but has no autoscripts, or automation is disabled just notify that we're using it.
      return
   debugNotify("Automations active. Checking for CustomScript...", 4)
   if re.search(r'CustomScript', fetchProperty(card, 'AutoActions')): 
      if chkTargeting(card) == 'ABORT': return
      if CustomScript(card,'USE') == 'CLICK USED': autoscriptOtherPlayers('CardAction', card)  # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   debugNotify("+++ All checks done!. Starting Choice Parse...", 5)
   ### Checking if card has multiple autoscript options and providing choice to player.
   Autoscripts = fetchProperty(card, 'AutoActions').split('||')
   autoScriptSnapshot = list(Autoscripts)
   for autoS in autoScriptSnapshot: # Checking and removing any clickscripts which were put here in error.
      if (re.search(r'while(Rezzed|Scored)', autoS) 
         or re.search(r'on(Play|Score|Install)', autoS) 
         or re.search(r'AtTurn(Start|End)', autoS)
         or not card.isFaceUp and not re.search(r'onAccess', autoS) # If the card is still unrezzed and the ability does not have "onAccess" on it, it can't be used.
         or (re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor)
         or (re.search(r'(CreateDummy|excludeDummy)', autoS) and card.highlight == DummyColor)): # Dummies in general don't create new dummies
         Autoscripts.remove(autoS)
   debugNotify("Removed bad options", 2)
   if len(Autoscripts) == 0:
      useCard(card) # If the card had only "WhileInstalled"  or AtTurnStart effect, just announce that it is being used.
      return 
   if len(Autoscripts) > 1: 
      #abilConcat = "This card has multiple abilities.\nWhich one would you like to use?\
                #\n\n(Tip: You can put multiple abilities one after the the other (e.g. '110'). Max 9 at once)\n\n" # We start a concat which we use in our confirm window.
      if Automations['WinForms']: ChoiceTXT = "This card has multiple abilities.\nSelect the ones you would like to use, in order, and press the [Finish Selection] button"
      else: ChoiceTXT = "This card has multiple abilities.\nType the ones you would like to use, in order, and press the [OK] button"
      cardInstructions = card.Instructions.split('||')
      if len(cardInstructions) > 1: choices = cardInstructions
      else:
         choices = []
         for idx in range(len(Autoscripts)): # If a card has multiple abilities, we go through each of them to create a nicely written option for the player.
            debugNotify("Autoscripts {}".format(Autoscripts), 2) # Debug
            abilRegex = re.search(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):([A-Z][A-Za-z ]+)([0-9]*)([A-Za-z ]*)-?(.*)", Autoscripts[idx]) # This regexp returns 3-4 groups, which we then reformat and put in the confirm dialogue in a better readable format.
            debugNotify("Choice Regex is {}".format(abilRegex.groups()), 2) # Debug
            if abilRegex.group(1) != '0': abilCost = 'Use {} Clicks'.format(abilRegex.group(1))
            else: abilCost = '' 
            if abilRegex.group(2) != '0': 
               if abilCost != '': 
                  if abilRegex.group(3) != '0' or abilRegex.group(4) != '0': abilCost += ', '
                  else: abilCost += ' and '
               abilCost += 'Pay {} Credits'.format(abilRegex.group(2))
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
               if not re.search(r'-isCost', Autoscripts[idx]): 
                  abilCost = 'Activate' 
                  connectTXT = ' to '
               else: 
                  abilCost = '' # If the ability claims to be a cost, then we need to put it as part of it, before the "to"
                  connectTXT = ''
            else:
               if not re.search(r'-isCost', Autoscripts[idx]): connectTXT = ' to ' # If there isn't an extra cost, then we connect with a "to" clause
               else: connectTXT = 'and ' 
            if abilRegex.group(6):
               if abilRegex.group(6) == '999': abilX = 'all'
               else: abilX = abilRegex.group(6)
            else: abilX = abilRegex.group(6)
            if re.search(r'-isSubroutine', Autoscripts[idx]): 
               if abilCost == 'Activate':  # IF there's no extra costs to the subroutine, we just use the "enter" glyph
                  abilCost = uniSubroutine()
                  connectTXT = ''
               else: abilCost = '{} '.format(uniSubroutine()) + abilCost # If there's extra costs to the subroutine, we prepend the "enter" glyph to the rest of the costs.
            #abilConcat += '{}: {}{}{} {} {}'.format(idx, abilCost, connectTXT, abilRegex.group(5), abilX, abilRegex.group(7)) # We add the first three groups to the concat. Those groups are always Gain/Hoard/Prod ## Favo/Solaris/Spice
            choices.insert(idx,'{}{}{} {} {}'.format(abilCost, connectTXT, abilRegex.group(5), abilX, abilRegex.group(7)))
            if abilRegex.group(5) == 'Put' or abilRegex.group(5) == 'Remove' or abilRegex.group(5) == 'Refill': choices[idx] += ' counter' # If it's putting a counter, we clarify that.
            debugNotify("About to check rest of choice regex", 3)
            if abilRegex.group(8): # If the autoscript has an 8th group, then it means it has subconditions. Such as "per Marker" or "is Subroutine"
               subconditions = abilRegex.group(8).split('$$') # These subconditions are always separated by dashes "-", so we use them to split the string
               for idx2 in range(len(subconditions)):
                  debugNotify(" Checking subcondition {}:{}".format(idx2,subconditions[idx2]), 4)
                  if re.search(r'isCost', Autoscripts[idx]) and idx2 == 1: choices[idx] += ' to' # The extra costs of an action are always at the first part (i.e. before the $$)
                  elif idx2 > 0: choices[idx] += ' and'
                  subadditions = subconditions[idx2].split('-')
                  for idx3 in range(len(subadditions)):
                     debugNotify(" Checking subaddition {}-{}:{}".format(idx2,idx3,subadditions[idx3]), 4)
                     if re.search(r'warn[A-Z][A-Za-z0-9 ]+', subadditions[idx3]): continue # Don't mention warnings.
                     if subadditions[idx3] in IgnoredModulators: continue # We ignore modulators which are internal to the engine.
                     choices[idx] += ' {}'.format(subadditions[idx3]) #  Then we iterate through each distinct subcondition and display it without the dashes between them. (In the future I may also add whitespaces between the distinct words)
            #abilConcat += '\n' # Finally add a newline at the concatenated string for the next ability to be listed.
      abilChoice = multiChoice(ChoiceTXT, choices,card) # We use the ability concatenation we crafted before to give the player a choice of the abilities on the card.
      if abilChoice == [] or abilChoice == 'ABORT' or abilChoice == None: return # If the player closed the window, or pressed Cancel, abort.
      #choiceStr = str(abilChoice) # We convert our number into a string
      for choice in abilChoice: 
         if choice < len(Autoscripts): AutoscriptsList.append(Autoscripts[choice].split('$$'))
         else: continue # if the player has somehow selected a number that is not a valid option, we just ignore it
      debugNotify("AutoscriptsList: {}".format(AutoscriptsList), 2) # Debug
   else: AutoscriptsList.append(Autoscripts[0].split('$$'))
   prev_announceText = 'NULL'
   multiCount = 0
   if len(AutoscriptsList): playUseSound(card)
   startingCreds = me.Credits # We store our starting credits so that we may see if we won or lost any after our action is complete, to announce.
   for iter in range(len(AutoscriptsList)):
      debugNotify("iter = {}".format(iter), 2)
      selectedAutoscripts = AutoscriptsList[iter]
      timesNothingDone = 0 # A variable that keeps track if we've done any of the autoscripts defined. If none have been coded, we just engage the card.
      X = 0 # Variable for special costs.
      if card.highlight == DummyColor: lingering = ' the lingering effect of' # A text that we append to point out when a player is using a lingering effect in the form of a dummy card.
      else: lingering = ''
      for activeAutoscript in selectedAutoscripts:
         #confirm("Active Autoscript: {}".format(activeAutoscript)) #Debug
         ### Checking if any of the card's effects requires one or more targets first
         if re.search(r'Targeted', activeAutoscript) and findTarget(activeAutoscript, dryRun = True) == []: return
      CardAction = False # A boolean which stores if the card's ability required a click or not.
      for activeAutoscript in selectedAutoscripts:
         debugNotify("Reached ifHave chk", 3)
         if not ifHave(activeAutoscript): continue # If the script requires the playet to have a specific counter value and they don't, do nothing.
         if re.search(r'onlyOnce',activeAutoscript) and oncePerTurn(card, silent = True) == 'ABORT': return
         if re.search(r'restrictionMarker',activeAutoscript) and chkRestrictionMarker(card, activeAutoscript, silent = True) == 'ABORT': continue
         targetC = findTarget(activeAutoscript)
         ### Warning the player in case we need to
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         if chkTagged(activeAutoscript) == 'ABORT': return
         if not checkOrigSpecialRestrictions(activeAutoscript,card): continue  
         ### Checking the activation cost and preparing a relevant string for the announcement
         actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", activeAutoscript) 
         # This is the cost of the card.  It starts with A which is the amount of Clicks needed to activate
         # After A follows B for Credit cost, then for aGenda cost.
         # T takes a binary value. A value of 1 means the card needs to be trashed.
         if actionCost: # If there's no match, it means we've already been through the cost part once and now we're going through the '$$' part.
            if actionCost.group(1) != '0': # If we need to use clicks
               Acost = useClick(count = num(actionCost.group(1)))
               if Acost == 'ABORT': return
               else: announceText = Acost
               CardAction = True
            else: announceText = '{}'.format(me) # A variable with the text to be announced at the end of the action.
            if actionCost.group(2) != '0': # If we need to pay credits
               reduction = reduceCost(card, 'USE', num(actionCost.group(2)))
               gatheredCardList = True # We set this to true, so that reduceCost doesn't scan the table for subsequent executions
               if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))  
               elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
               else: extraText = ''
               Bcost = payCost(num(actionCost.group(2)) - reduction)
               if Bcost == 'ABORT': # if they can't pay the cost afterall, we return them their clicks and abort.
                  me.Clicks += num(actionCost.group(1))
                  return
               if actionCost.group(1) != '0':
                  if actionCost.group(3) != '0' or actionCost.group(4) != '0': announceText += ', '
                  else: announceText += ' and '
               else: announceText += ' '
               announceText += 'pays {}{}'.format(uniCredit(num(actionCost.group(2)) - reduction),extraText)
            if actionCost.group(3) != '0': # If we need to pay agenda points...
               Gcost = payCost(actionCost.group(3), counter = 'AP')
               if Gcost == 'ABORT': 
                  me.Clicks += num(actionCost.group(1))
                  me.counters['Credits'].value += num(actionCost.group(2))
                  return
               if actionCost.group(1) != '0' or actionCost.group(2)  != '0':
                  if actionCost.group(4) != '0': announceText += ', '
                  else: announceText += ' and '
               else: announceText += ' '
               announceText += 'liquidates {} Agenda Points'.format(actionCost.group(3))
            if actionCost.group(4) != '0': # If the card needs to be trashed...
               if (actionCost.group(4) == '2' and oncePerTurn(card, silent = True) == 'ABORT') or (actionCost.group(4) == '1' and not confirm("This action will trash the card as a cost. Are you sure you want to continue?")):
                  # On trash cost, we confirm first to avoid double-click accidents
                  me.Clicks += num(actionCost.group(1))
                  me.counters['Credits'].value += num(actionCost.group(2))
                  me.counters['Agenda Points'].value += num(actionCost.group(3))
                  return
               if actionCost.group(1) != '0' or actionCost.group(2) != '0' or actionCost.group(3) != '0': announceText += ' and '
               else: announceText += ' '
               if actionCost.group(4) == '1': announceText += 'trashes {} to use its ability'.format(card)
               else: announceText += 'activates the once-per-turn ability of{} {}'.format(lingering,card)
            else: announceText += ' to activate{} {}'.format(lingering,card) # If we don't have to trash the card, we need to still announce the name of the card we're using.
            if actionCost.group(1) == '0' and actionCost.group(2) == '0' and actionCost.group(3) == '0' and actionCost.group(4) == '0':
               if card.Type == 'ICE': announceText = '{} activates {}'.format(me, card)
               else: announceText = '{} uses the ability of{} {}'.format(me, lingering, card)
            if re.search(r'-isSubroutine', activeAutoscript): announceText = '{} '.format(uniSubroutine()) + announceText # if we are in a subroutine, we use the special icon to make it obvious.
            announceText += ' in order to'
         elif not announceText.endswith(' in order to') and not announceText.endswith(' and'): announceText += ' and'
         debugNotify("Entering useAbility() Choice with Autoscript: {}".format(activeAutoscript), 2) # Debug
         ### Calling the relevant function depending on if we're increasing our own counters, the hoard's or putting card markers.
         if regexHooks['GainX'].search(activeAutoscript): 
            gainTuple = GainX(activeAutoscript, announceText, card, targetC, n = X)
            if gainTuple == 'ABORT': announceText == 'ABORT'
            else:
               announceText = gainTuple[0] 
               X = gainTuple[1] 
         elif regexHooks['CreateDummy'].search(activeAutoscript): announceText = CreateDummy(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['ReshuffleX'].search(activeAutoscript): 
            reshuffleTuple = ReshuffleX(activeAutoscript, announceText, card) # The reshuffleX() function is special because it returns a tuple.
            announceText = reshuffleTuple[0] # The first element of the tuple contains the announceText string
            X = reshuffleTuple[1] # The second element of the tuple contains the number of cards that were reshuffled from the hand in the deck.
         elif regexHooks['RetrieveX'].search(activeAutoscript): 
            retrieveTuple = RetrieveX(activeAutoscript, announceText, card, targetC, n = X)
            if retrieveTuple == 'ABORT': announceText == 'ABORT'
            else:
               announceText = retrieveTuple[0] # The first element of the tuple contains the announceText string
               X = len(retrieveTuple[1]) # The second element of the tuple contains the cards which were retrieved. by countring them we have the X
         elif regexHooks['RollX'].search(activeAutoscript): 
            rollTuple = RollX(activeAutoscript, announceText, card) # Returns like reshuffleX()
            announceText = rollTuple[0] 
            X = rollTuple[1] 
         elif regexHooks['RequestInt'].search(activeAutoscript): 
            numberTuple = RequestInt(activeAutoscript, announceText, card) # Returns like reshuffleX()
            if numberTuple == 'ABORT': announceText == 'ABORT'
            else:
               announceText = numberTuple[0] 
               X = numberTuple[1] 
         elif regexHooks['DiscardX'].search(activeAutoscript): 
            discardTuple = DiscardX(activeAutoscript, announceText, card, targetC, n = X) # Returns like reshuffleX()
            announceText = discardTuple[0] 
            X = discardTuple[1] 
         elif regexHooks['TokensX'].search(activeAutoscript):           announceText = TokensX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['TransferX'].search(activeAutoscript):         announceText = TransferX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['DrawX'].search(activeAutoscript):             announceText = DrawX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['ShuffleX'].search(activeAutoscript):          announceText = ShuffleX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['RunX'].search(activeAutoscript):              announceText = RunX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['TraceX'].search(activeAutoscript):            announceText = TraceX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['InflictX'].search(activeAutoscript):          announceText = InflictX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['ModifyStatus'].search(activeAutoscript):      announceText = ModifyStatus(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['SimplyAnnounce'].search(activeAutoscript):    announceText = SimplyAnnounce(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['ChooseKeyword'].search(activeAutoscript):     announceText = ChooseKeyword(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['UseCustomAbility'].search(activeAutoscript):  announceText = UseCustomAbility(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['PsiX'].search(activeAutoscript):              announceText = PsiX(activeAutoscript, announceText, card, targetC, n = X)
         elif regexHooks['SetVarX'].search(activeAutoscript):           SetVarX(activeAutoscript, announceText, card, targetC, n = X) # Setting a variable does not change the announcement text.
         else: timesNothingDone += 1
         debugNotify("<<< useAbility() choice. TXT = {}".format(announceText), 3) # Debug
         if announceText == 'ABORT': 
            autoscriptCostUndo(card, selectedAutoscripts[0]) # If nothing was done, try to undo. The first item in selectedAutoscripts[] contains the cost.
            gatheredCardList = False
            return
         if failedRequirement: break # If part of an AutoAction could not pay the cost, we stop the rest of it.
      if announceText.endswith(' in order to'): # If our text annouce ends with " to", it means that nothing happened. Try to undo and inform player.
         autoscriptCostUndo(card, selectedAutoscripts[0])
         notify("{} but there was nothing to do.".format(announceText[:-len(' in order to')]))
      elif announceText.endswith(' and'):
         announceText = announceText[:-len(' and')] # If for some reason we end with " and" (say because the last action did nothing), we remove it.
      else: # If we did something and everything finished as expected, then take the costs.
         if re.search(r"T1:", selectedAutoscripts[0]): intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
      if iter == len(AutoscriptsList) - 1: # If this is the last script in the list, then we always announce the script we're running (We reduce by 1 because iterators always start as '0')
         debugNotify("Entering last notification", 2)
         if prev_announceText == 'NULL': # If it's NULL it's the only  script we run in this loop, so we just announce.
            notify("{}.".format(announceText)) # Finally announce what the player just did by using the concatenated string.
         else: # If it's not NULL, then there was a script run last time, so we check to see if it's a duplicate
            if prev_announceText == announceText: # If the previous script had the same notification output as the current one, we merge them.
               multiCount += 1
               if me.Credits != startingCreds: announceText = announceText + " (remaining bank: {})".format(uniCredit(me.Credits)) # If we spent money during this script execution, we want to point out the new player's credit total.
               notify("({}x) {}.".format(multiCount,announceText))
            else: # If the previous script did not have the same output as the current one, we announce them both together.
               if multiCount > 1: notify("({}x) {}.".format(multiCount,prev_announceText)) # If there were multiple versions of the last script used, announce them along with how many there were
               else: notify("{}.".format(prev_announceText))
               if me.Credits != startingCreds: announceText = announceText + " (remaining bank: {})".format(uniCredit(me.Credits)) # If we spent money during this script execution, we want to point out the new player's credit total.
               notify("{}.".format(announceText)) # Finally we announce the current script's concatenated notification.
      else: #if it's not the last script we run, then we just check if we should announce the previous script or just add another replication.
         debugNotify("Entering notification grouping check", 2)
         if prev_announceText == 'NULL': # If it's null, it's the first script we run in this loop...
            multiCount += 1 # ...so we don't announce but rather increase a counter and and just move to the next script, in case it's a duplicate announcement.
            prev_announceText = announceText # We also set the variable we're going to check in the next iteration, to see if it's a duplicate announcement.
         else:
            if prev_announceText == announceText: # If the previous script had the same notification output as the current one...
               multiCount += 1 # ...we merge them and continue without announcing.
            else: # If the previous script did not have the same notification output as the current one, we announce the previous one.
               if me.Credits != startingCreds: prev_announceText = prev_announceText + " (remaining bank: {})".format(uniCredit(me.Credits)) # If we spent money during this script execution, we want to point out the new player's credit total.
               if multiCount > 1: notify("({}x) {}.".format(multiCount,prev_announceText)) # If there were multiple versions of the last script used, announce them along with how many there were
               else: notify("{}.".format(prev_announceText)) 
               multiCount = 1 # We reset the counter so that we start counting how many duplicates of the current script we're going to have in the future.
               prev_announceText = announceText # And finally we reset the variable holding the previous script.
      chkNoisy(card)
      gatheredCardList = False  # We set this variable to False, so that reduceCost() calls from other functions can start scanning the table again.
      if announceText != 'ABORT' and CardAction: autoscriptOtherPlayers('CardAction', card)

#------------------------------------------------------------------------------
# Other Player trigger
#------------------------------------------------------------------------------
   
def autoscriptOtherPlayers(lookup, origin_card = Identity, count = 1): # Function that triggers effects based on the opponent's cards.
# This function is called from other functions in order to go through the table and see if other players have any cards which would be activated by it.
# For example a card that would produce credits whenever a trace was attempted. 
   if not Automations['Triggers']: return
   debugNotify(">>> autoscriptOtherPlayers() with lookup: {}".format(lookup)) #Debug
   debugNotify("origin_card = {}".format(origin_card), 3) #Debug
   if not Automations['Play, Score and Rez']: return # If automations have been disabled, do nothing.
   for card in table:
      debugNotify('Checking {}'.format(card), 2) # Debug
      if not card.isFaceUp: continue # Don't take into accounts cards that are not rezzed.
      if card.highlight == InactiveColor: continue # We don't take into account inactive cards.
      costText = '{} activates {} to'.format(card.controller, card) 
      Autoscripts = CardsAS.get(card.model,'').split('||')
      debugNotify("{}'s AS: {}".format(card,Autoscripts), 4) # Debug
      autoScriptSnapshot = list(Autoscripts)
      for autoS in autoScriptSnapshot: # Checking and removing anything other than whileRezzed or whileScored.
         if not re.search(r'while(Rezzed|Scored|Running|Installed|InPlay)', autoS): 
            debugNotify("Card does not have triggered ability while in play. Aborting", 2) #Debug
            Autoscripts.remove(autoS)
         if not chkRunningStatus(autoS): Autoscripts.remove(autoS) # If the script only works while running a specific server, and we're not, then abort.
      if len(Autoscripts) == 0: continue
      for autoS in Autoscripts:
         debugNotify('Checking autoS: {}'.format(autoS), 2) # Debug
         if not re.search(r'{}'.format(lookup), autoS): 
            debugNotify("lookup: {} not found in CardScript. Aborting".format(lookup))
            continue # Search if in the script of the card, the string that was sent to us exists. The sent string is decided by the function calling us, so for example the ProdX() function knows it only needs to send the 'GeneratedSpice' string.
         if chkPlayer(autoS, card.controller,False) == 0: continue # Check that the effect's origninator is valid.
         if card.Type == 'Identity' and card.Side == 'runner' and chkCerebralStatic(): continue # If Cerebral Static is still active, we abort the scripts.
         if not ifHave(autoS,card.controller,silent = True): continue # If the script requires the playet to have a specific counter value and they don't, do nothing.
         if re.search(r'whileScored',autoS) and card.controller.getGlobalVariable('ds') != 'corp': continue # If the card is only working while scored, then its controller has to be the corp.
         if chkTagged(autoS, True) == 'ABORT': continue
         if not chkRunStatus(autoS): continue
         if not checkCardRestrictions(gatherCardProperties(origin_card), prepareRestrictions(autoS, 'type')): continue #If we have the '-type' modulator in the script, then need ot check what type of property it's looking for
         if not checkSpecialRestrictions(autoS,origin_card): continue #If we fail the special restrictions on the trigger card, we also abort.
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue # If the card's ability is only once per turn, use it or silently abort if it's already been used
         if re.search(r'onTriggerCard',autoS): targetCard = [origin_card] # if we have the "-onTriggerCard" modulator, then the target of the script will be the original card (e.g. see Grimoire)
         elif re.search(r'AutoTargeted',autoS): targetCard = findTarget(autoS)
         else: targetCard = None
         debugNotify("Automatic Autoscripts: {}".format(autoS), 2) # Debug
         #effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{} -]*)', autoS)
         #passedScript = "{}".format(effect.group(0))
         #confirm('effects: {}'.format(passedScript)) #Debug
         if regexHooks['CustomScript'].search(autoS):
            customScriptResult = CustomScript(card,'USE',origin_card, lookup)
            if customScriptResult == 'CLICK USED': autoscriptOtherPlayers('CardAction', card)  # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
            if customScriptResult == 'ABORT': break
         elif regexHooks['GainX'].search(autoS):
            gainTuple = GainX(autoS, costText, card, targetCard, notification = 'Automatic', n = count)
            if gainTuple == 'ABORT': break
         elif regexHooks['TokensX'].search(autoS): 
            if TokensX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['TransferX'].search(autoS): 
            if TransferX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['InflictX'].search(autoS): 
            remoteCall(fetchCorpPL(),'InflictX',[autoS, costText, card, targetCard, 'Automatic', count]) # We always have the corp itself do the damage
            #if InflictX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['DrawX'].search(autoS):
            if DrawX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['ModifyStatus'].search(autoS):
            if ModifyStatus(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['SetVarX'].search(autoS):
            if SetVarX(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['UseCustomAbility'].search(autoS):
            if UseCustomAbility(autoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
   debugNotify("<<< autoscriptOtherPlayers()", 3) # Debug

#------------------------------------------------------------------------------
# Start/End of Turn/Run trigger
#------------------------------------------------------------------------------
   
def atTimedEffects(Time = 'Start', AlternativeRunResultUsed = False): # Function which triggers card effects at the start or end of the turn.
   mute()
   debugNotify(">>> atTimedEffects() at time: {}".format(Time)) #Debug
   global failedRequirement
   failedRequirement = False
   if not Automations['Start/End-of-Turn']: return
   TitleDone = False
   #AlternativeRunResultUsed = False # Used for SuccessfulRun effects which replace the normal effect of running a server. If set to True, then no more effects on that server will be processed (to avoid 2 bank jobs triggering at the same time for example).
   X = 0
   tableCards = sortPriority([card for card in table if card.highlight != InactiveColor and card.highlight != RevealedColor])
   inactiveCards = [card for card in table if card.highlight == InactiveColor or card.highlight == RevealedColor]
   # tableCards.extend(inactiveCards) # Nope, we don't check inactive cards anymore. If they were inactive at the start of the turn, they won't trigger (See http://boardgamegeek.com/article/11686680#11686680)
   for card in tableCards:
      #if card.controller != me: continue # Obsoleted. Using the chkPlayer() function below
      if card.highlight == InactiveColor or card.highlight == RevealedColor: 
         debugNotify("Rejecting {} Because highlight == {}".format(card, card.highlight), 4)
         continue
      if not card.isFaceUp: continue
      if card.Type == 'Identity' and card.Side == 'runner' and chkCerebralStatic(): continue # If Cerebral Static is still active, we abort the scripts.
      Autoscripts = CardsAS.get(card.model,'').split('||')
      for autoS in Autoscripts:
         debugNotify("Processing {} Autoscript: {}".format(card, autoS), 3)
         if Time == 'Run': effect = re.search(r'at(Run)Start:(.*)', autoS) # Putting Run in a group, only to retain the search results groupings later
         elif Time == 'JackOut': effect = re.search(r'at(JackOut):(.*)', autoS) # Same as above
         elif Time == 'SuccessfulRun': effect = re.search(r'at(SuccessfulRun):(.*)', autoS) # Same as above
         elif Time == 'PreStart' or Time == 'PreEnd': effect = re.search(r'atTurn(PreStart|PreEnd):(.*)', autoS)
         else: effect = re.search(r'atTurn(Start|End):(.*)', autoS) #Putting "Start" or "End" in a group to compare with the Time variable later
         if not effect: 
            debugNotify("Not effect Regex found. Aborting")
            continue
         debugNotify("Time maches. Script triggers on: {}".format(effect.group(1)), 3)
         if re.search(r'-ifSuccessfulRun', autoS):
            if Time == 'SuccessfulRun' or (Time == 'JackOut' and getGlobalVariable('SuccessfulRun') == 'True'): #If we're looking only for successful runs, we need the Time to be a successful run or jackout period.
               requiredTarget = re.search(r'-ifSuccessfulRun([A-Za-z&]+)', autoS) # We check what the script requires to be the successful target
               if getGlobalVariable('feintTarget') != 'None': currentRunTarget = getGlobalVariable('feintTarget')
               else: 
                  currentRunTargetRegex = re.search(r'running([A-Za-z&]+)', getGlobalVariable('status')) # We check what the target of the current run was.
                  currentRunTarget = currentRunTargetRegex.group(1)
               if debugVerbosity >= 2: 
                  if requiredTarget and currentRunTargetRegex: notify("!!! Regex requiredTarget: {}\n!!! currentRunTarget: {}".format(requiredTarget.groups(),currentRunTarget))
                  else: notify ("No requiredTarget or currentRunTarget regex match :(")
               if requiredTarget.group(1) == 'Any': pass # -ifSuccessfulRunAny means we run the script on any successful run (e.g. Desperado)
               elif requiredTarget.group(1) == currentRunTarget: pass # If the card requires a successful run on a server that the global variable points that we were running at, we can proceed.
               else: continue # If none of the above, it means the card script is not triggering for this server.
               debugNotify("All checked OK", 3)
            else: continue
         if re.search(r'-ifUnsuccessfulRun', autoS):
            if Time == 'JackOut' and getGlobalVariable('SuccessfulRun') == 'False': #If we're looking only for unsuccessful runs, we need the Time to be a jackout without a successful run shared var..
               requiredTarget = re.search(r'-ifUnsuccessfulRun([A-Za-z&]+)', autoS) # We check what the script requires to be the unsuccessful target
               if getGlobalVariable('feintTarget') != 'None': currentRunTarget = getGlobalVariable('feintTarget')
               else: 
                  currentRunTargetRegex = re.search(r'running([A-Za-z&]+)', getGlobalVariable('status')) # We check what the target of the current run was.
                  currentRunTarget = currentRunTargetRegex.group(1)
               if debugVerbosity >= 2: 
                  if requiredTarget and currentRunTargetRegex: notify("!!! Regex requiredTarget: {}\n!!! currentRunTarget: {}".format(requiredTarget.groups(),currentRunTarget))
                  else: notify ("No requiredTarget or currentRunTarget regex match :(")
               if requiredTarget.group(1) == 'Any': pass # -ifSuccessfulRunAny means we run the script on any successful run (e.g. Desperado)
               elif requiredTarget.group(1) == currentRunTarget: pass # If the card requires a successful run on a server that the global variable points that we were running at, we can proceed.
               else: continue # If none of the above, it means the card script is not triggering for this server.
               debugNotify("All checked OK", 3)
            else: continue
         if chkPlayer(effect.group(2), card.controller,False) == 0: continue # Check that the effect's origninator is valid. 
         if not ifHave(autoS,card.controller,silent = True): continue # If the script requires the playet to have a specific counter value and they don't, do nothing.
         if not checkOrigSpecialRestrictions(autoS,card): continue
         if not chkRunStatus(autoS): continue
         if chkTagged(autoS, True) == 'ABORT': continue
         if effect.group(1) != Time: continue # If the effect trigger we're checking (e.g. start-of-run) does not match the period trigger we're in (e.g. end-of-turn)
         debugNotify("split Autoscript: {}".format(autoS), 3)
         if debugVerbosity >= 2 and effect: notify("!!! effects: {}".format(effect.groups()))
         if re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: continue
         if re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: continue
         if re.search(r'isAlternativeRunResult', effect.group(2)) and AlternativeRunResultUsed: continue # If we're already used an alternative run result and this card has one as well, ignore it
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'dryRun') == 'ABORT': continue
         if re.search(r'restrictionMarker',autoS) and chkRestrictionMarker(card, autoS, silent = True, act = 'dryRun') == 'ABORT': continue
         if re.search(r'isOptional', effect.group(2)) and not (Time == 'SuccessfulRun' and getGlobalVariable('SuccessfulRun') != 'True'):
            extraCountersTXT = '' 
            for cmarker in card.markers: # If the card has any markers, we mention them do that the player can better decide which one they wanted to use (e.g. multiple bank jobs)
               extraCountersTXT += " {}x {}\n".format(card.markers[cmarker],cmarker[0])
            if extraCountersTXT != '': extraCountersTXT = "\n\nThis card has the following counters on it\n" + extraCountersTXT
            if not confirm("{} can have its optional ability take effect at this point. Do you want to activate it?{}".format(fetchProperty(card, 'name'),extraCountersTXT)): continue         
         if re.search(r'isAlternativeRunResult', effect.group(2)) and not (Time == 'SuccessfulRun' and getGlobalVariable('SuccessfulRun') != 'True'): AlternativeRunResultUsed = True # If the card has an alternative result to the normal access for a run, mark that we've used it.         
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue
         if re.search(r'restrictionMarker',autoS) and chkRestrictionMarker(card, autoS, silent = True, act = 'automatic') == 'ABORT': continue
         splitAutoscripts = effect.group(2).split('$$')
         for passedScript in splitAutoscripts:
            if Time == 'SuccessfulRun' and getGlobalVariable('SuccessfulRun') != 'True': continue # Required for Crisium Grid
            targetC = findTarget(passedScript)
            if re.search(r'Targeted', passedScript) and len(targetC) == 0: 
               debugNotify("Needed target but have non. Aborting")
               continue # If our script requires a target and we can't find any, do nothing.
            if not TitleDone: 
               debugNotify("Preparing Title")
               title = None
               if Time == 'Run': title = "{}'s Start-of-Run Effects".format(me)
               elif Time == 'JackOut': title = "{}'s Jack-Out Effects".format(me)
               elif Time == 'SuccessfulRun': title = "{}'s Successful Run Effects".format(me)
               elif Time != 'PreStart' and Time != 'PreEnd': title = "{}'s {}-of-Turn Effects".format(me,effect.group(1))
               if title: notify("{:=^36}".format(title))
            TitleDone = True
            debugNotify("passedScript: {}".format(passedScript), 2)
            if card.highlight == DummyColor: announceText = "{}'s lingering effects:".format(card)
            else: announceText = "{} triggers to".format(card)
            if regexHooks['GainX'].search(passedScript):
               gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if gainTuple == 'ABORT': break
               X = gainTuple[1] 
            elif regexHooks['TransferX'].search(passedScript):
               if TransferX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['DrawX'].search(passedScript):
               if DrawX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['RollX'].search(passedScript):
               rollTuple = RollX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if rollTuple == 'ABORT': break
               X = rollTuple[1] 
            elif regexHooks['TokensX'].search(passedScript):
               if TokensX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['InflictX'].search(passedScript):
               if InflictX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['RetrieveX'].search(passedScript):
               retrieveTuple = RetrieveX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if retrieveTuple == 'ABORT': return
               X = len(retrieveTuple[1])
            elif regexHooks['ModifyStatus'].search(passedScript):
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['DiscardX'].search(passedScript): 
               discardTuple = DiscardX(passedScript, announceText, card, targetC, notification = 'Automatic', n = X)
               if discardTuple == 'ABORT': break
               X = discardTuple[1] 
            elif regexHooks['RequestInt'].search(passedScript): 
               numberTuple = RequestInt(passedScript, announceText, card) # Returns like reshuffleX()
               if numberTuple == 'ABORT': break
               X = numberTuple[1] 
            elif regexHooks['SimplyAnnounce'].search(passedScript):
               SimplyAnnounce(passedScript, announceText, card, notification = 'Automatic', n = X)
            elif regexHooks['SetVarX'].search(passedScript):
               SetVarX(passedScript, announceText, card, notification = 'Automatic', n = X)
            elif regexHooks['CustomScript'].search(passedScript): 
               customScriptResult = CustomScript(card, Time, original_action = Time)
               if customScriptResult == 'CLICK USED': autoscriptOtherPlayers('CardAction', card)   # Some cards (I.e. Collective) just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
               if customScriptResult == 'ABORT': break
               if customScriptResult == 'ALTERNATIVE RUN': AlternativeRunResultUsed = True # Custom scripts might introduce alt-run results which need to stop normal access.
            if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
   markerEffects(Time) 
   ASVarEffects(Time) 
   CustomEffects(Time)
   if me.counters['Credits'].value < 0: 
      if Time == 'Run': notify(":::Warning::: {}'s Start-of-run effects cost more Credits than {} had in their Credit Pool!".format(me,me))
      elif Time == 'JackOut': notify(":::Warning::: {}'s Jacking-Out effects cost more Credits than {} had in their Credit Pool!".format(me,me))
      elif Time == 'SuccessfulRun': notify(":::Warning::: {}'s Successful Run effects cost more Credits than {} had in their Credit Pool!".format(me,me))
      else: notify(":::Warning::: {}'s {}-of-turn effects cost more Credits than {} had in their Credit Pool!".format(me,Time,me))
   if ds == 'corp' and Time =='Start': draw(me.piles['R&D/Stack'])
   if Time == 'SuccessfulRun' and not AlternativeRunResultUsed: # If we have a successful Run and no alternative effect was used, we ask the user if they want to automatically use one of the standard ones.
      if getGlobalVariable('feintTarget') != 'None': currentRunTarget = getGlobalVariable('feintTarget')
      else: 
         currentRunTargetRegex = re.search(r'running([A-Za-z&]+)', getGlobalVariable('status')) # We check what the target of the current run was.
         currentRunTarget = currentRunTargetRegex.group(1)
      if currentRunTarget == 'HQ' and confirm("Rerouting to auth.level 9 corporate grid...OK\
                                             \nAuthenticating secure credentials...OK\
                                             \nDecrypting Home Folder...OK\
                                           \n\nAccess to HQ Granted!\
                                             \nWelcome back Err:::[Segmentation Fault]. Would you like to see today's priority item? \
                                           \n\n============================\
                                             \nAccess HQ? Y/n:"):
         HQaccess(silent = True)
      if currentRunTarget == 'R&D' and confirm("Processing Security Token...OK.\
                                              \nAccess to R&D files authorized for user {}.\
                                            \n\n============================\
                                              \nProceed to R&D files? Y/n:".format(me.name)):
         RDaccessX()
      if currentRunTarget == 'Archives' and confirm("Authorization for user {} processed.\
                                                   \nDecrypting Archive Store...OK.\
                                                 \n\n============================\
                                                   \nRetrieve Archives? Y/n:".format(me.name)):
         ARCscore()
   if TitleDone: notify(":::{:=^30}:::".format('='))   
   debugNotify("<<< atTimedEffects()", 3) # Debug

#------------------------------------------------------------------------------
# Post-Trace/Psi Trigger
#------------------------------------------------------------------------------

def executePostEffects(card,Autoscript,count = 0,type = 'Trace'):
   debugNotify(">>> executePostEffects(){}".format(extraASDebug(Autoscript))) #Debug
   global failedRequirement
   failedRequirement = False
   X = count # The X Starts as the "count" passed variable, which in traces is the difference between the corp's trace and the runner's link
   Autoscripts = Autoscript.split('||')
   for autoS in Autoscripts:
      selectedAutoscripts = autoS.split('++')
      if debugVerbosity >= 2: notify ('selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for passedScript in selectedAutoscripts: X = redirect(passedScript, card, "{}'s {} succeeds to".format(card,type), 'Quick', X)
      if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
         
#------------------------------------------------------------------------------
# Remote player script execution
#------------------------------------------------------------------------------
      
def remoteAutoscript(card = None, Autoscript = ''):
   debugNotify('>>> remoteAutoscript')
   debugNotify("Autoscript sent: {}".format(Autoscript))
   mute()
   if card: storeProperties(card, True)
   if re.search(r'-isOptional', Autoscript):
      if not confirm("The runner has accessed {} and you can choose to activate it at this point. Do you want to do so?".format(fetchProperty(card, 'name'))):
         notify("{} opts not to activate {}'s optional ability".format(me,card))
         return 'ABORT'
      else: notify("{} activates {}'s ability".format(me,card))
   selectedAutoscripts = Autoscript.split('$$')
   debugNotify ('selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
   X = 0
   for passedScript in selectedAutoscripts: 
      X = redirect(passedScript, card, "{} triggers to".format(card), 'Quick', X)
      if X == 'ABORT': return
   debugNotify('<<< remoteAutoscript')

#------------------------------------------------------------------------------
# Core Commands redirect
#------------------------------------------------------------------------------
      
def redirect(Autoscript, card, announceText = None, notificationType = 'Quick', X = 0):
   debugNotify(">>> redirect(){}".format(extraASDebug(Autoscript))) #Debug
   if re.search(r':Pass\b', Autoscript): return X # Pass is a simple command of doing nothing ^_^
   targetC = findTarget(Autoscript)
   debugNotify("card.owner = {}".format(card.owner),2)
   targetPL = ofwhom(Autoscript,card.owner) # So that we know to announce the right person the effect, affects.
   if not announceText: announceText = "{} uses {}'s ability to".format(targetPL,card) 
   debugNotify(" targetC: {}. Notification Type = {}".format(targetC,notificationType), 3) # Debug
   if regexHooks['GainX'].search(Autoscript):
      gainTuple = GainX(Autoscript, announceText, card, notification = notificationType, n = X)
      if gainTuple == 'ABORT': return 'ABORT'
      X = gainTuple[1] 
   elif regexHooks['CreateDummy'].search(Autoscript): 
      if CreateDummy(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['DrawX'].search(Autoscript): 
      if DrawX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['TokensX'].search(Autoscript): 
      if TokensX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['RollX'].search(Autoscript): 
      rollTuple = RollX(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
      if rollTuple == 'ABORT': return 'ABORT'
      X = rollTuple[1] 
   elif regexHooks['RequestInt'].search(Autoscript): 
      numberTuple = RequestInt(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
      if numberTuple == 'ABORT': return 'ABORT'
      X = numberTuple[1] 
   elif regexHooks['DiscardX'].search(Autoscript): 
      discardTuple = DiscardX(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
      if discardTuple == 'ABORT': return 'ABORT'
      X = discardTuple[1] 
   elif regexHooks['RunX'].search(Autoscript): 
      if RunX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['TraceX'].search(Autoscript): 
      if TraceX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['ReshuffleX'].search(Autoscript): 
      reshuffleTuple = ReshuffleX(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
      if reshuffleTuple == 'ABORT': return 'ABORT'
      X = reshuffleTuple[1]
   elif regexHooks['ShuffleX'].search(Autoscript): 
      if ShuffleX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['ChooseKeyword'].search(Autoscript): 
      if ChooseKeyword(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['InflictX'].search(Autoscript): 
      if InflictX(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['ModifyStatus'].search(Autoscript): 
      if ModifyStatus(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   elif regexHooks['SimplyAnnounce'].search(Autoscript):
      SimplyAnnounce(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
   elif regexHooks['SetVarX'].search(Autoscript):
      SetVarX(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
   elif regexHooks['PsiX'].search(Autoscript):
      PsiX(Autoscript, announceText, card, targetC, notification = notificationType, n = X)
   elif regexHooks['UseCustomAbility'].search(Autoscript):
      if UseCustomAbility(Autoscript, announceText, card, targetC, notification = notificationType, n = X) == 'ABORT': return 'ABORT'
   else: debugNotify(" No regexhook match! :(") # Debug
   debugNotify("Loop for scipt {} finished".format(Autoscript), 2)
   debugNotify("<<< redirect with X = {}".format(X))
   return X

#------------------------------------------------------------------------------
# Core Commands
#------------------------------------------------------------------------------
   
def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0, actionType = 'USE'): # Core Command for modifying counters or global variables
   debugNotify(">>> GainX(){}".format(extraASDebug(Autoscript))) #Debug
   debugNotify("notification = {}".format(notification), 3)
   if targetCards is None: targetCards = []
   global lastKnownNrClicks
   gain = 0
   extraText = ''
   reduction = 0
   exactFail = False # A Variable that changes the notification if the cost needs to be paid exact, but the target player does not have enough counters.
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   debugNotify("action groups: {}. Autoscript: {}".format(action.groups(0),Autoscript), 2) # Debug
   actiontypeRegex = re.search(r'actiontype([A-Z]+)',Autoscript) # This is used by some scripts so that they do not use the triggered action as the type of action that triggers the effect. For example, Draco's ability is not a "Rez" action and thus its cost is not affected by card that affect ICE rez costs, like Project Braintrust
   if actiontypeRegex: actionType = actiontypeRegex.group(1)
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript, card.owner)
   if targetPL != me: 
      otherTXT = ' force {} to'.format(targetPL)
      if action.group(1) == 'Lose': actionType = 'Force'
   else: otherTXT = ''
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0:
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   debugNotify("GainX() after per", 3) #Debug
   if action.group(1) == 'Lose': 
      if action.group(3) == 'Credits' or action.group(3) == 'Agenda Points' or action.group(3) == 'Clicks' or action.group(3) == 'MU' or action.group(3) == 'Base Link' or action.group(3) == 'Bad Publicity' or action.group(3) == 'Tags' or action.group(3) == 'Hand Size':
         overcharge = (gain * multiplier) - targetPL.counters[action.group(3)].value  # we use this to calculate how much of the requested LoseX was used.
         debugNotify(" We have an overcharge of {}".format(overcharge), 4)
         if overcharge < 0: overcharge = 0 # But if the overcharge is 0 or less, it means that all the loss could be taken out.
      else: overcharge = 0
      gain *= -1
      debugNotify(" overcharge = {}\n#### Gain = {}.\n #### Multiplier = {}.".format(overcharge,gain,multiplier), 2)
   if re.search(r'ifNoisyOpponent', Autoscript) and targetPL.getGlobalVariable('wasNoisy') != '1': return announceText # If our effect only takes place when our opponent has been noisy, and they haven't been, don't do anything. We return the announcement so that we don't crash the parent function expecting it
   gainReduce = findCounterPrevention(gain * multiplier, action.group(3), targetPL) # If we're going to gain counter, then we check to see if we have any markers which might reduce the cost.
   #confirm("multiplier: {}, gain: {}, reduction: {}".format(multiplier, gain, gainReduce)) # Debug
   if re.match(r'Credits', action.group(3)): # Note to self: I can probably comprress the following, by using variables and by putting the counter object into a variable as well.
      if action.group(1) == 'SetTo': targetPL.counters['Credits'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Credits'].value = 0
      else: 
         debugNotify(" Checking Cost Reduction", 2)
         reversePlayer = actionType == 'Force' # If the loss is forced on another player, we reverse the recude cost player checking effects, to check for their reduction effects and not ours
         if re.search(r'isCost', Autoscript) and action.group(1) == 'Lose':
            reduction = reduceCost(card, actionType, gain * multiplier, reversePlayer = reversePlayer)
         elif action.group(1) == 'Lose':
            if targetPL == me: actionType = 'None' # If we're losing money from a card effect that's not a cost, we considered a 'use' cost.
            reduction = reduceCost(card, actionType, gain * multiplier, reversePlayer = reversePlayer) # If the loss is not a cost, we still check for generic reductions such as BP
         if action.group(1) == 'Lose' and re.search(r'isExact', Autoscript) and targetPL.counters['Credits'].value < abs((gain * multiplier) + reduction): 
            exactFail = True
         else: 
            targetPL.counters['Credits'].value += (gain * multiplier) + reduction
            if reduction > 0: extraText = ' (Reduced by {})'.format(uniCredit(reduction))
            elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      if targetPL.counters['Credits'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Credits'].value = 0
   elif re.match(r'Agenda Points', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Agenda Points'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Agenda Points'].value = 0
      else: targetPL.counters['Agenda Points'].value += (gain * multiplier) - gainReduce
      if me.counters['Agenda Points'].value >= 7 or (getSpecial('Identity',fetchCorpPL()).name == "Harmony Medtech" and me.counters['Agenda Points'].value >= 6): 
         notify("{} wins the game!".format(me))
         reportGame()      
      if targetPL.counters['Agenda Points'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         #Agenda Points can go negative
   elif re.match(r'Clicks', action.group(3)): 
      if action.group(1) == 'SetTo': 
         targetPL.Clicks = 0 # If we're setting to a specific value, we wipe what it's currently.
         lastKnownNrClicks = 0
      if gain == -999: 
         targetPL.Clicks = 0
         lastKnownNrClicks = 0
      else: 
         if action.group(1) == 'Lose' and re.search(r'isExact', Autoscript) and targetPL.Clicks < abs((gain * multiplier) - gainReduce): 
            exactFail = True
         else:
            debugNotify("Proceeding to gain/lose clicks. Had {} Clicks. Modification is {}".format(targetPL.Clicks,(gain * multiplier) - gainReduce), 2)
            targetPL.Clicks += (gain * multiplier) - gainReduce
            lastKnownNrClicks += (gain * multiplier) - gainReduce # We also increase the offset, to make sure we announce the correct current action.
   elif re.match(r'MU', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.MU = 0 # If we're setting to a specific value, we wipe what it's currently.
      else: targetPL.MU += (gain * multiplier) - gainReduce
      if targetPL.MU < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.MU = 0
   elif re.match(r'Base Link', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Base Link'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      else: targetPL.counters['Base Link'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Base Link'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Base Link'].value = 0
      chkCloud() # After we modify player link, we check for enabled cloud connections.
   elif re.match(r'Bad Publicity', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Bad Publicity'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bad Publicity'].value = 0
      else: 
         if action.group(1) == 'Lose' and re.search(r'isExact', Autoscript) and targetPL.counters['Bad Publicity'].value < abs((gain * multiplier)) - gainReduce: 
            exactFail = True
         else:
            targetPL.counters['Bad Publicity'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Bad Publicity'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bad Publicity'].value = 0
   elif re.match(r'Tags', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Tags = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Tags = 0
      else: 
         if action.group(1) == 'Lose' and re.search(r'isExact', Autoscript) and targetPL.Tags < abs((gain * multiplier) - gainReduce): 
            exactFail = True
         else:
            targetPL.Tags += (gain * multiplier) - gainReduce
      if targetPL.Tags < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.Tags = 0
   elif re.match(r'Max Click', action.group(3)): 
      if action.group(1) == 'SetTo': modType = 'set to' 
      else: modType = 'increment' 
      modClicks(targetPL = targetPL, count = gain * multiplier, action = modType)
   elif re.match(r'Hand Size', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Hand Size'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      targetPL.counters['Hand Size'].value += gain * multiplier
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   debugNotify("Gainx() Finished counter manipulation", 2)
   if notification != 'Automatic': # Since the verb is in the middle of the sentence, we want it lowercase.
      if action.group(1) == 'Gain': 
         verb = 'gain'
      elif action.group(1) == 'Lose': 
         if re.search(r'isCost', Autoscript): verb = 'pay'
         else: verb = 'lose'
      else: 
         verb = 'set to'
   else: 
      verb = action.group(1) # Automatic notifications start with the verb, so it needs to be capitaliszed. 
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   elif action.group(1) == 'Lose' and re.search(r'isCost', Autoscript): total = abs(gain * multiplier)
   elif action.group(1) == 'Lose' and not re.search(r'isPenalty', Autoscript): total = abs(gain * multiplier) - overcharge - reduction
   else: total = abs(gain * multiplier) - reduction# Else it's just the absolute value which we announce they "gain" or "lose"
   closureTXT = ASclosureTXT(action.group(3), total)
   if re.match(r'Credits', action.group(3)): 
      finalCounter = ' (new total: {})'.format(uniCredit(targetPL.Credits))
   else: 
      finalCounter = ''
   debugNotify("Gainx() about to announce", 2)
   if notification == 'Quick': 
      if exactFail: announceString = ":::WARNING::: {}'s ability failed to work because {} didn't have exactly {} {} to lose".format(card, targetPL, action.group(2), action.group(3))
      else: announceString = "{}{} {} {}{}{}".format(announceText, otherTXT, verb, closureTXT,extraText,finalCounter)
   else: 
      if exactFail: 
         announceString = announceText
         notify(":::WARNING::: {}'s ability failed to work because {} didn't have exactly {} {} to lose".format(card, targetPL, action.group(2), action.group(3)))
      else: announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraText)
   debugNotify("notification = {}".format(notification), 4)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   debugNotify("<<< Gain() total: {}".format(total), 3)
   return (announceString,total)
   
def TransferX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for converting tokens to counter values
   debugNotify(">>> TransferX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   #breakadd = 1
   total = 0
   totalReduce = 0
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   action = re.search(r'\bTransfer([0-9]+)([A-Za-z ]+)-?', Autoscript)
   if re.search(r'Credit',action.group(2)): destGroup = me.counters['Credits']
   elif re.search(r'Click',action.group(2)): destGroup = me.counters['Clicks']
   else:
      whisper(":::WARNING::: Not a valid transfer. Aborting!")
      return 'ABORT'
   debugNotify("!!! regex groups: {}".format(action.groups()), 3) #Debug   
   multiplier = per(Autoscript, card, n, targetCards, notification)   
   count = num(action.group(1)) * multiplier
   for targetCard in targetCards:
      foundMarker = findMarker(targetCard, action.group(2))
      if not foundMarker: 
         whisper("There was nothing to transfer from {}.".format(targetCard))
         continue
      if action.group(1) == '999':
         if targetCard.markers[foundMarker]: count = targetCard.markers[foundMarker]
         else: count = 0
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
   closureTXT = ASclosureTXT(action.group(2), total)
   if notification == 'Quick': announceString = "{} takes {}{}".format(announceText, closureTXT, reduceTXT)
   elif notification == 'Automatic': announceString = "{} Transfer {} to {}{}".format(announceText, closureTXT, me, reduceTXT)
   else: announceString = "{} take {} from {}{}".format(announceText, closureTXT, targetCardlist,reduceTXT)
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< TransferX()", 3)
   return announceString   

def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for adding tokens to cards
   debugNotify(">>> TokensX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   #confirm("TokensX List: {}".format(targetCardlist)) # Debug
   foundKey = False # We use this to see if the marker used in the AutoAction is already defined.
   action = re.search(r'\b(Put|Remove|Refill|Use|Infect)([0-9]+)([A-Za-z: ]+)-?', Autoscript)
   #confirm("{}".format(action.group(3))) # Debug
   if action.group(3) in mdict: token = mdict[action.group(3)]
   else: # If the marker we're looking for it not defined, then either create a new one with a random color, or look for a token with the custom name we used above.
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
   debugNotify("Token = {}".format(token))
   count = num(action.group(2))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   modtokens = count * multiplier
   if re.search(r'isCost', Autoscript): # If we remove tokens as a cost, then we do a dry run to see if we have enough tokens on the targeted cards available
                                        # This way we can stop the execution without actually removing any tokens
      dryRunAmount = 0 # We reset for the next loop
      for targetCard in targetCards: # First we do a dry-run for removing tokens.
         if targetCard.markers[token]: dryRunAmount += targetCard.markers[token]
         debugNotify("Added {} tokens to the pool ({}) from {} at pos {}".format(targetCard.markers[token],dryRunAmount,targetCard,targetCard.position))
      if dryRunAmount < modtokens and not (num(action.group(2)) == 999 and dryRunAmount > 0):
         debugNotify("Found {} tokens. Required {}. Aborting".format(dryRunAmount,modtokens))
         if notification != 'Automatic': delayed_whisper ("Not enough counters to remove. Aborting!") #Some end of turn effect put a special counter and then remove it so that they only run for one turn. This avoids us announcing that it doesn't have markers every turn.
         return 'ABORT'
   tokenAmount = 0  # We count the amount of token we've manipulated, to be used with the -isExactAmount modulator.
   modifiedCards = [] # A list which holds the cards whose tokens we modified ,so that we can announce only the right names.
   for targetCard in targetCards:
      for iter in range(modtokens): # We're removng the tokens 1 by 1, so we can stop once we reached an exact amount that we want.
         if (re.search(r'isExactAmount', Autoscript) or re.search(r'isCost', Autoscript)) and tokenAmount == modtokens: 
            debugNotify("Aborting loop because tokenAmount reached ({})".format(tokenAmount))
            break 
         # If we're modifying the tokens by an exact amount (cost is always this way), then we will stop manipulating tokens on all cards as soon as this amount it reached.
         # If we've accumulated the amount of tokens we need to manipulate, we stop removing any more.
         if action.group(1) == 'Remove':
            if not targetCard.markers[token]:
               #if not re.search(r'isSilent', Autoscript): delayed_whisper("There was nothing to remove.") 
               break
            else: 
               targetCard.markers[token] -= 1 
               if token[0] == "Credit": # If the tokens we removed were credits, we check if the card is supposed to be trashed when it runs out.
                  Autoscripts = fetchProperty(targetCard, 'AutoScripts').split('||')
                  for autoS in Autoscripts:
                     if re.search(r'Reduce(.+?)Cost',autoS) and re.search(r'trashCost-ifEmpty', autoS) and not targetCard.markers[mdict["Credit"]]: 
                        intTrashCard(targetCard, targetCard.Stat, cost = "free", silent = True)
                        notify("-- {} {} {} because it was empty".format(me,uniTrash(),targetCard))
         else:
            if action.group(1) == 'Refill' and targetCard.markers[token] and targetCard.markers[token] >= modtokens: break # If we're refilling the tokens and we've already exceeded that amount, we don't add more
            targetCard.markers[token] += 1
         tokenAmount += 1
         if targetCard not in modifiedCards: modifiedCards.append(targetCard)
   debugNotify("tokenAmount = {}".format(tokenAmount))
   if len(modifiedCards) == 1 and modifiedCards[0] == card: targetCardlist = ' on it'
   else: 
      targetCardlist = ' on' # A text field holding which cards are going to get tokens.
      for targetCard in modifiedCards:
         targetCardlist += ' {},'.format(targetCard)
   if num(action.group(2)) == 999: total = 'all'
   else: total = modtokens
   if re.search(r'isPriority', Autoscript): card.highlight = PriorityColor
   if action.group(1) == 'Refill': 
      if token[0] == 'Credit': 
         announceString = "{} {} to {}".format(announceText, action.group(1), uniRecurring(count * multiplier)) # We need a special announcement for refill, since it always needs to point out the max.
      else: 
         announceString = "{} {} to {} {}".format(announceText, action.group(1), count * multiplier, token[0]) # We need a special announcement for refill, since it always needs to point out the max.
   elif re.search(r'forfeitCounter:',action.group(3)):
      counter = re.search(r'forfeitCounter:(\w+)',action.group(3))
      if not victim or victim == me: announceString = '{} forfeit their next {} {}'.format(announceText,total,counter.group(1)) # If we're putting on forfeit counters, we don't announce it as an infection.
      else: announceString = '{} force {} to forfeit their next {} {}'.format(announceText, victim, total,counter.group(1))
   else: announceString = "{} {} {} {} counters{}".format(announceText, action.group(1).lower(), total, token[0],targetCardlist)
   if notification and modtokens != 0 and not re.search(r'isSilent', Autoscript): notify('--> {}.'.format(announceString))
   debugNotify("TokensX() String: {}".format(announceString), 2) #Debug
   debugNotify("<<< TokensX()", 3)
   if re.search(r'isSilent', Autoscript): return announceText # If it's a silent marker, we don't want to announce anything. Returning the original announceText will be processed by any receiving function as having done nothing.
   else: return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> DrawX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   destiVerb = 'draw'
   action = re.search(r'\bDraw([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.owner)
   if targetPL != me: destiVerb = 'move'
   if re.search(r'-fromTrash', Autoscript): source = targetPL.piles['Heap/Archives(Face-up)']
   else: source = targetPL.piles['R&D/Stack']
   if re.search(r'-toStack', Autoscript): 
      destination = targetPL.piles['R&D/Stack']
      destiVerb = 'move'
   elif re.search(r'-toTrash', Autoscript):
      if targetPL.getGlobalVariable('ds') == 'corp': destination = targetPL.piles['Archives(Hidden)']
      else: destination = targetPL.piles['Heap/Archives(Face-up)']
      destiVerb = 'trash'   
   else: destination = targetPL.hand
   if destiVerb == 'draw' and ModifyDraw > 0 and not confirm("You have a card effect in play that modifies the amount of cards you draw. Do you want to continue as normal anyway?\n\n(Answering 'No' will abort this action so that you can prepare for the special changes that happen to your draw."): return 'ABORT'
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
   debugNotify("About to announce.", 2)
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} draws {} cards".format(announceText, count)
   elif targetPL == me: announceString = "{} {} {} cards from their {}{}".format(announceText, destiVerb, count, pileName(source), destPath)
   else: announceString = "{} {} {} cards from {}'s {}".format(announceText, destiVerb, count, targetPL, pileName(source), destPath)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   debugNotify("<<< DrawX()", 3)
   return announceString

def DiscardX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> DiscardX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bDiscard([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.owner)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   discardNR = num(action.group(1))
   if discardNR == 999:
      multiplier = 1
      discardNR = len(targetPL.hand) # 999 means we discard our whole hand
   if re.search(r'-isRandom',Autoscript): # Any other number just discard as many cards at random.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = handRandomDiscard(targetPL.hand, discardNR * multiplier, targetPL, silent = True)
      if re.search(r'isCost', Autoscript) and count < discardNR:
         whisper("You do not have enough cards in your hand to discard")
         return ('ABORT',0)
   else: # Otherwise we just discard the targeted cards from hand  
      multiplier = 1
      count = len(targetCards)
      if re.search(r'isCost', Autoscript) and count < discardNR:
         whisper("You do not have enough cards in your hand to discard")
         return ('ABORT',0)
      for targetC in targetCards: handDiscard(targetC, True)
      debugNotify("Finished discarding targeted cards from hand")
   if count == 0: 
      debugNotify("Exiting because count == 0")
      return (announceText,count) # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} discards {} cards ({})".format(announceText, count, [c.name for c in targetCards])
   else: announceString = "{}{} discard {} cards ({}) from their hand".format(announceText,otherTXT, count,[c.name for c in targetCards])
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   debugNotify("<<< DiscardX()", 3)
   return (announceString,count)
         
def ReshuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack and replenishing the pile with the same number of cards.
   debugNotify(">>> ReshuffleX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   mute()
   X = 0
   targetPL = ofwhom(Autoscript, card.owner)
   action = re.search(r'\bReshuffle([A-Za-z& ]+)', Autoscript)
   debugNotify("!!! regex: {}".format(action.groups())) # Debug
   if action.group(1) == 'HQ' or action.group(1) == 'Stack':
      namestuple = groupToDeck(targetPL.hand, targetPL , True) # We do a silent hand reshuffle into the deck, which returns a tuple
      X = namestuple[2] # The 3rd part of the tuple is how many cards were in our hand before it got shuffled.
   elif action.group(1) == 'Archives' or action.group(1) == 'Heap':
      if targetPL.getGlobalVariable('ds') == "corp": groupToDeck(targetPL.piles['Archives(Hidden)'], targetPL , True)
      namestuple = groupToDeck(targetPL.piles['Heap/Archives(Face-up)'], targetPL, True)    
   else: 
      whisper("Wat Group? [Error in autoscript!]")
      return 'ABORT'
   shuffle(targetPL.piles['R&D/Stack'])
   if notification == 'Quick': announceString = "{} shuffles their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   else: announceString = "{} shuffle their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< ReshuffleX() return with X = {}".format(X), 3)
   return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for shuffling a pile into the R&D/Stack
   debugNotify(">>> ShuffleX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   mute()
   action = re.search(r'\bShuffle([A-Za-z& ]+)', Autoscript)
   targetPL = ofwhom(Autoscript, card.owner)
   if action.group(1) == 'Trash' or action.group(1) == 'Archives': pile = targetPL.piles['Heap/Archives(Face-up)']
   elif action.group(1) == 'Stack' or action.group(1) == 'R&D': pile = targetPL.piles['R&D/Stack']
   elif action.group(1) == 'Hidden Archives': pile = targetPL.piles['Archives(Hidden)']
   random = rnd(10,100) # Small wait (bug workaround) to make sure all animations are done.
   shuffle(pile)
   if notification == 'Quick': announceString = "{} shuffles their {}".format(announceText, pileName(pile))
   elif targetPL == me: announceString = "{} shuffle their {}".format(announceText, pileName(pile))
   else: announceString = "{} shuffle {}' {}".format(announceText, targetPL, pileName(pile))
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< ShuffleX()", 3)
   return announceString
   
def RollX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for rolling a Die
   debugNotify(">>> RollX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   d6 = 0
   d6list = []
   result = 0
   action = re.search(r'\bRoll([0-9]+)Dice(-chk)?([1-6])?', Autoscript)
   multiplier = per(Autoscript, card, n, targetCards, notification)
   count = num(action.group(1)) * multiplier 
   for d in range(count):
      if d == 2: whisper("-- Please wait. Rolling {} dice...".format(count))
      if d == 8: whisper("-- A little while longer...")
      d6 = rolld6(silent = True)
      d6list.append(d6)
      if action.group(3): # If we have a chk modulator, it means we only increase our total if we hit a specific number.
         if num(action.group(3)) == d6: result += 1
      else: result += d6 # Otherwise we add all totals together.
      debugNotify("iter:{} with roll {} and total result: {}".format(d,d6,result), 2)
   if notification == 'Quick': announceString = "{} rolls {} on {} dice".format(announceText, d6list, count)
   else: announceString = "{} roll {} dice with the following results: {}".format(announceText,count, d6list)
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< RollX() with result: {}".format(result), 3)
   return (announceString, result)

def RequestInt(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> RequestInt(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRequestInt(-Min)?([0-9]*)(-div)?([0-9]*)(-Max)?([0-9]*)(-Msg)?\{?([A-Za-z0-9?$&\(\) ]*)\}?', Autoscript)
   if debugVerbosity >= 2:
      if action: notify('!!! regex: {}'.format(action.groups()))
      else: notify("!!! No regex match :(")
   debugNotify("Checking for Min", 2)
   if action.group(2): 
      min = num(action.group(2))
      minTXT = ' (minimum {})'.format(min)
   else: 
      min = 0
      minTXT = ''
   debugNotify("Checking for Max", 2)
   if action.group(6): 
      max = num(action.group(6))
      minTXT += ' (maximum {})'.format(max)
   else: 
      max = None
   debugNotify("Checking for div", 2)
   if action.group(4): 
      div = num(action.group(4))
      minTXT += ' (must be a multiple of {})'.format(div)
   else: div = 1
   debugNotify("Checking for Msg", 2)
   if action.group(8): 
      message = action.group(8)
   else: message = "{}:\nThis effect requires that you provide an 'X'. What should that number be?{}".format(fetchProperty(card, 'name'),minTXT)
   number = min - 1
   debugNotify("About to ask", 2)
   while number < min or number % div or (max and number > max):
      number = askInteger(message,min)
      if number == None: 
         whisper("Aborting Function")
         return 'ABORT'
   debugNotify("<<< RequestInt() with return into = {}".format(number), 3)
   return (announceText, number) # We do not modify the announcement with this function.
   
def RunX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> RunX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRun([A-Z][A-Za-z& ]+)', Autoscript)
   if debugVerbosity >= 2: 
      if action: notify("!!! Regex results: {}".format(action.groups()))
      else: notify("!!! No Regex match :(")
   if action.group(1) == 'End':
      playCorpEndSound()
      jackOut(silent = True)
      if notification == 'Quick': announceString = "{} end the run".format(announceText)
      else: announceString = "{} end the run".format(announceText)
   else:
      if action.group(1) == 'Generic':
         targets = findTarget('Targeted-atServer-isMutedTarget')
         if targets == []: # If the player has not targeted a server, then we ask them what they're targeting.
            debugNotify("No targets found. Asking", 3)
            choice = SingleChoice("Which server are you going to run at?\
                              \n\n(In the future you can target a server before you start a run and we will automatically pick that as the target)",\
                                  ['Remote Server','HQ','R&D','Archives'])
            if choice != None: # Just in case the player didn't just close the askInteger window.
               if choice == 0: targetServer = 'Remote'
               elif choice == 1: targetServer = 'HQ'
               elif choice == 2: targetServer = 'R&D'
               elif choice == 3: targetServer = 'Archives'
               else: return 'ABORT'
            else: return 'ABORT'
         else: # If the player has targeted a server before playing/using their card, then we just use that one
            debugNotify("Targeted Server found!", 3)
            if targets[0].name == 'Remote Server': targetServer = 'Remote'
            else: targetServer = targets[0].name
      else: 
         targetServer = action.group(1)
         if targetServer == 'Remote' and card.name == 'Remote Server': card.target(True) # If the player double clicked the remote server to start a run, then we target it, in order to allow an arrow to be painted.
      feint = re.search(r'-feintTo([A-Za-z&]+)', Autoscript)
      if feint:
         setGlobalVariable('feintTarget',feint.group(1)) # If the card script is feinting to a different fort, set a shared variable so that the corp knows it.
      runTarget = ' on {}'.format(targetServer)
      if intRun(0,targetServer,True) == 'ABORT': return 'ABORT'
      if notification == 'Quick': announceString = "{} starts a run{}".format(announceText, runTarget)
      else: announceString = "{} start a run{}".format(announceText, runTarget)
   if notification and not re.search(r'isSilent', Autoscript): notify('--> {}.'.format(announceString))
   debugNotify("<<< RunX()", 3)
   if re.search(r'isSilent', Autoscript): return announceText
   else: return announceString

def SimplyAnnounce(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> SimplyAnnounce(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bSimplyAnnounce{([A-Za-z0-9&,\. ]+)}', Autoscript)
   if debugVerbosity >= 2: #Debug
      if action: notify("!!! regex: {}".format(action.groups())) 
      else: notify("!!! regex failed :(") 
   if re.search(r'break',Autoscript) and re.search(r'subroutine',Autoscript): penaltyNoisy(card)
   if notification == 'Quick': announceString = "{} {}".format(announceText, action.group(1))
   else: announceString = "{} {}".format(announceText, action.group(1))
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< SimplyAnnounce()", 3)
   return announceString

def SetVarX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> SetVarX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bSetVar([A-Za-z0-9 ]+)-To([A-Za-z0-9 ]+)', Autoscript)
   if debugVerbosity >= 2: #Debug
      if action: notify("!!! regex: {}".format(action.groups()))
      else: notify("!!! regex failed :(") 
   ASVars = eval(getGlobalVariable('AutoScript Variables'))
   ASVars[action.group(1)] = action.group(2)
   setGlobalVariable('AutoScript Variables',str(ASVars))
   debugNotify("ASVars = {}".format(str(ASVars)),4)
   debugNotify("<<< SetVarX()", 3)
   return ''

def CreateDummy(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for creating dummy cards.
   debugNotify(">>> CreateDummy(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global Stored_Name, Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_autoScripts
   dummyCard = None
   action = re.search(r'\bCreateDummy[A-Za-z0-9_ -]*(-with)(?!onOpponent|-doNotTrash|-nonUnique)([A-Za-z0-9_ -]*)', Autoscript)
   if debugVerbosity >= 3 and action: notify('clicks regex: {}'.format(action.groups())) # debug
   targetPL = ofwhom(Autoscript, card.owner)
   for c in table:
      if c.model == card.model and c.controller == targetPL and c.highlight == DummyColor: dummyCard = c # We check if already have a dummy of the same type on the table.
   if not dummyCard or re.search(r'nonUnique',Autoscript): #Some create dummy effects allow for creating multiple copies of the same card model.
      if getSetting('Dummywarn',True) and re.search('onOpponent',Autoscript):
         if not confirm("This action creates an effect for your opponent and a way for them to remove it.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nYou opponent can activate any abilities meant for them on the Dummy card. If this card has one, they can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nOnce the   dummy card is on the table, please right-click on it and select 'Pass control to {}'\
                     \n\nDo you want to see this warning again?".format(targetPL)): setSetting('Dummywarn',False)
      elif getSetting('Dummywarn',True):
         if not confirm("This card's effect requires that you trash it, but its lingering effects will only work automatically while a copy is in play.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nSome cards provide you with an ability that you can activate after they're been trashed. If this card has one, you can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nDo you want to see this warning again?"): setSetting('Dummywarn',False)
      dummyCard = table.create(card.model, -680, 200 * playerside, 1) # This will create a fake card like the one we just created.
      dummyCard.highlight = DummyColor
      storeProperties(dummyCard)
      if re.search(r'onOpponent', Autoscript): passCardControl(dummyCard,findOpponent())
   #confirm("Dummy ID: {}\n\nList Dummy ID: {}".format(dummyCard._id,passedlist[0]._id)) #Debug
   if not re.search(r'doNotTrash',Autoscript):
      debugNotify("Did not find string 'doNotTrash' in {}. Trashing Card".format(Autoscript))
      sendToTrash(card)
   if action: announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard, n = n) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   else: announceString = announceText + 'create a lingering effect for {}'.format(targetPL)
   debugNotify("<<< CreateDummy()", 3)
   return announceString # Creating a dummy isn't usually announced.

def ChooseKeyword(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for marking cards to be of a different keyword than they are
   debugNotify(">>> ChooseKeyword(){}".format(extraASDebug(Autoscript))) #Debug
   #confirm("Reached ChooseKeyword") # Debug
   choiceTXT = ''
   targetCardlist = ''
   existingKeyword = None
   if targetCards is None: targetCards = []
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   if re.search(r'-simpleAnnounce', Autoscript): simpleAnnounce = True # This is needed for cards which select a keyword but it's not meant to assign it to themselves exactly, but we just recycle this function.
   else: simpleAnnounce = False
   action = re.search(r'\bChooseKeyword{([A-Za-z\| ]+)}', Autoscript)
   keywords = action.group(1).split('|')
   if len(keywords) == 1: choice = 0
   else:
      if simpleAnnounce: choiceTXT = 'Please choose keyword'
      else: choiceTXT = 'Choose one of the following keywords to assign to this card'
      choice = SingleChoice(choiceTXT, keywords, type = 'button', default = 0)
      if choice == None: return 'ABORT'
   for targetCard in targetCards:
      if targetCard.markers:
         for key in targetCard.markers:
            if re.search('Keyword:',key[0]):
               existingKeyword = key
      if re.search(r'{}'.format(keywords[choice]),targetCard.Keywords): 
         if existingKeyword: targetCard.markers[existingKeyword] = 0
         else: pass # If the keyword is anyway the same printed on the card, and it had no previous keyword, there is nothing to do
      elif existingKeyword:
         debugNotify("Searching for {} in {}".format(keywords[choice],existingKeyword[0])) # Debug               
         if re.search(r'{}'.format(keywords[choice]),existingKeyword[0]): pass # If the keyword is the same as is already there, do nothing.
         else: 
            targetCard.markers[existingKeyword] = 0 
            TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
      else: TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
   if notification == 'Quick': 
      if simpleAnnounce: announceString = "{} selects {} for {}".format(announceText, keywords[choice], targetCardlist)
      else: announceString = "{} marks {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   else: 
      if simpleAnnounce: announceString = "{} select {} for {}".format(announceText, keywords[choice], targetCardlist)
      else: announceString = "{} mark {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< ChooseKeyword()", 3)
   return announceString
            
def TraceX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   debugNotify(">>> TraceX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bTrace([0-9]+)', Autoscript)
   multiplier = per(Autoscript, card, n, targetCards)
   TraceStrength = num(action.group(1)) * multiplier
   reinforcement = inputTraceValue(card,silent = True)
   if reinforcement == 'ABORT': return 'ABORT'
   if reinforcement: reinforceTXT =  "and reinforced by {} (Total: {})".format(uniCredit(reinforcement),TraceStrength + reinforcement)
   else: reinforceTXT = "(Not reinforced)"
   setGlobalVariable('CorpTraceValue',str(TraceStrength + reinforcement))
   traceEffects = re.search(r'-traceEffects<(.*?),(.*?)>', Autoscript)
   debugNotify("Checking for Trace Effects", 2) #Debug
   if traceEffects:
      traceEffectTuple = (card._id,traceEffects.group(1),traceEffects.group(2))
      debugNotify("TraceEffectsTuple: {}".format(traceEffectTuple), 2) #Debug
      setGlobalVariable('CurrentTraceEffect',str(traceEffectTuple))
   if notification == 'Quick': announceString = "{} starts a Trace with a base strength of {} {}".format(announceText, TraceStrength, reinforceTXT)
   else: announceString = "{} start a trace with a base strength of {} {}".format(announceText, TraceStrength, reinforceTXT)
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< TraceX()", 3)
   return announceString

def PsiX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for setting up a Psi Struggle.
   debugNotify(">>> PsiX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bPsi', Autoscript)
   psiEffects = re.search(r'-psiEffects<(.*?),(.*?)>', Autoscript)
   debugNotify("Checking for Psi Effects", 2) #Debug
   if psiEffects:
      psiEffectTuple = (psiEffects.group(1),psiEffects.group(2))
      debugNotify("psiEffectsTuple: {}".format(psiEffectTuple), 2) #Debug
      setGlobalVariable('CurrentPsiEffect',str(psiEffectTuple))
   else: psiEffectTuple = None
   barNotifyAll('#000000',"{} is initiating a Psi struggle...".format(me))
   playPsiStartSound()
   secretCred = askInteger("How many credits do you want to secretly spend for the Psi effect of {}?".format(fetchProperty(card, 'Name')),0)
   while secretCred and (secretCred - reduceCost(card, 'PSI', secretCred, dryRun = True) > me.Credits) or (secretCred > 2):
      if secretCred - reduceCost(card, 'PSI', secretCred, dryRun = True) > me.Credits and confirm("You do not have that many credits to spend. Bypass?"): break
      if secretCred > 2: warn = ":::ERROR::: You cannot spend more than 2 credits!\n"
      else: warn = ''
      secretCred = askInteger("{}How many credits do you want to secretly spend?".format(warn),0)
   if secretCred != None: 
      notify("{} has spent a hidden amount of credits for {}.".format(me,fetchProperty(card, 'Name')))
      remoteCall(findOpponent(),'runnerPsi',[secretCred,psiEffectTuple,card,me])
   else: return 'ABORT'
   if notification == 'Quick': announceString = "{} sets their hidden Psi value".format(announceText)
   else: announceString = "{} set their hidden Psi value".format(announceText)
   if notification: notify('--> {}.'.format(announceString))
   debugNotify("<<< PsiX()", 3)
   return announceString

def runnerPsi(CorpPsiCount,psiEffectTuple,card,corpPlayer):
   debugNotify(">>> runnerPsi()") #Debug
   mute()
   barNotifyAll('#000000',"{} is guessing the correct Psi value.".format(me))
   secretCred = askInteger("How many credits do you want to spend for the Psi effect of {}?".format(fetchProperty(card, 'Name')),0)
   while secretCred and (secretCred - reduceCost(card, 'PSI', secretCred, dryRun = True) > me.Credits) or (secretCred > 2):
      if secretCred - reduceCost(card, 'PSI', secretCred, dryRun = True) > me.Credits and confirm("You do not have that many credits to spend. Bypass?"): break
      if secretCred > 2: warn = ":::ERROR::: You cannot spend more than 2 credits!\n"
      else: warn = ''
      secretCred = askInteger("{}How many credits do you want to spend?".format(warn),0)
   if secretCred == None: secretCred = 0
   me.Credits -= secretCred - reduceCost(card, 'PSI', secretCred)
   corpPlayer.Credits -= CorpPsiCount - reduceCost(card, 'PSI', CorpPsiCount, reversePlayer = True)
   autoscriptOtherPlayers('RevealedPSI', card)
   if psiEffectTuple: # If the tuple is None, then there's no effects specified for this psi effect.
      debugNotify("Found currentPsiEffectTuple")
      if secretCred != CorpPsiCount:
         notify("-- {} has failed the Psi struggle!\n   ({}: {} VS {}: {})".format(Identity,corpPlayer,uniCredit(CorpPsiCount),me,uniCredit(secretCred)))
         if psiEffectTuple[0] != 'None': executePostEffects(card,psiEffectTuple[0], 0,'Psi')
      else:
         notify("-- {} has succeeded the Psi struggle!\n   ({}: {} VS {}: {})".format(Identity,corpPlayer,uniCredit(CorpPsiCount),me,uniCredit(secretCred)))
         if psiEffectTuple[1] != 'None': executePostEffects(card,psiEffectTuple[1], 0,'Psi')
   pauseRecovery = eval(getGlobalVariable('Paused Runner'))
   if pauseRecovery:
      if pauseRecovery[0] == 'R&D': remoteCall(fetchRunnerPL(),"RDaccessX",[table,0,0,0])
      elif  pauseRecovery[0] == 'HQ': remoteCall(fetchRunnerPL(),"HQaccess",[table,0,0])
   debugNotify("<<< runnerPsi()") #Debug

def ModifyStatus(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for modifying the status of a card on the table.
   debugNotify(">>> ModifyStatus(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   extraText = ''
   action = re.search(r'\b(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile|Rework|Install|Score|Rehost|SendToBottom)(Target|Host|Multi|Myself)[-to]*([A-Z][A-Za-z&_ ]+)?', Autoscript)
   if action.group(2) == 'Myself': 
      del targetCards[:] # Empty the list, just in case.
      targetCards.append(card)
   if action.group(2) == 'Host': 
      del targetCards[:] # Empty the list, just in case.
      debugNotify("Finding Host")
      host = fetchHost(card)
      if host: targetCards = [host]
      else: 
         debugNotify("No Host Found? Aborting!")
         return 'ABORT'      
   if action.group(3): dest = action.group(3)
   else: dest = 'hand'
   for targetCard in targetCards: 
      if action.group(1) == 'Derez': 
         targetCardlist += '{},'.format(fetchProperty(targetCard, 'name')) # Derez saves the name because by the time we announce the action, the card will be face down.
      else: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   for targetCard in targetCards:
      if re.search(r'-ifEmpty',Autoscript):
         debugNotify("Checking if card with {} credits and {} power is empty".format(targetCard.markers[mdict['Credits']],targetCard.markers[mdict['Power']]))
         if targetCard.markers[mdict['Credits']] or targetCard.markers[mdict['Power']]:
            debugNotify("Card is not Empty")
            if len(targetCards) > 1: continue #If the modification only happens when the card runs out of credits or power, then we abort if it still has any
            else: return announceText # If there's only 1 card and it's not supposed to be trashed yet, do nothing.
      if action.group(1) == 'Rez':
         if re.search(r'-payCost',Autoscript): # This modulator means the script is going to pay for the card normally
            preReducRegex = re.search(r'-reduc([0-9])',Autoscript) # this one means its going to reduce the cost a bit.
            if preReducRegex: preReduc = num(preReducRegex.group(1))
            else: preReduc = 0
            intRez(targetCard, cost = 'not free', preReduction = preReduc)
         else: 
            preReduc = 0
            intRez(targetCard, cost = 'free', silent = True)
      elif action.group(1) == 'Derez' and derez(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Expose': 
         exposeResult = expose(targetCard, silent = True)
         if exposeResult == 'ABORT': return 'ABORT'
         elif exposeResult == 'COUNTERED': extraText = " (Countered!)"
      elif action.group(1) == 'Uninstall' and uninstall(targetCard, destination = dest, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Possess':
         if re.search(r'-forceHost',Autoscript):
            if possess(card, targetCard, silent = True, force = True) == 'ABORT': return 'ABORT'
         elif possess(card, targetCard, silent = True) == 'ABORT': return 'ABORT'
      elif action.group(1) == 'Rehost':
         if re.search(r'Caissa', targetCard.Keywords): newHost = chkHostType(targetCard,'DemiAutoTargeted', caissa = True)
         else: newHost = chkHostType(targetCard,'DemiAutoTargeted')
         if not newHost: 
            delayed_whisper("Not a card that {} can rehost on. Bad script?!".format(targetCard))
            return 'ABORT'
         else:
            try:
               if newHost == 'ABORT':
                  delayed_whisper("Please target an appropriate card to host {}".format(targetCard))
                  return 'ABORT'
            except: hostMe(targetCard,newHost)
      elif action.group(1) == 'Trash':
         if targetCard.group.name == "Hand":
            if targetCard.group.controller == me: handDiscard(targetCard, True)
            else: remoteCall(targetCard.group.controller, 'handDiscard', [targetCard,True])
         else:
            trashResult = intTrashCard(targetCard, fetchProperty(targetCard,'Stat'), "free", silent = True)
            if trashResult == 'ABORT': return 'ABORT'
            elif trashResult == 'COUNTERED': extraText = " (Countered!)"
      elif action.group(1) == 'SendToBottom' and movetoBottomOfStack(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Exile' and exileCard(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Rework': # Rework puts a card on top of R&D (usually shuffling afterwards)
         changeCardGroup(targetCard,targetCard.controller.piles['R&D/Stack'])
         #targetCard.moveTo(targetCard.controller.piles['R&D/Stack'])
      elif action.group(1) == 'Install': # Install simply plays a cast on the table unrezzed without paying any costs.
         if re.search(r'-payCost',Autoscript): # This modulator means the script is going to pay for the card normally
            preReducRegex = re.search(r'-reduc([0-9])',Autoscript) # this one means its going to reduce the cost a bit.
            if preReducRegex: preReduc = num(preReducRegex.group(1))
            else: preReduc = 0
            payCost = 'not free'
         else: 
            preReduc = 0
            payCost = 'free'         
         intPlay(targetCard, payCost, True, preReduc)
         extraTokens = re.search(r'-with([0-9][A-Z][A-Za-z&_ ]+)', Autoscript)
         if extraTokens: TokensX('Put{}'.format(extraTokens.group(1)), '',targetCard) # If we have a -with in our autoscript, this is meant to put some tokens on the installed card.
      elif action.group(1) == 'Score': # Score takes a card and claims it as an agenda
         targetPL = ofwhom(Autoscript, targetCard.owner)
         grabCardControl(targetCard)
         if targetPL.getGlobalVariable('ds') == 'corp': scoreType = 'scoredAgenda'
         else: scoreType = 'liberatedAgenda'
         placeCard(targetCard, 'SCORE', type = scoreType)
         #rnd(1,100)
         update()
         card.highlight = None
         card.isFaceUp = True
         update()
         if targetCard.Type == 'Agenda': 
            targetCard.markers[mdict['Scored']] += 1
            targetPL.counters['Agenda Points'].value += num(fetchProperty(targetCard,'Stat'))
            if targetPL.getGlobalVariable('ds') == 'corp': 
               autoscriptOtherPlayers('AgendaScored',card)
               clearCurrents('SCORE',card)
            else: 
               autoscriptOtherPlayers('AgendaLiberated',card)
               clearCurrents('LIBERATE',card)
         debugNotify("Current card group before scoring = {}".format(targetCard.group.name))
         grabCardControl(targetCard,targetPL)
         # We do not autoscript other players (see http://boardgamegeek.com/thread/914076/personal-evolution-and-notoriety)
         if targetPL.counters['Agenda Points'].value >= 7 or (getSpecial('Identity',fetchCorpPL()).name == "Harmony Medtech" and targetPL.counters['Agenda Points'].value >= 6):
            notify("{} wins the game!".format(targetPL))
            if targetPL == me: reportGame()         
            else: reportGame('AgendaDefeat')
      else: return 'ABORT'
      if action.group(2) != 'Multi': break # If we're not doing a multi-targeting, abort after the first run.
   if notification == 'Quick': announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist,extraText)
   else: announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist, extraText)
   if notification and not re.search(r'isSilent', Autoscript): notify('--> {}.'.format(announceString))
   debugNotify("<<< ModifyStatus()", 3)
   if re.search(r'isSilent', Autoscript): return announceText
   else: return announceString
         
def InflictX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for inflicting Damage to players (even ourselves)
   debugNotify(">>> InflictX(){}".format(extraASDebug(Autoscript))) #Debug
   mute()
   if targetCards is None: targetCards = []
   global failedRequirement
   localDMGwarn = True #A variable to check if we've already warned the player during this damage dealing.
   action = re.search(r'\b(Inflict)([0-9]+)(Meat|Net|Brain)Damage', Autoscript) # Find out what kind of damage we're going
   multiplier = per(Autoscript, card, n, targetCards)
   enhancer = findEnhancements(Autoscript) #See if any of our cards increases damage we deal
   debugNotify("card.owner = {}".format(card.owner),3)
   targetPL = fetchRunnerPL() #Damage always goes to the runner
   if enhancer > 0: enhanceTXT = ' (Enhanced: +{})'.format(enhancer) #Also notify that this is the case
   else: enhanceTXT = ''
   if multiplier == 0 or num(action.group(2)) == 0: DMG = 0 # if we don't do any damage, we don't enhance it
   else: DMG = (num(action.group(2)) * multiplier) + enhancer #Calculate our damage
   preventTXT = ''
   if DMG and Automations['Damage']: #The actual effects happen only if the Damage automation switch is ON. It should be ON by default.
      if getSetting('DMGwarn',True) and localDMGwarn:
         localDMGwarn = False # We don't want to warn the player for every point of damage.
         if targetPL != me: notify(":::ATTENTION::: {} is about to inflict {} {} Damage to {}!".format(me,DMG,action.group(3),targetPL))
         if not confirm(":::Warning::: You are about to inflict automatic damage!\
                       \nBefore you do that, please make sure that your target is not currently manipulating their hand or this might cause the game to crash.\
                     \n\nImportant: Before proceeding, ask your target to activate any cards they want that add protection against this type of damage. If this is yourself, please make sure you do this before you activate damage effects.\
                     \n\nDo you want this warning message will to appear again next time you do damage? (Recommended)"): setSetting('DMGwarn',False)
      if re.search(r'nonPreventable', Autoscript): 
         DMGprevented = 0
         preventTXT = ' (Unpreventable)'
      else: DMGprevented = findDMGProtection(DMG, action.group(3), targetPL)
      if DMGprevented == 'ABORT': return 'ABORT'
      elif DMGprevented > 0:
         preventTXT = ' ({} prevented)'.format(DMGprevented)
         DMG -= DMGprevented
      if DMG:
         specialReduction = chkDmgSpecialEffects(action.group(3),DMG)
         finalDMG = DMG - specialReduction[0] # We check if any effect hijacks the normal damage effect, but we don't want to change the number of damage we announce is being done.
         if specialReduction[1]: DMG = 0 
         remoteCall(targetPL, 'intdamageDiscard',[finalDMG])
         if action.group(3) == 'Brain': applyBrainDmg(targetPL, DMG)
      if DMG: 
         autoscriptOtherPlayers('{}DMGInflicted'.format(action.group(3)),getSpecial('Identity',targetPL),DMG) # We also trigger any script for damage
         playDMGSound(action.group(3))
   if targetPL == me: targetPL = 'theirself' # Just changing the announcement to fit better.
   if re.search(r'isRequirement', Autoscript) and DMG < 1: failedRequirement = True # Requirement means that the cost is still paid but other clicks are not going to follow.
   if notification == 'Quick': announceString = "{} suffer {} {} damage{}".format(announceText,DMG,action.group(3),preventTXT)
   else: announceString = "{} inflict {} {} damage{} to {}{}".format(announceText,DMG,action.group(3),enhanceTXT,targetPL,preventTXT)
   if notification and DMG > 0: notify('--> {}.'.format(announceString))
   debugNotify("<<< InflictX()", 3)
   return announceString

def RetrieveX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for finding a specific card from a pile and putting it in hand or trash pile
   debugNotify(">>> RetrieveX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRetrieve([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.owner)
   debugNotify("Setting Source", 2)
   if re.search(r'-fromTrash', Autoscript) or re.search(r'-fromArchives', Autoscript) or re.search(r'-fromHeap', Autoscript):
      source = targetPL.piles['Heap/Archives(Face-up)']
   else:
      source = targetPL.piles['R&D/Stack']
      source.addViewer(me)   
      debugNotify("Making R&D/Stack vidible", 2)
      rnd(1,10) # We give a delay to allow OCTGN to read the card properties before we proceed with checking them
   sourcePath =  "from their {}".format(pileName(source))
   if sourcePath == "from their Face-up Archives": sourcePath = "from their Archives"
   debugNotify("Setting Destination", 2)
   if re.search(r'-toTable', Autoscript):
      destination = table
      if re.search(r'-grab.*?(Event|Operation)',Autoscript): destiVerb = 'play'   
      else: destiVerb = 'install'   
   elif re.search(r'-toDeck', Autoscript):
      destination = targetPL.piles['R&D/Stack']
      destiVerb = 'rework'
   else: 
      destination = targetPL.hand
      destiVerb = 'retrieve'
   debugNotify("Fething Script Variables", 2)
   count = num(action.group(1))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   restrictions = prepareRestrictions(Autoscript, seek = 'retrieve')
   cardList = []
   countRestriction = re.search(r'-onTop([0-9]+)Cards', Autoscript)
   if countRestriction: topCount = num(countRestriction.group(1))
   else: topCount = len(source)
   for c in source.top(topCount):
      debugNotify("Checking card: {}".format(c), 4)
      if checkCardRestrictions(gatherCardProperties(c), restrictions) and checkSpecialRestrictions(Autoscript,c):
         cardList.append(c)
         if re.search(r'-isTopmost', Autoscript) and len(cardList) == count: break # If we're selecting only the topmost cards, we select only the first matches we get.         
   if re.search(r'-fromArchives', Autoscript) and not re.search(r'-faceUpOnly', Autoscript): # If the card is being retrieved from archives, we need to also check hidden archives.
      for c in targetPL.piles['Archives(Hidden)']:
         debugNotify("Checking Hidden Arc card: {}".format(c), 4)
         if checkCardRestrictions(gatherCardProperties(c), restrictions) and checkSpecialRestrictions(Autoscript,c):
            cardList.append(c)
            if re.search(r'-isTopmost', Autoscript) and len(cardList) == count: break # If we're selecting only the topmost cards, we select only the first matches we get.     
   debugNotify("cardList: {}".format([c.name for c in cardList]), 3)
   chosenCList = []
   abortedRetrieve = False
   if len(cardList) > count or re.search(r'upToAmount',Autoscript):
      cardChoices = []
      cardTexts = []
      if count > len(cardList): count = len(cardList) # To avoid crashing if the pile has less cards than the amount we want to retrieve.
      notify(":> {} starts retrieving cards with {}...".format(me,card,count))
      for iter in range(count):
         del cardChoices[:]
         del cardTexts[:]
         for c in cardList:
            if (c.Rules,c.group.name) not in cardTexts or re.search(r'-showDuplicates',Autoscript): # we don't want to provide the player with a the same card as a choice twice, so we check if the a card in this group was already an option.
               debugNotify("Appending card", 4)
               cardChoices.append(c)
               cardTexts.append((c.Rules,c.group.name))
         if re.search(r'upToAmount',Autoscript): cancelButtonName = 'Done'
         else: cancelButtonName = 'Cancel'
         if re.search(r'-fromArchives', Autoscript): showGroup = True # If the card comes from the archives, then we want to inform the player from which group the card is coming from, so that they know to select from Hidden or Face-up Archives
         else: showGroup = False
         choice = SingleChoice("Choose card to retrieve{}".format({1:''}.get(count,' {}/{}'.format(iter + 1,count))), makeChoiceListfromCardList(cardChoices, includeGroup = showGroup), type = 'button', cancelName = cancelButtonName)
         if choice == None:
            if not re.search(r'upToAmount',Autoscript): abortedRetrieve = True # If we have the upToAmount, it means the retrieve can get less cards than the max amount, so cancel does not work as a cancel necessarily.            
            break
         else:
            chosenCList.append(cardChoices[choice])
            cardList.remove(cardChoices[choice])
            if iter + 1 != count: notify(":-> {} out of {} chosen...".format(iter + 1,count))
   else: chosenCList = cardList
   debugNotify("Generating cardNames", 2)
   if re.search(r'doNotReveal',Autoscript): # If we do not reveal the cards, we still want to tell which cards from the face-up archives were taken
      if re.search(r'-fromArchives', Autoscript):
         debugNotify(str(["{} in {}".format(c.name, c.group.name) for c in chosenCList]))
         shownArcCards = [c.name for c in chosenCList if c.group == targetPL.piles['Heap/Archives(Face-up)']]
         debugNotify("shownArcCards = {}".format(shownArcCards))
         hiddenArcCards = [c.name for c in chosenCList if c.group == targetPL.piles['Archives(Hidden)']]
         debugNotify("hiddenArcCards = {}".format(hiddenArcCards))
         if len(shownArcCards) and len(hiddenArcCards): cardNames = "{} and {} hidden card(s)".format(shownArcCards,len(hiddenArcCards))
         elif len(shownArcCards): cardNames = str(shownArcCards)
         else: cardNames = "{} hidden cards".format(len(chosenCList))
      else: cardNames = "{} cards".format(len(chosenCList))
   else: cardNames = str([c.name for c in chosenCList])
   debugNotify("About to move {} to {}".format([c for c in chosenCList],destination.name))
   if not abortedRetrieve:
      for c in chosenCList:
         if destination == table: 
            if re.search(r'-payCost',Autoscript): # This modulator means the script is going to pay for the card normally
               preReducRegex = re.search(r'-reduc([0-9]+)',Autoscript) # this one means its going to reduce the cost a bit.
               if preReducRegex: preReduc = num(preReducRegex.group(1))
               else: preReduc = 0
               payCost = 'not free'
            else: 
               preReduc = 0
               payCost = 'free'         
            intPlay(c, payCost, True, preReduc)
         else: 
            if re.search(r'-sendToBottom', Autoscript): c.moveToBottom(destination)
            else: c.moveTo(destination)
         tokensRegex = re.search(r'-with([A-Za-z0-9: ]+)', Autoscript) # If we have a -with in our autoscript, this is meant to put some tokens on the retrieved card.
         if tokensRegex: TokensX('Put{}'.format(tokensRegex.group(1)), announceText,c, n = n) 
   debugNotify("About to restore pile.", 2)
   if source == targetPL.piles['R&D/Stack']: # If our source was the scripting pile, we know we just checked the R&D,
      source.removeViewer(me)
   if abortedRetrieve: #If the player canceled a retrieve effect from R&D / Stack, we make sure to shuffle their pile as well.
      notify("{} has aborted the retrieval effect from {}".format(me,card))
      if source == me.ScriptingPile: shuffle(targetPL.piles['R&D/Stack'])
      return 'ABORT'
   debugNotify("About to announce.", 2)
   if len(chosenCList) == 0: announceString = "{} attempts to {} a card {}, but there were no valid targets.".format(announceText, destiVerb, sourcePath)
   else: announceString = "{} {} {} {}".format(announceText, destiVerb, cardNames, sourcePath)
   if notification and multiplier > 0: notify(':> {}.'.format(announceString))
   debugNotify("<<< RetrieveX()", 3)
   return (announceString,chosenCList) # We also return which cards we've retrieved
      

#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------
   
def chkNoisy(card): # Check if the player successfully used a noisy icebreaker, and if so, give them the consequences...
   debugNotify(">>> chkNoisy()") #Debug
   if re.search(r'Noisy', fetchProperty(card, 'Keywords')) and re.search(r'Icebreaker', fetchProperty(card, 'Keywords')): 
      me.setGlobalVariable('wasNoisy', '1') # First of all, let all players know of this fact.
      debugNotify("Noisy credit Set!", 2) #Debug
   debugNotify("<<< chkNoisy()", 3) #Debug

def penaltyNoisy(card):
   debugNotify(">>> penaltyNoisy()") #Debug
   if re.search(r'Noisy', fetchProperty(card, 'Keywords')) and re.search(r'Icebreaker', fetchProperty(card, 'Keywords')): 
      NoisyCost = re.search(r'triggerNoisy([0-9]+)',CardsAS.get(card.model,''))
      if debugVerbosity >= 2: 
         if NoisyCost: notify("Noisy Trigger Found: {}".format(NoisyCost.group(1))) #Debug      
         else: notify("Noisy Trigger not found. AS was: {}".format(CardsAS.get(card.model,''))) #Debug      
      if NoisyCost: 
         total = 0
         cost = num(NoisyCost.group(1))
         stealthCards = [c for c in table 
                        if c.controller == me
                        and c.isFaceUp
                        and re.search(r'Stealth',getKeywords(c))
                        and c.markers[mdict['Credits']]]
         debugNotify("{} cards found".format(len(stealthCards)), 2)
         for Scard in sortPriority(stealthCards):
            debugNotify("Removing from {}".format(Scard), 3)
            while cost > 0 and Scard.markers[mdict['Credits']] > 0:
               Scard.markers[mdict['Credits']] -= 1
               cost -= 1
               total += 1
      notify("--> {}'s {} has destroyed a total of {} credits on stealth cards".format(me,card,total))
   debugNotify("<<< penaltyNoisy()", 3) #Debug
   
def autoscriptCostUndo(card, Autoscript): # Function for undoing the cost of an autoscript.
   debugNotify(">>> autoscriptCostUndo(){}".format(extraASDebug(Autoscript))) #Debug
   delayed_whisper("--> Undoing action...")
   actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", Autoscript)
   me.Clicks += num(actionCost.group(1))
   me.counters['Credits'].value += num(actionCost.group(2))
   me.counters['Agenda Points'].value += num(actionCost.group(3))
   if re.search(r"T2:", Autoscript):
      random = rnd(10,5000) # A little wait...
      card.orientation = Rot0

def findTarget(Autoscript, fromHand = False, card = None, dryRun = False): # Function for finding the target of an autoscript
   debugNotify(">>> findTarget(){}".format(extraASDebug(Autoscript))) #Debug
   try:
      if fromHand == True or re.search(r'-fromHand',Autoscript): 
         if re.search(r'-targetOpponents',Autoscript): group = findOpponent().hand
         else: group = me.hand
      elif re.search(r'-fromArchives',Autoscript): 
         if re.search(r'-targetOpponents',Autoscript): group = findOpponent().piles['Heap/Archives(Face-up)']
         else: group = me.piles['Heap/Archives(Face-up)']
      else: group = table
      foundTargets = []
      if re.search(r'Targeted', Autoscript):
         requiredAllegiances = []
         targetGroups = prepareRestrictions(Autoscript)
         debugNotify("About to start checking all targeted cards.\n### targetGroups:{}".format(targetGroups), 2) #Debug
         for targetLookup in group: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
            if (targetLookup.targetedBy and targetLookup.targetedBy == me) or (re.search(r'AutoTargeted', Autoscript) and targetLookup.highlight != DummyColor and targetLookup.highlight != RevealedColor and targetLookup.highlight != InactiveColor):
            # OK the above target check might need some decoding:
            # Look through all the cards on the group and start checking only IF...
            # * Card is targeted and targeted by the player OR target search has the -AutoTargeted modulator and it is NOT highlighted as a Dummy, Inactive or Revealed.
            # * The player who controls this card is supposed to be me or the enemy.
               debugNotify("Checking {}".format(targetLookup), 2)
               if not checkSpecialRestrictions(Autoscript,targetLookup): continue
               if re.search(r'-onHost',Autoscript): 
                  debugNotify("Looking for Host", 2)
                  if not card: continue # If this targeting script targets only a host and we have not passed what the attachment is, we cannot find the host, so we abort.
                  debugNotify("Attachment is: {}".format(card), 2)
                  hostCards = eval(getGlobalVariable('Host Cards'))
                  isHost = False
                  for attachment in hostCards:
                     if attachment == card._id and hostCards[attachment] == targetLookup._id: 
                        debugNotify("Host found! {}".format(targetLookup), 2)
                        isHost = True
                  if not isHost: continue
               if checkCardRestrictions(gatherCardProperties(targetLookup,Autoscript), targetGroups): 
                  if not targetLookup in foundTargets: 
                     debugNotify("About to append {}".format(targetLookup), 3) #Debug
                     foundTargets.append(targetLookup) # I don't know why but the first match is always processed twice by the for loop.
               else: debugNotify("findTarget() Rejected {}".format(targetLookup), 3)# Debug
         debugNotify("Finished seeking. foundTargets List = {}".format([T.name for T in foundTargets]), 2)
         if re.search(r'DemiAutoTargeted', Autoscript):
            debugNotify("Checking DemiAutoTargeted switches", 2)# Debug
            targetNRregex = re.search(r'-choose([1-9])',Autoscript)
            targetedCards = 0
            foundTargetsTargeted = []
            debugNotify("About to count targeted cards", 2)# Debug
            for targetC in foundTargets:
               if targetC.targetedBy and targetC.targetedBy == me: foundTargetsTargeted.append(targetC)
            if targetNRregex:
               debugNotify("!!! targetNRregex exists", 2)# Debug
               if num(targetNRregex.group(1)) > len(foundTargetsTargeted): pass # Not implemented yet. Once I have choose2 etc I'll work on this
               else: # If we have the same amount of cards targeted as the amount we need, then we just select the targeted cards
                  foundTargets = foundTargetsTargeted # This will also work if the player has targeted more cards than they need. The later choice will be simply between those cards.
            else: # If we do not want to choose, then it's probably a bad script. In any case we make sure that the player has targeted something (as the alternative it giving them a random choice of the valid targets)
               del foundTargets[:]
         if len(foundTargets) == 0 and not re.search(r'(?<!Demi)AutoTargeted', Autoscript): 
            targetsText = ''
            mergedList = []
            for posRestrictions in targetGroups: 
               debugNotify("About to notify on restrictions", 2)# Debug
               if targetsText == '': targetsText = '\n -- You need: '
               else: targetsText += ', or '
               del mergedList[:]
               mergedList += posRestrictions[0]
               if len(mergedList) > 0: targetsText += "{} and ".format(mergedList)  
               del mergedList[:]
               mergedList += posRestrictions[1]
               if len(mergedList) > 0: targetsText += "not {}".format(mergedList)
               if targetsText.endswith(' and '): targetsText = targetsText[:-len(' and ')]
            debugNotify("About to chkPlayer()", 2)# Debug
            if not chkPlayer(Autoscript, targetLookup.controller, False, True): 
               allegiance = re.search(r'by(Opponent|Me)', Autoscript)
               requiredAllegiances.append(allegiance.group(1))
            if len(requiredAllegiances) > 0: targetsText += "\n00 Valid Target Allegiance: {}.".format(requiredAllegiances)
            if re.search(r'isRezzed',Autoscript): targetsText += "\n -- Card Status: Rezzed"
            if re.search(r'isUnrezzed',Autoscript): targetsText += "\n -- Card Status: Unrezzed"
            if not re.search(r'isMutedTarget', Autoscript): delayed_whisper(":::ERROR::: You need to target a valid card before using this action{}.".format(targetsText))
         elif len(foundTargets) >= 1 and re.search(r'-choose',Autoscript):
            if dryRun: pass # In dry runs we just want to check we have valid targets
            else:
               debugNotify("Going for a choice menu", 2)# Debug
               choiceType = re.search(r'-choose([0-9]+)',Autoscript)
               targetChoices = makeChoiceListfromCardList(foundTargets)
               if not card: choiceTitle = "Choose one of the valid targets for this effect"
               else: choiceTitle = "Choose one of the valid targets for {}".format(fetchProperty(card, 'name'))
               debugNotify("Checking for SingleChoice", 2)# Debug
               if choiceType.group(1) == '1':
                  if len(foundTargets) == 1: choice = 0 # If we only have one valid target, autoselect it.
                  else: choice = SingleChoice(choiceTitle, targetChoices, type = 'button', default = 0)
                  if choice == 'ABORT': del foundTargets[:]
                  else: foundTargets = [foundTargets.pop(choice)] # if we select the target we want, we make our list only hold that target
         elif re.search(r'-randomTarget',Autoscript): # This modulator randomly selects one card from the valid cards as the single target. Usually paired with AutoTargeted
            debugNotify("Going for a random choice menu")# Debug
            rndChoice = rnd(0,len(foundTargets) - 1)
            foundTargets = [foundTargets[rndChoice]]
      if debugVerbosity >= 3: # Debug
         tlist = [] 
         for foundTarget in foundTargets: tlist.append(foundTarget.name) # Debug
         notify("<<< findTarget() by returning: {}".format(tlist))
      return foundTargets
   except: notify("!!!ERROR!!! on findTarget()")   
   
def gatherCardProperties(card,Autoscript = ''):
   debugNotify(">>> gatherCardProperties()") #Debug     
   cardProperties = []
   if storeProperties(card) != 'ABORT': # We store the card properties so that we don't start flipping the cards over each time.
      debugNotify("Appending name", 4) #Debug
      cName = fetchProperty(card, 'Name')
      cardProperties.append(cName.replace('-','_')) # We are going to check its name. We replace all dashes to underscores to avoid messing up our lookup in prepareRestrictions() 
      debugNotify("Appending Type", 4) #Debug                
      cardProperties.append(fetchProperty(card, 'Type')) # We are going to check its Type
      debugNotify("Appending Keywords", 4) #Debug                
      cardSubkeywords = getKeywords(card).split('-') # And each individual keyword. keywords are separated by " - "
      for cardSubkeyword in cardSubkeywords:
         strippedCS = cardSubkeyword.strip() # Remove any leading/trailing spaces between keywords. We need to use a new variable, because we can't modify the loop iterator.
         if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
      debugNotify("<<< gatherCardProperties() with Card Properties: {}".format(cardProperties), 3) #Debug
   return cardProperties

def prepareRestrictions(Autoscript, seek = 'target'):
# This is a function that takes an autoscript and attempts to find restrictions on card keywords/types/names etc. 
# It goes looks for a specific working and then gathers all restrictions into a list of tuples, where each tuple has a negative and a positive entry
# The positive entry (position [0] in the tuple) contains what card properties a card needs to have to be a valid selection
# The negative entry (position [1] in the tuple) contains what card properties a card needs to NOT have to be a vaid selection.
   debugNotify(">>> prepareRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
   targetGroups = []
   if seek == 'type': whatTarget = re.search(r'\b(type)([A-Za-z0-9_{},&. ]+)[-]?', Autoscript) # seek of "type" is used by autoscripting other players, and it's separated so that the same card can have two different triggers (e.g. see Darth Vader)
   elif seek == 'retrieve': whatTarget = re.search(r'\b(grab)([A-Za-z0-9_{},&. ]+)[-]?', Autoscript) # seek of "retrieve" is used when checking what types of cards to retrieve from one's deck or discard pile
   elif seek == 'reduce': whatTarget = re.search(r'\b(affects)([A-Za-z0-9_{},&. ]+)[-]?', Autoscript) # seek of "reduce" is used when checking for what types of cards to recuce the cost.
   else: whatTarget = re.search(r'\b(at)([A-Za-z0-9_{},&. ]+)[-]?', Autoscript) # We signify target restrictions keywords by starting a string with "or"
   if whatTarget: 
      debugNotify("whatTarget = {}".format(whatTarget.groups()))
      debugNotify("Splitting on _or_", 2) #Debug
      validTargets = whatTarget.group(2).split('_or_') # If we have a list of valid targets, split them into a list, separated by the string "_or_". Usually this results in a list of 1 item.
      ValidTargetsSnapshot = list(validTargets) # We have to work on a snapshot, because we're going to be modifying the actual list as we iterate.
      for iter in range(len(ValidTargetsSnapshot)): # Now we go through each list item and see if it has more than one condition (Eg, non-desert fief)
         debugNotify("Creating empty list tuple", 2) #Debug            
         targetGroups.insert(iter,([],[])) # We create a tuple of two list. The first list is the valid properties, the second the invalid ones
         multiConditionTargets = ValidTargetsSnapshot[iter].split('_and_') # We put all the mutliple conditions in a new list, separating each element.
         debugNotify("Splitting on _and_ & _or_ ", 2) #Debug
         debugNotify("multiConditionTargets is: {}".format(multiConditionTargets), 4) #Debug
         for chkCondition in multiConditionTargets:
            debugNotify("Checking: {}".format(chkCondition), 4) #Debug
            regexCondition = re.search(r'(no[nt]){?([A-Za-z,& ]+)}?', chkCondition) # Do a search to see if in the multicondition targets there's one with "non" in front
            if regexCondition and (regexCondition.group(1) == 'non' or regexCondition.group(1) == 'not'):
               debugNotify("Invalid Target", 4) #Debug
               if regexCondition.group(2) not in targetGroups[iter][1]: targetGroups[iter][1].append(regexCondition.group(2)) # If there is, move it without the "non" into the invalidTargets list.
            else: 
               debugNotify("Valid Target", 4) #Debug
               targetGroups[iter][0].append(chkCondition) # Else just move the individual condition to the end if validTargets list
   else: debugNotify("No restrictions regex", 2) #Debug 
   debugNotify("<<< prepareRestrictions() by returning: {}.".format(targetGroups), 3)
   return targetGroups

def checkCardRestrictions(cardPropertyList, restrictionsList):
   debugNotify(">>> checkCardRestrictions()") #Debug
   debugNotify("cardPropertyList = {}".format(cardPropertyList)) #Debug
   debugNotify("restrictionsList = {}".format(restrictionsList)) #Debug
   validCard = True
   for restrictionsGroup in restrictionsList: 
   # We check each card's properties against each restrictions group of valid + invalid properties.
   # Each Restrictions group is a tuple of two lists. First list (tuple[0]) is the valid properties, and the second list is the invalid properties
   # We check if all the properties from the valid list are in the card properties
   # And then we check if no properties from the invalid list are in the properties
   # If both of these are true, then the card is a valid choice for our action.
      validCard = True # We need to set it here as well for further loops
      debugNotify("restrictionsGroup checking: {}".format(restrictionsGroup), 3)
      if len(restrictionsList) > 0 and len(restrictionsGroup[0]) > 0: 
         for validtargetCHK in restrictionsGroup[0]: # look if the card we're going through matches our valid target checks
            debugNotify("Checking for valid match on {}".format(validtargetCHK), 4) #Debug
            if not validtargetCHK in cardPropertyList: 
               debugNotify("{} not found in {}".format(validtargetCHK,cardPropertyList), 4) #Debug
               validCard = False
      else: debugNotify("No positive restrictions", 4)
      if len(restrictionsList) > 0 and len(restrictionsGroup[1]) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
         for invalidtargetCHK in restrictionsGroup[1]:
            debugNotify("Checking for invalid match on {}".format(invalidtargetCHK), 4) #Debug
            if invalidtargetCHK in cardPropertyList: validCard = False
      else: debugNotify("No negative restrictions", 4)
      if validCard: break # If we already passed a restrictions check, we don't need to continue checking restrictions 
   debugNotify("<<< checkCardRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def checkSpecialRestrictions(Autoscript,card):
# Check the autoscript for special restrictions of a valid card
# If the card does not validate all the restrictions included in the autoscript, we reject it
   debugNotify(">>> checkSpecialRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   debugNotify("Card: {}".format(card)) #Debug
   validCard = True
   if not chkPlayer(Autoscript, card.controller, False, True): validCard = False
   if re.search(r'isICE',Autoscript) and card.orientation != Rot90: 
      debugNotify("Rejecting because it isn't an ICE")
      validCard = False # We made a special check for ICE, because some cards must be able target face-down ICE without being able to read its properties.
   if re.search(r'isRezzed',Autoscript) and not card.isFaceUp: 
      debugNotify("Rejecting because it's not unrezzed")
      validCard = False
   if re.search(r'isUnrezzed',Autoscript) and card.isFaceUp: 
      debugNotify("Rejecting because it's not rezzed")
      validCard = False
   if re.search(r'isScored',Autoscript) and not card.markers[mdict['Scored']] and not card.markers[mdict['ScorePenalty']]:
      debugNotify("Rejecting because it's not a scored agenda")
      validCard = False
   markerName = re.search(r'-hasMarker{([\w ]+)}',Autoscript) # Checking if we need specific markers on the card.
   if markerName: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      debugNotify("Checking marker restrictions", 2)# Debug
      debugNotify("Marker Name: {}".format(markerName.group(1)), 2)# Debug
      marker = findMarker(card, markerName.group(1))
      if not marker: 
         debugNotify("Rejecting because marker not found")
         validCard = False
   markerNeg = re.search(r'-hasntMarker{([\w ]+)}',Autoscript) # Checking if we need to not have specific markers on the card.
   if markerNeg: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      debugNotify("Checking negative marker restrictions", 2)# Debug
      debugNotify("Marker Name: {}".format(markerNeg.group(1)), 2)# Debug
      marker = findMarker(card, markerNeg.group(1))
      if marker: 
         debugNotify("Rejecting because marker was found")
         validCard = False
   else: debugNotify("No marker restrictions.", 4)
   propertyReq = re.search(r'-hasProperty{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript) 
   # Checking if the target needs to have a property at a certiain value. 
   # eq = equal, le = less than/equal, ge = greater than/equal, lt = less than, gt = greater than.
   if propertyReq:
      if propertyReq.group(2) == 'eq' and card.properties[propertyReq.group(1)] != propertyReq.group(3): validCard = False
      if propertyReq.group(2) == 'le' and num(card.properties[propertyReq.group(1)]) > num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'ge' and num(card.properties[propertyReq.group(1)]) < num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'lt' and num(card.properties[propertyReq.group(1)]) >= num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'gt' and num(card.properties[propertyReq.group(1)]) <= num(propertyReq.group(3)): validCard = False
   debugNotify("<<< checkSpecialRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def checkOrigSpecialRestrictions(Autoscript,card):
# Check the autoscript for special restrictions of a originator card
# If the card does not validate all the restrictions included in the autoscript, we reject it
   debugNotify(">>> checkOrigSpecialRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   debugNotify("Card: {}".format(card)) #Debug
   validCard = True
   markerName = re.search(r'-hasOrigMarker{([\w ]+)}',Autoscript) # Checking if we need specific markers on the card.
   if markerName: #If we're looking for markers, then we go through originator's markers any relevant ones
      debugNotify("Checking marker restrictions", 2)# Debug
      debugNotify("Marker Name: {}".format(markerName.group(1)), 2)# Debug
      marker = findMarker(card, markerName.group(1))
      if not marker: 
         debugNotify("Rejecting Originator because marker not found")
         validCard = False
   markerNeg = re.search(r'-hasntOrigMarker{([\w ]+)}',Autoscript) # Checking if we need to not have specific markers on the card.
   if markerNeg: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      debugNotify("Checking negative marker restrictions", 2)# Debug
      debugNotify("Marker Name: {}".format(markerNeg.group(1)), 2)# Debug
      marker = findMarker(card, markerNeg.group(1))
      if marker: 
         debugNotify("Rejecting Originator because marker was found")
         validCard = False
   else: debugNotify("No marker restrictions.", 4)
   # Checking if the target needs to have a markers at a particular value.
   MarkerReq = re.search(r'-ifOrigmarkers{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript)
   if MarkerReq and validCard: 
      debugNotify("Found marker comparison req. regex groups: {}".format(MarkerReq.groups()), 4)
      markerSeek = findMarker(card, MarkerReq.group(1))
      if markerSeek:
         validCard = compareValue(MarkerReq.group(2), card.markers[markerSeek], num(MarkerReq.group(3)))
      else: validCard = compareValue(MarkerReq.group(2), 0, num(MarkerReq.group(3))) #If the card has no markers, then we treat it as having 0 markers.
   debugNotify("<<< checkOrigSpecialRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def makeChoiceListfromCardList(cardList,includeText = False, includeGroup = False):
# A function that returns a list of strings suitable for a choice menu, out of a list of cards
# Each member of the list includes a card's name, traits, resources, markers and, if applicable, combat icons
   debugNotify(">>> makeChoiceListfromCardList()")
   debugNotify("cardList: {}".format([c.name for c in cardList]), 2)
   targetChoices = []
   debugNotify("About to prepare choices list.", 2)# Debug
   for T in cardList:
      debugNotify("Checking {}".format(T), 4)# Debug
      markers = 'Counters:'
      if T.markers[mdict['Advancement']] and T.markers[mdict['Advancement']] >= 1: markers += " {} Advancement,".format(T.markers[mdict['Advancement']])
      if T.markers[mdict['Credits']] and T.markers[mdict['Credits']] >= 1: markers += " {} Credits,".format(T.markers[mdict['Credits']])
      if T.markers[mdict['Power']] and T.markers[mdict['Power']] >= 1: markers += " {} Power.".format(T.markers[mdict['Power']])
      if T.markers[mdict['Virus']] and T.markers[mdict['Virus']] >= 1: markers += " {} Virus.".format(T.markers[mdict['Virus']])
      if T.markers[mdict['Agenda']] and T.markers[mdict['Agenda']] >= 1: markers += " {} Agenda.".format(T.markers[mdict['Agenda']])
      if T.markers[mdict['DaemonMU']] and T.markers[mdict['DaemonMU']] >= 1: markers += " {} Daemon MU.".format(T.markers[mdict['DaemonMU']])
      if markers != 'Counters:': markers += '\n'
      else: markers = ''
      debugNotify("Finished Adding Markers. Adding stats...", 4)# Debug               
      stats = ''
      stats += "Cost: {}. ".format(fetchProperty(T, 'Cost'))
      cStat = fetchProperty(T, 'Stat')
      cType = fetchProperty(T, 'Type')
      if cType == 'ICE': stats += "Strength: {}.".format(cStat)
      if cType == 'Program': stats += "MU: {}.".format(fetchProperty(T, 'Requirement'))
      if cType == 'Agenda': stats += "Agenda Points: {}.".format(cStat)
      if cType == 'Asset' or cType == 'Upgrade': stats += "Trash Cost: {}.".format(cStat)
      if includeText: cText = '\n' + fetchProperty(T, 'Rules')
      else: cText = ''
      hostCards = eval(getGlobalVariable('Host Cards'))
      attachmentsList = [Card(cID).name for cID in hostCards if hostCards[cID] == T._id]
      if len(attachmentsList) >= 1: cAttachments = '\nAttachments:' + str(attachmentsList)
      else: cAttachments = ''
      if includeGroup: cGroup = '\n' + pileName(T.group) # Include group is used to inform the player where the card resides in cases where they're selecting cards from multiple groups.
      else: cGroup = ''
      debugNotify("Finished Adding Stats. Going to choice...", 4)# Debug               
      choiceTXT = "{}\n{}\n{}\n{}{}{}{}{}".format(fetchProperty(T, 'name'),cType,getKeywords(T),markers,stats,cAttachments,cText,cGroup)
      targetChoices.append(choiceTXT)
   return targetChoices
   debugNotify("<<< makeChoiceListfromCardList()", 3)
   
def chkWarn(card, Autoscript): # Function for checking that an autoscript announces a warning to the player
   debugNotify(">>> chkWarn(){}".format(extraASDebug(Autoscript))) #Debug
   warning = re.search(r'warn([A-Z][A-Za-z0-9 ]+)-?', Autoscript)
   if debugVerbosity >= 2:  notify("About to check warning")
   if warning:
      if warning.group(1) == 'Discard': 
         if not confirm("This action requires that you discard some cards. Have you done this already?"):
            whisper("--> Aborting action. Please discard the necessary amount of cards and run this action again")
            return 'ABORT'
      if warning.group(1) == 'ReshuffleOpponent': 
         if not confirm("This action will reshuffle your opponent's pile(s). Are you sure?\n\n[Important: Please ask your opponent not to take any clicks with their piles until this clicks is complete or the game might crash]"):
            whisper("--> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'GiveToOpponent': confirm('This card has an effect which if meant for your opponent. Please use the menu option "pass control to" to give them control.')
      if warning.group(1) == 'Reshuffle': 
         if not confirm("This action will reshuffle your piles. Are you sure?"):
            whisper("--> Aborting action.")
            return 'ABORT'
      if warning.group(1) == 'Workaround':
         notify(":::Note:::{} is using a workaround autoscript".format(me))
      if warning.group(1) == 'LotsofStuff': 
         if not confirm("This card performs a lot of complex clicks that will very difficult to undo. Are you sure you want to proceed?"):
            whisper("--> Aborting action.")
            return 'ABORT'
   debugNotify("<<< chkWarn() gracefully", 3) 
   return 'OK'

def ASclosureTXT(string, count): # Used by Gain and Transfer, to return unicode credits, link etc when it's used in notifications
   debugNotify(">>> ASclosureTXT(). String: {}. Count: {}".format(string, count)) #Debug
 # function that returns a special string with the ANR unicode characters, based on the string and count that we provide it. 
 # So if it's provided with 'Credits', 2, it will return 2 [credits] (where [credits] is either the word or its symbol, depending on the unicode switch.
   if string == 'Base Link': closureTXT = '{} {}'.format(count,uniLink())
   elif string == 'Clicks' or string == 'Click': closureTXT = '{} {}'.format(count,uniClick())
   elif string == 'Credits' or string == 'Credit': 
      if count == 'all': closureTXT = 'all Credits'
      else: closureTXT = uniCredit(count)
   elif string == 'MU': closureTXT = uniMU(count)
   else: closureTXT = "{} {}".format(count,string)
   debugNotify("<<< ASclosureTXT() returning: {}".format(closureTXT), 3)
   return closureTXT
   
def ofwhom(Autoscript, controller = me): 
   debugNotify(">>> ofwhom(){}".format(extraASDebug(Autoscript))) #Debug
   debugNotify("Controller = {}".format(controller),2) #Debug
   if re.search(r'o[fn]Opponent', Autoscript):
      if debugVerbosity >= 2:  notify("Autoscript requirement found!")
      if len(players) > 1:
         if controller == me: # If we're the current controller of the card who's scripts are being checked, then we look for our opponent
            targetPL = None # First we Null the variable, to make sure it is filled.
            for player in players:
               if player.getGlobalVariable('ds') == '': continue # This is a spectator 
               elif player != me and player.getGlobalVariable('ds') != ds:
                  targetPL = player # Opponent needs to be not us, and of a different type. 
                                    # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
            if not targetPL: # If the variable was not filled, it means the opponent may not have set up their side first. In that case, we try and guess who it is
               for player in players:
                  if len(player.hand) > 0: targetPL = player # If they have at least loaded a deck, we assume they're the opponent, as spectators shouldn't be loading up decks
               if not targetPL: # If we still don't have a probable opponent, we just choose the second player (but there's a chance we'll grab a spectator)
                  targetPL = players[1]
         else: targetPL = me # if we're not the controller of the card we're using, then we're the opponent of the player (i.e. we're trashing their card)
      else: 
         if debugVerbosity >= 1: whisper("There's no valid Opponents! Selecting myself.")
         targetPL = me
   else: 
      if debugVerbosity >= 2:  notify("No autoscript requirement found")
      if len(players) > 1:
         if controller != me: targetPL = controller         
         else: targetPL = me
      else: targetPL = me
   if debugVerbosity >= 3:  notify("<<< ofwhom() returning {}".format(targetPL.name))
   return targetPL
   
def per(Autoscript, card = None, count = 0, targetCards = None, notification = None): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   debugNotify(">>> per(){}".format(extraASDebug(Autoscript))) #Debug
   debugNotify("per() passwd vars: card = {}. count = {}".format(card,count),4)
   div = 1
   ignore = 0
   max = 0 # A maximum of 0 means no limit   
   per = re.search(r'\b(per|upto)(Target|Host|Every)?([A-Z][^-]*)-?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable. 
   if per and not re.search(r'<.*?(per|upto).*?>',Autoscript): # If the  search was successful...
                                                               # We ignore "per" between <> as these are trace effects and are not part of the same script
      debugNotify("per Regex groups: {}".format(per.groups()),3)
      multiplier = 0
      if per.group(2) and (per.group(2) == 'Target' or per.group(2) == 'Every'): # If we're looking for a target or any specific type of card, we need to scour the requested group for targets.
         debugNotify("Checking for Targeted per", 2)
         perTargetRegex = re.search(r'\bper(Target|Every)', Autoscript)
         perReqRegex = re.search(r'\bper(Target|Every).*?-at(.*)', Autoscript)
         debugNotify("perTargetRegex = {}".format(perTargetRegex.groups()))
         if not perReqRegex: seek = ''
         else: seek = '-at{}'.format(perReqRegex.group(2))            
         if perTargetRegex.group(1) == 'Target':
            if re.search('fromHand', Autoscript): 
               targetCards = findTarget('Targeted{}'.format(seek),True)
            else: targetCards = findTarget('Targeted{}'.format(seek))
         else: 
            if re.search('fromHand', Autoscript): targetCards = findTarget('AutoTargeted{}'.format(seek),True)
            else: targetCards = findTarget('AutoTargeted-{}'.format(seek))
         if len(targetCards) == 0: pass # If we were expecting some targeted cards but found none, we return a multiplier of 0
         else:
            debugNotify("Looping through {} targetCards".format(len(targetCards)))
            for perCard in targetCards:
               debugNotify("perCard = {}".format(perCard), 2)
               if re.search(r'Marker',per.group(3)):
                  debugNotify("Counting Markers on Card")
                  markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
                  marker = findMarker(perCard, markerName.group(1))
                  if marker: multiplier += perCard.markers[marker]
               elif re.search(r'Property',per.group(3)):
                  debugNotify("Counting Property stat on Card")
                  property = re.search(r'Property{([\w ]+)}',per.group(3))
                  multiplier += num(perCard.properties[property.group(1)])
               else: 
                  multiplier += 1 # If there's no special conditions, then we just add one multiplier per valid (auto)target.
                  debugNotify("Increasing Multiplier by 1 to {}".format(multiplier))
      else: #If we're not looking for a particular target, then we check for everything else.
         debugNotify("Doing no table lookup", 2) # Debug.
         if per.group(3) == 'X': multiplier = count # Probably not needed and the next elif can handle alone anyway.
         elif re.search(r'Marker',per.group(3)):
            markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
            debugNotify("found per Marker requirement: {}".format(markerName.group(1)),4)
            marker = findMarker(card, markerName.group(1))
            if marker:
               debugNotify("found {} Marker(s)".format(card.markers[marker]),4)
               multiplier = card.markers[marker]
            else: 
               debugNotify("Didn't find any relevant Markers",4)
               multiplier = 0
         elif re.search(r'Property',per.group(3)):
            property = re.search(r'Property{([\w ]+)}',per.group(3))
            multiplier = num(card.properties[property.group(1)])
         elif re.search(r'Counter',per.group(3)):
            debugNotify("Checking perCounter", 2) # Debug.   
            counter = re.search(r'Counter{([\w ]+)}',per.group(3))
            if re.search(r'MyCounter',per.group(3)): 
               if card.controller == me: player = me
               else: player = findOpponent()
            else:
               if card.controller == me: player = findOpponent()
               else: player = me
            multiplier = player.counters[counter.group(1)].value
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
      debugNotify("Checking ignore", 2) # Debug.            
      ignS = re.search(r'-ignore([0-9]+)',Autoscript)
      if ignS: ignore = num(ignS.group(1))
      debugNotify("Checking div", 2) # Debug.            
      divS = re.search(r'-div([0-9]+)',Autoscript)
      if divS: div = num(divS.group(1))
      debugNotify("Checking max") # Debug.            
      maxS = re.search(r'-max([0-9]+)',Autoscript)
      if maxS: max = num(maxS.group(1))
   else: 
      debugNotify("no per")
      multiplier = 1
   finalMultiplier = (multiplier - ignore) / div
   if max and finalMultiplier > max: 
      debugNotify("Reducing Multiplier to Max",2)
      finalMultiplier = max
   debugNotify("<<< per() with Multiplier: {}".format((multiplier - ignore) / div), 2) # Debug
   return finalMultiplier

def ifHave(Autoscript,controller = me,silent = False):
# A functions that checks if a player has a specific property at a particular level or not and returns True/False appropriately
   debugNotify(">>> ifHave(){}".format(extraASDebug(Autoscript))) #Debug
   Result = True
   if re.search(r'isSilentHaveChk',Autoscript): silent = True
   ifHave = re.search(r"\bif(I|Opponent)(Have|Hasnt)([0-9]+)([A-Za-z ]+)",Autoscript)
   if ifHave:
      debugNotify("ifHave groups: {}".format(ifHave.groups()), 3)
      if ifHave.group(1) == 'I':
         if controller == me: player = me
         else: player = findOpponent()
      else: 
         if controller == me: player = findOpponent()
         else: player = me
      count = num(ifHave.group(3))
      property = ifHave.group(4)
      if ifHave.group(2) == 'Have': # 'Have' means that we're looking for a counter value that is equal or higher than the count
         if not player.counters[property].value >= count: 
            Result = False # If we're looking for the player having their counter at a specific level and they do not, then we return false
            if not silent: delayed_whisper(":::ERROR::: You need at least {} {} to use this effect".format(property,count))
      else: # Having a 'Hasn't' means that we're looking for a counter value that is lower than the count.
         if not player.counters[property].value < count: 
            Result = False
            if not silent: delayed_whisper(":::ERROR::: You need at least {} {} to use this effect".format(property,count))
   debugNotify("<<< ifHave() with Result: {}".format(Result), 3) # Debug
   return Result # If we don't have an ifHave clause, then the result is always True      
      
def ifVarSet(Autoscript):
# A functions that checks if a shared variable has been set to a certain value before allowing a script to proceed.
   debugNotify(">>> ifVarSet(){}".format(extraASDebug(Autoscript))) #Debug
   Result = True
   ifVar = re.search(r"\bifVar([0-9A-Za-z ]+)_SetTo_([0-9A-Za-z ]+)",Autoscript)
   if ifVar:
      debugNotify("ifVar groups: {}".format(ifVar.groups()), 3)
      ASVars = eval(getGlobalVariable('AutoScript Variables'))
      if ASVars.get(ifVar.group(1),'NULL') != ifVar.group(2): Result = False
   debugNotify("<<< ifVarSet() with Result: {}".format(Result), 3) # Debug
   return Result # If we don't have an ifHave clause, then the result is always True      
      
def chkRunningStatus(autoS): # Checks a script to see if it requires a run to be in progress and returns True or False if it passes the check.
   debugNotify(">>> chkRunningStatus() with autoS = {}".format(autoS)) #Debug
   Result = True
   runRegex = re.search(r'whileRunning([A-Za-z&]+)?', autoS)
   if runRegex:
      if debugVerbosity >= 2:
         try: notify("runRegex group(1) = {}".format(runRegex.group(1)))
         except: notify(":::ERROR::: while checking runRegex.group(1)")
      statusRegex = re.search(r'running([A-Za-z&]+)',getGlobalVariable('status')) # This global variable holds the status of the game. I.e. if there's a run ongoing or not.
      if not statusRegex: Result = False # Some autoscripted abilities only work while a run is in progress (e.g. Spinal Modem.)
      elif runRegex.group(1) and runRegex.group(1) != statusRegex.group(1): Result = False # If the script only works while running a specific server, and we're not, then abort.
   debugNotify("<<< chkRunningStatus() with Result: {}".format(Result), 3) # Debug
   return Result
   
def chkPlayer(Autoscript, controller, manual, targetChk = False, reversePlayerChk = False): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   debugNotify(">>> chkPlayer(). Controller is: {}".format(controller)) #Debug
   try:
      if targetChk: # If set to true, it means we're checking from the findTarget() function, which needs a different keyword in case we end up with two checks on a card's controller on the same script
         byOpponent = re.search(r'targetOpponents', Autoscript)
         byMe = re.search(r'targetMine', Autoscript)
      else:
         byOpponent = re.search(r'(byOpponent|duringOpponentTurn|forOpponent)', Autoscript)
         byMe = re.search(r'(byMe|duringMyTurn|forMe)', Autoscript)
      if manual or len(players) == 1: # If there's only one player, we always return true for debug purposes.
         debugNotify("Succeeded at Manual/Debug", 2)
         validPlayer = 1 #manual means that the clicks was called by a player double clicking on the card. In which case we always do it.
      elif not byOpponent and not byMe: 
         debugNotify("Succeeded at Neutral", 2)   
         validPlayer = 1 # If the card has no restrictions on being us or a rival.
      elif byOpponent and controller != me: 
         debugNotify("Succeeded at byOpponent", 2)   
         validPlayer =  1 # If the card needs to be played by a rival.
      elif byMe and controller == me: 
         debugNotify("Succeeded at byMe", 2)   
         validPlayer =  1 # If the card needs to be played by us.
      else: 
         debugNotify("Failed all checks", 2) # Debug
         validPlayer =  0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 whic
      if not reversePlayerChk: 
         debugNotify("<<< chkPlayer() (not reversed)", 3) # Debug
         return validPlayer
      else: # In case reversePlayerChk is set to true, we want to return the opposite result. This means that if a scripts expect the one running the effect to be the player, we'll return 1 only if the one running the effect is the opponent. See Decoy at Dantoine for a reason
         debugNotify("<<< chkPlayer() (reversed)", 3) # Debug      
         if validPlayer == 0: return 1
         else: return 0
   except: 
      notify("!!!ERROR!!! Null value on chkPlayer()")
      return 0
   
def chkTagged(Autoscript, silent = False):
### Check if the action needs the player or his opponent to be targeted
   debugNotify(">>> chkTagged(). Autoscript is: {}".format(Autoscript))
   if ds == 'corp': runnerPL = findOpponent()
   else: runnerPL = me
   regexTag = re.search(r'ifTagged([0-9]+)', Autoscript)
   if regexTag and runnerPL.Tags < num(regexTag.group(1)) and not re.search(r'doesNotBlock', Autoscript): #See if the target needs to be tagged a specific number of times.
      if not silent:
         if regexTag.group(1) == '1': whisper("The runner needs to be tagged for you to use this action")
         else: whisper("The Runner needs to be tagged {} times for you to to use this action".format(regexTag.group(1)))
      return 'ABORT'
   return 'OK'

def chkRunStatus(Autoscript): # Function for figuring out if an autoscript is supposed to work only when a central or remote was run or not.
   debugNotify(">>> chkRunStatus(). Autoscript is: {}".format(Autoscript)) #Debug
   runCentral = getGlobalVariable('Central Run')
   runRemote = getGlobalVariable('Remote Run')
   debugNotify("runCentral = {}, runRemote = {}".format(runCentral,runRemote))
   validCard = True
   if re.search(r'-ifHasRunAny',Autoscript) and runCentral == 'False' and runRemote == 'False': 
      debugNotify("Rejecting because no server was run")
      validCard = False
   if re.search(r'-ifHasRunCentral',Autoscript) and runCentral == 'False': 
      debugNotify("Rejecting because Central Server not run")
      validCard = False
   if re.search(r'-ifHasRunRemote',Autoscript) and runRemote == 'False': 
      debugNotify("Rejecting because Remote Server not run")
      validCard = False
   if re.search(r'-ifHasSucceededAny',Autoscript) and runCentral != 'Success' and runRemote != 'Success': 
      debugNotify("Rejecting because no server was run successfully")
      validCard = False
   if re.search(r'-ifHasSucceededCentral',Autoscript) and runCentral != 'Success': 
      debugNotify("Rejecting because Central Server not run successfully")
      validCard = False
   if re.search(r'-ifHasSucceededRemote',Autoscript) and runRemote != 'Success': 
      debugNotify("Rejecting because Remote Server not run successfully")
      validCard = False
   if re.search(r'-ifHasnotRunAny',Autoscript) and (runCentral != 'False' or runRemote != 'False'): 
      debugNotify("Rejecting because any server was run")
      validCard = False
   if re.search(r'-ifHasnotRunCentral',Autoscript) and runCentral != 'False': 
      debugNotify("Rejecting because Central Server was run")
      validCard = False
   if re.search(r'-ifHasnotRunRemote',Autoscript) and runRemote != 'False': 
      debugNotify("Rejecting because Remote Server was run")
      validCard = False
   if re.search(r'-ifHasnotSucceededAny',Autoscript) and (runCentral == 'Success' or runRemote == 'Success'): 
      debugNotify("Rejecting because any server was run successfully")
      validCard = False
   if re.search(r'-ifHasnotSucceededCentral',Autoscript) and runCentral == 'Success': 
      debugNotify("Rejecting because Central Server was run successfully")
      validCard = False
   if re.search(r'-ifHasnotSucceededRemote',Autoscript) and runRemote == 'Success': 
      debugNotify("Rejecting because Remote Server was run successfully")
      validCard = False
   debugNotify("<<< chkRunStatus(). validCard is: {}".format(validCard)) #Debug
   return validCard
