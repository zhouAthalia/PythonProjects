#pip install numpy in terminal
import numpy as np
import pygame
import sys
import math


ROW_COUNT = 6 #amount of rows 
COLUMN_COUNT = 7 # amount of columns 

PURPLE = (200,100,200)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #creates the board and fills it upo with 0's
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0 #checks if the colum is filled up all the way 

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
   print(np.flip(board, 0))

def winning_move(board, piece):
   # Check horizontal for win
   for c in range(COLUMN_COUNT-3):
    for r in range(ROW_COUNT):
       if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
          return True
       
    # Check vertical for win
    for c in range(COLUMN_COUNT):
       for r in range(ROW_COUNT-3):
           if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
               return True
           
    # Check poitively sloped diagonal
    for c in range(COLUMN_COUNT -3):
       for r in range(ROW_COUNT-3):
           if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
               return True
           
    # Check negativly sloped diagionals
    for c in range(COLUMN_COUNT-3):
       for r in range(3, ROW_COUNT):
           if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
               return True

def draw_board(board):
   for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT):
         pygame.draw.rect(screen, PURPLE, ((c*SQUARESIZE), (r*SQUARESIZE)+SQUARESIZE, SQUARESIZE, SQUARESIZE))
         pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2),int((r*SQUARESIZE)+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
   for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT):
         if board[r][c] == 1:
            pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int((r*SQUARESIZE)+SQUARESIZE/2)), RADIUS)
         elif board[r][c] == 2 :
            pygame.draw.circle(screen, BLUE, (int(c*SQUARESIZE+SQUARESIZE/2), height - int((r*SQUARESIZE)+SQUARESIZE/2)), RADIUS)
 
   pygame.display.update()



# variables
board = create_board()
game_over = False
turn = 0 

# initialize pygame
pygame.init()

# game size
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

# has pygame read size
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

#creates a font for display
myfont = pygame.font.SysFont("gabriola", 120)


#loop starts 
while not game_over:
    
    for event in pygame.event.get():
      # properly shuts down the game 
        if event.type == pygame.QUIT:
          sys.exit()

        # addtional feature at the top to show what player it is
        if event.type == pygame.MOUSEMOTION:
           #returns the background to black
           pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
           posx = event.pos[0]
           
           if turn == 0:
              pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
           else:
               pygame.draw.circle(screen, BLUE, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update()
              
              


       # if mouse is clicked then piece drops
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # PLayer 1's turn
            if turn == 0:
              posx = event.pos[0]
              col = int(math.floor(posx/SQUARESIZE))
              
              turn += 1
              turn = turn % 2

                     
              if is_valid_location(board, col):
                 row = get_next_open_row(board, col)
                 drop_piece(board, row, col, 1)
                
                 print_board(board)
                 draw_board(board)

                 if winning_move(board, 1):
                    #puts the text on the screen
                    label = myfont.render("Player 1 wins!!", 1, PURPLE)
                    screen.blit(label, (90,5))
                    pygame.display.update()

                    game_over = True
            

        # Player 2 turn
            else:
               posx = event.pos[0]
               col = int(math.floor(posx/SQUARESIZE))
           
               if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        print_board(board)
                        draw_board(board)

                        turn += 1
                        turn = turn % 2

                        if winning_move(board, 2):
                            #puts the text on the screen
                            label = myfont.render("Player 2 wins!!", 1, PURPLE)
                            screen.blit(label, (90, 5))
                            pygame.display.update()

                            game_over = True


            if game_over:
               pygame.time.wait(5000)