import copy
import functhons  as f
positive_infinity = 10000
negative_infinity = -10000
heuristic_number=None

def isMovesLeft(othello) :
    for i in range(8) :
        for j in range(8) :
            if (othello[i][j].legal==True) :
                return True
    return False

def sumCoinParity(othello):
    ais=0
    os=0
    for row in range(8):
        for col in range(8):
            if othello[row][col].color==f.aiplayer:
                ais=ais+1 
            if othello[row][col].color==f.opponent:
                os=os+1
    return [ais,os]

def minimaxAlphabeta(board, depth, isMax,alpha, beta):
    f.make_all_not_legal(board)
    if(isMax):
        f.calc_legal_moves(f.aiplayer,board)
    else:
        f.calc_legal_moves(f.opponent,board)
   
    score=game_heuristic(board=board,heuristic=heuristic_number)
    #print(score)
    if isMovesLeft(board)==False: 
        #print("out in isMovesLeft")
        return score
    if(depth==10):
        #print("out in isMovesLeft depth==3")
        return score
    if isMax:
        best = negative_infinity
        for i in range(8) :		
            for j in range(8) :
                if (board[i][j].legal==True) :
                    temp=copy.deepcopy(board)
                    f.flip_tokens(f.aiplayer,i,j,board)
                    val=minimaxAlphabeta(board,depth + 1,False,alpha,beta)
                    best= max(best, val)
                    alpha = max(alpha, best)
                    board=copy.deepcopy(temp)
                    if beta <= alpha: 
                        #print("alpha break")
                        break
        return best
    else :
        best = positive_infinity
        for i in range(8) :		
            for j in range(8) :
                if (board[i][j].legal==True) :
                    temp=copy.deepcopy(board)
                    f.flip_tokens(f.opponent,i,j,board)
                    val =  minimaxAlphabeta(board, depth + 1, True,alpha,beta)
                    best = min(best, val)
                    beta = min(beta, best)
                    board=copy.deepcopy(temp)
                    if beta <= alpha:
                        #print("beta break")
                        break
        return best

def findBestMove(othello) :
    bestVal = negative_infinity
    bestMove = [-1, -1]
    for i in range(8) :	
        for j in range(8) :
            if othello[i][j].legal==True :
                temp=copy.deepcopy(othello)
                f.flip_tokens(f.aiplayer,i,j,othello)
                f.calc_legal_moves(f.aiplayer,othello)
                moveVal = minimaxAlphabeta(othello, 0, False,negative_infinity,negative_infinity)
                othello=copy.copy(temp)
                if (moveVal > bestVal) :
                    bestMove = [i, j]
                    bestVal = moveVal
    return bestMove

def game_heuristic(board,heuristic=4):
    # defining the ai and Opponent color
    my_color = f.aiplayer
    opp_color = f.opponent
    coin = 0
    corner = 0
    mobility = 0
    # 1 - Coin Parity
    l=sumCoinParity(board)
    coin= 100 * (l[0] -l[1] ) / (l[0] + l[1])
    # 2 - Mobility
    '''
    It attempts to capture the relative difference between 
    the number of possible moves for the max and the min players,
    with the intent of restricting the
    opponents mobility and increasing ones own mobility
    '''
    # basically it calculates the difference between available moves
    f.calc_legal_moves(f.aiplayer,board)
    my_tiles = len(f.return_list_of_legal_moves(board)[0])
    f.make_all_not_legal(board)
    
    f.calc_legal_moves(f.opponent,board)
    opp_tiles = len(f.return_list_of_legal_moves(board)[0])
    f.make_all_not_legal(board)
    if (my_tiles + opp_tiles != 0): 
        mobility = (100.0 * (my_tiles - opp_tiles)) / (my_tiles + opp_tiles)
    else:
        mobility = 0
    # 3 - Corner occupancy
    '''
    Examine all 4 corners :
    if they were my color add a point to me 
    if they were enemies add a point to the enemy
    '''
    my_tiles = opp_tiles = 0
    if board[0][0].color == my_color:
        my_tiles += 1
    elif board[0][0].color == opp_color:
        opp_tiles += 1
    if board[0][7].color == my_color:
        my_tiles += 1
    elif board[0][7].color == opp_color:
        opp_tiles += 1
    if board[7][0].color == my_color:
        my_tiles += 1
    elif board[7][0].color == opp_color:
        opp_tiles += 1
    if board[7][7].color == my_color:
        my_tiles += 1
    elif board[7][7].color == opp_color:
        opp_tiles += 1

    if (my_tiles + opp_tiles != 0):
        corner = 100 * (my_tiles - opp_tiles) / (my_tiles + opp_tiles)
    else:
        corner = 0
    
    # final weighted score
    # adding different weights to different evaluations
    if heuristic == 1:
        #print("we are using coin is ",coin)
        return coin
    elif heuristic == 2:
        #print("we are using mobility is ",mobility)
        return mobility
    elif heuristic == 3:
        #print("we are using corner is ",corner)
        return corner
    else:
        #print("we are using all heuristic",coin+mobility+corner)
        return int( (5 * coin) + (35 * corner) + (25 * mobility) )


