import z3
import numpy as np
import pandas as pd
from random import randint

def play_game(board, player):
  
  if check_win(board) == 0: return("Draw!")
  if check_win(board) == 1: return("Player {} Wins!".format(player_display[player]))

  board = make_play(board, player)
  print(board, end = "\n\n")
  player = (player + 1) % 2
  result = play_game(board, player)

  return(result)

def make_play(board, player):

  select_position_x = randint(0, rows - 1)
  select_position_y = randint(0, cols - 1)

  while board[select_position_x][select_position_y] != -1:

    select_position_x = randint(0, rows - 1)
    select_position_y = randint(0, cols - 1)

  board[select_position_x][select_position_y] = player

  return(board)

def check_win(board): 

  possible_wins = [
    board[0,:], board[1,:], board[2,:],
    board[:,0], board[:,1], board[:,2],
    np.diagonal(board), np.fliplr(board).diagonal(),
  ]

  possible_win = sum(list(map(lambda x: len(np.unique(x)) == 1 and np.unique(x)[0] in [0, 1], possible_wins)))
  result = 1 if possible_win > 0 else (0 if (-1 not in np.unique(board)) else -1)

  return(result)

rows = 3
cols = 3
board = np.full((rows, cols), -1)
player_display = {0: "1", 1: "2"}
player = 0

print(play_game(board, player))


