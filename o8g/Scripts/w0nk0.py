__author__ = 'w0nk0'


def HELP_AddStartEndButtons(group,x=0,y=0): ##TODO w0nk0: implement respective cards -->execute="goToSot",execute="goToEndTurn"
    """
    ##TODO: create GUIDs 5f7ff64b-1df3-4ce8-9153-7d4370fc32b3 / cfc45a19-54ab-46c3-9e51-9b4e01b1bed0
    pngs to /sets-markers-cards
    create cards with ability
    make cards trigger start/end run
    """
    if ds == 'runner':
       table.create('5f7ff64b-1df3-4ce8-9153-7d4370fc32b3', (500 * flipBoard) + flipModX,(-290 * flipBoard) + flipModY, 1) #Start turn
       table.create('cfc45a19-54ab-46c3-9e51-9b4e01b1bed0', (560 * flipBoard) + flipModX, (-290 * flipBoard) + flipModY, 1) #End turn
    else:
       table.create('5f7ff64b-1df3-4ce8-9153-7d4370fc32b3', (500 * flipBoard) + flipModX,(260 * flipBoard) + flipModY, 1) #Start turn
       table.create('cfc45a19-54ab-46c3-9e51-9b4e01b1bed0', (560 * flipBoard) + flipModX, (260 * flipBoard) + flipModY, 1) #End turn
    #table.create('1ce4f50d-2604-4afe-8d8c-551ce0623d70', 0, 0, 1) # Access Granted

