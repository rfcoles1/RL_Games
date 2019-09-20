import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from Model_Chem_Config import Config
from Model_Drop import Droplet

class Board(object):
    def __init__(self):
        self.config = Config 
        self.reset()
        self.species = []

        #board class can move the drops it contains
        self.actions= {'R': self.move_drop_right,
            'L': self.move_drop_left,
            'U': self.move_drop_up,
            'D': self.move_drop_down}       


    def reset(self):        
        self.board = np.empty([self.config.board_size_x, self.config.board_size_y], dtype=Droplet)

    def get_list(self):#returns a list of all the drops remaining on the board
        info = []
        for i in range(self.config.board_size_x):
            for j in range(self.config.board_size_y):
                this_cell = self.board[i,j]
                if this_cell != None:
                    info.append([[i,j],this_cell])
        return info                   
       
    def add_drop(self, pos, drop):#adds drop on given position
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print 'Position is not on the Chip'
        elif self.board[pos[0],pos[1]] != None:
            print 'Position already full'
        else:
            self.board[pos[0],pos[1]] = drop

    def get_drop(self, pos):#returns the drop object at given position
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print 'Position is not on the Chip'
        else:#returns None is no drop located at that grid position
            return self.board[pos[0],pos[1]]

    def remove_drop(self, pos):#removes drop at given position
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print 'Position is not on the Chip'
        else:
            self.board[pos[0],pos[1]] = None

    ### Methods for moving an individual drop ###   
    def move_drop_up(self,pos):
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print('Position is not on the Chip')
            return
        if pos[1]+1 > self.config.board_size_y-1:
            print('Cell is already at the top')
            return

        curr_drop = self.board[pos[0],pos[1]]
        if curr_drop == None:
            print('No drop at (%d,%d)'%(pos[0],pos[1]))    
            return 

        new_cell = self.board[pos[0], pos[1]+1]
        if new_cell == None:
            self.remove_drop(pos)                
            pos = [pos[0], pos[1]+1]
            self.add_drop(pos, curr_drop)
        else:
            new_cell.combine(curr_drop)
            self.board[pos[0],pos[1]] = None

    def move_drop_down(self,pos):
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print('Position is not on the Chip')
            return     
        if pos[1]-1 < 0:
            print('Cell is already at the bottom')
            return

        curr_drop = self.board[pos[0],pos[1]]
        if curr_drop == None:
            print('No drop at (%d,%d)'%(pos[0],pos[1]))
            return 

        new_cell = self.board[pos[0], pos[1]-1]
        if new_cell == None:
            self.remove_drop(pos)                
            pos = [pos[0], pos[1]-1]
            self.add_drop(pos, curr_drop)
        else:
            new_cell.combine(curr_drop)
            self.board[pos[0],pos[1]] = None

    def move_drop_left(self,pos):
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print('Position is not on the Chip')
            return
        if pos[0]-1 < 0:
            print('Cell is already on the left')
            return

        curr_drop = self.board[pos[0],pos[1]]
        if curr_drop == None:
            print('No drop at (%d,%d)'%(pos[0],pos[1]))
            return

        new_cell = self.board[pos[0]-1, pos[1]]
        if new_cell == None:
            self.remove_drop(pos)                
            pos = [pos[0]-1, pos[1]]
            self.add_drop(pos, curr_drop)
        else:
            new_cell.combine(curr_drop)
            self.board[pos[0],pos[1]] = None

    def move_drop_right(self,pos):
        if pos[0] < 0 or pos[0] > (self.config.board_size_x - 1)\
            or pos[1] < 0 or pos[1] > (self.config.board_size_y - 1):
            print('Position is not on the Chip')
            return
        if pos[0]+1 > self.config.board_size_x-1:
            print('Cell is already on the right')
            return

        curr_drop = self.board[pos[0],pos[1]]
        if curr_drop == None:
            print('No drop at (%d,%d)'%(pos[0],pos[1]))
            return
        
        new_cell = self.board[pos[0]+1, pos[1]]
        if new_cell == None:
            self.remove_drop(pos)                
            pos = [pos[0]+1, pos[1]]
            self.add_drop(pos, curr_drop)
        else:
            new_cell.combine(curr_drop)
            self.board[pos[0],pos[1]] = None
 

    def display(self):
        board2plot = np.zeros([self.config.board_size_x, self.config.board_size_y])#all empty cells will be 0
        elements = self.get_list()
        names_set = [] #keeps track of species such that one colour = one species 
        rgbarray = np.ones(3) #white for the background
        for curr in elements:
            pos = curr[0]
            name = curr[1]
            if name in names_set:
                index = names_set.index(name)
                board2plot[pos[0],pos[1]] = index+1
            else:
                names_set.append(name)
                board2plot[pos[0],pos[1]] = len(names_set)
                rgbarray = np.vstack([rgbarray,name.color]) 
        
        cmap = mcolors.ListedColormap(rgbarray)
        bounds = np.arange(0,len(names_set)+2)
        norms = mcolors.BoundaryNorm(bounds,cmap.N)
        im = plt.imshow(board2plot, origin = 'lower', cmap=cmap, norm=norms)
        ax = plt.gca()
        ax.set_xticks(np.arange(0, self.config.board_size_x,1))
        ax.set_yticks(np.arange(0, self.config.board_size_y,1))
        ax.set_xticks(np.arange(-0.5, self.config.board_size_x,1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.config.board_size_y,1), minor=True)
        ax.grid(which='minor')
        colors = [im.cmap(im.norm(value+1)) for value in range(len(names_set))]
        patches = [mpatches.Patch(color=colors[i], label = names_set[i]) for i in range(len(colors))] 
        plt.legend(handles=patches, bbox_to_anchor=(1,1), loc =2) 
        plt.show() 
