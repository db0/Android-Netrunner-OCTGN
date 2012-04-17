Netrunner CCG plugin for OCTGN
=========================

Considered by most one of the best Card Games ever conceived, Netrunner is an asymmetrical Cyberpunk CCG that everyone should play at least once.

Note: This is just the game engine, you'll also need to download [the sets](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=212). If you've never played the Netrunner before, you can find [some links to check out here](http://octgn.gamersjudgement.com/viewtopic.php?f=40&t=208&sid=253a1e9b14f4c47f0796b3301fa117c6)


Changelog
---------

### 1.5.3

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
