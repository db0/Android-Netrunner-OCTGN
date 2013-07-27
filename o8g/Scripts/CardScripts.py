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
whileRezzed:Gain1Base Link
+++++
	
.....
Account Siphon
-----
bc0f047c-01b1-427f-a439-d451eda01018
-----
onPlay:RunHQ||atSuccessfulRun:Lose5Credits-ofOpponent-isOptional-isAlternativeRunResult$$Gain2Credits-perX$$Gain2Tags$$TrashMyself-ifSuccessfulRunHQ-isSilent
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
onAccess:Reveal-ifInstalled
+++++
A0B2G0T0:TrashMulti-Targeted-atProgram-onAccess
.....
Akamatsu Mem Chip
-----
bc0f047c-01b1-427f-a439-d451eda01038
-----
whileRezzed:Gain1MU
+++++

.....
Akitaro Watanabe
-----
bc0f047c-01b1-427f-a439-d451eda01079
-----

+++++
	
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
onInstall:Put2Credits||whileRezzed:Reduce#CostDeltag-forAll-excludeDummy-forMe||atTurnPreStart:Refill2Credits-excludeDummy-duringMyTurn||onDamage:Put3protectionMeatDMG-trashCost-excludeDummy
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
onInstall:Put1Credits-isSilent||whileRezzed:Reduce#CostUse-forIcebreaker-forMe||whileRezzed:Reduce#CostInstall-forVirus-forMe||atTurnPreStart:Refill1Credits-duringMyTurn
+++++
	
.....
Data Dealer
-----
bc0f047c-01b1-427f-a439-d451eda01031
-----

+++++
A1B0G0T0:ExileTarget-Targeted-isScored-targetMine$$Gain9Credits	
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
whileRezzed:Gain1MU||atSuccessfulRun:Gain1Credits
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
A0B0G0T0:PossessTarget-Targeted-atProgram_and_nonIcebreaker-targetMine||A1B1G0T0:Retrieve1Card-typeVirus$$ShuffleStack
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
onAccess:Reveal-ifInstalled
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
whileRezzed:Gain2MU||whileRezzed:Put1Virus-foreachCardInstall-onTriggerCard-typeVirus
+++++
A0B0G0T0:Put1Virus-Targeted-atProgram_and_Virus
.....
Haas-Bioroid
-----
bc0f047c-01b1-427f-a439-d451eda01054
-----
whileRezzed:Gain1Credits-perCardInstall-byMe-onlyOnce
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
whileRezzed:Inflict1NetDamage-onOpponent-foreachAgendaScored||whileRezzed:Inflict1NetDamage-onOpponent-foreachAgendaLiberated
+++++
	
.....
Kate "Mac" McCaffrey
-----
bc0f047c-01b1-427f-a439-d451eda01033
-----
whileRezzed:Reduce1CostInstall-forHardware-onlyOnce-forMe||whileRezzed:Reduce1CostInstall-forProgram-onlyOnce-forMe||whileRezzed:Pass-foreachCardInstall-typeProgram_or_Hardware-byMe-onlyOnce
+++++
	
.....
Lemuria Codecracker
-----
bc0f047c-01b1-427f-a439-d451eda01023
-----

+++++
A1B1G0T0:ExposeTarget-Targeted	
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
onPlay:Put3Credits$$Put1Click-isPriority||whileRezzed:Reduce#CostInstall-forHardware-onlyOnce-forMe||whileRezzed:Reduce#CostInstall-forProgram-onlyOnce-forMe||whileRezzed:Transfer1Click-foreachCardInstall
+++++
	
.....
NBN
-----
bc0f047c-01b1-427f-a439-d451eda01080
-----
atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostTrace-forAll-forMe
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
whileRezzed:Draw1Card-toTrash-ofOpponent-foreachCardInstall-typeVirus-byMe
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
onAccess:Reveal-ifInstalled
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
whileRezzed:Gain1Base Link||onInstall:CustomScript
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
whileRezzed:Gain2Hand Size
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
onPlay:Put3Click||whileRezzed:Transfer1Click-foreachCardInstall
+++++
	
.....
Snare!
-----
bc0f047c-01b1-427f-a439-d451eda01070
-----
onAccess:Reveal
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
onPlay:Retrieve1Card-typeIcebreaker$$ShuffleStack
+++++
	
.....
Stimhack
-----
bc0f047c-01b1-427f-a439-d451eda01004
-----
onPlay:RunGeneric$$Put9Credits||whileRunning:Reduce#CostAll-forAll-forMe||atJackOut:Inflict1BrainDamage-nonPreventable$$TrashMyself
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
whileRezzed:Gain2MU$$Gain2Base Link||onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostUse-forIcebreaker-forMe
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
whileRezzed:Gain1Credits-foreachCardPlay-typeTransaction-byMe
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
onScore:Put1Agenda-perMarker{Advancement}-ignore3-div2||whileScored:ReduceXCostRez-forICE-perMarker{Agenda}-forMe
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
onInstall:Put4protectionMeatDMG
+++++

.....
Project Atlas
-----
bc0f047c-01b1-427f-a439-d451eda02018
-----
onScore:Put1Agenda-perMarker{Advancement}-ignore3
+++++
A0B0G0T0:Remove1Agenda-isCost$$SimplyAnnounce{Retrieve one card from R&D}
.....
Restructured Datapool
-----
bc0f047c-01b1-427f-a439-d451eda02016
-----

+++++
A1B0G0T0:Trace2e-traceEffects<Gain1Tags-onOpponent,None>
.....
Snowflake
-----
bc0f047c-01b1-427f-a439-d451eda02015
-----

+++++
A0B0G0T0:CustomScript
.....
Spinal Modem
-----
bc0f047c-01b1-427f-a439-d451eda02002
-----
onInstall:Put2Credits-isSilent||whileInstalled:Gain1MU||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostUse-forIcebreaker-forMe||whileRunning:Inflict1BrainDamage-foreachUnavoidedTrace-byMe
+++++

.....
The Helpful AI
-----
bc0f047c-01b1-427f-a439-d451eda02008
-----
whileRezzed:Gain1Base Link
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
atTurnPreStart:Refill3Credits-duringMyTurn||Reduce#CostTrash-forAll-forMe
+++++

.....
Haas-Bioroid
-----
bc0f047c-01b1-427f-a439-d451eda02010
-----
whileRezzed:Put1PlusOnePerm-foreachCardRezzed-onTriggerCard-typeBioroid_and_ICE||whileRezzed:Remove1PlusOnePerm-foreachCardDerezzed-onTriggerCard-typeBioroid_and_ICE
+++++

.....
ZU.13 Key Master
-----
bc0f047c-01b1-427f-a439-d451eda02007
-----
constantAbility:Cloud2Link
+++++
A0B1G0T0:SimplyAnnounce{break code gate subroutine}||A0B1G0T0:Put1PlusOne
.....
Amazon Industrial Zone
-----
bc0f047c-01b1-427f-a439-d451eda02038
-----

+++++

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
onInstall:Put1Credits-isSilent||atTurnPreStart:Refill1Credits-duringMyTurn||whileRezzed:Reduce#CostTrace-forAll-forMe||whileRezzed:Gain1Credits-foreachCardRezzed-typeICE
+++++

.....
Dyson Mem Chip
-----
bc0f047c-01b1-427f-a439-d451eda02028
-----
whileRezzed:Gain1Base Link$$Gain1MU
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
whileRezzed:Increase1CostTrash-forAll-forOpponent-ifInstalled
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
onAccess:Inflict2NetDamage-onOpponent||onLiberation:Lose2Credits-isCost-onOpponent
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
onInstall:Put1Dinosaurus Hosted-isSilent
+++++
A0B0G0T0:PossessTarget-Targeted-atIcebreaker_and_nonAI-targetMine-forceHost$$Put2PlusOnePerm-Targeted-atIcebreaker_and_nonAI-targetMine
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

+++++
A0B0G0T0:ExposeTarget-Targeted-isICE
.....
Public Sympathy
-----
bc0f047c-01b1-427f-a439-d451eda02050
-----
whileRezzed:Gain2Hand Size
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
onPlay:Gain1Credits-perTargetMarker{Advancement}-Targeted-atICE
+++++

.....
Edge of World
-----
bc0f047c-01b1-427f-a439-d451eda02053
-----
onAccess:Reveal-ifInstalled
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
A0B0G0T0:Remove1Agenda-isCost$$SimplyAnnounce{Retrieve one card from their Archives to their HQ}
.....
Test Run
-----
bc0f047c-01b1-427f-a439-d451eda02047
-----
onPlay:Retrieve1Card-typeProgram-toTable-with1Test Run$$ShuffleStack||onPlay:Retrieve1Card-fromHeap-typeProgram-toTable-with1Test Run||atTurnEnd:UninstallTarget-toStack-AutoTargeted-atProgram-hasMarker{Test Run}
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
onStartup:Gain1MU-isSilent
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
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostTrash-forAll-forMe
+++++

.....
Doppelganger
-----
bc0f047c-01b1-427f-a439-d451eda02064
-----
whileRezzed:Gain1MU
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
onInstall:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostInstall-forHardware-forMe
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
onPlay:Gain3Credits$$Draw1Cards
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
onRez:Put2Credits-isSilent||atTurnPreStart:Refill2Credits-duringMyTurn||whileRezzed:Reduce#CostRez-forICE-forMe
+++++

.....
Bullfrog
-----
bc0f047c-01b1-427f-a439-d451eda02073
-----

+++++
A0B0G0T0:CustomScript
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
onRez:Put1Credits-perOpponentCounter{Base Link}||atTurnPreStart:Refill1Credits-perOpponentCounter{Base Link}-duringMyTurn||whileRezzed:Reduce#CostTrace-forAll-forMe
+++++

.....
Weyland Consortium: Because we Build it
-----
bc0f047c-01b1-427f-a439-d451eda02076
-----
atTurnPreStart:Refill1Credits-duringMyTurn||whileRezzed:Reduce#CostAdvancement-forICE-forMe
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
whileRezzed:Increase1CostRez-forAll-isICE-forOpponent
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
atSuccessfulRun:Put1Virus-ifSuccessfulRunHQ||onRez:Put1Credits-perMarker{Virus}||atTurnPreStart:Refill1Credits-perMarker{Virus}-duringMyTurn||whileRunningHQ:Reduce#CostAll-forAll-forMe
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
whileRezzed:UseCustomAbility-foreachCardInstall-onTriggerCard-typeHardware-byMe
+++++

.....
Creeper
-----
bc0f047c-01b1-427f-a439-d451eda02089
-----
constantAbility:Cloud2Link
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
A0B0G0T0:Trace2-isSubroutine-traceEffects<SimplyAnnounce{sniff the runner's stack},None>||A0B0G0T0:UseCustomAbility

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
onPlay:RunArchives||atSuccessfulRun:Retrieve1Card-fromHeap-typeProgram-toTable-isOptional-isAlternativeRunResult$$TrashMyself-ifSuccessfulRunArchives-isSilent
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
onStartup:Gain1Hand Size-isSilent||onMulligan:Gain1Hand Size-isSilent
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
atTurnPreEnd:SetTo1Hand Size-perCounter{Credits}
+++++

.....
Next Design: Guarding the Net
-----
bc0f047c-01b1-427f-a439-d451eda03003
-----

+++++
A0B0G0T0:InstallMulti-Targeted-atICE-fromHand$$Draw999Cards
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
A1B0G0T0:Gain2Clicks
.....
Project Wotan
-----
bc0f047c-01b1-427f-a439-d451eda03006
-----
onScore:Put3Agenda||atJackOut:Remove999Project Wotan ETR-AutoTargeted-atICE-hasMarker{Project Wotan ETR}
+++++
A0B0G0T0:Put1Project Wotan ETR-Targeted-atICE_and_Bioroid-isRezzed
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
whileRezzed:Gain1Power-foreachCardInstall
+++++
A1B0G0T1:Gain2Credits-perMarker{Power}
.....
Cerebral Overwriter
-----
bc0f047c-01b1-427f-a439-d451eda03009
-----
onAccess:Reveal-ifInstalled
+++++
A0B3G0T0:Inflict1BrainDamage-onOpponent-perMarker{Advancement}-onAccess	
.....
Director Haas
-----
bc0f047c-01b1-427f-a439-d451eda03010
-----
onRez:Gain1Clicks$$Gain1Max Click||onTrash:ScoreMyself-forOpponent-ifAccessed-ifUnscored-preventTrash$$Gain2Agenda Points-onOpponent-ifAccessed-ifUnscored$$Lose1Max Click-ifActive-ifUnscored$$Lose1Clicks-ifActive-ifUnscored$$Put2Scored-isSilent-ifAccessed-ifUnscored
+++++

.....
Haas Arcology AI
-----
bc0f047c-01b1-427f-a439-d451eda03011
-----

+++++

.....
Thomas Haas
-----
bc0f047c-01b1-427f-a439-d451eda03012
-----

+++++

.....
Bioroid Efficiency Research
-----
bc0f047c-01b1-427f-a439-d451eda03013
-----

+++++

.....
Successful Demonstration
-----
bc0f047c-01b1-427f-a439-d451eda03014
-----

+++++

.....
Heimdall 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03015
-----

+++++

.....
Howler
-----
bc0f047c-01b1-427f-a439-d451eda03016
-----

+++++

.....
Ichi 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03017
-----

+++++

.....
Minelayer
-----
bc0f047c-01b1-427f-a439-d451eda03018
-----

+++++

.....
Viktor 2.0
-----
bc0f047c-01b1-427f-a439-d451eda03019
-----

+++++

.....
Zed 1.0
-----
bc0f047c-01b1-427f-a439-d451eda03020
-----

+++++

.....
Awakening Center
-----
bc0f047c-01b1-427f-a439-d451eda03021
-----

+++++

.....
Tyr's Hand
-----
bc0f047c-01b1-427f-a439-d451eda03022
-----

+++++

.....
Gila Hands Arcology
-----
bc0f047c-01b1-427f-a439-d451eda03023
-----

+++++

.....
Levy University
-----
bc0f047c-01b1-427f-a439-d451eda03024
-----

+++++

.....
Server Diagnostics
-----
bc0f047c-01b1-427f-a439-d451eda03025
-----

+++++

.....
Bastion
-----
bc0f047c-01b1-427f-a439-d451eda03026
-----

+++++

.....
Datapike
-----
bc0f047c-01b1-427f-a439-d451eda03027
-----

+++++

.....
Rielle "Kit" Peddler: Transhuman
-----
bc0f047c-01b1-427f-a439-d451eda03028
-----

+++++

.....
The Professor: Keeper of Knowledge
-----
bc0f047c-01b1-427f-a439-d451eda03029
-----

+++++

.....
Exile: Streethawk
-----
bc0f047c-01b1-427f-a439-d451eda03030
-----

+++++

.....
Escher
-----
bc0f047c-01b1-427f-a439-d451eda03031
-----

+++++

.....
Exploratory Romp
-----
bc0f047c-01b1-427f-a439-d451eda03032
-----

+++++

.....
Freelance Coding Contract
-----
bc0f047c-01b1-427f-a439-d451eda03033
-----

+++++

.....
Scavenge
-----
bc0f047c-01b1-427f-a439-d451eda03034
-----

+++++

.....
Levy AR Lab Access
-----
bc0f047c-01b1-427f-a439-d451eda03035
-----

+++++

.....
Monolith
-----
bc0f047c-01b1-427f-a439-d451eda03036
-----

+++++

.....
Feedback Filter
-----
bc0f047c-01b1-427f-a439-d451eda03037
-----

+++++

.....
Clone Chip
-----
bc0f047c-01b1-427f-a439-d451eda03038
-----

+++++

.....
Omni-drive
-----
bc0f047c-01b1-427f-a439-d451eda03039
-----

+++++

.....
Atman
-----
bc0f047c-01b1-427f-a439-d451eda03040
-----

+++++

.....
Cloak
-----
bc0f047c-01b1-427f-a439-d451eda03041
-----

+++++

.....
Dagger
-----
bc0f047c-01b1-427f-a439-d451eda03042
-----

+++++

.....
Chakana
-----
bc0f047c-01b1-427f-a439-d451eda03043
-----

+++++

.....
Cyber-Cypher
-----
bc0f047c-01b1-427f-a439-d451eda03044
-----

+++++

.....
Paricia
-----
bc0f047c-01b1-427f-a439-d451eda03045
-----

+++++

.....
Self-modifying Code
-----
bc0f047c-01b1-427f-a439-d451eda03046
-----

+++++

.....
Sahasrara
-----
bc0f047c-01b1-427f-a439-d451eda03047
-----

+++++

.....
Inti
-----
bc0f047c-01b1-427f-a439-d451eda03048
-----

+++++

.....
Professional Contacts
-----
bc0f047c-01b1-427f-a439-d451eda03049
-----

+++++

.....
Borrowed Satellite
-----
bc0f047c-01b1-427f-a439-d451eda03050
-----

+++++

.....
Ice Analyzer
-----
bc0f047c-01b1-427f-a439-d451eda03051
-----

+++++

.....
Dirty Laundry
-----
bc0f047c-01b1-427f-a439-d451eda03052
-----

+++++

.....
Daily Casts
-----
bc0f047c-01b1-427f-a439-d451eda03053
-----

+++++

.....
Same Old Thing
-----
bc0f047c-01b1-427f-a439-d451eda03054
-----

+++++

.....
The Source
-----
bc0f047c-01b1-427f-a439-d451eda03055
-----

+++++

.....

ENDSCRIPTS
=====
'''