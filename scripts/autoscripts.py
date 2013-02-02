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
reversePlayerChk = False

#------------------------------------------------------------------------------
# Play/Score/Rez/Trash trigger
#------------------------------------------------------------------------------

def executePlayScripts(card, action):
   action = action.upper() # Just in case we passed the wrong case
   if debugVerbosity >= 1: notify(">>> executePlayScripts() with action: {}".format(action)) #Debug
   global failedRequirement
   if not Automations['Play, Score and Rez']: 
      if debugVerbosity >= 2: notify("Exiting because automations are off")
      return
   if not card.isFaceUp: 
      if debugVerbosity >= 2: notify("Exiting because card is face down")
      return
   if CardsAS.get(card.model,'') == '': 
      if debugVerbosity >= 2: notify("Exiting because card has no autoscripts")
      return
   failedRequirement = False
   X = 0
   Autoscripts = CardsAS.get(card.model,'').split('||') # When playing cards, the || is used as an "and" separator, rather than "or". i.e. we don't do choices (yet)
   AutoScriptsSnapshot = list(Autoscripts) # Need to work on a snapshot, because we'll be modifying the list.
   for autoS in AutoScriptsSnapshot: # Checking and removing any "AtTurnStart" clicks.
      if (re.search(r'atTurn(Start|End)', autoS) or 
          re.search(r'atRunStart', autoS) or 
          re.search(r'Reduce[0-9#X]Cost', autoS) or 
          re.search(r'whileRunning', autoS) or 
          re.search(r'atJackOut', autoS) or 
          re.search(r'atSuccessfulRun', autoS) or 
          re.search(r'onAccess', autoS) or 
          re.search(r'Placement', autoS) or 
          re.search(r'onPay', autoS) or # onPay effects are only useful before we go to the autoscripts, for the cost reduction.
          re.search(r'triggerNoisy', autoS) or # Trigger Noisy are used automatically during action use.
          re.search(r'-isTrigger', autoS)): Autoscripts.remove(autoS)
      elif re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: Autoscripts.remove(autoS)
      elif re.search(r'CustomScript', autoS): 
         CustomScript(card,action)
         Autoscripts.remove(autoS)
   if len(Autoscripts) == 0: return
   for AutoS in Autoscripts:
      if debugVerbosity >= 2: notify("### First Processing: {}".format(AutoS)) # Debug
      effectType = re.search(r'(on[A-Za-z]+|while[A-Za-z]+):', AutoS) 
      if ((effectType.group(1) == 'onRez' and action != 'REZ') or # We don't want onPlay effects to activate onTrash for example.
          (effectType.group(1) == 'onPlay' and action != 'PLAY') or
          (effectType.group(1) == 'onInstall' and action != 'INSTALL') or
          (effectType.group(1) == 'onScore' and action != 'SCORE') or
          (effectType.group(1) == 'whileScored' and ds != 'corp') or
          (effectType.group(1) == 'whileLiberated' and ds != 'runner') or
          (effectType.group(1) == 'onDamage' and action != 'DAMAGE') or
          (effectType.group(1) == 'onLiberation' and action != 'LIBERATE') or
          (effectType.group(1) == 'onTrash' and (action != 'TRASH' or action!= 'UNINSTALL' or action != 'DEREZ')) or
          (effectType.group(1) == 'onDerez' and action != 'DEREZ')): continue 
      if re.search(r'-isOptional', AutoS):
         if not confirm("This card has an optional ability you can activate at this point. Do you want to do so?"): 
            notify("{} opts not to activate {}'s optional ability".format(me,card))
            return 'ABORT'
         else: notify("{} activates {}'s optional ability".format(me,card))
      selectedAutoscripts = AutoS.split('$$')
      if debugVerbosity >= 2: notify ('### selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for activeAutoscript in selectedAutoscripts:
         if debugVerbosity >= 2: notify("### Second Processing: {}".format(activeAutoscript)) # Debug
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         if re.search(r':Pass\b', activeAutoscript): return # Pass is a simple command of doing nothing ^_^
         effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{}\|:,<> -]*)', activeAutoscript)
         if debugVerbosity >= 2: notify('### effects: {}'.format(effect.groups())) #Debug
         if effectType.group(1) == 'whileRezzed' or effectType.group(1) == 'whileScored':
            if effect.group(1) != 'Gain' and effect.group(1) != 'Lose': continue # The only things that whileRezzed and whileScored affect in execute Automations is GainX scripts (for now). All else is onTrash, onPlay etc
            if action == 'DEREZ' or ((action == 'TRASH' or action == 'UNINSTALL') and card.isFaceUp): Removal = True
            else: Removal = False
         elif action == 'DEREZ' or action == 'TRASH': return # If it's just a one-off event, and we're trashing it, then do nothing.
         else: Removal = False
         targetC = findTarget(activeAutoscript)
         targetPL = ofwhom(activeAutoscript,card.controller) # So that we know to announce the right person the effect, affects.
         announceText = "{} uses {}'s ability and".format(targetPL,card)
         if debugVerbosity >= 3: notify("#### targetC: {}".format(targetC)) # Debug
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
            if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
            gainTuple = GainX(passedScript, announceText, card, targetC, notification = 'Quick', n = X, actionType = action)
            if gainTuple == 'ABORT': return
            X = gainTuple[1] 
         else: 
            passedScript = effect.group(0)
            if debugVerbosity >= 2: notify("### passedscript: {}".format(passedScript)) # Debug
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
            elif regexHooks['ModifyStatus'].search(passedScript): 
               if ModifyStatus(passedScript, announceText, card, targetC, notification = 'Quick', n = X) == 'ABORT': return
         if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
         if debugVerbosity >= 2: notify("Loop for scipt {} finished".format(passedScript))

#------------------------------------------------------------------------------
# Card Use trigger
#------------------------------------------------------------------------------

def useAbility(card, x = 0, y = 0): # The start of autoscript activation.
   if debugVerbosity >= 1: notify(">>> useAbility(){}".format(extraASDebug())) #Debug
   mute()
   global failedRequirement,gatheredCardList
   AutoscriptsList = [] # An empty list which we'll put the AutoActions to execute.
   storeProperties(card) # Just in case
   failedRequirement = False # We set it to false when we start a new autoscript.
   if debugVerbosity >= 5: notify("+++ Checking if Tracing card...")
   if (card._id in Stored_Type and fetchProperty(card, 'Type') == 'Tracing') or card.model == 'eb7e719e-007b-4fab-973c-3fe228c6ce20': # If the player double clicks on the Tracing card...
      if debugVerbosity >= 5: notify("+++ Confirmed tacting card. Checking Status...")
      if card.isFaceUp and not card.markers[mdict['Credits']]: inputTraceValue(card, limit = 0)
      elif card.isFaceUp and card.markers[mdict['Credits']]: payTraceValue(card)
      elif not card.isFaceUp: card.isFaceUp = True
      return
   if debugVerbosity >= 5: notify("+++ Not a tracing card. Checking highlight...")
   if card.highlight == InactiveColor:
      accessRegex = re.search(r'onAccess:([^|]+)',CardsAS.get(card.model,''))
      if not accessRegex:
         whisper("You cannot use inactive cards. Please use the relevant card abilities to clear them first. Aborting")
         return
   if debugVerbosity >= 5: notify("+++ Not an inactive card. Checking Stored_Autoactions{}...")
   if debugVerbosity >= 5: notify("+++ Finished storing CardsAA.get(card.model,'')s. Checking Rez status")
   if not card.isFaceUp:
      if re.search(r'onAccess',fetchProperty(card, 'AutoActions')) and confirm("This card has an ability that can be activated even when unrezzed. Would you like to activate that now?"): card.isFaceUp = True # Activating an on-access ability requires the card to be exposed, it it's no already.
      elif re.search(r'Hidden',fetchProperty(card, 'Keywords')): card.isFaceUp # If the card is a hidden resource, just turn it face up for its imminent use.
      elif fetchProperty(card, 'Type') == 'Agenda': 
         scrAgenda(card) # If the player double-clicks on an Agenda card, assume they wanted to Score it.
         return
      else: 
         intRez(card) # If card is face down or not rezzed assume they wanted to rez       
         return
   if debugVerbosity >= 5: notify("+++ Card not unrezzed. Checking for automations switch...")
   if not Automations['Play, Score and Rez'] or fetchProperty(card, 'AutoActions') == "": 
      useCard(card) # If card is face up but has no autoscripts, or automation is disabled just notify that we're using it.
      return
   if debugVerbosity >= 5: notify("+++ Automations active. Checking for CustomScript...")
   if re.search(r'CustomScript', fetchProperty(card, 'AutoActions')): 
      if chkTargeting(card) == 'ABORT': return
      CustomScript(card,'USE') # Some cards just have a fairly unique effect and there's no use in trying to make them work in the generic framework.
      return
   if debugVerbosity >= 5: notify("+++ All checks done!. Starting Choice Parse...")
   ### Checking if card has multiple autoscript options and providing choice to player.
   Autoscripts = fetchProperty(card, 'AutoActions').split('||')
   AutoScriptSnapshot = list(Autoscripts)
   for autoS in AutoScriptSnapshot: # Checking and removing any clickscripts which were put here in error.
      if (re.search(r'while(Rezzed|Scored)', autoS) 
         or re.search(r'on(Play|Score|Install)', autoS) 
         or re.search(r'AtTurn(Start|End)', autoS)
         or not card.isFaceUp and not re.search(r'onAccess', autoS) # If the card is still unrezzed and the ability does not have "onAccess" on it, it can't be used.
         or (re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor)
         or (re.search(r'(CreateDummy|excludeDummy)', autoS) and card.highlight == DummyColor)): # Dummies in general don't create new dummies
         Autoscripts.remove(autoS)
   if debugVerbosity >= 2: notify("### Removed bad options")
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
            if debugVerbosity >= 2: notify("Autoscripts {}".format(Autoscripts)) # Debug
            abilRegex = re.search(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):([A-Z][A-Za-z ]+)([0-9]*)([A-Za-z ]*)-?(.*)", Autoscripts[idx]) # This regexp returns 3-4 groups, which we then reformat and put in the confirm dialogue in a better readable format.
            if debugVerbosity >= 2: notify("### Choice Regex is {}".format(abilRegex.groups())) # Debug
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
            if debugVerbosity >= 3: notify("### About to check rest of choice regex")
            if abilRegex.group(8): # If the autoscript has an 8th group, then it means it has subconditions. Such as "per Marker" or "is Subroutine"
               subconditions = abilRegex.group(8).split('$$') # These subconditions are always separated by dashes "-", so we use them to split the string
               for idx2 in range(len(subconditions)):
                  if debugVerbosity >= 4: notify("#### Checking subcondition {}:{}".format(idx2,subconditions[idx2]))
                  if re.search(r'isCost', Autoscripts[idx]) and idx2 == 1: choices[idx] += ' to' # The extra costs of an action are always at the first part (i.e. before the $$)
                  elif idx2 > 0: choices[idx] += ' and'
                  subadditions = subconditions[idx2].split('-')
                  for idx3 in range(len(subadditions)):
                     if debugVerbosity >= 4: notify("#### Checking subaddition {}-{}:{}".format(idx2,idx3,subadditions[idx3]))
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
      if debugVerbosity >= 2: notify("### AutoscriptsList: {}".format(AutoscriptsList)) # Debug
   else: AutoscriptsList.append(Autoscripts[0].split('$$'))
   prev_announceText = 'NULL'
   multiCount = 0
   for iter in range(len(AutoscriptsList)):
      if debugVerbosity >= 2: notify("### iter = {}".format(iter))
      selectedAutoscripts = AutoscriptsList[iter]
      timesNothingDone = 0 # A variable that keeps track if we've done any of the autoscripts defined. If none have been coded, we just engage the card.
      X = 0 # Variable for special costs.
      if card.highlight == DummyColor: lingering = ' the lingering effect of' # A text that we append to point out when a player is using a lingering effect in the form of a dummy card.
      else: lingering = ''
      for activeAutoscript in selectedAutoscripts:
         #confirm("Active Autoscript: {}".format(activeAutoscript)) #Debug
         ### Checking if any of the card's effects requires one or more targets first
         if re.search(r'Targeted', activeAutoscript) and findTarget(activeAutoscript) == []: return
      for activeAutoscript in selectedAutoscripts:
         targetC = findTarget(activeAutoscript)
         ### Warning the player in case we need to
         if chkWarn(card, activeAutoscript) == 'ABORT': return
         ### Check if the action needs the player or his opponent to be targeted
         targetPL = ofwhom(activeAutoscript)
         regexTag = re.search(r'ifTagged([0-9]+)', activeAutoscript)
         if regexTag and targetPL.Tags < num(regexTag.group(1)): #See if the target needs to be tagged a specific number of times.
            if regexTag.group(1) == '1': whisper("Your opponent needs to be tagged for you to use this action")
            else: whisper("Your opponent needs to be tagged {} times for you to to use this action".format(regexTag.group(1)))
            return 'ABORT'
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
         if debugVerbosity >= 2: notify("### Entering useAbility() Choice with Autoscript: {}".format(activeAutoscript)) # Debug
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
         else: timesNothingDone += 1
         if debugVerbosity >= 3: notify("<<< useAbility() choice. TXT = {}".format(announceText)) # Debug
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
         if re.search(r"T1:", selectedAutoscripts[0]): 
            executePlayScripts(card,'trash')
            card.moveTo(card.owner.piles['Heap/Archives(Face-up)'])
      if iter == len(AutoscriptsList) - 1: # If this is the last script in the list, then we always announce the script we're running (We reduce by 1 because iterators always start as '0')
         if debugVerbosity >= 2: notify("### Entering last notification")
         if prev_announceText == 'NULL': # If it's NULL it's the only  script we run in this loop, so we just announce.
            notify("{}.".format(announceText)) # Finally announce what the player just did by using the concatenated string.
         else: # If it's not NULL, then there was a script run last time, so we check to see if it's a duplicate
            if prev_announceText == announceText: # If the previous script had the same notification output as the current one, we merge them.
               multiCount += 1
               notify("({}x) {}.".format(multiCount,announceText))
            else: # If the previous script did not have the same output as the current one, we announce them both together.
               if multiCount > 1: notify("({}x) {}.".format(multiCount,prev_announceText)) # If there were multiple versions of the last script used, announce them along with how many there were
               else: notify("{}.".format(prev_announceText))
               notify("{}.".format(announceText)) # Finally we announce the current script's concatenated notification.
      else: #if it's not the last script we run, then we just check if we should announce the previous script or just add another replication.
         if debugVerbosity >= 2: notify("### Entering notification grouping check")
         if prev_announceText == 'NULL': # If it's null, it's the first script we run in this loop...
            multiCount += 1 # ...so we don't announce but rather increase a counter and and just move to the next script, in case it's a duplicate announcement.
            prev_announceText = announceText # We also set the variable we're going to check in the next iteration, to see if it's a duplicate announcement.
         else:
            if prev_announceText == announceText: # If the previous script had the same notification output as the current one...
               multiCount += 1 # ...we merge them and continue without announcing.
            else: # If the previous script did not have the same notification output as the current one, we announce the previous one.
               if multiCount > 1: notify("({}x) {}.".format(multiCount,prev_announceText)) # If there were multiple versions of the last script used, announce them along with how many there were
               else: notify("{}.".format(prev_announceText)) 
               multiCount = 1 # We reset the counter so that we start counting how many duplicates of the current script we're going to have in the future.
               prev_announceText = announceText # And finally we reset the variable holding the previous script.
      chkNoisy(card)
      gatheredCardList = False  # We set this variable to False, so that reduceCost() calls from other functions can start scanning the table again.

#------------------------------------------------------------------------------
# Other Player trigger
#------------------------------------------------------------------------------
   
def autoscriptOtherPlayers(lookup, origin_card = Identity, count = 1): # Function that triggers effects based on the opponent's cards.
# This function is called from other functions in order to go through the table and see if other players have any cards which would be activated by it.
# For example a card that would produce credits whenever a trace was attempted. 
   if not Automations['Triggers']: return
   if debugVerbosity >= 1: notify(">>> autoscriptOtherPlayers() with lookup: {}".format(lookup)) #Debug
   if debugVerbosity >= 3: notify("### origin_card = {}".format(origin_card)) #Debug
   if not Automations['Play, Score and Rez']: return # If automations have been disabled, do nothing.
   for card in table:
      if debugVerbosity >= 2: notify('Checking {}'.format(card)) # Debug
      if not card.isFaceUp: continue # Don't take into accounts cards that are not rezzed.
      costText = '{} activates {} to'.format(card.controller, card) 
      Autoscripts = CardsAS.get(card.model,'').split('||')
      if debugVerbosity >= 4: notify("### {}'s AS: {}".format(card,Autoscripts)) # Debug
      AutoScriptSnapshot = list(Autoscripts)
      for autoS in AutoScriptSnapshot: # Checking and removing anything other than whileRezzed or whileScored.
         if not re.search(r'while(Rezzed|Scored|Running)', autoS): Autoscripts.remove(autoS)
         elif re.search(r'whileRunning', autoS) and not re.search(r'running',getGlobalVariable('status')): Autoscripts.remove(autoS) # Some autoscripted abilities only work while a run is in progress (e.g. Spinal Modem.)
      if len(Autoscripts) == 0: continue
      for AutoS in Autoscripts:
         if debugVerbosity >= 2: notify('Checking AutoS: {}'.format(AutoS)) # Debug
         if not re.search(r'{}'.format(lookup), AutoS): continue # Search if in the script of the card, the string that was sent to us exists. The sent string is decided by the function calling us, so for example the ProdX() function knows it only needs to send the 'GeneratedSpice' string.
         if chkPlayer(AutoS, card.controller,False) == 0: continue # Check that the effect's origninator is valid.
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue # If the card's ability is only once per turn, use it or silently abort if it's already been used
         if not checkCardRestrictions(gatherCardProperties(origin_card), prepareRestrictions(autoS)): continue #If we have the '-type' modulator in the script, then need ot check what type of property it's looking for
         if re.search(r'onTriggerCard',autoS): targetCard = [origin_card] # if we have the "-onTriggerCard" modulator, then the target of the script will be the original card (e.g. see Grimoire)
         else: targetCard = None
         if debugVerbosity >= 2: notify("### Automatic Autoscripts: {}".format(AutoS)) # Debug
         #effect = re.search(r'\b([A-Z][A-Za-z]+)([0-9]*)([A-Za-z& ]*)\b([^:]?[A-Za-z0-9_&{} -]*)', AutoS)
         #passedScript = "{}".format(effect.group(0))
         #confirm('effects: {}'.format(passedScript)) #Debug
         if regexHooks['GainX'].search(AutoS):
            gainTuple = GainX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count)
            if gainTuple == 'ABORT': break
         elif regexHooks['TokensX'].search(AutoS): 
            if TokensX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['TransferX'].search(AutoS): 
            if TransferX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['InflictX'].search(AutoS):
            if InflictX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
         elif regexHooks['DrawX'].search(AutoS):
            if DrawX(AutoS, costText, card, targetCard, notification = 'Automatic', n = count) == 'ABORT': break
   if debugVerbosity >= 3: notify("<<< autoscriptOtherPlayers()") # Debug

#------------------------------------------------------------------------------
# Start/End of Turn/Run trigger
#------------------------------------------------------------------------------
   
def atTimedEffects(Time = 'Start'): # Function which triggers card effects at the start or end of the turn.
   mute()
   if debugVerbosity >= 1: notify(">>> atTimedEffects() at time: {}".format(Time)) #Debug
   global failedRequirement
   failedRequirement = False
   if not Automations['Start/End-of-Turn']: return
   TitleDone = False
   AlternativeRunResultUsed = False # Used for SuccessfulRun effects which replace the normal effect of running a server. If set to True, then no more effects on that server will be processed (to avoid 2 bank jobs triggering at the same time for example).
   X = 0
   for card in table:
      #if card.controller != me: continue # Obsoleted. Using the chkPlayer() function below
      if card.highlight == InactiveColor or card.highlight == RevealedColor: continue
      if not card.isFaceUp: continue
      Autoscripts = CardsAS.get(card.model,'').split('||')
      for autoS in Autoscripts:
         if debugVerbosity >= 3: notify("### Processing {} Autoscript: {}".format(card, autoS))
         if Time == 'Run': effect = re.search(r'at(Run)Start:(.*)', autoS) # Putting Run in a group, only to retain the search results groupings later
         elif Time == 'JackOut': effect = re.search(r'at(JackOut):(.*)', autoS) # Same as above
         elif Time == 'SuccessfulRun': effect = re.search(r'at(SuccessfulRun):(.*)', autoS) # Same as above
         else: effect = re.search(r'atTurn(Start|End):(.*)', autoS) #Putting "Start" or "End" in a group to compare with the Time variable later
         if not effect: continue
         if debugVerbosity >= 3: notify("### Time maches. Script triggers on: {}".format(effect.group(1)))
         if re.search(r'-ifSuccessfulRun', autoS):
            if Time == 'SuccessfulRun': #If we're looking only for successful runs, we need the Time to be a successful run.
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
               if debugVerbosity >= 3: notify("### All checked OK")
            else: continue
         if chkPlayer(effect.group(2), card.controller,False) == 0: continue # Check that the effect's origninator is valid. 
         if effect.group(1) != Time: continue # If the effect trigger we're checking (e.g. start-of-run) does not match the period trigger we're in (e.g. end-of-turn)
         if debugVerbosity >= 3: notify("### split Autoscript: {}".format(autoS))
         if debugVerbosity >= 2 and effect: notify("!!! effects: {}".format(effect.groups()))
         if re.search(r'excludeDummy', autoS) and card.highlight == DummyColor: continue
         if re.search(r'onlyforDummy', autoS) and card.highlight != DummyColor: continue
         if re.search(r'isAlternativeRunResult', effect.group(2)) and AlternativeRunResultUsed: continue # If we're already used an alternative run result and this card has one as well, ignore it
         if re.search(r'isOptional', effect.group(2)):
            extraCountersTXT = '' 
            for cmarker in card.markers: # If the card has any markers, we mention them do that the player can better decide which one they wanted to use (e.g. multiple bank jobs)
               extraCountersTXT += " {}x {}\n".format(card.markers[cmarker],cmarker[0])
            if extraCountersTXT != '': extraCountersTXT = "\n\nThis card has the following counters on it\n" + extraCountersTXT
            if not confirm("{} can have its optional ability take effect at this point. Do you want to activate it?{}".format(fetchProperty(card, 'name'),extraCountersTXT)): continue         
         if re.search(r'isAlternativeRunResult', effect.group(2)): AlternativeRunResultUsed = True # If the card has an alternative result to the normal access for a run, mark that we've used it.         
         if re.search(r'onlyOnce',autoS) and oncePerTurn(card, silent = True, act = 'automatic') == 'ABORT': continue
         splitAutoscripts = effect.group(2).split('$$')
         for passedScript in splitAutoscripts:
            if not TitleDone: 
               if Time == 'Run': title = "{}'s Start-of-Run Effects".format(me)
               elif Time == 'JackOut': title = "{}'s Jack-Out Effects".format(me)
               elif Time == 'SuccessfulRun': title = "{}'s Successful Run Effects".format(me)
               else: title = "{}'s {}-of-Turn Effects".format(me,effect.group(1))
               notify("{:=^36}".format(title))
            TitleDone = True
            if debugVerbosity >= 2: notify("### passedScript: {}".format(passedScript))
            if card.highlight == DummyColor: announceText = "{}'s lingering effects:".format(card)
            else: announceText = "{} triggers to".format(card)
            if regexHooks['GainX'].search(passedScript):
               gainTuple = GainX(passedScript, announceText, card, notification = 'Automatic', n = X)
               if gainTuple == 'ABORT': break
               X = gainTuple[1] 
            elif regexHooks['TransferX'].search(passedScript):
               if TransferX(passedScript, announceText, card, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['DrawX'].search(passedScript):
               if DrawX(passedScript, announceText, card, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['RollX'].search(passedScript):
               rollTuple = RollX(passedScript, announceText, card, notification = 'Automatic', n = X)
               if rollTuple == 'ABORT': break
               X = rollTuple[1] 
            elif regexHooks['TokensX'].search(passedScript):
               if TokensX(passedScript, announceText, card, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['InflictX'].search(passedScript):
               if InflictX(passedScript, announceText, card, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['ModifyStatus'].search(passedScript):
               if ModifyStatus(passedScript, announceText, card, notification = 'Automatic', n = X) == 'ABORT': break
            elif regexHooks['DiscardX'].search(passedScript): 
               discardTuple = DiscardX(passedScript, announceText, card, notification = 'Automatic', n = X)
               if discardTuple == 'ABORT': break
               X = discardTuple[1] 
            elif regexHooks['RequestInt'].search(passedScript): 
               numberTuple = RequestInt(passedScript, announceText, card) # Returns like reshuffleX()
               if numberTuple == 'ABORT': break
               X = numberTuple[1] 
            elif regexHooks['CustomScript'].search(passedScript):
               if CustomScript(card, action = 'Turn{}'.format(Time)) == 'ABORT': break
            if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
   markerEffects(Time) 
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
                                             \nWelcome back Err:::[Segmentation Fault]. Would you like to see today's priority item? Y/N:\
                                          \n\n(If you select 'No', you'll be able to continue with this action later by pressing [Ctrl]+[Q].)"):
         HQaccess(silent = True)
      if currentRunTarget == 'R&D' and confirm("Processing Sec. Token...OK. Access to R&D files authorized for user {}.\nProceed? Y/N:\
                                            \n\n(If you select 'No', you'll be able to continue with this action later by pressing [Ctrl]+[A].)".format(me.name)):
         RDaccessX()
      if currentRunTarget == 'Archives' and confirm("Authorization for user {} processed. Decrypting Archive Store...OK.\nProceed? Y/N:\
                                                \n\n(If you select 'No', you'll be able to continue with this action later by pressing [Ctrl]+[H].)".format(me.name)):
         ARCscore()
   if TitleDone: notify(":::{:=^30}:::".format('='))   
   if debugVerbosity >= 3: notify("<<< atTimedEffects()") # Debug

def markerEffects(Time = 'Start'):
   if debugVerbosity >= 1: notify(">>> markerEffects() at time: {}".format(Time)) #Debug
### Following is not yet implemented. It's from Netrunner classic. Commented out just in case I need it.
#   CounterHold = getSpecial('Identity')
   ### Checking triggers from markers in our own Counter Hold.
#   for marker in CounterHold.markers: # Not used in ANR (yet)
#      count = CounterHold.markers[marker]
#      if debugVerbosity >= 3: notify("### marker: {}".format(marker[0])) # Debug
#      if re.search(r'virusScaldan',marker[0]) and Time == 'Start':
#         total = 0
#         for iter in range(count):
#            rollTuple = RollX('Roll1Dice', 'Scaldan virus:', CounterHold, notification = 'Automatic')
#            if rollTuple[1] >= 5: total += 1
#         me.counters['Bad Publicity'].value += total
#         if total: notify("--> {} receives {} Bad Publicity due to their Scaldan virus infestation".format(me,total))
#      if re.search(r'virusSkivviss',marker[0]) and Time == 'Start':
#         passedScript = 'Draw{}Cards'.format(count)
#         DrawX(passedScript, "Skivviss virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'virusTax',marker[0]) and Time == 'Start':
#         GainX('Lose1Credits-perMarker{virusTax}-div2', "Tax virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'Doppelganger',marker[0]) and Time == 'Start':
#         GainX('Lose1Credits-perMarker{Doppelganger}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'virusPipe',marker[0]) and Time == 'Start':
#         passedScript = 'Infect{}forfeitCounter:Clicks'.format(count)
#         TokensX(passedScript, "Pipe virus:", CounterHold, notification = 'Automatic')
#      if re.search(r'Data Raven',marker[0]) and Time == 'Start':
#         GainX('Gain1Tags-perMarker{Data Raven}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Mastiff',marker[0]) and Time == 'Run':
#         InflictX('Inflict1BrainDamage-perMarker{Mastiff}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Cerberus',marker[0]) and Time == 'Run':
#         InflictX('Inflict2NetDamage-perMarker{Cerberus}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#      if re.search(r'Baskerville',marker[0]) and Time == 'Run':
#         InflictX('Inflict2NetDamage-perMarker{Baskerville}', "{}:".format(marker[0]), CounterHold, notification = 'Automatic')
#   targetPL = ofwhom('-ofOpponent')          
   ### Checking triggers from markers in opponent's Counter Hold.
#   CounterHold = getSpecial('Identity', targetPL) # Some viruses also trigger on our opponent's turns
#   for marker in CounterHold.markers:
#      count = CounterHold.markers[marker]
#      if marker == mdict['virusButcherBoy'] and Time == 'Start':
#         GainX('Gain1Credits-onOpponent-perMarker{virusButcherBoy}-div2', "Opponent's Butcher Boy virus:", OpponentCounterHold, notification = 'Automatic')
   ### Checking triggers from markers the rest of our cards.
   cardList = [c for c in table if c.markers]
   for card in cardList:
      for marker in card.markers:
         if re.search(r'Tinkering',marker[0]) and Time == 'End':
            TokensX('Remove1Keyword:Code Gate', "Tinkering:", card)
            TokensX('Remove1Keyword:Sentry', "Tinkering:", card)
            TokensX('Remove1Keyword:Barrier', "Tinkering:", card)
            TokensX('Remove1Tinkering', "Tinkering:", card)
            notify("--> {} removes tinkering effect from {}".format(me,card))
         if re.search(r'Cortez Chip',marker[0]) and Time == 'End':
            TokensX('Remove1Cortez Chip', "Cortez Chip:", card)
            notify("--> {} removes Cortez Chip effect from {}".format(me,card))
   
#------------------------------------------------------------------------------
# Post-Trace Trigger
#------------------------------------------------------------------------------

def executeTraceEffects(card,Autoscript):
   if debugVerbosity >= 1: notify(">>> executeTraceEffects(){}".format(extraASDebug(Autoscript))) #Debug
   global failedRequirement
   failedRequirement = False
   X = 0
   Autoscripts = Autoscript.split('||')
   for autoS in Autoscripts:
      selectedAutoscripts = autoS.split('++')
      if debugVerbosity >= 2: notify ('### selectedAutoscripts: {}'.format(selectedAutoscripts)) # Debug
      for passedScript in selectedAutoscripts: X = redirect(passedScript, card, 'Quick', X)
      if failedRequirement: break # If one of the Autoscripts was a cost that couldn't be paid, stop everything else.
            
def redirect(Autoscript, card, notificationType = 'Quick', X = 0):
   if debugVerbosity >= 1: notify(">>> redirect(){}".format(extraASDebug(Autoscript))) #Debug
   if re.search(r':Pass\b', Autoscript): return # Pass is a simple command of doing nothing ^_^
   targetC = findTarget(Autoscript)
   targetPL = ofwhom(Autoscript,card.controller) # So that we know to announce the right person the effect, affects.
   announceText = "{} uses {}'s ability to".format(targetPL,card) 
   if debugVerbosity >= 3: notify("#### targetC: {}".format(targetC)) # Debug
   if regexHooks['GainX'].search(Autoscript):
      gainTuple = GainX(Autoscript, announceText, card, notificationType, n = X)
      if gainTuple == 'ABORT': return
      X = gainTuple[1] 
   elif regexHooks['CreateDummy'].search(Autoscript): 
      if CreateDummy(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['DrawX'].search(Autoscript): 
      if DrawX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['TokensX'].search(Autoscript): 
      if TokensX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['RollX'].search(Autoscript): 
      rollTuple = RollX(Autoscript, announceText, card, targetC, notificationType, n = X)
      if rollTuple == 'ABORT': return
      X = rollTuple[1] 
   elif regexHooks['RequestInt'].search(Autoscript): 
      numberTuple = RequestInt(Autoscript, announceText, card, targetC, notificationType, n = X)
      if numberTuple == 'ABORT': return
      X = numberTuple[1] 
   elif regexHooks['DiscardX'].search(Autoscript): 
      discardTuple = DiscardX(Autoscript, announceText, card, targetC, notificationType, n = X)
      if discardTuple == 'ABORT': return
      X = discardTuple[1] 
   elif regexHooks['RunX'].search(Autoscript): 
      if RunX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['TraceX'].search(Autoscript): 
      if TraceX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['ReshuffleX'].search(Autoscript): 
      reshuffleTuple = ReshuffleX(Autoscript, announceText, card, targetC, notificationType, n = X)
      if reshuffleTuple == 'ABORT': return
      X = reshuffleTuple[1]
   elif regexHooks['ShuffleX'].search(Autoscript): 
      if ShuffleX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['ChooseKeyword'].search(Autoscript): 
      if ChooseKeyword(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['InflictX'].search(Autoscript): 
      if InflictX(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['ModifyStatus'].search(Autoscript): 
      if ModifyStatus(Autoscript, announceText, card, targetC, notificationType, n = X) == 'ABORT': return
   elif regexHooks['SimplyAnnounce'].search(Autoscript):
      SimplyAnnounce(Autoscript, announceText, card, targetC, notificationType, n = X)
   elif debugVerbosity >= 1: notify("#### No regexhook match! :(") # Debug
   if debugVerbosity >= 2: notify("### Loop for scipt {} finished".format(Autoscript))
   return X

#------------------------------------------------------------------------------
# Core Commands
#------------------------------------------------------------------------------
   
def GainX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0, actionType = 'USE'): # Core Command for modifying counters or global variables
   if debugVerbosity >= 1: notify(">>> GainX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global maxClicks, lastKnownNrClicks
   gain = 0
   extraText = ''
   reduction = 0
   action = re.search(r'\b(Gain|Lose|SetTo)([0-9]+)([A-Z][A-Za-z &]+)-?', Autoscript)
   if debugVerbosity >= 2: notify("### action groups: {}. Autoscript: {}".format(action.groups(0),Autoscript)) # Debug
   gain += num(action.group(2))
   targetPL = ofwhom(Autoscript, card.controller)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   if re.search(r'ifTagged', Autoscript) and targetPL.Tags == 0:
      whisper("Your opponent needs to be tagged to use this action")
      return 'ABORT'
   multiplier = per(Autoscript, card, n, targetCards) # We check if the card provides a gain based on something else, such as favour bought, or number of dune fiefs controlled by rivals.
   if debugVerbosity >= 3: notify("### GainX() after per") #Debug
   if action.group(1) == 'Lose': 
      if action.group(3) == 'Credits' or action.group(3) == 'Agenda Points' or action.group(3) == 'Clicks' or action.group(3) == 'MU' or action.group(3) == 'Base Link' or action.group(3) == 'Bad Publicity' or action.group(3) == 'Tags' or action.group(3) == 'Hand Size':
         overcharge = (gain * multiplier) - targetPL.counters[action.group(3)].value  # we use this to calculate how much of the requested LoseX was used.
         if debugVerbosity >= 4: notify("#### We have an overcharge of {}".format(overcharge))
         if overcharge < 0: overcharge = 0 # But if the overcharge is 0 or less, it means that all the loss could be taken out.
      else: overcharge = 0
      gain *= -1
      if debugVerbosity >= 2: notify("#### overcharge = {}\n#### Gain = {}.\n #### Multiplier = {}.\n#### Counter = {}".format(overcharge,gain,multiplier,targetPL.counters[action.group(3)].value))
   if re.search(r'ifNoisyOpponent', Autoscript) and targetPL.getGlobalVariable('wasNoisy') != '1': return announceText # If our effect only takes place when our opponent has been noisy, and they haven't been, don't do anything. We return the announcement so that we don't crash the parent function expecting it
   gainReduce = findCounterPrevention(gain * multiplier, action.group(3), targetPL) # If we're going to gain counter, then we check to see if we have any markers which might reduce the cost.
   #confirm("multiplier: {}, gain: {}, reduction: {}".format(multiplier, gain, gainReduce)) # Debug
   if re.match(r'Credits', action.group(3)): # Note to self: I can probably comprress the following, by using variables and by putting the counter object into a variable as well.
      if action.group(1) == 'SetTo': targetPL.counters['Credits'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Credits'].value = 0
      else: 
         if re.search(r'isCost', Autoscript) and action.group(1) == 'Lose':
            if debugVerbosity >= 2: notify("#### Checking Cost Reduction")
            reduction = reduceCost(card, actionType, gain * multiplier)
            targetPL.counters['Credits'].value += (gain * multiplier) + reduction
            if reduction > 0: extraText = ' (Reduced by {})'.format(uniCredit(reduction))
            elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
         else: targetPL.counters['Credits'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Credits'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Credits'].value = 0
   elif re.match(r'Agenda Points', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Agenda Points'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Agenda Points'].value = 0
      else: targetPL.counters['Agenda Points'].value += (gain * multiplier) - gainReduce
      if me.counters['Agenda Points'].value >= 7: 
         notify("{} wins the game!".format(me))
         reportGame()      
      if targetPL.counters['Agenda Points'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Agenda Points'].value = 0
   elif re.match(r'Clicks', action.group(3)): 
      if action.group(1) == 'SetTo': 
         targetPL.Clicks = 0 # If we're setting to a specific value, we wipe what it's currently.
         lastKnownNrClicks = 0
      if gain == -999: 
         targetPL.Clicks = 0
         lastKnownNrClicks = 0
      else: 
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
   elif re.match(r'Bad Publicity', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Bad Publicity'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.counters['Bad Publicity'].value = 0
      else: targetPL.counters['Bad Publicity'].value += (gain * multiplier) - gainReduce
      if targetPL.counters['Bad Publicity'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.counters['Bad Publicity'].value = 0
   elif re.match(r'Tags', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.Tags = 0 # If we're setting to a specific value, we wipe what it's currently.
      if gain == -999: targetPL.Tags = 0
      else: targetPL.Tags += (gain * multiplier) - gainReduce
      if targetPL.Tags < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(targetPL,action.group(3)))
         elif re.search(r'isPenalty', Autoscript): pass #If an action is marked as penalty, it means that the value can go negative and the player will have to recover that amount.
         else: targetPL.Tags = 0
   elif re.match(r'Max Click', action.group(3)): 
      if targetPL == me: 
         if action.group(1) == 'SetTo': maxClicks = 0 # If we're setting to a specific value, we wipe what it's currently.
         maxClicks += gain * multiplier
      else: notify("--> {} loses {} clicks maximum. They must make this modification manually".format(targetPL,gain * multiplier))
   elif re.match(r'Hand Size', action.group(3)): 
      if action.group(1) == 'SetTo': targetPL.counters['Hand Size'].value = 0 # If we're setting to a specific value, we wipe what it's currently.
      targetPL.counters['Hand Size'].value += gain * multiplier
      if targetPL.counters['Hand Size'].value < 0: 
         if re.search(r'isCost', Autoscript): notify(":::Warning:::{} did not have enough {} to pay the cost of this action".format(action.group(3)))
         else: targetPL.counters['Hand Size'].value = 0
   else: 
      whisper("Gain what?! (Bad autoscript)")
      return 'ABORT'
   if debugVerbosity >= 2: notify("### Gainx() Finished counter manipulation")
   if notification != 'Automatic': # Since the verb is in the middle of the sentence, we want it lowercase.
      if action.group(1) == 'Gain': verb = 'gain'
      elif action.group(1) == 'Lose': 
         if re.search(r'isCost', Autoscript): verb = 'pay'
         else: verb = 'lose'
      else: verb = 'set to'
   else: verb = action.group(1) # Automatic notifications start with the verb, so it needs to be capitaliszed. 
   if abs(gain) == abs(999): total = 'all' # If we have +/-999 as the count, then this mean "all" of the particular counter.
   elif action.group(1) == 'Lose' and re.search(r'isCost', Autoscript): total = abs(gain * multiplier)
   elif action.group(1) == 'Lose' and not re.search(r'isPenalty', Autoscript): total = abs(gain * multiplier) - overcharge - reduction
   else: total = abs(gain * multiplier) - reduction# Else it's just the absolute value which we announce they "gain" or "lose"
   closureTXT = ASclosureTXT(action.group(3), total)
   if debugVerbosity >= 2: notify("### Gainx() about to announce")
   if notification == 'Quick': announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraText)
   else: announceString = "{}{} {} {}{}".format(announceText, otherTXT, verb, closureTXT,extraText)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< Gain() total: {}".format(total))
   return (announceString,total)
   
def TransferX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for converting tokens to counter values
   if debugVerbosity >= 1: notify(">>> TransferX(){}".format(extraASDebug(Autoscript))) #Debug
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
   if debugVerbosity >= 3: notify("!!! regex groups: {}".format(action.groups())) #Debug   
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
   elif notification == 'Automatic': announceString = "{} Transfers {} to {}{}".format(announceText, closureTXT, me, reduceTXT)
   else: announceString = "{} take {} from {}{}".format(announceText, closureTXT, targetCardlist,reduceTXT)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< TransferX()")
   return announceString   

def TokensX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for adding tokens to cards
   if debugVerbosity >= 1: notify(">>> TokensX(){}".format(extraASDebug(Autoscript))) #Debug
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
         victim = ofwhom(Autoscript, card.controller)
         if targetCards[0] == card: targetCards[0] = getSpecial('Identity',victim)
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
   count = num(action.group(2))
   multiplier = per(Autoscript, card, n, targetCards, notification)
   for targetCard in targetCards:
      #confirm("TargetCard ID: {}".format(targetCard._id)) # Debug
      if action.group(1) == 'Put': modtokens = count * multiplier
      elif action.group(1) == 'Refill': modtokens = count - targetCard.markers[token]
      elif action.group(1) == 'Infect':
         targetCardlist = '' #We don't want to mention the target card for infections. It's always the same.
         victim = ofwhom(Autoscript, card.controller)
         if targetCard == card: targetCard = getSpecial('Identity',victim) # For infecting targets, the target is never the card causing the effect.
         modtokens = count * multiplier
         if re.search('virus',token[0]) and token != mdict['protectionVirus']: # We don't want us to prevent putting virus protection tokens, even though we put them with the "Infect" keyword.
            Virusprevented = findVirusProtection(targetCard, victim, modtokens)
            if Virusprevented > 0:
               preventTXT = ' ({} prevented)'.format(Virusprevented)
               modtokens -= Virusprevented
         infectTXT = ' {} with'.format(victim)
         #notify("Token is {}".format(token[0])) # Debug
      elif action.group(1) == 'USE':
         if not targetCard.markers[token] or count > targetCard.markers[token]: 
            whisper("There's not enough counters left on the card to use this ability!")
            return 'ABORT'
         else: modtokens = -count * multiplier
      else: #Last option is for removing tokens.
         if count == 999: # 999 effectively means "all markers on card"
            if action.group(3) == 'BrainDMG': # We need to remove brain damage from the Identity
               targetCardlist = ''
               victim = ofwhom(Autoscript, card.controller)
               if not targetCard or targetCard == card: targetCard = getSpecial('Identity',victim)
               if targetCard.markers[token]: count = targetCard.markers[token]
               else: count = 0
               #confirm("count: {}".format(count)) # Debug
            elif targetCard.markers[token]: count = targetCard.markers[token]
            else: 
               delayed_whisper("There was nothing to remove.")
               count = 0
         elif re.search(r'isCost', Autoscript) and (not targetCard.markers[token] or (targetCard.markers[token] and count > targetCard.markers[token])):
            if notification != 'Automatic': whisper ("No markers to remove. Aborting!") #Some end of turn effect put a special counter and then remove it so that they only run for one turn. This avoids us announcing that it doesn't have markers every turn.
            return 'ABORT'
         elif not targetCard.markers[token]: 
            whisper("There was nothing to remove.")        
            count = 0 # If we don't have any markers, we have obviously nothing to remove.
         modtokens = -count * multiplier
      targetCard.markers[token] += modtokens # Finally we apply the marker modification
   if abs(num(action.group(2))) == abs(999): total = 'all'
   else: total = abs(modtokens)
   if re.search(r'isPriority', Autoscript): card.highlight = PriorityColor
   if action.group(1) == 'Refill': 
      if token[0] == 'Credit': 
         announceString = "{} {} to {}".format(announceText, action.group(1), uniRecurring(count)) # We need a special announcement for refill, since it always needs to point out the max.
      else: 
         announceString = "{} {} to {} {}".format(announceText, action.group(1), count, token[0]) # We need a special announcement for refill, since it always needs to point out the max.
   elif re.search(r'forfeitCounter:',action.group(3)):
      counter = re.search(r'forfeitCounter:(\w+)',action.group(3))
      if not victim or victim == me: announceString = '{} forfeit their next {} {}'.format(announceText,total,counter.group(1)) # If we're putting on forfeit counters, we don't announce it as an infection.
      else: announceString = '{} force {} to forfeit their next {} {}'.format(announceText, victim, total,counter.group(1))
   else: announceString = "{} {}{} {} {} counters{}{}".format(announceText, action.group(1).lower(),infectTXT, total, token[0],targetCardlist,preventTXT)
   if notification and modtokens != 0 and not re.search(r'isSilent', Autoscript): notify('--> {}.'.format(announceString))
   if debugVerbosity >= 2: notify("### TokensX() String: {}".format(announceString)) #Debug
   if debugVerbosity >= 3: notify("<<< TokensX()")
   if re.search(r'isSilent', Autoscript): return announceText # If it's a silent marker, we don't want to announce anything. Returning the original announceText will be processed by any receiving function as having done nothing.
   else: return announceString
 
def DrawX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DrawX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   destiVerb = 'draw'
   action = re.search(r'\bDraw([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
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
   if debugVerbosity >= 2: notify("### About to announce.")
   if count == 0: return announceText # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} draws {} cards".format(announceText, count)
   elif targetPL == me: announceString = "{} {} {} cards from their {}{}".format(announceText, destiVerb, count, pileName(source), destPath)
   else: announceString = "{} {} {} cards from {}'s {}".format(announceText, destiVerb, count, targetPL, pileName(source), destPath)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< DrawX()")
   return announceString

def DiscardX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> DiscardX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bDiscard([0-9]+)Card', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if targetPL != me: otherTXT = ' force {} to'.format(targetPL)
   else: otherTXT = ''
   discardNR = num(action.group(1))
   if discardNR == 999:
      multiplier = 1
      discardNR = len(targetPL.hand) # 999 means we discard our whole hand
   else: # Any other number just discard as many cards at random.
      multiplier = per(Autoscript, card, n, targetCards, notification)
      count = handRandomDiscard(targetPL.hand, discardNR * multiplier, targetPL, silent = True)
      if re.search(r'isCost', Autoscript) and count < discardNR:
         whisper("You do not have enough cards in your hand to discard")
         return ('ABORT',0)
   if count == 0: return (announceText,count) # If there are no cards, then we effectively did nothing, so we don't change the notification.
   if notification == 'Quick': announceString = "{} discards {} cards".format(announceText, count)
   else: announceString = "{}{} discard {} cards from their hand".format(announceText,otherTXT, count)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< DiscardX()")
   return (announceString,count)
         
def ReshuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ReshuffleX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   mute()
   X = 0
   targetPL = ofwhom(Autoscript, card.controller)
   action = re.search(r'\bReshuffle([A-Za-z& ]+)', Autoscript)
   if debugVerbosity >= 1: notify("!!! regex: {}".format(action.groups())) # Debug
   if action.group(1) == 'HQ' or action.group(1) == 'Stack':
      namestuple = groupToDeck(targetPL.hand, targetPL , True) # We do a silent hand reshuffle into the deck, which returns a tuple
      X = namestuple[2] # The 3rd part of the tuple is how many cards were in our hand before it got shuffled.
   elif action.group(1) == 'Archives' or action.group(1) == 'Trash':
      if targetPL.getGlobalVariable('ds') == "corp": groupToDeck(targetPL.piles['Archives(Hidden)'], targetPL , True)
      namestuple = groupToDeck(targetPL.piles['Heap/Archives(Face-up)'], targetPL, True)    
   else: 
      whisper("Wat Group? [Error in autoscript!]")
      return 'ABORT'
   shuffle(targetPL.piles['R&D/Stack'])
   if notification == 'Quick': announceString = "{} shuffles their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   else: announceString = "{} shuffle their {} into their {}".format(announceText, namestuple[0], namestuple[1])
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ReshuffleX() return with X = {}".format(X))
   return (announceString, X)

def ShuffleX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # A Core Command for reshuffling a pile into the R&D/Stack
   if debugVerbosity >= 1: notify(">>> ShuffleX(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   mute()
   action = re.search(r'\bShuffle([A-Za-z& ]+)', Autoscript)
   targetPL = ofwhom(Autoscript, card.controller)
   if action.group(1) == 'Trash' or action.group(1) == 'Archives': pile = targetPL.piles['Heap/Archives(Face-up)']
   elif action.group(1) == 'Stack' or action.group(1) == 'R&D': pile = targetPL.piles['R&D/Stack']
   elif action.group(1) == 'Hidden Archives': pile = targetPL.piles['Archives(Hidden)']
   random = rnd(10,100) # Small wait (bug workaround) to make sure all animations are done.
   shuffle(pile)
   if notification == 'Quick': announceString = "{} shuffles their {}".format(announceText, pile.name)
   elif targetPL == me: announceString = "{} shuffle their {}".format(announceText, pile.name)
   else: announceString = "{} shuffle {}' {}".format(announceText, targetPL, pile.name)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ShuffleX()")
   return announceString
   
def RollX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RollX(){}".format(extraASDebug())) #Debug
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
      if debugVerbosity >= 2: notify("### iter:{} with roll {} and total result: {}".format(d,d6,result))
   if notification == 'Quick': announceString = "{} rolls {} on {} dice".format(announceText, d6list, count)
   else: announceString = "{} roll {} dice with the following results: {}".format(announceText,count, d6list)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< RollX() with result: {}".format(result))
   return (announceString, result)

def RequestInt(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RequestInt(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRequestInt(-Min)?([0-9]*)(-div)?([0-9]*)(-Max)?([0-9]*)(-Msg)?\{?([A-Za-z0-9?$& ]*)\}?', Autoscript)
   if debugVerbosity >= 2:
      if action: notify('!!! regex: {}'.format(action.groups()))
      else: notify("!!! No regex match :(")
   if debugVerbosity >= 2: notify("### Checking for Min")
   if action.group(2): 
      min = num(action.group(2))
      minTXT = ' (minimum {})'.format(min)
   else: 
      min = 0
      minTXT = ''
   if debugVerbosity >= 2: notify("### Checking for Max")
   if action.group(6): 
      max = num(action.group(6))
      minTXT += ' (maximum {})'.format(max)
   else: 
      max = None
   if debugVerbosity >= 2: notify("### Checking for div")
   if action.group(4): 
      div = num(action.group(4))
      minTXT += ' (must be a multiple of {})'.format(div)
   else: div = 1
   if debugVerbosity >= 2: notify("### Checking for Msg")
   if action.group(8): 
      message = action.group(8)
   else: message = "{}:\nThis effect requires that you provide an 'X'. What should that number be?{}".format(fetchProperty(card, 'name'),minTXT)
   number = min - 1
   if debugVerbosity >= 2: notify("### About to ask")
   while number < min or number % div or (max and number > max):
      number = askInteger(message,min)
      if number == None: 
         whisper("Aborting Function")
         return 'ABORT'
   if debugVerbosity >= 3: notify("<<< RequestInt()")
   return (announceText, number) # We do not modify the announcement with this function.
   
def RunX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> RunX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bRun([A-Z][A-Za-z& ]+)', Autoscript)
   if debugVerbosity >= 2: 
      if action: notify("!!! Regex results: {}".format(action.groups()))
      else: notify("!!! No Regex match :(")
   if action.group(1) == 'End':
      jackOut(silent = True)
      if notification == 'Quick': announceString = "{} ends the run".format(announceText)
      else: announceString = "{} end the run".format(announceText)
   else:
      if action.group(1) == 'Generic':
         targets = findTarget('Targeted-atServer')
         if targets == []: # If the player has not targeted a server, then we ask them what they're targeting.
            if debugVerbosity >= 3: notify("### No targets found. Asking")
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
            if debugVerbosity >= 3: notify("### Targeted Server found!")
            if targets[0].name == 'Remote Server': targetServer = 'Remote'
            else: targetServer = targets[0].name
      else: targetServer = action.group(1)
      feint = re.search(r'-feintTo([A-Za-z&]+)', Autoscript)
      if feint:
         setGlobalVariable('feintTarget',feint.group(1)) # If the card script is feinting to a different fort, set a shared variable so that the corp knows it.
      runTarget = ' on {}'.format(targetServer)
      intRun(0,targetServer,True)
      if notification == 'Quick': announceString = "{} starts a run{}".format(announceText, runTarget)
      else: announceString = "{} start a run{}".format(announceText, runTarget)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< RunX()")
   return announceString

def SimplyAnnounce(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> SimplyAnnounce(){}".format(extraASDebug())) #Debug
   if targetCards is None: targetCards = []
   action = re.search(r'\bSimplyAnnounce{([A-Za-z0-9&,\. ]+)}', Autoscript)
   if debugVerbosity >= 2: #Debug
      if action: notify("!!! regex: {}".format(action.groups())) 
      else: notify("!!! regex failed :(") 
   if re.search(r'break',Autoscript) and re.search(r'subroutine',Autoscript): penaltyNoisy(card)
   if notification == 'Quick': announceString = "{} {}".format(announceText, action.group(1))
   else: announceString = "{} {}".format(announceText, action.group(1))
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< SimplyAnnounce()")
   return announceString

def CreateDummy(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for creating dummy cards.
   if debugVerbosity >= 1: notify(">>> CreateDummy(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global Dummywarn
   global Stored_Type, Stored_Cost, Stored_Keywords, Stored_AutoActions, Stored_AutoScripts
   dummyCard = None
   action = re.search(r'\bCreateDummy[A-Za-z0-9_ -]*(-with)(?!onOpponent|-doNotTrash|-nonUnique)([A-Za-z0-9_ -]*)', Autoscript)
   if debugVerbosity >= 3 and action: notify('clicks regex: {}'.format(action.groups())) # debug
   targetPL = ofwhom(Autoscript, card.controller)
   for c in table:
      if c.model == card.model and c.controller == targetPL and c.highlight == DummyColor: dummyCard = c # We check if already have a dummy of the same type on the table.
   if not dummyCard or re.search(r'nonUnique',Autoscript): #Some create dummy effects allow for creating multiple copies of the same card model.
      if Dummywarn and re.search('onOpponent',Autoscript):
         if not confirm("This action creates an effect for your opponent and a way for them to remove it.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nYou opponent can activate any abilities meant for them on the Dummy card. If this card has one, they can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nOnce the   dummy card is on the table, please right-click on it and select 'Pass control to {}'\
                     \n\nDo you want to see this warning again?".format(targetPL)): Dummywarn = False      
      elif Dummywarn:
         if not confirm("This card's effect requires that you trash it, but its lingering effects will only work automatically while a copy is in play.\
                       \nFor this reason we've created a dummy card on the table and marked it with a special highlight so that you know that it's just a token.\
                     \n\nSome cards provide you with an ability that you can activate after they're been trashed. If this card has one, you can activate it by double clicking on the dummy. Very often, this will often remove the dummy since its effect will disappear.\
                     \n\nDo you want to see this warning again?"): Dummywarn = False
      elif re.search(r'onOpponent', Autoscript): information('The dummy card just created is meant for your opponent. Please right-click on it and select "Pass control to {}"'.format(targetPL))
      dummyCard = table.create(card.model, -680, 200 * playerside, 1) # This will create a fake card like the one we just created.
      dummyCard.highlight = DummyColor
      storeProperties(dummyCard)
   #confirm("Dummy ID: {}\n\nList Dummy ID: {}".format(dummyCard._id,passedlist[0]._id)) #Debug
   if not re.search(r'doNotTrash',Autoscript): card.moveTo(card.owner.piles['Heap/Archives(Face-up)'])
   if action: announceString = TokensX('Put{}'.format(action.group(2)), announceText,dummyCard, n = n) # If we have a -with in our autoscript, this is meant to put some tokens on the dummy card.
   else: announceString = announceText + 'create a lingering effect for {}'.format(targetPL)
   if debugVerbosity >= 3: notify("<<< CreateDummy()")
   return announceString # Creating a dummy isn't usually announced.

def ChooseKeyword(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for marking cards to be of a different keyword than they are
   if debugVerbosity >= 1: notify(">>> ChooseKeyword(){}".format(extraASDebug(Autoscript))) #Debug
   #confirm("Reached ChooseKeyword") # Debug
   choiceTXT = ''
   targetCardlist = ''
   existingKeyword = None
   if targetCards is None: targetCards = []
   if len(targetCards) == 0: targetCards.append(card) # If there's been to target card given, assume the target is the card itself.
   for targetCard in targetCards: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   action = re.search(r'\bChooseKeyword{([A-Za-z\| ]+)}', Autoscript)
   #confirm("search results: {}".format(action.groups())) # Debug
   keywords = action.group(1).split('|')
   #confirm("List: {}".format(keywords)) # Debug
   if len(keywords) > 1:
      for i in range(len(keywords)): choiceTXT += '{}: {}\n'.format(i, keywords[i])
      choice = len(keywords)
   else: choice = 0
   while choice > len(keywords) - 1: 
      choice = askInteger("Choose one of the following keywords to assign to this card:\n\n{}".format(choiceTXT),0)
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
         if debugVerbosity >= 1: notify("### Searching for {} in {}".format(keywords[choice],existingKeyword[0])) # Debug               
         if re.search(r'{}'.format(keywords[choice]),existingKeyword[0]): pass # If the keyword is the same as is already there, do nothing.
         else: 
            targetCard.markers[existingKeyword] = 0 
            TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
      else: TokensX('Put1Keyword:{}'.format(keywords[choice]), '', targetCard)
   if notification == 'Quick': announceString = "{} marks {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   else: announceString = "{} mark {} as being {} now".format(announceText, targetCardlist, keywords[choice])
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ChooseKeyword()")
   return announceString
            
def TraceX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for drawing X Cards from the house deck to your hand.
   if debugVerbosity >= 1: notify(">>> TraceX(){}".format(extraASDebug(Autoscript))) #Debug
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
   if debugVerbosity >= 2: notify("### Checking for Trace Effects") #Debug
   if traceEffects:
      traceEffectTuple = (card._id,traceEffects.group(1),traceEffects.group(2))
      if debugVerbosity >= 2: notify("### TraceEffectsTuple: {}".format(traceEffectTuple)) #Debug
      setGlobalVariable('CurrentTraceEffect',str(traceEffectTuple))
   if notification == 'Quick': announceString = "{} starts a Trace with a base strength of {} {}".format(announceText, TraceStrength, reinforceTXT)
   else: announceString = "{} start a trace with a base strength of {} {}".format(announceText, TraceStrength, reinforceTXT)
   if notification: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< TraceX()")
   return announceString

def ModifyStatus(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for modifying the status of a card on the table.
   if debugVerbosity >= 1: notify(">>> ModifyStatus(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   targetCardlist = '' # A text field holding which cards are going to get tokens.
   extraText = ''
   action = re.search(r'\b(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)(Target|Parent|Multi|Myself)[-to]*([A-Z][A-Za-z&_ ]+)?', Autoscript)
   if action.group(2) == 'Myself': 
      del targetCards[:] # Empty the list, just in case.
      targetCards.append(card)
   if action.group(3): dest = action.group(3)
   else: dest = 'hand'
   for targetCard in targetCards: 
      if action.group(1) == 'Derez': 
         targetCardlist += '{},'.format(fetchProperty(targetCard, 'name')) # Derez saves the name because by the time we announce the action, the card will be face down.
      else: targetCardlist += '{},'.format(targetCard)
   targetCardlist = targetCardlist.strip(',') # Re remove the trailing comma
   for targetCard in targetCards:
      if re.search(r'-ifEmpty',Autoscript) and targetCard.markers[mdict['Credits']] and targetCard.markers[mdict['Credits']] > 0: 
         if len(targetCards) > 1: continue #If the modification only happens when the card runs out of credits, then we abort if it still has any
         else: return announceText # If there's only 1 card and it's not supposed to be trashed yet, do nothing.
      if action.group(1) == 'Rez' and intRez(targetCard, cost = 'free', silent = True) != 'ABORT': pass
      elif action.group(1) == 'Derez' and derez(targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Expose': 
         exposeResult = expose(targetCard, silent = True)
         if exposeResult == 'ABORT': return 'ABORT'
         elif exposeResult == 'COUNTERED': extraText = " (Countered!)"
      elif action.group(1) == 'Uninstall' and uninstall(targetCard, destination = dest, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Possess' and possess(card, targetCard, silent = True) != 'ABORT': pass
      elif action.group(1) == 'Trash':
         trashResult = intTrashCard(targetCard, fetchProperty(targetCard,'Stat'), "free", silent = True)
         if trashResult == 'ABORT': return 'ABORT'
         elif trashResult == 'COUNTERED': extraText = " (Countered!)"
      elif action.group(1) == 'Exile' and exileCard(targetCard, silent = True) != 'ABORT': pass
      else: return 'ABORT'
      if action.group(2) != 'Multi': break # If we're not doing a multi-targeting, abort after the first run.
   if notification == 'Quick': announceString = "{} {}es {}{}".format(announceText, action.group(1), targetCardlist,extraText)
   else: announceString = "{} {} {}{}".format(announceText, action.group(1), targetCardlist, extraText)
   if notification and not re.search(r'isSilent', Autoscript): notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< ModifyStatus()")
   if re.search(r'isSilent', Autoscript): return announceText
   else: return announceString
         
def InflictX(Autoscript, announceText, card, targetCards = None, notification = None, n = 0): # Core Command for inflicting Damage to players (even ourselves)
   if debugVerbosity >= 1: notify(">>> InflictX(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   global DMGwarn, failedRequirement
   localDMGwarn = True #A variable to check if we've already warned the player during this damage dealing.
   action = re.search(r'\b(Inflict)([0-9]+)(Meat|Net|Brain)Damage', Autoscript) # Find out what kind of damage we're going
   multiplier = per(Autoscript, card, n, targetCards)
   enhancer = findEnhancements(Autoscript) #See if any of our cards increases damage we deal
   targetPL = ofwhom(Autoscript, card.controller) #Find out who the target is
   if enhancer > 0: enhanceTXT = ' (Enhanced: +{})'.format(enhancer) #Also notify that this is the case
   else: enhanceTXT = ''
   if multiplier == 0 or num(action.group(2)) == 0: DMG = 0 # if we don't do any damage, we don't enhance it
   else: DMG = (num(action.group(2)) * multiplier) + enhancer #Calculate our damage
   preventTXT = ''
   if DMG and Automations['Damage']: #The actual effects happen only if the Damage automation switch is ON. It should be ON by default.
      if DMGwarn and localDMGwarn:
         localDMGwarn = False # We don't want to warn the player for every point of damage.
         if targetPL != me: notify(":::ATTENTION::: {} is about to inflict {} {} Damage to {}!".format(me,DMG,action.group(3),targetPL))
         if not confirm(":::Warning::: You are about to inflict automatic damage!\
                       \nBefore you do that, please make sure that your target is not currently manipulating their hand or this might cause the game to crash.\
                     \n\nImportant: Before proceeding, ask your target to activate any cards they want that add protection against this type of damage. If this is yourself, please make sure you do this before you activate damage effects.\
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
            if targetPL != me: reportGame('FlatlineVictory') # In case of an effect like the Jinteki's ability
            else: reportGame('Flatlined')
            break
         else: #Otherwise, warn the player doing it for the first time
            whisper("+++ Applying damage {} of {}...".format(DMGpt+1,DMG))
            DMGcard = targetPL.hand.random() # Pick a random card from their hand
            if targetPL.getGlobalVariable('ds') == 'corp': DMGcard.moveTo(targetPL.piles['Archives(Hidden)']) # If they're a corp, move it to the hidden archive
            else: DMGcard.moveTo(targetPL.piles['Heap/Archives(Face-up)']) #If they're a runner, move it to trash.
            if action.group(3) == 'Brain':  
               #targetPL.counters['Hand Size'].value -= 1 # If it's brain damage, also reduce the player's maximum handsize.               
               applyBrainDmg(targetPL)
   if targetPL == me: targetPL = 'theirself' # Just changing the announcement to fit better.
   if re.search(r'isRequirement', Autoscript) and DMG < 1: failedRequirement = True # Requirement means that the cost is still paid but other clicks are not going to follow.
   if notification == 'Quick': announceString = "{} suffers {} {} damage{}".format(announceText,DMG,action.group(3),preventTXT)
   else: announceString = "{} inflict {} {} damage{} to {}{}".format(announceText,DMG,action.group(3),enhanceTXT,targetPL,preventTXT)
   if notification and multiplier > 0: notify('--> {}.'.format(announceString))
   if debugVerbosity >= 3: notify("<<< InflictX()")
   return announceString
   
def UseCustomAbility(Autoscript, announceText, card, targetCards = None, notification = None, n = 0):
   if fetchProperty(card, 'name') == "Tollbooth":
      targetPL = ofwhom('ofOpponent')
      global reversePlayerChk
      reversePlayerChk = True
      reduction = reduceCost(card, 'FORCE', 3, True) # We use a dry-run to see if they have a card which card reduce the tollbooth cost such as stimhack
      reversePlayerChk = False
      if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))  
      elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: extraText = ''
      if targetPL.Credits >= 3 - reduction: 
         reversePlayerChk = True
         targetPL.Credits -= 3 - reduceCost(card, 'FORCE', 3)
         reversePlayerChk = False
         announceString = announceText + ' force {} to pay {}{}'.format(targetPL,uniCredit(3),extraText)
      else: 
         jackOut(silent = True)
         announceString = announceText + ' end the run'.format(targetPL,uniCredit(3))   
   return announceString
   
def CustomScript(card, action = 'PLAY'): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   if debugVerbosity >= 1: notify(">>> CustomScript() with action: {}".format(action)) #Debug
   global ModifyDraw
   trash = me.piles['Heap/Archives(Face-up)']
   arcH = me.piles['Archives(Hidden)']
   deck = me.piles['R&D/Stack']
   #confirm("Customscript") # Debug
   if card.model == '23473bd3-f7a5-40be-8c66-7d35796b6031' and action == 'USE': # Virus Scan Special Ability
      clickCost = useClick(count = 3)
      if clickCost == 'ABORT': return
      for c in table: 
         foundMarker = findMarker(c,'Virus')
         if foundMarker: c.markers[foundMarker] = 0
      notify("{} to clean all viruses from their corporate grid".format(clickCost))
   elif card.model == '71a89203-94cd-42cd-b9a8-15377caf4437' and action == 'USE': # Technical Difficulties Special Ability
      knownMarkers = []
      for marker in card.markers:
         if marker[0] in markerRemovals: # If the name of the marker exists in the markerRemovals dictionary it means it can be removed and has a specific cost.
            knownMarkers.append(marker)
      if len(knownMarkers) == 0: 
         whisper("No known markers with ability to remove")
         return
      elif len(knownMarkers) == 1: selectedMarker = knownMarkers[0]
      else: 
         selectTXT = 'Please select a marker to remove\n\n'
         iter = 0
         for choice in knownMarkers:
            selectTXT += '{}: {} ({} {} and {})\n'.format(iter,knownMarkers[iter][0],markerRemovals[choice[0]][0],uniClick(),markerRemovals[choice[0]][1])
            iter += 1
         sel = askInteger(selectTXT,0)
         selectedMarker = knownMarkers[sel]
      aCost = markerRemovals[selectedMarker[0]][0] # The first field in the tuple for the entry with the same name as the selected marker, in the markerRemovals dictionary. All clear? Good.
      cost = markerRemovals[selectedMarker[0]][1]
      clickCost = useClick(count = aCost)
      if clickCost == 'ABORT': return
      creditCost = payCost(cost)
      if creditCost == 'ABORT':
         me.Clicks += aCost # If the player can't pay the cost after all and aborts, we give him his clicks back as well.
         return         
      card.markers[selectedMarker] -= 1
      notify("{} to remove {} for {}.".format(clickCost,selectedMarker[0],creditCost))
   elif fetchProperty(card, 'name') == 'Accelerated Beta Test' and action == 'SCORE':
      if not confirm("Would you like to initiate an accelerated beta test?"): return
      iter = 0
      for c in deck.top(3):
         c.moveTo(arcH)
         loopChk(c,'Type')
         if c.type == 'ICE':
            placeCard(c,'InstallRezzed')
            c.orientation ^= Rot90
            iter +=1
            notify(" -- {} Beta Tested!".format(c))
            autoscriptOtherPlayers('CardInstall',c)
            autoscriptOtherPlayers('CardRezzed',c)
      if iter: # If we found any ice in the top 3
         notify("{} initiates an Accelerated Beta Test and reveals {} Ice from the top of their R&D. These Ice are automatically installed and rezzed".format(me, iter))
      else: notify("{} initiates a Accelerated Beta Test but their beta team was incompetent.".format(me))
   elif fetchProperty(card, 'name') == 'Infiltration' and action == 'PLAY':
      tCards = [c for c in table if c.targetedBy and c.targetedBy == me and c.isFaceUp == False]
      if tCards: expose(tCards[0]) # If the player has any face-down cards currently targeted, we assume he wanted to expose them.
      elif confirm("Do you wish to gain 2 credits?\
                \n\nIf you want to expose a target, simply ask the corp to use the 'Expose' option on the table.\
                \n\nHowever if you have a target selected when you play this card, we will also announce that for you."):
         me.Credits += 2
         notify("--> {} gains {}".format(me,uniCredit(2)))
   elif fetchProperty(card, 'name') == "Rabbit Hole" and action == 'INSTALL':
      if not confirm("Would you like to extend the rabbit hole?"): 
         return
      cardList = [c for c in deck]
      reduction = 0
      rabbits = 0
      totalCost = 0
      for c in cardList: c.moveTo(arcH)
      rnd(1,100)
      if debugVerbosity >= 2: notify("Entering rabbit search loop")
      for c in cardList: 
         if c.model == "bc0f047c-01b1-427f-a439-d451eda01039":
            if debugVerbosity >= 2: notify("found rabbit!")
            storeProperties(c)
            reduction += reduceCost(c, action, num(c.Cost)) #Checking to see if the cost is going to be reduced by cards we have in play.
            rc = payCost(num(c.Cost) - reduction, "not free")
            if rc == "ABORT": break
            else: totalCost += (num(c.Cost) - reduction)
            placeCard(c, action)
            rabbits += 1
            cardList.remove(c)
            if not confirm("Rabbit Hole extended! Would you like to dig deeper?"): break
      for c in cardList: c.moveTo(deck)
      rnd(1,10)
      shuffle(deck)
      if rabbits: # If the player managed to find and install some extra rabbit holes...
         if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.    
         elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
         else: extraText = ''
         me.counters['Base Link'].value += rabbits
         notify("{} has extended the Rabbit Hole by {} {} by paying {}{}".format(me,rabbits,uniLink(),uniCredit(totalCost),extraText))
      else: notify("{} does not find enough rabbits.".format(me))
   elif fetchProperty(card, 'name') == 'Snowflake' and action == 'USE':
      global secretCred
      if secretCred == None:
         secretCred = askInteger("How many credits do you want to secretly spend?\n\nOnce you have selected your total, ask your opponent to spend their own amount visibly, then re-use this card.",0)
         while secretCred and (secretCred > me.Credits) or (secretCred > 2):
            if secretCred > me.Credits and confirm("You do not have that many credits to spend. Bypass?"): break
            if secretCred > 2: warn = ":::ERROR::: You cannot spend more than 2 credits!\n"
            else: warn = ''
            secretCred = askInteger("{}How many credits do you want to secretly spend?".format(warn),0)
         if secretCred != None: notify("{} has spent a hidden amount of credits for {}. Runner must now declare how many credits to spend".format(me,card))
      else: 
         notify("{} has spent {} in secret for {}'s subroutine".format(me,uniCredit(secretCred),card))
         me.Credits -= secretCred
         secretCred = None
   elif action == 'USE': useCard(card)
   if debugVerbosity >= 3: notify("<<< CustomScript()") #Debug
#------------------------------------------------------------------------------
# Helper Functions
#------------------------------------------------------------------------------
   
def chkNoisy(card): # Check if the player successfully used a noisy icebreaker, and if so, give them the consequences...
   if debugVerbosity >= 1: notify(">>> chkNoisy()") #Debug
   if re.search(r'Noisy', fetchProperty(card, 'Keywords')) and re.search(r'Icebreaker', fetchProperty(card, 'Keywords')): 
      me.setGlobalVariable('wasNoisy', '1') # First of all, let all players know of this fact.
      if debugVerbosity >= 2: notify("### Noisy credit Set!") #Debug
   if debugVerbosity >= 3: notify("<<< chkNoisy()") #Debug

def penaltyNoisy(card):
   if debugVerbosity >= 1: notify(">>> penaltyNoisy()") #Debug
   if re.search(r'Noisy', fetchProperty(card, 'Keywords')) and re.search(r'Icebreaker', fetchProperty(card, 'Keywords')): 
      NoisyCost = re.search(r'triggerNoisy([0-9]+)',CardsAS.get(card.model,''))
      if debugVerbosity >= 2: 
         if NoisyCost: notify("### Noisy Trigger Found: {}".format(NoisyCost.group(1))) #Debug      
         else: notify("### Noisy Trigger not found. AS was: {}".format(CardsAS.get(card.model,''))) #Debug      
      if NoisyCost: 
         total = 0
         cost = num(NoisyCost.group(1))
         stealthCards = [c for c in table 
                        if c.controller == me
                        and c.isFaceUp
                        and re.search(r'Stealth',getKeywords(c))
                        and c.markers[mdict['Credits']]]
         if debugVerbosity >= 2: notify("{} cards found".format(len(stealthCards)))
         for Scard in sortPriority(stealthCards):
            if debugVerbosity >= 3: notify("Removing from {}".format(Scard))
            while cost > 0 and Scard.markers[mdict['Credits']] > 0:
               Scard.markers[mdict['Credits']] -= 1
               cost -= 1
               total += 1
      notify("--> {}'s {} has destroyed a total of {} credits on stealth cards".format(me,card,total))
   if debugVerbosity >= 3: notify("<<< penaltyNoisy()") #Debug
   
def autoscriptCostUndo(card, Autoscript): # Function for undoing the cost of an autoscript.
   if debugVerbosity >= 1: notify(">>> autoscriptCostUndo(){}".format(extraASDebug(Autoscript))) #Debug
   delayed_whisper("--> Undoing action...")
   actionCost = re.match(r"A([0-9]+)B([0-9]+)G([0-9]+)T([0-9]+):", Autoscript)
   me.Clicks += num(actionCost.group(1))
   me.counters['Credits'].value += num(actionCost.group(2))
   me.counters['Agenda Points'].value += num(actionCost.group(3))
   if re.search(r"T2:", Autoscript):
      random = rnd(10,5000) # A little wait...
      card.orientation = Rot0

def findTarget(Autoscript, fromHand = False, card = None): # Function for finding the target of an autoscript
   if debugVerbosity >= 1: notify(">>> findTarget(){}".format(extraASDebug(Autoscript))) #Debug
   try:
      if fromHand == True: group = me.hand
      else: group = table
      foundTargets = []
      if re.search(r'Targeted', Autoscript):
         requiredAllegiances = []
         targetGroups = prepareRestrictions(Autoscript)
         if debugVerbosity >= 2: notify("### About to start checking all targeted cards.\n### targetGroups:{}".format(targetGroups)) #Debug
         for targetLookup in group: # Now that we have our list of restrictions, we go through each targeted card on the table to check if it matches.
            if (targetLookup.targetedBy and targetLookup.targetedBy == me) or (re.search(r'AutoTargeted', Autoscript) and targetLookup.highlight != DummyColor and targetLookup.highlight != RevealedColor and targetLookup.highlight != InactiveColor):
            # OK the above target check might need some decoding:
            # Look through all the cards on the group and start checking only IF...
            # * Card is targeted and targeted by the player OR target search has the -AutoTargeted modulator and it is NOT highlighted as a Dummy, Inactive or Revealed.
            # * The player who controls this card is supposed to be me or the enemy.
               if debugVerbosity >= 2: notify("### Checking {}".format(targetLookup))
               if not checkSpecialRestrictions(Autoscript,targetLookup): continue
               if re.search(r'-onHost',Autoscript): 
                  if debugVerbosity >= 2: notify("### Looking for Host")
                  if not card: continue # If this targeting script targets only a host and we have not passed what the attachment is, we cannot find the host, so we abort.
                  if debugVerbosity >= 2: notify("### Attachment is: {}".format(card))
                  hostCards = eval(getGlobalVariable('Host Cards'))
                  isHost = False
                  for attachment in hostCards:
                     if attachment == card._id and hostCards[attachment] == targetLookup._id: 
                        if debugVerbosity >= 2: notify("### Host found! {}".format(targetLookup))
                        isHost = True
                  if not isHost: continue
               if checkCardRestrictions(gatherCardProperties(targetLookup,Autoscript), targetGroups): 
                  if not targetLookup in foundTargets: 
                     if debugVerbosity >= 3: notify("### About to append {}".format(targetLookup)) #Debug
                     foundTargets.append(targetLookup) # I don't know why but the first match is always processed twice by the for loop.
               elif debugVerbosity >= 3: notify("### findTarget() Rejected {}".format(targetLookup))# Debug
         if debugVerbosity >= 2: notify("### Finished seeking. foundTargets List = {}".format([T.name for T in foundTargets]))
         if re.search(r'DemiAutoTargeted', Autoscript):
            if debugVerbosity >= 2: notify("### Checking DemiAutoTargeted switches")# Debug
            targetNRregex = re.search(r'-choose([1-9])',Autoscript)
            targetedCards = 0
            foundTargetsTargeted = []
            if debugVerbosity >= 2: notify("### About to count targeted cards")# Debug
            for targetC in foundTargets:
               if targetC.targetedBy and targetC.targetedBy == me: foundTargetsTargeted.append(targetC)
            if targetNRregex:
               if debugVerbosity >= 2: notify("!!! targetNRregex exists")# Debug
               if num(targetNRregex.group(1)) > len(foundTargetsTargeted): pass # Not implemented yet. Once I have choose2 etc I'll work on this
               else: # If we have the same amount of cards targeted as the amount we need, then we just select the targeted cards
                  foundTargets = foundTargetsTargeted # This will also work if the player has targeted more cards than they need. The later choice will be simply between those cards.
            else: # If we do not want to choose, then it's probably a bad script. In any case we make sure that the player has targeted something (as the alternative it giving them a random choice of the valid targets)
               del foundTargets[:]
         if len(foundTargets) == 0 and not re.search(r'(?<!Demi)AutoTargeted', Autoscript): 
            targetsText = ''
            mergedList = []
            for posRestrictions in targetGroups: 
               if debugVerbosity >= 2: notify("### About to notify on restrictions")# Debug
               if targetsText == '': targetsText = '\n -- You need: '
               else: targetsText += ', or '
               del mergedList[:]
               mergedList += posRestrictions[0]
               if len(mergedList) > 0: targetsText += "{} and ".format(mergedList)  
               del mergedList[:]
               mergedList += posRestrictions[1]
               if len(mergedList) > 0: targetsText += "not {}".format(mergedList)
               if targetsText.endswith(' and '): targetsText = targetsText[:-len(' and ')]
            if debugVerbosity >= 2: notify("### About to chkPlayer()")# Debug
            if not chkPlayer(Autoscript, targetLookup.controller, False, True): 
               allegiance = re.search(r'by(Opponent|Me)', Autoscript)
               requiredAllegiances.append(allegiance.group(1))
            if len(requiredAllegiances) > 0: targetsText += "\n00 Valid Target Allegiance: {}.".format(requiredAllegiances)
            if re.search(r'isRezzed',Autoscript): targetsText += "\n -- Card Status: Rezzed"
            if re.search(r'isUnrezzed',Autoscript): targetsText += "\n -- Card Status: Unrezzed"
            delayed_whisper(":::ERROR::: You need to target a valid card before using this action{}.".format(targetsText))
         elif len(foundTargets) >= 1 and re.search(r'-choose',Autoscript):
            if debugVerbosity >= 2: notify("### Going for a choice menu")# Debug
            choiceType = re.search(r'-choose([0-9]+)',Autoscript)
            targetChoices = makeChoiceListfromCardList(foundTargets)
            if not card: choiceTitle = "Choose one of the valid targets for this effect"
            else: choiceTitle = "Choose one of the valid targets for {}'s ability".format(fetchProperty(card, 'name'))
            if debugVerbosity >= 2: notify("### Checking for SingleChoice")# Debug
            if choiceType.group(1) == '1':
               if len(foundTargets) == 1: choice = 0 # If we only have one valid target, autoselect it.
               else: choice = SingleChoice(choiceTitle, targetChoices, type = 'button', default = 0)
               if choice == 'ABORT': del foundTargets[:]
               else: foundTargets = [foundTargets.pop(choice)] # if we select the target we want, we make our list only hold that target
      if debugVerbosity >= 3: # Debug
         tlist = [] 
         for foundTarget in foundTargets: tlist.append(foundTarget.name) # Debug
         notify("<<< findTarget() by returning: {}".format(tlist))
      return foundTargets
   except: notify("!!!ERROR!!! on findTarget()")   
   
def gatherCardProperties(card,Autoscript = ''):
   if debugVerbosity >= 1: notify(">>> gatherCardProperties()") #Debug
   # This function can also sent an autoscript with it, which I then check to see that I'm not doing an autotargeted search of the table, 
   # This will allow me to avoid looking up running storeProperties() on every card the opponent has.
   if not re.search(r'AutoTargeted', Autoscript): storeProperties(card)
   cardProperties = []
   if debugVerbosity >= 4: notify("### Appending name") #Debug                
   cardProperties.append(card.name) # We are going to check its name
   if debugVerbosity >= 4: notify("### Appending Type") #Debug                
   cardProperties.append(fetchProperty(card, 'Type')) # We are going to check its Type
   if debugVerbosity >= 4: notify("### Appending Keywords") #Debug                
   cardSubkeywords = getKeywords(card).split('-') # And each individual keyword. keywords are separated by " - "
   for cardSubkeyword in cardSubkeywords:
      strippedCS = cardSubkeyword.strip() # Remove any leading/trailing spaces between keywords. We need to use a new variable, because we can't modify the loop iterator.
      if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
   if debugVerbosity >= 3: notify("<<< gatherCardProperties() with Card Properties: {}".format(cardProperties)) #Debug
   return cardProperties

def prepareRestrictions(Autoscript):
# This is a function that takes an autoscript and attempts to find restrictions on card keywords/types/names etc. 
# It goes looks for a specific working and then gathers all restrictions into a list of tuples, where each tuple has a negative and a positive entry
# The positive entry (position [0] in the tuple) contains what card properties a card needs to have to be a valid selection
# The negative entry (position [1] in the tuple) contains what card properties a card needs to NOT have to be a vaid selection.
   if debugVerbosity >= 1: notify(">>> prepareRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   validTargets = [] # a list that holds any type that a card must be, in order to be a valid target.
   targetGroups = []
   whatTarget = re.search(r'\b(at|for|type)([A-Za-z_{},& ]+)[-]?', Autoscript) # We signify target restrictions keywords by starting a string with "or"
   if whatTarget: 
      if debugVerbosity >= 2: notify("### Splitting on _or_") #Debug
      validTargets = whatTarget.group(2).split('_or_') # If we have a list of valid targets, split them into a list, separated by the string "_or_". Usually this results in a list of 1 item.
      ValidTargetsSnapshot = list(validTargets) # We have to work on a snapshot, because we're going to be modifying the actual list as we iterate.
      for iter in range(len(ValidTargetsSnapshot)): # Now we go through each list item and see if it has more than one condition (Eg, non-desert fief)
         if debugVerbosity >= 2: notify("### Creating empty list tuple") #Debug            
         targetGroups.insert(iter,([],[])) # We create a tuple of two list. The first list is the valid properties, the second the invalid ones
         multiConditionTargets = ValidTargetsSnapshot[iter].split('_and_') # We put all the mutliple conditions in a new list, separating each element.
         if debugVerbosity >= 2: notify("###Splitting on _and_ & _or_ ") #Debug
         if debugVerbosity >= 4: notify("### multiConditionTargets is: {}".format(multiConditionTargets)) #Debug
         for chkCondition in multiConditionTargets:
            if debugVerbosity >= 4: notify("### Checking: {}".format(chkCondition)) #Debug
            regexCondition = re.search(r'(no[nt]){?([A-Za-z,& ]+)}?', chkCondition) # Do a search to see if in the multicondition targets there's one with "non" in front
            if regexCondition and (regexCondition.group(1) == 'non' or regexCondition.group(1) == 'not'):
               if debugVerbosity >= 4: notify("### Invalid Target") #Debug
               if regexCondition.group(2) not in targetGroups[iter][1]: targetGroups[iter][1].append(regexCondition.group(2)) # If there is, move it without the "non" into the invalidTargets list.
            else: 
               if debugVerbosity >= 4: notify("### Valid Target") #Debug
               targetGroups[iter][0].append(chkCondition) # Else just move the individual condition to the end if validTargets list
   elif debugVerbosity >= 2: notify("### No restrictions regex") #Debug 
   if debugVerbosity >= 3: notify("<<< prepareRestrictions() by returning: {}.".format(targetGroups))
   return targetGroups

def checkCardRestrictions(cardPropertyList, restrictionsList):
   if debugVerbosity >= 1: notify(">>> checkCardRestrictions()") #Debug
   if debugVerbosity >= 2: notify("### cardPropertyList = {}".format(cardPropertyList)) #Debug
   if debugVerbosity >= 2: notify("### restrictionsList = {}".format(restrictionsList)) #Debug
   validCard = True
   for restrictionsGroup in restrictionsList: 
   # We check each card's properties against each restrictions group of valid + invalid properties.
   # Each Restrictions group is a tuple of two lists. First list (tuple[0]) is the valid properties, and the second list is the invalid properties
   # We check if all the properties from the valid list are in the card properties
   # And then we check if no properties from the invalid list are in the properties
   # If both of these are true, then the card is a valid choice for our action.
      validCard = True # We need to set it here as well for further loops
      if debugVerbosity >= 3: notify("### restrictionsGroup checking: {}".format(restrictionsGroup))
      if len(restrictionsList) > 0 and len(restrictionsGroup[0]) > 0: 
         for validtargetCHK in restrictionsGroup[0]: # look if the card we're going through matches our valid target checks
            if debugVerbosity >= 4: notify("### Checking for valid match on {}".format(validtargetCHK)) #Debug
            if not validtargetCHK in cardPropertyList: 
               if debugVerbosity >= 4: notify("### {} not found in {}".format(validtargetCHK,cardPropertyList)) #Debug
               validCard = False
      elif debugVerbosity >= 4: notify("### No positive restrictions")
      if len(restrictionsList) > 0 and len(restrictionsGroup[1]) > 0: # If we have no target restrictions, any selected card will do as long as it's a valid target.
         for invalidtargetCHK in restrictionsGroup[1]:
            if debugVerbosity >= 4: notify("### Checking for invalid match on {}".format(invalidtargetCHK)) #Debug
            if invalidtargetCHK in cardPropertyList: validCard = False
      elif debugVerbosity >= 4: notify("### No negative restrictions")
      if validCard: break # If we already passed a restrictions check, we don't need to continue checking restrictions 
   if debugVerbosity >= 1: notify("<<< checkCardRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def checkSpecialRestrictions(Autoscript,card):
# Check the autoscript for special restrictions of a valid card
# If the card does not validate all the restrictions included in the autoscript, we reject it
   if debugVerbosity >= 1: notify(">>> checkSpecialRestrictions() {}".format(extraASDebug(Autoscript))) #Debug
   if debugVerbosity >= 1: notify("### Card: {}".format(card)) #Debug
   validCard = True
   if not chkPlayer(Autoscript, card.controller, False, True): validCard = False
   if re.search(r'isRezzed',Autoscript) and not card.isFaceUp: validCard = False
   if re.search(r'isUnrezzed',Autoscript) and card.isFaceUp: validCard = False
   markerName = re.search(r'-hasMarker{([\w ]+)}',Autoscript) # Checking if we need specific markers on the card.
   if markerName: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerName.group(1)))# Debug
      marker = findMarker(card, markerName.group(1))
      if not marker: validCard = False
   markerNeg = re.search(r'-hasntMarker{([\w ]+)}',Autoscript) # Checking if we need to not have specific markers on the card.
   if markerNeg: #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
      if debugVerbosity >= 2: notify("### Checking negative marker restrictions")# Debug
      if debugVerbosity >= 2: notify("### Marker Name: {}".format(markerNeg.group(1)))# Debug
      marker = findMarker(card, markerNeg.group(1))
      if marker: validCard = False
   elif debugVerbosity >= 4: notify("### No marker restrictions.")
   propertyReq = re.search(r'-hasProperty{([\w ]+)}(eq|le|ge|gt|lt)([0-9])',Autoscript) 
   # Checking if the target needs to have a property at a certiain value. 
   # eq = equal, le = less than/equal, ge = greater than/equal, lt = less than, gt = greater than.
   if propertyReq:
      if propertyReq.group(2) == 'eq' and card.properties[propertyReq.group(1)] != propertyReq.group(3): validCard = False
      if propertyReq.group(2) == 'le' and num(card.properties[propertyReq.group(1)]) > num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'ge' and num(card.properties[propertyReq.group(1)]) < num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'lt' and num(card.properties[propertyReq.group(1)]) >= num(propertyReq.group(3)): validCard = False
      if propertyReq.group(2) == 'gt' and num(card.properties[propertyReq.group(1)]) <= num(propertyReq.group(3)): validCard = False
   if debugVerbosity >= 1: notify("<<< checkSpecialRestrictions() with return {}".format(validCard)) #Debug
   return validCard

def makeChoiceListfromCardList(cardList):
# A function that returns a list of strings suitable for a choice menu, out of a list of cards
# Each member of the list includes a card's name, traits, resources, markers and, if applicable, combat icons
   if debugVerbosity >= 1: notify(">>> makeChoiceListfromCardList()")
   targetChoices = []
   if debugVerbosity >= 2: notify("### About to prepare choices list.")# Debug
   for T in cardList:
      if debugVerbosity >= 4: notify("### Checking {}".format(T))# Debug
      markers = 'Counters:'
      if T.markers[mdict['Advance']] and T.markers[mdict['Advance']] >= 1: markers += " {} Advance,".format(T.markers[mdict['Advance']])
      if T.markers[mdict['Credits']] and T.markers[mdict['Credits']] >= 1: markers += " {} Credits,".format(T.markers[mdict['Credits']])
      if T.markers[mdict['Power']] and T.markers[mdict['Power']] >= 1: markers += " {} Power.".format(T.markers[mdict['Power']])
      if T.markers[mdict['Virus']] and T.markers[mdict['Virus']] >= 1: markers += " {} Virus.".format(T.markers[mdict['Virus']])
      if T.markers[mdict['Agenda']] and T.markers[mdict['Agenda']] >= 1: markers += " {} Agenda.".format(T.markers[mdict['Agenda']])
      if markers != 'Counters:': markers += '\n'
      else: markers = ''
      if debugVerbosity >= 4: notify("### Finished Adding Markers. Adding stats...")# Debug               
      stats = ''
      stats += "Cost: {}. ".format(fetchProperty(card, 'Cost'))
      cStat = fetchProperty(card, 'Stat')
      cType = fetchProperty(card, 'Type')
      if cType == 'ICE': stats += "Strength: {}.".format(cStat)
      if cType == 'Agenda': stats += "Agenda Points: {}.".format(cStat)
      if cType == 'Asset' or cType == 'Upgrade': stats += "Trash Cost: {}.".format(cStat)
      if debugVerbosity >= 4: notify("### Finished Adding Stats. Going to choice...")# Debug               
      choiceTXT = "{}\n{}\n{}{}".format(fetchProperty(card, 'name'),cType,markers,stats)
      targetChoices.append(choiceTXT)
   return targetChoices
   if debugVerbosity >= 3: notify("<<< makeChoiceListfromCardList()")
   
def chkWarn(card, Autoscript): # Function for checking that an autoscript announces a warning to the player
   if debugVerbosity >= 1: notify(">>> chkWarn(){}".format(extraASDebug(Autoscript))) #Debug
   global AfterRunInf, AfterTraceInf
   warning = re.search(r'warn([A-Z][A-Za-z0-9 ]+)-?', Autoscript)
   if debugVerbosity >= 2:  notify("### About to check warning")
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
      if warning.group(1) == 'AfterRun': 
         information("Some cards, like the one you just played, have a secondary effect that only works if your run is successful.\
                       \nIn those cases, usually the secondary effect has been scripted as well, but you will need to manually activate it. To do so, just double click on the Event card you used to start the run.\
                     \n\n(This message will not appear again.)")
         AfterRunInf = False  
      if warning.group(1) == 'AfterTrace': 
         information("Some cards, like the one you just played, have a secondary effect that only works if your trace is successful.\
                       \nIn those cases, usually the secondary effect has been scripted as well, but you will need to manually activate it. To do so, just double click on the Operation card you used to start the trace.\
                     \n\n(This message will not appear again.)")
         AfterTraceInf = False  
   if debugVerbosity >= 3: notify("<<< chkWarn() gracefully") 
   return 'OK'

def ASclosureTXT(string, count): # Used by Gain and Transfer, to return unicode credits, link etc when it's used in notifications
   if debugVerbosity >= 1: notify(">>> ASclosureTXT(). String: {}. Count: {}".format(string, count)) #Debug
 # function that returns a special string with the ANR unicode characters, based on the string and count that we provide it. 
 # So if it's provided with 'Credits', 2, it will return 2 [credits] (where [credits] is either the word or its symbol, depending on the unicode switch.
   if string == 'Base Link': closureTXT = '{} {}'.format(count,uniLink())
   elif string == 'Clicks' or string == 'Click': closureTXT = '{} {}'.format(count,uniClick())
   elif string == 'Credits' or string == 'Credit': 
      if count == 'all': closureTXT = 'all Credits'
      else: closureTXT = uniCredit(count)
   elif string == 'MU': closureTXT = uniMU(count)
   else: closureTXT = "{} {}".format(count,string)
   if debugVerbosity >= 3: notify("<<< ASclosureTXT() returning: {}".format(closureTXT))
   return closureTXT
   
def ofwhom(Autoscript, controller = me): 
   if debugVerbosity >= 1: notify(">>> ofwhom(){}".format(extraASDebug(Autoscript))) #Debug
   if re.search(r'o[fn]Opponent', Autoscript):
      if debugVerbosity >= 2:  notify("### Autoscript requirement found!")
      if len(players) > 1:
         if controller == me: # If we're the current controller of the card who's scripts are being checked, then we look for our opponent
            for player in players:
               if player.getGlobalVariable('ds') == '': continue # This is a spectator 
               elif player != me and player.getGlobalVariable('ds') != ds:
                  targetPL = player # Opponent needs to be not us, and of a different type. 
                                    # In the future I'll also be checking for teams by using a global player variable for it and having players select their team on startup.
         else: targetPL = me # if we're not the controller of the card we're using, then we're the opponent of the player (i.e. we're trashing their card)
      else: 
         if debugVerbosity >= 1: whisper("There's no valid Opponents! Selecting myself.")
         targetPL = me
   else: 
      if debugVerbosity >= 2:  notify("### No autoscript requirement found")
      if len(players) > 1:
         if controller != me: targetPL = controller         
         else: targetPL = me
      else: targetPL = me
   if debugVerbosity >= 3:  notify("<<< ofwhom() returning {}".format(targetPL.name))
   return targetPL
   
def per(Autoscript, card = None, count = 0, targetCards = None, notification = None): # This function goes through the autoscript and looks for the words "per<Something>". Then figures out what the card multiplies its effect with, and returns the appropriate multiplier.
   if debugVerbosity >= 1: notify(">>> per(){}".format(extraASDebug(Autoscript))) #Debug
   if targetCards is None: targetCards = []
   div = 1
   ignore = 0
   per = re.search(r'\b(per|upto)(Target|Parent|Every)?([A-Z][^-]*)-?', Autoscript) # We're searching for the word per, and grabbing all after that, until the first dash "-" as the variable.   
   if per: # If the  search was successful...
      multiplier = 0
      if debugVerbosity >= 2: notify("Groups: {}. Count: {}".format(per.groups(),count)) #Debug
      if per.group(2) and (per.group(2) == 'Target' or per.group(2) == 'Every'): # If we're looking for a target or any specific type of card, we need to scour the requested group for targets.
         ### IMPORTANT. THIS NEEDS WORK! cardgroup needs to NOT be assigned chkItem. FIX THIS BEFORE ADDING TARGETED PER ###
         perCHK = per.group(3).split('_on_') # First we check to see if in our conditions we're looking for markers or card properties, to remove them from the checks
         perCHKSnapshot = list(perCHK)
         for chkItem in perCHKSnapshot:
            if re.search(r'(Marker|Property|Any)',chkItem):
               perCHK.remove(chkItem) # We remove markers and card.properties from names of the card keywords  we'll be looking for later.
         if re.search(r'fromHand', Autoscript): cardgroup = findTarget('Targeted-at' + chkItem, fromHand = True)
         else: cardgroup = findTarget('Targeted-at' + chkItem)
         cardProperties = [] #we're making a big list with all the properties of the card we need to match
         for c in cardgroup: # Go through each card on the table and gather its properties, then see if they match.
            del cardProperties[:] # Cleaning the previous entries
            cFaceD = False # Variable to note down if a card was face-down when we were checking it, or not.
            if c.targetedBy and not c.isFaceUp: # If the card we're checking is not face up, we turn it temporarily to grab its properties for checking. We only check targeted cards though.
               c.isFaceUp = True
               cFaceD = True
               random = rnd(10,100) # Bug workaround.
            cardProperties.append(fetchProperty(c, 'name')) # We are going to check its name
            cardProperties.append(c.Type) # It's type
            cardSubtypes = getKeywords(c).split('-') # And each individual trait. Traits are separated by " - "
            for cardSubtype in cardSubtypes:
               strippedCS = cardSubtype.strip() # Remove any leading/trailing spaces between traits. We need to use a new variable, because we can't modify the loop iterator.
               if strippedCS: cardProperties.append(strippedCS) # If there's anything left after the stip (i.e. it's not an empty string anymrore) add it to the list.
            cardProperties.append(c.Side) # We are also going to check if the card is for runner or corp.
            if cFaceD: c.isFaceUp = False # If the card was originally face-down, return it to that state again.
            perCHK = True # Variable to show us if the card we're checking is still passing all the requirements.
            #confirm("Bump") #Debug
            if debugVerbosity >= 2: notify("### Starting check with {}.\nProperties: {}".format(c, cardProperties)) # Debug
            for perItem in perItemMatch: # Now we check if the card properties include all the properties we need
               if perItem not in cardProperties: perCHK = False # The perCHK starts as True. We only need one missing item to turn it to False, since they all have to exist.
            for perItem in perItemExclusion:
               if perItem in cardProperties: perCHK = False # Pretty much the opposite of the above.
            if perCHK: # If we still have not dismissed the card and we're supposed to reveal them to the other players...
               #notify("group2: {}. card is: {}. Targeting is: {}".format(per.group(2),c,c.targetedBy))
               if re.search(r'isExposeTarget', Autoscript) and c.isFaceUp: perCHK = False                             # We exclude the card if it's supposed to get exposed but can't (i.e. see encryption breakthrough)
               if re.search(r'isRezzed', Autoscript) and not c.isFaceUp: perCHK = False    # We exclude the card if it's supposed to be rezzed but isn't
               if re.search(r'isUnrezzed', Autoscript) and c.isFaceUp: perCHK = False  # We exclude the card if it's supposed to be unrezzed but isn't
               if re.search(r'Target',per.group(2)) and (not c.targetedBy or not c.targetedBy == me): perCHK = False  # We exclude the card if we only gather targets but it's not one.
            if perCHK: # Here we find out how much multiplier we get from those cards.
               if debugVerbosity >= 2: notify("### Target Found: {}".format(c)) # Debug
               if re.search(r'isExposeTarget', Autoscript) and not c.isFaceUp and c.targetedBy == me: expose(c) # If the card is supposed to be exposed to get the benefit, then do so now.
               if re.search(r'(Reveal&Shuffle|Reveal&Recover)', Autoscript) and c.targetedBy and c.targetedBy == me: 
                  c.moveToTable((70 * iter) - 150, 0 - yaxisMove(card), False) # If the card is supposed to be revealed to get the benefit, then we do so now
                  c.highlight = RevealedColor
                  notify("- {} reveals {} from their hand".format(me,c))
                  iter +=1
               if re.search(r'SendToTrash', Autoscript) and c.targetedBy and c.targetedBy == me: handDiscard(c)
               if re.search(r'Marker',per.group(3)): #If we're looking for markers, then we go through each targeted card and check if it has any relevant markers
                  markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # If we're looking for markers on the card, increase the multiplier by the number of markers found.
                  marker = findMarker(card, markerName.group(1))
                  if marker: multiplier += card.markers[marker]
               elif re.search(r'Property',per.group(3)): # If we're looking for a specific property on the card, increase the multiplier by the total of the properties on the cards found.
                  property = re.search(r'Property{([\w ]+)}',per.group(3))
                  multiplier += num(c.properties[property.group(1)]) # Don't forget to turn it into an integer first!
               else: multiplier += 1 * chkPlayer(Autoscript, c.controller, False) # If the perCHK remains 1 after the above loop, means that the card matches all our requirements. We only check faceup cards so that we don't take into acoount peeked face-down ones.
                                                                                  # We also multiply it with chkPlayer() which will return 0 if the player is not of the correct allegiance (i.e. Rival, or Me)
         #confirm("Finished checking") # Debug
         revealedCards = [c for c in table if c.highlight == RevealedColor] # If we have any revealed cards that need to be reshuffled, we need to do so now.
         if re.search(r'Reveal&Shuffle', Autoscript) and len(revealedCards) > 0: 
            information("The cards you've just revealed will be reshuffled into your deck once your opponents have had a chance to look at them.\
                   \nOnce you are ready, press any button to reshuffle them back into your deck")
            for c in revealedCards: c.moveTo(me.piles['R&D/Stack'])
            random = rnd(10,500) # Bug workaround.
            shuffle(me.piles['R&D/Stack'])
            notify("- {} Shuffles their revealed cards back into their {}".format(me,pileName(me.piles['R&D/Stack'])))
         if re.search(r'Reveal&Recover', Autoscript) and len(revealedCards) > 0: 
            information("The cards you've just revealed will be returned to your hand once your opponents have had a chance to look at them.\
                   \nOnce you are ready, press any button to return them to your hand.")
            for c in revealedCards: c.moveTo(me.hand)
            notify("- {} returns the revealed cards back into their hand".format(me))
      else: #If we're not looking for a particular target, then we check for everything else.
         if debugVerbosity >= 2: notify("### Doing no table lookup") # Debug.
         if per.group(3) == 'X': multiplier = count # Probably not needed and the next elif can handle alone anyway.
         elif count: multiplier = num(count) * chkPlayer(Autoscript, card.controller, False) # All non-special-rules per<somcething> requests use this formula.
                                                                                              # Usually there is a count sent to this function (eg, number of favour purchased) with which to multiply the end result with
                                                                                              # and some cards may only work when a rival owns or does something.
         elif re.search(r'Marker',per.group(3)):
            markerName = re.search(r'Marker{([\w ]+)}',per.group(3)) # I don't understand why I had to make the curly brackets optional, but it seens atTurnStart/End completely eats them when it parses the CardsAS.get(card.model,'')
            marker = findMarker(card, markerName.group(1))
            if marker: multiplier = card.markers[marker]
            else: multiplier = 0
         elif re.search(r'Property',per.group(3)):
            property = re.search(r'Property{([\w ]+)}',per.group(3))
            multiplier = card.properties[property.group(1)]
      if debugVerbosity >= 2: notify("### Checking ignore") # Debug.            
      ignS = re.search(r'-ignore([0-9]+)',Autoscript)
      if ignS: ignore = num(ignS.group(1))
      if debugVerbosity >= 2: notify("### Checking div") # Debug.            
      divS = re.search(r'-div([0-9]+)',Autoscript)
      if divS: div = num(divS.group(1))
   else: multiplier = 1
   if debugVerbosity >= 2: notify("<<< per() with Multiplier: {}".format((multiplier - ignore) / div)) # Debug
   return (multiplier - ignore) / div

def chkPlayer(Autoscript, controller, manual, targetChk = False): # Function for figuring out if an autoscript is supposed to target an opponent's cards or ours.
# Function returns 1 if the card is not only for rivals, or if it is for rivals and the card being activated it not ours.
# This is then multiplied by the multiplier, which means that if the card activated only works for Rival's cards, our cards will have a 0 gain.
# This will probably make no sense when I read it in 10 years...
   if debugVerbosity >= 1: notify(">>> chkPlayer(). Controller is: {}".format(controller)) #Debug
   try:
      if targetChk: # If set to true, it means we're checking from the findTarget() function, which needs a different keyword in case we end up with two checks on a card's controller on the same script
         byOpponent = re.search(r'targetOpponents', Autoscript)
         byMe = re.search(r'targetMine', Autoscript)
      else:
         byOpponent = re.search(r'(byOpponent|duringOpponentTurn|forOpponent)', Autoscript)
         byMe = re.search(r'(byMe|duringMyTurn|forMe)', Autoscript)
      if manual or len(players) == 1: # If there's only one player, we always return true for debug purposes.
         if debugVerbosity >= 2: notify("### Succeeded at Manual/Debug")
         validPlayer = 1 #manual means that the clicks was called by a player double clicking on the card. In which case we always do it.
      elif not byOpponent and not byMe: 
         if debugVerbosity >= 2: notify("### Succeeded at Neutral")   
         validPlayer = 1 # If the card has no restrictions on being us or a rival.
      elif byOpponent and controller != me: 
         if debugVerbosity >= 2: notify("### Succeeded at byOpponent")   
         validPlayer =  1 # If the card needs to be played by a rival.
      elif byMe and controller == me: 
         if debugVerbosity >= 2: notify("### Succeeded at byMe")   
         validPlayer =  1 # If the card needs to be played by us.
      else: 
         if debugVerbosity >= 2: notify("### Failed all checks") # Debug
         validPlayer =  0 # If all the above fail, it means that we're not supposed to be triggering, so we'll return 0 whic
      if not reversePlayerChk: 
         if debugVerbosity >= 3: notify("<<< chkPlayer() (not reversed)") # Debug
         return validPlayer
      else: # In case reversePlayerChk is set to true, we want to return the opposite result. This means that if a scripts expect the one running the effect to be the player, we'll return 1 only if the one running the effect is the opponent. See Decoy at Dantoine for a reason
         if debugVerbosity >= 3: notify("<<< chkPlayer() (reversed)") # Debug      
         if validPlayer == 0: return 1
         else: return 0
   except: 
      notify("!!!ERROR!!! Null value on chkPlayer()")
      return 0
   
