### ANR CARD SCRIPTS ###
# 5 Equal Signs (=) signifiies a break between the description (what you're currently reading) and the code
# 5 Dashes  (-) signifies a break between the card name, the GUID and the card scripts. The card name is ignored by the code, only the GUID and Scripts are used.
# 5 Plus Signs (+) signifies a break between AutoActions and AutoScripts for the same card
# 5 Dots (.) signifies a break between different cards.
# Do not edit below the line
ScriptsLocal = '''
=====
Virus Scan
-----
23473bd3-f7a5-40be-8c66-7d35796b6031
-----

+++++
A3B0G0T0:CustomScript
.....
HQ
-----
81cba950-9703-424f-9a6f-af02e0203762
-----

+++++
A1B0G0T0:RunEnd-isSilent$$RunHQ
.....
R&D
-----
fbb865c9-fccc-4372-9618-ae83a47101a2
-----

+++++
A1B0G0T0:RunEnd-isSilent$$RunR&D
.....
Archives
-----
47597fa5-cc0c-4451-943b-9a14417c2007
-----

+++++
A1B0G0T0:RunEnd-isSilent$$RunArchives
.....
Remote Server
-----
d59fc50c-c727-4b69-83eb-36c475d60dcb
-----

+++++
A1B0G0T0:RunEnd-isSilent$$RunRemote
.....
Divided by Zer0
-----
bc0f047c-01b1-427f-a439-d451eda00000
-----

+++++
A0B0G0T0:ExileTarget-Targeted-atAgenda-targetMine-isCost$$SimplyAnnounce{force the corp to forfeit an agenda}
.....
Accelerated Beta Test
-----
bc0f047c-01b1-427f-a439-d451eda01055
-----
onScore:CustomScript
+++++
	
.....
Access to Globalsec
-----
bc0f047c-01b1-427f-a439-d451eda01052
-----
whileInstalled:Gain1Base Link
+++++
	
.....
Account Siphon
-----
bc0f047c-01b1-427f-a439-d451eda01018
-----
onPlay:RunHQ||atSuccessfulRun:Lose5Credits-ofOpponent-isOptional-isAlternativeRunResult$$Gain2Credits-perX$$Gain2Tags||atJackOut:TrashMyself-isSilent
+++++
	
.....
Adonis Campaign
-----
bc0f047c-01b1-427f-a439-d451eda01056
-----
onRez:Put12Credits||atTurnStart:Transfer3Credits-byMe$$TrashMyself-ifEmpty
+++++
	
.....
Aesop's Pawnshop
-----
bc0f047c-01b1-427f-a439-d451eda01047
-----

+++++
A0B0G0T2:TrashTarget-Targeted-targetMine$$Gain3Credits	
.....
Aggressive Negotiation
-----
bc0f047c-01b1-427f-a439-d451eda01097
-----

+++++
	
.....
Aggressive Secretary
-----
bc0f047c-01b1-427f-a439-d451eda01057
-----
onAccess:UseCustomAbility-ifInstalled-isOptional-pauseRunner
+++++
A0B2G0T0:TrashMulti-Targeted-atProgram-onAccess
.....
Akamatsu Mem Chip
-----
bc0f047c-01b1-427f-a439-d451eda01038
-----
whileInPlay:Provide1MU
+++++

.....
Akitaro Watanabe
-----
bc0f047c-01b1-427f-a439-d451eda01079
-----

+++++
A0B0G0T0:RezTarget-Targeted-isICE-payCost-reduc2
.....
Anonymous Tip
-----
bc0f047c-01b1-427f-a439-d451eda01083
-----
onPlay:Draw3Cards
+++++
	
.....
Archer
-----
bc0f047c-01b1-427f-a439-d451eda01101
-----
onRez:ExileTarget-Targeted-atAgenda
+++++
A0B0G0T0:Gain2Credits-isSubroutine||A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Archived Memories
-----
bc0f047c-01b1-427f-a439-d451eda01058
-----
onPlay:Retrieve1Cards-fromArchives-doNotReveal
+++++
	
.....
Armitage Codebusting
-----
bc0f047c-01b1-427f-a439-d451eda01053
-----
onInstall:Put12Credits
+++++
A1B0G0T0:Transfer2Credits$$TrashMyself-ifEmpty	
.....
AstroScript Pilot Program
-----
bc0f047c-01b1-427f-a439-d451eda01081
-----
onScore:Put1Agenda
+++++
A0B0G0T0:Remove1Agenda-isCost$$Put1Advancement-Targeted	
.....
Aurora
-----
bc0f047c-01b1-427f-a439-d451eda01025
-----

+++++
A0B2G0T0:SimplyAnnounce{break barrier subroutine}||A0B2G0T0:Put3PlusOne	
.....
Bank Job
-----
bc0f047c-01b1-427f-a439-d451eda01029
-----
onInstall:Put8Credits||atSuccessfulRun:RequestInt-isOptional-isAlternativeRunResult$$Transfer1Credits-perX-ifSuccessfulRunRemote$$TrashMyself-ifEmpty
+++++
	
.....
Battering Ram
-----
bc0f047c-01b1-427f-a439-d451eda01042
-----

+++++
A0B2G0T0:SimplyAnnounce{break up to 2 barrier subroutines}||A0B1G0T0:Put1PlusOne
.....
Beanstalk Royalties
-----
bc0f047c-01b1-427f-a439-d451eda01098
-----
onPlay:Gain3Credits
+++++
	
.....
Biotic Labor
-----
bc0f047c-01b1-427f-a439-d451eda01059
-----
onPlay:Gain2Clicks
+++++
	
.....
Breaking News
-----
bc0f047c-01b1-427f-a439-d451eda01082
-----
onScore:Gain2Tags-onOpponent$$Put1BreakingNews||atTurnEnd:Remove1BreakingNews-isCost-byMe$$Lose2Tags-onOpponent
+++++
	
.....
Cell Portal
-----
bc0f047c-01b1-427f-a439-d451eda01074
-----

+++++
A0B0G0T0:SimplyAnnounce{deflects the runner to the outermost piece of ice}-isSubroutine$$DerezMyself	
.....
Chum
-----
bc0f047c-01b1-427f-a439-d451eda01075
-----

+++++
A0B0G0T0:Put2PlusOne-Targeted-atICE-isSubroutine||A0B0G0T0:Inflict3NetDamage-onOpponent-isSubroutine	
.....
Closed Accounts
-----
bc0f047c-01b1-427f-a439-d451eda01084
-----
onPlay:Lose999Credits-onOpponent-ifTagged1
+++++
	
.....
Corporate Troubleshooter
-----
bc0f047c-01b1-427f-a439-d451eda01065
-----

+++++
A0B0G0T1:RequestInt$$Lose1Credits-perX-isCost$$Put1PlusOne-perX-Targeted-atICE-isRezzed
.....
Corroder
-----
bc0f047c-01b1-427f-a439-d451eda01007
-----

+++++
A0B1G0T0:SimplyAnnounce{break barrier subroutine}||A0B1G0T0:Put1PlusOne	
.....
Crash Space
-----
bc0f047c-01b1-427f-a439-d451eda01030
-----
onInstall:Put2Credits||whileInstalled:Reduce#CostDeltag-affectsAll-excludeDummy-forMe||atTurnPreStart:Refill2Credits-excludeDummy-duringMyTurn||onDamage:CreateDummy-with3protectionMeatDMG-trashCost$$TrashMyself-isSilent
+++++
A0B0G0T1:CreateDummy-with3protectionMeatDMG-trashCost
.....
Crypsis
-----
bc0f047c-01b1-427f-a439-d451eda01051
-----

+++++
A0B1G0T0:SimplyAnnounce{break ice subroutine}||A0B1G0T0:Put1PlusOne||A0B0G0T0:Remove1Virus||A1B0G0T0:Put1Virus
.....
Cyberfeeder
-----
bc0f047c-01b1-427f-a439-d451eda01005
-----
onInstall:Put1Credits-isSilent||whileInstalled:Reduce#CostUse-affectsIcebreaker-forMe||whileInstalled:Reduce#CostInstall-affectsVirus-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++
	
.....
Data Dealer
-----
bc0f047c-01b1-427f-a439-d451eda01031
-----

+++++
A1B0G0T0:ExileTarget-Targeted-isScored$$Gain9Credits	
.....
Data Mine
-----
bc0f047c-01b1-427f-a439-d451eda01076
-----

+++++
A0B0G0T1:Inflict1NetDamage-onOpponent-isSubroutine	
.....
Data Raven
-----
bc0f047c-01b1-427f-a439-d451eda01088
-----

+++++
A0B0G0T0:Gain1Tags-onOpponent||A0B0G0T0:Trace3-isSubroutine-traceEffects<Put1Power,None>||A0B0G0T0:Remove1Power-isCost$$Gain1Tags-onOpponent	
.....
Datasucker
-----
bc0f047c-01b1-427f-a439-d451eda01008
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunHQ||atSuccessfulRun:Put1Virus-ifSuccessfulRunR&D||atSuccessfulRun:Put1Virus-ifSuccessfulRunArchives
+++++
A0B0G0T0:Remove1Virus-isCost$$Put1MinusOne-Targeted-atICE	
.....
Decoy
-----
bc0f047c-01b1-427f-a439-d451eda01032
-----

+++++
A0B0G0T1:Lose1Tags-isPenalty
.....
Deja Vu
-----
bc0f047c-01b1-427f-a439-d451eda01002
-----
onPlay:Retrieve1Card-fromHeap||onPlay:Retrieve2Cards-fromHeap-grabVirus
+++++
	
.....
Demolition Run
-----
bc0f047c-01b1-427f-a439-d451eda01003
-----
onPlay:RunGeneric
+++++
	
.....
Desperado
-----
bc0f047c-01b1-427f-a439-d451eda01024
-----
whileInPlay:Provide1MU||atSuccessfulRun:Gain1Credits
+++++
	
.....
Diesel
-----
bc0f047c-01b1-427f-a439-d451eda01034
-----
onPlay:Draw3Cards
+++++
	
.....
Djinn
-----
bc0f047c-01b1-427f-a439-d451eda01009
-----
onInstall:Put3DaemonMU-isSilent
+++++
A0B0G0T0:PossessTarget-Targeted-atProgram_and_nonIcebreaker-targetMine||A1B1G0T0:Retrieve1Card-grabVirus$$ShuffleStack
.....
Easy Mark
-----
bc0f047c-01b1-427f-a439-d451eda01019
-----
onPlay:Gain3Credits
+++++
	
.....
Enigma
-----
bc0f047c-01b1-427f-a439-d451eda01111
-----

+++++
A0B0G0T0:Lose1Clicks-onOpponent-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Experiential Data
-----
bc0f047c-01b1-427f-a439-d451eda01066
-----

+++++
	
.....
Femme Fatale
-----
bc0f047c-01b1-427f-a439-d451eda01026
-----
onInstall:Put1Femme Fatale-Targeted-isICE-isOptional
+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B2G0T0:Put1PlusOne||A0B0G0T0:RequestInt-Msg{How many subroutines does the target ice have?}$$Lose1Credits-perX-isCost$$SimplyAnnounce{bypass target ice}	
.....
Forged Activation Orders
-----
bc0f047c-01b1-427f-a439-d451eda01020
-----

+++++
	
.....
Gabriel Santiago
-----
bc0f047c-01b1-427f-a439-d451eda01017
-----
atSuccessfulRun:Gain2Credits-ifSuccessfulRunHQ-onlyOnce
+++++
	
.....
Ghost Branch
-----
bc0f047c-01b1-427f-a439-d451eda01087
-----
onAccess:Gain1Tags-onOpponent-perMarker{Advancement}-isOptional-ifInstalled-pauseRunner
+++++
A0B0G0T0:Gain1Tags-onOpponent-perMarker{Advancement}-onAccess	
.....
Gordian Blade
-----
bc0f047c-01b1-427f-a439-d451eda01043
-----

+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B1G0T0:Put1PlusOne	
.....
Grimoire
-----
bc0f047c-01b1-427f-a439-d451eda01006
-----
whileInPlay:Provide2MU||whileInPlay:Put1Virus-foreachCardInstall-onTriggerCard-typeVirus
+++++
A0B0G0T0:Put1Virus-Targeted-atProgram_and_Virus
.....
Haas-Bioroid
-----
bc0f047c-01b1-427f-a439-d451eda01054
-----
whileInPlay:Gain1Credits-foreachCardInstall-byMe-onlyOnce
+++++
	
.....
Hadrian's Wall
-----
bc0f047c-01b1-427f-a439-d451eda01102
-----

+++++
A0B0G0T0:RunEnd-isSubroutine	
.....
Hedge Fund
-----
bc0f047c-01b1-427f-a439-d451eda01110
-----
onPlay:Gain9Credits
+++++
	
.....
Heimdall 1.0
-----
bc0f047c-01b1-427f-a439-d451eda01061
-----

+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Hostile Takeover
-----
bc0f047c-01b1-427f-a439-d451eda01094
-----
onScore:Gain7Credits$$Gain1Bad Publicity
+++++
	
.....
Hunter
-----
bc0f047c-01b1-427f-a439-d451eda01112
-----

+++++
A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
Ice Carver
-----
bc0f047c-01b1-427f-a439-d451eda01015
-----

+++++
	
.....
Ice Wall
-----
bc0f047c-01b1-427f-a439-d451eda01103
-----

+++++
A0B0G0T0:RunEnd-isSubroutine	
.....
Ichi 1.0
-----
bc0f047c-01b1-427f-a439-d451eda01062
-----

+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:Trace1-isSubroutine-traceEffects<Gain1Tags-onOpponent++Inflict1BrainDamage-onOpponent,None>	
.....
Infiltration
-----
bc0f047c-01b1-427f-a439-d451eda01049
-----
onPlay:CustomScript
+++++
	
.....
Inside Job
-----
bc0f047c-01b1-427f-a439-d451eda01021
-----
onPlay:RunGeneric
+++++
	
.....
Jinteki
-----
bc0f047c-01b1-427f-a439-d451eda01067
-----
whileInPlay:Inflict1NetDamage-onOpponent-foreachAgendaScored||whileInPlay:Inflict1NetDamage-onOpponent-foreachAgendaLiberated
+++++
	
.....
Kate "Mac" McCaffrey
-----
bc0f047c-01b1-427f-a439-d451eda01033
-----
whileInstalled:Reduce1CostInstall-affectsHardware-onlyOnce-forMe||whileInstalled:Reduce1CostInstall-affectsProgram-onlyOnce-forMe||whileInPlay:Pass-foreachCardInstall-typeProgram_or_Hardware-byMe-onlyOnce
+++++
	
.....
Lemuria Codecracker
-----
bc0f047c-01b1-427f-a439-d451eda01023
-----

+++++
A1B1G0T0:ExposeTarget-Targeted-isUnrezzed	
.....
Magnum Opus
-----
bc0f047c-01b1-427f-a439-d451eda01044
-----

+++++
A1B0G0T0:Gain2Credits	
.....
Matrix Analyzer
-----
bc0f047c-01b1-427f-a439-d451eda01089
-----

+++++
A0B1G0T0:Put1Advancement-Targeted||A0B0G0T0:Trace2-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
Medium
-----
bc0f047c-01b1-427f-a439-d451eda01010
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunR&D
+++++
	
.....
Melange Mining Corp
-----
bc0f047c-01b1-427f-a439-d451eda01108
-----

+++++
A3B0G0T0:Gain7Credits	
.....
Mimic
-----
bc0f047c-01b1-427f-a439-d451eda01011
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}	
.....
Modded
-----
bc0f047c-01b1-427f-a439-d451eda01035
-----
onPlay:InstallTarget-DemiAutoTargeted-atProgram_or_Hardware-fromHand-choose1-payCost-reduc3
+++++
	
.....
NBN
-----
bc0f047c-01b1-427f-a439-d451eda01080
-----
atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostTrace-affectsAll-forMe
+++++
	
.....
Net Shield
-----
bc0f047c-01b1-427f-a439-d451eda01045
-----
onDamage:Lose1Credits-isCost$$Put1protectionNetDMG-onlyOnce-isPriority
+++++
A0B1G0T2:Put1protectionNetDMG
.....
Neural EMP
-----
bc0f047c-01b1-427f-a439-d451eda01072
-----
onPlay:Inflict1NetDamage-onOpponent
+++++
	
.....
Neural Katana
-----
bc0f047c-01b1-427f-a439-d451eda01077
-----

+++++
A0B0G0T0:Inflict3NetDamage-onOpponent-isSubroutine	
.....
Ninja
-----
bc0f047c-01b1-427f-a439-d451eda01027
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B3G0T0:Put5PlusOne	
.....
Nisei MK II
-----
bc0f047c-01b1-427f-a439-d451eda01068
-----
onScore:Put1Agenda
+++++
A0B0G0T0:Remove1Agenda-isCost$$RunEnd	
.....
Noise
-----
bc0f047c-01b1-427f-a439-d451eda01001
-----
whileInPlay:Draw1Card-toTrash-ofOpponent-foreachCardInstall-typeVirus-byMe
+++++
	
.....
PAD Campaign
-----
bc0f047c-01b1-427f-a439-d451eda01109
-----
atTurnStart:Gain1Credits-duringMyTurn
+++++
	
.....
Parasite
-----
bc0f047c-01b1-427f-a439-d451eda01012
-----
atTurnStart:Put1Virus-duringMyTurn||Placement:ICE-isRezzed
+++++
	
.....
Pipeline
-----
bc0f047c-01b1-427f-a439-d451eda01046
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B2G0T0:Put1PlusOne	
.....
Posted Bounty
-----
bc0f047c-01b1-427f-a439-d451eda01095
-----
onScore:Gain1Bad Publicity-isOptional$$Gain1Tags-onOpponent$$ExileMyself
+++++
	
.....
Precognition
-----
bc0f047c-01b1-427f-a439-d451eda01073
-----
onPlay:CustomScript
+++++
	
.....
Priority Requisition
-----
bc0f047c-01b1-427f-a439-d451eda01106
-----
onScore:RezTarget-Targeted-atICE
+++++
	
.....
Private Security Force
-----
bc0f047c-01b1-427f-a439-d451eda01107
-----

+++++
A1B0G0T0:Inflict1MeatDamage-onOpponent-ifTagged1	
.....
Project Junebug
-----
bc0f047c-01b1-427f-a439-d451eda01069
-----
onAccess:Lose1Credits-isCost-isOptional-ifInstalled-pauseRunner$$Inflict2NetDamage-onOpponent-perMarker{Advancement}
+++++
A0B1G0T0:Inflict2NetDamage-onOpponent-perMarker{Advancement}-onAccess
.....
Psychographics
-----
bc0f047c-01b1-427f-a439-d451eda01085
-----
onPlay:RequestInt$$Lose1Credits-perX-isCost$$Put1Advancement-perX-Targeted
+++++
	
.....
Rabbit Hole
-----
bc0f047c-01b1-427f-a439-d451eda01039
-----
whileInstalled:Gain1Base Link||onInstall:CustomScript
+++++
	
.....
Red Herrings
-----
bc0f047c-01b1-427f-a439-d451eda01091
-----

+++++
	
.....
Research Station
-----
bc0f047c-01b1-427f-a439-d451eda01105
-----
whileInPlay:Provide2HandSize-forCorp
+++++
	
.....
Rototurret
-----
bc0f047c-01b1-427f-a439-d451eda01064
-----

+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Sacrificial Construct
-----
bc0f047c-01b1-427f-a439-d451eda01048
-----

+++++
A0B0G0T1:SimplyAnnounce{prevent an installed program or hardware from being trashed}	
.....
SanSan City Grid
-----
bc0f047c-01b1-427f-a439-d451eda01092
-----

+++++
	
.....
Scorched Earth
-----
bc0f047c-01b1-427f-a439-d451eda01099
-----
onPlay:Inflict4MeatDamage-onOpponent-ifTagged1
+++++
	
.....
SEA Source
-----
bc0f047c-01b1-427f-a439-d451eda01086
-----
onPlay:Trace3-traceEffects<Gain1Tags-onOpponent,None>
+++++

.....
Security Subcontract
-----
bc0f047c-01b1-427f-a439-d451eda01096
-----

+++++
A1B0G0T0:TrashTarget-Targeted-atICE-targetMine-isRezzed$$Gain4Credits	
.....
Shadow
-----
bc0f047c-01b1-427f-a439-d451eda01104
-----

+++++
A0B0G0T0:Gain2Credits-isSubroutine||A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
Shipment from Kaguya
-----
bc0f047c-01b1-427f-a439-d451eda01100
-----
onPlay:Put1Advancement-Targeted
+++++
	
.....
Shipment from Mirrormorph
-----
bc0f047c-01b1-427f-a439-d451eda01060
-----
onPlay:InstallMulti-Targeted-atnonOperation-fromHand
+++++
	
.....
Snare!
-----
bc0f047c-01b1-427f-a439-d451eda01070
-----
onAccess:Lose4Credits-isCost-isOptional$$Inflict3NetDamage-onOpponent$$Gain1Tags-onOpponent
+++++
A0B4G0T0:Inflict3NetDamage-onOpponent-onAccess$$Gain1Tags-onOpponent
.....
Sneakdoor Beta
-----
bc0f047c-01b1-427f-a439-d451eda01028
-----

+++++
A1B0G0T0:RunArchives-feintToHQ	
.....
Special Order
-----
bc0f047c-01b1-427f-a439-d451eda01022
-----
onPlay:Retrieve1Card-grabIcebreaker$$ShuffleStack
+++++
	
.....
Stimhack
-----
bc0f047c-01b1-427f-a439-d451eda01004
-----
onPlay:RunGeneric$$Put9Credits||whileRunning:Reduce#CostAll-affectsAll-forMe||atJackOut:Inflict1BrainDamage-nonPreventable$$TrashMyself
+++++
	
.....
Sure Gamble
-----
bc0f047c-01b1-427f-a439-d451eda01050
-----
onPlay:Gain9Credits
+++++
	
.....
The Maker's Eye
-----
bc0f047c-01b1-427f-a439-d451eda01036
-----
onPlay:RunR&D
+++++
	
.....
The Personal Touch
-----
bc0f047c-01b1-427f-a439-d451eda01040
-----
onInstall:Put1PlusOnePerm-Targeted-atIcebreaker||Placement:Icebreaker-targetMine
+++++
	
.....
The Toolbox
-----
bc0f047c-01b1-427f-a439-d451eda01041
-----
whileInPlay:Provide2MU||whileInstalled:Gain2Base Link||onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostUse-affectsIcebreaker-forMe
+++++
	
.....
Tinkering
-----
bc0f047c-01b1-427f-a439-d451eda01037
-----
onPlay:Put1Keyword:Sentry-Targeted-isICE-isSilent$$Put1Keyword:Code Gate-Targeted-isICE-isSilent$$Put1Keyword:Barrier-Targeted-isICE-isSilent$$Put1Tinkering-Targeted-isICE
+++++
	
.....
Tollbooth
-----
bc0f047c-01b1-427f-a439-d451eda01090
-----

+++++
A0B0G0T0:UseCustomAbility||A0B0G0T0:RunEnd-isSubroutine	
.....
Viktor 1.0
-----
bc0f047c-01b1-427f-a439-d451eda01063
-----

+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Wall of Static
-----
bc0f047c-01b1-427f-a439-d451eda01113
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Wall of Thorns
-----
bc0f047c-01b1-427f-a439-d451eda01078
-----

+++++
A0B0G0T0:Inflict2NetDamage-onOpponent-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Weyland Consortium
-----
bc0f047c-01b1-427f-a439-d451eda01093
-----
whileInPlay:Gain1Credits-foreachCardPlay-typeTransaction-byMe
+++++
	
.....
Wyldside
-----
bc0f047c-01b1-427f-a439-d451eda01016
-----
atTurnStart:Draw2Cards-duringMyTurn$$Lose1Clicks
+++++
	
.....
Wyrm
-----
bc0f047c-01b1-427f-a439-d451eda01013
-----

+++++
A0B3G0T0:SimplyAnnounce{break ice subroutine}||A0B1G0T0:Put1MinusOne-Targeted-atICE||A0B1G0T0:Put1PlusOne	
.....
Yog.0
-----
bc0f047c-01b1-427f-a439-d451eda01014
-----

+++++
A0B0G0T0:SimplyAnnounce{break code gate subroutine}	
.....
Zaibatsu Loyalty
-----
bc0f047c-01b1-427f-a439-d451eda01071
-----

+++++
A0B1G0T0:SimplyAnnounce{prevent card from being exposed}||A0B0G0T1:SimplyAnnounce{prevent card from being exposed}
......
Ash 2X3ZB9CY
-----
bc0f047c-01b1-427f-a439-d451eda02013
-----

+++++
A0B0G0T0:Trace4-traceEffects<SimplyAnnounce{stop the runner from accessing anymore cards},None>
.....
Braintrust
-----
bc0f047c-01b1-427f-a439-d451eda02014
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore3-div2||whileScored:ReduceXCostRez-affectsICE-perMarker{Agenda}-forMe
+++++

.....
Caduceus
-----
bc0f047c-01b1-427f-a439-d451eda02019
-----

+++++
A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain3Credits,None>||A0B0G0T0:Trace2-isSubroutine-traceEffects<RunEnd,None>
.....
Cortez Chip
-----
bc0f047c-01b1-427f-a439-d451eda02005
-----

+++++
A0B0G0T1:Put1Cortez Chip-Targeted-isICE
.....
Draco
-----
bc0f047c-01b1-427f-a439-d451eda02020
-----
onRez:RequestInt-Msg{How many Power counters do you want to add on Draco?}$$Lose1Credits-perX-isCost-actiontypeUSE$$Put1PlusOnePerm-perX
+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<Gain1Tags-onOpponent++RunEnd,None>
.....
Imp
-----
bc0f047c-01b1-427f-a439-d451eda02003
-----
onInstall:Put2Virus
+++++
A0B0G0T2:Remove1Virus-isCost$$SimplyAnnounce{trash an accessed card}
.....
Janus 1.0
-----
bc0f047c-01b1-427f-a439-d451eda02012
-----

+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine
.....
Mandatory Upgrades
-----
bc0f047c-01b1-427f-a439-d451eda02011
-----
whileScored:Gain1Max Click||onScore:Gain1Clicks
+++++

.....
Morning Star
-----
bc0f047c-01b1-427f-a439-d451eda02004
-----

+++++
A0B1G0T0:SimplyAnnounce{break any number of barrier subroutines}
.....
Peacock
-----
bc0f047c-01b1-427f-a439-d451eda02006
-----

+++++
A0B2G0T0:SimplyAnnounce{break code gate subroutine}||A0B2G0T0:Put3PlusOne
.....
Plascrete Carapace
-----
bc0f047c-01b1-427f-a439-d451eda02009
-----
onInstall:Put4Power||onDamage:Remove1Power-isCost$$TrashMyself-ifEmpty$$CreateDummy-with1protectionMeatDMG-doNotTrash-trashCost
+++++
A0B0G0T0:Remove1Power-isCost$$TrashMyself-ifEmpty$$CreateDummy-with1protectionMeatDMG-doNotTrash-trashCost
.....
Project Atlas
-----
bc0f047c-01b1-427f-a439-d451eda02018
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore3
+++++
A0B0G0T0:Remove1Agenda-isCost$$Retrieve1Card$$ShuffleStack
.....
Restructured Datapool
-----
bc0f047c-01b1-427f-a439-d451eda02016
-----

+++++
A1B0G0T0:Trace2-traceEffects<Gain1Tags-onOpponent,None>
.....
Snowflake
-----
bc0f047c-01b1-427f-a439-d451eda02015
-----

+++++
A0B0G0T0:Psi-psiEffects<RunEnd,None>-isSubroutine
.....
Spinal Modem
-----
bc0f047c-01b1-427f-a439-d451eda02002
-----
onInstall:Put2Credits-isSilent||whileInPlay:Provide1MU||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostUse-affectsIcebreaker-forMe||whileRunning:Inflict1BrainDamage-foreachUnavoidedTrace-byMe
+++++

.....
The Helpful AI
-----
bc0f047c-01b1-427f-a439-d451eda02008
-----
whileInstalled:Gain1Base Link
+++++
A0B0G0T1:Put2PlusOne-Targeted-atIcebreaker
.....
TMI
-----
bc0f047c-01b1-427f-a439-d451eda02017
-----
onRez:Trace2-traceEffects<None,DerezMyself>
+++++
A0B0G0T0:RunEnd
.....
Whizzard
-----
bc0f047c-01b1-427f-a439-d451eda02001
-----
atTurnPreStart:Refill3Credits-duringMyTurn||Reduce#CostTrash-affectsAll-forMe
+++++

.....
Haas-Bioroid
-----
bc0f047c-01b1-427f-a439-d451eda02010
-----
whileInPlay:Put1PlusOnePerm-foreachCardRezzed-onTriggerCard-typeBioroid_and_ICE||whileInPlay:Remove1PlusOnePerm-foreachCardDerezzed-onTriggerCard-typeBioroid_and_ICE
+++++

.....
ZU.13 Key Master
-----
bc0f047c-01b1-427f-a439-d451eda02007
-----
ConstantAbility:Cloud2Link
+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B1G0T0:Put1PlusOne
.....
Amazon Industrial Zone
-----
bc0f047c-01b1-427f-a439-d451eda02038
-----

+++++
A0B0G0T0:RezTarget-Targeted-isICE-payCost-reduc3
.....
Big Brother
-----
bc0f047c-01b1-427f-a439-d451eda02035
-----
onPlay:Gain2Tags-onOpponent-ifTagged1
+++++

.....
ChiLo City Grid
-----
bc0f047c-01b1-427f-a439-d451eda02036
-----

+++++
A0B0G0T0:Gain1Tags-onOpponent
.....
Compromised Employee
-----
bc0f047c-01b1-427f-a439-d451eda02025
-----
onInstall:Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileInstalled:Reduce#CostTrace-affectsAll-forMe||whileInPlay:Gain1Credits-foreachCardRezzed-typeICE
+++++

.....
Dyson Mem Chip
-----
bc0f047c-01b1-427f-a439-d451eda02028
-----
whileInstalled:Gain1Base Link$||whileInPlay:Provide1MU
+++++

.....
E3 Feedback Implants
-----
bc0f047c-01b1-427f-a439-d451eda02024
-----

+++++
A0B1G0T0:SimplyAnnounce{break 1 additional subroutine on the current ICE}
.....
Encryption Protocol
-----
bc0f047c-01b1-427f-a439-d451eda02029
-----
whileRezzed:Increase1CostTrash-affectsAll-forOpponent-ifInstalled
+++++

.....
Executive Retreat
-----
bc0f047c-01b1-427f-a439-d451eda02039
-----
onScore:Put1Agenda-isSilent$$ReshuffleHQ
+++++
A1B0G0T0:Remove1Agenda-isCost$$Draw5Cards
.....
Fetal AI
-----
bc0f047c-01b1-427f-a439-d451eda02032
-----
onAccess:Inflict2NetDamage-onOpponent
+++++

.....
Freelancer
-----
bc0f047c-01b1-427f-a439-d451eda02040
-----
onPlay:TrashMulti-Targeted-atResource
+++++

.....
Jinteki
-----
bc0f047c-01b1-427f-a439-d451eda02031
-----

+++++

.....
Liberated Account
-----
bc0f047c-01b1-427f-a439-d451eda02022
-----
onInstall:Put16Credits
+++++
A1B0G0T0:Transfer4Credits$$TrashMyself-ifEmpty	
.....
Notoriety
-----
bc0f047c-01b1-427f-a439-d451eda02026
-----
onPlay:Gain1Agenda Points$$ScoreMyself$$Put1Scored-isSilent
+++++

.....
Power Grid Overload
-----
bc0f047c-01b1-427f-a439-d451eda02037
-----
onPlay:Trace2
+++++
A0B0G0T0:TrashTarget-Targeted-atHardware
.....
Satellite Uplink
-----
bc0f047c-01b1-427f-a439-d451eda02023
-----
onPlay:ExposeMulti-Targeted-isUnrezzed
+++++

.....
Sensei
-----
bc0f047c-01b1-427f-a439-d451eda02034
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Sherlock 1.0
-----
bc0f047c-01b1-427f-a439-d451eda02030
-----

+++++
A0B0G0T0:Trace4||A0B0G0T0:UninstallTarget-toStack-Targeted-atProgram
.....
Snowball
-----
bc0f047c-01b1-427f-a439-d451eda02027
-----
atJackOut:Remove999Snowball
+++++
A0B1G0T0:SimplyAnnounce{break barrier subroutine}$$Put1Snowball||A0B1G0T0:Put1PlusOne	
.....
Trick of Light
-----
bc0f047c-01b1-427f-a439-d451eda02033
-----

+++++

.....
Vamp
-----
bc0f047c-01b1-427f-a439-d451eda02021
-----
onPlay:RunHQ||atSuccessfulRun:RequestInt-Msg{How many credits do you want to burn?}$$Lose1Credits-perX-isCost-isOptional-isAlternativeRunResult$$Lose1Credits-perX-ofOpponent$$Gain1Tags$$TrashMyself-ifSuccessfulRunHQ
+++++

.....
Nerve Agent
-----
bc0f047c-01b1-427f-a439-d451eda02041
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunHQ
+++++
	
.....
Joshua B.
-----
bc0f047c-01b1-427f-a439-d451eda02042
-----

+++++
A0B0G0T2:Gain1Clicks$$Infect1Joshua Enhancement-isSilent
.....
Dinosaurus
-----
bc0f047c-01b1-427f-a439-d451eda02048
-----
onInstall:Put1Dinosaurus Hosted-isSilent||ConstantAbility:CountsAsDaemon||onHost:Put2PlusOnePerm-isSilent
+++++
A0B0G0T0:PossessTarget-Targeted-atIcebreaker_and_nonAI-targetMine
.....
Emergency Shutdown
-----
bc0f047c-01b1-427f-a439-d451eda02043
-----
onPlay:DerezTarget-Targeted-atICE
+++++

.....
Muresh Bodysuit
-----
bc0f047c-01b1-427f-a439-d451eda02044
-----
onDamage:Put1protectionMeatDMG-onlyOnce-isPriority
+++++
A0B0G0T2:Put1protectionMeatDMG
.....
Snitch
-----
bc0f047c-01b1-427f-a439-d451eda02045
-----
atJackOut:Remove999Snitched-isSilent
+++++
A0B0G0T0:ExposeTarget-Targeted-isICE-restrictionMarkerSnitched
.....
Public Sympathy
-----
bc0f047c-01b1-427f-a439-d451eda02050
-----
whileInPlay:Provide2HandSize-forRunner
+++++

.....
Chimera
-----
bc0f047c-01b1-427f-a439-d451eda02060
-----
onRez:ChooseKeyword{Code Gate|Barrier|Sentry}||atTurnEnd:DerezMyself$$Remove1Keyword:Sentry-isSilent$$Remove1Keyword:Barrier-isSilent$$Remove1Keyword:Code Gate-isSilent
+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Commercialization
-----
bc0f047c-01b1-427f-a439-d451eda02058
-----
onPlay:Gain1Credits-perTargetMarker{Advancement}-Targeted-atICE-isICE
+++++

.....
Edge of World
-----
bc0f047c-01b1-427f-a439-d451eda02053
-----
onAccess:Lose3Credits-isCost-isOptional-ifInstalled$$RequestInt-Msg{How many ICE are installed on this server?}$$Inflict1BrainDamage-onOpponent-perX
+++++
A0B3G0T0:RequestInt-Msg{How many ICE are installed on this server?}-onAccess-ifInstalled$$Inflict1BrainDamage-onOpponent-perX
.....
Marked Accounts
-----
bc0f047c-01b1-427f-a439-d451eda02055
-----
atTurnStart:Transfer1Credits-duringMyTurn
+++++
A1B0G0T0:Put3Credits
.....
Personal Workshop
-----
bc0f047c-01b1-427f-a439-d451eda02049
-----
atTurnStart:CustomScript
+++++
A1B0G0T0:CustomScript
.....
Pop-up Window
-----
bc0f047c-01b1-427f-a439-d451eda02056
-----

+++++
A0B0G0T0:Gain1Credits||A0B0G0T0:Lose1Credits-ofOpponent-isCost-isSubroutine||A0B0G0T0:RunEnd-isSubroutine
.....
Private Contracts
-----
bc0f047c-01b1-427f-a439-d451eda02059
-----
onRez:Put14Credits
+++++
A1B0G0T0:Transfer2Credits$$TrashMyself-ifEmpty	
.....
Project Vitruvius
-----
bc0f047c-01b1-427f-a439-d451eda02051
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore3
+++++
A0B0G0T0:Remove1Agenda-isCost$$Retrieve1Cards-fromArchives-doNotReveal
.....
Test Run
-----
bc0f047c-01b1-427f-a439-d451eda02047
-----
onPlay:Retrieve1Card-grabProgram-toTable-with1Test Run$$ShuffleStack||onPlay:Retrieve1Card-fromHeap-grabProgram-toTable-with1Test Run
+++++
A0B0G0T0:UninstallTarget-toStack-AutoTargeted-atProgram-hasMarker{Test Run}$$TrashMyself
.....
Viper
-----
bc0f047c-01b1-427f-a439-d451eda02052
-----

+++++
A0B0G0T0:Trace3-isSubroutine-traceEffects<Lose1Clicks-ofOpponent,None>||A0B0G0T0:Trace3-isSubroutine-traceEffects<RunEnd,None>
.....
Woodcutter
-----
bc0f047c-01b1-427f-a439-d451eda02057
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine	
.....
Chaos Theory
-----
bc0f047c-01b1-427f-a439-d451eda02046
-----
whileInPlay:Provide1MU
+++++

.....
Disrupter
-----
bc0f047c-01b1-427f-a439-d451eda02061
-----

+++++
A0B0G0T1:SimplyAnnounce{Prevent the Trace and initiate it again with a base strength of 0}
.....
Force of Nature
-----
bc0f047c-01b1-427f-a439-d451eda02062
-----

+++++
A0B2G0T0:SimplyAnnounce{break up to 2 code gate subroutines}||A0B1G0T0:Put1PlusOne	
.....
Scrubber
-----
bc0f047c-01b1-427f-a439-d451eda02063
-----
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileInstalled:Reduce#CostTrash-affectsAll-forMe
+++++

.....
Doppelganger
-----
bc0f047c-01b1-427f-a439-d451eda02064
-----
whileInPlay:Provide1MU
+++++
A0B0G0T2:RunEnd-isSilent$$RunGeneric
.....
Crescentus
-----
bc0f047c-01b1-427f-a439-d451eda02065
-----

+++++
A0B0G0T1:DerezTarget-Targeted-atICE-isRezzed
.....
Deus X
-----
bc0f047c-01b1-427f-a439-d451eda02066
-----
onDamage:Put100protectionNetDMG-trashCost-excludeDummy
+++++
A0B0G0T1:SimplyAnnounce{break any number of AP subroutines}-excludeDummy||A0B0G0T1:CreateDummy-with100protectionNetDMG-trashCost
.....
All Nighter
-----
bc0f047c-01b1-427f-a439-d451eda02067
-----

+++++
A1B0G0T1:Gain2Clicks
.....
Inside Man
-----
bc0f047c-01b1-427f-a439-d451eda02068
-----
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileInstalled:Reduce#CostInstall-affectsHardware-forMe
+++++

.....
Underworld Contact
-----
bc0f047c-01b1-427f-a439-d451eda02069
-----
atTurnStart:Gain1Credits-ifIHave2Base Link-duringMyTurn
+++++

.....
Green Level Clearance
-----
bc0f047c-01b1-427f-a439-d451eda02070
-----
onPlay:Gain3Credits$$Draw1Card
+++++

.....
Hourglass
-----
bc0f047c-01b1-427f-a439-d451eda02071
-----

+++++
A0B0G0T0:Lose1Clicks-onOpponent-isSubroutine
.....
Dedicated Server
-----
bc0f047c-01b1-427f-a439-d451eda02072
-----
onRez:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostRez-affectsICE-forMe
+++++

.....
Bullfrog
-----
bc0f047c-01b1-427f-a439-d451eda02073
-----

+++++
A0B0G0T0:Psi-psiEffects<UseCustomAbility,None>-isSubroutine
.....
Uroboros
-----
bc0f047c-01b1-427f-a439-d451eda02074
-----

+++++
A0B0G0T0:Trace4-isSubroutine-traceEffects<SimplyAnnounce{stop the runner from making any more runs this turn},None>||A0B0G0T0:Trace4-isSubroutine-traceEffects<RunEnd,None>
.....
Net Police
-----
bc0f047c-01b1-427f-a439-d451eda02075
-----
onRez:Put1Credits-perOpponentCounter{Base Link}||atTurnPreStart:Refill1Credits-perOpponentCounter{Base Link}-duringMyTurn||whileRezzed:Reduce#CostTrace-affectsAll-forMe
+++++

.....
Weyland Consortium: Because we Build it
-----
bc0f047c-01b1-427f-a439-d451eda02076
-----
atTurnPreStart:Refill1Credits-duringMyTurn||whileRezzed:Reduce#CostAdvancement-affectsICE-forMe
+++++

.....
Government Contracts
-----
bc0f047c-01b1-427f-a439-d451eda02077
-----

+++++
A2B0G0T0:Gain4Credits
.....
Tyrant
-----
bc0f047c-01b1-427f-a439-d451eda02078
-----

+++++
A0B0G0T0:RunEnd-isSubroutine	
.....
Oversight AI
-----
bc0f047c-01b1-427f-a439-d451eda02079
-----
Placement:ICE-isUnrezzed||onPlay:RezTarget-Targeted-atICE-isUnrezzed
+++++

.....
False Lead
-----
bc0f047c-01b1-427f-a439-d451eda02080
-----

+++++
A0B0G0T0:Lose2Clicks-ofOpponent-isExact$$ExileMyself
.....
Surge
-----
bc0f047c-01b1-427f-a439-d451eda02081
-----
onPlay:Put2Virus-Targeted-atProgram
+++++

.....
Xanadu
-----
bc0f047c-01b1-427f-a439-d451eda02082
-----
whileInstalled:Increase1CostRez-affectsAll-isICE-forOpponent
+++++

.....
Andromeda
-----
bc0f047c-01b1-427f-a439-d451eda02083
-----
onStartup:Draw4Cards-isSilent||onMulligan:Draw4Cards-isSilent
+++++

.....
Networking
-----
bc0f047c-01b1-427f-a439-d451eda02084
-----
onPlay:Lose1Tags
+++++
A0B1G0T0:UninstallMyself-isSilent$$SimplyAnnounce{take networking back into their grip}
.....
HQ Interface
-----
bc0f047c-01b1-427f-a439-d451eda02085
-----

+++++

.....
Pheromones
-----
bc0f047c-01b1-427f-a439-d451eda02086
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunHQ||onRez:Put1Credits-perMarker{Virus}||atTurnPreStart:Refill1Credits-perMarker{Virus}-duringMyTurn||whileRunningHQ:Reduce#CostAll-affectsAll-forMe
+++++

.....
Quality Time
-----
bc0f047c-01b1-427f-a439-d451eda02087
-----
onPlay:Draw5Cards
+++++

.....
Replicator
-----
bc0f047c-01b1-427f-a439-d451eda02088
-----
whileInPlay:UseCustomAbility-foreachCardInstall-onTriggerCard-typeHardware-byMe
+++++

.....
Creeper
-----
bc0f047c-01b1-427f-a439-d451eda02089
-----
ConstantAbility:Cloud2Link
+++++
A0B2G0T0:SimplyAnnounce{break sentry subroutine}||A0B1G0T0:Put1PlusOne
.....
Kraken
-----
bc0f047c-01b1-427f-a439-d451eda02090
-----
onPlay:SimplyAnnounce{force the corp to trash a piece of ice on target server}
+++++

.....
Kati Jones
-----
bc0f047c-01b1-427f-a439-d451eda02091
-----

+++++
A1B0G0T0:Put3Credits-onlyOnce||A1B0G0T0:Transfer999Credits-onlyOnce
.....
Eve Campaign
-----
bc0f047c-01b1-427f-a439-d451eda02092
-----
onRez:Put16Credits||atTurnStart:Transfer2Credits-byMe$$TrashMyself-ifEmpty
+++++

.....
Rework
-----
bc0f047c-01b1-427f-a439-d451eda02093
-----
onPlay:ReworkTarget-Targeted-fromHand$$ShuffleR&D-isSilent
+++++

.....
Whirlpool
-----
bc0f047c-01b1-427f-a439-d451eda02094
-----

+++++
A0B0G0T1:SimplyAnnounce{prevent the runner from jacking out for the remainder of this run}
.....
Hosukai Grid
-----
bc0f047c-01b1-427f-a439-d451eda02095
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent
.....
Data Hound
-----
bc0f047c-01b1-427f-a439-d451eda02096
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<SimplyAnnounce{sniff the runner stack},None>||A0B0G0T0:UseCustomAbility

.....
Bernice Mai
-----
bc0f047c-01b1-427f-a439-d451eda02097
-----

+++++
A0B0G0T0:Trace5-traceEffects<Gain1Tags-onOpponent,TrashMyself>
.....
Salvage
-----
bc0f047c-01b1-427f-a439-d451eda02098
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
Simone Diego
-----
bc0f047c-01b1-427f-a439-d451eda02099
-----
onRez:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn
+++++
A1B0G0T0:Remove1Credits-isCost$$Put1Advancement-Targeted
.....
Foxfire
-----
bc0f047c-01b1-427f-a439-d451eda02100
-----
onPlay:Trace7-traceEffects<SimplyAnnounce{trash 1 virtual resource, or 1 link},None>
+++++
A0B0G0T0:TrashTarget-Targeted-atVirtual_and_Resource_or_Link
.....

Retrieval Run
-----
bc0f047c-01b1-427f-a439-d451eda02101
-----
onPlay:RunArchives||atSuccessfulRun:Retrieve1Card-fromHeap-grabProgram-toTable-isOptional-isAlternativeRunResult$$TrashMyself-ifSuccessfulRunArchives-isSilent
+++++

.....

Darwin
-----
bc0f047c-01b1-427f-a439-d451eda02102
-----
atTurnStart:Lose1Credits-isCost-isOptional-duringMyTurn$$Put1Virus
+++++
A0B2G0T0:SimplyAnnounce{break ICE subroutine}
.....

Data Leak Reversal
-----
bc0f047c-01b1-427f-a439-d451eda02103
-----
onInstall:UninstallMyself-ifHasnotSucceededCentral$$Gain1Clicks-isSilent-ifHasnotSucceededCentral
+++++
A1B0G0T0:Draw1Card-toTrash-ofOpponent-ifTagged1
.....

Faerie
-----
bc0f047c-01b1-427f-a439-d451eda02104
-----

+++++
A0B0G0T0:SimplyAnnounce{break sentry subroutine}||A0B1G0T0:Put1PlusOne
.....

Mr. Li
-----
bc0f047c-01b1-427f-a439-d451eda02105
-----

+++++
A1B0G0T0:CustomScript
.....

Indexing
-----
bc0f047c-01b1-427f-a439-d451eda02106
-----
onPlay:RunR&D||atSuccessfulRun:CustomScript-isAlternativeRunResult-isOptional-ifSuccessfulRunR&D$$TrashMyself-ifSuccessfulRunR&D-isSilent
+++++

.....

R&D Interface
-----
bc0f047c-01b1-427f-a439-d451eda02107
-----

+++++

.....

Deep Thought
-----
bc0f047c-01b1-427f-a439-d451eda02108
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunR&D||atTurnStart:CustomScript-duringMyTurn
+++++

.....

New Angeles City Hall
-----
bc0f047c-01b1-427f-a439-d451eda02109
-----
whileInstalled:TrashMyself-foreachAgendaLiberated
+++++
A0B2G0T0:Lose1Tags
.....

Eli 1.0
-----
bc0f047c-01b1-427f-a439-d451eda02110
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....

Ruhr Valley
-----
bc0f047c-01b1-427f-a439-d451eda02111
-----

+++++
A0B0G0T0:Autoaction
.....

Ronin
-----
bc0f047c-01b1-427f-a439-d451eda02112
-----

+++++
A1B0G0T1:Remove4Advancement-isCost$$Inflict3NetDamage-onOpponent
.....

Midori
-----
bc0f047c-01b1-427f-a439-d451eda02113
-----

+++++
A0B0G0T0:CustomScript
.....

NBN: The World is Yours
-----
bc0f047c-01b1-427f-a439-d451eda02114
-----
whileInPlay:Provide1HandSize-forCorp
+++++

.....

Project Beale
-----
bc0f047c-01b1-427f-a439-d451eda02115
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore3-div2||whileScored:Gain1Agenda Points-perMarker{Agenda}
+++++

.....

Midseason Replacements
-----
bc0f047c-01b1-427f-a439-d451eda02116
-----
onPlay:Trace6-traceEffects<Gain1Tags-perX-onOpponent,None>
+++++

.....

Flare
-----
bc0f047c-01b1-427f-a439-d451eda02117
-----

+++++
A0B0G0T0:Trace6-isSubroutine-traceEffects<Inflict2MeatDamage-nonPreventable-onOpponent++RunEnd,None>||A0B0G0T0:TrashTarget-Targeted-atHardware
.....

Dedicated Response Team
-----
bc0f047c-01b1-427f-a439-d451eda02118
-----
atJackOut:Inflict2MeatDamage-onOpponent-ifTagged1-ifSuccessfulRunAny
+++++

.....

Burke Bugs
-----
bc0f047c-01b1-427f-a439-d451eda02119
-----

+++++
A0B0G0T0:Trace0-isSubroutine-traceEffects<SimplyAnnounce{force the runner to trash a program},None>
.....

Corporate War
-----
bc0f047c-01b1-427f-a439-d451eda02120
-----
onScore:Gain7Credits-ifIHave7Credits-isSilentHaveChk$$Lose999Credits-ifIHasnt7Credits-isSilentHaveChk
+++++

.....
Cerebral Imaging: Infinite Frontiers
-----
bc0f047c-01b1-427f-a439-d451eda03001
-----
whileInPlay:SetToSpecialHandSize-forCorp
+++++

.....
Next Design: Guarding the Net
-----
bc0f047c-01b1-427f-a439-d451eda03003
-----

+++++
A0B0G0T0:InstallMulti-Targeted-atICE-fromHand||A0B0G0T0:Draw999Cards
.....
Director Haas' Pet Project
-----
bc0f047c-01b1-427f-a439-d451eda03004
-----
onScore:CustomScript
+++++

.....
Efficiency Committee
-----
bc0f047c-01b1-427f-a439-d451eda03005
-----
onScore:Put3Agenda
+++++
A1B0G0T0:Remove1Agenda-isCost$$Gain2Clicks
.....
Project Wotan
-----
bc0f047c-01b1-427f-a439-d451eda03006
-----
onScore:Put3Agenda||atJackOut:Remove999Project Wotan ETR-AutoTargeted-atICE-hasMarker{Project Wotan ETR}
+++++
A0B0G0T0:Remove1Agenda-isCost$$Put1Project Wotan ETR-Targeted-atICE_and_Bioroid-isRezzed
.....
Sentinel Defense Program
-----
bc0f047c-01b1-427f-a439-d451eda03007
-----
whileScored:Inflict1NetDamage-onOpponent-foreachBrainDMGInflicted
+++++

.....
Alix T4LB07
-----
bc0f047c-01b1-427f-a439-d451eda03008
-----
whileInPlay:Put1Power-foreachCardInstall-byMe
+++++
A1B0G0T1:Gain2Credits-perMarker{Power}
.....
Cerebral Overwriter
-----
bc0f047c-01b1-427f-a439-d451eda03009
-----
onAccess:Lose3Credits-isCost-isOptional-ifInstalled-pauseRunner$$Inflict1BrainDamage-onOpponent-perMarker{Advancement}
+++++
A0B3G0T0:Inflict1BrainDamage-onOpponent-perMarker{Advancement}-onAccess	
.....
Director Haas
-----
bc0f047c-01b1-427f-a439-d451eda03010
-----
onRez:Gain1Clicks$$Gain1Max Click||onTrash:Lose1Max Click-ifActive-ifUnscored$$Lose1Clicks-ifActive-ifUnscored$$ScoreMyself-onOpponent-ifAccessed-ifUnscored-preventTrash-runTrashScriptWhileInactive-explicitTrash$$Gain2Agenda Points-onOpponent-ifAccessed-ifUnscored-explicitTrash$$Put2Scored-isSilent-ifAccessed-ifUnscored-explicitTrash
+++++

.....
Haas Arcology AI
-----
bc0f047c-01b1-427f-a439-d451eda03011
-----

+++++
A1B0G0T0:Remove1Advancement-isCost-onlyOnce$$Gain2Clicks
.....
Thomas Haas
-----
bc0f047c-01b1-427f-a439-d451eda03012
-----

+++++
A0B0G0T1:Gain2Credits-perMarker{Advancement}
.....
Bioroid Efficiency Research
-----
bc0f047c-01b1-427f-a439-d451eda03013
-----
Placement:ICE_and_Bioroid-isUnrezzed||onPlay:RezTarget-Targeted-atICE_and_Bioroid-isUnrezzed||onTrash:DerezHost
+++++

.....
Successful Demonstration
-----
bc0f047c-01b1-427f-a439-d451eda03014
-----
onPlay:Gain7Credits
+++++

.....
Heimdall 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03015
-----

+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine||A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine$$RunEnd||A0B0G0T0:RunEnd-isSubroutine	
.....
Howler
-----
bc0f047c-01b1-427f-a439-d451eda03016
-----
atJackOut:DerezTarget-AutoTargeted-atICE_and_Bioroid-hasMarker{Howler}$$TrashTarget-AutoTargeted-atHowler-hasMarker{Howler}$$Remove1Howler-AutoTargeted-isIce-hasMarker{Howler}
+++++
A0B0G0T0:CustomScript
.....
Ichi 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03017
-----

+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain1Tags-onOpponent++Inflict1BrainDamage-onOpponent,None>	
.....
Minelayer
-----
bc0f047c-01b1-427f-a439-d451eda03018
-----

+++++
A0B0G0T0:InstallTarget-Targeted-atICE-fromHand
.....
Viktor 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03019
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<Put1Power,None>||A0B0G0T0:RunEnd-isSubroutine||A0B0G0T0:Remove1Power-isCost$$Inflict1BrainDamage-onOpponent
.....
Zed 1.0
-----
bc0f047c-01b1-427f-a439-d451eda03020
-----

+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent
.....
Awakening Center
-----
bc0f047c-01b1-427f-a439-d451eda03021
-----
atJackOut:TrashTarget-AutoTargeted-atICE_and_Bioroid-hasMarker{AwakeningCenter}
+++++
A1B0G0T0:CustomScript
.....
Tyr's Hand
-----
bc0f047c-01b1-427f-a439-d451eda03022
-----

+++++
A0B0G0T1:SimplyAnnounce{prevent a subroutine from being broken on a piece of bioroid ice protecting this server}
.....
Gila Hands Arcology
-----
bc0f047c-01b1-427f-a439-d451eda03023
-----

+++++
A2B0G0T0:Gain3Credits
.....
Levy University
-----
bc0f047c-01b1-427f-a439-d451eda03024
-----

+++++
A1B1G0T0:Retrieve1Card-grabICE$$ShuffleR&D
.....
Server Diagnostics
-----
bc0f047c-01b1-427f-a439-d451eda03025
-----
atTurnStart:Gain2Credits-duringMyTurn||whileRezzed:TrashMyself-foreachCardInstall-isICE
+++++

.....
Bastion
-----
bc0f047c-01b1-427f-a439-d451eda03026
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Datapike
-----
bc0f047c-01b1-427f-a439-d451eda03027
-----

+++++
A0B0G0T0:UseCustomAbility-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Rielle "Kit" Peddler: Transhuman
-----
bc0f047c-01b1-427f-a439-d451eda03028
-----

+++++

.....
Exile: Streethawk
-----
bc0f047c-01b1-427f-a439-d451eda03030
-----

+++++
A0B0G0T0:Draw1Card
.....
Escher
-----
bc0f047c-01b1-427f-a439-d451eda03031
-----
onPlay:RunHQ||atSuccessfulRun:CustomScript-isOptional-isAlternativeRunResult-ifSuccessfulRunHQ||atJackOut:CustomScript
+++++

.....
Exploratory Romp
-----
bc0f047c-01b1-427f-a439-d451eda03032
-----
onPlay:RunGeneric||atSuccessfulRun:Remove3Advancement-DemiAutoTargeted-hasMarker{Advancement}-choose1-isAlternativeRunResult$$TrashMyself-isSilent
+++++
A0B0G0T0:Remove3Advancement-Targeted-hasMarker{Advancement}
.....
Freelance Coding Contract
-----
bc0f047c-01b1-427f-a439-d451eda03033
-----
onPlay:Discard0Card-Targeted-atProgram-fromHand$$Gain2Credits-perX
+++++

.....
Scavenge
-----
bc0f047c-01b1-427f-a439-d451eda03034
-----
onPlay:CustomScript
+++++

.....
Levy AR Lab Access
-----
bc0f047c-01b1-427f-a439-d451eda03035
-----
onPlay:TrashMulti-AutoTargeted-atEvent_and_nonCurrent-hasntMarker{Scored}$$ReshuffleHeap-warnReshuffle$$ReshuffleStack$$Draw5Cards$$ExileMyself
+++++

.....
Monolith
-----
bc0f047c-01b1-427f-a439-d451eda03036
-----
whileInPlay:Provide3MU||onInstall:InstallMulti-Targeted-atProgram-fromHand-payCost-reduc4||onDamage:Discard1Card-isCost-DemiAutoTargeted-atProgram-fromHand-choose1$$Put1protectionNetBrainDMG
+++++
A0B0G0T0:Discard1Card-isCost-DemiAutoTargeted-atProgram-fromHand-choose1$$Put1protectionNetBrainDMG
.....
Feedback Filter
-----
bc0f047c-01b1-427f-a439-d451eda03037
-----
onDamage:Lose3Credits-isCost$$Put1protectionNetDMG-excludeDummy-isSilent||onDamage:CreateDummy-with2protectionBrainDMG-trashCost
+++++
A0B3G0T0:Put1protectionNetDMG-excludeDummy||A0B0G0T1:CreateDummy-with2protectionBrainDMG-trashCost
.....
Clone Chip
-----
bc0f047c-01b1-427f-a439-d451eda03038
-----

+++++
A0B0G0T1:Retrieve1Card-grabProgram-fromHeap-toTable-payCost
.....
Omni-drive
-----
bc0f047c-01b1-427f-a439-d451eda03039
-----
onInstall:Put1DaemonMU-isSilent$$Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileRezzed:Reduce#CostUse-affectsAll-forMe-ifHosted||ConstantAbility:CountsAsDaemon
+++++
A0B0G0T0:PossessTarget-Targeted-atProgram-targetMine
.....
Atman
-----
bc0f047c-01b1-427f-a439-d451eda03040
-----
onInstall:RequestInt-Msg{How many Power counters do you want to add on Atman?}$$Lose1Credits-perX-isCost-actiontypeUSE$$Put1PlusOnePerm-perX
+++++
A0B1G0T0:SimplyAnnounce{break ICE subroutine}
.....
Cloak
-----
bc0f047c-01b1-427f-a439-d451eda03041
-----
onInstall:Put1Credits-isSilent||whileInstalled:Reduce#CostUse-affectsIcebreaker-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++

.....
Dagger
-----
bc0f047c-01b1-427f-a439-d451eda03042
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B0G0T0:Remove1Credits-AutoTargeted-atStealth-isCost$$Put5PlusOne
.....
Chakana
-----
bc0f047c-01b1-427f-a439-d451eda03043
-----
atSuccessfulRun:Put1Virus-ifSuccessfulRunR&D||whileInPlay:Increase1Advancement-perMarker{Virus}-div3-max1
+++++

.....
Cyber-Cypher
-----
bc0f047c-01b1-427f-a439-d451eda03044
-----
onInstall:Put1CyberCypher-Targeted-isServer
+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B1G0T0:Put1PlusOne	
.....
Paricia
-----
bc0f047c-01b1-427f-a439-d451eda03045
-----
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileInstalled:Reduce#CostTrash-affectsAsset-forMe
+++++

.....
Self-modifying Code
-----
bc0f047c-01b1-427f-a439-d451eda03046
-----

+++++
A0B2G0T0:TrashMyself$$Retrieve1Card-grabProgram-fromStack-toTable-payCost$$ShuffleStack
.....
Sahasrara
-----
bc0f047c-01b1-427f-a439-d451eda03047
-----
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostInstall-affectsProgram-forMe
+++++

.....
Inti
-----
bc0f047c-01b1-427f-a439-d451eda03048
-----

+++++
A0B1G0T0:SimplyAnnounce{break a barrier subroutine}||A0B2G0T0:Put1PlusOne	
.....
Professional Contacts
-----
bc0f047c-01b1-427f-a439-d451eda03049
-----

+++++
A1B0G0T0:Gain1Credits$$Draw1Card
.....
Borrowed Satellite
-----
bc0f047c-01b1-427f-a439-d451eda03050
-----
whileInPlay:Provide1HandSize-forRunner$$Gain1Base Link
+++++

.....
Ice Analyzer
-----
bc0f047c-01b1-427f-a439-d451eda03051
-----
whileInstalled:Reduce#CostInstall-affectsProgram-forMe||whileInPlay:Put1Credits-foreachCardRezzed-typeICE
+++++

.....
Dirty Laundry
-----
bc0f047c-01b1-427f-a439-d451eda03052
-----
onPlay:RunGeneric||atJackOut:Gain5Credits$$TrashMyself-ifSuccessfulRunAny
+++++

.....
Daily Casts
-----
bc0f047c-01b1-427f-a439-d451eda03053
-----
onInstall:Put8Credits||atTurnStart:Transfer2Credits-byMe$$TrashMyself-ifEmpty
+++++

.....
Same Old Thing
-----
bc0f047c-01b1-427f-a439-d451eda03054
-----

+++++
A2B0G0T0:CustomScript
.....
The Source
-----
bc0f047c-01b1-427f-a439-d451eda03055
-----
whileInPlay:Lose3Credits-isCost-foreachAgendaLiberated-typeAgenda||whileInPlay:TrashMyself-foreachAgendaLiberated-typeAgenda||whileInPlay:TrashMyself-foreachAgendaScored||whileInPlay:Increase1Advancement
+++++

.....
Frame Job
-----
bc0f047c-01b1-427f-a439-d451eda04001
-----
onPlay:ExileTarget-Targeted-isScored-targetMine$$Gain1Bad Publicity-onOpponent
+++++

.....
Pawn
-----
bc0f047c-01b1-427f-a439-d451eda04002
-----
CaissaPlace:ICE
+++++
A1B0G0T0:RehostMyself-Targeted-atICE||A0B0G0T0:RehostMyself-Targeted-isICE||A0B0G0T1:InstallTarget-DemiAutoTargeted-atCaissa-fromHand-choose1||A0B0G0T1:Retrieve1Card-fromHeap-grabCaissa-toTable||A0B0G0T0:RehostMyself-Targeted-isICE$$Gain1Credits$$Draw1Cards$$Remove1Test Run-isSilent
.....
Rook
-----
bc0f047c-01b1-427f-a439-d451eda04003
-----
CaissaPlace:ICE
+++++
A1B0G0T0:RehostMyself-Targeted-isICE
.....
Hostage
-----
bc0f047c-01b1-427f-a439-d451eda04004
-----
onPlay:Retrieve1Card-grabConnection$$ShuffleStack||onPlay:Retrieve1Card-grabConnection-toTable-payCost$$ShuffleStack
+++++

.....
Gorman Drip v1
-----
bc0f047c-01b1-427f-a439-d451eda04005
-----
whileInPlay:Put1Virus-foreachCreditClicked-byOpponent||whileInPlay:Put1Virus-foreachCardDrawnClicked-byOpponent
+++++
A1B0G0T1:Gain1Credits-perMarker{Virus}
.....
Lockpick
-----
bc0f047c-01b1-427f-a439-d451eda04006
-----
onInstall:Put1Credits-isSilent||whileInstalled:Reduce#CostUse-affectsDecoder-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++

.....
False Echo
-----
bc0f047c-01b1-427f-a439-d451eda04007
-----

+++++
A0B0G0T1:SimplyAnnounce{force the corporation to rez target ICE or uninstall it to HQ}
.....
Motivation
-----
bc0f047c-01b1-427f-a439-d451eda04008
-----
atTurnStart:CustomScript-duringMyTurn
+++++

.....
John Masanori
-----
bc0f047c-01b1-427f-a439-d451eda04009
-----
atSuccessfulRun:Draw1Card-onlyOnce||atJackOut:Gain1Tags-ifUnsuccessfulRunAny-restrictionMarkerMasanori Unsuccessful
+++++

.....
Project Ares
-----
bc0f047c-01b1-427f-a439-d451eda04010
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore4$$Gain1Bad Publicity-hasOrigMarker{Agenda}
+++++

.....
NEXT Bronze
-----
bc0f047c-01b1-427f-a439-d451eda04011
-----
whileRezzed:Refill1PlusOnePerm-perEveryCard-atNEXT-isICE-isRezzed-foreachCardRezzed-typeNEXT_and_ICE-isSilent||whileRezzed:Remove1PlusOnePerm-foreachCardDerezzed-typeNEXT_and_ICE-isSilent||whileRezzed:Remove1PlusOnePerm-foreachCardTrashed-typeNEXT_and_ICE-isSilent||onDerez:Remove999PlusOnePerm||onTrash:Remove999PlusOnePerm
+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Celebrity Gift
-----
bc0f047c-01b1-427f-a439-d451eda04012
-----
onPlay:CustomScript
+++++

.....
Himitsu-Bako
-----
bc0f047c-01b1-427f-a439-d451eda04013
-----

+++++
A0B1G0T0:UninstallMyself||A0B0G0T0:RunEnd-isSubroutine
.....
Character Assassination
-----
bc0f047c-01b1-427f-a439-d451eda04014
-----
onScore:TrashTarget-DemiAutoTargeted-atResource-choose1
+++++

.....
Jackson Howard
-----
bc0f047c-01b1-427f-a439-d451eda04015
-----

+++++
A1B0G0T0:Draw2Cards||A0B0G0T0:ExileMyself$$Retrieve3Cards-fromArchives-toDeck-upToAmount-doNotReveal$$ShuffleR&D
.....
Invasion of Privacy
-----
bc0f047c-01b1-427f-a439-d451eda04016
-----
onPlay:Trace2-traceEffects<UseCustomAbility,Gain1Bad Publicity>
+++++

.....
Geothermal Fracking
-----
bc0f047c-01b1-427f-a439-d451eda04017
-----
onScore:Put2Agenda
+++++
A1B0G0T0:Remove1Agenda-isCost$$Gain7Credits$$Gain1Bad Publicity
.....
Swarm
-----
bc0f047c-01b1-427f-a439-d451eda04018
-----
onRez:Gain1Bad Publicity
+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:Lose3Credits-onOpponent-perMarker{Advancement}
.....
Cyberdex Trial
-----
bc0f047c-01b1-427f-a439-d451eda04019
-----
onPlay:Remove999Virus-AutoTargeted-atProgram-hasMarker{Virus}-targetOpponents
+++++

.....
Grim
-----
bc0f047c-01b1-427f-a439-d451eda04020
-----
onRez:Gain1Bad Publicity
+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine
.....
The Collective
-----
bc0f047c-01b1-427f-a439-d451eda00001
-----
whileInPlay:CustomScript-foreachCardInstall-duringMyTurn||whileInPlay:CustomScript-foreachCardPlay-duringMyTurn||whileInPlay:CustomScript-foreachCardDrawnClicked-duringMyTurn||whileInPlay:CustomScript-foreachCreditClicked-duringMyTurn||whileInPlay:CustomScript-foreachCardAction-duringMyTurn||atRunStart:CustomScript-duringMyTurn||atTurnStart:CustomScript-duringMyTurn
+++++
A0B0G0T0:Gain1Clicks
.....
Bishop
-----
bc0f047c-01b1-427f-a439-d451eda04021
-----
CaissaPlace:ICE
+++++
A1B0G0T0:RehostMyself-Targeted-isICE

.....
Scheherazade
-----
bc0f047c-01b1-427f-a439-d451eda04022
-----
onInstall:Put1001Scheherazade Hosted-isSilent||onHost:Gain1Credits
+++++
A0B0G0T0:PossessTarget-Targeted-atProgram-targetMine
.....
Hard at Work
-----
bc0f047c-01b1-427f-a439-d451eda04023
-----
atTurnStart:Gain2Credits-duringMyTurn$$Lose1Clicks
+++++

.....
Recon
-----
bc0f047c-01b1-427f-a439-d451eda04024
-----
onPlay:RunGeneric
+++++

.....
Copycat
-----
bc0f047c-01b1-427f-a439-d451eda04025
-----

+++++
A0B0G0T1:CustomScript
.....
Leviathan
-----
bc0f047c-01b1-427f-a439-d451eda04026
-----

+++++
A0B3G0T0:SimplyAnnounce{break up to 3 code gate subroutines}||A0B3G0T0:Put5PlusOne
.....
Eureka!
-----
bc0f047c-01b1-427f-a439-d451eda04027
-----
onPlay:CustomScript
+++++

.....
Record Reconstructor
-----
bc0f047c-01b1-427f-a439-d451eda04028
-----
atSuccessfulRun:Retrieve1Cards-fromArchives-faceUpOnly-toDeck-onOpponent-ifSuccessfulRunArchives-isOptional-isAlternativeRunResult
+++++

.....
Prepaid VoicePAD
-----
bc0f047c-01b1-427f-a439-d451eda04029
-----
onInstall:Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileInstalled:Reduce#CostPlay-affectsEvent-forMe
+++++

.....
Wotan
-----
bc0f047c-01b1-427f-a439-d451eda04030
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Hellion Alpha Test
-----
bc0f047c-01b1-427f-a439-d451eda04031
-----
onPlay:Trace2-traceEffects<SimplyAnnounce{add 1 installed resource to the top of the Runner stack},Gain1Bad Publicity>
+++++
A0B0G0T0:UninstallTarget-toStack-Targeted-atResource$$TrashMyself
.....
Clone Retirement
-----
bc0f047c-01b1-427f-a439-d451eda04032
-----
onScore:Lose1Bad Publicity||onLiberation:Gain1Bad Publicity
+++++

.....
Swordsman
-----
bc0f047c-01b1-427f-a439-d451eda04033
-----

+++++
A0B0G0T0:TrashTarget-Targeted-atProgram_and_AI-isSubroutine||A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine

.....
Shipment from SanSan
-----
bc0f047c-01b1-427f-a439-d451eda04034
-----
onPlay:Put2Advancement-Targeted
+++++

.....
Muckraker
-----
bc0f047c-01b1-427f-a439-d451eda04035
-----
onRez:Gain1Bad Publicity
+++++
A0B0G0T0:Trace1-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>||A0B0G0T0:Trace2-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>||A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>||A0B0G0T0:RunEnd-isSubroutine
.....
The Cleaners
-----
bc0f047c-01b1-427f-a439-d451eda04036
-----
ConstantAbility:Enhance1MeatDamage-isScored
+++++

.....
Elizabeth Mills
-----
bc0f047c-01b1-427f-a439-d451eda04037
-----
onRez:Lose1Bad Publicity
+++++
A1B0G0T1:TrashTarget-Targeted-atLocation$$Gain1Bad Publicity
.....
Off the Grid
-----
bc0f047c-01b1-427f-a439-d451eda04038
-----
atSuccessfulRun:TrashMyself-ifSuccessfulRunHQ
+++++

.....
Profiteering
-----
bc0f047c-01b1-427f-a439-d451eda04039
-----
onScore:RequestInt-Msg{How much bad publicity do you want to take? (max 3)}$$Gain1Bad Publicity-perX$$Gain5Credits-perX
+++++

.....
Restructure
-----
bc0f047c-01b1-427f-a439-d451eda04040
-----
onPlay:Gain15Credits
+++++

.....
Reina Roja
-----
bc0f047c-01b1-427f-a439-d451eda04041
-----
whileInstalled:Increase1CostRez-affectsAll-isICE-forOpponent-onlyOnce
+++++

.....
Deep Red
-----
bc0f047c-01b1-427f-a439-d451eda04042
-----
whileInPlay:Provide3MU||whileInPlay:Put1Deep Red-foreachCardInstall-onTriggerCard-typeCaissa
+++++

.....
Knight
-----
bc0f047c-01b1-427f-a439-d451eda04043
-----
CaissaPlace:ICE
+++++
A0B2G0T0:SimplyAnnounce{break ICE subroutine}||A1B0G0T0:RehostMyself-Targeted-isICE
.....
Running Interference
-----
bc0f047c-01b1-427f-a439-d451eda04044
-----
onPlay:RunGeneric||whileInPlay:IncreaseSCostRez-affectsAll-isICE-forOpponent||atJackOut:TrashMyself
+++++

.....
Expert Schedule Analyzer
-----
bc0f047c-01b1-427f-a439-d451eda04045
-----
atSuccessfulRun:CustomScript-isOptional-isAlternativeRunResult-ifSuccessfulRunHQ-hasOrigMarker{Running}||atJackOut:Remove1Running-isSilent
+++++
A1B0G0T0:RunHQ$$Put1Running
.....
Grifter
-----
bc0f047c-01b1-427f-a439-d451eda04046
-----
atTurnEnd:Gain1Credits-ifHasSucceededAny-duringMyTurn||atTurnEnd:TrashMyself-ifHasnotSucceededAny-duringMyTurn
+++++

.....
Torch
-----
bc0f047c-01b1-427f-a439-d451eda04047
-----

+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B1G0T0:Put1PlusOne
.....
Woman in the Red Dress
-----
bc0f047c-01b1-427f-a439-d451eda04048
-----
atTurnStart:CustomScript-duringMyTurn
+++++

.....
Raymond Flint (Script in parseNewCounters())
-----
bc0f047c-01b1-427f-a439-d451eda04049
-----

+++++
A0B0G0T1:ExposeTarget-Targeted-isUnrezzed
.....
Isabel McGuire
-----
bc0f047c-01b1-427f-a439-d451eda04050
-----

+++++
A1B0G0T0:UninstallTarget-Targeted
.....
Hudson 1.0
-----
bc0f047c-01b1-427f-a439-d451eda04051
-----

+++++
A0B0G0T0:SimplyAnnounce{stop the Runner from accessing more than 1 card during this run}-isSubroutine
.....
Accelerated Diagnostics
-----
bc0f047c-01b1-427f-a439-d451eda04052
-----
onPlay:CustomScript
+++++

.....
Unorthodox Predictions
-----
bc0f047c-01b1-427f-a439-d451eda04053
-----
onScore:ChooseKeyword{Code Gate|Barrier|Sentry}-simpleAnnounce||atTurnStart:Remove1Keyword:Sentry-isSilent$$Remove1Keyword:Barrier-isSilent$$Remove1Keyword:Code Gate-isSilent
+++++

.....
Sundew
-----
bc0f047c-01b1-427f-a439-d451eda04054
-----

+++++
A0B0G0T0:Gain2Credits-onlyOnce
.....
City Surveillance
-----
bc0f047c-01b1-427f-a439-d451eda04055
-----
atTurnStart:CustomScript-duringOpponentTurn
+++++

.....
Snoop
-----
bc0f047c-01b1-427f-a439-d451eda04056
-----

+++++
A0B0G0T0:UseCustomAbility-isFirstCustom||A0B0G0T0:Remove1Power-isCost$$UseCustomAbility-isSecondCustom||A0B0G0T0:Trace3-isSubroutine-traceEffects<Put1Power,None>
.....
Ireress
-----
bc0f047c-01b1-427f-a439-d451eda04057
-----

+++++
A0B0G0T0:Lose1Credits-ofOpponent-isSubroutine
.....
Power Shutdown
-----
bc0f047c-01b1-427f-a439-d451eda04058
-----
onPlay:CustomScript
+++++

.....
Paper Wall
-----
bc0f047c-01b1-427f-a439-d451eda04059
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Interns
-----
bc0f047c-01b1-427f-a439-d451eda04060
-----
onPlay:Retrieve1Card-grabnonOperation-fromArchives-toTable-doNotReveal||onPlay:InstallTarget-DemiAutoTargeted-atnonOperation-fromHand-choose1
+++++

.....
Keyhole
-----
bc0f047c-01b1-427f-a439-d451eda04061
-----
atSuccessfulRun:CustomScript-isAlternativeRunResult-ifSuccessfulRunR&D-hasOrigMarker{Running}||atJackOut:Remove1Running-isSilent
+++++
A1B0G0T0:RunR&D$$Put1Running
.....
Activist Support
-----
bc0f047c-01b1-427f-a439-d451eda04062
-----
atTurnStart:Gain1Tags-ifIHasnt1Tags-duringOpponentTurn||atTurnStart:Gain1Bad Publicity-onOpponent-ifOpponentHasnt1Bad Publicity-duringMyTurn
+++++

.....
Lawyer Up
-----
bc0f047c-01b1-427f-a439-d451eda04063
-----
onPlay:Lose2Tags$$Draw3Cards
+++++

.....
Leverage
-----
bc0f047c-01b1-427f-a439-d451eda04064
-----
onPlay:CustomScript||atTurnStart:TrashMyself-onlyforDummy-duringMyTurn
+++++

.....
Garrote
-----
bc0f047c-01b1-427f-a439-d451eda04065
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B1G0T0:Put1PlusOne	
.....
LLDS Processor
-----
bc0f047c-01b1-427f-a439-d451eda04066
-----
whileInPlay:Put1LLDS Processor-foreachCardInstall-onTriggerCard-typeIcebreaker
+++++

.....
Sharpshooter
-----
bc0f047c-01b1-427f-a439-d451eda04067
-----

+++++
A0B0G0T1:SimplyAnnounce{break any number of destroyer subroutines}||A0B1G0T0:Put2PlusOne
.....
Capstone
-----
bc0f047c-01b1-427f-a439-d451eda04068
-----

+++++
A1B0G0T0:CustomScript
.....
Starlight Crusade Funding
-----
bc0f047c-01b1-427f-a439-d451eda04069
-----
atTurnStart:Lose1Clicks-duringMyTurn
+++++

.....
Rex Campaign
-----
bc0f047c-01b1-427f-a439-d451eda04070
-----
onRez:Put3Power||atTurnStart:Remove1Power-duringMyTurn$$CustomScript
+++++

.....
Fenris
-----
bc0f047c-01b1-427f-a439-d451eda04071
-----
onRez:Gain1Bad Publicity
+++++
A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine||A0B0G0T0:RunEnd-isSubroutine	
.....
Panic Button
-----
bc0f047c-01b1-427f-a439-d451eda04072
-----

+++++
A0B1G0T0:Draw1Card
.....
Shock!
-----
bc0f047c-01b1-427f-a439-d451eda04073
-----
onAccess:Inflict1NetDamage-onOpponent-worksInArchives
+++++

.....
Tsurugi
-----
bc0f047c-01b1-427f-a439-d451eda04074
-----

+++++
A0B0G0T0:RunEnd-isSubroutine||A0B0G0T0:Lose1Credits-isSubroutine||A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine
.....
TGTBT
-----
bc0f047c-01b1-427f-a439-d451eda04075
-----
onAccess:Gain1Tags-onOpponent-worksInArchives
+++++

.....
Sweeps Week
-----
bc0f047c-01b1-427f-a439-d451eda04076
-----
onPlay:CustomScript
+++++

.....
RSVP
-----
bc0f047c-01b1-427f-a439-d451eda04077
-----

+++++
A0B0G0T0:SimplyAnnounce{prevent the Runner from spending any credits for the remainder of this run}
.....
Curtain Wall
-----
bc0f047c-01b1-427f-a439-d451eda04078
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Punitive Counterstrike
-----
bc0f047c-01b1-427f-a439-d451eda04079
-----
onPlay:Trace5-traceEffects<UseCustomAbility,None>
+++++

.....
Veterans Program
-----
bc0f047c-01b1-427f-a439-d451eda04080
-----
onScore:Lose2Bad Publicity
+++++

.....
Chronos Protocol (Jinteki)
-----
bc0f047c-01b1-427f-a439-d451eda00003
-----

+++++

.....
Chronos Protocol (HB)
-----
bc0f047c-01b1-427f-a439-d451eda00004
-----

+++++

.....
Quest Completed
-----
bc0f047c-01b1-427f-a439-d451eda04081
-----
onPlay:CustomScript-Targeted-targetOpponents
+++++

.....
Hemorrhage
-----
bc0f047c-01b1-427f-a439-d451eda04082
-----
atSuccessfulRun:Put1Virus
+++++
A1B0G0T0:Remove2Virus-isCost$$SimplyAnnounce{force the corp to trash one card from their hand}
.....
Tallie Perrault
-----
bc0f047c-01b1-427f-a439-d451eda04083
-----

+++++
A0B0G0T0:Gain1Bad Publicity-onOpponent$$Gain1Tags||A0B0G0T1:Draw1Cards-perOpponentCounter{Bad Publicity}
.....
Executive Wiretaps
-----
bc0f047c-01b1-427f-a439-d451eda04084
-----
onPlay:CustomScript
+++++

.....
Blackguard
-----
bc0f047c-01b1-427f-a439-d451eda04085
-----
whileInPlay:Provide2MU
+++++
A0B0G0T0:SimplyAnnounce{force the corp to rez the accessed card by paying its rez cost, if able.}
.....
CyberSolutions Mem Chip
-----
bc0f047c-01b1-427f-a439-d451eda04086
-----
whileInPlay:Provide2MU
+++++

.....
Alpha
-----
bc0f047c-01b1-427f-a439-d451eda04087
-----

+++++
A0B1G0T0:SimplyAnnounce{break ICE subroutine}||A0B1G0T0:Put1PlusOne	
.....
Omega
-----
bc0f047c-01b1-427f-a439-d451eda04088
-----

+++++
A0B1G0T0:SimplyAnnounce{break ICE subroutine}||A0B1G0T0:Put1PlusOne	
.....
Blackmail
-----
bc0f047c-01b1-427f-a439-d451eda04089
-----
onPlay:Put1Blackmail-AutoTargeted-isUnrezzed-isICE$$RunGeneric||atJackOut:Remove1Blackmail-AutoTargeted-isUnrezzed-isICE
+++++

.....
Blue Level Clearance
-----
bc0f047c-01b1-427f-a439-d451eda04090
-----
onPlay:Gain5Credits$$Draw2Card
+++++

.....
Strongbox
-----
bc0f047c-01b1-427f-a439-d451eda04091
-----

+++++

.....
Toshiyuki Sakai
-----
bc0f047c-01b1-427f-a439-d451eda04092
-----
onAccess:UseCustomAbility-ifInstalled-isOptional-pauseRunner
+++++
A0B0G0T0:UseCustomAbility-ifInstalled
.....
Yagura
-----
bc0f047c-01b1-427f-a439-d451eda04093
-----

+++++
A0B0G0T0:UseCustomAbility-isSubroutine||A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine
.....
Restoring Face
-----
bc0f047c-01b1-427f-a439-d451eda04094
-----
onPlay:TrashTarget-Targeted-atSysop_or_Executive_or_Clone$$Lose2Bad Publicity
+++++
 
.....
Market Research
-----
bc0f047c-01b1-427f-a439-d451eda04095
-----
onScore:Put1Agenda-ifOpponentHave1Tags-isSilentHaveChk||whileScored:Gain1Agenda Points-perMarker{Agenda}
+++++

.....
Wraparound
-----
bc0f047c-01b1-427f-a439-d451eda04096
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
GRNDL
-----
bc0f047c-01b1-427f-a439-d451eda04097
-----
onStartup:Gain5Credits-isSilent$$SetTo1Bad Publicity-isSilent
+++++

.....
Vulcan Coverup
-----
bc0f047c-01b1-427f-a439-d451eda04098
-----
onScore:Inflict2MeatDamage-onOpponent||onLiberation:Gain1Bad Publicity
+++++

.....
GRNDL Refinery
-----
bc0f047c-01b1-427f-a439-d451eda04099
-----

+++++
A1B0G0T1:Gain4Credits-perMarker{Advancement}
.....
Subliminal Messaging
-----
bc0f047c-01b1-427f-a439-d451eda04100
-----
onPlay:Gain1Credits$$Gain1Clicks-ifVarSubliminal_SetTo_False$$SetVarSubliminal-ToTrue
+++++

.....
Singularity
-----
bc0f047c-01b1-427f-a439-d451eda04101
-----
onPlay:RunRemote||atSuccessfulRun:SimplyAnnounce{trash all cards in the server}-isAlternativeRunResult$$TrashMyself
+++++

.....
Queen&#039;s Gambit
-----
bc0f047c-01b1-427f-a439-d451eda04102
-----
onPlay:RequestInt-Max3-Msg{How many advancement counters do you want to put on target card?}$$Put1Advancement-perX-Targeted-isUnrezzed$$Gain2Credits-perX
+++++

.....
Dyson Fractal Generator
-----
bc0f047c-01b1-427f-a439-d451eda04103
-----
onInstall:Put1Credits-isSilent||whileInstalled:Reduce#CostUse-affectsFracter-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++

.....
Silencer
-----
bc0f047c-01b1-427f-a439-d451eda04104
-----
onInstall:Put1Credits-isSilent||whileInstalled:Reduce#CostUse-affectsKiller-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++

.....
Savoir-faire
-----
bc0f047c-01b1-427f-a439-d451eda04105
-----

+++++
A0B2G0T0:InstallTarget-DemiAutoTargeted-atProgram-fromHand-payCost-choose1-onlyOnce
.....
Fall Guy
-----
bc0f047c-01b1-427f-a439-d451eda04106
-----

+++++
A0B0G0T1:SimplyAnnounce{prevent an installed resource from being trashed}||A0B0G0T1:Gain2Credits
.....
Power Nap
-----
bc0f047c-01b1-427f-a439-d451eda04107
-----
onPlay:Gain2Credits$$UseCustomAbility
+++++

.....
Paintbrush
-----
bc0f047c-01b1-427f-a439-d451eda04108
-----

+++++
A1B0G0T0:Put1Keyword:Sentry-Targeted-isICE-isRezzed-isSilent$$Put1Keyword:Code Gate-Targeted-isICE-isSilent-isRezzed$$Put1Keyword:Barrier-Targeted-isICE-isSilent-isRezzed$$Put1Paintbrush-Targeted-isICE-isRezzed
.....
Lucky Find
-----
bc0f047c-01b1-427f-a439-d451eda04109
-----
onPlay:Gain9Credits
+++++

.....
Gyri Labyrinth
-----
bc0f047c-01b1-427f-a439-d451eda04110
-----

+++++
A0B0G0T0:Put1Gyri Labyrinth-AutoTargeted-atIdentity-targetOpponents-isSilent$$SimplyAnnounce{reduce the runner maximum hand size by 2 until the beggining of the Corp turn}
.....
Reclamation Order
-----
bc0f047c-01b1-427f-a439-d451eda04111
-----
onPlay:CustomScript
+++++

.....
Broadcast Square
-----
bc0f047c-01b1-427f-a439-d451eda04112
-----

+++++
A0B0G0T0:Trace3-traceEffects<Lose1Bad Publicity,None>
.....
Corporate Shuffle
-----
bc0f047c-01b1-427f-a439-d451eda04113
-----
onPlay:ReshuffleHQ$$Draw5Cards
+++++

.....
Caprice Nisei
-----
bc0f047c-01b1-427f-a439-d451eda04114
-----

+++++
A0B0G0T0:Psi-psiEffects<RunEnd,None>
.....
Shinobi
-----
bc0f047c-01b1-427f-a439-d451eda04115
-----
onRez:Gain1Bad Publicity
+++++
A0B0G0T0:Trace1-isSubroutine-traceEffects<Inflict1NetDamage-onOpponent,None>||A0B0G0T0:Trace2-isSubroutine-traceEffects<Inflict2NetDamage-onOpponent,None>||A0B0G0T0:Trace3-isSubroutine-traceEffects<Inflict3NetDamage-onOpponent++RunEnd,None>
.....
Marker
-----
bc0f047c-01b1-427f-a439-d451eda04116
-----

+++++
A0B0G0T0:SimplyAnnounce{give the next piece of ICE an End the Run subroutine}-isSubroutine
.....
Hive
-----
bc0f047c-01b1-427f-a439-d451eda04117
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Witness Tampering
-----
bc0f047c-01b1-427f-a439-d451eda04118
-----
onPlay:Lose2Bad Publicity
+++++

.....
NAPD Contract
-----
bc0f047c-01b1-427f-a439-d451eda04119
-----

+++++

.....
Quandary
-----
bc0f047c-01b1-427f-a439-d451eda04120
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Harmony Medtech
-----
bc0f047c-01b1-427f-a439-d451eda05001
-----

+++++

.....
Nisei Division
-----
bc0f047c-01b1-427f-a439-d451eda05002
-----
whileInPlay:Gain1Credits-foreachRevealedPSI
+++++

.....
Tennin Institute
-----
bc0f047c-01b1-427f-a439-d451eda05003
-----

+++++
A0B0G0T0:Put1Advancement-Targeted
.....
House of Knives
-----
bc0f047c-01b1-427f-a439-d451eda05004
-----
onScore:Put3Agenda
+++++
A0B0G0T0:Remove1Agenda-isCost$$Inflict1NetDamage-onOpponent
.....
Medical Breakthrough
-----
bc0f047c-01b1-427f-a439-d451eda05005
-----
whileScored:Decrease1Advancement-affectsMedical Breakthrough
+++++

.....
Philotic Entanglement
-----
bc0f047c-01b1-427f-a439-d451eda05006
-----
onScore:Inflict1NetDamage-onOpponent-perEveryCard-at-isScored-targetOpponents
+++++

.....
The Future Perfect
-----
bc0f047c-01b1-427f-a439-d451eda05007
-----
onAccess:Psi-psiEffects<None,ScoreMyself-onOpponent>-ifNotInstalled-pauseRunner-worksInArchives-disableAutoStealingInArchives
+++++

.....
Chairman Hiro
-----
bc0f047c-01b1-427f-a439-d451eda05008
-----
whileInPlay:Steal2HandSize-forRunner||onTrash:ScoreMyself-onOpponent-ifAccessed-ifUnscored-preventTrash-runTrashScriptWhileInactive-explicitTrash$$Gain2Agenda Points-onOpponent-ifAccessed-ifUnscored-explicitTrash$$Put2Scored-isSilent-ifAccessed-ifUnscored-explicitTrash
+++++

.....
Mental Health Clinic
-----
bc0f047c-01b1-427f-a439-d451eda05009
-----
whileInPlay:Provide1HandSize-forRunner||atTurnStart:Gain1Credits-duringMyTurn
+++++

.....
Psychic Field
-----
bc0f047c-01b1-427f-a439-d451eda05010
-----
onAccess:Psi-psiEffects<Inflict1NetDamage-onOppponent-perEveryCard-at-fromHand,None>-ifInstalled
+++++
A0B0G0T0:Psi-psiEffects<Inflict1NetDamage-onOppponent-perEveryCard-at-fromHand,None>
.....
Shi.Kyu
-----
bc0f047c-01b1-427f-a439-d451eda05011
-----
onAccess:UseCustomAbility-ifNotAccessedInRD-worksInArchives
+++++

.....
Tenma Line
-----
bc0f047c-01b1-427f-a439-d451eda05012
-----

+++++
A1B0G0T0:SimplyAnnounce{Swap 2 pieces of installed ICE}
.....
Cerebral Cast
-----
bc0f047c-01b1-427f-a439-d451eda05013
-----
onPlay:Psi-psiEffects<UseCustomAbility,None>
+++++

.....
Medical Research Fundraiser
-----
bc0f047c-01b1-427f-a439-d451eda05014
-----
onPlay:Gain8Credits$$Gain3Credits-onOpponent
+++++

.....
Mushin No Shin
-----
bc0f047c-01b1-427f-a439-d451eda05015
-----
onPlay:InstallTarget-DemiAutoTargeted-atAsset_or_Upgrade_or_Agenda-fromHand-choose1-with3Advancement
+++++

.....
Inazuma
-----
bc0f047c-01b1-427f-a439-d451eda05016
-----

+++++
A0B0G0T0:SimplyAnnounce{prevent the Runner from breaking any subroutines on the next piece of ice he or she encounters during this run.}-isSubroutine||A0B0G0T0:SimplyAnnounce{prevent the Runner from jacking out until after encountering the next piece of ice during this run}-isSubroutine
.....
Komainu
-----
bc0f047c-01b1-427f-a439-d451eda05017
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine
.....
Pup
-----
bc0f047c-01b1-427f-a439-d451eda05018
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine||A0B0G0T0:Lose1Credits-onOpponent-isSubroutine
.....
Shiro
-----
bc0f047c-01b1-427f-a439-d451eda05019
-----

+++++
A0B0G0T0:UseCustomAbility-isFirstCustom-isSubroutine||A0B0G0T0:Pay1Credits-isCost-isSubroutine||A0B0G0T0:UseCustomAbility-isSecondCustom-isSubroutine
.....
Susanoo-No-Mikoto
-----
bc0f047c-01b1-427f-a439-d451eda05020
-----

+++++
A0B0G0T0:UseCustomAbility-isSubroutine
.....
NeoTokyo City Grid
-----
bc0f047c-01b1-427f-a439-d451eda05021
-----

+++++
A0B0G0T0:Gain1Credits
.....
Tori Hanzo #Hardcoded#
-----
bc0f047c-01b1-427f-a439-d451eda05022
-----

+++++

.....
Plan B
-----
bc0f047c-01b1-427f-a439-d451eda05023
-----
onAccess:UseCustomAbility-ifInstalled
+++++
A0B0G0T0:UseCustomAbility
.....
Guard
-----
bc0f047c-01b1-427f-a439-d451eda05024
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Rainbow
-----
bc0f047c-01b1-427f-a439-d451eda05025
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Diversified Portfolio
-----
bc0f047c-01b1-427f-a439-d451eda05026
-----
onPlay:RequestInt-Msg{How many remote servers with a card installed in them do you currently have?}$$Gain1Credits-perX
+++++

.....
Fast Track
-----
bc0f047c-01b1-427f-a439-d451eda05027
-----
onPlay:Retrieve1Card-grabAgenda$$ShuffleStack
+++++

.....
Iain Stirling
-----
bc0f047c-01b1-427f-a439-d451eda05028
-----
atTurnStart:CustomScript-duringMyTurn
+++++

.....
Ken "Express" Tenma
-----
bc0f047c-01b1-427f-a439-d451eda05029
-----
whileInPlay:Gain1Credits-foreachCardPlay-typeRun_and_Event-byMe-onlyOnce
+++++

.....
Silhouette
-----
bc0f047c-01b1-427f-a439-d451eda05030
-----

+++++
A0B0G0T0:ExposeTarget-Targeted-isUnrezzed
.....
Calling in Favors
-----
bc0f047c-01b1-427f-a439-d451eda05031
-----
onPlay:Gain1Credits-perEveryCard-atConnection_and_Resource
+++++

.....
Early Bird
-----
bc0f047c-01b1-427f-a439-d451eda05032
-----
onPlay:RunGeneric$$Gain1Clicks
+++++

.....
Express Delivery
-----
bc0f047c-01b1-427f-a439-d451eda05033
-----
onPlay:Retrieve1Cards-onTop4Cards-doNotReveal$$ShuffleStack
+++++

.....
Feint
-----
bc0f047c-01b1-427f-a439-d451eda05034
-----
onPlay:RunHQ||atSuccessfulRun:SimplyAnnounce{stop accessing cards}-isAlternativeRunResult$$TrashMyself-ifSuccessfulRunHQ-isSilent
+++++

.....
Legwork
-----
bc0f047c-01b1-427f-a439-d451eda05035
-----
onPlay:RunHQ
+++++

.....
Planned Assault
-----
bc0f047c-01b1-427f-a439-d451eda05036
-----
onPlay:Retrieve1Card-grabRun_and_Event-toTable-payCost$$ShuffleStack
+++++

.....
Logos
-----
bc0f047c-01b1-427f-a439-d451eda05037
-----
whileInPlay:Provide1HandSize-forRunner||whileInPlay:Provide1MU
+++++
A0B0G0T0:Retrieve1Card-doNotReveal$$ShuffleStack
.....
Public Terminal
-----
bc0f047c-01b1-427f-a439-d451eda05038
-----
onInstall:Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileInstalled:Reduce#CostPlay-affectsRun_and_Event-forMe
+++++

.....
Unregistered S&amp;W 35
-----
bc0f047c-01b1-427f-a439-d451eda05039
-----

+++++
A2B0G0T0:TrashTarget-Targeted-atBioroid_and_nonICE_or_Clone_or_Executive_or_Sysop
.....
Window
-----
bc0f047c-01b1-427f-a439-d451eda05040
-----

+++++
A1B0G0T0:UseCustomAbility
.....
Alias
-----
bc0f047c-01b1-427f-a439-d451eda05041
-----

+++++
A0B1G0T0:SimplyAnnounce{break sentry subroutine}||A0B2G0T0:Put3PlusOne
.....
Breach
-----
bc0f047c-01b1-427f-a439-d451eda05042
-----

+++++
A0B2G0T0:SimplyAnnounce{break up to 3 barrier subroutine}||A0B2G0T0:Put4PlusOne
.....
Bug
-----
bc0f047c-01b1-427f-a439-d451eda05043
-----

+++++
A0B2G0T0:UseCustomAbility
.....
Gingerbread
-----
bc0f047c-01b1-427f-a439-d451eda05044
-----

+++++
A0B1G0T0:SimplyAnnounce{break tracer subroutine}||A0B2G0T0:Put3PlusOne
.....
Grappling Hook
-----
bc0f047c-01b1-427f-a439-d451eda05045
-----

+++++
A0B0G0T1:SimplyAnnounce{break all but 1 subroutines on a piece of ice.}
.....
Passport
-----
bc0f047c-01b1-427f-a439-d451eda05046
-----

+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B2G0T0:Put2PlusOne
.....
Push Your Luck
-----
bc0f047c-01b1-427f-a439-d451eda05047
-----
onPlay:CustomScript
+++++

.....
Security Testing
-----
bc0f047c-01b1-427f-a439-d451eda05048
-----
atTurnStart:CustomScript-duringMyTurn||atSuccessfulRun:CustomScript||atTurnEnd:Remove999SecurityTesting-AutoTargeted_atServer_or_Security Testing
+++++
A0B0G0T0:Remove999SecurityTesting-Targeted-isCost$$Gain2Credits-onlyOnce
.....
Theophilius Bagbiter
-----
bc0f047c-01b1-427f-a439-d451eda05049
-----
onInstall:Lose999Credits||whileInPlay:SetToSpecialHandSize-forRunner
+++++

.....
Tri-maf Contact
-----
bc0f047c-01b1-427f-a439-d451eda05050
-----
onTrash:Inflict3MeatDamage
+++++
A1B0G0T0:Gain2Credits-onlyOnce
.....
Mass Install
-----
bc0f047c-01b1-427f-a439-d451eda05051
-----
onPlay:InstallMulti-Targeted-atProgram-fromHand-payCost
+++++

.....
Q-Coherence Chip
-----
bc0f047c-01b1-427f-a439-d451eda05052
-----
whileInPlay:Provide1MU||whileInPlay:TrashMyself-foreachCardTrashed-typeProgram
+++++

.....
Overmind
-----
bc0f047c-01b1-427f-a439-d451eda05053
-----
onInstall:Put1Power-perMyCounter{MU}$$Remove1Power-isSilent
+++++
A0B0G0T0:Remove1Power-isCost$$SimplyAnnounce{break ICE subroutine}||A0B1G0T0:Put1PlusOne
.....
Oracle May
-----
bc0f047c-01b1-427f-a439-d451eda05054
-----

+++++
A1B0G0T0:UseCustomAbility-onlyOnce
.....
Donut Taganes
-----
bc0f047c-01b1-427f-a439-d451eda05055
-----
whileInstalled:Increase1CostPlay-affectsAll
+++++

.....
Domestic Sleepers
-----
bc0f047c-01b1-427f-a439-d451eda06001
-----
onTrash:Lose1Agenda Points-ifOrigmarkers{Agenda}ge1
+++++
A3B0G0T0:Put1Agenda$$Gain1Agenda Points-ifOrigmarkers{Agenda}eq1
.....
NEXT Silver
-----
bc0f047c-01b1-427f-a439-d451eda06002
-----
whileRezzed:Refill1NEXTSubroutine-perEveryCard-atNEXT-isICE-isRezzed-foreachCardRezzed-typeNEXT_and_ICE-isSilent||whileRezzed:Remove1NEXTSubroutine-foreachCardDerezzed-typeNEXT_and_ICE-isSilent||whileRezzed:Remove1NEXTSubroutine-foreachCardTrashed-typeNEXT_and_ICE-isSilent||onDerez:Remove999NEXTSubroutine||onTrash:Remove999NEXTSubroutine
+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Lotus Field
-----
bc0f047c-01b1-427f-a439-d451eda06003
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Mutate
-----
bc0f047c-01b1-427f-a439-d451eda06004
-----
onPlay:CustomScript
+++++

.....
Near-Earth Hub
-----
bc0f047c-01b1-427f-a439-d451eda06005
-----

+++++
A0B0G0T0:Draw1Card-onlyOnce
.....
Primary Transmission Dish
-----
bc0f047c-01b1-427f-a439-d451eda06006
-----
onRez:Put3Credits||atTurnPreStart:Refill3Credits-duringMyTurn||whileRezzed:Reduce#CostTrace-affectsAll-forMe
+++++

.....
Midway Station Grid
-----
bc0f047c-01b1-427f-a439-d451eda06007
-----

+++++
A0B0G0T0:Lose1Credits-onOpponent
.....
The Root
-----
bc0f047c-01b1-427f-a439-d451eda06008
-----
onRez:Put3Credits||atTurnPreStart:Refill3Credits-duringMyTurn||whileRezzed:Reduce#CostAdvancement-affectsAll-forMe||whileRezzed:Reduce#CostInstall-affectsAll-forMe||whileRezzed:Reduce#CostRez-affectsAll-forMe
+++++
A0B0G0T0:Remove1Credits-isCost$$SimplyAnnounce{to pay for ICE install costs}
.....
Taurus
-----
bc0f047c-01b1-427f-a439-d451eda06009
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<SimplyAnnounce{trash a piece of hardware},None>||A0B0G0T0:TrashTarget-Targeted-atHardware
.....
Mother Goddess
-----
bc0f047c-01b1-427f-a439-d451eda06010
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Galahad
-----
bc0f047c-01b1-427f-a439-d451eda06011
-----
atJackOut:TrashMyself-onlyforDummy
+++++
A0B0G0T0:UseCustomAbility-excludeDummy||A0B0G0T0:RunEnd-isSubroutine-excludeDummy||A0B0G0T0:RunEnd-isSubroutine-onlyforDummy$$TrashMyself-isSilent
.....
Bad Times
-----
bc0f047c-01b1-427f-a439-d451eda06012
-----
onPlay:SimplyAnnounce{reduce the Runner's memory limit by 2 until the end of the turn.}
+++++

.....
Cyber Threat
-----
bc0f047c-01b1-427f-a439-d451eda06013
-----
onPlay:CustomScript
+++++

.....
Lamprey
-----
bc0f047c-01b1-427f-a439-d451eda06014
-----
atSuccessfulRun:Lose1Credits-onOpponent-ifSuccessfulRunHQ||whileInPlay:TrashMyself-foreachVirusPurged
+++++

.....
Paper Tripping
-----
bc0f047c-01b1-427f-a439-d451eda06015
-----
onPlay:Lose999Tags
+++++

.....
Power Tap
-----
bc0f047c-01b1-427f-a439-d451eda06016
-----
whileInPlay:Gain1Credits-foreachInitiatedTrace
+++++

.....
Nasir Meidan
-----
bc0f047c-01b1-427f-a439-d451eda06017
-----

+++++
A0B0G0T0:CustomScript
.....
Social Engineering
-----
bc0f047c-01b1-427f-a439-d451eda06018
-----
atTurnEnd:TrashMyself||onPlay:Put1Social Engineering-Targeted-isICE-isSilent$$CreateDummy||whileInPlay:UseCustomAbility-foreachCardRezzed-typeICE-onTriggerCard-onlyforDummy
+++++

.....
Leprechaun
-----
bc0f047c-01b1-427f-a439-d451eda06019
-----
onInstall:Put6DaemonMU-isSilent
+++++
A0B0G0T0:PossessTarget-Targeted-atProgram-targetMine
.....
Eden Shard
-----
bc0f047c-01b1-427f-a439-d451eda06020
-----
onDragDrop:IgnoreCosts-isSourceShard
+++++
A0B0G0T1:Draw2Cards-onOpponent
.....
The Foundry
-----
bc0f047c-01b1-427f-a439-d451eda06021
-----
whileInPlay:UseCustomAbility-foreachCardRezzed-typeICE-onTriggerCard-typeICE-byMe-onlyOnce
+++++

.....
Enhanced Login Protocol
-----
bc0f047c-01b1-427f-a439-d451eda06022
-----

+++++

.....
Heinlein Grid
-----
bc0f047c-01b1-427f-a439-d451eda06023
-----

+++++
A0B0G0T0:Lose999Credits-onOpponent
.....
Encrypted Portals
-----
bc0f047c-01b1-427f-a439-d451eda06024
-----
onScore:Gain1Credits-perEveryCard-atCode Gate-isRezzed
+++++

.....
Cerebral Static
-----
bc0f047c-01b1-427f-a439-d451eda06025
-----

+++++

.....
Targeted Marketing
-----
bc0f047c-01b1-427f-a439-d451eda06026
-----

+++++
A0B0G0T0:Gain10Credits
.....
Information Overload
-----
bc0f047c-01b1-427f-a439-d451eda06027
-----

+++++
A0B0G0T0:Trace1-traceEffects<Gain1Tags-onOpponent,None>
.....
Paywall Implementation
-----
bc0f047c-01b1-427f-a439-d451eda06028
-----
atSuccessfulRun:Gain1Credits
+++++

.....
Sealed Vault
-----
bc0f047c-01b1-427f-a439-d451eda06029
-----

+++++
A0B0G0T0:CustomScript
.....
Eden Fragment
-----
bc0f047c-01b1-427f-a439-d451eda06030
-----

+++++

.....
Lag Time
-----
bc0f047c-01b1-427f-a439-d451eda06031
-----

+++++

.....
Will-o&#039;-the-Wisp
-----
bc0f047c-01b1-427f-a439-d451eda06032
-----

+++++
A0B0G0T1:SendToBottomTarget-Targeted-atIcebreaker
.....
D4v1d
-----
bc0f047c-01b1-427f-a439-d451eda06033
-----
onInstall:Put3Power
+++++
A0B0G0T0:Remove1Power-isCost$$SimplyAnnounce{break ICE Subroutine}
.....
Scrubbed
-----
bc0f047c-01b1-427f-a439-d451eda06034
-----

+++++
A0B0G0T0:Put2MinusOne-Targeted-atICE-onlyOnce
.....
Three Steps Ahead
-----
bc0f047c-01b1-427f-a439-d451eda06035
-----
onPlay:CreateDummy||atSuccessfulRun:Put1Power||atTurnEnd:Gain2Credits-perMarker{Power}$$TrashMyself-isSilent
+++++

.....
Unscheduled Maintenance
-----
bc0f047c-01b1-427f-a439-d451eda06036
-----

+++++

.....
Cache
-----
bc0f047c-01b1-427f-a439-d451eda06037
-----
onInstall:Put3Virus
+++++
A0B0G0T0:Remove1Virus-isCost$$Gain1Credits
.....
Net Celebrity
-----
bc0f047c-01b1-427f-a439-d451eda06038
-----
onPlay:Put1Credits-isSilent||whileRunning:Reduce#CostAll-affectsAll-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++

.....
Energy Regulator
-----
bc0f047c-01b1-427f-a439-d451eda06039
-----

+++++
A0B3G0T0:SimplyAnnounce{prevent an installed piece of hardware from being trashed}||A0B0G0T1:SimplyAnnounce{prevent an installed piece of hardware from being trashed}
.....
Ghost Runner
-----
bc0f047c-01b1-427f-a439-d451eda06040
-----
onInstall:Put3Credits$$ReserveMyself||whileRunning:Reduce#CostAll-affectsAll-forMe-trashCost-ifEmpty
+++++

.....
IQ
-----
bc0f047c-01b1-427f-a439-d451eda06041
-----

+++++

.....
Eliza&#039;s Toybox
-----
bc0f047c-01b1-427f-a439-d451eda06042
-----

+++++
A3B0G0T0:RezTarget-Targeted
.....
Kitsune
-----
bc0f047c-01b1-427f-a439-d451eda06043
-----

+++++
A0B0G0T0:CustomScript
.....
Port Anson Grid
-----
bc0f047c-01b1-427f-a439-d451eda06044
-----

+++++

.....
The News Now Hour
-----
bc0f047c-01b1-427f-a439-d451eda06045
-----

+++++

.....
Manhunt
-----
bc0f047c-01b1-427f-a439-d451eda06046
-----

+++++
A0B0G0T0:Trace2-traceEffects<Gain1Tags-onOpponent,None>
.....
Wendigo
-----
bc0f047c-01b1-427f-a439-d451eda06047
-----

+++++

.....
Crisium Grid
-----
bc0f047c-01b1-427f-a439-d451eda06048
-----
atJackOut:Remove999Enabled
+++++
A0B0G0T0:Put1Enabled
.....
Chronos Project
-----
bc0f047c-01b1-427f-a439-d451eda06049
-----
onScore:ExileMulti-AutoTargeted-fromArchives-targetOpponents
+++++

.....
Shattered Remains
-----
bc0f047c-01b1-427f-a439-d451eda06050
-----
onAccess:UseCustomAbility-ifInstalled-isOptional-pauseRunner
+++++
A0B1G0T0:TrashMulti-Targeted-atHardware-onAccess
.....
Lancelot
-----
bc0f047c-01b1-427f-a439-d451eda06051
-----
atJackOut:TrashMyself-onlyforDummy
+++++
A0B0G0T0:UseCustomAbility-excludeDummy||A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine-excludeDummy||A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine-onlyforDummy$$TrashMyself-isSilent
.....
Quetzal
-----
bc0f047c-01b1-427f-a439-d451eda06052
-----

+++++
A0B0G0T0:SimplyAnnounce{break barrier subroutine}-onlyOnce
.....
BlacKat
-----
bc0f047c-01b1-427f-a439-d451eda06053
-----

+++++
A0B1G0T0:SimplyAnnounce{break 1 barrier subroutine}||A0B1G0T0:SimplyAnnounce{break up to 3 barrier subroutines}||A0B2G0T0:Put1PlusOne||A0B2G0T0:Put2PlusOne
.....
Duggar&#039;s
-----
bc0f047c-01b1-427f-a439-d451eda06054
-----

+++++
A4B0G0T0:Draw10Cards
.....
BOX-E
-----
bc0f047c-01b1-427f-a439-d451eda06055
-----
whileInPlay:Provide2HandSize-forRunner||whileInPlay:Provide2MU
+++++

.....
The Supplier
-----
bc0f047c-01b1-427f-a439-d451eda06056
-----

+++++
A1B0G0T0:CustomScript
.....
Refractor
-----
bc0f047c-01b1-427f-a439-d451eda06057
-----

+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B0G0T0:Remove1Credits-AutoTargeted-atStealth-isCost$$Put3PlusOne
.....
Order of Sol
-----
bc0f047c-01b1-427f-a439-d451eda06058
-----

+++++
A0B0G0T0:Gain1Credits-onlyOnce
.....
Hades Shard
-----
bc0f047c-01b1-427f-a439-d451eda06059
-----
onDragDrop:IgnoreCosts-isSourceShard
+++++
A0B0G0T1:CustomScript
.....
Rachel Beckman
-----
bc0f047c-01b1-427f-a439-d451eda06060
-----
whileInstalled:Gain1Max Click
+++++

.....
Architect
-----
bc0f047c-01b1-427f-a439-d451eda06061
-----

+++++
A0B0G0T0:Retrieve1Card-toTable-onTop5Cards-doNotReveal-isSubroutine-showDuplicates||A0B0G0T0:Retrieve1Card-fromArchives-toTable-doNotReveal-isSubroutine||A0B0G0T0:InstallTarget-DemiAutoTargeted-atnonOperation-choose1-fromHand-isSubroutine
.....
Peak Efficiency
-----
bc0f047c-01b1-427f-a439-d451eda06062
-----
onPlay:Gain1Credits-perEveryCard-atICE-isRezzed
+++++

.....
Labyrinthine Servers
-----
bc0f047c-01b1-427f-a439-d451eda06063
-----
onScore:Put2Agenda
+++++
A0B0G0T0:Remove1Agenda-isCost$$SimplyAnnounce{prevent the runner from jacking out for the remainder of this run}
.....
Ashigaru
-----
bc0f047c-01b1-427f-a439-d451eda06064
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Mamba
-----
bc0f047c-01b1-427f-a439-d451eda06065
-----

+++++
A0B0G0T0:Remove1Power-isCost$$Inflict1NetDamage-onOpponent||A0B0G0T0:Inflict1NetDamage-onOpponent-isSubroutine||A0B0G0T0:Psi-psiEffects<Put1Power,None>-isSubroutine
.....
Reversed Accounts
-----
bc0f047c-01b1-427f-a439-d451eda06066
-----

+++++
A1B0G0T1:Lose4Credits-onOpponent-perMarker{Advancement}
.....
Universal Connectivity Fee
-----
bc0f047c-01b1-427f-a439-d451eda06067
-----

+++++
A0B0G0T0:Lose1Credits-onOpponent-isSubroutine||A0B0G0T0:Lose999Credits-onOpponent-ifTagged1-isSubroutine$$TrashMyself
.....
Blue Sun
-----
bc0f047c-01b1-427f-a439-d451eda06068
-----

+++++
A0B0G0T0:Gain1Credits-perTargetProperty{Cost}-Targeted-isRezzed-targetMine-onlyOnce$$UninstallTarget-Targeted-targetMine-isRezzed
.....
Changeling
-----
bc0f047c-01b1-427f-a439-d451eda06069
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Reuse
-----
bc0f047c-01b1-427f-a439-d451eda06070
-----
onPlay:Gain2Credits-perTargetCard-fromHand$$TrashMulti-Targeted-fromHand
+++++

.....
Hades Fragment
-----
bc0f047c-01b1-427f-a439-d451eda06071
-----

+++++
A0B0G0T0:Retrieve1Card-fromArchives-toDeck-sendToBottom-doNotReveal-onlyOnce
.....
Docklands Crackdown
-----
bc0f047c-01b1-427f-a439-d451eda06072
-----
whileRezzed:IncreaseXCostInstall-affectsAll-forOpponent-perMarker{Power}-onlyOnce
+++++
A2B0G0T0:Put1Power
.....
Inject
-----
bc0f047c-01b1-427f-a439-d451eda06073
-----
onPlay:CustomScript
+++++

.....
Origami
-----
bc0f047c-01b1-427f-a439-d451eda06074
-----
whileInPlay:ProvideSpecialHandSize-forRunner
+++++

.....
Fester
-----
bc0f047c-01b1-427f-a439-d451eda06075
-----
whileInPlay:Lose2Credits-onOpponent-foreachVirusPurged
+++++

.....
Autoscripter
-----
bc0f047c-01b1-427f-a439-d451eda06076
-----
atJackOut:TrashMyself-ifUnsuccessfulRunAny
+++++
A0B0G0T0:Gain1Clicks-onlyOnce
.....
Switchblade
-----
bc0f047c-01b1-427f-a439-d451eda06077
-----

+++++
A0B0G0T0:Remove1Credits-AutoTargeted-atStealth-isCost$$SimplyAnnounce{break any number of sentry subroutines}||A0B0G0T0:Remove1Credits-AutoTargeted-atStealth-isCost$$Put7PlusOne
.....
Trade-In
-----
bc0f047c-01b1-427f-a439-d451eda06078
-----
onPlay:UseCustomAbility$$TrashTarget-Targeted-atHardware-isSilent$$Retrieve1Card-grabHardware
+++++

.....
Astrolabe
-----
bc0f047c-01b1-427f-a439-d451eda06079
-----
whileInPlay:Provide1MU
+++++
A0B0G0T0:Draw1Cards
.....
Angel Arena
-----
bc0f047c-01b1-427f-a439-d451eda06080
-----
onInstall:RequestInt-Msg{What install cost do you want to use?}$$Lose1Credits-perX-isCost$$Put1Power-perX
+++++
A0B0G0T0:Remove1Power-isCost$$UseCustomAbility
.....
Bifrost Array
-----
bc0f047c-01b1-427f-a439-d451eda06081
-----
onScore:CustomScript
+++++

......
Sagittarius
-----
bc0f047c-01b1-427f-a439-d451eda06082
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<SimplyAnnounce{trash one program},None>||A0B0G0T0:TrashTarget-Targeted-atProgram
.....
Hostile Infrastructure
-----
bc0f047c-01b1-427f-a439-d451eda06083
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent
.....
Gemini
-----
bc0f047c-01b1-427f-a439-d451eda06084
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<Inflict1NetDamage-onOppponent,None>||A0B0G0T0:Inflict1NetDamage-onOppponent
.....
License Acquisition
-----
bc0f047c-01b1-427f-a439-d451eda06085
-----
onScore:Retrieve1Card-fromArchives-grabAsset_or_Upgrade-toTable-rezFree||onScore:InstallTarget-fromHand-DemiAutoTargeted-atAsset_or_Upgrade-choose1-rezFree
+++++

.....
Daily Business Show
-----
bc0f047c-01b1-427f-a439-d451eda06086
-----

+++++

.....
Superior Cyberwalls
-----
bc0f047c-01b1-427f-a439-d451eda06087
-----
onScore:Gain1Credits-perEveryCard-atBarrier-isRezzed
+++++

.....
Executive Boot Camp
-----
bc0f047c-01b1-427f-a439-d451eda06088
-----

+++++
A0B0G0T0:RezTarget-Targeted-atnonOperation_andnonAgenda-payCost-reduc1-onlyOnce||A0B1G0T1:Retrieve1Card-grabAsset$$ShuffleR&D
.....
Lycan
-----
bc0f047c-01b1-427f-a439-d451eda06089
-----

+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine
.....
Snatch and Grab
-----
bc0f047c-01b1-427f-a439-d451eda06090
-----
onPlay:Trace3<SimplyAnnounce{trash a connection unless the runner takes 1 tag},None>
+++++

.....
Merlin
-----
bc0f047c-01b1-427f-a439-d451eda06091
-----

+++++
A0B0G0T0:UseCustomAbility-excludeDummy||A0B0G0T0:Inflict2NetDamage-onOpponent-isSubroutine-excludeDummy||A0B0G0T0:Inflict2NetDamage-onOpponent-isSubroutine-onlyforDummy$$TrashMyself-isSilent
.....
Shell Corporation
-----
bc0f047c-01b1-427f-a439-d451eda06092
-----

+++++
A1B0G0T0:Put3Credits-onlyOnce||A1B0G0T0:Transfer999Credits-onlyOnce
.....
Ekomind
-----
bc0f047c-01b1-427f-a439-d451eda06093
-----
whileInPlay:SetToSpecialMU
+++++

.....
Cerberus "Cuj.0" H3
-----
bc0f047c-01b1-427f-a439-d451eda06094
-----
onInstall:Put4Power
+++++
A0B0G0T0:Remove1Power-isCost$$SimplyAnnounce{break up to 2 sentry subroutines}||A0B1G0T0:Put1PlusOne	
.....
Leela Patel
-----
bc0f047c-01b1-427f-a439-d451eda06095
-----

+++++
A0B0G0T0:UninstallTarget-Targeted-targetOpponents-isUnrezzed
.....
Cerberus "Rex" H2
-----
bc0f047c-01b1-427f-a439-d451eda06096
-----
onInstall:Put4Power
+++++
A0B0G0T0:Remove1Power-isCost$$SimplyAnnounce{break up to 2 code gate subroutines}||A0B1G0T0:Put1PlusOne	
.....
Zona Sul Shipping
-----
bc0f047c-01b1-427f-a439-d451eda06097
-----
atTurnStart:Put1Credits-duringMyTurn
+++++
A1B0G0T0:Transfer999Credits
.....
Cybsoft MacroDrive
-----
bc0f047c-01b1-427f-a439-d451eda06098
-----
onInstall:Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileRezzed:Reduce#CostInstall-affectsProgram-forMe
+++++

.....
Cerberus "Lady" H1
-----
bc0f047c-01b1-427f-a439-d451eda06099
-----
onInstall:Put4Power
+++++
A0B0G0T0:Remove1Power-isCost$$SimplyAnnounce{break up to 2 barrier subroutines}||A0B1G0T0:Put1PlusOne	
.....
Utopia Shard
-----
bc0f047c-01b1-427f-a439-d451eda06100
-----
onDragDrop:IgnoreCosts-isSourceShard
+++++
A0B0G0T0:CustomScript
.....
Helium-3 Deposit
-----
bc0f047c-01b1-427f-a439-d451eda06101
-----
onScore:Put2Power-DemiAutoTargeted-hasMarker{Power}-choose1
+++++

.....
Errand Boy
-----
bc0f047c-01b1-427f-a439-d451eda06102
-----

+++++
A0B0G0T0:Gain1Credits-isSubroutine||A0B0G0T0:Draw1Card-isSubroutine
.....
IT Department
-----
bc0f047c-01b1-427f-a439-d451eda06103
-----

+++++
A1B0G0T0:Put1Power||A0B0G0T0:Put1IT Department-Targeted-atICE-isRezzed$$Remove1Power
.....
Markus 1.0
-----
bc0f047c-01b1-427f-a439-d451eda06104
-----

+++++
A0B0G0T0:SimplyAnnounce{Force the runner to trash one of their installed cards}-isSubroutine||A0B0G0T0:RunEnd-isSubroutine
.....
Industrial Genomics
-----
bc0f047c-01b1-427f-a439-d451eda06105
-----
whileInPlay:IncreaseSCostTrash-affectsAll-forOpponent
+++++

.....
Turtlebacks
-----
bc0f047c-01b1-427f-a439-d451eda06106
-----

+++++
A0B0G0T0:Gain1Credits
.....
Shoot the Moon
-----
bc0f047c-01b1-427f-a439-d451eda06107
-----
onPlay:RezMultiple-Targeted-isICE-isUnrezzed-ifTagged1
+++++

.....
Troll
-----
bc0f047c-01b1-427f-a439-d451eda06108
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<UseCustomAbility,None>
.....
Virgo
-----
bc0f047c-01b1-427f-a439-d451eda06109
-----

+++++
A0B0G0T0:Trace2-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>||A0B0G0T0:Gain1Tags-onOpponent
.....
Utopia Fragment
-----
bc0f047c-01b1-427f-a439-d451eda06110
-----

+++++

.....
Excalibur
-----
bc0f047c-01b1-427f-a439-d451eda06111
-----
atJackOut:TrashMyself-onlyforDummy
+++++
A0B0G0T0:SimplyAnnounce{stop the runner from making more runs}-isSubroutine-excludeDummy||A0B0G0T0:SimplyAnnounce{stop the runner from making more runs}-isSubroutine-onlyforDummy$$TrashMyself-isSilent
.....
Self-destruct
-----
bc0f047c-01b1-427f-a439-d451eda06112
-----

+++++
A0B0G0T1:Trace1-perTargetAsset_or_Upgrade_or_Agenda_or_ICE-traceEffects<Inflict3NetDamage-onOpponent,None>$$TrashMultiple-Targeted-atAsset_or_Upgrade_or_Agenda-isSilent
.....
Incubator
-----
bc0f047c-01b1-427f-a439-d451eda06113
-----
atTurnStart:Put1Virus-duringMyTurn
+++++
A1B0G0T1:Put1Virus-perMyselfMarker{Virus}-Targeted-atVirus_and_Program
.....
Ixodidae
-----
bc0f047c-01b1-427f-a439-d451eda06114
-----
whileInPlay:TrashMyself-foreachVirusPurged
+++++
A0B0G0T0:Gain1Credits
.....
Code Siphon
-----
bc0f047c-01b1-427f-a439-d451eda06115
-----
onPlay:RunR&D||atSuccessfulRun:CustomScript-isOptional-isAlternativeRunResult$$Gain1Tags||atJackOut:TrashMyself-isSilent
+++++

.....
Collective Consciousness
-----
bc0f047c-01b1-427f-a439-d451eda06116
-----
whileInPlay:Draw1Card-foreachCardRezzed-typeICE
+++++

.....
Sage
-----
bc0f047c-01b1-427f-a439-d451eda06117
-----

+++++
A0B2G0T0:SimplyAnnounce{break code gate or barrier subroutine}
.....
Bribery
-----
bc0f047c-01b1-427f-a439-d451eda06118
-----
onPlay:RequestInt-msg{How much do you want to bribe with?}$$Lose1Credits-perX-isCost$$Put1Power-perX$$RunGeneric||whileInPlay:IncreaseXCostRez-affectsAll-isICE-forOpponent-perMarker{Power}-onlyOnce||atJackOut:TrashMyself-isSilent
+++++

.....
Au Revoir
-----
bc0f047c-01b1-427f-a439-d451eda06119
-----

+++++
A0B0G0T0:Gain1Credits
.....
Earthrise Hotel
-----
bc0f047c-01b1-427f-a439-d451eda06120
-----
onInstall:Put3Power||atTurnStart:Remove1Power-isCost-isSilent-duringMyTurn$$Draw2Cards$$CustomScript
+++++

.....
Argus Security
-----
bc0f047c-01b1-427f-a439-d451eda07001
-----
whileInPlay:CustomScript-foreachAgendaLiberated
+++++

.....
Gagarin Deep Space
-----
bc0f047c-01b1-427f-a439-d451eda07002
-----

+++++

.....
Titan Transnational
-----
bc0f047c-01b1-427f-a439-d451eda07003
-----
whileInPlay:Put1Agenda-foreachAgendaScored-onTriggerCard
+++++

.....
Firmware Updates
-----
bc0f047c-01b1-427f-a439-d451eda07004
-----
onScore:Put3Agenda
+++++
A0B0G0T0:Remove1Agenda-isCost$$Put1Advancement-Targeted-atICE-onlyOnce
.....
Glenn Station
-----
bc0f047c-01b1-427f-a439-d451eda07005
-----

+++++
A1B0G0T0:CustomScript
.....
Government Takeover
-----
bc0f047c-01b1-427f-a439-d451eda07006
-----

+++++
A1B0G0T0:Gain3Credits
.....
High-Risk Investment
-----
bc0f047c-01b1-427f-a439-d451eda07007
-----
onScore:Put1Agenda
+++++
A1B0G0T0:Remove1Agenda-isCost$$Gain1Credits-perOpponentCounter{Credits}
.....
Constellation Protocol
-----
bc0f047c-01b1-427f-a439-d451eda07008
-----

+++++

.....
Mark Yale
-----
bc0f047c-01b1-427f-a439-d451eda07009
-----

+++++
A0B0G0T0:Gain1Credits||A0B0G0T1:Gain2Credits||A0B0G0T0:Remove1Agenda-DemiAutoTargeted-hasMarker{Agenda}-choose1-isCost$$Gain3Credits
.....
Space Camp
-----
bc0f047c-01b1-427f-a439-d451eda07010
-----
onAccess:UseCustomAbility-isOptional-worksInArchives
+++++

.....
The Board
-----
bc0f047c-01b1-427f-a439-d451eda07011
-----
onTrash:ScoreMyself-onOpponent-ifAccessed-ifUnscored-preventTrash-runTrashScriptWhileInactive-explicitTrash$$Gain2Agenda Points-onOpponent-ifAccessed-ifUnscored-explicitTrash$$Put2Scored-isSilent-ifAccessed-ifUnscored-explicitTrash
+++++

.....
Asteroid Belt
-----
bc0f047c-01b1-427f-a439-d451eda07012
-----
onRez:Gain3Credits-perMarker{Advancement}-max3
+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Wormhole
-----
bc0f047c-01b1-427f-a439-d451eda07013
-----
onRez:Gain3Credits-perMarker{Advancement}-max3
+++++
A0B0G0T0:SimplyAnnounce{use the subroutine on another piece of rezzed ICE}-isSubroutine
.....
Nebula
-----
bc0f047c-01b1-427f-a439-d451eda07014
-----
onRez:Gain3Credits-perMarker{Advancement}-max3
+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine
.....
Orion
-----
bc0f047c-01b1-427f-a439-d451eda07015
-----
onRez:Gain3Credits-perMarker{Advancement}-max5
+++++
A0B0G0T0:TrashTarget-Targeted-atProgram-isSubroutine||A0B0G0T0:SimplyAnnounce{use the subroutine on another piece of rezzed ICE}-isSubroutine||A0B0G0T0:RunEnd-isSubroutine
.....
Builder
-----
bc0f047c-01b1-427f-a439-d451eda07016
-----

+++++
A1B0G0T0:SimplyAnnounce{move to the outermost position of any server}||A0B0G0T0:Put1Advancement-Targeted-atICE-isSubroutine 
.....
Checkpoint
-----
bc0f047c-01b1-427f-a439-d451eda07017
-----
onRez:Gain1Bad Publicity||atSuccessfulRun:Inflict3MeatDamage-perMarker{Checked}-onOpponent$$Remove999Checked||atJackOut:Remove999Checked
+++++
A0B0G0T0:Trace5-traceEffects<Put1Checked,None>
.....
Fire Wall
-----
bc0f047c-01b1-427f-a439-d451eda07018
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Searchlight
-----
bc0f047c-01b1-427f-a439-d451eda07019
-----

+++++
A0B0G0T0:Trace1-perMarker{Advancement}-traceEffects<Gain1Tags-onOpponent,None>
.....
Housekeeping
-----
bc0f047c-01b1-427f-a439-d451eda07020
-----

+++++
A0B0G0T0:SimplyAnnounce{force the runner to trash a card from their Grip}-onlyOnce
.....
Patch
-----
bc0f047c-01b1-427f-a439-d451eda07021
-----
Placement:ICE-isRezzed
+++++

.....
Traffic Accident
-----
bc0f047c-01b1-427f-a439-d451eda07022
-----
onPlay:Inflict2MeatDamage-onOpponent-ifTagged2	
+++++

.....
Satellite Grid
-----
bc0f047c-01b1-427f-a439-d451eda07023
-----

+++++

.....
The Twins
-----
bc0f047c-01b1-427f-a439-d451eda07024
-----

+++++
A0B0G0T0:TrashTarget-DemiAutoTargeted-atICE-fromHand-choose1$$SimplyAnnounce{force the runner to enounter the same ICE again}
.....
Sub Boost
-----
bc0f047c-01b1-427f-a439-d451eda07025
-----
Placement:ICE-isRezzed||onPlay:Put1Keyword:Barrier-Targeted-onHost-isSilent
+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Dedicated Technician Team
-----
bc0f047c-01b1-427f-a439-d451eda07026
-----
atTurnPreStart:Refill2Credits-duringMyTurn
+++++
A0B0G0T0:Remove1Credits
.....
Cyberdex Virus Suite
-----
bc0f047c-01b1-427f-a439-d451eda07027
-----
onAccess:UseCustomAbility-isOptional-worksInArchives
+++++
A0B0G0T1:UseCustomAbility
.....
Edward Kim
-----
bc0f047c-01b1-427f-a439-d451eda07028
-----

+++++
A0B0G0T2:SimplyAnnounce{trash an accessed operation}
.....
MaxX
-----
bc0f047c-01b1-427f-a439-d451eda07029
-----
atTurnStart:Draw2Cards-toTrash-duringMyTurn$$Draw1Card
+++++

.....
Valencia Estevez
-----
bc0f047c-01b1-427f-a439-d451eda07030
-----
onStartup:SetTo1Bad Publicity-onOpponent
+++++

.....
Amped Up
-----
bc0f047c-01b1-427f-a439-d451eda07031
-----
onPlay:Gain3Clicks$$Inflict1BrainDamage-nonPreventable
+++++

.....
I've Had Worse
-----
bc0f047c-01b1-427f-a439-d451eda07032
-----
onPlay:Draw3Cards||onMeatDMGDiscard:Draw3Cards||onNetDMGDiscard:Draw3Cards
+++++

.....
Itinerant Protesters
-----
bc0f047c-01b1-427f-a439-d451eda07033
-----

+++++

.....
Showing Off
-----
bc0f047c-01b1-427f-a439-d451eda07034
-----
onPlay:RunR&D||atJackOut:TrashMyself-isSilent
+++++

.....
Wanton Destruction
-----
bc0f047c-01b1-427f-a439-d451eda07035
-----
onPlay:RunHQ||atSuccessfulRun:CustomScript-isAlternativeRunResult-isOptional-ifSuccessfulRunHQ$$TrashMyself-ifSuccessfulRunHQ-isSilent
+++++

.....
Day Job
-----
bc0f047c-01b1-427f-a439-d451eda07036
-----
onPlay:Lose3Clicks-isCost$$Gain10Credits
+++++

.....
Forked
-----
bc0f047c-01b1-427f-a439-d451eda07037
-----
onPlay:RunGeneric
+++++
A0B0G0T0:TrashTarged-Targeted-atICE_and_Sentry-isRezzed
.....
Knifed
-----
bc0f047c-01b1-427f-a439-d451eda07038
-----
onPlay:RunGeneric
+++++
A0B0G0T0:TrashTarged-Targeted-atICE_and_Barrier-isRezzed
.....
Spooned
-----
bc0f047c-01b1-427f-a439-d451eda07039
-----
onPlay:RunGeneric
+++++
A0B0G0T0:TrashTarged-Targeted-atICE_and_Code Gate-isRezzed
.....
Eater
-----
bc0f047c-01b1-427f-a439-d451eda07040
-----
atJackOut:Remove999Fed
+++++
A0B1G0T0:SimplyAnnounce{break ICE subroutine}$$Put1Fed||A0B1G0T0:Put1PlusOne
.....
Gravedigger
-----
bc0f047c-01b1-427f-a439-d451eda07041
-----
whileInstalled:Put1Virus-foreachCardTrashed-byOpponent-typenon{Operation}_and_non{Program}_and_non{Hardware}_and_non{Event}_and_non{Resource}
+++++
A1B0G0T0:Remove1Virus-isCost$$Draw1Card-toTrash-ofOpponent
.....
Hivemind
-----
bc0f047c-01b1-427f-a439-d451eda07042
-----
onInstall:Put1Virus
+++++
A0B0G0T0:Remove1Virus-isCost$$Put1Virus-Targeted-atProgram_and_Virus
.....
Progenitor
-----
bc0f047c-01b1-427f-a439-d451eda07043
-----
onInstall:Put3DaemonMU||whileInstalled:Put1Virus-AutoTargeted-onAttachment-foreachVirusPurged
+++++

.....
Archives Interface
-----
bc0f047c-01b1-427f-a439-d451eda07044
-----

+++++
A0B0G0T0:ExileTarget-DemiAutoTargeted-choose1-fromArchives-targetOpponents
.....
Chop Bot 3000
-----
bc0f047c-01b1-427f-a439-d451eda07045
-----

+++++
A0B0G0T2:TrashTarget-Targeted-targetMine$$Draw1Card||A0B0G0T2:TrashTarget-Targeted-targetMine$$Lose1Tags
.....
MemStrips
-----
bc0f047c-01b1-427f-a439-d451eda07046
-----
whileInPlay:Provide3MU
+++++

.....
Vigil
-----
bc0f047c-01b1-427f-a439-d451eda07047
-----
whileInPlay:Provide1MU||atTurnStart:CustomScript-duringMyTurn
+++++
A0B0G0T0:Draw1Card
.....
Human First
-----
bc0f047c-01b1-427f-a439-d451eda07048
-----
whileInstalled:Gain1Credits-perTriggeringProperty{Stat}-foreachAgendaScored-onTriggerCard||whileInstalled:Gain1Credits-perTargetProperty{Stat}-foreachAgendaLiberated-onTriggerCard
+++++

.....
Investigative Journalism
-----
bc0f047c-01b1-427f-a439-d451eda07049
-----

+++++
A4B0G0T1:Gain1Bad Publicity-onOpponent
.....
Sacrificial Clone
-----
bc0f047c-01b1-427f-a439-d451eda07050
-----
onDamage:TrashMultiple-AutoTargeted-atHardware_or_Resource_and_nonVirtual$$Discard999Cards$$Lose999Credits$$Lose999Tags$$CreateDummy-with100protectionAllDMG-trashCost
+++++
A0B0G0T1:TrashMultiple-AutoTargeted-atHardware_or_Resource_and_nonVirtual$$Discard999Cards$$Lose999Credits$$Lose999Tags$$CreateDummy-with100protectionAllDMG-trashCost
.....
Stim Dealer
-----
bc0f047c-01b1-427f-a439-d451eda07051
-----
atTurnStart:Inflict1BrainDamage-nonPreventable-ifOrigmarkers{Power}ge2-duringMyTurn$$Remove99Power$$Put1Brained||atTurnStart:Put1Power-hasntOrigMarker{Brained}-ifOrigmarkers{Power}le1-duringMyTurn||atTurnStart:Remove99Brained-duringMyTurn
+++++

.....
Virus Breeding Ground
-----
bc0f047c-01b1-427f-a439-d451eda07052
-----
atTurnStart:Put1Virus-duringMyTurn
+++++
A1B0G0T0:Remove1Virus-isCost$$Put1Virus-DemiAutoTargeted-hasMarker{Virus}-choose1
.....
Uninstall
-----
bc0f047c-01b1-427f-a439-d451eda07053
-----
onPlay:UninstallTarget-DemiAutoTargeted-atProgram_or_Hardware-choose1
+++++

.....
Qianju PT # Scripted manually in parseNewCounters()
-----
bc0f047c-01b1-427f-a439-d451eda07054
-----
atTurnPreStart:Remove1Power
+++++
A0B0G0T0:Lose1Clicks-isCost-onlyOnce$$Put1Power
.....
Data Folding
-----
bc0f047c-01b1-427f-a439-d451eda07055
-----
atTurnStart:Gain1Credits-ifIHave2MU-duringMyTurn
+++++

.....
Clot
-----
bc0f047c-01b1-427f-a439-d451eda08001
-----
whileInPlay:TrashMyself-foreachVirusPurged
+++++

.....
Paige Piper
-----
bc0f047c-01b1-427f-a439-d451eda08002
-----

+++++
A0B0G0T0:CustomScript-onlyOnce
.....
Adjusted Chronotype
-----
bc0f047c-01b1-427f-a439-d451eda08003
-----

+++++
A0B0G0T0:Gain1Clicks-onlyOnce
.....
Spike
-----
bc0f047c-01b1-427f-a439-d451eda08004
-----
ConstantAbility:Cloud2Link
+++++
A0B0G0T1:SimplyAnnounce{break up to 3 barrier subroutines}
.....
Enhanced Vision
-----
bc0f047c-01b1-427f-a439-d451eda08005
-----
atSuccessfulRun:CustomScript-onlyOnce
+++++

.....
Gene Conditioning Shoppe
-----
bc0f047c-01b1-427f-a439-d451eda08006
-----

+++++

.....
Synthetic Blood
-----
bc0f047c-01b1-427f-a439-d451eda08007
-----
whileInPlay:Draw1Cards-forEachMeatDMGTaken-onlyOnce||whileInPlay:Draw1Cards-forEachNetDMGTaken-onlyOnce||whileInPlay:Draw1Cards-forEachBrainDMGTaken-onlyOnce
+++++

.....
Traffic Jam
-----
bc0f047c-01b1-427f-a439-d451eda08008
-----
whileInPlay:Increase0Advancement
+++++

.....
Symmetrical Visage
-----
bc0f047c-01b1-427f-a439-d451eda08009
-----
whileInPlay:Gain1Credits-foreachCardDrawnClicked-byMe-onlyOnce
+++++

.....
Brain-Taping Warehouse
-----
bc0f047c-01b1-427f-a439-d451eda08010
-----
whileInPlay:ReduceSCostRez-affectsICE_and_Bioroid
+++++

.....
NEXT Gold
-----
bc0f047c-01b1-427f-a439-d451eda08011
-----

+++++
A0B0G0T0:Inflict1NetDamage-perEveryCard-atNEXT-isICE-isRezzed-isSubroutine||A0B0G0T0:TrashMulti-Targeted-atProgram-isSubtourine
.....
Jinteki Biotech
-----
bc0f047c-01b1-427f-a439-d451eda08012
-----

+++++
A0B0G0T0:CustomScript
.....
Genetic Resequencing
-----
bc0f047c-01b1-427f-a439-d451eda08013
-----
onScore:Put1Agenda-DemiAutoTargeted-isScored-targetMine-choose1
+++++

.....
Cortex Lock
-----
bc0f047c-01b1-427f-a439-d451eda08014
-----

+++++
A0B0G0T0:Inflict1NetDamage-perOpponentCounter{MU}-OpCounter-isSubroutine
.....
Valley Grid
-----
bc0f047c-01b1-427f-a439-d451eda08015
-----

+++++
A0B0G0T0:Put1Valley Grid-AutoTargeted-atIdentity-targetOpponents-isSilent$$SimplyAnnounce{reduce their maximum hand size until the beggining of your next turn}
.....
Bandwidth
-----
bc0f047c-01b1-427f-a439-d451eda08016
-----

+++++
A0B0G0T0:Gain1Tags-onOpponent-isSubroutine$$Put1Bandwidth Logged-AutoTargeted-atIdentity-targetOpponents
.....
Predictive Algorithm
-----
bc0f047c-01b1-427f-a439-d451eda08017
-----

+++++

.....
Capital Investors
-----
bc0f047c-01b1-427f-a439-d451eda08018
-----

+++++
A1B0G0T0:Gain2Credits
.....
Negotiator
-----
bc0f047c-01b1-427f-a439-d451eda08019
-----

+++++
A0B0G0T0:Gain2Credits-isSubroutine||A0B0G0T0:TrashTarget-Targeted-atProgram-isSubrourine
.....
Tech Startup
-----
bc0f047c-01b1-427f-a439-d451eda08020
-----

+++++
A0B0G0T1:Retrieve1Card-grabAsset-toTable$$ShuffleR&D
.....
Hacktivist Meeting
-----
bc0f047c-01b1-427f-a439-d451eda08021
-----
whileInPlay:UseCustomAbility-foreachCardRezzed-typenonICE-byOpponent
+++++

.....
Off-Campus Apartment
-----
bc0f047c-01b1-427f-a439-d451eda08022
-----

+++++
A1B0G0T0:CustomScript
.....
Career Fair
-----
bc0f047c-01b1-427f-a439-d451eda08023
-----
onPlay:InstallTarget-DemiAutoTargeted-atResource-fromHand-choose1-payCost-reduc3
+++++

.....
Dorm Computer
-----
bc0f047c-01b1-427f-a439-d451eda08024
-----
onInstall:Put4Power-isSilent||atJackOut:Remove999preventCounter:Tags
+++++
A1B0G0T0:Remove1Power-isCost$$RunGeneric$$Put100preventCounter:Tags
.....
Hayley Kaplan
-----
bc0f047c-01b1-427f-a439-d451eda08025
-----
whileInPlay:Pass-foreachCardInstall-typeProgram_or_Hardware_or_Resource-byMe-onlyOnce
+++++
A0B0G0T0:InstallTarget-DemiAutoTargeted-atnonEvent-fromHand-choose1-payCost
.....
Game Day
-----
bc0f047c-01b1-427f-a439-d451eda08026
-----
onPlay:Draw999Cards
+++++

.....
Comet
-----
bc0f047c-01b1-427f-a439-d451eda08027
-----
whileInPlay:Pass-foreachCardPlay-typeEvent-byMe-onlyOnce||whileInPlay:Provide1MU
+++++
A0B0G0T0:InstallTarget-DemiAutoTargeted-atEvent-fromHand-choose1-payCost
.....
Study Guide
-----
bc0f047c-01b1-427f-a439-d451eda08028
-----

+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B2G0T0:Put1Power
.....
London Library
-----
bc0f047c-01b1-427f-a439-d451eda08029
-----

+++++
A1B0G0T0:UseCustomAbility
.....
Tyson Observatory
-----
bc0f047c-01b1-427f-a439-d451eda08030
-----

+++++
A2B0G0T0:Retrieve1Cards-grabHardware
.....
Beach Party
-----
bc0f047c-01b1-427f-a439-d451eda08031
-----
atTurnStart:Lose1Clicks-duringMyTurn||whileInPlay:Provide5HandSize-forRunner
+++++

.....
Research Grant
-----
bc0f047c-01b1-427f-a439-d451eda08032
-----
onScore:ScoreTarget-Targeted-atResearch Grant-isMutedTarget
+++++

.....
Turing
-----
bc0f047c-01b1-427f-a439-d451eda08033
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Crick
-----
bc0f047c-01b1-427f-a439-d451eda08034
-----

+++++
A0B0G0T0:Retrieve1Cards-fromArchives-toTable-doNotReveal
.....
Recruiting Trip
-----
bc0f047c-01b1-427f-a439-d451eda08035
-----
onPlay:RequestInt-Msg{How many sysops are you recruiting?}$$Lose1Credits-perX-isCost$$Retrieve1Cards-perX-grabSysop$$ShuffleR&D
+++++

.....
Blacklist
-----
bc0f047c-01b1-427f-a439-d451eda08036
-----

+++++

.....
Gutenberg
-----
bc0f047c-01b1-427f-a439-d451eda08037
-----

+++++
A0B0G0T0:Trace7-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
Student Loans
-----
bc0f047c-01b1-427f-a439-d451eda08038
-----
whileRezzed:IncreaseSCostPlay-affectsEvent
+++++

.....
Meru Mati
-----
bc0f047c-01b1-427f-a439-d451eda08039
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Breaker Bay Grid
-----
bc0f047c-01b1-427f-a439-d451eda08040
-----

+++++
A0B0G0T0:RezTarget-Targeted-isnotICE-payCost-reduc5
.....
Immolation Script
-----
bc0f047c-01b1-427f-a439-d451eda08041
-----
onPlay:RunArchives||atJackOut:TrashMyself-isSilent
+++++
A0B0G0T0:TrashTarget-Targeted-atICE-isRezzed
.....
Skulljack
-----
bc0f047c-01b1-427f-a439-d451eda08042
-----
onInstall:Inflict1BrainDamage||whileInPlay:Reduce1CostTrash-affectsAll-forMe
+++++

.....
Turntable
-----
bc0f047c-01b1-427f-a439-d451eda08043
-----
whileInPlay:Provide1MU
+++++
A0B0G0T0:CustomScript
.....
Chrome Parlor
-----
bc0f047c-01b1-427f-a439-d451eda08044
-----

+++++
A0B0G0T0:Put100protectionAllDMG
.....
Titanium Ribs
-----
bc0f047c-01b1-427f-a439-d451eda08045
-----
onInstall:Inflict2MeatDamage
+++++

.....
Crowbar
-----
bc0f047c-01b1-427f-a439-d451eda08046
-----
ConstantAbility:Cloud2Link
+++++
A0B0G0T1:SimplyAnnounce{break up to 3 code gate subroutines}
.....
Net-Ready Eyes
-----
bc0f047c-01b1-427f-a439-d451eda08047
-----
onInstall:Inflict2MeatDamage
+++++
A0B0G0T0:Put1PlusOne-DemiAutoTargeted-atIcebreaker-choose1
.....
Analog Dreamers
-----
bc0f047c-01b1-427f-a439-d451eda08048
-----
atSuccessfulRun:CustomScript-isAlternativeRunResult-isOptional-ifSuccessfulRunR&D-hasOrigMarker{Running}||atJackOut:Remove1Running-isSilent
+++++
A1B0G0T0:RunR&D$$Put1Running
.....
Brain Cage
-----
bc0f047c-01b1-427f-a439-d451eda08049
-----
whileInPlay:Provide3HandSize-forRunner||onInstall:Inflict1BrainDamage
+++++

.....
Cybernetics Division
-----
bc0f047c-01b1-427f-a439-d451eda08050
-----
whileInPlay:Steal1HandSize-forRunner||whileInPlay:Steal1HandSize-forCorp
+++++

.....
Self-Destruct Chips
-----
bc0f047c-01b1-427f-a439-d451eda08051
-----
whileInPlay:Steal1HandSize-forRunner
+++++

.....
Lab Dog
-----
bc0f047c-01b1-427f-a439-d451eda08052
-----

+++++
A0B0G0T1:TrashTarget-DemiAutoTargeted-atHardware-isSubroutine-choose1
.....
Oaktown Grid
-----
bc0f047c-01b1-427f-a439-d451eda08053
-----
whileRezzed:IncreaseXCostTrash-affectsAll-forOpponent-perMarker{Power}||atJackOut:Remove999Power
+++++
A0B0G0T0:Put3Power
.....
Ryon Knight
-----
bc0f047c-01b1-427f-a439-d451eda08054
-----

+++++
A0B0G0T1:Inflict1BrainDamage-onOpponent
.....
Clairvoyant Monitor
-----
bc0f047c-01b1-427f-a439-d451eda08055
-----

+++++
A0B0G0T0:Psi-psiEffects<Put1Advancement-Targeted++RunEnd,None>-isSubroutine
.....
Lockdown
-----
bc0f047c-01b1-427f-a439-d451eda08056
-----
atTurnEnd:Remove999Power
+++++
A0B0G0T0:SimplyAnnounce{prevent the runner from drawing cards for the remainder of this turn}-isSubroutine$$Put1Power-isSilent
.....
Little Engine
-----
bc0f047c-01b1-427f-a439-d451eda08057
-----

+++++
A0B0G0T0:RunEnd-isSubroutine||A0B0G0T0:Gain5Credits-onOpponent-isSubroutine
.....
Oaktown Renovation
-----
bc0f047c-01b1-427f-a439-d451eda08058
-----
onAdvance:Gain2Credits$$Gain1Credits-ifOrigmarkers{Advancement}ge5
+++++

.....
Corporate Town
-----
bc0f047c-01b1-427f-a439-d451eda08059
-----
onRez:ExileTarget-DemiAutoTargeted-targetMine-isScored-choose1||atTurnStart:TrashTarget-Targeted-atResource-duringMyTurn-isMutedTarget
+++++

.....
Quicksand
-----
bc0f047c-01b1-427f-a439-d451eda08060
-----

+++++
A0B0G0T0:Put1Power||A0B0G0T0:RunEnd-isSubroutine
.....
Faust
-----
bc0f047c-01b1-427f-a439-d451eda08061
-----

+++++
A0B0G0T0:TrashTarget-DemiAutoTargeted-fromHand-choose1-isCost$$SimplyAnnounce{Break ICE Subtourine}||A0B0G0T0:TrashTarget-DemiAutoTargeted-fromHand-choose1-isCost$$Put2PlusOne
.....
Street Peddler
-----
bc0f047c-01b1-427f-a439-d451eda08062
-----
onInstall:CustomScript
+++++

.....
Armand "Geist" Walker
-----
bc0f047c-01b1-427f-a439-d451eda08063
-----

+++++
A0B0G0T0:Draw1Card
.....
Drive By
-----
bc0f047c-01b1-427f-a439-d451eda08064
-----
onPlay:ExposeTarget-Targeted-isUnrezzed
+++++
A0B0G0T0:TrashTarget-Targeted-atAsset_or_Upgrade
.....
Forger
-----
bc0f047c-01b1-427f-a439-d451eda08065
-----
whileInstalled:Gain1Base Link
+++++
A0B0G0T1:Lose1Tags
.....
Shiv
-----
bc0f047c-01b1-427f-a439-d451eda08066
-----
ConstantAbility:Cloud2Link
+++++
A0B0G0T1:SimplyAnnounce{Break up to 3 sentry subroutines}
.....
Gang Sign
-----
bc0f047c-01b1-427f-a439-d451eda08067
-----
whileInPlay:CustomScript-foreachAgendaScored
+++++

.....
Muertos Gang Member
-----
bc0f047c-01b1-427f-a439-d451eda08068
-----
onInstall:CustomScript
+++++
A0B0G0T1:Draw1Cards
.....
Chameleon
-----
bc0f047c-01b1-427f-a439-d451eda08069
-----
onInstall:CustomScript||atTurnEnd:UninstallMyself
+++++
A0B1G0T0:SimplyAnnounce{Break subroutine of the named subtype}
.....
Hyperdriver
-----
bc0f047c-01b1-427f-a439-d451eda08070
-----

+++++
A0B0G0T0:ExileMyself$$Gain3Clicks
.....
Test Ground
-----
bc0f047c-01b1-427f-a439-d451eda08071
-----

+++++
A0B0G0T1:DerezMulti-Targeted-isRezzed-TargetMine
.....
Defective Brainchips
-----
bc0f047c-01b1-427f-a439-d451eda08072
-----
whileInPlay:Inflict1BrainDamage-forEachBrainDMGTaken-onlyOnce
+++++

.....
Allele Repression
-----
bc0f047c-01b1-427f-a439-d451eda08073
-----

+++++
A0B0G0T1:CustomScript
.....
Marcus Batty
-----
bc0f047c-01b1-427f-a439-d451eda08074
-----

+++++
A0B0G0T1:Psi-psiEffects<SimplyAnnounce{resolve 1 subroutine on a rezzed ICE protecting this server},None>-isSubroutine
.....
Expose
-----
bc0f047c-01b1-427f-a439-d451eda08075
-----

+++++
A0B0G0T1:Lose1Bad Publicity-perMarker{Advancement}
.....
Pachinko
-----
bc0f047c-01b1-427f-a439-d451eda08076
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Underway Renovation
-----
bc0f047c-01b1-427f-a439-d451eda08077
-----
onAdvance:Draw1Card-toTrash-ofOpponent$$Draw1Card-toTrash-ofOpponent-ifOrigmarkers{Advancement}ge4
+++++

.....
Contract Killer
-----
bc0f047c-01b1-427f-a439-d451eda08078
-----

+++++
A1B0G0T1:Remove2Advancement-isCost$$TrashTarget-DemiAutoTargeted-atConnection-choose1||A1B0G0T1:Remove2Advancement-isCost$$Inflict2MeatDamage-onOpponent
.....
Spiderweb
-----
bc0f047c-01b1-427f-a439-d451eda08079
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Underway Grid
-----
bc0f047c-01b1-427f-a439-d451eda08080
-----

+++++

.....
Trope
-----
bc0f047c-01b1-427f-a439-d451eda08081
-----
atTurnStart:Put1Power-duringMyTurn
+++++
A1B0G0T0:TrashMulti-AutoTargeted-atEvent_and_nonCurrent-hasntMarker{Scored}$$Retrieve1Card-fromHeap-toDeck-perMarker{Power}$$ShuffleStack$$ExileMyself
.....
Spoilers
-----
bc0f047c-01b1-427f-a439-d451eda08082
-----
whileInPlay:Draw1Card-toTrash-ofOpponent-foreachAgendaScored
+++++

.....
Drug Dealer
-----
bc0f047c-01b1-427f-a439-d451eda08083
-----
atTurnStart:Lose1Credits-duringMyTurn||atTurnStart:CustomScript-duringOpponentTurn
+++++

.....
Rolodex
-----
bc0f047c-01b1-427f-a439-d451eda08084
-----
onInstall:CustomScript||onTrash:Draw3Cards-toTrash
+++++

.....
Fan Site
-----
bc0f047c-01b1-427f-a439-d451eda08085
-----
whileInPlay:ScoreMyself-foreachAgendaScored-hasntMarker{Scored}||whileInPlay:Put1ScorePenalty-isSilent-foreachAgendaScored-hasntMarker{Scored}||whileInPlay:Put1Scored-isSilent-isSilent-foreachAgendaScored-hasntMarker{Scored}
+++++

.....
Film Critic
-----
bc0f047c-01b1-427f-a439-d451eda08086
-----

+++++
A2B0G0T0:CustomScript
.....
Paparazzi
-----
bc0f047c-01b1-427f-a439-d451eda08087
-----
onInstall:Put101protectionMeatDMG
+++++

.....
Ronald Five
-----
bc0f047c-01b1-427f-a439-d451eda08088
-----
whileInPlay:Lose1Clicks-ofOpponent-foreachCardTrashed-byOpponent-typenon{Program}_and_non{Hardware}_and_non{Event}_and_non{Resource}||whileInPlay:Lose1Clicks-ofOpponent-foreachOutofPlayTrashed-byOpponent-typenon{Program}_and_non{Hardware}_and_non{Event}_and_non{Resource}
+++++
A0B0G0T0:Lose1Clicks-onOpponent
.....
Enforcer 1.0
-----
bc0f047c-01b1-427f-a439-d451eda08089
-----
onRez:ExileTarget-Targeted-isScored
+++++
A0B0G0T0:TrashTarget-DemiAutoTargeted-atProgram-choose1-isSubroutine||A0B0G0T0:Inflict1BrainDamage-onOpponent-isSubroutine||A0B0G0T0:TrashTarget-DemiAutoTargeted-atConsole-choose1-isSubroutine||A0B0G0T0:TrashMulti-AutoTargeted-atResource_and_Virtual-isSubroutine
.....
It's a Trap!
-----
bc0f047c-01b1-427f-a439-d451eda08090
-----
onExpose:Inflict2NetDamage-onOpponent
+++++
A0B0G0T0:SimplyAnnounce{force the runner to trash one of their cards}-isSubroutine
.....
An Offer You Can't Refuse
-----
bc0f047c-01b1-427f-a439-d451eda08091
-----
onPlay:CustomScript
+++++

.....
Haarpsichord Studios
-----
bc0f047c-01b1-427f-a439-d451eda08092
-----

+++++

.....
Award Bait
-----
bc0f047c-01b1-427f-a439-d451eda08093
-----
onAccess:UseCustomAbility-isOptional-worksInArchives
+++++

.....
Explode-a-palooza
-----
bc0f047c-01b1-427f-a439-d451eda08094
-----
onAccess:Gain5Credits-isOptional-worksInArchives
+++++

.....
Early Premiere
-----
bc0f047c-01b1-427f-a439-d451eda08095
-----

+++++
A0B1G0T0:Put1Advancement-Targeted
.....
Casting Call
-----
bc0f047c-01b1-427f-a439-d451eda08096
-----
onPlay:UseCustomAbility-DemiAutoTargeted-atAgenda-fromHand-choose1||onHostAccess:Gain2Tags-onOpponent
+++++

.....
Old Hollywood Grid
-----
bc0f047c-01b1-427f-a439-d451eda08097
-----

+++++

.....
Hollywood Renovation
-----
bc0f047c-01b1-427f-a439-d451eda08098
-----
onAdvance:Put1Advancement-Targeted$$Put1Advancement-Targeted-ifOrigmarkers{Advancement}ge6
+++++

.....
Back Channels
-----
bc0f047c-01b1-427f-a439-d451eda08099
-----
onPlay:Gain3Credits-perTargetMarker{Advancement}-Targeted-atnonICE$$TrashTarget-Targeted-atnonICE
+++++

.....
Vanity Project
-----
bc0f047c-01b1-427f-a439-d451eda08100
-----

+++++

.....
Power to the People
-----
bc0f047c-01b1-427f-a439-d451eda08101
-----
onPlay:CreateDummy
+++++
A0B0G0T1:Gain7Credits-onlyforDummy
.....
Surfer
-----
bc0f047c-01b1-427f-a439-d451eda08102
-----

+++++
A0B2G0T0:SimplyAnnounce{swap the Barrier ICE being encountered with another ICE before or after it}
.....
DDoS
-----
bc0f047c-01b1-427f-a439-d451eda08103
-----

+++++
A0B0G0T1:SimplyAnnounce{prevent the rez of the outermost ICE in all servers}
.....
Laramy Fisk
-----
bc0f047c-01b1-427f-a439-d451eda08104
-----
atSuccessfulRun:Draw1Card-onOpponent-ifSuccessfulRunHQ-onlyOnce-isOptional||atSuccessfulRun:Draw1Card-onOpponent-ifSuccessfulRunR&D-onlyOnce-isOptional||atSuccessfulRun:Draw1Card-onOpponent-ifSuccessfulRunArchives-onlyOnce-isOptional
+++++

.....
Fisk Investment Seminar
-----
bc0f047c-01b1-427f-a439-d451eda08105
-----
onPlay:Draw3Cards$$Draw3Cards-onOpponent
+++++

.....
Bookmark
-----
bc0f047c-01b1-427f-a439-d451eda08106
-----

+++++
A1B0G0T0:CustomScript
.....
DaVinci
-----
bc0f047c-01b1-427f-a439-d451eda08107
-----
atSuccessfulRun:Put1Power
+++++
A0B0G0T1:CustomScript
.....
Wireless Net Pavilion
-----
bc0f047c-01b1-427f-a439-d451eda08108
-----

+++++

.....
Cybernetics Court
-----
bc0f047c-01b1-427f-a439-d451eda08109
-----
whileInPlay:Provide4HandSize-forCorp
+++++

.....
Team Sponsorship
-----
bc0f047c-01b1-427f-a439-d451eda08110
-----
whileInPlay:CustomScript-isOptional-foreachAgendaScored
+++++

.....
Chronos Protocol
-----
bc0f047c-01b1-427f-a439-d451eda08111
-----

+++++

.....
Ancestral Imager
-----
bc0f047c-01b1-427f-a439-d451eda08112
-----

+++++
A0B0G0T0:Inflict1NetDamage-onOpponent
.....
Genetics Pavilion
-----
bc0f047c-01b1-427f-a439-d451eda08113
-----

+++++

.....
Franchise City
-----
bc0f047c-01b1-427f-a439-d451eda08114
-----

+++++
A0B0G0T0:Gain1Agenda Points$$ScoreMyself$$Put1Scored-isSilent
.....
Product Placement
-----
bc0f047c-01b1-427f-a439-d451eda08115
-----
onAccess:Gain2Credits
+++++

.....
Worlds Plaza
-----
bc0f047c-01b1-427f-a439-d451eda08116
-----

+++++
A0B0G0T0:CustomScript
.....
Public Support
-----
bc0f047c-01b1-427f-a439-d451eda08117
-----
onRez:Put3Power||atTurnStart:Remove1Power-duringMyTurn||atTurnStart:Gain1Agenda Points-hasntOrigMarker{Power}-ifOrigmarkers{Scored}eq0-duringMyTurn$$ScoreMyself$$Put1Scored-isSilent
+++++

.....
Tour Guide
-----
bc0f047c-01b1-427f-a439-d451eda08118
-----

+++++
A0B0G0T0:RunEnd-isSubroutine
.....
Expo Grid
-----
bc0f047c-01b1-427f-a439-d451eda08119
-----

+++++
A0B0G0T0:Gain1Credits-onlyOnce
.....
The Future is Now
-----
bc0f047c-01b1-427f-a439-d451eda08120
-----
onScore:Retrieve1Cards-doNotReveal$$ShuffleR&D
+++++

.....
SYNC
-----
bc0f047c-01b1-427f-a439-d451eda09001
-----
whileInPlay:Increase1CostDeltag-affectsAll-ifAlterDefault||whileInPlay:Reduce2CostTrash-affectsResource-ifAlterFlipped
+++++
A0B0G0T0:CustomScript
.....
New Angeles Sol
-----
bc0f047c-01b1-427f-a439-d451eda09002
-----

+++++
A0B0G0T0:InstallTarget-DemiAutoTargeted-atCurrent_and_Operation-fromHand-choose1-payCost||A0B0G0T0:Retrieve1Cards-fromArchives-grabCurrent_and_Operation-toTable-payCost
.....
Spark Agency
-----
bc0f047c-01b1-427f-a439-d451eda09003
-----
whileInPlay:Lose1Credits-onOpponent-foreachCardRezzed-typeAdvertisement-onlyOnce
+++++

.....
15 Minutes
-----
bc0f047c-01b1-427f-a439-d451eda09004
-----

+++++
A1B0G0T0:ReworkMyself$$ShuffleR&D
.....
Improved Tracers
-----
bc0f047c-01b1-427f-a439-d451eda09005
-----

+++++

.....
Rebranding Team
-----
bc0f047c-01b1-427f-a439-d451eda09006
-----

+++++

.....
Quantum Predictive Model
-----
bc0f047c-01b1-427f-a439-d451eda09007
-----
onAccess:ScoreMyself-ifTagged1-worksInArchives
+++++

.....
Lily Lockwell
-----
bc0f047c-01b1-427f-a439-d451eda09008
-----
onRez:Draw3Cards
+++++
A1B0G0T0:Lose1Tags-onOpponent-isCost$$UseCustomAbility
.....
News Team
-----
bc0f047c-01b1-427f-a439-d451eda09009
-----
onAccess:UseCustomAbility-worksInArchives
+++++

.....
Shannon Claire
-----
bc0f047c-01b1-427f-a439-d451eda09010
-----

+++++
A1B0G0T0:UseCustomAbility-isFirstCustom||A0B0G0T1:UseCustomAbility-isSecondCustom||A0B0G0T1:UseCustomAbility-isThirdCustom
.....
Victoria Jenkins
-----
bc0f047c-01b1-427f-a439-d451eda09011
-----
onRez:Lose1Clicks-onOpponent-duringOpponentTurn$$Lose1Max Click-onOpponent||onTrash:Gain1Clicks-onOpponent-duringOpponentTurn-isSilent-ifActive-ifUnscored$$Gain1Max Click-onOpponent-isSilent-ifActive-ifUnscored$$ScoreMyself-onOpponent-ifAccessed-ifUnscored-preventTrash-runTrashScriptWhileInactive-explicitTrash$$Gain2Agenda Points-onOpponent-ifAccessed-ifUnscored-explicitTrash$$Put2Scored-isSilent-ifAccessed-ifUnscored-explicitTrash
+++++

.....
Reality Threedee
-----
bc0f047c-01b1-427f-a439-d451eda09012
-----
onRez:Gain1Bad Publicity||atTurnStart:Gain1Credits-duringMyTurn-ifTagged0||atTurnStart:Gain2Credits-duringMyTurn-ifTagged1
+++++

.....
Archangel
-----
bc0f047c-01b1-427f-a439-d451eda09013
-----
onAccess:Lose3Credits-isCost-isOptional$$Trace6-isSubroutine-traceEffects<UseCustomAbility,None>
+++++
A0B0G0T0:Trace6-isSubroutine-traceEffects<UseCustomAbility,None>
.....
News Hound
-----
bc0f047c-01b1-427f-a439-d451eda09014
-----

+++++
A0B0G0T0:Trace3-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>||A0B0G0T0:RunEnd
.....
Resistor
-----
bc0f047c-01b1-427f-a439-d451eda09015
-----

+++++
A0B0G0T0:Trace4-isSubroutine-traceEffects<RunEnd,None>
.....
Special Offer
-----
bc0f047c-01b1-427f-a439-d451eda09016
-----

+++++
A0B0G0T0:Gain5Credits-isSubroutine$$TrashMyself
.....
TL;DR
-----
bc0f047c-01b1-427f-a439-d451eda09017
-----

+++++
A0B0G0T0:SimplyAnnounce{duplicate the subs on the next piece of ICE}-isSubroutine
.....
Turnpike
-----
bc0f047c-01b1-427f-a439-d451eda09018
-----

+++++
A0B0G0T0:Lose1Credits-onOpponent||A0B0G0T0:Trace5-isSubroutine-traceEffects<Gain1Tags-onOpponent,None>
.....
24/7 News Cycle
-----
bc0f047c-01b1-427f-a439-d451eda09019
-----
onPlay:ExileTarget-Targeted-atAgenda-targetMine-isCost$$UseCustomAbility
+++++

.....
Ad Blitz
-----
bc0f047c-01b1-427f-a439-d451eda09020
-----
onPlay:RequestInt-Msg{How many Advertisements do you want to install and rez?}$$Lose1Credits-perX-isCost$$UseCustomAbility
+++++

.....
Media Blitz
-----
bc0f047c-01b1-427f-a439-d451eda09021
-----
onPlay:CustomScript
+++++

.....
The All-Seeing I
-----
bc0f047c-01b1-427f-a439-d451eda09022
-----
onPlay:CustomScript-ifTagged1
+++++

.....
Surveillance Sweep
-----
bc0f047c-01b1-427f-a439-d451eda09023
-----

+++++

.....
Keegan Lane
-----
bc0f047c-01b1-427f-a439-d451eda09024
-----

+++++
A0B0G0T1:Lose1Tags-onOpponent-isCost$$TrashTarget-DemiAutoTargeted-atProgram-choose1
.....
Rutherford Grid
-----
bc0f047c-01b1-427f-a439-d451eda09025
-----

+++++

.....
Global Food Initiative
-----
bc0f047c-01b1-427f-a439-d451eda09026
-----
onLiberation:Lose1Agenda Points-onOpponent
+++++

.....
Launch Campaign
-----
bc0f047c-01b1-427f-a439-d451eda09027
-----
onRez:Put6Credits||atTurnStart:Transfer2Credits-duringMyTurn$$TrashMyself-ifEmpty
+++++

.....
Assassin
-----
bc0f047c-01b1-427f-a439-d451eda09028
-----

+++++
A0B0G0T0:Trace5-traceEffects<Inflict3NetDamage-onOpponent,None>-isSubroutine||A0B0G0T0:Trace4-traceEffects<TrashTarget-DemiAutoTargeted-atProgram-choose1,None>-isSubroutine
.....
Apex
-----
bc0f047c-01b1-427f-a439-d451eda09029
-----

+++++
A0B0G0T0:CustomScript
.....
Apocalypse
-----
bc0f047c-01b1-427f-a439-d451eda09030
-----
onPlay:TrashMulti-AutoTargeted-atICE_or_Upgrade_or_Asset_or_Agenda-isUnscored$$ApexFlipMulti-AutoTargeted-atProgram_or_Resource_or_Hardware-isSilent
+++++

.....
Prey
-----
bc0f047c-01b1-427f-a439-d451eda09031
-----
onPlay:RunGeneric
+++++
A0B0G0T0:TrashMulti-Targeted-targetMine$$TrashTarget-Targeted-atICE-isRezzed
.....
Heartbeat
-----
bc0f047c-01b1-427f-a439-d451eda09032
-----
whileInPlay:Provide1MU||onDamage:TrashTarget-DemiAutoTargeted-targetMine-isCost-choose1$$Put1protectionAllDMG
+++++
A0B0G0T0:TrashTarget-DemiAutoTargeted-targetMine-isCost-choose1$$Put1protectionAllDMG
.....
Endless Hunger
-----
bc0f047c-01b1-427f-a439-d451eda09033
-----

+++++
A0B0G0T0:TrashTarget-DemiAutoTargeted-targetMine-isCost$$SimplyAnnounce{break one End The Run subroutine}
.....
Harbinger
-----
bc0f047c-01b1-427f-a439-d451eda09034
-----
onTrash:ApexFlipMyself-preventTrash
+++++

.....
Hunting Grounds
-----
bc0f047c-01b1-427f-a439-d451eda09035
-----

+++++
A0B0G0T0:SimplyAnnounce{prevent one When Encountered ability}-onlyOnce||A0B0G0T1:UseCustomAbility
.....
Wasteland
-----
bc0f047c-01b1-427f-a439-d451eda09036
-----
whileInPlay:Gain1Credits-foreachCardTrashed-typeProgram_or_Hardware_or_Resource_or_Event-byMe-onlyOnce
+++++
A0B0G0T0:Gain1Credits-onlyOnce
.....
Adam
-----
bc0f047c-01b1-427f-a439-d451eda09037
-----

+++++

.....
Independent Thinking
-----
bc0f047c-01b1-427f-a439-d451eda09038
-----
onPlay:CustomScript
+++++

.....
Brain Chip
-----
bc0f047c-01b1-427f-a439-d451eda09039
-----
whileInPlay:ProvideSpecialHandSize-forRunner||whileInPlay:SetToSpecialMU
+++++

.....
Multithreader
-----
bc0f047c-01b1-427f-a439-d451eda09040
-----
onInstall:Put2Credits-isSilent||whileInstalled:Reduce#CostUse-affectsProgram-forMe||atTurnPreStart:Refill2Credits-duringMyTurn
+++++

.....
Always Be Running
-----
bc0f047c-01b1-427f-a439-d451eda09041
-----

+++++
A0B0G0T0:Lose2Clicks-isCost$$SimplyAnnounce{break ICE subroutine}-onlyOnce
.....
Dr. Lovegood
-----
bc0f047c-01b1-427f-a439-d451eda09042
-----

+++++
A0B0G0T0:Put1Feelgood-DemiAutoTargeted-targetMine-atProgram_or_Hardware_or_Resource-choose1-onlyOnce
.....
Neutralize All Threats
-----
bc0f047c-01b1-427f-a439-d451eda09043
-----

+++++

.....
Safety First
-----
bc0f047c-01b1-427f-a439-d451eda09044
-----
whileInPlay:Steal2HandSize-forRunner||atTurnEnd:CustomScript-duringMyTurn
+++++

.....
Sunny Lebeau
-----
bc0f047c-01b1-427f-a439-d451eda09045
-----

+++++

.....
Security Chip
-----
bc0f047c-01b1-427f-a439-d451eda09046
-----

+++++
A0B0G0T1:Put1PlusOne-Targeted-atIcebreaker-perMyCounter{Base Link}
.....
Security Nexus
-----
bc0f047c-01b1-427f-a439-d451eda09047
-----
whileInPlay:Provide1MU||whileInstalled:Gain1Base Link
+++++
A0B0G0T0:CustomScript
.....
GS Striker M1
-----
bc0f047c-01b1-427f-a439-d451eda09048
-----
ConstantAbility:Cloud2Link
+++++
A0B2G0T0:SimplyAnnounce{break any number of code gate subroutines}||A0B2G0T0:Put3PlusOne
.....
GS Shrike M2
-----
bc0f047c-01b1-427f-a439-d451eda09049
-----
ConstantAbility:Cloud2Link
+++++
A0B2G0T0:SimplyAnnounce{break any number of sentry subroutines}||A0B2G0T0:Put3PlusOne
.....
GS Sherman M3
-----
bc0f047c-01b1-427f-a439-d451eda09050
-----
ConstantAbility:Cloud2Link
+++++
A0B2G0T0:SimplyAnnounce{break any number of barrier subroutines}||A0B2G0T0:Put3PlusOne
.....
Globalsec Security Clearance
-----
bc0f047c-01b1-427f-a439-d451eda09051
-----

+++++
A1B0G0T0:CustomScript
.....
Jak Sinclair
-----
bc0f047c-01b1-427f-a439-d451eda09052
-----
onPay:Reduce1CostAll-perMyCounter{Base Link}
+++++
A0B0G0T0:RunGeneric-onlyOnce
.....
Employee Strike
-----
bc0f047c-01b1-427f-a439-d451eda09053
-----

+++++

.....
Windfall
-----
bc0f047c-01b1-427f-a439-d451eda09054
-----
onPlay:CustomScript
+++++

.....
Technical Writer
-----
bc0f047c-01b1-427f-a439-d451eda09055
-----
whileInPlay:Put1Credit-foreachCardInstall-typeProgram_or_Hardware
+++++
A1B0G0T1:Transfer999Credits
.....
Run Amok
-----
bc0f047c-01b1-427f-a439-d451eda10001
-----
onPlay:RunGeneric
+++++
A0B0G0T1:TrashTarget-Targeted-atICE
.....
Ramujan-reliant 550 BMI
-----
bc0f047c-01b1-427f-a439-d451eda10002
-----
onDamage:Put1protectionNetBrainDMG-trashCost-excludeDummy-perEveryCard-atRamujan-reliant 550 BMI$$TrashMyself-isSilent
+++++
A0B0G0T1:CreateDummy-with1protectionNetBrainDMG-perEveryCard-atRamujan-reliant 550 BMI
.....
Street Magic
-----
bc0f047c-01b1-427f-a439-d451eda10003
-----

+++++

.....
High-stakes Job
-----
bc0f047c-01b1-427f-a439-d451eda10004
-----
onPlay:RunGeneric||atSuccessfulRun:Gain12Credits||atJackOut:TrashMyself-isSilent
+++++

.....
Mongoose
-----
bc0f047c-01b1-427f-a439-d451eda10005
-----

+++++
A0B1G0T0:SimplyAnnounce{break up to 2 sentry subroutines}||A0B2G0T0:Put2PlusOne
.....
Jesminder Sareen
-----
bc0f047c-01b1-427f-a439-d451eda10006
-----

+++++
A0B0G0T0:Lose1Tags-onlyOnce
.....
Maya
-----
bc0f047c-01b1-427f-a439-d451eda10007
-----
whileInPlay:Provide2MU
+++++

.....
Panchatantra
-----
bc0f047c-01b1-427f-a439-d451eda10008
-----

+++++
A0B0G0T2:SimplyAnnounce{Give the encountered ICE a new subtype}
.....
Artist Colony
-----
bc0f047c-01b1-427f-a439-d451eda10009
-----

+++++
A0B0G0T0:ExileTarget-Targeted-isScored-isCost$$Retrieve1Cards-grabnonEvent-toTable-payCost
.....
Chatterjee University
-----
bc0f047c-01b1-427f-a439-d451eda10010
-----

+++++
A1B0G0T0:Put1Power||A1B0G0T0:UseCustomAbility$$Remove1Power
.....
Advanced Concept Hopper
-----
bc0f047c-01b1-427f-a439-d451eda10011
-----
atRunStart:CustomScript
+++++

.....
Vikram 1.0
-----
bc0f047c-01b1-427f-a439-d451eda10012
-----

+++++
A0B0G0T0:SimplyAnnounce{prevent the runner from using any programs for the remainder of this run}-isSubroutine||A0B0G0T0:Trace4-isSubroutine-traceEffects<Inflict1BrainDamage-onOpponent,None>
.....
Heritage Committee
-----
bc0f047c-01b1-427f-a439-d451eda10013
-----
onPlay:Draw3Cards$$ReworkTarget-DemiAutoTargeted-choose1-fromHand
+++++

.....
Mumbad City Grid
-----
bc0f047c-01b1-427f-a439-d451eda10014
-----

+++++
A0B0G0T0:SimplyAnnounce{swap the passed ICE with another piece of ice on this server}
.....
Kala Ghoda Real TV
-----
bc0f047c-01b1-427f-a439-d451eda10015
-----
atTurnStart:CustomScript-duringMyTurn
+++++
A0B0G0T1:Draw1Card-toTrash-ofOpponent
.....
Interrupt 0
-----
bc0f047c-01b1-427f-a439-d451eda10016
-----
atJackOut:Remove999Interrupt
+++++
A0B0G0T0:Put1Interrupt-isSilent$$SimplyAnnounce{force the runner to pay 1 credit as an additional cost each time they use an icebreaker to break at least 1 subroutine}
.....
Dedication Ceremony
-----
bc0f047c-01b1-427f-a439-d451eda10017
-----
onPlay:Put3Advancement-DemiAutoTargeted-atICE_or_Asset_or_Upgrade-isRezzed-choose1
+++++

.....
Mumba Temple
-----
bc0f047c-01b1-427f-a439-d451eda10018
-----
onRez:Put2Credits||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostRez-affectsAll-forMe
+++++

.....
Museum of History
-----
bc0f047c-01b1-427f-a439-d451eda10019
-----
atTurnStart:Retrieve1Card-fromArchives-toDeck-doNotReveal-duringMyTurn-isOptional$$ShuffleR&D
+++++

.....
ENDSCRIPTS
=====
'''
