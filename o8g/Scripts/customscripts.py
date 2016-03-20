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
# This file contains the autoscripting for cards with specialized effects. So called 'CustomScripts'
# * UseCustomAbility() is used among other scripts, and it just one custom ability among other normal core commands
# * CustomScipt() is a completely specialized effect, that is usually so unique, that it's not worth updating my core commands to facilitate it for just one card.
###=================================================================================================================###

collectiveSequence = []
hijackDefaultAction = []
#------------------------------------------------------------------------------
# Custom Abilities. These are abilities that can be added as part of a larger script
#------------------------------------------------------------------------------

def UseCustomAbility(Autoscript, announceText, card, targetCards = None, notification = None, n = 0):
   global reversePlayerChk, hijackDefaultAction
   trash = me.piles['Heap/Archives(Face-up)']
   arcH = me.piles['Archives(Hidden)']
   deck = me.piles['R&D/Stack']
   if fetchProperty(card, 'name') == "Tollbooth":
      targetPL = findOpponent()
      # We reverse for which player the reduce effects work, because we want cards which pay for the opponent's credit cost to take effect now.
      reduction = reduceCost(card, 'FORCE', 3, True, reversePlayer = True) # We use a dry-run to see if they have a card which card reduce the tollbooth cost such as stimhack
      if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))  
      elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: extraText = ''
      if targetPL.Credits >= 3 - reduction: 
         finalAmount = targetPL.Credits - 3 # We note it down to mention it later due to a bug that may occur.
         targetPL.Credits -= 3 - reduceCost(card, 'FORCE', 3, reversePlayer = True)
         announceString = announceText + ' force {} to pay {}{}, bringing them down to {}'.format(targetPL,uniCredit(3),extraText,uniCredit(finalAmount))
      else: 
         jackOut(silent = True)
         announceString = announceText + ' end the run'
   if fetchProperty(card, 'name') == "Datapike":
      targetPL = findOpponent()
      # We reverse for which player the reduce effects work, because we want cards which pay for the opponent's credit cost to take effect now.
      reduction = reduceCost(card, 'FORCE', 2, True, reversePlayer = True) # We use a dry-run to see if they have a card which card reduce the tollbooth cost such as stimhack
      if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))  
      elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: extraText = ''
      if targetPL.Credits >= 2 - reduction:
         finalAmount = targetPL.Credits - 2
         targetPL.Credits -= 2 - reduceCost(card, 'FORCE', 2, reversePlayer = True)
         announceString = announceText + ' force {} to pay {}{}, bringing them down to {}'.format(targetPL,uniCredit(2),extraText,uniCredit(finalAmount))
      else: 
         jackOut(silent = True)
         announceString = announceText + ' end the run'
   if fetchProperty(card, 'name') == "Replicator":
      targetC = targetCards[0] # For this to be triggered a program has to have been installed, which was passed to us in an array.
      if not confirm("Would you like to replicate the {}?".format(targetC.Name)):
         return 'ABORT'
      retrieveResult = RetrieveX('Retrieve1Card-grab{}-isTopmost'.format(targetC.Name.replace('-','_')), announceText, card)
      shuffle(me.piles['R&D/Stack'])
      if re.search(r'no valid targets',retrieveResult[0]): announceString = "{} tries to use their replicator to create a copy of {}, but they run out of juice.".format(me,targetC.Name) # If we couldn't find a copy of the played card to replicate, we inform of this
      else: announceString = "{} uses their replicator to create a copy of {}".format(me,targetC.Name)
      notify(announceString)
   if fetchProperty(card, 'name') == "Data Hound":
      count = askInteger("By which amount of trace strength did you exceeded the runner's link strength?",1)
      if not count: return 'ABORT'
      targetPL = findOpponent()
      cardList = list(targetPL.piles['R&D/Stack'].top(count)) # We make a list of the top cards the corp can look at.
      debugNotify("Turning Runner's Stack Face Up", 2)
      if len(cardList) > 1:
         notify(":> {}'s Data Hound is sniffing through {}'s Stack".format(me,targetPL))
         trashedC = askCard(cardList,"Choose card to Trash from the runner's Stack",card.Name)
         cardList.remove(trashedC)
      else: trashedC = cardList.pop(0)
      debugNotify("Trashing {}".format(trashedC), 2)
      sendToTrash(trashedC)
      if len(cardList) > 1: notify("{}'s Data Hound has sniffed out and trashed {} and is now reorganizing {}'s Stack".format(me,trashedC,targetPL))
      else: notify("{} has sniffed out and trashed {}".format(me,trashedC))
      idx = 0 # The index where we're going to be placing each card.
      while len(cardList) > 0:
         if len(cardList) == 1: movedC = cardList[0]
         else: movedC = askCard(cardList,"Choose card put on the {} position of the Stack".format(numOrder(idx),card.Name))
         cardList.remove(movedC)
         changeCardGroup(movedC, targetPL.piles['R&D/Stack'], index = idx)
         idx += 1
      debugNotify("Removing Visibility", 2)
      announceString = ':=> Sniff'
         #      __
         # (___()'`;   *Sniff*
         # /,    /`
         # \\"--\\      
         # Pity the chatbox does not support formatting :(
   if fetchProperty(card, 'name') == "Invasion of Privacy":
      cardList = []
      count = len(me.hand)
      iter = 0
      for c in me.hand:
         cardList.append(c)
         c.moveToTable(playerside * iter * cwidth(c) - (count * cwidth(c) / 2), 0 - yaxisMove(c), False)
         c.highlight = RevealedColor
         iter += 1
      notify("{} reveals {} from their hand. Target the cards you want to trash and press 'Del'".format(me,[c.name for c in cardList]))
      while not confirm("You have revealed your hand to your opponent. Return them to Grip?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
         notify("{} would like to know if it's OK to return their remaining cards to their Grip.".format(me))
      for c in cardList: 
         if c.group == table: c.moveTo(me.hand)
   if fetchProperty(card, 'name') == "Aggressive Secretary":
      programTargets = [c for c in table if c.Type == 'Program']
      debugNotify("Found {} Programs on table".format(len(programTargets)))
      if not len(programTargets): 
         notify("{} can find no programs to trash".format(card))
         return
      rc = payCost(2, 'not free')
      if rc == "ABORT": 
         notify("{} could not pay to use {}".format(me,card))
         return
      chosenProgs = multiChoice('Please choose {} programs to trash'.format(card.markers[mdict['Advancement']]), makeChoiceListfromCardList(programTargets),card)
      if chosenProgs == 'ABORT': return
      while len(chosenProgs) > card.markers[mdict['Advancement']]:
         chosenProgs = multiChoice('You chose too many programs. Please choose up to {} programs to trash'.format(card.markers[mdict['Advancement']]), makeChoiceListfromCardList(programTargets),card)
         if chosenProgs == 'ABORT': return
      for choiceProg in chosenProgs:
         prog = programTargets[choiceProg]
         intTrashCard(prog, fetchProperty(prog,'Stat'), "free", silent = True)
         notify(":> {} trashes {}".format(card,prog))
      announceString = ''
   if fetchProperty(card, 'name') == "Snoop":
      if re.search(r'-isFirstCustom',Autoscript): 
         remoteCall(findOpponent(),"Snoop",['Simply Reveal'])
         announceString = announceText + " reveal the runner's hand"
      else: 
         remoteCall(findOpponent(),"Snoop",['Reveal and Trash'])
         announceString = announceText + " reveal the runner's hand and trash a card"
   if fetchProperty(card, 'name') == "Punitive Counterstrike":
      barNotifyAll("000000","--The runner is setting how many agenda points they stole last turn.")
      count = askInteger("How many agenda points did you steal last turn?", 0)
      if count: InflictX('Inflict{}MeatDamage-onOpponent'.format(count), '', card)
      notify("--> {} is punished for their shenanigans with {} meat damage".format(me,count))
   if fetchProperty(card, 'name') == "Yagura":
      me.piles['R&D/Stack'].setVisibility('me')
      topC = me.piles['R&D/Stack'][0]
      cardDetails = makeChoiceListfromCardList([topC])[0]
      me.piles['R&D/Stack'].setVisibility('none')
      #notify("{}".format(topCard))
      notify("{} is looking at the top card in their R&D...".format(me))
      if confirm("The top card is:\n{}\n\nDo you want to send it to the bottom of your deck?".format(cardDetails)):
         topC.moveToBottom(me.piles['R&D/Stack'])
         announceString = announceText + " send the top card of their R&D to the bottom".format(me)
      else:
         announceString = announceText + " look at the top card of their R&D and leave it where it is".format(me)   
   if fetchProperty(card, 'name') == "Toshiyuki Sakai":
      handTargets = [c for c in me.hand if c.Type == 'Agenda' or c.Type == 'Asset']
      debugNotify("Found {} Assets / Agendas in hand".format(len(handTargets)))
      if not len(handTargets): 
         notify("{} can find no assets or agendas in your hand".format(card))
         return
      chosenInstall = SingleChoice('Please choose one asset/agenda from your hand with which to replace Toshiyuki Sakai', makeChoiceListfromCardList(handTargets))
      if chosenInstall == 'ABORT': return
      x,y = card.position
      handTargets[chosenInstall].moveToTable(x, y, True)
      handTargets[chosenInstall].markers[mdict['Advancement']] = card.markers[mdict['Advancement']]
      card.moveTo(me.hand)
      notify(":> {} replaces {} with a new card from their hand".format(me,card))
      announceString = ''
   if fetchProperty(card, 'name') == "Power Nap":
      doubles = len([c for c in me.piles['Heap/Archives(Face-up)'] if re.search(r'Double',c.Keywords)])
      if doubles:
         me.Credits += doubles
         notify('--> {} gains {} extra credits for the double events in their Heap'.format(me,uniCredit(doubles)))
      announceString = ''
   if fetchProperty(card, 'name') == "Bullfrog":
      remoteCall(findOpponent(),"Bullfrog",[card])
      announceString = ''
   if card.model == "bc0f047c-01b1-427f-a439-d451eda05011":
      count = askInteger("How many credits do you want to pay for Shi.Kyu?", 0)
      if not count: count = 0
      while count > me.Credits: 
         count = askInteger(":::ERROR::: You do not have {} credits to spend.\n\nHow many credits do you want to pay for Shi.Kyu?".format(count), 0)
         if not count: count = 0
      me.Credits -= count
      notify("{} opts spend {} credits to power Shi.Kyu".format(me,count))
      remoteCall(findOpponent(),"ShiKyu",[card,count])
      announceString = ''
   if fetchProperty(card, 'name') == "Cerebral Cast":
      choice = SingleChoice("Do you want to take a tag or 1 brain damage?",["Take a Tag","Suffer 1 Brain Damage"])
      if choice == 0: 
         me.Tags += 1
         notify("{} chooses to take a Tag".format(me))
      else: 
         InflictX('Inflict1BrainDamage-onOpponent', '', card)
         notify("{} chooses to take a brain damage".format(me))
      announceString = ''
   if fetchProperty(card, 'name') == "Shiro":
      if re.search(r'-isFirstCustom',Autoscript): 
         announceString = announceText + " look and rearrange at the top 3 card of their R&D"
         me.piles['R&D/Stack'].addViewer(me)
         cardList = list(me.piles['R&D/Stack'].top(3)) # We make a list of the top cards we will look at.
         if len(cardList): loopChk(cardList[len(cardList) - 1])
         notify(":> {} is rearranging through {}'s R&D".format(card,me))
         idx = 0 # The index where we're going to be placing each card.
         while len(cardList) > 0:
            if len(cardList) == 1: choice = 0
            else: choice = SingleChoice("Choose card put on the {} position of the R&D".format(numOrder(idx)), makeChoiceListfromCardList(cardList))
            movedC = cardList.pop(choice)
            movedC.moveTo(me.piles['R&D/Stack'],idx) # If there's only one card left, we put it in the last available index location in the Stack. We always put the card one index position deeper, because the first card is the cover.
            idx += 1
         notify("{} has finished preparing the R&D".format(card))
         debugNotify("Removing Visibility", 2)
         me.piles['R&D/Stack'].removeViewer(me)
      else:
         announceString = announceText + " force the runner to access the top card from their R&D"
         remoteCall(fetchRunnerPL(),"RDaccessX",[table,0,0,1])
   if fetchProperty(card, 'name') == "Susanoo-No-Mikoto":
      setGlobalVariable('status','runningArchives') # We change the global variable which holds on which server the runner is currently running on
      enemyIdent = getSpecial('Identity',fetchRunnerPL())
      #confirm("{}.{}".format(runnerPL,getSpecial('Archives',me).name))
      enemyIdent.arrow(getSpecial('Archives',me), False)
      enemyIdent.arrow(getSpecial('Archives',me), True)
      announceString = announceText + " deflect the runner to Archives. The Runner cannot  jack out until after he or she encounters a piece of ice."
   if fetchProperty(card, 'name') == "Plan B":
      if not card.markers[mdict['Advancement']]: advCount = 0
      else: advCount = card.markers[mdict['Advancement']] # We store the count of advancement markers in case the runner proceeds to trash the trap.
      if advCount > 1 and len(me.hand):
         scorableAgendas = [c for c in me.hand if c.Type == 'Agenda' and num(c.Cost) <= advCount]
         if len(scorableAgendas): extraTXT = "You have the following agendas in your HQ you can score with Plan B:\n\n{}".format([c.Name for c in scorableAgendas])
         else: extraTXT = ''
         if confirm("Do you want to initiate a Plan B?{}.\n\n(This dialogue also servers as a pause so that your opponent does not know if have any agendas you can score in HQ or not)".format(extraTXT)):
            if len(scorableAgendas):
               if len(scorableAgendas) == 1: choice = 0
               else:
                  choice = SingleChoice("Choose which agenda to score", makeChoiceListfromCardList(scorableAgendas,True))
               if choice == None: notify("{} opts not to initiate their Plan B.".format(me))
               else: 
                  scrAgenda(scorableAgendas[choice], silent = True, forced = True)
                  notify("{} initiates their {} and scores {} from their HQ".format(me,card,scorableAgendas[choice]))
            else: notify("{} opts not to initiate their Plan B".format(me))
         else: notify("{} opts not to initiate their Plan B".format(me))
      else: notify("{} wasn't prepared enough to succeed".format(card))
      announceString = ''
   if fetchProperty(card, 'name') == "Window":
      me.piles['R&D/Stack'].bottom().moveTo(me.hand)
      announceString = announceText + " draw the bottom card from their stack"
   if fetchProperty(card, 'name') == "Bug":
      bugMemory = getGlobalVariable('Bug Memory')
      if bugMemory == 'None': 
         whisper(":::ERROR::: The corp didn't draw a card recently to expose")
         announceString = announceText
      else: announceString = announceText + " expose {} just drawn by the corp".format(bugMemory)
   if fetchProperty(card, 'name') == "Oracle May":
      choice = SingleChoice("What kind of card type do you think is on top of your deck?",['Event','Program','Hardware','Resource'])
      if choice == None: announceString = announceText
      foreseenCard = me.piles['R&D/Stack'].top()
      foreseenCard.moveTo(me.piles['Heap/Archives(Face-up)'])
      update()
      notify(":> {} reveals a {}".format(card,foreseenCard))
      choiceType = ['Event','Program','Hardware','Resource'][choice]
      if foreseenCard.Type == choiceType:
         announceString = announceText + " foresee an {} accurately! {} draws {} to their hand and gains {}".format(choiceType,me,foreseenCard.Name,uniCredit(2))
         foreseenCard.moveTo(me.hand)
         me.Credits += 2
      else: announceString = announceText + " attempt to foresee a {}, but was mistaken. {} is trashed".format(choiceType,foreseenCard)
   if fetchProperty(card, 'name') == "Galahad" or fetchProperty(card, 'name') == "Lancelot" or fetchProperty(card, 'name') == "Merlin" or fetchProperty(card, 'name') == "Excalibur":
      revealedCards = findTarget('Targeted-atGrail-fromHand')
      del revealedCards[2:] # We don't want it to be more than 5 cards
      if len(revealedCards) == 0: 
         delayed_whisper("You need to target some Grail first!")
         return 'ABORT'
      for c in revealedCards: CreateDummy('CreateDummy-doNotTrash-nonUnique', '', c)
      notify("{} reveals {} as their Grail support".format(me,[c.Name for c in revealedCards]))
      announceString = ''
   if fetchProperty(card, 'name') == "Social Engineering":
      #confirm('1')
      targetICE = targetCards[0]
      if findMarker(targetICE, 'Social Engineering'):
         card.controller.Credits += num(targetCards[0].Cost)
         notify("{} gains {} from their {}".format(card.controller,uniCredit(num(targetCards[0].Cost)),card))
      announceString = ''
   if fetchProperty(card, 'name') == "The Foundry":
      targetC = targetCards[0] # For this to be triggered an ICE has to have been rezzed, which was passed to us in an array.
      if not confirm("Would you like to forge another {}?".format(targetC.Name)):
         return 'ABORT'
      retrieveResult = RetrieveX('Retrieve1Card-grab{}-isTopmost'.format(targetC.Name.replace('-','_')), announceText, card)
      shuffle(me.piles['R&D/Stack'])
      if re.search(r'no valid targets',retrieveResult[0]): announceString = "{} tries to use The Foundry to create a copy of {}, but they run out of bits.".format(me,targetC.Name) # If we couldn't find a copy of the played card to replicate, we inform of this
      else: announceString = "{} uses The Foundry to create a copy of {}".format(me,targetC.Name)
      notify(announceString)
   if fetchProperty(card, 'name') == "Shattered Remains":
      programTargets = [c for c in table if c.Type == 'Hardware']
      debugNotify("Found {} Hardware on table".format(len(programTargets)))
      if not len(programTargets): 
         notify("{} can find no hardware to trash".format(card))
         return
      rc = payCost(1, 'not free')
      if rc == "ABORT": 
         notify("{} could not pay to use {}".format(me,card))
         return
      chosenHW = multiChoice('Please choose {} hardware to trash'.format(card.markers[mdict['Advancement']]), makeChoiceListfromCardList(programTargets),card)
      if chosenHW == 'ABORT': return
      while len(chosenHW) > card.markers[mdict['Advancement']]:
         chosenHW = multiChoice('You chose too many hardware. Please choose up to {} hardware to trash'.format(card.markers[mdict['Advancement']]), makeChoiceListfromCardList(programTargets),card)
         if chosenHW == 'ABORT': return
      for chosenCard in chosenHW:
         hw = programTargets[chosenCard]
         intTrashCard(hw, fetchProperty(hw,'Stat'), "free", silent = True)
         notify(":> {} trashes {}".format(card,hw))
      announceString = ''
   if fetchProperty(card, 'name') == "Trade-In": # This is only the part where it returns half the cost. The rest is done in the autoscript.
      hardware = findTarget("Targeted-atHardware")
      if not len(hardware): return 'ABORT'
      price = int(num(hardware[0].Cost) / 2)
      me.Credits += price
      notify(":> {} trades-in {} for {}".format(me,hardware[0],uniCredit(price)))
      announceString = ''
   if fetchProperty(card, 'name') == "Angel Arena":
      if len(deck) == 0: 
         delayed_whisper("There's no more opponents to fight!")
         return 'ABORT'
      revealedCard = deck.top()
      revealedCard.moveToTable(playerside * cwidth(revealedCard), 0 - yaxisMove(revealedCard), False)
      revealedCard.highlight = RevealedColor
      notify(":> {} reveals {} during their {} matchup".format(me,revealedCard,card))
      if not confirm("You have revealed your {} to your opponent. Do you want to send the card to the bottom of your Stack?".format(revealedCard.Name)): 
         revealedCard.moveTo(deck)
         notify("{} chooses to leave it at top of their Stack")
      else: 
         revealedCard.moveToBottom(deck)     
         notify("{} chooses to send it to the bottom of their Stack")
      announceString = ''
   if fetchProperty(card, 'name') == "Troll":
      remoteCall(fetchRunnerPL(),'Troll',[card])
      notify(':> {} forces {} to pay {} or end the run.'.format(card,fetchRunnerPL(),uniClick()))
      announceString = ''
   if fetchProperty(card, 'name') == "Space Camp":
      notify(':> {} is thinking where to add the  {} advancement...'.format(card,me))
      whisper(":::INFO::: Double click on a card you control to add an advancement counter")
      hijackDefaultAction.append(card)
      showHijackQueue()
      announceString = ''
   if fetchProperty(card, 'name') == 'Cyberdex Virus Suite': 
      playVirusPurgeSound()
      for c in table: 
         foundMarker = findMarker(c,'Virus')
         if foundMarker: c.markers[foundMarker] = 0
      notify("{} triggers to clean all viruses from the corporate grid".format(card))
      autoscriptOtherPlayers('VirusPurged',card)
      announceString = ''
   if fetchProperty(card, 'name') == 'Hacktivist Meeting': 
      remoteCall(fetchCorpPL(),'HacktivistMeeting',[card])
      announceString = ''
   if fetchProperty(card, 'name') == 'London Library': 
      handTargets = [c for c in me.hand if c.targetedBy and c.targetedBy == me and c.Type == 'Program' and not re.search(r'Virus', getKeywords(c))]
      tableTargets = [c for c in table if findMarker(c, 'London Library') and c.targetedBy and c.targetedBy == me ]
      if len(handTargets):
         hostMe(handTargets[0],card)
         TokensX('Put1London Library-isSilent', "", handTargets[0])
         announceString = "{} host {} in the {}".format(announceText,handTargets[0],card)
      elif len(tableTargets):
         uninstall(tableTargets[0], silent = True)
         announceString = "{} uninstall {} from the {}".format(announceText,tableTargets[0],card)
      else:
         whisper(":::ERROR::: Please target a card to host or uninstall for the {}".format(card))
         announceString = ''
   if fetchProperty(card, 'name') == "Award Bait":
      notify(':> {} is thinking where to add the  {} advancement...'.format(card,me))
      whisper(":::INFO::: Double click on a card you control to add an advancement counter")
      hijackDefaultAction.append(card)
      showHijackQueue()
      announceString = ''
   if fetchProperty(card, 'name') == 'Casting Call':
      agenda = targetCards[0]
      agenda.moveToTable(0,0)
      card.moveToTable(0,0)
      placeCard(agenda, 'INSTALL')
      hostMe(card,agenda)
      notify("{} installs {} using a {}".format(me,agenda,card))
      announceString = ''
   if fetchProperty(card, 'name') == 'Lily Lockwell':
      opCard = RetrieveX('Retrieve1Cards-grabOperation', announceText, card)
      deck.shuffle()
      if not len(opCard[1]):
         notify('{} had no Operations to retrieve with {}'.format(me,card))
         announceString = ''
      else:
         changeCardGroup(opCard[1][0],me.piles['R&D/Stack'])
         announceString = "{} put {} on top of their shuffled R&D".format(announceText,opCard[1][0].Name)
   if fetchProperty(card, 'name') == 'News Team':
      remoteCall(fetchRunnerPL(),'NewsTeam',[card])
      announceString = ''
   if fetchProperty(card, 'name') == "Shannon Claire":
      if re.search(r'-isFirstCustom',Autoscript): 
         me.piles['R&D/Stack'].bottom().moveTo(me.hand)
         announceString = announceText + " draw the bottom card from their R&D"
      elif re.search(r'-isSecondCustom',Autoscript): 
         opCard = RetrieveX('Retrieve1Cards-grabAgenda', announceText, card)
         deck.shuffle()
         if not len(opCard[1]):
            notify('{} had no Agendas in R&D to retrieve with {}'.format(me,card))
            announceString = ''
         else:
            changeCardGroup(opCard[1][0],me.piles['R&D/Stack'],True)
            announceString = "{} put {} on the bottom of their shuffled R&D".format(announceText,opCard[1][0].Name)
      elif re.search(r'-isThirdCustom',Autoscript): 
         opCard = RetrieveX('Retrieve1Cards-grabAgenda-fromArchives', announceText, card)
         if not len(opCard[1]):
            notify('{} had no Agendas in Archives to retrieve with {}'.format(me,card))
            announceString = ''
         else:
            changeCardGroup(opCard[1][0],me.piles['R&D/Stack'],True)
            announceString = "{} put {} on the bottom of their shuffled R&D".format(announceText,opCard[1][0].Name)
   if fetchProperty(card, 'name') == "24/7 News Cycle":
      scoredAgendas = [c for c in table if c.Type == 'Agenda' and c.markers[mdict['Scored']] and c.controller == me]
      if not len(scoredAgendas): 
         whisper("You need a scored agenda to use with {}".format(card))
         return ''
      elif len(scoredAgendas) == 1: chosenAgenda = scoredAgendas[0]
      else: 
         choice = SingleChoice('Choose one of your agendas with a "when scored" ability to resolve', makeChoiceListfromCardList(scoredAgendas))
         if choice == None: return ''
         chosenAgenda = scoredAgendas[choice]
      executePlayScripts(chosenAgenda,'SCORE')
      announceString = "{} resolve the ability of {}".format(announceText,chosenAgenda)
   if fetchProperty(card, 'name') == "Ad Blitz":
      for iter in range(n): # n should be the number provided by the player
         if SingleChoice('Install {} advertisement from Archives or HQ? ({}/{})'.format(numOrder(iter),iter+1,n),['Archives','HQ']) == 0:
            RetrieveX('Retrieve1Card-grabAdvertisement-fromArchives-toTable-rezPay', announceText, card)
         else: 
            ModifyStatus('InstallTarget-rezPay', announceText, card,findTarget('DemiAutoTargeted-atAdvertisement-choose1-fromHand'))
      announceString = "{} install and rez {} advertisements".format(announceText,n)
   if fetchProperty(card, 'name') == "Archangel":
      remoteCall(fetchCorpPL(),'Archangel',[card])
      announceString = ''
   if fetchProperty(card, 'name') == "Hunting Grounds":
      for c in deck.top(3):
         placeCard(c, action = 'INSTALL', type = 'Apex')
      announceString = "{} increase their apetite...".format(announceText)
   if fetchProperty(card, 'name') == "Chatterjee University":  
      announceString = ModifyStatus('InstallTarget-payCost-reduc{}'.format(card.markers[mdict['Power']]),announceText,card,findTarget('DemiAutoTargeted-atProgram-fromHand-choose1'))
   if fetchProperty(card, 'name') == "Disposable HQ":  
      #confirm('a')
      for iter in range(len(me.hand)):
         returnCard = askCard([c for c in me.hand],"Choose next card to add to the bottom of your R&D. Close this window to finish")
         if returnCard:         
            changeCardGroup(returnCard, me.piles['R&D/Stack'], True)
            notify("-- {} returned {} card into the bottom of R&D".format(me,numOrder(iter)))
         else:
            notify("-- {} has finished resolving their disposable HQ")
            break
      remoteCall(fetchRunnerPL(),"accessTarget",[table,0,0,True,card])
      remoteCall(fetchRunnerPL(),"HQaccess",[table,0,0])
      if card.group == me.hand: changeCardGroup(card, me.ScriptingPile) # If the disposable HQ is still in our hand, it means it was already accessed in HQ, so we need to put it in the scripting pile to mark it as already accessed
      announceString = ''
   return announceString
 
 
#------------------------------------------------------------------------------
# Custom Scripts. These are card scripts that take over the whole execution. 
# Nothing else can be added to them and they need to have click and credit payment written in them
#------------------------------------------------------------------------------
 
def CustomScript(card, action = 'PLAY', origin_card = None, original_action = None): # Scripts that are complex and fairly unique to specific cards, not worth making a whole generic function for them.
   global ModifyDraw, secretCred, collectiveSequence
   debugNotify(">>> CustomScript() with action: {}".format(action)) #Debug
   trash = me.piles['Heap/Archives(Face-up)']
   arcH = me.piles['Archives(Hidden)']
   deck = me.piles['R&D/Stack']
   #confirm("Customscript") # Debug
   if card.model == '23473bd3-f7a5-40be-8c66-7d35796b6031' and action == 'USE': # Virus Scan Special Ability
      clickCost = useClick(count = 3)
      if clickCost == 'ABORT': return 'ABORT'
      playVirusPurgeSound()
      for c in table: 
         foundMarker = findMarker(c,'Virus')
         if foundMarker: c.markers[foundMarker] = 0
      notify("{} to clean all viruses from their corporate grid".format(clickCost))
      autoscriptOtherPlayers('VirusPurged',card)
      return 'CLICK USED'
   elif card.model == '71a89203-94cd-42cd-b9a8-15377caf4437' and action == 'USE': # Technical Difficulties Special Ability
      knownMarkers = []
      for marker in card.markers:
         if marker[0] in markerRemovals: # If the name of the marker exists in the markerRemovals dictionary it means it can be removed and has a specific cost.
            knownMarkers.append(marker)
      if len(knownMarkers) == 0: 
         whisper("No known markers with ability to remove")
         return 'ABORT'
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
      if clickCost == 'ABORT': return 'ABORT'
      creditCost = payCost(cost)
      if creditCost == 'ABORT':
         me.Clicks += aCost # If the player can't pay the cost after all and aborts, we give him his clicks back as well.
         return 'ABORT' 
      card.markers[selectedMarker] -= 1
      notify("{} to remove {} for {}.".format(clickCost,selectedMarker[0],creditCost))
      return 'CLICK USED'      
   elif fetchProperty(card, 'name') == 'Accelerated Beta Test' and action == 'SCORE':
      if not confirm("Would you like to initiate an accelerated beta test?"): return 'ABORT'
      iter = 0
      foundICE = []
      allCards = list(deck.top(3))
      for c in allCards:
         c.moveTo(arcH)
         loopChk(c,'Type')
         if c.type == 'ICE': foundICE.append(c)
      information("You have beta tested the following cards.\n\n{}\n\n\n(This dialogue is a pause so that your opponent does not know if you saw any ICE or not)\n\nPress OK to continue.".format([c.Name for c in allCards]))
      installedICE = 0
      while len(foundICE):
         choice = SingleChoice("Chose an ICE to install or press Cancel to trash all remaining ICE", makeChoiceListfromCardList(foundICE, True))
         if choice != None:
            chosenC = foundICE.pop(choice)
            placeCard(chosenC,'InstallRezzed')
            chosenC.orientation ^= Rot90
            notify(" -- {} Beta Tested!".format(chosenC))
            executePlayScripts(chosenC,'REZ')
            autoscriptOtherPlayers('CardInstall',chosenC)
            autoscriptOtherPlayers('CardRezzed',chosenC)
            installedICE += 1
         else: break
      if installedICE: notify("{} initiates an Accelerated Beta Test and reveals {} Ice from the top of their R&D. These Ice are automatically installed and rezzed".format(me, installedICE))
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
         return 'ABORT'
      cardList = [c for c in deck]
      reduction = 0
      rabbits = 0
      totalCost = 0
      for c in cardList: c.moveTo(arcH)
      rnd(1,100)
      debugNotify("Entering rabbit search loop", 2)
      for c in cardList: 
         if c.model == "bc0f047c-01b1-427f-a439-d451eda01039":
            debugNotify("found rabbit!", 2)
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
   elif fetchProperty(card, 'name') == 'Personal Workshop':
      if action == 'USE':
         targetList = [c for c in me.hand  # First we see if they've targeted a card from their hand
                        if c.targetedBy 
                        and c.targetedBy == me 
                        and num(c.Cost) > 0
                        and (c.Type == 'Program' or c.Type == 'Hardware')]
         if len(targetList) > 0:
            selectedCard = targetList[0]
            actionCost = useClick(count = 1)
            if actionCost == 'ABORT': return 'ABORT'
            hostCards = eval(getGlobalVariable('Host Cards'))
            hostCards[selectedCard._id] = card._id # We set the Personal Workshop to be the card's host
            setGlobalVariable('Host Cards',str(hostCards))
            cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
            debugNotify("About to move into position", 2) #Debug
            storeProperties(selectedCard)
            orgAttachments(card)
            TokensX('Put1PersonalWorkshop-isSilent', "", selectedCard) # We add a Personal Workshop counter to be able to trigger the paying the cost ability
            announceText = TokensX('Put1Power-perProperty{Cost}', "{} to activate {} in order to ".format(actionCost,card), selectedCard)
            selectedCard.highlight = InactiveColor
            notify(announceText)
            return 'CLICK USED'
         else: 
            whisper(":::ERROR::: You need to target a program or hardware in your hand, with a cost of 1 or more, before using this action")  
            return 'ABORT'
      elif action == 'Start' and card.controller == me:
         hostCards = eval(getGlobalVariable('Host Cards'))
         PWcards = [Card(att_id) for att_id in hostCards if hostCards[att_id] == card._id]
         if len(PWcards) == 0: return 'ABORT'# No cards are hosted in the PW, we're doing nothing
         elif len(PWcards) == 1: selectedCard = PWcards[0] # If only one card is hosted in the PW, we remove a power from one of those.
         else: # Else we have to ask which one to remove.
            selectTXT = 'Personal Workshop: Please select one of your hosted cards from which to remove a power counter\n\n'
            iter = 0
            PWchoices = makeChoiceListfromCardList(PWcards)
            choice = SingleChoice("Choose one of the Personal Workshop hosted cards from which to remove a power counter", PWchoices, type = 'button', default = 0)
            selectedCard = PWcards[choice]
         TokensX('Remove1Power', "Personal Workshop:",selectedCard)
         notify("--> {}'s Personal Workshop removes 1 power marker from {}".format(me,selectedCard))
         if selectedCard.markers[mdict['Power']] == 0: # Empty of power markers means the card can be automatically installed
            host = chkHostType(selectedCard, seek = 'DemiAutoTargeted') 
            if host:
               try:
                  if host == 'ABORT': 
                     selectedCard.markers[mdict['Power']] += 1
                     delayed_whisper("-- Undoing Personal Workshop build")
                     return 'ABORT'
               except:
                  extraTXT = ' and hosted on {}'.format(host) # If the card requires a valid host and we found one, we will mention it later.
            else: extraTXT = ''
            clearAttachLinks(selectedCard) # We unhost it from Personal Workshop so that it's not trashed if PW is trashed
            placeCard(selectedCard, hostCard = host)
            orgAttachments(card)
            selectedCard.markers[mdict['PersonalWorkshop']] = 0
            selectedCard.highlight = None
            executePlayScripts(selectedCard,'INSTALL')
            autoscriptOtherPlayers('CardInstall',selectedCard)
            MUtext = chkRAM(selectedCard)
            notify("--> {} has been built{} from {}'s Personal Workshop{}".format(selectedCard,extraTXT,identName,MUtext))         
   elif fetchProperty(card, 'name') == 'Mr. Li' and action == 'USE':
      ClickCost = useClick(count = 1)
      if ClickCost == 'ABORT': return 'ABORT'
      StackTop = list(deck.top(2))
      if len(StackTop) < 2:
         whisper("Your Stack is does not have enough cards. You cannot take this action")
         return 'ABORT'
      notify("--> {} is visiting Mr. Li...".format(me))
      for c in StackTop: changeCardGroup(c,me.hand)
      returnedCard = askCard(StackTop,'Choose which card to send to the bottom of your deck',card.Name)
      returnedCard.moveToBottom(deck)
      catchwords = ["Excellent.","Don't leave town.","We'll be in touch.","We'll be seeing you soon...","Always a pleasure.","Remember our agreement.","Interesting request there."]
      goodbye = catchwords.pop(rnd(0, len(catchwords) - 1))
      notify('{} to have {} procure 1 card.\n- "{}"'.format(ClickCost,card,goodbye))
      return 'CLICK USED'
   elif fetchProperty(card, 'name') == "Indexing" and action == 'SuccessfulRun':
      targetPL = findOpponent()
      addGroupVisibility(targetPL.piles['R&D/Stack'],me) # Workaround for OCTGN bug #1242
      debugNotify("Taking R&D Control")
      grabPileControl(targetPL.piles['R&D/Stack'])
      if len(targetPL.piles['R&D/Stack']) < 5: count = len(targetPL.piles['R&D/Stack'])
      else: count = 5
      cardList = list(targetPL.piles['R&D/Stack'].top(count)) # We make a list of the top 5 cards the runner can look at.
      debugNotify("Taking R&D Visibility")
      targetPL.piles['R&D/Stack'].addViewer(me)
      if len(cardList): loopChk(cardList[len(cardList) - 1])
      idx = 0 # The index where we're going to be placing each card.
      while len(cardList) > 0:
         if len(cardList) == 1: choice = 0
         else: choice = SingleChoice("Choose card put on the {} position of the Stack".format(numOrder(idx)), makeChoiceListfromCardList(cardList), cancelButton = False, type = 'button')
         movedC = cardList.pop(choice)
         movedC.moveTo(targetPL.piles['R&D/Stack'],idx) # If there's only one card left, we put it in the last available index location in the Stack. 
         idx += 1
      notify("{} has successfully indexed {}'s R&D".format(me,targetPL))
      targetPL.piles['R&D/Stack'].removeViewer(me)
      passPileControl(targetPL.piles['R&D/Stack'],targetPL)
      delGroupVisibility(targetPL.piles['R&D/Stack'],me) # Workaround for OCTGN bug #1242
   elif fetchProperty(card, 'name') == "Deep Thought" and action == 'Start':
      if card.markers[mdict['Virus']] and card.markers[mdict['Virus']] >= 3:
         targetPL = findOpponent()
         debugNotify("Moving Corp's Top card to our Scripting Pile", 2)
         cardView = targetPL.piles['R&D/Stack'].top()
         cardView.moveTo(me.ScriptingPile)
         rnd(1,10)
         notify(":> Deep Thought has revealed the top card of R&D to {}".format(me))
         delayed_whisper(":> Deep Thought: {} is upcoming! Ommm...".format(cardView))
         rnd(1,10)
         cardView.moveTo(targetPL.piles['R&D/Stack'])
   elif fetchProperty(card, 'name') == "Midori" and action == 'USE':
      targetCards = findTarget('Targeted-atICE-isMutedTarget')
      if not len(targetCards):
         delayed_whisper(":::ERROR::: You need to target an installed to use this ability")
         return 'ABORT'
      tableICE = targetCards[0]
      targetCards = findTarget('Targeted-atICE-fromHand-isMutedTarget')
      if not len(targetCards):
         delayed_whisper(":::ERROR::: You need to also target an ICE in your hand to use this ability")
         return 'ABORT'
      if oncePerTurn(card) == 'ABORT': return 'ABORT'
      handICE = targetCards[0]
      storeProperties(handICE)
      x,y = tableICE.position
      handICE.moveToTable(x,y,True)
      handICE.orientation = Rot90
      tableICE.moveTo(me.hand)
      autoscriptOtherPlayers('CardInstall',handICE)
      notify('{} activates Midori to replace the approached {}, with an ICE from the HQ.'.format(me,tableICE.Name))
      notify('- "Naughty Naughty..."')
   elif fetchProperty(card, 'name') == "Director Haas' Pet Project" and action == 'SCORE':
      debugNotify("about to implement Director Haas' Pet Project")
      # First we need to gather all the valid cards from hand or archives.
      installableCards = []
      for c in me.hand:
         if c.Type != 'Operation': installableCards.append(c)
      for c in me.piles['Heap/Archives(Face-up)']:
         if c.Type != 'Operation': installableCards.append(c)
      for c in me.piles['Archives(Hidden)']:
         if c.Type != 'Operation': installableCards.append(c)
      debugNotify("Finished creating installableCards[]")
      if len(installableCards) == 0:
         notify("Director Haas cannot find any cards to use for their pet project :(")
         return 'ABORT'
      if not confirm("Would you like to initiate Director Haass' Pet Project?"): return 'ABORT'
      cardChoices = []
      cardTexts = []
      chosenCList = []
      for iter in range(3):
         debugNotify("len(installableCards) = {}".format(len(installableCards)))
         debugNotify("installableCards: {}".format([rootC.Name for rootC in installableCards]), 4)
         debugNotify("iter: {}/{}".format(iter,3), 4)
         del cardChoices[:]
         del cardTexts[:]
         for c in installableCards:
            if (c.Rules,c.group) not in cardTexts: # we don't want to provide the player with a the same card as a choice twice.
               debugNotify("Appending card", 4)
               cardChoices.append(c)
               cardTexts.append((c.Rules,c.group))
         choice = SingleChoice("Choose {} card to install in the pet project".format(numOrder(iter)), makeChoiceListfromCardList(cardChoices, includeGroup = True), [], 'Cancel')
         debugNotify("choice = {}".format(choice))
         if choice == None: break
         chosenCList.append(cardChoices[choice])
         if cardChoices[choice].group == me.piles['Heap/Archives(Face-up)']: notify("--> {} selected their {} card ({}) from their {}".format(me, numOrder(iter), cardChoices[choice], pileName(cardChoices[choice].group)))
         else: notify("--> {} selected their {} card from their {}".format(me, numOrder(iter), pileName(cardChoices[choice].group))         )
         installableCards.remove(cardChoices[choice])
         if cardChoices[choice].Type == 'Asset' or cardChoices[choice].Type == 'Agenda': # If we install an asset or agenda, we can't install any more of those so we remove them from the choice list.
            for rootC in installableCards:
               if rootC.Type == 'Asset' or rootC.Type == 'Agenda': 
                  debugNotify("{} Type = {}. Removing".format(rootC,rootC.Type))
                  installableCards.remove(rootC) 
               else:
                  debugNotify("{} Type = {}. Keeping".format(rootC,rootC.Type))            
         if len(installableCards) < 2 - iter: break
      if len(chosenCList) > 0: # If it's 0, it means the player changed their mind and pressed cancel on the first choice.
         debugNotify("chosenCList = {}".format([c.name for c in chosenCList]))
         debugNotify("About to create the new remote")
         Server = table.create("d59fc50c-c727-4b69-83eb-36c475d60dcb", 0, 0 - (40 * playerside), 1, False)
         placeCard(Server,'INSTALL')
         x,y = Server.position
         serverRoot = 0
         serverICE = 0
         debugNotify("About the place the cards in the new remote")
         for c in chosenCList:
            storeProperties(c)
            if c.Type == 'ICE':
               c.moveToTable(x - (10 * flipBoard), (120 * flipBoard) + flipModY - (70 * serverICE * playerside),True)
               c.orientation = Rot90
               serverICE += 1
            else:
               c.moveToTable(x - (serverRoot * 30 * flipBoard), (255 * flipBoard) + flipModY,True)
               serverRoot += 1
            debugNotify("Peeking() at Director Haas' Pet Project")
            c.peek()
            autoscriptOtherPlayers('CardInstall',c)
         notify("{} implements {} and installs {} ICE and {} cards in the server root".format(me,card,serverICE,serverRoot))
   elif fetchProperty(card, 'name') == "Howler" and action == 'USE':
      debugNotify("about to Howl!")
      # First we need to gather all the valid cards from hand or archives.
      installableCards = []
      for c in me.hand:
         if c.Type == 'ICE' and re.search('Bioroid',getKeywords(c)): installableCards.append(c)
      for c in me.piles['Heap/Archives(Face-up)']:
         if c.Type == 'ICE' and re.search('Bioroid',getKeywords(c)): installableCards.append(c)
      for c in me.piles['Archives(Hidden)']:
         if c.Type == 'ICE' and re.search('Bioroid',getKeywords(c)): installableCards.append(c)
      debugNotify("Finished creating installableCards[]")
      if len(installableCards) == 0:
         notify("Howler has no valid targets to shout for >_<")
         return 'ABORT'
      debugNotify("len(installableCards) = {}".format(len(installableCards)))
      debugNotify("installableCards: {}".format([rootC.name for rootC in installableCards]), 4)
      choice = SingleChoice("WAAAaaAAaa! Choose a Bioroid ICE to awaken!", makeChoiceListfromCardList(installableCards, includeGroup = True), [], 'Cancel')
      debugNotify("choice = {}".format(choice))
      if choice == None: return 'ABORT'
      chosenC = installableCards[choice]
      previousGroup = pileName(chosenC.group)
      debugNotify("chosenC = {}".format(chosenC))
      storeProperties(chosenC)
      debugNotify("About to move ICE behind the Howler")
      x,y = card.position
      chosenC.moveToTable(x, y + (40 * flipBoard))
      chosenC.orientation = Rot90
      TokensX('Put1Howler-isSilent', "", card, [chosenC,card])
      notify("{} wueaaAAAA! {} has awakened a {} from {} for the defense of this server!".format(uniSubroutine(),card,chosenC,previousGroup))
      autoscriptOtherPlayers('CardInstall',chosenC)
      autoscriptOtherPlayers('CardRezzed',chosenC)
   elif fetchProperty(card, 'name') == 'Awakening Center' and action == 'USE':
      targetList = [c for c in me.hand  # First we see if they've targeted a card from their hand
                     if c.targetedBy 
                     and c.targetedBy == me 
                     and c.Type == 'ICE'
                     and re.search('Bioroid',getKeywords(c))]
      if len(targetList) > 0:
         selectedCard = targetList[0]
         actionCost = useClick(count = 1)
         if actionCost == 'ABORT': return 'ABORT'
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[selectedCard._id] = card._id # We set the Awakening Center to be the card's host
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
         debugNotify("About to move into position", 2) #Debug
         storeProperties(selectedCard)
         orgAttachments(card)
         TokensX('Put1Awakening Center-isSilent', "", selectedCard) # We add an Awakening Center counter to be able to trigger the rez the ice ability
         selectedCard.highlight = InactiveColor
         notify("{} has installed a Bioroid ICE in their {}".format(me,card))
         autoscriptOtherPlayers('CardInstall',selectedCard)
         return 'CLICK USED'
      else: 
         whisper(":::ERROR::: You need to target a Bioroid ICE in your HQ before using this action")  
         return 'ABORT'
   elif fetchProperty(card, 'name') == 'Escher':
      tableICE = [c for c in table if fetchProperty(c, 'Type') == 'ICE' or (not c.isFaceUp and c.orientation == Rot90)]
      if action == 'SuccessfulRun':
         for c in tableICE: c.setController(me)
         TokensX('Put1Escher-isSilent', "", card, tableICE)
         notify("{} uses non-euclidian hacks to re-organize the corporation's ICE.".format(Identity))
         delayed_whisper(":::INFO::: All ICE control has been passed to you. Jack Out to pass control back to the corporation player.")
      if action == 'JackOut':
         for c in tableICE: c.setController(findOpponent())
         TokensX('Remove1Escher-isSilent', "", card, tableICE)
         card.moveTo(card.owner.piles['Heap/Archives(Face-up)'])
   elif fetchProperty(card, 'name') == 'Scavenge' and action == 'PLAY':
      targetPrograms = findTarget('Targeted-atProgram')
      if len(targetPrograms) == 0: return 'ABORT'
      else: trashProgram = targetPrograms[0]
      intTrashCard(trashProgram, fetchProperty(trashProgram,'Stat'), "free", silent = True) # We trash it immediately as it can be picked up by scavenge itself.
      gripTargets = findTarget('Targeted-atProgram-fromHand-isMutedTarget') # First we check if the player has targeted a program from their grip as well, this way we don't have to ask.
      if len(gripTargets) > 0: 
         debugNotify("Found Hand Card Targeted group = {}".format([c.name for c in gripTargets]))
         newProgram = gripTargets[0] #If they've targeted more than one, they shouldn't have. We just select the first.
         targetPile = 'Grip'
      else:
         debugNotify("Didn't find hand card targeted")
         gripProgsNR = len([c for c in me.hand if c.Type == 'Program'])
         heapProgsNR = len([c for c in me.piles['Heap/Archives(Face-up)'] if c.Type == 'Program'])
         debugNotify("gripProgsNR = {}, heapProgsNR = {}".format(gripProgsNR,heapProgsNR))
         if gripProgsNR == 0 and heapProgsNR == 0:
            notify("{} wanted to scavenge but forgot they don't have any programs in their grip and heap")
            return 'ABORT'
         elif gripProgsNR == 0: targetPile = 'Heap'
         elif heapProgsNR == 0: targetPile = 'Grip'
         else:
            if confirm("Do you want to install the program from your heap?"):
               targetPile = 'Heap'
            else:
               targetPile = 'Grip'
         if targetPile == 'Heap':
            debugNotify("Retrieving from {}".format(targetPile))
            retrieveTuple = RetrieveX('Retrieve1Card-fromHeap-grabProgram', '', card)
            debugNotify("retrieveTuple = {}".format(retrieveTuple))
            if len(retrieveTuple[1]) == 0: 
               notify("{} scavenged their heap but couldn't find a program to install.".format(me))
               return 'ABORT'
            newProgram = retrieveTuple[1][0]
            pile = me.piles['Heap/Archives(Face-up)']
         else:
            debugNotify("Retrieving from {}".format(targetPile))
            gripTargets = findTarget('AutoTargeted-atProgram-fromHand')
            debugNotify("About to SingleChoice")
            newProgram = gripTargets[SingleChoice("Choose a program to scavenge from your grip", makeChoiceListfromCardList(gripTargets))]
            pile = me.hand
      cardCost = num(fetchProperty(newProgram, 'Cost')) - num(trashProgram.Cost)
      if cardCost < 0: cardCost = 0
      reduction = reduceCost(newProgram, 'INSTALL', cardCost, dryRun = True)
      rc = payCost(cardCost - reduction, "not free")
      if rc == 'ABORT': return 'ABORT' # If the cost couldn't be paid, we don't proceed.
      reduceCost(newProgram, 'INSTALL', cardCost) # If the cost could be paid, we finally take the credits out from cost reducing cards.
      if reduction: reduceTXT = ' (reduced by {})'.format(reduction)
      else: reduceTXT = ''
      MUtext = chkRAM(newProgram)
      placeCard(newProgram)
      rnd(1,100) # A small pause because it seems MU take a bit to update after a multiple choice selection. This means that scavenging an Overmind, would give an extra MU for some reason
      debugNotify("Executing newProgram triggers")
      executePlayScripts(newProgram,'INSTALL')
      autoscriptOtherPlayers('CardInstall',newProgram)
      debugNotify("About to announce")
      notify("{} has trashed {} and {}d through their {} finding and installing {} for {}{}{}.".format(me,trashProgram,card,targetPile,newProgram,uniCredit(cardCost),reduceTXT,MUtext))
   elif fetchProperty(card, 'name') == 'Same Old Thing' and action == 'USE':
      if useClick(count = 2) == 'ABORT': return 'ABORT' #If the player didn't have enough clicks and opted not to proceed, do nothing.
      retrieveTuple = RetrieveX('Retrieve1Card-fromHeap-grabEvent', '', card)
      debugNotify("retrieveTuple = {}".format(retrieveTuple))
      if len(retrieveTuple[1]) == 0: 
         notify("{} tried to do the same old thing but they never did a thing in their life!".format(me))
         return 'ABORT'
      sameOldThing = retrieveTuple[1][0]
      if re.search(r'Double', getKeywords(sameOldThing)) and not chkDoublePrevention() and useClick() == 'ABORT': return 'ABORT' # If it's a double event, we need to pay any double costs.
      notify("{} does the same old {}".format(me,sameOldThing))
      intTrashCard(card, fetchProperty(sameOldThing,'Stat'), "free", silent = True)
      intPlay(sameOldThing,scripted = True)
      return 'CLICK USED'
   elif fetchProperty(card, 'name') == "Motivation" and action == 'Start':
      targetPL = me
      debugNotify("Moving Top card to our Scripting Pile", 2)
      cardView = targetPL.piles['R&D/Stack'].top()
      cardView.moveTo(me.ScriptingPile)
      rnd(1,10)
      notify(":> Motivation has revealed the top card of their Stack to {}".format(me))
      delayed_whisper(":> Motivation: {} is next! Go get 'em!".format(cardView))
      rnd(1,10)
      cardView.moveTo(targetPL.piles['R&D/Stack'])
   elif fetchProperty(card, 'name') == 'Celebrity Gift' and action == 'PLAY':
      revealedCards = findTarget('Targeted-fromHand')
      del revealedCards[5:] # We don't want it to be more than 5 cards
      if len(revealedCards) == 0: 
         delayed_whisper("You need to gift something to the celebrities first you cheapskate!")
         return 'ABORT'
      iter = 0
      for c in revealedCards:
         c.moveToTable(playerside * iter * cwidth(c) - (len(revealedCards) * cwidth(c) / 2), 0 - yaxisMove(c), False)
         c.highlight = RevealedColor
         iter += 1
      notify("{} reveals {} as their celebrity gift and gains {}".format(me,[c.Name for c in revealedCards],uniCredit(len(revealedCards) * 2)))
      while not confirm("You have revealed your celebrity gifts to your opponent. Return them to HQ?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
         notify("{} would like to know if it's OK to return their celebrity gifts to their HQ.".format(me))
      for c in revealedCards: c.moveTo(me.hand)
      me.Credits += len(revealedCards) * 2
   elif fetchProperty(card, 'name') == 'The Collective':
      if action == 'USE' or action == 'Run':
         debugNotify("Current collectiveSequence = {}".format(collectiveSequence),3)
         debugNotify("origin_card = {}. original_action = {}".format(origin_card.name,original_action),3)
         if not len(collectiveSequence):
            debugNotify("Empty collectiveSequence List")
            collectiveSequence.extend([original_action,1,origin_card.Name])
         elif collectiveSequence[0] == original_action:
            debugNotify("Matched original_action")
            if original_action == 'CardAction' and collectiveSequence[2] != origin_card.Name:
               debugNotify("{} and no match of {} with {}".format(action,collectiveSequence[2],origin_card.Name),3)
               del collectiveSequence[:]
               collectiveSequence.extend([original_action,1,origin_card.Name])
            else: 
               debugNotify("{} and matched {} with {}".format(action,collectiveSequence[2],origin_card.Name),3)
               collectiveSequence[1] += 1
         else:
            debugNotify("No match on original_action")
            del collectiveSequence[:]
            collectiveSequence.extend([original_action,1,origin_card.Name])
         if collectiveSequence[1] == 3:
            if oncePerTurn(card) == 'ABORT': return 'ABORT'
            else: 
               me.Clicks += 1
               notify(":> {} has streamlined their processes and gained 1 extra {}.".format(card,uniClick()))
      elif action == 'Start': del collectiveSequence[:]
      debugNotify("Exiting with collectiveSequence = {}".format(collectiveSequence))
   elif fetchProperty(card, 'name') == 'Copycat' and action == 'USE':
      runTargetRegex = re.search(r'running([A-Za-z&]+)',getGlobalVariable('status'))
      if not runTargetRegex: 
         whisper(":::ERROR::: You need to be currently running to use Copycat!")
         return 'ABORT'
      choice = SingleChoice("Which server are you continuing the run from?",['Remote Server','HQ','R&D','Archives'])
      if choice != None: # Just in case the player didn't just close the askInteger window.
         if choice == 0: Name = 'Remote'
         elif choice == 1: Name = 'HQ'
         elif choice == 2: Name = 'R&D'
         elif choice == 3: Name = 'Archives'
         else: return 'ABORT'
      myIdent = getSpecial('Identity',me)
      myIdent.target(False)
      if Name != 'Remote':
         enemyIdent = getSpecial('Identity',findOpponent())
         targetServer = getSpecial(Name,enemyIdent.controller)
         if targetServer: myIdent.arrow(targetServer, True) # If for some reason we can't find the relevant central server card (e.g. during debug), we abort gracefully
      setGlobalVariable('status','running{}'.format(Name))
      notify("{} trashes {} to switch runs to the {} server".format(me,card,Name))
      intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
   elif fetchProperty(card, 'name') == 'Eureka!' and action == 'PLAY':
      c = deck.top()
      c.moveTo(me.piles['Heap/Archives(Face-up)'])
      if c.Type != 'Event':
         extraCost = num(c.Cost) - 10
         if extraCost < 0: extraCost = 0
         reduction = reduceCost(c, 'TRASH', extraCost, dryRun = True)
         if reduction > 0:
            extraText = " ({} - {})".format(extraCost,reduction)
            extraText2 = " (reduced by {})".format(uniCredit(reduction))
         elif reduction < 0:
            extraText = " ({} + {})".format(extraCost,abs(reduction))
            extraText2 = " (increased by {})".format(uniCredit(reduction))
         else:
            extraText = ''
            extraText2 = ''
         if confirm("The top card of your Stack is {}. It will cost you {}{} to install and you have {} credits. Install?".format(c.Name,extraCost - reduction,extraText,me.Credits)):
            intPlay(c, 'not free', True, 10)
         else: notify("{} almost had a breakthrough while working on {}, but didn't have the funds or willpower to follow through.".format(me,c))
      else: notify("{} went for a random breakthrough, but only remembered they should have {}'d instead.".format(me,c))
   elif fetchProperty(card, 'name') == 'Expert Schedule Analyzer' and action == 'SuccessfulRun':
      remoteCall(findOpponent(),"ESA",[])
   elif fetchProperty(card, 'name') == "Woman in the Red Dress" and action == 'Start':
      remoteCall(findOpponent(),"WitRD",[])
   elif fetchProperty(card, 'name') == 'Accelerated Diagnostics' and action == 'PLAY':
      if len(me.piles['R&D/Stack']) < 3: count = len(me.piles['R&D/Stack'])
      else: count = 3
      cardList = []
      trashedList = []
      debugNotify("Moving all cards to the scripting pile")
      for c in me.piles['R&D/Stack'].top(count): 
         c.moveTo(me.ScriptingPile)
         if fetchProperty(c, 'Type') != 'Operation': # We move all cards in execution limbo (see http://boardgamegeek.com/thread/1086167/double-accelerated-diagnostics)
            debugNotify("Appending to trashedList")
            trashedList.append(c)
         else: 
            debugNotify("Appending to cardList")
            cardList.append(c)
      debugNotify("Finished checing Types")
      if len(cardList) == 0: notify("{} initiated an Accelerated Diagnostics but their beta team was incompetent".format(me))
      else:
         debugNotify("Starting to play operations")
         opsNr = len(cardList)
         for iter in range(opsNr):
            choice = SingleChoice("Choose {} diagnostic to run".format(numOrder(iter)), makeChoiceListfromCardList(cardList,True), cancelName = 'Done')
            if choice == None: break
            intPlay(cardList[choice], 'not free', True)
            debugNotify("Card Played, trashing it")
            cardList[choice].moveTo(me.piles['Heap/Archives(Face-up)'])
            cardList.remove(cardList[choice])
         notify("{} initiated an {} for {} operations and trashed {} other cards".format(me,card,3 - len(cardList) - len(trashedList), len(cardList) + len(trashedList)))
      for c in trashedList: c.moveTo(me.piles['Archives(Hidden)']) 
      for c in cardList: c.moveTo(me.piles['Archives(Hidden)'])
   elif fetchProperty(card, 'name') == "City Surveillance" and action == 'Start': # We don't need a remote call, since it's going to be the runner pressing F1 anyway in this case.
      reduction = reduceCost(card, 'Force', 1, dryRun = True)
      if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction)) #If it is, make sure to inform.
      elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
      else: extraText = ''
      if me.Credits >= 1 - reduction and confirm("City Surveilance: Pay 1 Credit?"): 
         payCost(1 - reduction, 'not free')
         reduction = reduceCost(card, 'Force', 1)
         notify(":> {} paid {} {} to avoid the {} tag".format(me,1 - reduction, extraText, card))
      else: 
         me.Tags += 1
         notify(":> {} has been caught on {} and received 1 tag".format(me,card))
   elif fetchProperty(card, 'name') == 'Power Shutdown' and action == 'PLAY':
      count = askInteger("Trash How many cards from R&D (max {})".format(len(me.piles['R&D/Stack'])),0)
      if count > len(me.piles['R&D/Stack']): count = len(me.piles['R&D/Stack'])
      for c in me.piles['R&D/Stack'].top(count): c.moveTo(me.piles['Archives(Hidden)'])
      notify("{} has initiated a power shutdown and trashed {} cards. The runner must trash 1 installed program or hardware with an install cost of {} or less".format(me,count,count))
   elif fetchProperty(card, 'name') == 'Keyhole' and action == 'SuccessfulRun':
      targetPL = findOpponent()
      grabPileControl(targetPL.piles['R&D/Stack'])
      grabPileControl(targetPL.piles['Heap/Archives(Face-up)'])
      if len(targetPL.piles['R&D/Stack']) < 3: count = len(targetPL.piles['R&D/Stack'])
      else: count = 3
      cardList = list(targetPL.piles['R&D/Stack'].top(count)) # We make a list of the top 3 cards the runner can look at.
      debugNotify("Peeking at Corp's Stack.", 2)
      for c in targetPL.piles['R&D/Stack']: c.peek()
      update() # Delay to be able to read card info
      rnd(1,100) # More delay because apparently it wasn't enough.
      choice = SingleChoice("Choose a card to trash", makeChoiceListfromCardList(cardList, True), type = 'button')
      trashedC = cardList[choice]
      sendToTrash(trashedC)
      debugNotify("Shuffling Pile")
      shuffle(targetPL.piles['R&D/Stack'])
      notify("{} has peeked through the {} at R&D and trashed {}".format(me,card,trashedC))
      passPileControl(targetPL.piles['R&D/Stack'],targetPL)
      passPileControl(targetPL.piles['Heap/Archives(Face-up)'],targetPL)
   elif fetchProperty(card, 'name') == 'Leverage' and action == 'PLAY':
      remoteCall(findOpponent(),"Leverage",[card])
   elif fetchProperty(card, 'name') == 'Capstone' and action == 'USE':
      trashTargets = findTarget('Targeted-fromHand')
      if len(trashTargets) == 0: whisper("Capstone cannot function without at least some juice!")
      else:
         actionCost = useClick(count = 1)
         if actionCost == 'ABORT': return 'ABORT'
         count = 0
         for c in trashTargets:
            foundDuplicate = False
            for seek in table:
               if c.Name == seek.Name: foundDuplicate = True
            if foundDuplicate: count += 1
            c.moveTo(me.piles['Heap/Archives(Face-up)'])
         drawMany(me.piles['R&D/Stack'], count, silent = False)
         notify("{} to activate {} in order to trash {} from their hand and draw {} new cards".format(actionCost,card,[c.Name for c in trashTargets],count))
         return 'CLICK USED'
   elif fetchProperty(card, 'name') == 'Rex Campaign' and action == 'Start':
      debugNotify("Checking Rex Campaign")
      if not card.markers[mdict['Power']]:
         if confirm("Your Rex Campaign has concluded. Do you want to gain 5 credits?\
                 \n\n(Pressing 'No' will remove 1 Bad Publicity instead)"):
            me.Credits += 5
            notify("--> The Rex Campaign concludes and provides {} with {}".format(me,uniCredit(5)))
         else:
            me.counters['Bad Publicity'].value -= 1
            notify("=> The Rex Campaign concludes and reduces {}'s Bad Publicity by 1".format(me))     
         sendToTrash(card)
   elif fetchProperty(card, 'name') == 'Sweeps Week' and action == 'PLAY':
      targetPL = findOpponent()
      me.Credits += len(targetPL.hand)
      notify("--> {} uses {}'s ability to gain {}".format(me,card,uniCredit(len(targetPL.hand))))
   elif fetchProperty(card, 'name') == 'Precognition' and action == 'PLAY':
      notify("{} foresees the future...".format(me))
      me.piles['R&D/Stack'].lookAt(5)
   elif fetchProperty(card, 'name') == 'Quest Completed' and action == 'PLAY':
      accessC = findTarget('Targeted-targetOpponents')
      if len(accessC): accessTarget(accessC[0], noQuestionsAsked = True)
      else: whisper("You need to target an card to access before playing this event")      
   elif fetchProperty(card, 'name') == "Executive Wiretaps" and action == 'PLAY':
      remoteCall(findOpponent(),"ExecWire",[])
   elif fetchProperty(card, 'name') == 'Reclamation Order' and action == 'PLAY':
      retrieveTuple = RetrieveX('Retrieve1Card-fromArchives', '', card)
      count = 0
      if retrieveTuple == 'ABORT': return 'ABORT'
      else:
         arcPiles = list(me.piles['Heap/Archives(Face-up)'])
         arcPiles.extend(me.piles['Archives(Hidden)'])
         foundMore = []
         for c in arcPiles:
            if c.Name == retrieveTuple[1][0].Name: foundMore.append(c)
         if len(foundMore):
            count = askInteger("There's {} more copies of {} in your Archives. Retrieve how many?\n\n(We'll retrieve from Open Archives first)".format(len(foundMore),retrieveTuple[1][0].Name),len(foundMore))
            for iter in range(count): foundMore.pop(0).moveTo(me.hand)
      notify("{} retrieved {} copies of {} from their Archives".format(me,len(retrieveTuple[1]) + count,retrieveTuple[1][0].Name))
   elif fetchProperty(card, 'name') == 'Iain Stirling' and action == 'Start':
      if me.counters['Agenda Points'].value < fetchCorpPL().counters['Agenda Points'].value:
         me.Credits += 2
         notify("{}: Provides {}".format(card,uniCredit(2)))
   elif fetchProperty(card, 'name') == "Push Your Luck" and action == 'PLAY':
      count = askInteger("How many credits do you want to spend?",me.Credits)
      while count > me.Credits: count = askInteger(":::Error::: You cannot spend more credits than you have\n\nHow many credits do you want to spend?",me.Credits)
      remoteCall(findOpponent(),"PYL",[count])
   elif fetchProperty(card, 'name') == "Security Testing":
      if action == 'Start':
         choice = SingleChoice("Which server would you like to security test today?",['HQ','R&D','Archives','Remote'])
         if choice == 3 or choice == None:
            card.markers[mdict['SecurityTesting']] += 1
            whisper(":::INFO::: Please manually move your Security Testing marker to the targeted remote server.\nOnce you successful run that server, target it and double click on {} to get your credits manually.".format(card))
         else:
            targetServer = getSpecial({0:'HQ',1:'R&D',2:'Archives'}.get(choice),fetchCorpPL())
            if not targetServer.markers[mdict['SecurityTesting']]: targetServer.markers[mdict['SecurityTesting']] += 1 # Apparently you cannot use more than one replacement effect each run, so only one of these counters can be placed per server
         notify("{} is going to be {} {} this turn".format(me,card,{0:'HQ',1:'R&D',2:'the Archives',3:'a remote server'}.get(choice)))
      else: 
         if getGlobalVariable('feintTarget') != 'None': currentRunTarget = getGlobalVariable('feintTarget')
         else: 
            currentRunTargetRegex = re.search(r'running([A-Za-z&]+)', getGlobalVariable('status')) # We check what the target of the current run was.
            currentRunTarget = currentRunTargetRegex.group(1)
         if currentRunTarget != 'Remote':
            targetServer = getSpecial(currentRunTarget,fetchCorpPL())
            if targetServer.markers[mdict['SecurityTesting']]: 
               #gain = targetServer.markers[mdict['SecurityTesting']] * 2
               for c in table:
                  if c.Name == "Security Testing" and c.orientation == Rot0: 
                     c.orientation = Rot90
                     break # We only set one Sec.Testing as used per run.
               targetServer.markers[mdict['SecurityTesting']] = 0
               me.Credits += 2
               notify("{}: Successful Penetration nets {} {} instead of access.".format(card,me,uniCredit(2)))
               return 'ALTERNATIVE RUN'
   elif fetchProperty(card, 'name') == 'Mutate' and action == 'PLAY':
      targetICE = findTarget('Targeted-atICE-isRezzed')
      if len(targetICE) == 0: return 'ABORT'
      else: trashICE = targetICE[0]
      intTrashCard(trashICE, fetchProperty(trashICE,'Stat'), "free", silent = True)
      revealList = []
      newICE = None
      for c in deck:
         storeProperties(c, True)
         update()
         if fetchProperty(c, 'Type') == 'ICE': 
            newICE = c
            break
         else: 
            cName = fetchProperty(c, 'name')
            revealList.append(cName)
      if not newICE: 
         notify("{} tried to mutate {} but there was no ICE left in their R&D...")
         shuffle(deck)
      else:
         placeCard(newICE,'InstallRezzed')
         shuffle(deck)
         newICE.orientation ^= Rot90
         storeProperties(newICE,True)
         executePlayScripts(newICE,'REZ')
         autoscriptOtherPlayers('CardInstall',newICE)
         autoscriptOtherPlayers('CardRezzed',newICE)
         debugNotify("About to announce")
         if len(revealList): notify("{} has mutated {} into {}. In the process they revealed the following cards before shuffling R&D\n -- {}.".format(me,trashICE,newICE,revealList))
         else: notify("{} has mutated {} into {}. That was the top card of their R&D before it wa shuffled.".format(me,trashICE,newICE))
   elif fetchProperty(card, 'name') == 'Cyber Threat' and action == 'PLAY':
      targetServer = findTarget('Targeted-atServer')
      if not len(targetServer): whisper(":::WARNING::: You should target a server before you play this card!")
      if confirm("Did the corp rez an ICE at the targeted server?"): return
      else: 
         RunX('RunGeneric', '', card)
         if len(targetServer): notify("{} takes advantage of the {} to make a run on {}".format(me,card,targetServer[0]))
         else: notify("{} takes advantage of the {} to make a run".format(me,card))
   elif fetchProperty(card, 'name') == 'Nasir Meidan' and action == 'USE':
      targetICE = findTarget('Targeted-atICE-isRezzed')
      if not len(targetICE): whisper(":::ERROR::: You need to target a rezzed ICE to use this ability")
      else:
         diff = num(targetICE[0].Cost) - me.Credits
         if diff >= 0: diff = "+{}".format(uniCredit(diff))
         else: diff = "-{}".format(uniCredit(abs(diff)))
         me.Credits = num(targetICE[0].Cost)
         me.markers[mdict['BadPublicity']] = 0
         for c in table: 
            if c.Name == 'Stimhack': c.markers[mdict['Credits']] = 0
         notify("{} encounters freshly rezzed {} and sets their Credits to {} ({})".format(me,targetICE[0],me.Credits,diff))
   elif fetchProperty(card, 'name') == 'Sealed Vault' and action == 'USE':
      if not card.markers[mdict["Credit"]] and not me.Credits: 
         notify("{} wanted to use their {} but it was full of spiderwebs and their bank accounts would shame a pauper.".format(me,card))
         return "ABORT"
      elif not card.markers[mdict["Credit"]]: choice = 0
      elif not me.Credits: choice = 1
      else: choice = SingleChoice("Choose Option", ["Move any number of credits from your credit pool to Sealed Vault.","[Click] or [Trash]: Move any number of credits from Sealed Vault to your credit pool."])
      if choice == 0:
         if payCost(1, 'not free') == "ABORT": return "ABORT"
         transfer = askInteger("How many credits do you want to transfer to the Sealed Vault?", me.Credits)
         if transfer > me.Credits: transfer = me.Credits # If they exceed their credits, we just transfer the max they have
         card.markers[mdict["Credit"]] += transfer
         me.Credits -= transfer
         notify("{} pays {} to transfer {} from their credit pool to the {}. They have {} remaining".format(me,uniCredit(1),uniCredit(transfer),card,uniCredit(me.Credits)))
      else:   
         if confirm("Trash {} to grab the credits?".format(card.Name)): trashUse = True
         else: 
            clickTXT = useClick()
            if clickTXT == 'ABORT': return clickTXT
            trashUse = False         
         transfer = askInteger("How many credits do you want to transfer from the Sealed Vault to your bank?", card.markers[mdict["Credit"]])
         if transfer > card.markers[mdict["Credit"]]: transfer = card.markers[mdict["Credit"]] # If they exceed their credits, we just transfer the max they have
         card.markers[mdict["Credit"]] -= transfer
         me.Credits += transfer
         if trashUse: 
            notify("{} {} {} to transfer {} from it to their credit pool. They now have {}".format(me,uniTrash(),card,uniCredit(transfer),uniCredit(me.Credits)))
            intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
         else: notify("{} to {} {} and transfers {} from it to their credit pool. They now have {}".format(clickTXT,uniTrash(),card,uniCredit(transfer),uniCredit(me.Credits)))         
   elif fetchProperty(card, 'name') == 'Kitsune' and action == 'USE':
      cardList = findTarget('DemiAutoTargeted-fromHand-choose1')
      remoteCall(fetchRunnerPL(),"HQaccess",[table,0,0,False,cardList])
      intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
      notify("{} {} stumbles onto Kitsune who forces them to access a card from HQ before trashing itself".format(uniSubroutine(),fetchRunnerPL()))
   elif fetchProperty(card, 'name') == 'The Supplier' and action == 'USE':
      targetList = [c for c in me.hand  # First we see if they've targeted a card from their hand
                     if c.targetedBy 
                     and c.targetedBy == me 
                     and num(c.Cost) > 0
                     and (c.Type == 'Resource' or c.Type == 'Hardware')]
      if len(targetList) > 0:
         selectedCard = targetList[0]
         actionCost = useClick(count = 1)
         if actionCost == 'ABORT': return 'ABORT'
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCards[selectedCard._id] = card._id # We set the Supplier to be the card's host
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
         debugNotify("About to move into position", 2) #Debug
         storeProperties(selectedCard)
         orgAttachments(card)
         TokensX('Put1Supplied-isSilent', "", selectedCard) # We add a Supplied counter to be able to trigger the paying the cost ability
         selectedCard.highlight = InactiveColor
         notify("{} to request {} from {}".format(actionCost,selectedCard,card))
         return 'CLICK USED'
      else: 
         whisper(":::ERROR::: You need to target a resource or hardware in your hand, before using this action")  
         return 'ABORT'
   elif fetchProperty(card, 'name') == 'Hades Shard' and action == 'USE': 
      ARCscore()      
      intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
      notify("{} activates the {} to instantly access all cards in archives".format(me,card))
   elif fetchProperty(card, 'name') == 'Inject' and action == 'PLAY':
      revealedCards = list(deck.top(4))
      if len(revealedCards) == 0: 
         delayed_whisper("Your syringe is empty!")
         return 'ABORT'
      iter = 0
      progs = 0
      for c in revealedCards:
         c.moveToTable(playerside * iter * cwidth(c) - (len(revealedCards) * cwidth(c) / 2), 0 - yaxisMove(c), False)
         c.highlight = RevealedColor
         iter += 1
         if c.Type == 'Program': progs += 1
      notify("{} reveals {} during their injection and gains {}".format(me,[c.Name for c in revealedCards],uniCredit(progs)))
      while not confirm("You have revealed your injected data to your opponent. Return all non-programs to Grip?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
         notify("{} would like to know if it's OK to return their cards to their Grip.".format(me))
      for c in revealedCards:
         if c.Type == 'Program': c.moveTo(trash)
         else: c.moveTo(me.hand)
      me.Credits += progs
   elif fetchProperty(card, 'name') == 'Bifrost Array' and action == 'SCORE': 
      targetAgenda = findTarget('DemiAutoTargeted-atAgenda_and_notBifrost Array-isScored-choose1')
      if len(targetAgenda) and confirm("Do you want to use the optional ability of Bifrost Array?"):
         notify('{} triggers the "when scored" ability of {}'.format(me,targetAgenda[0]))
         executePlayScripts(targetAgenda[0],'SCORE')
   elif fetchProperty(card, 'name') == 'Utopia Shard' and action == 'USE': 
      corpPL = fetchCorpPL()
      remoteCall(corpPL,'handRandomDiscard',[corpPL.hand,2])
      intTrashCard(card, fetchProperty(card,'Stat'), "free", silent = True)
      notify("{} activates the {} to force {} to discard 2 cards at random".format(me,card,corpPL))
   elif fetchProperty(card, 'name') == "Code Siphon" and action == 'SuccessfulRun':
      RDICE = askInteger("How many ICE does the R&D server have?",1)
      if not RDICE: RDICE = 0
      RetrieveX("Retrieve1Card-fromStack-grabProgram-toTable-payCost-reducX", '{} uses {} to'.format(me,card), card, notification = 'Automatic', n = 3 * RDICE)
   elif fetchProperty(card, 'name') == 'Earthrise Hotel' and action == 'Start': # This is just for trashing the card when empty.
      if not card.markers[mdict['Power']]: 
         sendToTrash(card)
         notify(":> {} {} {} because it expired".format(me,uniTrash(),card))
   elif fetchProperty(card, 'name') == 'Argus Security' and action == 'USE': 
      remoteCall(fetchRunnerPL(),'ArgusSecurity',[card])
   elif fetchProperty(card, 'name') == 'Glenn Station' and action == 'USE':
      actionCost = useClick(count = 1)
      if actionCost == 'ABORT': return 'ABORT'
      hostCards = eval(getGlobalVariable('Host Cards'))
      if len([HQcardID for HQcardID in hostCards if hostCards[HQcardID] == card._id]): # IF we have an attachment, we obviously want to return it to HQ now.
         glennGuest = Card([HQcardID for HQcardID in hostCards if hostCards[HQcardID] == card._id][0])
         unlinkHosts(glennGuest)
         glennGuest.moveTo(me.hand)
         notify("{} {} adds a card from {} to their HQ".format(actionCost,me,card))
      else: # Otherwise we want to host a new one
         targetList = findTarget('DemiAutoTargeted-fromHand-choose1')
         if not len(targetList):
            whisper(":::ERROR::: You need to target a card in your hand before using this action")  
            return 'ABORT'
         selectedCard = targetList[0]
         hostCards[selectedCard._id] = card._id # We set the Personal Workshop to be the card's host
         setGlobalVariable('Host Cards',str(hostCards))
         cardAttachementsNR = len([att_id for att_id in hostCards if hostCards[att_id] == card._id])
         storeProperties(selectedCard)
         selectedCard.moveToTable(0,0,True)
         orgAttachments(card)
         selectedCard.highlight = InactiveColor
         notify("{} {} hosts a card on {} from their HQ".format(actionCost,me,card))
      return 'CLICK USED'
   elif fetchProperty(card, 'name') == "Wanton Destruction" and action == 'SuccessfulRun':
      trashNR = askInteger("You have {} clicks. How many do you want to use to trash Corp cards?".format(me.Clicks),me.Clicks)
      if trashNR: 
         me.Clicks -= trashNR
         remoteCall(fetchCorpPL(),'handRandomDiscard',[None,trashNR,None,None,True])
         notify(":> {} uses {} to force {} to trash {} cards from HQ at random".format(me,card,fetchCorpPL(),trashNR))
      return 'CLICK USED'
   elif fetchProperty(card, 'name') == "Vigil" and action == 'Start':
      corpPL = fetchCorpPL()
      if len(corpPL.hand) == corpPL.counters['Hand Size'].value: DrawX('Draw1Card', '{} uses {}'.format(me,card), card, targetCards = None, notification = 'Quick', n = 0)
   elif fetchProperty(card, 'name') == "Enhanced Vision" and action == 'SuccessfulRun':
      rndCard = fetchCorpPL().hand.random()
      notify(":> The runner's {} glimpses a {} inside the corp HQ".format(card,rndCard.Name))
   elif fetchProperty(card, 'name') == "Paige Piper" and action == 'USE':
      freshInstalls = [c for c in table if c.highlight == NewCardColor and c.controller == me and c.Type != 'Event']
      if not len(freshInstalls):
         whisper("You need to install a card first before you use this ability")
         return 'ABORT'
      else:
         freshCard = freshInstalls[0]
         foundCards = []
         for c in deck:
            if c.Name == freshCard.Name: foundCards.append(c)
         if len(foundCards):
            count = askInteger("We have found {} copies of {} in your deck, how many do you want to Trash?".format(len(foundCards),freshCard.Name),len(foundCards))
            if not count: notify(":> {}'s {} checked how many copies of {} they still have in their deck but chose to trash none of them".format(me,card,freshCard))
            else:
               if count > len(foundCards): count = len(foundCards)
               for iter in range(count):
                  changeCardGroup(foundCards.pop(),trash)
               notify(":> {}'s {} trashed {} copies of {} from their deck".format(me,card,count,freshCard))
         else:
            confirm("You have no further copies in your deck. This is a pause to avoid giving away this information to the corp. Press any button to continue")
            notify(":> {}'s {} checked how many copies of {} they still have in their deck but chose to trash none of them".format(me,card,freshCard))
         deck.shuffle()
   elif fetchProperty(card, 'name') == "Jinteki Biotech" and action == 'USE':
      if me.getGlobalVariable('TripleID') == 'None':
         notify(":> {} is selecting their {} department".format(me,card))
         choiceDict = {0: 'brewery', 1: 'tank', 2: 'greenhouse'}
         choice = SingleChoice("Which department of {} would you like to use today?".format(card.Name),['The Brewery\n(Do 2 net damage.)','The Tank\n(Shuffle Archives into R&D)','The Greenhouse\n(Place 4 advancement tokens)'],cancelButton = False)
         me.setGlobalVariable('TripleID',choiceDict.get(choice))
         notify(":> {}'s {} department is now set.".format(me,card))
      else:
         clickCost = useClick(count = 3)
         if clickCost == 'ABORT': return 'ABORT'
         if me.getGlobalVariable('TripleID') == 'greenhouse':
            targetCards = findTarget('Targeted')
            if not len(targetCards): 
               whisper(":::ERROR::: Target a card before you try to advance it")
               return 'ABORT'
         card.switchTo(me.getGlobalVariable('TripleID'))
         if card.alternate == 'brewery': 
            InflictX('Inflict2NetDamage-onOpponent', '', card)
            notify("{} reveals {} as their Jinteki Biotech department and uses it to inflict 2 net damage to the runner".format(me,card))
         if card.alternate == 'tank': 
            ReshuffleX('ReshuffleArchives', '', card)
            notify("{} reveals {} as their Jinteki Biotech department and uses it reshuffle their Archves into R&D".format(me,card))
         if card.alternate == 'greenhouse': 
            TokensX('Put4Advancement','',card,targetCards)
            notify("{} reveals {} as their Jinteki Biotech department and uses it to advance {} 4 times".format(me,card,targetCards[0]))               
   elif fetchProperty(card, 'name') == "Off-Campus Apartment" and action == 'USE':
      hostCards = eval(getGlobalVariable('Host Cards'))
      handConnections = [c for c in me.hand if c.targetedBy and c.targetedBy == me and re.search(r'Connection', c.Keywords)]
      if len(handConnections):
         connection = handConnections[0] # If they targeted more than one connection for some reason, we only host the first one we see.
         installedFromGrip = True
      else:
         tableConnections = [c for c in table if c.targetedBy and c.targetedBy == me and re.search(r'Connection', c.Keywords) and not hostCards.get(c._id,None) and c.highlight != RevealedColor and c.highlight != InactiveColor and c.highlight != DummyColor]
         if len(tableConnections):
            connection = tableConnections[0] # If they targeted more than one connection for some reason, we only host the first one we see.
            installedFromGrip = False
         else:
            connection = None
      if not connection: notify("Please target an unhosted Connection in your Grip or the table before using this action")
      else:
         payTXT = ''
         if installedFromGrip:
            if useClick() == 'ABORT': return 'ABORT'
            cardCost = num(fetchProperty(connection, 'Cost'))
            reduction = reduceCost(connection, 'INSTALL', cardCost, dryRun = True)
            rc = payCost(cardCost - reduction, "not free")
            if rc == 'ABORT': return 'ABORT' # If the cost couldn't be paid, we don't proceed.
            reduceCost(connection, 'INSTALL', cardCost) # If the cost could be paid, we finally take the credits out from cost reducing cards.
            if reduction: reduceTXT = ' (reduced by {})'.format(reduction)
            else: reduceTXT = ''
            payTXT = ' paying {}{}'.format(uniCredit(cardCost), reduceTXT)
         hostMe(connection,card)
         if installedFromGrip:
            executePlayScripts(connection,'INSTALL')
            autoscriptOtherPlayers('CardInstall',connection)
         if not connection.highlight: connection.highlight = NewCardColor
         drawMany(deck, 1,silent = True)
         notify(":> {} uses {} to host {}{} and draw 1 card".format(me,card,connection, payTXT))
   elif fetchProperty(card, 'name') == "Turntable" and action == 'USE':
      myAgenda = findTarget('DemiAutoTargeted-atAgenda-targetMine-isScored-isMutedTarget-choose1')
      opAgenda = findTarget('DemiAutoTargeted-atAgenda-targetOpponents-isScored-isMutedTarget-choose1')
      if not len(myAgenda) or not len(opAgenda):
         notify(':::ERROR::: You and your opponent need to have a scored agenda to use this effect')
         return 'ABORT'
      myX,myY = myAgenda[0].position
      opX,opY = opAgenda[0].position
      opponent = opAgenda[0].controller
      passCardControl(myAgenda[0],opponent)
      placeOnTable(myAgenda[0],opX,opY)
      grabCardControl(opAgenda[0])
      placeOnTable(opAgenda[0],myX,myY)
      me.counters['Agenda Points'].value -= num(fetchProperty(myAgenda[0],'Stat'))
      me.counters['Agenda Points'].value += num(fetchProperty(opAgenda[0],'Stat'))
      opponent.counters['Agenda Points'].value -= num(fetchProperty(opAgenda[0],'Stat'))
      opponent.counters['Agenda Points'].value += num(fetchProperty(myAgenda[0],'Stat'))
      notify("{}'s mad scratches on {} swap their {} for {}'s {}".format(me,card,myAgenda[0],opponent,opAgenda[0]))
      chkAgendaVictory()
      remoteCall(opponent,'chkAgendaVictory',[])
   elif fetchProperty(card, 'name') == "Analog Dreamers" and action == 'SuccessfulRun':
      reworkTarget = findTarget('Targeted-atAgenda_or_Asset_or_Upgrade-isUnrezzed-hasntMarker{Advancement}')
      if not len(reworkTarget): 
         notify(":::ERROR::: No valid target selected to rework with {}. Target a card before using this ability".format(card))
         return 'ABORT'
      changeCardGroup(reworkTarget[0],reworkTarget[0].controller.piles['R&D/Stack'])
      remoteCall(reworkTarget[0].controller,'shuffle',[reworkTarget[0].controller.piles['R&D/Stack']])
      notify(":> {} trigger to rework {}'s unrezzed card into their R&D".format(me,reworkTarget[0].controller))
   elif fetchProperty(card, 'name') == "Street Peddler" and action == 'INSTALL':
      for c in deck.top(3): 
         hostMe(c,card)
         TokensX('Put1Peddled-isSilent', "", c)
         c.highlight = InactiveColor
   elif fetchProperty(card, 'name') == "Muertos Gang Member":
      if action == 'INSTALL': remoteCall(fetchCorpPL(),'MuertosGangInstall',[card])
      elif card.group == table: remoteCall(fetchCorpPL(),'MuertosGangUninstall',[card])
   elif fetchProperty(card, 'name') == "Chameleon" and action == 'INSTALL':
      subtypes = ['Sentry','Code Gate','Barrier']
      choice = SingleChoice('Choose which subtype of ICE to be able to break',subtypes)
      if choice == None: return 'ABORT'
      TokensX('Put1Chameleon:{} Breaker'.format(subtypes[choice]), "", card)
   elif fetchProperty(card, 'name') == "Allele Repression" and action == 'USE':
      allArc = []
      HQmoves = []
      for c in trash: allArc.append(c)
      for c in arcH: allArc.append(c)
      for iter in range(card.markers[mdict['Advancement']]):
         if not len(me.hand): 
            whisper(":::INFO::: {} only found {} in hand to swap. Breaking off...".format(card,iter + 1))
            iter -= 1
            break
         notify("-- {} is swaping {} of {}".format(me,iter + 1,card.markers[mdict['Advancement']]))
         targetedCards = findTarget('Targeted-fromHand-isMutedTarget')
         if len(targetedCards): cardHQ = targetedCards[0]
         else: cardHQ = askCard([c for c in me.hand],"Choose which card to put into archives from HQ ({}/{})".format(iter + 1,card.markers[mdict['Advancement']]),'HQ Allele Repression')
         cardARC = askCard([c for c in allArc],"Choose which card to put into HQ from Archives ({}/{})".format(iter + 1,card.markers[mdict['Advancement']]),'Archives Allele Repression')
         if not cardHQ or not cardARC: 
            iter -= 1
            break
         HQmoves.append(cardARC)
         cardHQ.moveTo(arcH)
         allArc.remove(cardARC)
      for c in HQmoves: c.moveTo(me.hand)        
      notify(":> {} trashed {} to swap {} cards between HQ and Archives".format(me,card,iter + 1))
      intTrashCard(card,card.Stat,"free",silent = True)
   elif fetchProperty(card, 'name') == 'Gang Sign' and action == 'USE': 
      remoteCall(fetchRunnerPL(),'HQaccess',[])
   elif fetchProperty(card, 'name') == 'Rolodex' and action == 'INSTALL':
      me.piles['R&D/Stack'].lookAt(5)
   elif fetchProperty(card, 'name') == 'Film Critic' and action == 'USE':
      hostCards = eval(getGlobalVariable('Host Cards'))
      attachments = fetchAttachments(card)
      if len(attachments): 
         clickCost = useClick(count = 2)
         if clickCost == 'ABORT': return 'ABORT'
         ModifyStatus('ScoreTarget-onOpponent', '', card, targetCards = attachments)
         notify("{} get {} to review {}".format(clickCost,card,attachments[0]))
      else: whisper(":::ERROR::: You do not have any agendas hosted on the Film Critic")
   elif fetchProperty(card, 'name') == "An Offer You Can't Refuse" and action == 'PLAY':
      servers = ['HQ','R&D','Archives']
      choice = SingleChoice('Choose which server to offer to the runner',['HQ','R&D','Archives'])
      remoteCall(fetchRunnerPL(),'OfferRefuseBegin',[card,servers[choice]])
   elif fetchProperty(card, 'name') == 'Bookmark' and action == 'USE':
      choice = SingleChoice('What do you want to do with the bookmark?',['[Click] Host up to 3 cards from the grip','[Click] Take all cards on Bookmark to your grip','[Trash] Take all cards on Bookmark to your grip'])
      if choice == 0:
         targetList = [c for c in me.hand  # First we see if they've targeted cards from their hand
                        if c.targetedBy 
                        and c.targetedBy == me]
         if len(targetList) > 0:
            done = 0
            actionCost = useClick(count = 1)
            if actionCost == 'ABORT': return 'ABORT'
            for selectedCard in targetList:
               selectedCard.moveToTable(0,0,True)
               selectedCard.peek()
               hostMe(selectedCard,card)
               TokensX('Put1Bookmarked-isSilent', "", selectedCard) 
               selectedCard.highlight = InactiveColor
               done += 1
               if done > 2: break
            notify("{} to bookmark {} cards".format(actionCost,done))
            return 'CLICK USED'
         else: 
            whisper(":::ERROR::: You need to target at least one card in your hand before using this action")  
            return 'ABORT'
      else:
         if choice == 1:
            actionCost = useClick(count = 1)
            if actionCost == 'ABORT': return 'ABORT'
         attachments = fetchAttachments(card)
         for attach in attachments:
            clearAttachLinks(attach)
            changeCardGroup(attach, me.hand)
         if choice == 1:
            notify("{} to return their {} {}ed cards".format(actionCost,len(attachments),card))
            return 'CLICK USED'
         else:
            notify("{} {} {} to return their {} bookmarked cards".format(me,uniTrash(),card,len(attachments)))
            intTrashCard(card, card.Stat, cost = "free")
   elif fetchProperty(card, 'name') == 'DaVinci' and action == 'USE':
         targetLists = [c for c in me.hand  # First we see if they've targeted cards from their hand
                        if c.targetedBy 
                        and c.targetedBy == me]
         if not len(targetLists):
            targetLists = [c for c in me.hand if num(c.Cost) <= card.markers[mdict['Power']]] # If not, we just try to find cards with appropriate cost
         if not len(targetLists): 
            whisper(":::ERROR::: You need to target at least one card in your hand before using this action")  
            return 'ABORT'
         elif len(targetLists) == 1: chosenCard = targetLists[0]
         else:         
            choice = SingleChoice("Choose which card to bring in with DaVinci", makeChoiceListfromCardList(targetLists))
            if choice == None: return 'ABORT'
            else: chosenCard = targetLists[choice]
         intPlay(chosenCard,'free', True)
         notify("{} {} {} to bring in {} from their hand for free".format(me,uniTrash(),card,chosenCard))
         intTrashCard(card, card.Stat, "free", silent = True)
   elif fetchProperty(card, 'name') == 'Worlds Plaza' and action == 'USE':
      if len(fetchAttachments(card)) >= 3: 
         whisper(":::ERROR::: You cannot host more than 3 assetsa at {}".format(card.Name))
         return 'ABORT'
      targetList = findTarget('DemiAutoTargeted-atAsset-fromHand-choose1')
      if len(targetList) > 0:
         actionCost = useClick(count = 1)
         if actionCost == 'ABORT': return 'ABORT'
         selectedCard = targetList[0]
         hostMe(selectedCard,card)
         ModifyStatus('RezTarget-Targeted-payCost-reduc2','',card,targetCards = [selectedCard])
         notify("{} to host {} in {}".format(actionCost,selectedCard,card))
         return 'CLICK USED'
      else: return 'ABORT'
   elif fetchProperty(card, 'name') == 'SYNC' and action == 'USE':
      actionCost = useClick(count = 1)
      if actionCost == 'ABORT': return 'ABORT'  
      if card.alternate == '': card.switchTo('Flipped')
      else: card.switchTo()
      notify("{} to flip {}".format(actionCost,card))
   elif fetchProperty(card, 'name') == 'Media Blitz' and action == 'PLAY':
      scoredAgendas = findTarget('DemiAutoTargeted-atAgenda-targetOpponents-isScored-choose1')
      if not len(scoredAgendas): 
         notify(":::ERROR::: The runner needs to have a scored agenda to use with {}".format(card))
         return 'ABORT'
      else: chosenAgenda = scoredAgendas[0]
      dummyCard = table.create(chosenAgenda.model, 0,0, persist = True) # This will create a fake card of the agenda we selected
      dummyCard.highlight = DummyColor
      dummyCard.markers[mdict['Scored']] += 1
      hostMe(dummyCard,card)
      orgAttachments(card)
      notify("{} selects to copy the text of {}".format(me,chosenAgenda))
   elif fetchProperty(card, 'name') == 'The All-Seeing I' and action == 'PLAY':
      remoteCall(fetchRunnerPL(),'AllSeeingI',[card])
   elif fetchProperty(card, 'name') == 'Apex' and action == 'USE':
      if oncePerTurn(card) == 'ABORT': return 'ABORT'
      installTarget = findTarget('DemiAutoTargeted-fromHand-choose1')
      if len(installTarget): 
         placeCard(installTarget[0], action = 'INSTALL', type = 'Apex')
         notify("{}'s hunger grows...".format(card))
   elif fetchProperty(card, 'name') == 'Independent Thinking' and action == 'PLAY':
      targetCards = findTarget('Targeted-atProgram_or_Hardware_or_Resource-targetMine')
      if len(targetCards): 
         del targetCards[5:] # Max 5 cards
         multiplier = 1
         for c in targetCards:
            if re.search(r'Directive',getKeywords(c)): multiplier = 2
         DrawX('Draw{}Cards'.format(len(targetCards) * multiplier), '', card)
         notify("{} {} {} to draw {} cards".format(me,uniTrash(),[c.Name for c in targetCards],len(targetCards) * multiplier))
         for c in targetCards: intTrashCard(c,c.Stat,'free',silent = True)
   elif fetchProperty(card, 'name') == 'Safety First' and action == 'End':
      if len(me.hand) < currentHandSize(): DrawX('Draw1Cards', '{} uses {}'.format(me,card), card, notification = 'Quick')
   elif fetchProperty(card, 'name') == 'Security Nexus' and action == 'USE':
      if oncePerTurn(card) == 'ABORT': return 'ABORT'
      remoteCall(fetchCorpPL(),'TraceX',['Trace5-traceEffects<Gain1Tags++RunEnd,SimplyAnnounce{bypass the current ICE}>', '{} uses {}'.format(me,card), card, None, 'Quick', 0])
   elif fetchProperty(card, 'name') == "Globalsec Security Clearance" and action == 'USE':      
      if oncePerTurn(card, silent = True) == 'ABORT': return 'ABORT'
      actionCost = useClick(count = 1)
      if actionCost == 'ABORT': return 'ABORT'  
      corpPl = fetchCorpPL()
      notify(":::WARN::: {} uses {} to look at the top card of the Corp R&D.".format(me,card))
      whisper(":::INFO::: The top card of the corp R&D is {} ({})".format(corpPl.piles['R&D/Stack'].top().Name,corpPl.piles['R&D/Stack'].top().Type))
   elif fetchProperty(card, 'name') == "Windfall" and action == 'PLAY':      
      deck.shuffle()
      trashC = deck.top()
      intTrashCard(trashC, fetchProperty(trashC,'Stat'), "free", silent = True)
      if trashC.Type != 'Event': 
         me.Credits += num(trashC.Cost)
         notify(":> {}'s {} has provided them with {} credits".format(me,card,trashC.Cost))
      else: notify(":> {} tried to get a windfall but found only gas".format(me))
   elif fetchProperty(card, 'name') == 'Team Sponsorship' and action == 'USE':
      choice = SingleChoice("You have a Team Sponsorship!\n\nDo you want to install from Archives or HQ",['HQ','Archives'])
      if choice == None: return 'ABORT'
      elif choice == 0: ModifyStatus('InstallTarget','Team Sponsortship:',card,findTarget('DemiAutoTargeted-atnonOperation-fromHand-choose1'))
      else: RetrieveX('Retrieve1Cards-grabnonOperation-fromArchives-toTable', 'Team Sponsortship:', card, notification = 'Quick')
   elif fetchProperty(card, 'name') == 'Drug Dealer' and action == 'Start': # Have to use a custom script because due to the remote calls, 2/3 of this card will try to draw the same card.
      remoteCall(fetchRunnerPL(),'DrugDealer',[card]) # So we need to remote script the whole card draw to make sure the runner does the draws serially, after each has finished executing.
   elif fetchProperty(card, 'name') == 'Advanced Concept Hopper' and action == 'Run' and card.controller.getGlobalVariable('ds') == 'corp': 
      remoteCall(fetchCorpPL(),'ACH',[card])
   elif fetchProperty(card, 'name') == "Kala Ghoda Real TV" and action == 'Start':      
      runnerPl = fetchRunnerPL()
      notify(":::WARN::: {} uses {} to look at the top card of the Runer's Stack.".format(me,card))
      whisper(":::INFO::: The top card of the corp R&D is {} ({})".format(runnerPl.piles['R&D/Stack'].top().Name,runnerPl.piles['R&D/Stack'].top().Type))
   elif fetchProperty(card, 'name') == "CBI Raid" and action == 'SuccessfulRun':
      remoteCall(fetchCorpPL(),'CBIRaid',[card])
   elif fetchProperty(card, 'name') == 'Lakshmi Smartfabrics' and action == 'USE':
      count = askInteger("Remove how many power counters?",card.markers[mdict['Power']])
      if not count: return
      elif count > card.markers[mdict['Power']]: count = card.markers[mdict['Power']]
      notify(":::INFO::: {} removed {} power counters from their {} and is choosing an Agenda to protect".format(me,count,card))
      agenda = askCard([c for c in me.hand if num(c.Stat) == count],"Choose an Agenda worth exactly {} points to reveal".format(count))
      if not agenda: notify("-- {} decided to abort their use of {}".format(me,card))
      else:
         card.markers[mdict['Power']] -= count
         notify("{} is preventing copies of {} from being stolen for the rest of this turn".format(me,agenda.Name))
   elif action == 'USE': useCard(card)
      
            
def markerEffects(Time = 'Start'):
   mute()
   debugNotify(">>> markerEffects() at time: {}".format(Time)) #Debug
   ### Checking triggers from markers the rest of our cards.
   cardList = [c for c in table if c.markers]
   for card in cardList:
      for marker in card.markers:
         if (re.search(r'Tinkering',marker[0]) and Time == 'End') or (re.search(r'Paintbrush',marker[0])) and Time == 'JackOut':
            TokensX('Remove999Keyword:Code Gate-isSilent', "Tinkering:", card)
            TokensX('Remove999Keyword:Sentry-isSilent', "Tinkering:", card)
            TokensX('Remove999Keyword:Barrier-isSilent', "Tinkering:", card)
            if re.search(r'Tinkering',marker[0]): 
               TokensX('Remove999Tinkering', "Tinkering:", card)
               notify("--> {} removes tinkering effect from {}".format(me,card))
            else: 
               TokensX('Remove999Paintbrush', "Paintbrush:", card)
               notify("--> {} removes Paintbrush effect from {}".format(me,card))
         if re.search(r'Cortez Chip',marker[0]) and Time == 'End':
            TokensX('Remove1Cortez Chip-isSilent', "Cortez Chip:", card)
            notify("--> {} removes Cortez Chip effect from {}".format(me,card))
         if re.search(r'Joshua Enhancement',marker[0]) and Time == 'End': # We put Joshua's effect here, in case the runner trashes the card with Aesop's after using it
            TokensX('Remove1Joshua Enhancement-isSilent', "Joshua Enhancement:", card)
            GainX('Gain1Tags', "Joshua's Enhancements:".format(me), card)
            notify("--> Joshua's Enhancements give {} a tag".format(identName))
         if re.search(r'Test Run',marker[0]) and Time == 'End': # We put Test Run's effect here, as the card will be discarded after being played.
            notify("--> The Test Run {} is returned to {}'s stack".format(card,identName))
            rnd(1,10)
            ModifyStatus('UninstallMyself-toStack', 'Test Run:', card)
         if re.search(r'Deep Red',marker[0]) and Time == 'End': # We silently remove deep red effects
            TokensX('Remove1Deep Red-isSilent', "Deep Red:", card)
         if re.search(r'LLDS Processor',marker[0]) and Time == 'End': # We silently remove LLDS Processor bonus
            TokensX('Remove999LLDS Processor-isSilent', "LLDS Processor:", card)
         if re.search(r'Social Engineering',marker[0]) and Time == 'End':
            TokensX('Remove999Social Engineering-isSilent', "Social Engineering:", card)
         if re.search(r'Gyri Labyrinth',marker[0]) and Time == 'Start' and (card.controller != me or len(getPlayers()) == 1): 
            opponentPL = findOpponent()
            #opponentPL.counters['Hand Size'].value += card.markers[marker] * 2
            notify(":> Gyri Labyrinth's effect expires and {} recovers {} hand size".format(card,card.markers[marker] * 2))
            card.markers[marker] = 0
         if re.search(r'Valley Grid',marker[0]) and Time == 'Start' and (card.controller != me or len(getPlayers()) == 1): 
            opponentPL = findOpponent()
            #opponentPL.counters['Hand Size'].value += card.markers[marker]
            notify(":> Valley Grid's effect expires and {} recovers {} hand size".format(card,card.markers[marker] * 2))
            card.markers[marker] = 0
         if re.search(r'IT Department',marker[0]) and Time == 'End':
            TokensX('Remove999IT Department-isSilent', "IT Department:", card)
         if re.search(r'Bandwidth Logged',marker[0]) and Time == 'SuccessfulRun' or Time == 'JackOut':
            if Time == 'SuccessfulRun': GainX('Lose{}Tags'.format(card.markers[marker]), "Bandwidth:", card)
            TokensX('Remove999Bandwidth Logged-isSilent', "Bandwidth:", card)
         if re.search(r'Gene Conditioned',marker[0]) and Time == 'End':
            TokensX('Remove999Gene Conditioned-isSilent', "Gene Conditioned:", card)
         if re.search(r'London Library',marker[0]) and Time == 'End': # We put Test Run's effect here, as the card will be discarded after being played.
            notify("--> London Library reimages their systems and {} is trashed".format(card))
            ModifyStatus('TrashMyself', 'London Library:', card)
         if re.search(r'Feelgood',marker[0]) and Time == 'End':
            TokensX('Remove999Feelgood-isSilent', "Dr. Feelgood:", card)
         if re.search(r'Populist Rally',marker[0]) and Time == 'Start' and card.controller == me: 
            me.Clicks -= 1
            notify(":> Populist Rally's effect reduces {}'s {} for this turn by 1".format(me,uniClick()))
            TokensX('Remove1Populist Rally-isSilent', "Populist Rally:", card)


def ASVarEffects(Time = 'Start'):
   mute()
   debugNotify(">>> ASVarEffects() at time: {}".format(Time)) #Debug
   ### Checking triggers from AutoScript Variables
   ASVars = eval(getGlobalVariable('AutoScript Variables'))
   if Time == 'Start': ASVars['Subliminal'] = 'False' # At the very start of each turn, we set the Subliminal var to False to signify no Subliminal has been played yet.
   setGlobalVariable('AutoScript Variables',str(ASVars))

def CustomEffects(Time = 'Start'):
   mute()
   debugNotify(">>> CustomEffects() at time: {}".format(Time)) #Debug
   ### Checking for specific effects that require special card awareness.
   #AwarenessList = eval(me.getGlobalVariable('Awareness'))
   if Time == 'Start': #and 'Subliminal Messaging' in AwarenessList: 
      count = sum(1 for card in me.piles['Heap/Archives(Face-up)'] if card.Name == 'Subliminal Messaging')
      count += sum(1 for card in me.piles['Archives(Hidden)'] if card.Name == 'Subliminal Messaging')
      if count and getGlobalVariable('Central Run') == 'False' and getGlobalVariable('Remote Run') == 'False':
         choice = 4
         while count < choice: 
            choice = askInteger("How much Subliminal Messaging do you want to take back into your HQ (Max {})?\
                             \n\n(We'll start taking from Face-Up Archives)".format(count), 1)
         grabbed = 0
         if grabbed < choice:
            for card in me.piles['Heap/Archives(Face-up)']:      
               if card.Name == 'Subliminal Messaging': 
                  grabbed += 1
                  card.moveTo(me.hand)
                  notify(":> {} takes one Subliminal Messaging from Face-Up Archives to their HQ".format(me))
               if grabbed == choice: break
         if grabbed < choice:
            for card in me.piles['Archives(Hidden)']:
               if card.Name == 'Subliminal Messaging': 
                  grabbed += 1
                  card.moveTo(me.hand)
                  notify(":> {} takes one Subliminal Messaging from Hidden Archives to their HQ".format(me))
               if grabbed == choice: break

def markerScripts(card, action = 'USE'):
   debugNotify(">>> markerScripts() with action: {}".format(action)) #Debug
   foundSpecial = False
   for key in card.markers:
      if key[0] == 'Personal Workshop' and action == 'USE':
         foundSpecial = True
         count = askInteger("{} has {} power counters left.\nHow many do you want to pay to remove?".format(card.Name,card.markers[mdict['Power']]),card.markers[mdict['Power']])
         if not count: return foundSpecial
         if count > card.markers[mdict['Power']]: count = card.markers[mdict['Power']]
         host = chkHostType(card) 
         if host:
            try:
               if count == card.markers[mdict['Power']] and host == 'ABORT': 
                  delayed_whisper("-- Undoing Personal Workshop build")
                  return foundSpecial
            except: extraTXT = ' on {}'.format(host) # If the card requires a valid host and we found one, we will mention it later.
         else: extraTXT = ''
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCard = Card(hostCards[card._id])
         reduction = reduceCost(hostCard, 'USE', count, dryRun = True)
         rc = payCost(count - reduction, "not free")
         if rc == 'ABORT': return foundSpecial # If the cost couldn't be paid, we don't proceed.
         reduceCost(hostCard, 'USE', count) # If the cost could be paid, we finally take the credits out from cost reducing cards.
         card.markers[mdict['Power']] -= count
         if reduction: reduceTXT = ' (reduced by {})'.format(reduction)
         else: reduceTXT = ''
         if card.markers[mdict['Power']] == 0: 
            clearAttachLinks(card) # We unhost it from Personal Workshop so that it's not trashed if PW is trashed
            placeCard(card)
            orgAttachments(hostCard)
            card.markers[mdict['PersonalWorkshop']] = 0
            card.highlight = None
            executePlayScripts(card,'INSTALL')
            autoscriptOtherPlayers('CardInstall',card)
            MUtext = chkRAM(card)
            notify("{} has paid {}{} in order to install {}{} from their Personal Workshop{}".format(me,uniCredit(count),reduceTXT,card,extraTXT,MUtext))
         else:
            notify("{} has paid {}{} to remove {} power counters from {} in their Personal Workshop".format(me,uniCredit(count),reduceTXT,count,card))         
      if key[0] == 'Awakening Center' and action == 'USE' and not card.isFaceUp:
         foundSpecial = True
         host = chkHostType(card) 
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCard = Card(hostCards[card._id])
         cardCost = num(fetchProperty(card, 'Cost')) - 7
         if cardCost < 0: cardCost = 0
         reduction = reduceCost(card, 'REZ', cardCost, dryRun = True)
         rc = payCost(cardCost - reduction, "not free")
         if rc == 'ABORT': return foundSpecial # If the cost couldn't be paid, we don't proceed.
         reduceCost(card, 'REZ', cardCost) # If the cost could be paid, we finally take the credits out from cost reducing cards.
         if reduction: reduceTXT = ' (reduced by {})'.format(reduction)
         else: reduceTXT = ''
         #card.markers[mdict['AwakeningCenter']] = 0
         card.highlight = None
         intRez(card,cost = 'free',silent = True)
         notify("{} has paid {}{} in order to rez {} from their {}.".format(me,uniCredit(cardCost),reduceTXT,card,hostCard))
      if key[0] == 'Escher' and action == 'USE': 
         global EscherUse
         foundSpecial = True
         if ds == 'corp': 
            whisper("Our ICE shouldn't have Escher tokens! Cleaning")
            tableICE = [c for c in table if fetchProperty(c, 'Type') == 'ICE' or (not c.isFaceUp and c.orientation == Rot90)]
            TokensX('Remove1Escher-isSilent', "", card, tableICE)
         else:
            EscherUse +=1
            if EscherUse == 1: whisper(":::ERROR::: Runners are not allowed to rez Escher ICE")
            elif EscherUse == 2: whisper("Bweep! Please don't touch that!")
            elif EscherUse == 3: whisper("Bweep! Bweep! Intruder Alert!")
            elif EscherUse == 4: whisper("Please stay where you are. Our helpful assistants will be right with you.")
            elif EscherUse == 5: whisper("Please remain calm. Assistance is on the way.")
            elif EscherUse == 6: whisper("Please remain calm...")
            elif EscherUse == 7: whisper("Remain calm...")
            elif EscherUse == 8: whisper("Suddenly it is pitch black!")
            elif EscherUse == 9: whisper("It is pitch black! You feel that you should really consider jacking out any time now...")
            elif EscherUse == 10: whisper("You are likely to be eaten by a Grue...")
            elif EscherUse == 11: 
               if confirm("Fine! A Grue 1.0 is rezzed! Run away?"):
                  me.Clicks = 0
                  jackOut()
                  notify("{} has encountered a Grue and run away. They lose the rest of their turn for wasting so much time.".format(me))
               else:
                  delayed_whisper(":> You FOOL!")
                  notify("{} was looking for trouble in the dark and has been eaten by a Grue. {} has flatlined".format(me,me))
                  for i in range(6): applyBrainDmg()
                  jackOut()
            else: EscherUse = 0
      if key[0] == 'Deep Red' and action == 'USE':
         notify("{} uses Deep Red's ability to rehost {}".format(me,card))
         me.Clicks += 1
         card.markers[key] = 0
         # We do not return True on foundSpecial as we want the rest of the script to run its course as well.
      if key[0] == 'Blackmail' and action == 'USE' and not card.isFaceUp:
         foundSpecial = True
         whisper(":::ERROR::: You cannot rez ICE during this run, you are being Blackmailed!")
      if key[0] == 'Supplied' and action == 'USE':
         foundSpecial = True
         host = chkHostType(card) 
         hostCards = eval(getGlobalVariable('Host Cards'))
         hostCard = Card(hostCards[card._id])
         if hostCard.orientation == Rot90 and not confirm("You've already used The Supplier this turn! Bypass restriction?"): return foundSpecial
         cardCost = num(fetchProperty(card, 'Cost')) - 2
         if cardCost < 0: cardCost = 0
         reduction = reduceCost(card, 'INSTALL', cardCost, dryRun = True)
         rc = payCost(cardCost - reduction, "not free")
         if rc == 'ABORT': return foundSpecial # If the cost couldn't be paid, we don't proceed.
         reduceCost(card, 'INSTALL', cardCost) # If the cost could be paid, we finally take the credits out from cost reducing cards.
         if reduction: reduceTXT = ' (reduced by {})'.format(reduction)
         else: reduceTXT = ''
         clearAttachLinks(card) # We unhost it from Personal Workshop so that it's not trashed if PW is trashed
         placeCard(card)
         orgAttachments(hostCard)
         card.markers[key] = 0
         card.highlight = None
         executePlayScripts(card,'INSTALL')
         autoscriptOtherPlayers('CardInstall',card)
         notify("{} has paid {}{} in order to install {} from {}.".format(me,uniCredit(cardCost),reduceTXT,card,hostCard))
      if key[0] == 'Peddled' and action == 'USE':
         foundSpecial = True
         if card.Type == 'Event': notify(":::ERROR::: You cannot get events from the Street Peddler")
         else:
            streetPeddler = fetchHost(card)
            unlinkHosts(card)
            card.isFaceUp = True
            intPlay(card, cost = 'not free', scripted = True, preReduction = 1, retainPos = True)
            card.markers[key] = 0
            intTrashCard(streetPeddler, streetPeddler.Stat, cost = "free")
   return foundSpecial
   
def setAwareness(card):
# A function which stores if a special card exists in a player's deck, and activates extra scripts only then (to avoid unnecessary load)
   if card.Name == 'Subliminal Messaging': # For now we only have subliminal. In the future we might get more card names separated by OR clauses.
      AwarenessList = eval(me.getGlobalVariable('Awareness'))
      if card.Name not in AwarenessList: AwarenessList.append(card.Name)
      me.setGlobalVariable('Awareness',str(AwarenessList))

#------------------------------------------------------------------------------
# Hijack Functions
# These are card effects which have taken over the default action of the game temporarily.
#------------------------------------------------------------------------------

def hijack(card):
   mute()
   global hijackDefaultAction
   currentHijack = hijackDefaultAction[0]
   if currentHijack.Name == "Space Camp":
      TokensX('Put1Advancement-isSilent', "", card)
      notify("{} uses {} to add an advancement on {}".format(me,currentHijack.Name,card))
   if currentHijack.Name == "Award Bait":
      count = askInteger("How many tokens do you want to add to this card (Max 2)",2)
      if count == None: count = 0
      elif count > 2: count = 2
      TokensX('Put{}Advancement-isSilent'.format(count), "", card)
      notify("{} uses {} to add {} advancement tokens on {}".format(me,currentHijack.Name,count,card))
   if currentHijack.Name == "Muertos Gang Member":
      if currentHijack.group == table:
         if not (card.isFaceUp and card.controller == me and (card.Type == 'ICE' or card.Type == 'Asset'  or card.Type == 'Upgrade') and card.highlight != InactiveColor and card.highlight != RevealedColor and card.highlight != DummyColor):
            notify(":::ERROR::: You cannot derez that card")
            return
         else: derez(card)
      else: 
         if not (card.isFaceUp == False and card.controller == me and (card.Type == 'ICE' or card.Type == 'Asset'  or card.Type == 'Upgrade') and card.highlight != InactiveColor and card.highlight != RevealedColor and card.highlight != DummyColor):
            notify(":::ERROR::: You cannot rez that card")
            return
         else: rezForFree(card)
   hijackDefaultAction.pop()
#------------------------------------------------------------------------------
# Custom Remote Functions
#------------------------------------------------------------------------------

def ESA(): # Expert Schedule Analyzer
   debugNotify(">>> Remote Script ESA()") #Debug
   mute()
   revealedCards = []
   for c in me.hand: revealedCards.append(c)
   iter = 0
   for c in revealedCards:
      c.moveToTable(playerside * iter * cwidth(c) - (len(revealedCards) * cwidth(c) / 2), 0 - yaxisMove(c), False)
      c.highlight = RevealedColor
      iter += 1
   notify("The Expert Schedule Analyzer reveals {}".format([c.Name for c in revealedCards]))
   while not confirm("You have revealed your hand to your opponent. Return them to HQ?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
      notify("{} would like to know if it's OK to return their remaining cards to their HQ.".format(me))
   for c in revealedCards: c.moveTo(me.hand)
         
def WitRD(): # Woman in the Red Dress   
   debugNotify(">>> Remote Script WitRD()") #Debug     
   mute()   
   cardView = me.piles['R&D/Stack'].top()
   notify(":> The Woman in the Red Dress has revealed {}".format(cardView.Name))
   if confirm("Do you want to draw {} to your HQ?".format(cardView.Name)):
      notify("{} decided to take {} to their hand".format(me,cardView.Name))
      cardView.moveTo(me.hand)
   else: 
      notify("{} decided to leave {} in their R&D".format(me,cardView))

def Snoop(scenario = 'Simply Reveal', cardList = None):
   debugNotify(">>> Remote Script Snoop() with Scenario = {}".format(scenario)) #Debug     
   mute()
   if not cardList: cardList = []
   if scenario == 'Remote Corp Trash Select':
      choice = SingleChoice("Choose one card to trash", makeChoiceListfromCardList(cardList,True))
      if choice != None: 
         cardList[choice].moveTo(cardList[choice].owner.piles['Heap/Archives(Face-up)'])
         notify("{} decided to trash {} from the cards snooped at".format(me,cardList[choice]))
         cardList.remove(cardList[choice])
      for c in cardList: c.setController(c.owner)
      remoteCall(findOpponent(),"Snoop",['Recover Hand',cardList])            
   elif scenario == 'Recover Hand':
      for c in cardList: c.moveTo(me.hand)
   else:
      count = len(me.hand)
      if count == 0: 
         notify("There are no cards in the runner's Grip to snoop at")
         return
      iter = 0
      for c in me.hand:
         cardList.append(c)
         c.moveToTable(playerside * iter * cwidth(c) - (count * cwidth(c) / 2), 0 - yaxisMove(c), False)
         c.highlight = RevealedColor
         iter += 1
      notify("Snoop reveals {}".format([c.Name for c in cardList]))
      if scenario == 'Simply Reveal':
         while not confirm("You have revealed your hand to your opponent. Return them to Grip?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
            notify("{} would like to know if it's OK to return their remaining cards to their Grip.".format(me))
         for c in cardList: c.moveTo(me.hand)
      elif scenario == 'Reveal and Trash':
         for c in cardList: c.setController(findOpponent())
         remoteCall(findOpponent(),"Snoop",['Remote Corp Trash Select',cardList])
         
def Leverage(card): # Leverage
   mute()
   barNotifyAll('#000000',"The corporation is deliberating if the runner's leverage is sufficient.")
   #notify(" - {} is deliberating if the runner's leverage is sufficient.".format(me))
   if confirm("Your opponent has just played Leverage. Do you want to take 2 Bad Publicity in order to allow them to still suffer damage until their next turn?"):
      me.counters['Bad Publicity'].value += 2
      notify("The corporation has decided to take 2 Bad Publicity. Beware!")
   else:
      CreateDummy('CreateDummy-with99protectionAllDMG-onOpponent', '', card)
      notify("--> The corporation has caved in to the runner's leverage. The runner cannot take any damage until the start of their next turn.")
      
def ExecWire(): # Expert Schedule Analyzer
   debugNotify(">>> Remote Script ExecWire()") #Debug
   mute()
   revealedCards = []
   for c in me.hand: revealedCards.append(c)
   iter = 0
   for c in revealedCards:
      c.moveToTable(playerside * iter * cwidth(c) - (len(revealedCards) * cwidth(c) / 2), 0 - yaxisMove(c), False)
      c.highlight = RevealedColor
      iter += 1
   notify("The Executive Wiretaps reveal {}".format([c.Name for c in revealedCards]))
   while not confirm("You have revealed your hand to your opponent. Return them to HQ?\n\n(Pressing 'No' will send a ping to your opponent to see if they're done reading them)"):
      notify("{} would like to know if it's OK to return their remaining cards to their HQ.".format(me))
   for c in revealedCards: c.moveTo(me.hand)
         
def Bullfrog(card): # Bullfrog
   choice = SingleChoice("Which server are you going to redirect the run at?", ['Remote Server','HQ','R&D','Archives'])
   if choice != None: # Just in case the player didn't just close the askInteger window.
      if choice == 0: targetServer = 'Remote'
      elif choice == 1: targetServer = 'HQ'
      elif choice == 2: targetServer = 'R&D'
      elif choice == 3: targetServer = 'Archives'
      else: return 'ABORT'
   else: return 'ABORT'
   setGlobalVariable('status','running{}'.format(targetServer)) # We change the global variable which holds on which server the runner is currently running on
   if targetServer == 'Remote': announceText = 'a remote server'
   else: announceText = 'the ' + targetServer
   notify("--> {}'s Ability triggers and redirects the runner to {}.".format(card,announceText))

def ShiKyu(card,count): # Shi.Kyu
   mute()
   if confirm("Shi.Kyu is about to inflict {} Net Damage to you. Score it for -1 Agenda Points instead?".format(count)):
      GainX('Lose1Agenda Points-onOpponent-isSilent', '', card)
      ModifyStatus('ScoreMyself-onOpponent-isSilent', '', card)
      update()
      TokensX('Put1ScorePenalty-isSilent', '', card)
      notify("{} opts to score Shi.Kyu for -1 Agenda Point".format(me))
   else:
      remoteCall(fetchCorpPL(),'InflictX',['Inflict{}NetDamage-onOpponent'.format(count), '{} activates {} to'.format(card.owner, card), card, None, 'Automatic', count]) # We always have the corp itself do the damage
     
def PYL(count): # Push Your Luck
   mute()
   choice = SingleChoice("Do you think the runner spent an even or an odd number of credits pushing their luck?\n(They had {} to spend)".format(fetchRunnerPL().Credits),['Even','Odd'])
   if count % 2 == choice:
      notify("Failure! The corp correctly guessed the runner has spent an {} number of credits. {} lost {}".format({0:'Even',1:'Odd'}.get(count % 2),fetchRunnerPL(),uniCredit(count)))
      fetchRunnerPL().Credits -= count
      playSpecialSound('Special-Push_Your_Luck-Fail')
   else:
      notify("Success! The corp incorrectly thought the runner had spent an {} number of credits. {} gains {}".format({0:'Even',1:'Odd'}.get(count % 2),fetchRunnerPL(),uniCredit(count)))
      fetchRunnerPL().Credits += count
      playSpecialSound('Special-Push_Your_Luck-Success')
      
def Troll(card): # Troll
   mute()
   if not me.Clicks:
      playCorpEndSound()
      jackOut(silent = True)
      notify("{}'s {} ends the run because {} has no more {} to spend".format(card.controller,card,me,uniClick()))
   else: 
      choice = SingleChoice("Do you want to lose a click or end the run?",["Lose a Click.","End the Run."])
      if choice == 0: 
         me.Clicks -= 1
         notify("{} chooses to pay the {}'s {} toll".format(me,card,uniClick()))
      else: 
         playCorpEndSound()
         jackOut(silent = True)
         notify("{}'s {} ends the run because {} chose not to spend a {}".format(card.controller,card,me,uniClick()))
   
def ArgusSecurity(card): 
   mute()
   choice = SingleChoice("You cannot avoid Argus Security. Take 1 Tag or suffer 2 Meat Damage?",['Take 1 Tag','Suffer 2 Meat Damage'])
   if choice == 0: 
      me.Tags += 1
      notify("{} chooses to take 1 Tag from {}".format(me,card))
   else: 
      notify("{} chooses to suffer 2 Meat Damage from {}".format(me,card))
      InflictX('Inflict2MeatDamage-onMe', '', card)

def chkGagarinTax(card):
   mute()
   runTarget = getGlobalVariable('status')
   if runTarget != 'runningHQ' and runTarget != 'runningR&D' and runTarget != 'runningArchives': # Gagarin only works on remote servers
      findGagarin = [card for card in table if card.Name == 'Gagarin Deep Space']
      if len(findGagarin):
         gararin = findGagarin[0]
         reduction = reduceCost(card, 'ACCESS', 1)
         if reduction > 0: extraText = " (reduced by {})".format(uniCredit(reduction))
         elif reduction < 0: extraText = " (increased by {})".format(uniCredit(abs(reduction)))
         else: extraText = ''
         rc = payCost(1 - reduction, "not free")
         if rc != "ABORT":  # If the player couldn't pay to trash the card, we leave it where it is.
            notify(":> {} forced {} paid {}{} to access the remote server".format(gararin, me,uniCredit(1 - reduction),extraText))
         else: 
            notify(":> {} did not have enough money to pay the {} tax".format(me,gararin))
            return 'ABORT'
   return 'OK'

def HacktivistMeeting(card):
   mute()
   discardC = me.hand.random()
   if not discardC: notify(":::WARNING::: {} was supposed to trash a random card from HQ to rez their non-ICE card, but they had no cards left in hand".format(me))
   else:
      handDiscard(discardC, True)
      notify(":> {} trashed a card from HQ at random as an extra cost".format(me))
      
def MuertosGangInstall(card):
   rezzedOptions = [c for c in table if c.controller == me and c.isFaceUp and (c.Type == 'ICE' or c.Type == 'Asset' or c.Type == 'Upgrade') and c.highlight != InactiveColor and c.highlight != RevealedColor and c.highlight != DummyColor]
   if not len(rezzedOptions):
      notify(":::INFO::: {} did not have anything to derez for {}".format(me,card))
   elif len(rezzedOptions) == 1: derez(rezzedOptions[0])
   else:      
      if not confirm("A {} has just been installed and you need to derez one of your cards.\
                   \nYou need to double click on one of your rezzed card to derez it\
                   \n\nProceed?".format(card.Name)): return
      hijackDefaultAction.append(card)                
      showHijackQueue()
   
def MuertosGangUninstall(card):
   if not confirm("A {} has just been uninstalled and you may rez one of your cards.\
                \nYou need to double click on one of your unrezzed card to rez it\
                \n\nProceed? ('No' will forfeit this opportunity)".format(card.Name)): 
      notify(":> {} opts not to rez any of their cards for free".format(me))          
      return
   hijackDefaultAction.append(card)                
   showHijackQueue()
   
def chkFilmCritic(card):
   mute()
   if card.Type == 'Agenda':
      hostCards = eval(getGlobalVariable('Host Cards'))
      openCritic = None
      for c in table:
         notThisCritic = False # Checks if the current critic has an agenda hosted. If True, we skip this card
         if c.Name == 'Film Critic' and c.isFaceUp:
            for attachment in hostCards:
               if hostCards[attachment] == c._id: 
                  notThisCritic = True
                  break
            if not notThisCritic: # If we found a valid critic, we abort
               openCritic = c
               break
      if openCritic:
         if confirm("You have accessed {} and you have an available film Critic. Would you like them to host this Agenda".format(card.Name)):
            clearAttachLinks(card)
            hostMe(card,openCritic)
            card.highlight = InactiveColor
            flipCard(card)
            grabCardControl(card)
            return 'ABORT'   
   return 'OK'

def OfferRefuseBegin(card,server):
   if confirm("{} is making you an offer to run on their {}. Do you accept?".format(card.owner.name,server)):
      RunX('Run{}'.format(server), '', card)
      notify("{} has no choice but to accept {}'s offer and begins a run on {}".format(me,card.owner.name,server))
   else: 
      ModifyStatus('ScoreMyself', '', card)
      GainX('Gain1Agenda Points','',card)
      TokensX('Put1Scored-isSilent','',card)
      notify("{} is cowered and {} scores {} for 1 Agenda Point".format(me,card.owner.name,card))
      
def fifteenMinutesShuffle(player): # We need to remote call the deck shuffle or 15 minutes will always be placed on top of the R&D instead since the shuffle is too fast
   mute()
   remoteCall(player,'shuffle',[player.piles['R&D/Stack']])      
   
def NewsTeam(card):
   choice = SingleChoice("You have accessed a News Team! Do you want to take 2 tags or take this card for -1 Agenda Points?",['Take 2 Tags','-1 Agenda points'])
   if not choice: 
      GainX('Gain2Tags-isSilent-onOpponent', '', card)
      notify("{} opts to take two tags!".format(me))
   else: 
      GainX('Lose1Agenda Points-onOpponent-isSilent', '', card)
      ModifyStatus('ScoreMyself-onOpponent-isSilent', '', card)
      update()
      TokensX('Put1ScorePenalty-isSilent', '', card)
      notify("{} opts to score News Team for -1 Agenda Point".format(me))
      
def AllSeeingI(card):
   if me.counters['Bad Publicity'].value > 0 and confirm("Do you want to remove 1 bad publicity to prevent the All Seeing I?"):
      me.counters['Bad Publicity'].value -= 1
      notify("{} chooses to remove 1 bad publicity".format(me))
   else:
      for c in table:
         if c.Type == 'Resource' and c.isFaceUp: intTrashCard(c, c.Stat, "free", True)
      notify("The All Seeing I has trashed all of {}'s resources".format(me))         
         
def DrugDealer(card):
   drawMany(me.piles['R&D/Stack'], 1, silent = True)
   notify("--> {} triggers to hook {} up with 1 new card ".format(card,card.owner.name))
   
def Archangel(card):
   mute()
   targets = findTarget('DemiAutoTargeted-atProgram_or_Resource_or_Hardware-choose1')
   if len(targets): ModifyStatus('UninstallTarget', '', card, targets)

def ACH(card):
   if oncePerTurn(card, act = 'automatic') == 'ABORT': return 'ABORT'
   choice = SingleChoice("What do you want your {} to give you".format(card.Name), ["Do not use","Draw 1 Card","Gain 1 Credit"])
   if choice == 1: 
      DrawX('Draw1Cards', '', card)
      notify("{} uses {} to draw 1 card".format(me,card))
   elif choice == 2: 
      me.Credits += 1
      notify("{} uses {} to gain {}".format(me,card,uniCredit(1)))
   else:
      notify("{} opts not to use their {}".format(me,card))
   
def CBIRaid(card): 
   notify("{} is being raided by the CBI...".format(me))
   for iter in range(len(me.hand)):
      notify("-- Choosing {} card to place on top of R&D".format(numOrder(iter)))
      raidedCard = askCard([c for c in me.hand],"Choose next card to place on top of R&D")
      changeCardGroup(raidedCard,me.piles['R&D/Stack'])
   notify("The {} is completed".format(card))
   
