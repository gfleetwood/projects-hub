import numpy as np
from pandas import DataFrame
import random
from string import ascii_lowercase

cols = [x for x in ascii_lowercase[:10]]
rows = [i for i in range(1,11)]
players = {True: "player 1", False: "player 2"}
pieces = {True: "QW", False: "QB"}
arrows = {True: "AW", False: "AB️"}

def play():
  
  end = False
  player = True
  board = create_board()
  
  while not end:
    board = make_move(board, player)
    print(board)
    player = not player
    if check_win(board, player): end = True
    
def create_board():
  
  board = DataFrame(np.zeros((10,10), dtype = np.int8), index = rows, columns = cols)
  board.iloc[[0],[3]] = "♕"
  board.iloc[[0],[6]] = "♕"
  board.iloc[[3],[0]] = "♕"
  board.iloc[[3],[9]] = "♕"
  board.iloc[[6],[0]] = "♛"
  board.iloc[[6],[9]] = "♛"
  board.iloc[[9],[3]] = "♛"
  board.iloc[[9],[6]] = "♛"
  
  return(board)
    
def make_move(board, player):
  
  print(board)
  
  piece = pick_piece(board, player)
  move = pick_move(board, player, piece)
  arrow = fire_arrow(board, player, move)
  board = execute_turn(board, player, piece, move, arrow)
  
  return(board)
  
def pick_piece(board, player):
  
  valid = False
  
  while not valid:
    
    piece = input("Pick piece to move: ")
    
    if not validate_on_board(piece):
      print("Position not on board")
      continue
    if  not validate_is_piece(board, piece):
      print("This is not a piece")
      continue
    if not validate_correct_player_piece(board, player, piece):
      print("This is not your piece")
      continue
    
    valid = True
    
  return(piece)
  
def pick_move(board, player, piece):
    
  valid = False
  valid_moves = validate_is_valid_move(board, player, piece)
  
  while not valid:
    
    move = input("Pick position to move it to: ")
    
    if not validate_on_board(move):
      print("Position not on board")
      continue
    if move not in valid_moves:
      print(valid_moves)
      print("This move is not valid")
      continue
    if  not validate_is_empty(board, move):
      print("This spot is not empty")
      continue
    
    valid = True
    
  return(move)
  
def fire_arrow(board, player, move):
  
  valid = False
  valid_moves = validate_is_valid_move(board, player, move)
  
  while not valid:
    
    arrow = input("Pick a position to fire an arrow: ")
    
    if not validate_on_board(arrow):
      print("Position not on board")
      continue
    if arrow not in valid_moves:
      print("This move is not valid")
      continue
    if  not validate_is_empty(board,  arrow):
      print("This spot is not empty")
      continue
    
    valid = True
    
  return(arrow)
  
def execute_turn(board, player, piece, move, arrow):
  
  col_move, row_move = read_col_row(move)
  col_piece, row_piece = read_col_row(piece)
  col_arrow, row_arrow = read_col_row(arrow)
  
  board.loc[[row_move], [col_move]] = board.loc[[row_piece], [col_piece]].values[0][0]
  board.loc[[row_piece], [col_piece]] = 0
  board.loc[[row_arrow], [col_arrow]] = arrows[player]
  
  return(board)
  
def check_win(board, player):
  """
   The last player to be able to make a move wins.
   Check if the player can make a move
  """
  win = False
  
  piece_locs = [
    cols[j] + str(i + 1)
    for i in range(board.shape[0]) 
    for j in range(board.shape[1]) 
    if board.iloc[i,j] == pieces[player]
    ]
    
  valid_moves = sum(
    list(map(lambda loc: validate_is_valid_move(board, player, loc), piece_locs)),
    []
    )
  
  if len(valid_moves) == 0:
    win = True
    winner = players[not player]
    print(f"{winner} wins!")
    
  return(win)
  
def validate_on_board(loc):
  
  on_board = False
  
  col, row = loc[:1], int(loc[1:])
  
  if (col in cols) and (row in rows):
    on_board = True
  
  return(on_board)
  
def validate_is_piece(board, piece):
  
  is_piece = False
  col, row = piece[:1], int(piece[1:])
  
  if board.loc[[row], [col]].values[0][0] in list(pieces.values()):
    is_piece = True
    
  return(is_piece)
  
def validate_correct_player_piece(board, player, piece):
  
  correct_player_piece = False
  col, row = read_col_row(piece)
  
  if pieces[player] == board.loc[[row], [col]].values[0][0]:
    correct_player_piece = True
    
  return(correct_player_piece)
  
def validate_is_valid_move(board, player, loc):
  
  read_valid_moves = lambda moves: [x for x in moves if x[0] == True]
  
  is_valid_move = False
  col_index, row = cols.index(loc[:1]), int(loc[1:]) - 1
  
  # Fix row and move across columns
  
  moves_left = [
    [True, cols[col0] + str(row)] if board.iloc[[row], [col0]].values[0][0] == 0
    else [False, cols[col0] + str(row)]
    for col0 in range(0, col_index)
    ]
  
  moves_right = [
    [True, cols[col0] + str(row)] if board.iloc[[row], [col0]].values[0][0] == 0
    else [False, cols[col0] + str(row)]
    for col0 in range(col_index, 10)
    ]
    
  # Fix column and move across rows
  
  moves_up = [
    [True, cols[col_index] + str(row0 + 1)] if board.iloc[[row0], [col_index]].values[0][0] == 0
    else [False, cols[col_index] + str(row0 + 1)]
    for row0 in range(0, row)
    ]
  
  moves_down = [
    [True, cols[col_index] + str(row0 + 1)] if board.iloc[[row0], [col_index]].values[0][0] == 0
    else [False, cols[col_index] + str(row0 + 1)]
    for row0 in range(row, 10)
    ]
    
  # Leading diagonal
  
  # up = r-1, c-1 until one is 0
  
  moves_ldiag_up_locs = list(zip(range(row - 1, -1, -1), range(col_index - 1, -1, -1)))
  
  moves_ldiag_up = [
    [True, cols[loc[1]] + str(loc[0])] if board.iloc[[loc[0]], [loc[1]]].values[0][0] == 0
    else [False, cols[loc[1]] + str(loc[0])]
    for loc in moves_ldiag_up_locs
    ]
    
  # down = r+1, c+1 until one is 9
  
  moves_ldiag_down_locs = list(zip(range(row, 10), range(col_index, 10)))
    
  moves_ldiag_down = [
    [True, cols[loc[1]] + str(loc[0])] if board.iloc[[loc[0]], [loc[1]]].values[0][0] == 0
    else [False, cols[loc[1]] + str(loc[0])]
    for loc in moves_ldiag_down_locs
    ]
  
  # Non-leading diagonal
  
  # up = r-1, c + 1 until r is 0 or c is 9
  moves_nldiag_up_locs = list(zip(range(row - 1, -1, -1), range(col_index + 1, 10)))
  
  moves_nldiag_up = [
    [True, cols[loc[1]] + str(loc[0])] if board.iloc[[loc[0]], [loc[1]]].values[0][0] == 0
    else [False, cols[loc[1]] + str(loc[0])]
    for loc in moves_nldiag_up_locs
  ]
  
  # down = r+1, c - 1 until r is 9 or c is 0
  moves_nldiag_down_locs = list(zip(range(row, 10), range(col_index, -1, -1)))
  
  moves_nldiag_down = [
    [True, cols[loc[1]] + str(loc[0])] if board.iloc[[loc[0]], [loc[1]]].values[0][0] == 0
    else [False, cols[loc[1]] + str(loc[0])]
    for loc in moves_nldiag_down_locs
  ]
  
  valid_moves = read_valid_moves(moves_left) + read_valid_moves(moves_right) + \
                read_valid_moves(moves_up) + read_valid_moves(moves_down) + \
                read_valid_moves(moves_ldiag_up) + read_valid_moves(moves_ldiag_down) + \
                read_valid_moves(moves_nldiag_up) + read_valid_moves(moves_nldiag_down)
                
  valid_moves = [x[1] for x in valid_moves]
                              
  return(valid_moves)
  
def validate_is_empty(board, loc):
  
  is_empty = False
  col, row = loc[:1], int(loc[1:])
  
  if board.loc[[row], [col]].values[0][0] == 0:
    is_empty = True
    
  return(is_empty)
  
def read_col_row(loc):
  
  col, row = loc[:1], int(loc[1:])
  
  return((col, row))
