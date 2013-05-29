Changelog - Android:Netrunner LCG OCTGN Game Definition
===============================================

### 3.1.7.x

* Added the new sweet sweet tabletop

### 3.1.6.x

* Fixed Xanadu not increased ICE rez costs
* Fixed Midseason Replacements not taking into account existing link

#### 3.1.6.1

* Slightly better tabletop

### 3.1.5.x

* Fix for Fetal AI damaging the corp.
* Added more opaque board.

### 3.1.4.x

* Added new background
* Added new board (Many many thanks to [Simon Gunkel](http://boardgamegeek.com/user/susuexp)
* Repositioned cards to fit with the new board.
* Fixed Mr. Li's talking about the wrong cards.
* Reworked code to avoid https://github.com/kellyelton/OCTGN/issues/878
* Changed the Virus Scan card.

### 3.1.3.x

* Fixed Darwin, Faerie, Deep Thought not having MU requirement
* Deck checking will now check for more than 3 same cards. (Kiv)
* Deck checking will now work for 40-card Corp decks (Kiv)
* Salvage Trace is 2, not 3 (Kiv)

### 3.1.2.x

* Midori will remove hosted cards (like parasites) from ICE that goes in your hand.

### 3.1.1.x

* Fixed Replicator

### 3.1.0.x

* New game definition for **Future Proof**. All cards are scripted.

* ##### Cards NOT automated:
  * R&D Interface (Just select the number of cards during R&D access)
  * Ruhr Valley (Just remind the runner to lose a click)

* ##### Trickier Automations
  * Indexing: It will work automatically but you won't see card text (no space). To see card text, once the automated indexing is complete, eight click on the corp's R&D and select "Take Control" and then right click again and "View top 5 cards". Once you're finished re-arranging, right click on it again and pass control back to the corp
  * Deep Thought: It will automatically announce the top card of R&D at the start of your turn if it has 3 or more viruses. Mouse over the card name in the chat to see it normally.
  * Midori: Target an ICE on the table and an ICE in your hand before you double click Midori.
  * Flare: Damage and ETR are done as part of the trace automations. However you trash a HW separately. Once the trace is complete, target a hardwar, double click flare and use its second ability.

* Changed card information lookup (via inspect function) to netrunnercards.info
* Added debug code to help me trace down the pheromones recurr. creds bug



### 3.0.4.x

* Force Trashing a bit more newbie friendly now

### 3.0.3.x

* Replicator not once per turn anymore

### 3.0.2.x

* Fixed error when accessing HQ and trying to look at more cards than there are in the corp's hand.

### 3.0.1.x 

(Finally I can advance versions properly)

* Grimoire should not trigger off of personal workshop anymore
* Djinn will now use tutoring automations

### 3.0.0.65

* Programs fetched with Test Run should now use abilities that trigger when they're installed (e.g. Femme Fatale)

### 3.0.0.64

* Fixed Pheromones reducing the amount your Account Siphon took

### 3.0.0.62

* **Significant** (Hopefully) fixed bug where card properties were being mixes around
* Accessing cards from HQ should be faster and also not give away if the card has been accessed before

### 3.0.0.52

* Fixed Pheromones paying for runs on every server
* No more "target missing" whine when simply pressing F5 to run a remote.
* Double clicking on a server to start a run will silently end any previous runs currently ongoing.

### 3.0.0.46

* Fixed game breaking when using tutoring effects (I hope)

### 3.0.0.x

* Game Definition converted to OCTGN 3.1 format.
* New game definition supports **Humanity's Shadow**. All cards are scripted as always.
* **Significant:** Starting a run on a server will now automatically draw an arrow to make it obvious. This should help communication and casting.
* The runner can now double click on a Remote Server to start a run on that server, like they could already do with central servers.
* **Significant:** Tutoring effects are now automated. This means that cards like Special Order and Test Run are also automated and can be used more fluidly. 
* Test Run's ability will now adjust memory for the programs it installs and automatically unistall them to the top of the Stack at the end of the turn or when double clicked.
* **Significant:** Implemented Cloud Computing. What this means is that cards like ZU and Creeper automatically adjust the player's ram according to how much Link they have as per their rules. No more forgetting how many MUs you're using.
* Braintrust should not reduce the cost of Draco's ability anymore
* Doppelgänger now ends the previous run before starting a new one. Shouldn't allow the game to be confused on where the runner is on anymore.
* Kate's ability will now be wasted for a turn if cards are installed via the Personal Workshop or Test Run first, as it should be.

### 2.3.2

* Added a new function under the "Rez" menu, where the corporation can secretly flag a card to be rezzed automatically at the start of their turn.
  Cards which cannot be rezzed at the start of your turn (say because you run out of money during the runner's turn), will just be ignored and inform you about it.
* Hopefully made card access stop reporting occasionally '?' due to network lag
* Trace/Link Boosting now announces that the player is in the middle of doing that, so that the opponent knows to wait.
* Programs which trash themselves as part of their use cost, now properly restore their used MUs (e.g. see Crescentus)
* Cards should be auto-peeked at on derezz and unexpose as well.

### 2.3.1

* Fix for bug where bad publicity would reduce the amount of credits Account Siphon stole.

### 2.3.0

* New game definition for **A Study In Static**. All cards are scripted.
* Aggressive Secretary will now not clear her advancement markers when used.
* Corp Trace will now reset the current trace base strength to 0. Use this after the runner uses a card like Disrupter.
* Tag Markers will now be added to the runner ID when they're tagged. This won't automatically happen if you manually modify your tags counter though, but it will update at the next turn start.
* Game will remind the runner if they are tagged at the start of their turn.
* Trace/Elusion effects now occur before the actual trace effects.
* Central Servers are now controller by the runner. Runners are now able to double click on a central server to start a run on it.
* HQ Access will now not reveal all cards at the same time.
* Scored Agendas are placed slightly further apart, to allow you to see their markers better.
* Parasite won't trigger anymore at the start of the turn if it's just came off PW. (See http://boardgamegeek.com/article/11686680#11686680)

### 2.2.3

* **IMPORTANT** bug fix about bad publicity.

### 2.2.2

* New Button Cards to help players quickly shout announcements to their opponent.
  The Various buttons are: 
  * 'Access Imminent': Use this before you press F3 for a successful run, if you want to give the corporation an opportunity to rez upgrades/assets or use paid abilities
  * 'No Rez': Use this as a corp to inform the runner you're not rezzing the currently approached ICE.
  * 'Wait': Use this if you want to stop the opponent while you play reactions.
  * 'OK': Use this to inform your opponent you have no more reactions to play.
* Femme Fatale will now use BP credits for her bypass ability
* Unique cards now won't take forever to rez
* Added a new error message to make sure players realize when their markers are missing
* Cyberfeeder won't pay for cards in Personal Workshop anymore
* Trace card placed more visibly for the runner
* Console now placed next to the runner and distinct from the other hardware
* Parasites on Personal Workshop should now properly install on hosts at turn start
* Parasites on PW should now get a virus if installed at start of turn
* Made warning messages about HQ, R&D and Archive access clearer.

### 2.2.1

* Fix for PW taking power counters on the corp's turn

### 2.2.0

* New game definition for **Cyber Exodus**! Almost all cards in the data pack scripted
  * Personal Workshop: 
    To use PW target a program or hardware from your hand and double click it.
    At the start of each turn it will either automatically take from a single card, or ask you for which to work on
    To manually spend money on a card, simply double-click the PW-hosted card you want.
  * Dinosaurus:
    Dinosaurus cannot at the moment host cards automatically if you target it and play the program
    Rather, play your program, and then target it and double-click Dinosaurus
* Changed the counters to fit the new colour scheme
* Player summary tab now also displays clicks and MUs. Summary tab has been squeezed a bit as well
* HQ Access will now ask how many cards to access (to work with Nerve Agent). The cards will be chosen randomly and placed altogether on the table temporarily while the runner accesses them.


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