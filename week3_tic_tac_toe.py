"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 35         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 2.0   # Score for squares played by the other player

# Add your functions here.
def mc_trial(board, player):
    """
    Function that play board with defined player
    """
    _player = player
    _check = board.check_win()
    while _check==None:
        board.move(random.randrange(board.get_dim()), random.randrange(board.get_dim()), _player)
        _player = provided.switch_player(_player)  
        _check = board.check_win()
      
def mc_update_scores(scores, board, player):
    """
    Function that update the scores of a completed game
    """ 
    board.check_win()
    _player=player
    if board.check_win()==2 or board.check_win()==3:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if board.check_win()==player:
                    if board.square(row, col)==_player:
                        scores[row][col] += SCORE_CURRENT
                    elif board.square(row, col)!=1: 
                        scores[row][col] -= SCORE_OTHER
                else:
                    if board.square(row, col)==_player:
                        scores[row][col] -= SCORE_CURRENT
                    elif board.square(row, col)!=1: 
                        scores[row][col] += SCORE_OTHER

def get_best_move(board, scores):
    """
    Function that return a best move as a tuple (row, column)
    """
    _value = []
    _best_move=[]
    _max = 0
    
    for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                    if board.square(row, col)==1:
                        _value.append(scores[row][col])
    
    if len(_value)>=1:           
        _max = max(_value)
        
    for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                if (board.square(row, col)==1) and (scores[row][col]==_max):
                    _best_move.append((row,col))
    
    if len(_best_move)>0:
        return random.choice(_best_move)
      
def mc_move(board, player, trials):
    """
    Function that return a machine player move as a tuple (row, column)
    """
    _original_board = board
    # create score board for player
    _score=[[row + col for col in range(board.get_dim())] for row in range(board.get_dim())]
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            _score[row][col] = 0
    
    # iterate trials    	
    for num in range(trials):
        _board=board.clone()
        mc_trial(_board, player)
        mc_update_scores(_score, _board, player)
               
    _move =();
    if len(_original_board.get_empty_squares())>0:
        _move = get_best_move(_original_board, _score)
    
    return _move

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)    
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

