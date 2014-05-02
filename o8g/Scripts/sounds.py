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

import re

def playInstallSound(card, remoted = False):
   debugNotify(">>> playInstallSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if not remoted: remoteCall(findOpponent(),'playInstallSound',[card,True]) # Attempt to fix lag
   else: 
      if re.search(r'Daemon',getKeywords(card)): playSound('Install-Daemon')
      elif re.search(r'Chip',getKeywords(card)): playSound('Install-Chip')
      elif re.search(r'Gear',getKeywords(card)): playSound('Install-Gear')
      elif re.search(r'Console',getKeywords(card)): playSound('Install-Console')
      elif re.search(r'Virus',getKeywords(card)): playSound('Install-Virus')
      elif fetchProperty(card, 'Type') == 'Program': playSound('Install-Program')
      elif fetchProperty(card, 'Type') == 'Hardware': playSound('Install-Hardware')
      elif fetchProperty(card, 'Type') == 'Resource': playSound('Install-Resource')
      elif fetchProperty(card, 'Type') == 'ICE': playSound('Install-ICE')
      elif fetchProperty(card, 'Type') == 'Asset' or fetchProperty(card, 'Type') == 'Upgrade' or fetchProperty(card, 'Type') == 'Agenda': playSound('Install-Root')

def playEvOpSound(card):
   debugNotify(">>> playEvOpSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if fetchProperty(card, 'Type') == 'Event' or fetchProperty(card, 'Type') == 'Operation':
      if card.name == 'Stimhack': playSound('Play-Stimhack')
      elif card.name == 'Push Your Luck': playSound('Play-Push_Your_Luck')
      elif re.search(r'Transaction',getKeywords(card)): playSound('Play-Transaction')
      elif re.search(r'Job',getKeywords(card)): playSound('Play-Job')

def playRezSound(card):
   debugNotify(">>> playRezSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if fetchProperty(card, 'Name') == 'Archer': playSound('Rez-Archer')
   elif re.search(r'Sentry',getKeywords(card)): playSound('Rez-Sentry')
   elif re.search(r'Barrier',getKeywords(card)): playSound('Rez-Barrier')
   elif re.search(r'Code Gate',getKeywords(card)): playSound('Rez-Code_Gate')
   elif re.search(r'Trap',getKeywords(card)): playSound('Rez-Trap')
   elif fetchProperty(card, 'Type') == 'Upgrade': playSound('Rez-Upgrade')
   elif fetchProperty(card, 'Type') == 'Asset': playSound('Rez-Asset')
    
def playDerezSound(card):
   debugNotify(">>> playDerezSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if fetchProperty(card, 'Type') == 'ICE': playSound('Derez-ICE')
    
def playUseSound(card):
   debugNotify(">>> playUseSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   debugNotify("Keywords: {}".format(getKeywords(card)))
   if fetchProperty(card, 'Type') == 'ICE':
      if card.name == 'Pop-up Window':  playSound('Use-ICE_Pop-Up_Window')
      if card.name == 'Archer':  playSound('Use-ICE_Archer')
   elif re.search(r'Icebreaker',getKeywords(card)):  
      if re.search(r'AI',getKeywords(card)): playSound('Use-ICEbreaker_AI')
      elif re.search(r'Killer',getKeywords(card)): playSound('Use-ICEbreaker_Killer')
      elif re.search(r'Decoder',getKeywords(card)): playSound('Use-ICEbreaker_Decoder')
      elif re.search(r'Fracter',getKeywords(card)): playSound('Use-ICEbreaker_Fracter')
    
def playTurnStartSound():
   debugNotify(">>> playTurnStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if ds == 'runner': playSound('Runner-Start')
   else: playSound('Corp-Start')

def playTurnEndSound():
   debugNotify(">>> playTurnEndSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if ds == 'runner': playSound('Runner-End')
   else: playSound('Corp-End')

def playTrashSound(card):
   debugNotify(">>> playTrashSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if fetchProperty(card, 'Type') == 'Upgrade' or fetchProperty(card, 'Type') == 'Asset': 
      if card.controller != me: playSound('Trash-Opposing_Asset')
   if fetchProperty(card, 'Type') == 'Hardware': 
      if card.controller != me: playSound('Trash-Opposing_Hardware')
   if fetchProperty(card, 'Type') == 'Program': 
      if card.controller != me: playSound('Trash-Opposing_Program')
      else: playSound('Trash-Program')
   if fetchProperty(card, 'Type') == 'ICE' or (card.orientation == Rot90 and not card.isFaceUp): 
      if card.controller != me: playSound('Trash-Opposing_ICE')
      else: playSound('Trash-ICE')
   if fetchProperty(card, 'Type') == 'Resource' or (card.orientation == Rot90 and not card.isFaceUp): 
      if card.controller != me: playSound('Trash-Opposing_Resource')
      
def playButtonSound(buttonType):
   debugNotify(">>> playButtonSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if buttonType == 'Access': playSound('BTN-Access_Imminent')
   elif buttonType == 'NoRez': playSound('BTN-No_Rez')
   elif buttonType == 'Wait': playSound('BTN-Wait')  

def playPsiStartSound():
   debugNotify(">>> playTraceStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Psi-Start')
      
def playTraceStartSound():
   debugNotify(">>> playTraceStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Trace-Start')
      
def playTraceAvoidedSound():
   debugNotify(">>> playTraceAvoidedSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if rnd(1,10) == 10: playSound('Trace-Avoided_Zoidberg')
   else: playSound('Trace-Avoided')
   
def playTraceLostSound():
   debugNotify(">>> playTraceLostSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Trace-Lost')
   
def playRemoveTagSound():
   debugNotify(">>> playRemoveTagSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Tag-Remove')
   
def playScoreAgendaSound(card):
   debugNotify(">>> playScoreAgendaSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if ds == 'corp':
      if card.name == 'Breaking News': playSound('Score-Breaking_News')
      else: playSound('Score-Agenda')
   else: playSound('Liberate-Agenda')
   
def playDMGSound(DMGType):
   debugNotify(">>> playDMGSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   mute()
   if DMGType == 'Brain':
      if rnd(1,10) == 5: playSound('DMG-Brains')
      else: playSound('DMG-Brain')
   elif DMGType == 'Net': playSound('DMG-Net')
   elif DMGType == 'Meat':
      if rnd(1,10) == 10: playSound('DMG-Meat_Whilhelm')
      else: playSound('DMG-Meat{}'.format(rnd(1,4)))

def playRunStartSound():
   debugNotify(">>> playRunStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Run-Start')
   
def playRunUnsuccesfulSound():
   debugNotify(">>> playRunStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Run-Unsuccessful')
   
def playCorpEndSound():
   debugNotify(">>> playRunStartSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   #playSound('Run-End') # Disabled for now as it merges with other sounds usually.
   
def playAccessSound(ServerType):
   debugNotify(">>> playAccessSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   mute()
   if ServerType == 'HQ': playSound('Access-HQ')
   elif ServerType == 'R&D': playSound('Access-RD')
   elif ServerType == 'Archives': playSound('Access-Archives')
   
def playVirusPurgeSound():
   debugNotify(">>> playVirusPurgeSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound('Purge-Viruses')
   
def playClickCreditSound(remoted = False):
   debugNotify(">>> playClickCreditSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if remoted: playSound('Credit-Click')
   else: remoteCall(findOpponent(),'playClickCreditSound',[True]) # Attempt to fix lag
   
def playClickDrawSound(remoted = False):
   debugNotify(">>> playClickDrawSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if remoted: playSound('Draw-Card')
   else: remoteCall(findOpponent(),'playClickDrawSound',[True]) # Attempt to fix lag
   
def playDiscardHandCardSound():
   debugNotify(">>> playDiscardHandCardSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if ds == 'runner': playSound('Discard-Card_Runner') 
   else: playSound('Discard-Card_Corp')
   
def playGameEndSound(type = 'AgendaVictory'):
   debugNotify(">>> playGameEndSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   if type == 'Flatlined' or type == 'FlatlineVictory': playSound('Runner-Flatline') 
   
def playSpecialSound(soundName = 'Special-Push_Your_Luck-Fail'):
   debugNotify(">>> playSpecialSound()") #Debug
   if getSetting('Sounds', True) == 'False': return
   playSound(soundName) 
