Netrunner CCG plugin for OCTGN
=========================

Considered by most one of the best Card Games ever conceived, Netrunner is an asymmetrical Cyberpunk CCG that everyone should play at least once.

Note: This is just the game engine, you'll also need to download [the sets](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=212). If you've never played the Netrunner before, you can find [some links to check out here](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=208&sid=253a1e9b14f4c47f0796b3301fa117c6)


Changelog
---------

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
