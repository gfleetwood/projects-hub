"""
https://github.com/replit/play
https://en.wikipedia.org/wiki/Game_of_the_Amazons
"""

import play
import functions as hf
import numpy as np
from pandas import DataFrame
import random
from string import ascii_lowercase
from itertools import product

players = {True: "player 1", False: "player 2"}
pieces = {True: "QW", False: "QB"}
arrows = {True: "AW", False: "AB️"}

squares = list(product(range(10), range(10)))
board = []
ref_loc = (-225, 225)

tiles = ["assets/square brown dark_png_128px.png", "assets/square brown light_png_128px.png"]
pieces = [
  "assets/blackQueen.png", "assets/whiteQueen.png",
  "assets/blackPawn.png", "assets/whitePawn.png"
  ]

# Construct the chess board
play.new_box(
  color = 'white', x = 0, y = 0, width = 510, height = 510, 
  border_width = 5, transparency = 100, border_color = 'black'
    )

# Fill in the squares of the board
for sq in squares:
  board.append(
    play.new_image(image = tiles[(sq[0] + sq[1]) % 2], x = ref_loc[0] + sq[1]*50, y = ref_loc[1] - sq[0]*50, size = 39)
            )
       
# Place the queens on the board 
qb1 = play.new_image(image = pieces[0], x = ref_loc[0] + 3*50, y = ref_loc[1] - 0*50)
qb2 = play.new_image(image = pieces[0], x = ref_loc[0] + 6*50, y = ref_loc[1] - 0*50)
qb3 = play.new_image(image = pieces[0], x = ref_loc[0] + 0*50, y = ref_loc[1] - 3*50)
qb4 = play.new_image(image = pieces[0], x = ref_loc[0] + 9*50, y = ref_loc[1] - 3*50)

qw1 = play.new_image(image = pieces[1], x = ref_loc[0] + 3*50, y = ref_loc[1] - 9*50)
qw2 = play.new_image(image = pieces[1], x = ref_loc[0] + 6*50, y = ref_loc[1] - 9*50)
qw3 = play.new_image(image = pieces[1], x = ref_loc[0] + 0*50, y = ref_loc[1] - 6*50)
qw4 = play.new_image(image = pieces[1], x = ref_loc[0] + 9*50, y = ref_loc[1] - 6*50)

# 1d to 2d: (a,b) to 10a + b
# qw4.go_to(board[6])
#print(qw4.image)


play.start_program()
