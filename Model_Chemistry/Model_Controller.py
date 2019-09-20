import numpy as np
from queue import *

def get_neighbours(pos, board):#returns 4 manhattan neighbours 
    neighbours = []
    if pos[0] < 0 or pos[0] > (board.config.board_size_x - 1)\
        or pos[1] < 0 or pos[1] > (board.config.board_size_y - 1):
        print 'Position is not on the grid'
        return neighbours
    
    if pos[0] - 1 > -1:
        neighbours.append([[pos[0]-1, pos[1]], board.get_drop([pos[0]-1, pos[1]])])
    if pos[0] + 1 < board.config.board_size_x:
        neighbours.append([[pos[0]+1, pos[1]], board.get_drop([pos[0]+1, pos[1]])])
    if pos[1] - 1 > -1:
        neighbours.append([[pos[0], pos[1]-1], board.get_drop([pos[0], pos[1]-1])])
    if pos[1] + 1 < board.config.board_size_y:
        neighbours.append([[pos[0], pos[1]+1], board.get_drop([pos[0], pos[1]+1])])

    blocked, avail = [],[]
    for n in neighbours:
        if n[1] == None:
            avail.append(n)
        else:
            blocked.append(n) 
    return np.array(avail), np.array(blocked)

def bfs(board,start,end): #breadth-first search
    #returns a dictionary that links cells back to the previous
    frontier = Queue()
    frontier.put(start)
    came_from = {}
    #came_from[tuple(start)] = None
    while not frontier.empty():
        current = frontier.get()
        if current == tuple(end):
            return came_from
        
        avail,full = get_neighbours(current, board)
        for n in full:#see if end goal is an obstacle i.e another drop
            if n[0] == end:
                came_from[tuple(n[0])] = current
                return came_from
        
        for n in avail:#
            n = tuple(n[0])
            if not came_from.has_key(n):  
                came_from[n] = current
                frontier.put(n)
    return None

#returns the list of cells that lead from start to end
def get_path(board,start,end):
    came_from = bfs(board,start,end)
    if came_from == None:
        print 'No path between (%d,%d) and (%d,%d)'%(start[0], start[1], end[0], end[1])
        return []
    current = tuple(end)
    path = [tuple(end)]
    while not current == start:
        current = came_from[current]
        path.append(tuple(current))
    return path[::-1]

#translats the path into actions given in the board class
def get_moves(board,start,end):
    path = get_path(board,start,end)
    if path == None:
        return None
    moves = np.empty(len(path)-1, dtype = str)
    for i in range(len(path) - 1):
        difference = np.array(path[i+1]) - np.array(path[i])
        if (difference == np.array([1,0])).all():
            moves[i] = 'R'
        elif (difference == np.array([-1,0])).all():
            moves[i] = 'L'
        elif (difference == np.array([0,1])).all():
            moves[i] = 'U'
        elif (difference == np.array([0,-1])).all():
            moves[i] = 'D'
    return moves

def move_drop(board, start, end):
    path = get_path(board,start,end)
    if len(path) < 1:
        return  
    moves = get_moves(board,start,end)
    i = 0
    curr = path[i]
    for a in moves:
        board.actions[a](curr)
        i += 1
        curr = path[i]
    return True #if successfully moved

def mix_species(board, A, B):#move B into A
    drops = np.array(board.get_list())
    species = drops[:,1]
    placements = drops[:,0]    

    if A==B:
        print('Both drops are the same species')
        return

    #find positions of each species 
    placeA = []
    placeB = []
    for i in range(len(drops)):
        if A == species[i].name:
            placeA.append(placements[i])
        if B == species[i].name:
            placeB.append(placements[i])

    if placeA == []:
        print('No drops of %s remain'%A)
        return
    if placeB == []:
        print('No drops of %s remain'%B)
        return
    
    #attempt to move from first position found 
    for pA in placeA:
        for pB in placeB:
            if(move_drop(board,pB,pA) == True):
                return 
