# TIC TAC TOE

def printBoard(xState,zState):
    _0 = 'X' if xState[0] else ('O' if zState[0] else ' ')
    _1 = 'X' if xState[1] else ('O' if zState[1] else ' ')
    _2 = 'X' if xState[2] else ('O' if zState[2] else ' ')
    _3 = 'X' if xState[3] else ('O' if zState[3] else ' ')
    _4 = 'X' if xState[4] else ('O' if zState[4] else ' ')
    _5 = 'X' if xState[5] else ('O' if zState[5] else ' ')
    _6 = 'X' if xState[6] else ('O' if zState[6] else ' ')
    _7 = 'X' if xState[7] else ('O' if zState[7] else ' ')
    _8 = 'X' if xState[8] else ('O' if zState[8] else ' ')

    print(f' { _0} | { _1} | { _2}')
    print(f'---|---|---')
    print(f' { _3} | { _4} |{ _5}')
    print(f'---|---|---')
    print(f' { _6} | { _7} | { _8}')

def checkWin(xState,zState):
    Wins=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
    for win in Wins:
        if xState[win[0]]+xState[win[1]]+xState[win[2]]==3:
            print("X has won the game")
            return 1
        if zState[win[0]]+zState[win[1]]+zState[win[2]]==3:
            print("O has won the game")
            return 0
    if sum(xState)+sum(zState)==9:
        print("The match is a Tie")
        return 2
    return -1


name="main"
if name=="main":
    xState=[0,0,0,0,0,0,0,0,0]
    zState=[0,0,0,0,0,0,0,0,0]

    turn=1 # 1 for X and 0 for O
    print('Welcome to Tic Tac Toe Game')
    while True:
        printBoard(xState,zState)
        if turn==1:
            print('"X\'s Player\'s Turn"')
            value = int(input('Enter the position to place X (0-8): '))
            xState[value]=1
        else:
            print('"O\'s Player\'s Turn"')
            value = int(input('Enter the position to place O (0-8): '))
            zState[value]=1

        cwin=checkWin(xState,zState)
        if cwin!=-1:
            printBoard(xState,zState)
            break

        turn=1-turn
        