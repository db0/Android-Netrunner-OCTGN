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

def chkSideFlip(player,groups):
   debugNotify(">>> chkSideFlip()")
   debugNotify("Checking Identity", 3)
   global ds, flipBoard, flipModX, flipModY
   ds = None
   for card in me.hand:
      if card.Type != 'Identity':
         whisper(":::Warning::: You are not supposed to have any non-Identity cards in your hand when you start the game")
         card.moveToBottom(me.piles['R&D/Stack'])
         continue
      else:
         ds = card.Side.lower()
         storeSpecial(card)
         me.setGlobalVariable('ds', ds)
   if not ds:
      information(":::ERROR::: No identity found! Please load a deck which contains an identity card before proceeding to setup.")
      return
   debugNotify("Checking side Flip", 3)
   if (ds == 'corp' and me.hasInvertedTable()) or (ds == 'runner' and not me.hasInvertedTable()):
      debugNotify("Flipping Board")
      if flipBoard == 1:
         flipBoard = -1
         flipModX = -61
         flipModY = -77
         table.setBoardImage("table\\Tabletop_flipped.png")
   elif flipBoard == -1: 
      debugNotify("Restroring Board Orientation")
      flipBoard = 1
      flipModX = 0
      flipModY = 0
      table.setBoardImage("table\\Tabletop.png") # If they had already reversed the table before, we set it back proper again
   else: debugNotify("Leaving Board as is")
   