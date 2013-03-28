AutoScripts Legend
==================

This is how the autoscripts in the Netrunner game are formatted and work.  
For future reference and possibly benefit of other developers.


card.AutoScript
---------------

This field retains scripts that activate when a card comes into or leaves play, or something that happens at start/end of the turn sequence

The field before the colon, explains when the effect triggers

* onPlay: Activates when the player plays the card from their hand
* onScore: Activates when the agenda is scored by the corp
* onLiberation: Activates when the agenda is scored by the runner
* onRez: Activates when the card is rezzed 
* onDerez: Activates when the card is derezzed
* atTurnStart: Activates when the turn starts
* atTurnEnd: Activates when the turn ends
* atJackOut: Activates when the runner ends a run with [Esc] or [F3] or when the corp ends the run for them via a Wall

card.AutoAction
---------------

This field contains scripts that activate when the card is "used", most usually by the player double-clicking on it.

The field before the colons explains the cost of the action to the engine

* A[0-9]+ : How many actions does it cost to activate
* B[0-9]+ : How many Bits
* G[0-9]+ : How many Agenda Points
* T[0-9]+ : T is a special field that modifies the status of the card as part of the cost
  * T0: Nothing happens
  * T1: Card needs to be trashed
  * T2: Card can only use this ability once per turn. Card will be turned sideways to signify this.
  
The Core Commands
---------------

The various scripts are written in a way that they are easily readable by a human, but also understood from the engine (via regex) and easily expandable and modular

When a script is separated by two lines "||", this serves as an "or" for the engine (but only for cards that are used. i.e. for card.AutoAction). 
The player will be prompted to select one of the abilities and then the engine will execute it.

When a script is separated by two dollar signs "$$", this serves as an "and" for the engine.
All the effects of that particular script will be used. card.Autoscript uses "||" like this as well for now.
All scripts separated by $$ are exetuted serially, one after the other. If one of them aborts for some reason, the rest won't be done. This is useful for special costs (e.g. "If you inflicted any damage...")

The first words after the card.AutoAction costs, the card.AutoScript trigger, or the || and $$ separators are always what is called the __Core Commands__. 
These core commands are what tell the engine the general idea of what it's going to be doing for this script part.

To put this all together: lets take a script like: `A1B1G0T0:Draw2Cards$$Gain3Bits||A1B2G0T0:Gain1Agenda Points`

It will be parsed as follows:

*Use 1 Action, and pay 1 Bit to: Draw 2 cards and Gain 3 Bits, OR Use 1 Action, and pay 2 Bits to: Gain 1 Agenda point.*

Note that core commands after an "OR" bit, need a cost, while core commands after an "AND" bit, do not.

The core commands are usually written in a form like Gain3Bits, Put1virusPattel, or TrashTarget  
Any number is always attempted to put in the middle of the core command as part of the standard I'm using.

The same core commands can be triggered by different scripts in the card properties.  
So for example Gain2Bits, Lose1Tags, and SetTo1Hand Size will all trigger the same core command (in this case GainX())  
This is because all these three do similar things (modify counters) which allows the same command to handle all of them with slight modifications and flow control

To see a look of what core commands exist, look at the code after the useAbility() starting point.   
Each core command function is marked clearly in the comment next to its definition.   
Look at the regexHooks dictionary at the start of the script and you'll be able to see what kind of keywords will flow to each Core Command

Resident Effects
----------------

There are a few scripts that are in card.AutoScript, which are polled when specific events happen, like paying a cost, or doing damage.  
They are not core commands per se, but are put in the same location as those are. These are worth mention as they are easy to forget.

### Reduce

It reduces the Bit cost of something specific. If a number is next to "Reduce", then it will reduce the costs paid by always this amount  
If a hash "#" is next to "Reduce", the it will reduce the cost based on how many bits markers are on the card at the time the cost is being paid.

After that comes a "Cost" and anything after that is the event that is having its cost reduced

So the command is the end like: `Reduce#CostUse`. These are the triggers used until now.

* Use: Reduces the cost when the card is used (i.e. double clicked on the table)
* Play: Reduces the cost when the card is played from the hand
* Rez: Reduces the cost to rez a card
* Trace: Reduces the cost of paying traces
* Trash: Reduces the cost of trashing cards. The player needs to do the trash action himself though.
* Install: Reduces the cost to install a card that will stay in play
* DelTag: Reduces the cost to remove tags

Usually these require a specific requirement for their reduction. See the -for modulator below.

### Enhance

It increases the damage done by specific damage types. "Enhance" is followed by a number and then the damage type

So `whileScored:Enhance1MeatDamage` will increase all Meat Damage you do by 1 point.

The Modulators
-------------

scripts starting with dashes "-" are treated as modules for the same core command. Some tell it it needs to use a target. Others tell how many times the same effect applies etc  
The modulators are...well, _modular_. Any modulator that is not understood by the core command will be ignored. This allows me to even put modulators on modulators

Usually the same modulator starts in the same way always. So the target requirements always start with "-at", while pointing out the target player is with "-on" or "-of".  
The following are the modulators that I commonly use (for future reference)

Parts in [square brackets] signify variable parts. They are written without the square brackets

So for example writing -at[Requirement] means that I have something like -atIcebreaker in my scripts.


### -Targeted

This modulator tells the engine that this card needs a target. This is checked many times, sometimes before even the script begins.  
For example it is checked when the player is about to play a card from his handm, and if a valid target is not found, the player is given a chance to abort.

A valid target is one that has been targeted by the player who has used shift+click on it and has the proper requirements (see -at below)

### -AutoTargeted

This is very similar to the above, but instead of the player having to target a card first, the game will seek and select all the cards which match the requirements

#### -at[Requirements_and_exclusions_or_moreRequirements]

This modulator basically informs that -Targeted modulator on what is a valid target. the [part in the brackets] is the type of requirements for a valid target

so `-atIce` would look for Targets that are of the card.Type "Ice". 

There can be more of these, split by relevant `_and_` and `_or_`.  
So a target given at -atIcebreaker_and_Killer would look for a card which has both the Icebreaker and Killer keywords, while -atIcebreaker_or_Killer would look for a card which has either of those keywords.  
adding "non" or "not" in front of a requirement makes it an exclusion. So -atIce_and_nonSentry means a valid target is a non-Sentry Ice.  
Requirement and exclusions check the card.name, the card.Type and the card.Keywords at the same time

#### -o[nf]Opponent

the -onOpponent or -ofOpponent modulator is parsed by many different Core Commands and modulators. The -Targeted mod uses it as an exclusion requirement for a card.  
Core commands usually use it to select the target for their effect.

This means that `Lose2Bits-ofOpponent` will reduce the "Bit Pool" counter of your opponent instead of yours. The -o[fn]Opponent modulator is built in such a way to work also in 4-player games.

#### -isRezzed / -isUnrezzed

This is used by both -per and -Targeted as a requirement for valid targets. 

#### -byMe / -byOpponent

Used as a requirement by many functions and modulators

* with "-Targeted". It checks to see who the owner of the targeted card must be.
* with atTurnStart, atJackOut, atRunStart etc, it check to see if the controller of the card on a table has to be the same or opposing as the player who's turn/run is ending. For example, it's used in a PAD campaign, so that the opponent does not gain credits at the start of their own turn. But it's not used with Stimhack, so that the opponent DOES take damage if you end their run for them
* with the hidden triggers (function: autoscriptOtherPlayers()), this checks to see if the card can only be triggered by its controller or the by opposing player. (For example an effect like "Gain 1 credit when you install a card" needs to have the "-byMe modulator, so that the opponent's installations don't trigger the effect.)

#### -AutoTargeted

Instead of the player selecting each target, the game engine will target all cards of the specific type.

### -per

Another very important modulator. It tells the engine what the multiplier for a specific action will be. The items after -per explain how it will be used.  
A multiplier means that when we have a action that adds a something based on a number, the number will be multiplied by the conditions we set on per.

* -perTargetProperty{[Exact Property Name]}: This will multiply the effect by the targeted card's [specified] property value
* -perTargetMarker{[Exact Marker Name]}: This will multiply the effect by the targeted card's specified number of [markers]
* -perTarget[Requirement]: This will multiply the effect by the number of targeted cards of the [specified requirements]. 
* -perTargetAny: This will mutliply the effect by the number of targeted cards. Without any requirements.
* -perEvery[Keyword]: This will multiply the effects by the number of cards with card.name, card.Type, or card.Keywords which match the [Keyword] on the table. 
* -perX: This will multiply the effects by a number provided by another core command, such as the effects of RollX which rolls a 6-sided die.
* -perProperty{[Exact Property Name]}: Will multiply the effects by the activated card's [property] value
* -perMarker{[Exact Marker Name]}: Will multiply the effects by the activated card's specified number of [markers].

So to give an example: `onScore:Gain3Bits-perMarker{Advance}`

The above script would gain the player 3 bits per advance token on the card when it was scored as an agenda.

Another example: `A1B0G0T0:Lose1Bits-ofOpponent-perIce-isRezzed-byOpponent`

This script would make the opponent lose 1 bit for each rezzed ice they have.

-per also parses some specialized modulators

* -isExposeTarget: Will expose the targeted card
* -Reveal&Shuffle: Will Reveal the target card from the hand and shuffle it into the deck afterwards
* -Reveal&Recover: Will Reveal the target card from the hand and return it afterwars
* -SendToTrash: Will send the targets to the trash.
* -fromHand: The targets will be sought in our hand

### -toR&D / -toStack

Used as modulator to the uninstall core command, to select an alternative destination than me.hand.

### -isCost

Used by various core commands to signify if any part of a script is a cost. If the cost cannot be paid (i.e. there's not enough markers on the card to remove), then the whole script will abort.
-isCost usually goes as the first script in a Autoscript serial

example: `A0B0G0T0:Remove2Bits-isCost$$Gain1Actions`

This would remove 2 bits from the card to gain 1 action. If no bits where on the card, the second part would not occur.

### -with

Used with the CreateDummy core command. It adds a number of tokens on the card, much like being a Put core command.

example: `onPlay:RequestInt$$Lose2Bits-perX-isCost$$CreateDummy-with1Actions-perX`

Request a number (X) from the player, the player then need to be able to pay 2 times as many bits. Then we will create a dummy card with as many counters as X.

### -excludeDummy / -onlyforDummy

Another modulator for the CreateDummy core command. Any core command with -excludeDumm will not be an option if the card is a dummy and the opposite if the mod is -onlyforDummy

### -isOptional

Specifies a script as optional. Will prompt the player to proceed, and if the player refuses, the rest of the script will abort as well. (e.g. see card Caryatid)

### -isAlternative

Specifies if a atSuccessfulRun effect is replacing the normal effect that running on that fort would have (accessing R&D cards etc)

### -for

used by the "Reduce" Resident Effect. It signifies what is a valid trigger for the reduction of the cost. Anything after the -for is looked for in the card's type and keywords.

For example: `Reduce#CostUse-forProgram`

Will reduce the cost for using programs by the number of bit tokens on the card itself.

### -div

This Is used in combination with -perX usually and it merely divides the multiplier by the given amount. (E.g. see Food Fight)
When used in the RequestInt core command, it makes sure the player gives a number that can be cleanly divided.

### -ignore

It is used for cards like Project Venice, where we need to start counting a multiplier after a certain level.

### -from / -to 

Used by the DrawX core command to decide on from which pile and to which pile to send the cards it's drawing. 

For example: `Draw2Cards-toTrash` would send 2 cards from the player's R&D or Stack to their trash.

### -onAccess

When used on an AutoAction, then that autoscript can be activated even if the card is unrezzed (normally unrezzed cards try to rez or score on double-click)

The player will be prompted if this is what they want.

### -nonPreventable

Used by the InflictX core command. Any damage modded like this will not trigger damage prevention cards and will always discard cards from the target player's hand.

### -warn

The warn modulator merely provides some information to the player, and occasionally allows them to abort the operation, if they're not ready.

### -chk

Used by the RollX core command to see if the dice results needs to match a specific number

### -isSubroutine

Used only on ice. It tells the game which of their abilities are subroutines, so that we use the appropriate icon on the announcement.

### -ifSuccessfulRun(HQ|R&D|Archives|Generic)

This modulator modifies the script's trigger so that it doesn't go off unless the run has been successfully completed at a specific Server. (e.g. See cards like "Medium")

### -feintTo(HQ|R&D|Archives|Generic)

This modulator makes it so that the trigger thinks the real target of a run was another server (e.g. see Sneakdoor Beta)

### -trashCost

Used during damage reduction to signify a card that needs to be trashed as part of the cost for reducing damage (e.g. Crash Space)

### -isPriority

Used when putting tokens on cards to mark them to use those credits before all others

### -onTriggerCard

used during triggered scripts, to figure out if the target card is the trigger, or the triggered one.

### -afterCardInstall

Just another way of setting the trigger of a script.

### -afterUnavoidedTrace / -afterEludedTrace

Trigger after a trace has ended with the runner being traced or eluding it respectively. Usually this script is run by the runner player, in which case effects which need to target them (such as Spinal Modem's Brain Damage) need the -byMe modulator

### -traceEffects<Success Effect,Failure Effect>

A modulator added after the TraceX core command. It will put into memory what effects as successful or failed trace will have. 
Those effects will be run by the runner once they use their trace card to declare their final base link.
The modulator needs to be followed by the lesser/greater symbols <> wrapping two comma separated scripts. The script follow the usual core command rules and allow all modulators. 
The first script is for a successful Trace and the second script if for a failed trace (e.g. TMI)
If there is no script for either of these conditions, then the entry should say "None" exactly.
