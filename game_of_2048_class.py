# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:31:15 2018

@author: Nicholas DeLateur
"""

import numpy as np
import random

random.seed() # if you want to set the seed for reproducibility    

class game_of_2048:
    
    def grab_neighbors(self, index):
        x = index[0]
        y = index[1]
        neighbor_values = []
        
        if y-1 >= 0:
            neighbor_values.append(self.board[x, y-1])
        if x-1 >= 0:
            neighbor_values.append(self.board[x-1, y])
        if x+1 <= 3:
            neighbor_values.append(self.board[x+1, y])
        if y+1 <= 3:
            neighbor_values.append(self.board[x, y+1])
                
        return neighbor_values
    
    def random_tile(self):
        if random.random() < 0.9:
            return 2
        else:
            return 4
    
    def show_current_state(self):
        print(f'Move: {self.move_count}; Score: {self.score}', '\n',
              self.board, '\n',
              self.game_state, '\n')    

    def open_positions(self):
        possibilities = []
        for i in range(4):
            for j in range(4):
                if self.board[i,j] == 0:
                    possibilities.append([i,j])
        return possibilities
    
    def rotate_to_face_right(self, move):
        if move == 0:
            self.board = np.rot90(self.board, -1)
        elif move == 1:
            pass
        elif move == 2:
            self.board = np.rot90(self.board, 1)
        elif move == 3:
            self.board = np.rot90(self.board, -2)
        else:
            print('error, I do not recognize this move')
    
    def unrotate(self, move):
        if move == 0:
            self.board = np.rot90(self.board, 1)
        elif move == 1:
            pass
        elif move == 2:
            self.board = np.rot90(self.board, -1)
        elif move == 3:
            self.board = np.rot90(self.board, 2)
    
    def roll_right(self):
        # For each row
        for i in range(4):
            
            # Starting from the right most position and working backwards
            for j in range(3, -1, -1):
                
                # If there are still numbers in this range
                if sum(self.board[i,0:j+1]) != 0:
              
                    # as long as there's an empty space to move into
                    while self.board[i,j] == 0:
                        
                        # roll everything right 
                        self.board[i,0:j+1] = np.roll(self.board[i,0:j+1], 1)
    
    def squishes(self):
        # For each row
        for i in range(4):
            
            # Starting from the right most position and working backwards
            for j in range(3, 0, -1):
                
                # If the number that just got put to it's left is the same
                if self.board[i,j] == self.board[i, j-1] and self.board[i,j] != 0:
                    
                    # Take the left tile and delete it
                    self.board[i, j-1] = 0
                    
                    # And double the right tile
                    self.board[i, j] =  self.board[i,j] * 2
                    
                    # And add that to our score
                    self.score = self.score + self.board[i, j]
                    
    def add_tile(self):
        possible_positions = self.open_positions()
        if possible_positions != []:
            chosen_position = random.choice(possible_positions)
            self.board[chosen_position[0], chosen_position[1]] = self.random_tile()
          
    def squishables_exist(self):
        ''' This function only gets called if the board is full
            It checks if any number is next to an equal number '''
        
        squishables_do_exist = False
        
        # For each tile
        for index, value in np.ndenumerate(self.board):
        
            # Grab neighbor values
            neighbor_values = self.grab_neighbors(index)

            # Check to see if any are equal to the tile
            if (value in neighbor_values):
                squishables_do_exist = True
        
        if squishables_do_exist == False:
            self.game_state = 1 # 0=ongoing, 1=loss, 2=win
            print('You lose! Score:', self.score)
            
        return squishables_do_exist
    
    def check_that_valid_move_exists(self):
        valid_move_exists = False
        if (0 in self.board):
            valid_move_exists = True
        elif self.squishables_exist():
            valid_move_exists = True
        
        return valid_move_exists

    def check_for_win(self):
        if 2048 in self.board:
            print('You win! Score:', self.score)
            self.game_state = 2 # 0=ongoing, 1=loss, 2=win   
            
    def update_board_state(self, move):
        '''
        0 = move up
        1 = move right
        2 = move down 
        3 = move left
        
        What we actually do is rotate the game board such that any given move
        is calculated as moving right and then unrotate it back
        '''
        tempboard = np.copy(self.board)
        if self.game_state == 0:  # 0=ongoing, 1=loss, 2=win
            self.rotate_to_face_right(move)
            self.roll_right()
            self.squishes()
            self.roll_right()   
            self.unrotate(move)
            if not np.array_equal(tempboard, self.board):
                self.add_tile()
                self.move_count += 1
            #self.show_current_state()
 
        self.check_for_win()
        self.check_that_valid_move_exists()
        
        return self.move_count, self.score, self.game_state, self.board
    
    def __init__(self):
        self.game_state = 0 # 0=ongoing, 1=loss, 2=win
        self.board = np.zeros((4,4), dtype='int') 
        self.move_count = 0
        self.score = 0
        self.add_tile()
        self.add_tile()

if __name__ == '__main__':
    def play_games(X):
        results = []
        for _ in range(X):
            x = game_of_2048()
            state = 0
            score = 0
            move_count = 0
            
            while state == 0 and move_count < 200000:
                move_count, score, state, board = x.update_board_state(random.randint(0, 3))
            results.append([move_count, score, state])
            
        results = np.array(results)
        return results
    
    from timeit import Timer
    t = Timer('play_games(10)', 'from __main__ import play_games')
    print(t.repeat(number=10, repeat = 10))



