###==================================================File Contents==================================================###
# This file contains global variables in ANR. They should not be modified by the scripts at all.
###=================================================================================================================###

import re
#---------------------------------------------------------------------------
# These are constant global variables in ANR: They should not be modified by the scripts at all.
#---------------------------------------------------------------------------

mdict = dict( # A dictionary which holds all the hard coded markers (in the markers file)
             BadPublicity =            ("Bad Publicity", "7ae6b4f2-afee-423a-bc18-70a236b41292"),
             Agenda =                  ("Agenda", "38c5b2a0-caa2-40e4-b5b2-0f1cc7202782"), # We use the blue counter as agendas
             Power =                   ("Power", "815b944d-d7db-4846-8be2-20852a1c9530"),
             Virus =                   ("Virus", "7cbe3738-5c50-4a32-97e7-8cb43bf51afa"),
             Click =                   ("Click", "1c873bd4-007f-46f9-9b17-3d8780dabfc4"),
             Credit5 =                 ("5 Credits","feb0e161-da94-4705-8d56-b48f17d74a99"),
             Credits =                 ("Credit","bda3ae36-c312-4bf7-a288-7ee7760c26f7"),
             Tag =                     ("Tag","1d1e7dd2-c60a-4770-82b7-d2d9232b3be8"),
             Advancement =             ("Advancement", "f8372e2c-c5df-42d9-9d54-f5d9890e9821"),
             Scored =                  ("Scored", "4911f1ad-abf9-4b75-b4c5-86df3f9098ee"),
             PlusOnePerm =             ("Permanent +1", "1bd5cc9f-3528-45d2-a8fc-e7d7bd6865d5"),
             PlusOne =                 ("Temporary +1", "e8d0b72e-0384-4762-b983-31137d4b4625"),
             MinusOne =                ("Temporary -1", "d5466468-e05c-4ad8-8bc0-02fbfe4a2ec6"),
             protectionMeatDMG =       ("Meat Damage protection","2bcb7e73-125d-4cea-8874-d67b7532cbd5"),
             protectionNetDMG =        ("Net Damage protection","6ac8bd15-ac1d-4d0c-81e3-990124333a19"),
             protectionBrainDMG =      ("Brain damage protection","99fa1d76-5361-4213-8300-e4c173bc0143"),
             protectionNetBrainDMG =   ("Net & Brain Damage protection","de733be8-8aaf-4580-91ce-5fcaa1183865"),
             protectionAllDMG =        ("Complete Damage protection","13890548-8f1e-4c02-a422-0d93332777b2"),
             protectionVirus =         ("Virus protection","590322bd-83f0-43fa-9239-a2b723b08460"),
             BrainDMG =                ("Brain Damage","59810a63-2a6b-4ae2-a71c-348c8965d612"),
             DaemonMU =                ("Daemon MU", "17844835-3140-4555-b592-0f711048eabd"),
             BaseLink =                ("Base Link", "2fb5b6bb-31c5-409c-8aa6-2c46e971a8a5"))

             
regexHooks = dict( # A dictionary which holds the regex that then trigger each core command. 
                   # This is so that I can modify these "hooks" only in one place as I add core commands and modulators.
                   # We use "[:\$\|]" before all hooks, because we want to make sure the script is a core command, and nor part of a modulator (e.g -traceEffects)
                  GainX =              re.compile(r'(?<![<,+-])(Gain|Lose|SetTo)([0-9]+)'), 
                  CreateDummy =        re.compile(r'(?<![<,+-])CreateDummy'),
                  ReshuffleX =         re.compile(r'(?<![<,+-])Reshuffle([A-Za-z& ]+)'),
                  RollX =              re.compile(r'(?<![<,+-])Roll([0-9]+)'),
                  RequestInt =         re.compile(r'(?<![<,+-])RequestInt'),
                  DiscardX =           re.compile(r'(?<![<,+-])Discard[0-9]+'),
                  TokensX =            re.compile(r'(?<![<,+-])(Put|Remove|Refill|Use|Infect)([0-9]+)'),
                  TransferX =          re.compile(r'(?<![<,+-])Transfer([0-9]+)'),
                  DrawX =              re.compile(r'(?<![<,+-])Draw([0-9]+)'),
                  ShuffleX =           re.compile(r'(?<![<,+-])Shuffle([A-Za-z& ]+)'),
                  RunX =               re.compile(r'(?<![<,+-])Run([A-Za-z& ]+)'),
                  TraceX =             re.compile(r'(?<![<,+-])Trace([0-9]+)'),
                  InflictX =           re.compile(r'(?<![<,+-])Inflict([0-9]+)'),
                  ModifyStatus =       re.compile(r'(?<![<,+-])(Rez|Derez|Expose|Trash|Uninstall|Possess|Exile)'),
                  SimplyAnnounce =     re.compile(r'(?<![<,+-])SimplyAnnounce'),
                  ChooseKeyword =      re.compile(r'(?<![<,+-])ChooseKeyword'),
                  CustomScript =       re.compile(r'(?<![<,+-])CustomScript'),
                  UseCustomAbility =   re.compile(r'(?<![<,+-])UseCustomAbility'))

automatedMarkers = [] #Used in the Inspect() command to let the player know if the card has automations based on the markers it puts out.

place = dict( # A table holding tuples with the original location various card types are expected to start their setup
            Hardware =              (100, -208, 10, 3, 1),  # 1st value is X, second is Y third is Offset (i.e. how far from the other cards (in pixel size) each extra copy should be played. Negative values means it will fall on top of the previous ones slightly) 
            Program =               (-7, -220, 10, 10, -1), # 4th value is Loop Limit (i.e. at how many cards after the first do we loop back to the first position. Loop is always slightly offset, so as not to hide the previous ones completely)
            Resource =              (-6, -345, 10, 10, -1), # Last value is wether the cards will be placed towards the right or left. -1 means to the left.
            Event =                 (480, -190, 20, 2, 1),
            scoredAgenda =          (495, 8, -45, 6, 1),
            liberatedAgenda =       (336, -206, -45, 6, 1),
            Server =                (-10, 188, 80, 6, -1),
            Operation =             (480, 270, 20, 2, 1),
            ICE =                   (110, 110, 30, 7, -1), # Temporary. ICE, Upgrades, Assets and Agendas will be special
            Upgrade =               (-10, 248, -30, 13, -1), # Temporary.
            Asset =                 (-10, 248, -30, 13, -1), # Temporary.
            Agenda =                (-10, 248, -30, 13, -1) # Temporary.
            )
               
markerRemovals = { # A dictionary which holds the costs to remove various special markers.
                       # The costs are in a tuple. First is clicks cost and then is credit cost.
                     'Fang' :                        (1,2),
                     'Data Raven' :                  (1,1),
                     'Fragmentation Storm' :         (1,1),
                     'Rex' :                         (1,2),
                     'Crying' :                      (1,2),
                     'Cerberus' :                    (1,4),
                     'Baskerville' :                 (1,3),
                     'Doppelganger' :                (1,4),
                     'Mastiff' :                     (1,4)}

CorporateFactions = [
         'Haas-Bioroid',
         'The Weyland Consortium',
         'NBN',
         'Jinteki']
         
RunnerFactions = [
         'Anarch',
         'Shaper',
         'Criminal']
 
CorporationCardTypes = [
         'ICE',
         'Asset',
         'Agenda',
         'Upgrade',
         'Operation']
         
RunnerCardTypes = [
         'Program',
         'Hardware',
         'Resource',
         'Event']

IgnoredModulators = [ # These are modulators to core commands that we do not want to be mentioning on the multiple choice, of cards that have one
               'isSubroutine',
               'onAccess',
               'ignore',
               'div',
               'isOptional',
               'excludeDummy',
               'onlyforDummy',
               'isCost']
               
trashEasterEgg = [
   "You really shouldn't try to trash this kind of card.",
   "No really, stop trying to trash this card. You need it.",
   "Just how silly are you?",
   "You just won't rest until you've trashed a setup card will you?",
   "I'm warning you...",
   "OK, NOW I'm really warning you...",
   "Shit's just got real!",
   "Careful what you wish for..."]
trashEasterEggIDX = 0
 
ScoredColor = "#00ff44"
SelectColor = "#009900"
EmergencyColor = "#ff0000"
DummyColor = "#000000" # Marks cards which are supposed to be out of play, so that players can tell them apart.
RevealedColor = "#ffffff"
PriorityColor = "#ffd700"
InactiveColor = "#888888" # Cards which are in play but not active yer (e.g. see the shell traders)

Xaxis = 'x'
Yaxis = 'y'