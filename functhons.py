import copy

import numpy as np
import aiFuncthions as ai
from tkinter import *

aiplayer, opponent,noGame,drow = 'B', 'W','N','D'
class graphItem:
    def __init__(self) :
        self.color=noGame
        self.legal=False
    def setItemValus(self,color):
        self.color=color
    def setItemLegal(self,legal):
        self.legal=legal
     
othello_list=[
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(),graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()],
  [graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem(), graphItem()]
]
# make the intial board
othello=np.array(othello_list)
othello[3][3].setItemValus(opponent)
othello[3][4].setItemValus(aiplayer)
othello[4][3].setItemValus(aiplayer)
othello[4][4].setItemValus(opponent)

#لطباعه اللعبه
def printOthello(othello):
    print("*************************************************************************")
    for i in othello:
        row="*\t"
        for j in i:
            if j.legal and j.color==noGame:
                row=row+"Y\t" 
            elif j.color==opponent:
                row=row+opponent+"\t"
            elif j.color==aiplayer:
                row=row+aiplayer+"\t"
            else : row=row+"-\t"
        row=row+"*"
        print(row)
    print("*************************************************************************\n")
 
#لايجاد الاماكن المسموح اللعب فيها
def check_line_match(color,dr,dc,r,c,othello):
    if othello[r][c].color==color:
        return True
    if r+dr<0 or r+dr>7:
        return False
    if c+dc<0 or c+dc>7:
        return False 
    return check_line_match(color,dr,dc,r+dr,c+dc,othello)

def adj_sup(color,dr,dc,r,c,othello):
    other=None
    if color==opponent:
        other=aiplayer
    elif color==aiplayer:
        other=opponent
    else:
        print("ereoe adj_sup ",color)
        return False
    if r+dr<0 or r+dr>7:
        return False
    if c+dc<0 or c+dc>7:
        return False
    if othello[r+dr][c+dc].color !=other:
        return False
    if r+dr+dr <0 or r+dr+dr>7:
        return False
    if c+dc+dc <0 or c+dc+dc>7:
        return False
    return check_line_match(color,dr,dc,r+dr+dr,c+dc+dc,othello)
        
def calc_legal_moves(color,othello):
    for row in range(8):
        for col in range(8):
            nw=adj_sup(color,-1,-1,row,col,othello)
            nn=adj_sup(color,-1,0,row,col,othello)
            ne=adj_sup(color,-1,1,row,col,othello)
            ww=adj_sup(color,0,-1,row,col,othello)
            ee=adj_sup(color,0,1,row,col,othello)
            sw=adj_sup(color,1,-1,row,col,othello)
            ss=adj_sup(color,1,0,row,col,othello)
            se=adj_sup(color,1,1,row,col,othello)
            if (nw or nn or ne or ww or ee or sw or ss or se) and othello[row][col].color ==noGame:
                othello[row][col].legal=True
    return othello

#للقلب
def flip_line(color,dr,dc,r,c,othello) :
    if r+dr<0 or r+dr>7:
        return False
    if c+dc<0 or c+dc>7:
        return False
    if othello[r+dr][c+dc].color==noGame:
        return False
    if othello[r+dr][c+dc].color==color:
        return True
    else:
        if flip_line(color,dr,dc,r+dr,c+dc,othello):
            othello[r+dr][c+dc].color=color
            return True
        else: return False

def flip_tokens(color,row,col,othello ):
    othello[row][col].color=color
    flip_line(color,-1,-1,row,col,othello)
    flip_line(color,-1,0,row,col,othello)
    flip_line(color,-1,1,row,col,othello)
    flip_line(color,0,-1,row,col,othello)
    flip_line(color,0,1,row,col,othello)
    flip_line(color,1,-1,row,col,othello)
    flip_line(color,1,0,row,col,othello)
    flip_line(color,1,1,row,col,othello)

def make_all_not_legal(othello):
    for row in range(8):
        for col in range(8):
            othello[row][col].legal=False
    return othello

def return_list_of_legal_moves(othello):
    l=[]
    for row in range(8):
       for col in range(8):
            if othello[row][col].legal and othello[row][col].color==noGame :
                l.append([row,col])
    strr="pick on of this legal moves "
    for i in range(len(l)):
        strr=strr+str(i)+"-"+str(l[i])+"\t"
    return [l,strr]

def game_over(othello):
    full=0
    os=0
    ais=0
    winner=None
    gameover=False
    for row in range(8):
        for col in range(8):
            if othello[row][col].color!=noGame:
                full=full+1 
            if othello[row][col].color==opponent:
                os=os+1 
            if othello[row][col].color==aiplayer:
                ais=ais+1
    if os==0:
        winner=aiplayer
        gameover=True
    elif ais==0:
        winner=opponent
        gameover=True
    elif(full==64):
        if os>ais:
            winner=opponent
            gameover=True
        elif os<ais:
            winner=aiplayer
            gameover=True
        else: 
            winner=drow
            gameover=True
    if gameover :
        return [True,os,ais,winner]
    else :
        return [False,os,ais]
        
def one_on_one_main_fun(othello):
    turn=""
    j=1
    while True:
        data=game_over(othello)
        if data[0]:
            printOthello(othello)
            print("game over ended whith ",j," moves")
            w=data[3]
            if w==drow:
                print("drow both W and B has ",data[1]," point \n")
            elif w==opponent:
                print(opponent+" has won with ",data[1]," point \n")
            else : print(aiplayer+" has won with ",data[2]," point \n")
            break
        else :
            if j%2==0:
                turn=aiplayer
            else :
                turn=opponent
            print("its ",turn," turn ",opponent," has ",data[1]," point ",aiplayer," has ",data[2]," point  so sum is ",data[1]+data[2]," \n")
            printOthello(othello)
            othello=calc_legal_moves(turn,othello)
            printOthello(othello)
            legal_moves=return_list_of_legal_moves(othello)
            if(len(legal_moves[0])==0):
                print(turn," has no legal moves ")
                j=j+1
                continue
            while(True):
                i=int(input(legal_moves[1]))
                if i<0 or i>(len(legal_moves[0])-1) :
                    print("invald number")
                    continue
                else:
                    break 
            print(legal_moves[0][i])
            flip_tokens(turn,legal_moves[0][i][0],legal_moves[0][i][1],othello)
            make_all_not_legal(othello)
            j=j+1

def ai_on_one_main_fun(othello):
    turn=""
    j=1
    while True:
        data=game_over(othello)
        if data[0]:
            printOthello(othello)
            print("game over ended whith ",j," moves")
            w=data[3]
            if w==drow:
                print("drow both W and B has ",data[1]," point \n")
            elif w==opponent:
                print(opponent+" has won with ",data[1]," point \n")
            else : print(aiplayer+" has won with ",data[2]," point \n")
            break
        else :
            if j%2==0:
                turn=aiplayer
                print("its ai turn ai is ",aiplayer)
                printOthello(othello)
                calc_legal_moves(turn,othello)
                printOthello(othello)
                temp=copy.deepcopy(othello)
                ll=ai.findBestMove(othello)
                othello=copy.deepcopy(temp)
                print("The value of the best  Move in main is :",ll)
                if len(ll)==0:
                    print("ai has no legal move")
                    j=j+1
                    continue
                flip_tokens(turn,ll[0],ll[1],othello)
                make_all_not_legal(othello)
                j=j+1
                continue
            else :
                turn=opponent
                print("its ",turn," turn ",opponent," has ",data[1]," point ",aiplayer," has ",data[2]," point  so sum is ",data[1]+data[2]," \n")
                printOthello(othello)
                othello=calc_legal_moves(turn,othello)
                printOthello(othello)
                legal_moves=return_list_of_legal_moves(othello)
                if(len(legal_moves[0])==0):
                    print(turn," has no legal moves ")
                    j=j+1
                    continue
                while(True):
                    i=int(input(legal_moves[1]))
                    if i<0 or i>(len(legal_moves[0])-1) :
                        print("invald number")
                        continue
                    else:
                        break 
                print(legal_moves[0][i])
                flip_tokens(turn,legal_moves[0][i][0],legal_moves[0][i][1],othello)
                make_all_not_legal(othello)
                j=j+1              	
    

# main function human against ai
def ai_vs_human_main_fun_gui():
    '''this to be executed before the click function is called '''
    # useing global variables
    global root,screen,currntlegalMoves,turn,othello
    #claculate legal moves to change 'currentlegalMove' and to make the legal move appear on board
    currntlegalMoves = return_list_of_legal_moves(calc_legal_moves(opponent,othello)) 
    #draw the board
    drawBoard(othello)
    make_all_not_legal(othello)
    # these two lines will write the opponent in the screen
    screen.create_text (200,420,text =  opponent+"'s turn which is the human " ,fill="white")
    screen.update()
    '''---------------------------------------------------------'''
    #the function to click , it also send X and Y dimention
    screen.bind("<Button-1>", callback )
    #run screen -- an ininfty loop --
    root.mainloop()
"--------------------------------------------------------------------------------------------------------"
# this function makes the move you click move and the AI move(s)  
#it has a pramter that changes when you click 'event' that tells you the X of the click 'event.x' and Y of the click 'event.y'
def callback(event):
    #using global variables
    global currntcol, currntRow , othello, currntlegalMoves 
    # set the varaible data from game_over function
    data=game_over(othello)
    #make current move incase you have returned to play agains
    currntlegalMoves = return_list_of_legal_moves(calc_legal_moves(opponent,othello)) 
    #set the 'current row' to the row you clicked
    currntRow   = int (returnRowCol(event.x, event.y)[0] ) 
    #set the 'current col' to the row you clicked
    currntcol  = int ( returnRowCol(event.x, event.y)[1] )
    #if ai and huamn do not have legal moves --end game--
    if (len(currntlegalMoves[0]) <=0)  : 
        make_all_not_legal(othello)
        if ( len (return_list_of_legal_moves(calc_legal_moves(aiplayer,othello)))  <=0)  : 
                make_all_not_legal(othello)
                #delete screen
                screen.delete(ALL) 
                # draw the game over board
                drawBoard(othello,gameOver = True) 
                return
    # if unvalid click  do nothing
    if (currntlegalMoves[0].count([ currntRow ,currntcol]) <= 0 )  :    
            #print ("clicked at [" , currntRow , ',' ,  currntcol , ']')
            #print('the legal moves :' , currntlegalMoves[0])
            return     
    # human's move
    while True : 
            # calc your legal move
            currntlegalMoves = return_list_of_legal_moves(calc_legal_moves(opponent,othello)) 
            # index of the legal you picked
            moveIndex = currntlegalMoves[0].index([currntRow ,currntcol])
            # make your move
            makeMove ( opponent , moveIndex)
            # keep data up to date - in case you your move is the last
            data=game_over(othello)
            # draw the new board and update screen
            drawBoard(othello)
            # make all moves ilegal to clculate the next legal moves rightly 
            make_all_not_legal(othello)
            
            #check if AI has valid moves or not
            if (len (return_list_of_legal_moves (calc_legal_moves(aiplayer,othello))[0]) ==  0 ): 
                # if game over , if you get here means that your move was the last move in the game
                if (data[0]) : break
                # calculate legal moves to appear when i draw the board
                calc_legal_moves(opponent,othello)
                #draw the board that will appear befor the next click
                drawBoard(othello)
                # if the game isn't over , and human can play again the function will be called again
                print('ai has no legal moves human playes again ')
                return 
            # this loop would be executed only one time
            break 
    #AI's move
    while True : 
            #not to make any move when ai don't have
            if (len (return_list_of_legal_moves (calc_legal_moves(aiplayer,othello))[0]) ==  0 ): break
            # calculate AI's move
            currntlegalMoves = return_list_of_legal_moves(calc_legal_moves(aiplayer,othello))
            #make the best move using the alpha beta algprithm
            makeMove (aiplayer , AI =  True )
            # keep data up to date - in case you your move is the last
            data=game_over(othello)
            # draw the new board and update screen
            drawBoard(othello)  
            # make all moves ilegal to clculate the next legal moves rightly 
            make_all_not_legal(othello)
            # clculate the move of your opponant
            currntlegalMoves = return_list_of_legal_moves(calc_legal_moves(opponent,othello))
            #check if opponent has valid moves or not
            if (len (return_list_of_legal_moves (calc_legal_moves(opponent ,othello))[0]) ==  0 ): 
                # if game over , if you get here means that AI's move was the last move in the game
                if (data[0]) : break
                # if the game isn't over , and AI can play again you loop again
                print('human has no legal moves ai playes again ')
                continue 
            # this loop would be executed at least once and will loop repeatly as long as opponent dosen't have
            break 
    #if the above loops were broken and game over
    if (data[0])  :
            #delete screen
            screen.delete(ALL) 
            # draw the game over board
            drawBoard(othello,gameOver = True) 
            return
    # if game isn't over draw the board
    drawBoard(othello)  
    # these two lines will write the opponent in the screen
    screen.create_text (200,420,text =  opponent+"'s turn which is the human " ,fill="white")
    screen.update()
    #make moves not legal for later
    make_all_not_legal(othello)
    #end
    return  
# this function takes X and Y diemention of a point and returns it as row and col
def returnRowCol (x,y) : 
    col = 0
    row = 0
    if (x>0 and x<50) : 
        col = 0     
    elif (x>50 and x<100) : 
        col = 1
    elif (x>100 and x<150) : 
        col = 2    
    elif (x>150 and x<200) : 
        col = 3
    elif (x>200 and x<250) : 
        col = 4
    elif (x>250 and x<300) : 
        col = 5    
    elif (x>300 and x<350) : 
        col = 6
    elif (x>350 and x<400) : 
        col = 7
 
    if (y>0 and y<50) : 
        row = 0     
    elif (y>50 and y<100) : 
        row = 1     
    elif (y>100 and y<150) : 
        row = 2     
    elif (y>150 and y<200) : 
        row = 3     
    elif (y>200 and y<250) : 
        row = 4     
    elif (y>250 and y<300) : 
        row = 5     
    elif (y>300 and y<350) : 
        row = 6     
    elif (y>350 and y<400) : 
        row = 7     
         
    return [row,col]
# this function ereases screen and draw the paramter 'board' 
def drawBoard (othello,gameOver = False) :
      
        global root
        global screen
        global currntlegalMoves
        data = game_over(othello)
        screen.pack()
        screen.delete(ALL) 
                
        for x in range(9):
            screen.create_line (0, x*50,500, x*50, fill="grey") 
        for x in range(8):
            screen.create_line (x*50,400, x*50, 0, fill="grey")
                
        for x in range(8):
                for y in range(8):
                       if (othello[x][y].color=='W'):
                            screen.create_oval( 50*y +45,  50*x+45   ,   50*y+5   ,50*x+5 ,tags="tile {0}-{1}".format(x,y),fill="white",outline="black")
                       elif (othello[x][y].color=='B'):
                            screen.create_oval( 50*y +45,  50*x+45   ,   50*y+5   ,50*x+5 ,tags="tile {0}-{1}".format(x,y),fill="black",outline="white")
                       elif (othello[x][y].legal==True):
                            screen.create_text( 50*y +25,  50*x+25    ,  text = 'X' ,tags="tile {0}-{1}".format(x,y),fill="white")
        
        screen.create_text (50,420 , text = opponent + ' : '+  str (data[1]) , fill="white")
        screen.create_text (350,420, text = aiplayer +  '  : '+  str (data[2])  ,fill="white")
        root.wm_title("Othello game")
        screen.update()
        if (gameOver == True ) :  
            print( 'game is over  ' , opponent , 'score is : ' , data[1] , 'and ' , aiplayer , "'s score is : " , data[2]  )
            screen.create_text (200,420,text = "Game Over ! " ,fill="red")
#this move make best move if 'ai' and makes move when you send index of the move in the legal index  
def makeMove (turn,moveIndex=0 , AI = False) :
    global othello
   # printOthello(othello)
    calc_legal_moves(turn,othello)
   # printOthello(othello)
    currntlegalMoves = return_list_of_legal_moves(othello)
   
    if (AI == False) : 
        legal_moves = currntlegalMoves
        print('legal moves of ' , turn , "which is the human :",  currntlegalMoves[0])
        print('Human has done this ', legal_moves[0][moveIndex])
        i = moveIndex
        flip_tokens(turn,legal_moves[0][i][0],legal_moves[0][i][1],othello)

    elif (AI==True) : 
        temp=copy.deepcopy(othello)
        ll=ai.findBestMove(othello)
        print('legal moves of ' , turn , "which is the ai :",  currntlegalMoves[0])
        print('ai has done this ', ll)
        othello=copy.deepcopy(temp)
        flip_tokens(turn,ll[0],ll[1],othello)

    make_all_not_legal(othello)          
# the root of the screen
root = Tk()
# screen with spacific width and weight and back ground color
screen = Canvas(root, width=400, height=450, background="#222",highlightthickness=0)
#variables to use as globl after
currntcol = 0
currntRow = 0
currntlegalMoves = 0