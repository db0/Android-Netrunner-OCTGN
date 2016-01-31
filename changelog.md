Changelog - Android:Netrunner LCG OCTGN Game Definition
===============================================

### 3.23.0.x

* New game definition for **Kala Ghoda**. As always, almost every card scripted!
* ##### Trickier Automations
  * Run Amok: Target ICE and Double-click Run Amok to trash it.
  * Street Magic: Manual use
  * Jesminder Sareen: Manual use
  * Mumbad City Grid: Manual use
  * Interrupt 0: Use to track how much you pay per ICE you break, but I can't automate this further. Lose money manually afterwards
  * Dedication Ceremony: Won't prevent you from scoring. Just don't do it.
  * Kala Ghoda Real TV: Will whisper the card to you. DC it to trash it.
* Archangel will not reveal face-down attachments on Peddler
* **Added NAPD MW List to influence calculations**



### 3.22.4.x

* Brain Chip will now give correct MU
* Cerebral Imaging will now give correct Hand Size
* Genetics Pavilion will only work while face up
* Clot shouldn't warn the corp from the peddler
* Heartbit will now provide its MU
* Assassin's second traced should work now
* Charman Hiro not active when scored
* Corporate Town fixed in multiple ways
* Film Critic won't activate while in the peddler
* Independent Thinking will now announce the correct amount of cards drawn.
* Off Campus Apartment won't give an error instead of announcing its effect.


### 3.22.3.x

* Always be Running will now remind you to run first click
* Fixed Archives Interface

### 3.22.2.x

* Fixed Adam's directives disappearing after trasing
* Fixed Independent Thinking not trashing cards and giving you 2 cards only for directives.
* 15 minutes will remove AP from the runner when reshuffled back in R&D
* Fixed Media Blitz
* Keegan should remove tags now
* Fixed Archangel 
* Wasteland should only trigger for runner cards. Unfortunately it cannot trigger for face down events so a manual use has been added as well

### 3.22.1.x

* Fixed more than 1 Film Critic not working
* Fixed Windfall bugging out
* Fixed Keegan Lane
* Fixed Team Sponsorship not seeking in Arc
* Fixed Trope firing on corp turn
* Fixed Safety First firing on runner turn
* Fixed Public Support scoring each turn
* Fixed successful runs failing when an untriggered checkpoint is on the table
* Fixed Off-Campus Apartment (Thanks @jemeador)
* Dir. Haas. Pet Project will now list cards which are in different piles
* Game will now show you how many credits you had when you started a run



### 3.22.0.x

* New game definition for **Old HolyWood**, **Universe of Tomorrow** and **Data and Destiny!**. As always, almost every card scripted!

Given the amount of cards in this set, [please check here](https://docs.google.com/spreadsheets/d/1opShzG9mUKnI_gkVyYAvrMHdG340V1LL6pMMqmriI3k/edit?usp=sharing) for how well each card functions. Cards not listed are fully automated.

Also did an update on how Maximum Hand Size is calcated, and now it works like MU, with it always auto-updating. Please let me know if you notice any bugs.

PS: Lacking templates for the mini factions, so all their cards are proxies as neutrals, except their IDs, which use factions. If you're any good, I'd appreciate getting some templates for those.

### 3.21.2.x

* Muertos Gang Member won't trigger an uninstall when discarded via Damage
* Stopped cards exiled via Chronos Protocol triggerring their onTrash scripts
* Stopped information leaking when uninstalling NEXT ICE
* Off-Campus app. will now trigger scripts on hosted cards
* Ghost Runner will install pre-reserved for stealth, to prevent making mistakes when trying to use credits.


### 3.21.1.x

* Fixed Gang sign

### 3.21.0.x

* New game definition for **The Underway**. As always, almost every card scripted!

* ##### Trickier Automations
   * Armand "Geist" Walker: Manual use similar to Exile
   * Drive By: Expose manual as always (wait for Corp). After an expose, either the corp can trash, or you can trash by double-clicking Drive By
   * Test Ground will derez all targeted cards. Make sure you target as many as you have tokens the relevant ones
   * Allele Repression: You can target the cards in HQ before you use it to speed up the process.
   * Marcus Batty: Manually use the subroutine is Psi succeeds

### 3.20.1.x

* Fixed Mandatory Upgrades and Self-Destruction Chips triggering after every advance
* Valencia and GRNDL now properly put BP

### 3.20.0.x

* New game definition for **Chrome City**. As always, almost every card scripted!

* ##### Trickier Automations
   * Immolation Script: Manual use. Target the ICE and Double Click Immolation Script to trash it.
   * Turntable: Manual use. Target both agendas and Double Click
   * Chrome Parlor: Manual use. Double Click before playing genetics
   * Analog Dreamers: Target the unrezzed card before pressing F3
   * Oaktown Grid: Manually use it just before the runner is about to access cards in this server.
   * Clairvoyant Monitor: Target the ICE before using the Monitor
* Added "Thinking..." notification with Ctrl+5
* Valencia VS GRNDL won't end with 2 BP for GRNDL
* Fixed Shehe infinite loop on hosting itself
* Comet playing double events will now cost you a click
* Fixed hosting Parasite giving errors

### 3.19.5.x

Moved to API 3.1.0.1

### 3.19.4.x

* Fixes Caissas not rehosting
* Double Brain-Tapping Warehouses shouldn't conflict anymore

### 3.19.3.x

* Blacklist shouldn't fire when unrezzed

### 3.19.2.x

* Fixed the game reporting the R&D empty after stealing TFP from a solo access

### 3.19.1.x

* Crisium Grid will clear its state if the run was unsuccessful
* Off-Campus Apartment will cost a click to use now
* Beach Party will not a click only on corp turn
* Hayley Kaplan will be turned sideways whenever you install a card, to remind you, you have done so. You can still DC her to play a card from hand.
* Comet will give MU and won't bug out when trying to use it.



### 3.19.0.x

* New game definition for **Breaker Bat**. As always, almost every card scripted!

* ##### Trickier Automations
   * Hacktivist Meeting: Trash will happen after card is rezzed, so if the corp doesn't have a card they can still play non-ice. Don't do it.
   * Off Campus Apartment. Use it like Personal Workshop, not like a Daemon. Target connection from hand then DC it. In case you've already played the connection, you can target it and DB the OCA to host it manually after the fact.
   * Haley Kaplan: Manual use
   * Comet: Manual Use
   * Turing: Lose clicks manually.
   * Should prevent the runner using automated effects to fetch specific cards from their Heap, but won't prevent AR Lab Access.
   * Breaker bay Grid: Manual use (Target card to rez and DC)

### 3.18.1.0

* Fixes text spam on retrieval.

### 3.18.0.x

* New game definition for **The Valley**. As always, almost every card scripted!

* ##### Trickier Automations
   * Clot: Not scripted but will remind the corp
   * Paige Piper: Manual use after you install a card
   * Adjusted Chronotype: Manual use
   * Enhanced Vision: Will show only the title of the card
   * Jinteki Bioteck: You will have to choose your department at the start of your first turn (You can also double click to do it before F1)
   * Negotiator: Break with Credits manually.
* Autoscripter switched to manual use to avoid triggering off of Heap/Stack installs.
* Leela won't score bounced Chairmen
* Gagarin won't trigger during runs on centrals.


### 3.17.5.x

* Corp cannot flatline due to brain damage anymore ;)
* Exclibur doesn't have the option to reveal grail ICE anymore.
* Some effects, such as Public Sympathy shouldn't trigger from Damaged cards in hand anymore.
* Mr. Li and Data Hound now use the nicer askCard() function


### 3.17.4.x

* Fixed multiple-chhoice hosting (e.g. Kaissas) revealing face-down ICE
* Fixed Data Hound (again)
* Fixed Witness Tampering
* Fixed Emergency Shutdown not peeking the card for the corp.
* Fixed Human First

### 3.17.3.x

* Fixed Gravedigger
* Corp cards installed unrezzed won't trigger resident effects anymore (e.g. Mandatory Upgrades giving you a click on install)

### 3.17.2.x

* Hopefully fixes the issue with Agendas being scored face down, or cards being turned face down after trash from play.
* Should fix MaxX malfunctioning


### 3.17.1.x

* Livence Acquisition will now install from HQ and Archives properly, and rez what is installed.
* DRT will not refuse to rez is runner is untagged
* Utensils should make runs now
* Various small bugfixes

### 3.17.0.x

* New game definition for **Order and Chaos**. As always, almost every card scripted!

* ##### Trickier Automations
   * Titan Transnational: Will always put an agenda counter. I don't see why not and it will speed up play.
   * Constellation Protocol: Manual use
   * Mark Yale, credit for spending Agenda Counter is manual use. When using his ability to spend agenda counters, he gives you automatically 3 credits (2 for ability + 1 for trait)
   * Space Camp: After it's triggered, double click on any of your cards to add an advancement counter.
   * Wormhole: Manually use the ICE you want after using Wormhole
   * Housekeeping: Just announces to remind the runner. Runner should trash on their own.
   * Satellite Grid: not automated. You'll have to take care of the relevant effects manually.
   * The Twins, doesn't check ICE sameness
   * Sub Boost: Double click on the sub boost to end the run
   * Dedicated Technician Team: Manual use. Double click to remove a credit
   * Edward Kim: Manual use but is mandatory, so make sure you do it.
   * Itinerant Protesters: Manual Tracking (for now)
   * Knifed/Spooned/Forked: You can use them to trash ICE if the corp is too slow. Target ICE and Double-Click
   * Eater: Will put marker to remind you, but will not prevent access. Just select 0 cards.
   * Hivemind: Cannot make it host the viruses everywehre, so if you want to spend them for something (e.g. Datasucker), just drag the marker there, or target that ICE and DC Hivemind to transfer the Virus counter.
   * Progenitor has 3 MU of RAM, but don't host more than 1 proggie.
   * Archives Interface: Manual Use. Do it before accessing
   * Qianju PT: Manual use for starting the effect
   * The dummy Sac. Clone card won't trash itself when used. Will fix later.
  
  
### 3.16.5.x

* Supercharges are now global

### 3.16.4.x

* Fixed R&D Agenda scoring bug
* Fixed warning about not controlling cards during HQ and R&D access.

### 3.16.3.x

* Fixed woman in the red dress
* Fixed server placement when table is flipped
* Stopped warning about controlling cards when accessing cards.
* Fixed Stealing a Future Perfect during multi-access runs causing the resumed R&D run to skip a card.

### 3.16.2.x

* Fixed the borked server and button images from the new changes to the custom card sizes of OCTGN
* Removed a lot of hacks to make card visibility work accordingly now that this has been addressed. HQ and R&D access should be faster now.

### 3.16.1.x

* IT dept should now work correctly according to the ruling and also clear its counter at turn's end.
* Test Run markers now cannot be moved to other cards (say, by mistake)

### 3.16.0.x

* New game definition for **The Source**. As always, almost every card scripted!

* ##### Trickier Automations
  * Markus: First subroutine just announces.
  * Turtlebacks: Manual Use
  * Shoot the Moon: Will rez all targeted ICE. Don't exceed the tags!
  * Self-Destruct will require that you target all cards in the server to get the appropriate trace value.
  * Sage doesn't put +1 tokens. Track strength manually.
  * Ioxidae: Manual Use
  * Due to the special circumstances on what constitutes a "Jack Out" in ANR its use is manual (e.g. it doesn't work on an ETR or if the runner just presses ESC after seeing an ETR they cannot break to speed things up)
* Agendas with an extra cost to steal will now show this cost on the selection window, and take into account cost reduction effects (e.g. Bad Publicity). They will also warn a runner trying to steal an agenda they cannot afford. This will also take into account a Scored Utopia Fragment.
* Personal Workshop should no longer provide MU from inactive or revealed cards.
* Nasir will clear BP and Stimhack creds.
* Hades Fragment will no longer reveal retrieved hidden archives cards.

### 3.15.2.x

* Fixed Kitsune

### 3.15.1.x

* Inactive cards won't provide MUs anymore (e.g. card hosted on Supplier) 
* Utopia Shard will trash Corp Cards now
* Gorman Drip won't get a counter from the mandatory draw anymore.
* Docklands Crackdown should trigger only once now
* Fester doesn't trigger on install anymore.
* Reuse shouldn't announce trashed cards anymore.
* Hades shard should work now
* Deus X can now be re-hosted on daemons if its used to prevetn net damage

### 3.15.0.x

* New game definition for **All that Remains**. As always, almost every card scripted!

* ##### Trickier Automations
  * Hostile Infrastructure: Manual Use
  * Executive Boot Camp: TurnStart Rez is manual use
  * Lycan: Not scripted. Track manually.
  * Snatch and Grab: Trace effects not automated, only announces.
  * Lela Patel: Manual Use
  * Zona Sul Shipping: doesn't trash automatically on tag


### 3.14.1.x

* Future Perfect being scored will now clear corp currents
* Fixed Origami MU Cost
* Architect will now show all 5 cards, but this will allow you to choose operations. Don't do it.
* Fixed Origami MU
* Fixed Autoscripter taking 1 click when removed.

### 3.14.0.x

* New game definition for **Up and Over**. As always, almost every card scripted!

* ##### Trickier Automations
  * Labyrinthine Server: Just Announces
  * Blue Sun: Will not consider cards which increase rez costs
  * Changeling: Not scripted. Track manually
  * Hades Fragment: Manual Use
  * Astrolabe: Manual Use
* SoT on LARLA should now trash before LARLA resolves  
* Woman in the red dress will now announce when the corp has finished looking at the card and left it in R&D.
* Data Dealer should now exile Shi.Kyu, but can also target Corp cards due to this. Don't!
* Social Engineering will now only get money from the target ICE
* Mutated ICE can now use Subroutines
* LARLA shouldn't clear runner currents anymore
* Port Anson Grid and Kitsune should now work (nobody played them until now?)

### 3.13.0.x

* New game definition for **First Contact**. As always, almost every card scripted!

* ##### Trickier Automations
  * IQ: Rez Cost is tracked but not STR. Track that manually.
  * Port Anson Grid: Not automated. Don't jack out.
  * The News Now Hour: Not automated. Don't play currents.
  * Manhunt: Manual Use
  * Wendigo: Not Automated. Track manually.
  * Order of Sol: Manual Use.
  * Hades Shard: Shards can be installed manually when you're about to access. Simply drag them to the table and they'll skip their cost, and set the run to succeed, bypassing all costs. Warning this will bypass all corp acknowledgement, so make sure you use it after the corp has given the OK to access.
  * Rachel Beckman: Won't trash automatically when tagged.
  
### 3.12.2.x

* The Foundry can find new pop-up windows now
* Fixed LLDS Energy Regulator use Cost
* Plan B shouldn't announce itself in R&D

### 3.12.1.x

* The Foundry should find Bioroids now.
* Enhanced Login Protocol shouldn't work for card effect runs now.

### 3.12.0.x

* New game definition for **The Spaces Between**. As always, almost every card scripted!

* ##### Trickier Automations
  * Targeted Marketing: Manual Use
  * Cerebral Static: Won't reduce Chaos Theory's MU.
  * Unscheduled Maintenance: Not Automated
  * Information Overload: Only trace is automated, since the runner chooses what to trash for the subroutines.
  * Scrubbed: Not Automated
  * Energy Regulator: Just Announces
  * Lag Time: Not Automated
  * Encrypted Portals: Doesn't add markers or anything.
  


### 3.11.1.x

* Fixed mother goddess not being unique
* Mutated ICE can now be used
* Same Old Thing will be shuiffled in by Levy
* NEXT Silver gets markers
* TWIY won't give 7 hand size on mulligan.

### 3.11.0.x

* New game definition for **Upstalk**. As always, almost every card scripted!

* ##### Trickier Automations
  * Near-Earth Hub: Manual use
  * Midway Station Grid: Manual use
  * Galahad. First action just reveals the grail ICE you've targeted from HQ. The ICE will remain in play until jack out, at which point it will trash itself. You can double click those ICE to use their routines.
  * Galahad will also give an error if you use a spawned galahad to end the run. Don't worry about it, it does no harm. I just can't be bollocksed to write the code around it.
  * Bad Times: Manual use. Just calc the new temp MU and trash accordingly.
  * Priority Events: Don't rules enforce being played as the first click.
  * Leprechaun: Doesn't enforce the number of programs. Just don't host more than 2.
  * Nasir Meidan: Manual Use. Target the ICE you've just encountered and double click him.
  * Eden Shard: Shards can be installed manually when you're about to access. Simply drag them to the table and they'll skip their cost, and set the run to succeed, bypassing all costs. Warning this will bypass all corp acknowledgement, so make sure you use it after the corp has given the OK to access.

### 3.10.5.x

* Fixed manually suffering damage
* Overmind-Scavenge fix

### 3.10.4.x

* Fixed Oracle may
* Fixed Account Siphon not trashing itself when not used

### 3.10.3.x

* Fixed TFP HQ-access bug

### 3.10.2.x

* Made Shi.Kyu actually pay for the amount

### 3.10.1.x

* Same old thing will now use extra click for double events
* Started providing more running tallies for credits in the log.
* Start of turn will also mention how many cards the player is holding in their hand
* End of turn will also mention how many cards the player is holding in their hand and how many cards are left in their deck.
* Oracle may should now properly reveal the card
* Shi.Kyu can now take an agenda tally to negative
* Players can choose to steal Shi.Kyu when the net damage is 0
* Scored Shi.Kyu can now be sold to Data Dealers.
* HQ Interruption due to the Future Perfect will now cause another HQ access if TFP was the last card accessed.
* Security Testing should now block accesses to the chosen server
* Security Testing should now pop-up a choice for the corp anymore.
* Security Testing now cannot activate in multiples from the same server

### 3.10.0.x

* New game definition for **Honor & Profit**. As always, almost every card scripted!

* ##### Trickier Automations
  * Tennin Institute: Manual use. Just target the card and double click it.
  * Shi.Kyu: This thing is particularly nasty in archives, with no good way to deal with it.At  the moment the corp will have to choose their payment while the runner is still accessing archives. If there's Agendas with Jinteki:PE and shocks involved, those will have to finish before the runner has a chance to respond to Shi.Kyu. Sorry but I can't do this any better. In case of confusion, use voice chat, or do things manually.
  * The Future Perfect: This will won't provide the normal scoring window. Rather it will score itself if the runner wins the PSI struggle.
  * Tenma Line: Manual. Drag the ICE accordingly.
  * Inazuma: Doesn't rules enforce.
  * Neotokyo: Manual use.
  * Tori Hanzo doesn't know where he is located, so he'll trigger on every net damage. Just don't use him if you're not supposed to.
  * Silhoutte: Manual use. Just target and double click her.
  * Express Delivery: It won't show you duplicate cards. So you may see 3 or less option to select if there were multiples on the top.
  * Logos: Manual use.
  * Bug: Double click it after the corp draws a card to get the card name in the chat. If the corp draws another card, you lost your chance.
  * Security Testing: Remotes are a bit tricky. If you select a remote,move your token to the selected remote afterwards. When successfully run it, target the server and double click on one of your security tests to take the money.
  * Mass Install: Will install all programs you've targeted. Just don't do more than 3.

### 3.9.2.x

* ABT will not trigger HB:ETF more than once
* Liz Mills will now use a click for her ability
* PSI can now use BP
* Paintbrush will clear its markers on Jackout.
* Stopped Corp pressing F1 too fast and drawing too many cards.
* Dir. Haas Pet Project now announces origin groups  

### 3.9.1.x

* Added the Draft IDs under the Promos set. Now people can use decks they've drafted elsewhere to play.

### 3.9.0.x

* New game definition for **Double Time**. As always, almost every card scripted!

* ##### Trickier Automations
  * NAPD Contract: Will allow you to steal it if you don't have enough money. Just don't.
  * Marker: Not automated.
  * Fall Guy: Not automated, just trash it instead
  * Singularity: Does not autotrash, so just ask the corp to trash all
  

### 3.8.3.x

* Fixed Scavenge MUs
* Fixed Alt-Kati Art

### 3.8.2.x

* Added Alt-Art for HB:EtF and Kati Jones
* Levy Lab Access will now trash events on the table (fixes #410)
* Blackmail now goes only on ICE (fixes #409)
* All LLDS Processor tokens will now be removed at turn end (fixes #404)
* Beta Test will now provide an option to not rez the ICE when having the opportunity (fixes $401)

### 3.8.1.x

* Added Fucking Quick Access [FQA] because dear gawd...

### 3.8.0.x

* New game definition for **Fear & Loathing**. As always, almost every card scripted!

* ##### Trickier Automations
  * Quest Completed: Target the card you want to access before playing it.
  * Tallie Perrault: Not triggered automatically when Operations are trashed. Just double click her when appropriate
  * Blackguard: Rez not automated. Corp has to manually do it after exposing.
  * Blackmail: Does not check for BP. 
  * Hemorrhage: Does not trash the card since the corp has to choose it. It just announces that the corp has to do it now.

### 3.7.10.x

* Access Granted Button now doubles as F3
* Fixed Indexing and Data Hound. Now spam RevealTo messages :(
* Fixed Junebug etc.
* Automated Deja Vu
* Added info when a retrieve script is ongoing.

### 3.7.9.x

* Fixed Proxy IDs Influence/Deck Size being reversed
* Sped Up Deck checking
* Automated Precognition
* Fixed Edge of World
* Fixed Data Hound

### 3.7.8.x

* Fixed Whizzard trashing R&D Cards

### 3.7.7.x

* Scripted Chronos Protocol IDs. You can now play with their weird effects normally!

### 3.7.6.x

* Cost increasing effects now activate before BP, which takes effect before recurring credits (unless cards are prioritized)
* Fixed Encryption protocol not increasing its own trash cost when accessed while rezzed
* Fixed Braintrust not reducing ICE costs.
* Jinteki:RP now doesn't cost a click when it cancels the run after the runner double-clicks to to run a remote without running a central first.


### 3.7.5.x

* More script speed optimizations.

### 3.7.4.x

* Script speed optimizations

### 3.7.3.x

* Fixed Oversight AI and Bioroid Efficiency Research.
* Removed some notify tickers as they're not that useful.

### 3.7.2.x

* Fix for start of turn slowness
* Added message if changing pile control takes too long
* Using a custom card ability multiple times rapidly should hopefully work better now.

### 3.7.1.x

* Keyhole now uses a click and hopefully made it so that you don't see "???" anymore
* Attachments will now follow their host when it's moved on the table
* Fenris now gived Bad Pub.
* Director Haas now doesn't trash scored Director Haas when rezzed.
* Director Haas can now be properly scored when trashed from R&D
* If both players have the same alias (local game?), game should not be confused about runner/corp clicks anymore.
* Shock works from the archives as well now.

### 3.7.0.x

* New game definition for **True Colors**. As always, almost every card scripted!

* ##### Trickier Automations
  * RSVP: Not automated. Just don't spend any credits afterwards.
  * Curtain Wall: Does not update its str visibly in any way.
  * Capstone: Target the cards in your hand then use.
  
* Added Quick Access mode. When this mode is activated, as a runner you do not need to wait for the OK from the corp before you succeed a run and access cards. 
  If the corp has not pressed OK or F3 yet, the first time you press F3, the game will automatically use the Access Imminent button. The second time it will proceed to access.
  Obviously, you're expected to give the corp time to react so don't go pressing F3 2 times, all the time just to rush through.  
  To activate Quick Access, simply add the **[Quick Access]** tag in you game name (including [square brackers] (**[QA]** also works) or enable it from the Game menu. 
  If the game is not tagged as **[Quick Access]** then only the corp can set it as such. The runner can only request it from the corp, and only once.
  If the game is tagged as **[Quick Access]** via the game name, then Quick Access cannot be disabled. This is to allow runners who want to play this way to do so, without being thwarted by the opposing corp. 
  
* Started using notifyBars. These should provide a notification about the flow of the game on the top to all players. Let me know if you like them.  
* Did a bunch of recoding to stop the error spam that was triggered lately. It's not perfect but things should be much better now.  
* New cards coming into play will now have an orange highlight. This is to allow the other player to easily see what is coming in-play, especially if the corp played a bunch of face-down cards.
* Discarding down to your max size after pressing F12, will automatically end your turn (because people kept forgetting to press F12 again)

### 3.6.5.x

Changed code to take controllership of piles when manipulating their cards,to avoid errors

### 3.6.4.x

* Added code for Supercharging Patrons

### 3.6.3.x

* Expert Schedule Analyzer now only works if the HQ run was initiated by that.
* Woman in the Red Dress now will announce if the corp drew the card.

### 3.6.2.x

* Fixed Running Interference Influence cost
* Grifter will now work without counters and will give 1 credit if you play it after you run (fixes #355)
* Jinteki and Data Leak Reversal now check for central server run validity
* Project Ares will now give BP when overcharged

### 3.6.1.x

* Scheherazade-hosted program should now use MU properly.

### 3.6.0.x

* New game definition for **Mala Tempora**. As always, almost every card scripted!

* ##### Trickier Automations
  * Deep Red: All Caissas will gain a little marker when they come into play. When you rehost that Caissa that marker will give you one click. If you don't rehost, that Marker will go away at the end of your turn. You should always rehost that Caissa immediately if you need to.
  * Hudson 1.0: Doesn't enforce it. Just make sure you only access one card.
  * Accelerated Diagnostics: *Phew*, OK, this card is kinda ambiguous of how it works (see http://boardgamegeek.com/thread/1086167/double-accelerated-diagnostics). At the moment this treats allcard being "looked at" as being in some sort of execution limbo. As such any further ADs you draw with AD, will draw fresh cards.
    Due to the nature of scripting in OCTGN this will cause problem with cards which need a target. In those cases you need to ignore the error and replay the card afterwards, or just look at your top 3 cards before you play AD and see if any card will require targeting and do it before you play AD.
    Same is true for some sort of SEA Source + Scorched Earth combo. You'll need to wait until the trace is complete before playing the SE or it will fail if the runner doesn't have a tag. And so on. 
    Please understand that this scripting cannot be perfect and don't request miracles.
  * Unorthodox Predictions: It's not going to enforce it, but it will put a token to remind you what you've chosen.
  * Sundew: Not automated. Just double-click on it to gain 2 credits.
  

### 3.5.3.x

* Resampled all sounds to 44100:2 to stop errors

### 3.5.2.x

* The Cleaners should not enhance meat damage when liberated by the runner.
* ABT should execute onRez automations now
* Damage enhancers (e.g. The Cleaners) now also affect manual damage.

### 3.5.1.x

* Fixed bug where trashing face-down cards would send them in the face-up archives.

### 3.5.0.x

* New game definition for **Second Thoughts**. As always, almost every card scripted!

* ##### Trickier Automations
  * Bishop: Its placement is not restricted. To rehost it, just target an appropriate ICE and double click it. 
  * CopyCat: It won't check for the duplicate ICE. Just make sure you're using it when you're allowed to.
  * Wotan: Since the runner decides which routines fire, they've not been put at options. The runner can simply trash their progs, lose money and so on.
  * Hellion Alpha Test: When the trace succeeds, the card will just remain on the table. Just target the resource and double click The Helion Alpha Test to return that card to R&D
  * Off the Grid won't actually prevent runs automatically. Just don't do it.
  * Profiteering will allow you to put >3 BP. Just don't do it.

### 3.4.6.x

* Server access will now be blocked until the corp gives the OK. After 3 requests to access, the runner has a chance to bypass an unresponsive corp (but don't do this unless you're sure the corp is not still thinking about it). Second attempt will also directly prompt the corp to acknowledge the run or inform that they're working on their reacts.

### 3.4.5.x

* Can now derez Agendas
* Reconnect() will now return ICE to their normal position, in case they get screwed.
* Plascrete carapace now comes with power tokens and their use is optional. When you're about to receive meat damage, double click the carapace to use a token and create a damage-prevention effect on the table. That damage prevention will disappear once you receive any amount of meat damage, so don't use the carapace all at the same time just to prevent the 3 incoming PSF damage.


### 3.4.4.x

* Added code that gracefully handles players manually moving cards into or out of the table.
* Because of the above, now moving your ID to the table at the start of the game, will trigger the game setup, which should make things easier to remember.
* Freelance coding contract can now target only programs
* Fixed bug where you couldn't access face-up corp assets and upgrades.

### 3.4.3.x

* Should not be able to access face-down ICE anymore if you have them targeted.
* Brain DMG Flatline should now happen only at end of turn.
* Added warning when corp approaches decking
* Card draw effects can now deck the corp, as long as they initiated the effect themselves.
* Advanceable trap assets should now not trigger from R&D or H&Q
* Amazon industrial zone can rez ICE now (Target the ICE you just installed and double click on the industrial zone to rez it at a reduced cost.)
* Plascrete will now be trashed when emptied of Tokens
* Rezzed Awakening Center ICE now works correctly when used 


### 3.4.2.x

* Ambush assets such as Snare or Junebug will now immediately pop-up a question window to the corporation asking if they want to trigger their effects. This should hopefully stop mistakes of the runner trashing the asset before one had a chance to use it.

### 3.4.1.x

* Table board will flip for the spectators as well now.
* Dinosaurus can now host programs as you play them from hand, as long as you have it targeted.
* Snitch now once-per-run
* Cards accessed from HQ should not retain their revealed highlight when returned anymore.

### 3.4.0.x

* Added and Scripted The Collective and Laramy Fisk ;)


### 3.3.9.x

* Choice Form Pagination now will happen at 7 buttons, to work with people with smaller monitors.
* Paginated multichoice window as well.
* Corp can't press F3 to succeed the run for the runner anymore. Instead this will just announe that the corp acknowledges a successful run.

### 3.3.8.x

* Rook should now properly host on unrezzed ICE

### 3.3.7.x

* Notoriety shouldn't trigger Jinteki's ability anymore

### 3.3.6.x

* Notoriety will now announce game victory and submit stats
* Jackson will now announce the cards from the face-up archives and how many were hidden cards
* Jackson will now inform from which pile each card is coming from during selection.
* Added a lot more sounds to the game, and changed some of the annoying ones

### 3.3.5.x

* Turn Change won't clear stealth and priority highlights anymore

### 3.3.4.x

* Caissa Programs should now work properly. First placed on the table and then hosted manually, using clicks

### 3.3.3.x

* Replaced Run Start sound with something more discreet
* Added Trash Resource sound
* Replaced "[Click] - Gain Credit" sound

### 3.3.2.x

* Added option to turn sound effects off/on.
* Replaced some sounds.

### 3.3.1.x

* Added first batch of sounds (See [The ANR sound effects project](http://boardgamegeek.com/thread/1023387/octgn-the-anr-sound-effects-project)
* Jackson Howard will not announce which cards he retrieves
* Jackson Howard can now retrieve less than 3 cards
* Archived Memories now Automated

### 3.3.0.x

* New game definition for **Opening Moves**. As always, almost every card scripted!

* ##### Cards NOT automated:
  * Project Ares (It will just an appropriate amount of agenda markers to reming you how many to trash)
  * False Echo (It will just announce what needs to happen, but the corp will have to do it manually)
  
* ##### Trickier Automations
  * Pawn: Its placement is not automated. To Rehost it, just target the ICE you want, double click it and select the first option
  * Rook: Its placement is not restricted. To rehost it, just target an appropriate ICE and double click it. It also does not increase costs, you'll have to take care of this manually.
  * Invasion of Privacy: When the trace succeeds, the runners hand will go on the table. As the corporation, target the cards you can and want to trash and press "Del" for each one. Then the runner can press 'Yes' to retieve their hand back.

* Disabled hand shuffling because I'm hearing reports about weird bugs coming from it.

### 3.2.12.x

* **Significant** Game will now flip the board if the corp is on position B, or the runner in position A. many thanks to OCTGN for implementing the API to make this possible.
* Deck checking will now happen on deck load rather than setup. Game will pop-up a window if you have an illegal deck
* Game will now auto-update the tags on the runner ID, even if they were modified manually
* Game now more robust if someone manually drags a card off the table. Game will now clear attachment links to prevent mess-ups.


### 3.2.11.x

* Made all pop-up warnings once-only
* Removed game action to hide newbie warning since they're all disabled after the first time now
* The Source and Chakana will now increase advancement costs
* Fixed Crash Space not properly trashing when triggered during damage
* Fixed Mulligan not shuffling correctly on single player.

### 3.2.10.x

* HQ access now adds larger artificial delay after each pick to obscure whether the runner has seen the same card in HQ before
* HQ will now be shuffled before runner access.
* Tested HQ Access randomness. [It works fine you monkeys](http://boardgamegeek.com/article/13122604#13122604)!


### 3.2.9.x

* Each new MOTD will only appear once to the player
* Game will now announce during setup if it's a league match or not
* Added a new action (Ctrl+Alt+A) to manually set or unset the match from a league


### 3.2.8.x

* Trashing a program hosted in the omni-drive should now restore the omni-drive's MU
* Research Station won't reduce your hand size when trashed from HQ/R&D

### 3.2.7.x

* Fixed Dir. Haas getting trashed from runner's score pile when the corp rezzes a second one
* Fixed Data Hound

### 3.2.6.x

* Howler and Awakening center will now trigger Alix
* Howler will now trigger compromised employee and ice analyzer

### 3.2.5.x

* Next Design's ability now split into two parts, so that you don't see the new cards before you play the ICE
* The Source will now trash itself upon agenda score and will cost 3 credits upon agenda theft.
* Cancelling a tutor effect won't leave your deck in the scripting pile anymore.
* Inti's +1 now costs 2 creds.

### 3.2.4.x

* Escher won't peek at ICE at jack out anymore
* Dagger will now use credits from only as many Cloaks as required.
* Added menu action to reserve a card's credits for Stealth-using cards. Such cards won't use their credits on anything but cards which explicitly use stealth credits

### 3.2.3.x

* All Events/Operations in play will now be discarded in-between clicks. Should allow people to use Same Old Thing on an even events they played this turn if they need to.
* Test Run should not wipe Sahsara credits anymore
* Scavenge can now pick the card just trashed
* Howler will now properly remove the marker from the Bioroid once the run ends.

### 3.2.2.x

* Omni-drive now replicatable
* Original Hasbro won't give 1 credit on setup anymore
* Checking archives when there's no agendas shouldn't error out anymore
* Haas pet project will now peek at the cards she installs
* Cerebral Imaging will now use our own credit count.

### 3.2.1.x

* Fixed Dir. Haas losing the corp's clicks even when trashed from HQ or R&D
* Dir. Haas Now scores at the runner's Pile.
* Dirty Laundry now gives the credits on JackOut
* Fixed Tyr Hand's Cost

### 3.2.0.x

* New game definition for **Creation and Control**. Almost cards are scripted.

* ##### Cards NOT automated:
  * Chakana (It adds viruses but doesn't increase Agenda costs)
  * The Source

* ##### Trickier Automations
  * Exile: double click the identity to draw the card. it won't do it automatically.
  * Escher: After succeeding the run, you will automatically take control of all the corp ICE. You cann now move them around. Once you jack out, control will pass back to the corp.
  * Exploratory Romp: Target the card you want before you press F3. It you haven't it will target the best possible match but it may choose wrong. In that case, just reverse the effect manually
  * Freelance Coding Contract:  Target the 5 programs from your hand before you play it
  * Scavenge: Target the card from your hand if you want that. Otherwise it will select the right pile smartly and ask if it's confused.
  * Monolith: Target the programs you want to install in your hand before you play it

* **Significant** Added scripting which allows the game to install cards. As such I've changed the way Modded and Shipment from Mirrormorph works. Now you need to target the card(s) in your hand before you play them, and they will install them automatically. This should bring these two cards in line with other similar effects
* Cards will now refill their credits before every other card. This means that your unused cyberfeeders will never refill after Darwin uses them for example.

### 3.1.11.x

* Fixed Pop-up window/tollbooth not using stimhack/Pheromones money
* If you're doing damage and your opponent has a damage prevention card, a confirm window will appear and ask if to wait until they decide to use damage effects or not. 
  
  If you press 'No', a "ping" will be sent to the opponent to remind them to use their damage prevention effects, similar to how snare and other traps work
  
  If you press 'Yes' you will proceed to do the damage, so make sure you opponent has decided to use their effects or not.
  
  If your opponent is unresponsive, pinging more than 2 times will give you a chance to abort the damage and try to find out what is happening

### 3.1.10.x

* Added comprehensive rules in the documentation menu, [courtesy of netrunnercards.info](http://netrunnercards.info/rules/)
* Made the Runner Trace Card highlight yellow to stick out from the board.
* Deep Thought announces its use to the corp.

### 3.1.9.x

* New board again! Now with Runner red, and text
* False lead now will not lose clicks if the player doesn't have at least 2
* NBN:TWiY won't lose its extra hand size after mulligan
* Can now prioritize Start of Turn abilities. This way you can set your Wyldsize to fire before your Darwin, even if you played Wyldside later in the turn. (Make sure you prioritize your cyberfeeders over your Darwin, so that you always have money to pay for it)
* Hasbro:ST will now put visible +1 markers on your Bioroids
* Moved icons to the right side, to allow the chat box to expand vertically without hiding them.

### 3.1.8.x

* Quick fix to stop accessing snares from R&D crashing the scirpt

### 3.1.7.x

* Added the new sweet sweet tabletop
* Dedicated Response Team won't do damage on non-successful Runs

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