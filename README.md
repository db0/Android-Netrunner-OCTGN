Netrunner CCG plugin for OCTGN
=========================

Considered by most one of the best Card Games ever conceived, Netrunner is an asymmetrical Cyberpunk CCG that everyone should play at least once.

Note: This is just the game engine, you'll also need to download [the sets](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=361). If you've never played the Netrunner before, you can find [some links to check out here](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=208&sid=253a1e9b14f4c47f0796b3301fa117c6)

Screenshots
---------
(Click for larger size)

A game in progress at v2.0.4

[![](http://i.imgur.com/yDKgGl.jpg)](http://fav.me/d4y88aq)

How the custom fonts look like

[![](http://i.imgur.com/1Zcjy.png)](http://i.imgur.com/1Zcjy.png)



Changelog
---------
### 2.0.8.2

* No more crashing scripts when player closes windows that ask for numbers
* Increased the chat font-size to 11 to be more visible on high resolutions (eg 1920x1080)

### 2.0.7

* Added ⏎ character on the chatbox, when the player takes an action, to be able to distinguish those notifications better.
  * Important, because of the above change, you'll have to delete your old chat fonts if you're on windows XP and see a square instead of the Enter character. Simply delete the ```%USERPROFILE%\My Documents\Octgn\Games\13568561-7a2e-4572-8f31-3d99580ab245\cmd64.ttf``` file.
* Paying Action now take into account your max actions (as modified by cards and the player) 
* Cards that have the "double" trait now correctly use two actions when played. (Toon)
* Fixed some wonky indentations.
* Replaced "Note:" with ":::Warning:::" to make them stand out more.
* Playing Hardware Deck or Unique cards now will confirm and trash existing such cards of the player (Toon)
* Player will now be prevented from drawing cards automatically if they have an effect which modifies the amount of cards they draw each time. (Toon)
* Added action to check errata and rulings for a card on netrunneronline.com (Toon)
* Added more autoscripting. (Toon)
  * Runs
  * Losing tags
  * Rolling Dice
  * Refilling Hand
  * Increasing your Actions Max.


### 2.0.6

* Changed chat font size to 10 and menu size to 11

### 2.0.5.3

* Made +1 and -1 card markers counter each other.
* Added two extra markers. Generic and Advance (Toon)
* Added two extra autoscripts for adding extra actions and generic counters (Toon)
* Added a function to add any kind of marker.
* Made deck checking work robustly in multiplayer

### 2.0.4

* Added custom fonts to be used with OCTGN 3.0.1.4

### 2.0.3

* Fixed automations for cards like Cortical Cybermodem.


### 2.0.2

* Cards with MU cost now announce how much it is when they installed, and return it back to their owner when they're trashed.
* Fixed +MU card giving double the bonuses.

### 2.0.1

* Agenda scoring should now work for the runner.
* Fixe bug where Corp Upgrades were being installed face-up
* Put a warning in case people try to start a game without a two-sided-table
* Scored agendas now moved to the scoring player's side and stacked.

### 2.0.0

The latest release of the co-operation between Db0 and toon. Netrunner 2.0.0 is released!

* Autoscripts are now working without errors. This means that many of the cards that do something fairly simple, like drawing 3 cards, or increasing your handsize, now do that automatically.
* Function to disable Autoscripts in the game menu
* New each card has only one "Keywords" field instead of 5 separate ones. This means that filtering cards by their traits is much easier in the deck editor. This will require [a patching of your existing sets](https://github.com/downloads/db0/Netrunner-OCTGN/Patch_2.0.0.o8p)

Due to the significant changes in this version, it is strongly suggested that you delete your OCTGN\Database folder after patching. OCTGN should automatically reinstall all your games the next time you start it (If not, just go to options, select Install on Launch and restart OCTGN)
Don't forget to download the latest markers file as well.

Also keep in mind that the current (as of 20/04/2012) stable versions of OCTGN do not support the custom fonts that are enabled by the game. If you see squares where you should be seeing characters, (or if you just want to experience the awesomeness) use the [OCTGN Beta 4](https://github.com/downloads/Gravecorp/OCTGN/beta4.zip).

### 1.5.11

* Added Commodore 64 fonts for the chat box

### 1.5.10

* Added modified [Cyberpunks Not Dead font](http://www.dafont.com/cyberpunk-is-not-dead.font) (with some specific unicode support). many thanks to Aurelius :-)
* Changed some wordings.
* Agenda Points scored now visible on player summary.
* Changed the hand "Trash Card" actions to "Trash/Archive" to be more descriptive. 
* "Move to Archives H" now is "Move to Face-Up Archives" since the Hidden archives are alread delt with the normal "Trash/Archive".

### 1.5.9

* Renamed some option to be more thematic
* Converted all bit references to unicode via new function
* Reworked the automation ON/OFF to use boolean and to be smaller.
* Added option to switch unicode bits on/off
* Added Unicode font as default to be used in the upcoming version of OCTGN(untested)

### 1.5.8

* Fixed playing or rezzing cards at no cost not putting it on the table.

### 1.5.7

* Fixed the card placing for a 2-player inverted table setup.

### 1.5.6

* Disabled Automations so that the game can be playable until they are finalized

### 1.5.5

* Made The "Declare Start of Turn", "Declare End of Turn" more central to the game. It supposed to work as follows
  * At the start of your turn, you press F1 to declare the start of your turn. This also reinitializes your actions and makes some further checks for mistakes
  * When you're done with your turn, you press F12 to declare the end of your turn. It does some further checks and if it realizes that you have more cards in your hand than your handsize, it puts you in the "End Turn Phase" where you have to discard your excess cards
  * When done with discarding, you press F12 again and after some internal checks, the game announces the end of your turn.
* The mandatory draw action has been removed as its own unique entity. It has been merged into the normal card draw action, but to work correctly you need to use the end turn, start turn actions appropriately.
* Added more unicode Action and Bit characters on the menu!
* Now runs, paying to remove traces and paying to discard resources costs an action
* Added action to change your Action limit per turn. THis is used when they are automatically refreshed at Turn Start.
* Added new hand action for card discard. This automatically places the cards in the right pile depending if you're corp or runner. It also shows thematic messages when done during the end-of-turn phase.

### 1.5.4

* Reorganized the context menu for the table
* Now drawing a card uses an action. Playes can use the Draw Many option to avoid this.
* Advancing a card now uses propely the payCost() and useAction() functions
* Muted some trace functions
* Added function for players to use an action and get a bit
* Started using unicode "Return" character to denote which options require the use of an Action.
* Started using unicode [Dingbats](http://www.alanwood.net/unicode/dingbats.html) 10102 to 10111 to denote which options require the payment of bits. The getBit() function also uses them in its message.
* Removed the Brain damage counter and now using only the hand size one. The hand size counter has the brain icon now.

### 1.5.3

* Changed placement of various cards for corp and runner to make more use of the board setup
* Renamed the "Trash" to "Trash/Archives(face-up)" and "Archives" to "Archives(Hidden)"

### 1.5.2

* Trimmed down the unused actions
* Implemented a better Actions notification, based on the Actions counter. When player does not have enough default actions, they will be warned. 
* Superfluous "Action #2","Action #3" etc removed in favour of a single "Declare Action" action.
* When a player plays a card from their hand, the game automatically uses an action.
* Implemented a new payCost() function that takes care of reducing the player's Bit Pool and informing if that's not possible.
* Made card payment go through the payCost action. This takes into accound "play for free" actions
* Added Ctrl+Shift+S shortcut to Setup Game.
* Archives H renamed to Archives
* Archives renamed to Trash
* Rez and Trash actions now properly use the payCost() function
* Modified the placement of the corp's 3 starting data forts cards.


### 1.5.1

* New intPlay() function that is more consise but has the same functionality.
* Fixed issues with modifying counters and generally integers not being converted
* Changed some calls to counters to their shorthand names for better readability

### 1.5.0

* Fork in github of the work done by Toon offline. This version included more automation, particularly when playing cards.

### 1.0.0

* Initial version uploaded to OCTGN forums. Compatible with OCTGN2. Made by Toon & Firwally.
