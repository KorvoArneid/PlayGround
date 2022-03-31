from os import system, name
import time

def state(board):  #0 means none, 1 means player 1 , 2 means player 2 , 3 means draw
    checks=[
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]  
    ]
    end=1;
    for k in range(9):
        if(board[k]==0):
            end=0
    for check in checks:
        if(board[check[0]] == board[check[1]] == board[check[2]] and board[check[1]]!=0):
            return board[check[1]]
    if(end):
        return 3
    else:
        return 0

class node:
    def __init__(self):
        self.last = 1 # 0 means cross and 1 means naught
        self.lastMove = -1 #last move made
        self.board = [0]*9
        self.children = {}
        self.state = 0 # 0 means donno, -1 means lose, 1 means win
        self.bestMove = -1
        self.stateFound=0

def ltos(board):
    st = ""
    for k in board:
        st = st + str(k) + " "
    return st

memo = {}

def dfs(cur):
    if(memo.get(ltos(cur.board)) != None):
        found=memo[ltos(cur.board)] # stores 1 lengthed list in it to work as pointer
        cur.bestMove=found.bestMove
        cur.stateFound=found.stateFound
        cur.children=found.children.copy()
        cur.state=found.state
        return None
    
    best = -1
    for k in range(9):
        if(cur.board[k]!=0):
            continue
        child = node()
        child.last = 1 if(cur.last==0) else 0
        child.lastMove=k
        child.board=cur.board.copy()
        child.board[k]=child.last + 1

        condition=state(child.board);
        if(condition == 0):
            dfs(child)
        else:
            child.stateFound=1;
            if(condition==3):
                child.state=0;
            else:
                child.state=-1; #ending state can only be losing

        cur.children[k]=child
        if(child.state == -1 and best < 1):
            best=1
            cur.bestMove = child.lastMove
        elif(child.state == 0 and best < 0):
            best=0
            cur.bestMove = child.lastMove
        if(best == -1):
            cur.bestMove = child.lastMove

    cur.state=best;
    memo[ltos(cur.board)]=cur

def printb(board):
    for i in range(3):
        for j in range(3):
            if(board[i*3+j] == 0):
                print(i*3+j+1, end='')
            if(board[i*3+j] == 1):
                print('X', end='')
            if(board[i*3+j] == 2):
                print('O', end='')
        print()

def endstate(head):
    condition=state(head.board)
    if(condition==1):
        print("You won! :#")
    elif(condition==2):
        print("AHAHAH I WON!")
    elif(condition==3):
        print("DRAW, Nice play ;)")
    assert condition != 0

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def main():
    board=[0]*9
    head=node()
    dfs(head)
    st = 'N'
    while(st != 'Y'):
        clear()
        print("LETS START PLAYING TIC TAC TOE WITH AN AI")
        print("You have to enter a number in the cell of a board to select it as your choice...\npress any button to start...")
        st = input("Ready? (Y)es or (N)o? : ")

    #game loop
    while(True):
        clear()
        printb(board)
        if(head.stateFound):
            endstate(head)
            exit(0);
        
        choice = 0
        choice = int(input("enter your choice player : ")) 
        choice-=1
        if(choice < 0 or choice >=9 or board[choice]!=0):
            print("Wrong choice!! try again...wait a secs...")
            time.sleep(1)
            continue

        board[choice]=1
        clear()
        printb(board)
        head = head.children[choice]
        if(head.stateFound):
            endstate(head)
            exit(0)
        head = head.children[head.bestMove]
        board[head.lastMove]=2
        print("Ai chose ... "+str(head.lastMove+1)+" ...")
        time.sleep(1)

main()