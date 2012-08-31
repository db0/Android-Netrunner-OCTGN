Android:Netrunner LCG plugin for OCTGN
=========================
The latest reboot / reimplementation of the much loved franchise is coming to OCTGN. Stay tuned for updates

Gameplay
--------

Some basic instructions on how to use the new system will be forthcoming, but things should be fairly intuitive anyway. Some basic things to remember

* __The corp should be "Player [A]"!__ Otherwise your card placement will be on the other side. Don't forget to set that in the pre-game lobby!
* First thing you do after you load a deck is Setup (Ctrl+Shift+S)
* At the start of your turn, declare it with F1
* At the end of your turn, declare it with F12. Make sure the game announces that your turn has ended and is not expecting you to discard down to your max hand size ;)
* Play/Install cards from your hand by double-clicking them. Use cards on the table in the same way. 
* Always try to Trash or Uninstall cards by using the relevant function in the menu (e.g. 'del' key)
  * If you want to trash the card of an opponent, _first let them know_ then target the card (shift+click) and use the "Trash Target" options in the **table menu** (i.e. right-click on an empty spot on the table)
* Only ever drag & drop cards from your hand to the table, or from the table/hand to your trash, if there's no other way.

And some more advanced stuff:

* If you're the corp, remove all viruses by double-clicking your "Virus Scan" card. If you're the runner, remove Sentry markers by double-clicking on your "Technical Difficulties" card.
* Most card will automatically trigger their abilities when played/scored/rezzed so you don't need to do anything else. Pay attention to the notification area for messages from them.
* Cards with abilities which increase your MU, Hand Size, etc will automatically increase it when they come into play and reduce it when they go away, as long as you don't drag&drop them in or out of the table manually. Use the built-in commands for that. Rez, Derez, Trash etc
* Cards with abilities you activate while they're in play (like programs, agendas, upgrades etc) will trigger them when you double-click on them. If they have more than one ability (such as most icebreakers), the game will prompt you to select one and pay the appropriate cost.
* Cards which reduce the cost of other card's abilities, will also automatically work. If you have a card which has tokens which can pay the cost for activating icebreakers, they will be automatically used when you use one such ability. If you have more than one of these cards which can affect such costs they will be triggered in the order you put them on the table. If you wanted to use the tokens from another card instead, you can simply drag the token manually to the other card afterwards.
* There are cards which will automatically do damage to your opponent and thus discard random cards from their hand. Due to the way OCTGN works, this may crash the game if you opponent was manipulating the same card. There is a warning before all such damage that will warn you to inform your opponent to be hands-off while the effect is in progress. This warning will also give your opponent the opportunity to play cards which prevent damage.
* Yes, cards which reduce damage taken have been automated and work automatically depending on the kind of damage you take. As before, they too get triggered by the order they've been put on the table, so if you didn't want to lose the counters from one particular card, just drag them in from the card you did want to use.
* Some cards require that you select a target from the table or your hand. Do this before you play or activate the card. If you don't the action will abort and the game will inform you to select your targets first.  As always, keep your eye on the chatbox for such warnings.
* Cards which have effects which trigger at start/end of turn (i.e. refilling bit markers on them) will automatically work.
* Cards which put markers on a player, which __themselves__ have an automated ability (i.e. Fang, Baskerville, Armageddon etc) will _also_ automatically work.
* If you don't like some or all the automations, you can disable some or all of them. Go to the game menu, and you can disable damage automations (i.e. your opponent will have to use the damage options manually), Damage Prevention, Turn Start/End automations and Play/Score/Rez Automations (i.e. mostly everything). If you find that you'd rather do everything manually, just disable all of them and you'll have an experience as with most generic card game engines.
* Cards with multiple effects will request you to select one of them when you activate them. Select an ability by putting their number in the window that pop's up. You should be able to get the idea of which ability is each from the parsed script.

Phew, that should be the most basic things about the new automations. If you're not sure if a card is automated, simply use the 'Inspect' function and the game will inform you of the details.

Enjoy!

Screenshots
---------
(Click for larger size)

[![](http://i.imgur.com/GFD0Ll.jpg)](http://i.imgur.com/GFD0L.jpg)

[![](http://i.imgur.com/WPjZpl.jpg)](http://i.imgur.com/WPjZp.jpg)

Changelog
---------

### 1.1.6

 * Exposing a card now puts a white highlight, so that you don't confuse it with a rezzed one
 * Better multiple choice options
 * Using the subroutine icons is more fine tuned to ICE abilities (requires new patch)
 * Replaced the Agenda Points, Tags and Bad Publicity Counters with Vector based transparent icons in order to fit in with the rest.
 * Mulligan now also clears you dictionaries. Lets see if we get funky cards again
 * Added a "Card Debug" option when right clicking on cards. Use it when a card does not behave correctly (e.g. an ICE is not placed sideways) and [open a bug report](https://github.com/db0/Android-Netrunner-OCTGN/issues) with the text reported, what you were doing, and what had happened just before.
 

### 1.1.5

* Fixed bug with targeted card crashing when checking if the target is rezzed or not.
* Added help functions which puts some reference cards on the table.
* Exposing opponent's card now puts out a confirm window to check that the opponent does not have reactions

### 1.1.4

* Fixed a typo which prevented the runner form trashing upgrades.
* Private Security Force should now use an action for its ability
* NBN should now properly put credits to use for tracing
* Added an extra ability to Femme Fatale to pay X credits (1 per subroutine to announce breaking an ICE}
* Crash Space will now automatically pay to delete tags
* Hunter now has an ability to add tags as well.
* Fixed Shadow's ability crashing on use
* Added two new runner-only actions.
   * Action to access top X cards from Corps's pile and score/trash any you want. Runner will be prompted for each.
   * Action to score all Agendas in Archives. This will also send the Hidden archives into the Face-up ones.
* Looking for valid targets will try to avoid turning cards face up if it can do so. This should avoid a slow game giving a small window for your opponent to see your cards.

### 1.1.3.1

* Fixed start of turns effects not working anymore
* Fixed a nasty bug I introduced in 1.1.3

### 1.1.3

* Added Mulligan function on the hand context menu
* Added Switch to turn the Triggered abilities ON/OFF. Might improve performance if playing each card takes too long.
* Added new function to rescan the table. Might fix weird issues I've noticed sometimes, where card end up thinking they're of different types.
* Fixed bug where Wayland Ident would tap on opponent playing cards (but not give any money)
* Trashing Agendas will now take away their points and announce that.
* Added a check so that reduceCost() is not called if the cost is 0 anyway. Should improve performance.
* Added a whisper in the damage step, to let the current player know it's being applied.

### 1.1.2.3 

Fixed a bug where ICE would not be installed sideways in slow connections

### 1.1.2

* Fixed some automated abilities triggered by other cards not activating (like "Shipment from Mirrormorph")
* Accelerated Beta test didn't work. It trashed ICE.Added delay rnd loop to make sure it can see the card type it checks. Hopefully it works better now.
* Fixed a run started from a card effect costing 2 clicks.
* Accelerated Beta Test's ability was made optional
* Made Wayland Consortium Idenity work
* Posted Bounty is now optional on scoring
* Fixed Security Subcontract being able to trash also unrezzed ice as long as you targeted it.
* Noise's ability now works automatically. It didn't work before cause I'm an idiot.


### 1.1.1

Fixed the Jinteki home doing 2 damage per scored Agenda instead of 1

### 1.1.0

Added Automations for almost all the cards. 

Also a truckload of other small bugfixes and improvements

### 1.0.0

Cloned from Netrunner-OCTGN 3.0.0. Starting port.