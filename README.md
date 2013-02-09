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
* As the runner, use the blue card on your left to fight off traces. This is important for automation purposes (and it also looks nicer)
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

Wayland Corporation baits a criminal into a deadly ambush.
[![](http://i.imgur.com/u3YXqVyl.jpg)](http://i.imgur.com/u3YXqVy.jpg)

Kate Stealing the game from R&D.

[![](http://i.imgur.com/PgYecKsl.jpg)](http://i.imgur.com/PgYecKs.jpg)

Shaper running on a heavily fortifield Haas-Bioroid server.
[![](http://i.imgur.com/fYDVrl.jpg)](http://i.imgur.com/fYDVr.jpg)


Changelog
---------

### 2.1.11

* Installed corp cards will be autopeeked at
* Ending your turn will automatically use the green arrow function to signify the next player's turn.
* Tollbooth will now use Bad Publicity Credits
* Compromised Employee won't refill at the start of the corp's turn
* Parasite won't fail to install after a successful run but still take your money, MU and clicks


### 2.1.10

* Now multiple identical notifications will be grouped together and displayed in one line, with a mutliplier ('2x', '4x' etc in front)
  Here's how it will look when Crypsis breaks an Archer for example
  
  ![](http://i.imgur.com/8uHUwnU.png)
* Fix for Fetal AI charging the runner 2 credits when scored by the corp.

### 2.1.9

* Fix for Vamp eating less credits when using bad publicity credits
* When accessed traps are found in R&D and they can't trigger there, they won't be mentioned (e.g. Junebug)
* Better ordinal announces
* When game is won, it will inform the winner that it's submitting the stats.
* Added timeouts to stats submitting, in case they take too long.

### 2.1.8.1

* Made some modifications in reduceCost() to hopefully stop the "OCTGN stopped respondng" crashes, or at least make them more infrequent.
* Scoring agendas during access now won't ask you a second if you want to score them.

### 2.1.8

* **SIGNIFICANT** Accessing an ambush like Snare will now allow you to see what the corp writes in the chatbox, or any actions taken
* Accessed ambushes allow the runner to press "No" to send a "ping" to the corp to take action.
* Compromised Employee will now trigger from each ICE installed by an accelerated beta test
* Accelerated beta test will now announce which ICE it installed
* Encryption protocol will now not increase the cost of cards accessed from HQ
* Statistics will now start recording number of cards in the deck and number of agendas in the deck.
* Statistics will now record game names, which should be useful for tournament statistic gathering.

### 2.1.7

* Made custom fonts work again with the new version of OCTGN

### 2.1.6

* **IMPORTANT** Fixed a bug introduced in 2.1.5 which somehow made all attempts by the runner to declare their link give a python error.
  (I do not understand how nobody has reported it yet. Wasn't your traces failing?)
* Now cards which reduce costs via credits, announce how many credits they used.
* When BP is used to reduce costs, this is also announced.
* Fixed some broken issues with reducing costs (from multiple braintrusts or Encryption protocols for example). 
  

### v.2.1.5

* Fix for Rabbit Hole ability not costing any credits.
* Fix for tinkering revealing an ICEs name.
* Can now Inspect Opponent's card with "Inspect Target"
* Fixed TMI not derezzing itself after a failed trace
* Fixed Sherlock returning programs on top of the corps deck (bug #101)
* Trace boosting now mentions if the cost was reduced (feature #102)

### v2.1.4

* Effects which reduce or increase cost (Stimhack, Bad Publicity, Encryption Protocol etc) now mention their reduction in the announcements
  Those cards also inform you of the final amount of credits you're going to pay from your pool when you trash cards during access
* Fixed the "Pay and Rez" action always rezzing for free
* Fix not being able to setup the game a second time (i.e. after a table reset)
* Added some code which hopefully catches and fixes broken identity/trace card before it gives an error. 5 test games resulted in 0 bugs due to borked identity/trace card.
* Tollbooth now uses money from Bad Publicity and Stimhack (bug #95)

### v2.1.3

* Also fixed bug which made bad publicty credits sometimes be spent twice.

### v2.1.2

* Fixed Grimoire/Noise's abilities not triggering automatically

### v2.1.1

* Fixed creating remote server giving a python error

### v2.1.0

* **SIGNIFICANT:** Card can now be hosted properly on other cards. Cards which require a host will not be able to be played, unless you've targeted an appropriate host for them
  This affects cards like Parasite and Personal Touch but on the background it also is working for Daemons like Djinn.
  A hosted card will be trashed if its host ever leaves play. You don't need to do it manually anymore. 
  This is important because now trashing a Djinn which hosts programs will trash all its hosted programs as well. Yes, this will also cascade on nested Djinns as it should ;)  
* **SIGNIFICANT:** There's a new function which allows the runner to access cards in a server. It's in the table menu under "Access Target".
  You should use this after you've just had a successful run on a server and the Corp has passed on rezzing or triggering any abilities.
* Workaround for the borked traces and identities
* Trashing Djinns should now calculate MUs correctly.
* Fixed Spinal Modem not working at all
* Accessing cards now show you the final cost you're going to pay after all bonuses and penalties from other cards. It will show it in the form of "Pay 0 to trash (4-4)". 
  Cards like Stimhack and Bad Publicity are considered to be reducing the cost for this purpose.
* Cards can now affect the costs of your opponent
* Card effect can now increase the costs as well as decrease them
* Accessed card effects can now have the full range of scripting associated with them (e.g. Fetal AI). 
  When the runner accesses traps such as Junebug, it will reveal itself like a snare and allow the corp to use it.
* Swapped the Targeting functions for the more modular ones I developed for SW:LCG
* Players have the option to bypass the restriction on which cards can be trashed, when using the  "Pay to Trash" action.
* Removed the warning about trashing the opponent's cards. Never saw that being an issue after all and it's one extra click every time.
* Added the delayed_whisper() function
* Socred Agendas finally reset their positions after the game setup.
* Added a fix for the fonts for OCTGN 3.0.1.27
* Added fix so that only I can use the debug function, and not when I'm just in the game.

### v2.0.1.2 

* Fixed Spinal Modem working outside of runs

### v2.0.1.1

* Fixed cards like Mandatory Upgrades giving their effects to the runners.

### v2.0.1

* Stats should now be able to submit again
* Decking defeat is now collected as well

### v2.0.0

Big update which falls at the same time as What Lies Ahead. The most significant update is in the way traces work

* **SIGNIFICANT:** Traces are now automated. When the runner uses the trace card after being traced, the game will then calculate who wins
* **SIGNIFICANT:** Cards which trace now prepare their post-trace effect. Depending on who needs to win for it to fire, it will activate after the runner calculates their base link and compares with the corp's trace.
* Stats now include the subtitle in the name of the winner, in order to differentiate between identities in the same corp faction.
* What Lies Ahead added and scripted.

### v1.1.18.1

Fixed issue where succeeding the run would not jack-out immediately on next action, requiring an extra shortcut press

### v1.1.18

* Face-down Unique card now can be played when another face up unique card exists. (Bug #69)
* Unique cards also use their restrictions on rezzing as well
* Setting up the game does not give your opponent an opportunity to glimpse cards in your deck (Bug #67)
* **SIGNIFICANT:** After popular demand, I've stopped automated exposes from opponents. This is to avoid mistakes from people rushing their actions without reading the pop-up windows. Now the game will just announce the attempted expose, and the owner needs to do it manually.
* Fixed #66

### v1.1.17

* **SIGNIFICANT:** Runs work slightly differently now. [F3] does not jack-out the runner as well, but merely triggers the successful run effect (Gabriel, Desperato, Bank Job etc). This means that you can use both Bad Publicity tokens and Gabe's/Desperado ability at the same time to trash cards for example.
* Because [F3] does not finish a run, this needs to be done afterwards with [ESC] or by taking your next action. If you've pressed [F3] and take one action, the game will automatically jack you out (so for most players the gameplay should remain the same)
* Added a function to access a card from HQ [Ctrl]+[Q]. Don't use that before confirming with the corp.
* **SIGNIFICANT:** Now running central servers will automatically trigger their default access command. A confirmation window will pop-up if the runner has successfully run and ask them if they want to use that.
* Because of the above, if the runner opts to use cards which replace normal access with their own effects (Account Siphon for example), then the prompt for normal access won't be brought up.
* Cards which have optional effects which replace the normal access, now stop other cards from triggering them again (e.g. having two bank jobs on the table)
* When asking you to use optional effect, the game will also inform the player how many tokens each card has (to allow you to select the right bank job if you have multiple for example)
* The game announces the player's available credits at the start of their turn. Should make take-backsies a bit easier.
* Cell Portal should now announce its name when used

#### v1.1.16.2

Another attempt to fix the WinForms not appearing over OCTGN sometimes.

#### v1.1.16.1

* One-per-turn cards now refresh at the start **and** and of your turn, to be usable even on the opponent's turn (i.e. Net Shield).
* Closing the dialog for Accessing R&D cards (with X) does not force a trash now.
* Grimoire will now automatically place a virus counterson Virus cards you install.
* Fixed Stimhack not getting counters when running on a remote server without targeting it first
* Made some changes which hopefulle ensure that winforms spawn on top

### v1.1.16

* Added code to be able to submit statistics, filtered by tournament/league
* Fixed bug when accessing cards from R&D and paying to trash assets/upgrades, causing the next cards to be placed at the wrong index.

#### v1.1.15.6

* Fixed bug which sometimes caused the R&D to not be sorted correctly after a runner access where they paid to trash a card.

#### v1.1.15.4

* "Debug Card" now force refreshes a card's scripts and should work better on bugged cards.
* Inspect Card should now work on face-down cards better.
* End of Turn will now not discard revealed cards
* End of Run will now not clear highlights anymore
* Game will warn you if your opponent has a far too old version of the game.
* Game will inform more forcefully if you played more MUs than you have
* No more python errors if a players closes the trace reinforce window from an autoscript
* Fixed a bug which makes it possible that a player will take the identity name of their opponent

#### v1.1.15.3

* R&D Access also switched to the new WinForms.
* WinForms in general modified to look more like the built-in dialogs of OCTGN.

#### v1.1.15.2

* Added Switch in the game menu to turn the new custom forms ON/OFF, for those who preferred the old way with typing numbers
* Moved the trash card options to the root of the main menu and replaced the "Trash Target..." shortcuts with [del] and [ctrl][del] to be the same as normal trashing your own cards. So now to pay and trash an opponent's card, all you need to do is target it and press [ctrl]+[del]

#### v1.1.15.1

Small fix to allow the new custom forms to work with fullscreen OCTGN as well.

### v1.1.15

* **SIGNIFICANT:** We've got a new Multiple Choice Window, with nice buttons and everything. No more putting numbers in the field and limited to 9 chars. Just put as much as you want and go!
  * Further to the above, each option is now labeled nicely in a way that should be easy to understand what it does.
* Now information towards the player will be put in a special window with a single "OK" button. Should avoid confusions about yes/no which is not needed.
* Generic runs also use a form for selection of the target, with radiobuttons.
* **WARNING:** The above two windows, __rarely__  end up spawning behind your OCTGN window. In case you double click on a card and OCTGN seems to freeze, check if a new window has opened behind it before panicking!
* Now Damage inflicting effects will put out a notification just before they're about to do it. This should give a heads-up to the victim, in case their opponent does not inform them.
* Fixed the first Tollbooth effect which was confusing newbies.
* **SIGNIFICANT:** The Trace functions now automatically take their costs and announce their total Trace/Link strength. You do not need to double click on the Trace card a second time to Pay the cost. 
  * The Trace Card remains as a fake button though.

### v1.1.14

* Tinkering now should put all types on the ICE and then clear them at the end of the turn.
* On cards with multiple options, players can now put them all at the same time as a long number. So if the player wanted to boost crypsis 3 times and then break 2 subroutines, they would put 11100 in the field.
* Added option to concede in the game menu. This is to allow players who are losing badly to end the game prematurely and still store their stats.

### v1.1.13

* Cover card now should appear unless the target card is on the table
* End Run functions should now clear markers for both players
* When finding an illegal card in one's deck, it shouldn't just mention "card" anymore
* Tinkering should be able to put two traits on an ICE now
* Rabbit Hole now automated
* Playing modded should now not try to use Kate as well. Modded will go first and Kate will be used only if there's not enough reduction.

### v1.1.12

* When the game tries to read the properties of an opponent's cards, the game will now cover them with a fake card to avoid the opponent reading them
* Cards like Lemuria Codebreakers will now use their costs, even if their effects are countered by the opponent
* Better stats recording

### v.1.1.11

* Quick fix for cards which didn't announce their effect correctly (Eg. Armitage Codebusting)
* Jacking-Out now clears temporary markers (e.g. Icebreaker strength bonuses)
* Some other superficial fixes

### v1.1.10

* Added Functionality for fetching all card scripts from the github repository
* Now damage prevention effects have a chance to be activated by the one doing damage, during damage prevention. The game will ask if you want to activate them for yourself (or your opponent). Should solve issues of Net Shield not able to protect you from a Snare during R&D access due to the confirm window.
* Fixed #29
* Fixed #28
* Couldn't replicate #26. Assuming old def.
* Cards which trash themselves when empty should mention it all the time now
* Inspect now reports RunStart And RunEnd automations
* More Shortcuts
* Statistic gathering

### 1.1.9

* Added MOTD and DidYouKnow functionality
* Fixed Haas Bioroid tapping on opponent's installs
* Fixed Heimdall doing damage to the corp.

### 1.1.8

* **Important: Big change in the way Runs work**. Now Runs Start with the special actions on the runner's menu ([F5] to [F9]) or with actions cards. 
  * Once the run has ended, the runner must press either [Esc] to signify a failed run, or [F3] to signify a successful one. When this is done, abilities on cards which trigger from that (e.g. Medium, Gabriel etc) will automatically fire.
  * If the corp ends the run with an ICE, they __should__ use the subroutine on the ICE to do it. This will automatically end the run and trigger card abilities as well (e.g. Stimhack)
* If the runner uses an action which runs at any target, the game will automatically pick the first server they have targeted. If the runner has not targeted a server, the game will ask for input
* Removed all manual effect from cards which triggered after successful runs, like Gabriel and Desperado. Use the Finish the "Run succesfully" action ([F3]).
* Because of the above changes, Bad Publicity credits now work better. They get put on your runner identity as markers, and used whenever you pay costs. Once the run ends, they are removed.
* Moved Brain DMG counters to the Identity card and disabled Runner's Counter Hold for now since it was not really used.
* Added a small whisper when you have started playing a card from your hand. This will let you know if the effect has started and you need to wait, or if it didn't start at all.
* Finished migrating counter and group icons to vector based. Let me know if you find any improvement over them.
* Added new actions to the markers menu to add Power, Virus and Agenda Markers. Removed some obsolete actions.
* Added version checking. From now on, during the first setup, the game will inform the player if a new version is available to download.


### 1.1.7

* Runner looking at corp's deck now mentions the amount of cards.
* Tried to make the card properties storing function more robust and less likely to break your card properties
* The Card Debug will now also try to repair the card properties if possible. Try using the card again afterwards to see if it works
* Runner hitting an ambush during accessing cards from Corp's will now send the ambush to the table for the Corp to use.
* Having spectators should now (theoretically) not bork the system.


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