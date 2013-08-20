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

def playInstallSound(card):
   debugNotify(">>> playInstallSound()") #Debug
   if re.search(r'Daemon',getKeywords(card)): playSound('Install-Daemon')
   elif fetchProperty(card, 'Type') == 'Program': playSound('Install-Program')
   elif fetchProperty(card, 'Type') == 'Hardware': playSound('Install-Hardware')
   elif fetchProperty(card, 'Type') == 'ICE': playSound('Install-ICE')

def playRezSound(card):
   debugNotify(">>> playRezSound()") #Debug
   if fetchProperty(card, 'Name') == 'Archer': playSound('Rez-Archer')
   elif re.search(r'Sentry',getKeywords(card)): playSound('Rez-Sentry')
   elif re.search(r'Barrier',getKeywords(card)): playSound('Rez-Barrier')
   elif re.search(r'Code Gate',getKeywords(card)): playSound('Rez-Code_Gate')
   elif re.search(r'Trap',getKeywords(card)): playSound('Rez-Trap')
   elif fetchProperty(card, 'Type') == 'Upgrade': playSound('Rez-Upgrade')
   elif fetchProperty(card, 'Type') == 'Asset': playSound('Rez-Asset')
    
def playDerezSound(card):
   debugNotify(">>> playDerezSound()") #Debug
   if fetchProperty(card, 'Type') == 'ICE': playSound('Derez-ICE')
    
def playTurnStartSound():
   debugNotify(">>> playTurnStartSound()") #Debug
   if ds == 'runner': playSound('Runner-Start')

def playTrashSound(card):
   debugNotify(">>> playTrashSound()") #Debug
   if fetchProperty(card, 'Type') == 'Upgrade' or fetchProperty(card, 'Type') == 'Asset': 
      if card.controller != me: playSound('Trash-Opposing_Asset')
   if fetchProperty(card, 'Type') == 'Hardware': 
      if card.controller != me: playSound('Trash-Opposing_Hardware')
   if fetchProperty(card, 'Type') == 'Program': 
      if card.controller != me: playSound('Trash-Opposing_Program')
   if fetchProperty(card, 'Type') == 'ICE' or (card.orientation == Rot90 and not card.isFaceUp): 
      if card.controller != me: playSound('Trash-Opposing_ICE')
      
def playButtonSound(buttonType):
   debugNotify(">>> playButtonSound()") #Debug
   if buttonType == 'Access': playSound('BTN-Access_Imminent')
   elif buttonType == 'NoRez': playSound('BTN-No_Rez')
   elif buttonType == 'Wait': playSound('BTN-Wait')  
   
def playTraceAvoidedSound():
   debugNotify(">>> playTraceAvoidedSound()") #Debug
   playSound('Trace-Avoided')
   
def playTraceStartSound():
   debugNotify(">>> playTraceStartSound()") #Debug
   playSound('Trace-Start')
   
def playScoreAgendaSound():
   debugNotify(">>> playScoreAgendaSound()") #Debug
   if ds == 'corp': playSound('Score-Agenda')
   
def playDMGSound(DMGType):
   debugNotify(">>> playDMGSound()") #Debug
   mute()
   if DMGType == 'Brain':
      if rnd(1,10) == 5: playSound('DMG-Brains')
      else: playSound('DMG-Brain')
   elif DMGType == 'Net': playSound('DMG-Net')

def playRunStartSound():
   debugNotify(">>> playRunStartSound()") #Debug
   playSound('Run-Start')
   
def playRunUnsuccesfulSound():
   debugNotify(">>> playRunStartSound()") #Debug
   playSound('Run-Unsuccessful')
   
def playCorpEndSound():
   debugNotify(">>> playRunStartSound()") #Debug
   playSound('Run-End')
   
def playAccessSound(ServerType):
   debugNotify(">>> playAccessSound()") #Debug
   mute()
   if ServerType == 'HQ': playSound('Access-HQ')
   elif ServerType == 'R&D': playSound('Access-RD')
   
def playVirusPurgeSound():
   debugNotify(">>> playVirusPurgeSound()") #Debug
   playSound('Purge-Viruses')
   
def playClickCreditSound():
   debugNotify(">>> playClickCreditSound()") #Debug
   playSound('Credit-Click')
   
def playClickDrawSound():
   debugNotify(">>> playClickDrawSound()") #Debug
   playSound('Draw-Card')
   


