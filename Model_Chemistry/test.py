#from Model_Chem_Config import Config
from Model_Drop import Droplet
from Model_Chip import Board
from Model_Controller import *


#config = Config()

LabChip = Board()


Apple = Droplet('A', [1,0,0,0,0], [1,0,0])
Banana = Droplet('B', [0,1,0,0,0], [1,1,0])
Cabbage = Droplet('C', [0,0,1,0,0], [0,1,0])
DragonFruit = Droplet('D', [0,0,0,1,0], [0,0,1])
Egg = Droplet('E', [0,0,0,0,1])


"""
LabChip.add_drop([1,1], Hydrogen)
LabChip.add_drop([0,0], Hydrogen)

print(LabChip.board)
LabChip.move_drop_down([1,1])
print(LabChip.board)
LabChip.move_drop_down([0,0])
print(LabChip.board)
     
print(LabChip.get_list())
LabChip.remove_drop([0,0])
print(LabChip.get_list())
LabChip.reset()
print(LabChip.get_list())
"""

"""
LabChip.add_drop([0,0],Hydrogen)
LabChip.add_drop([1,0],Helium)
print(LabChip.get_list())
LabChip.display()
tmp = LabChip.get_drop([0,0])
print tmp.state
print tmp.return_last_true()
print(LabChip.board)
LabChip.move_drop_left([1,0])
print '---------------------------------'
print(LabChip.board)
tmp = LabChip.get_drop([0,0])
print tmp.state
truth =  tmp.return_last_true()
print truth

print(LabChip.get_list())
LabChip.display()
"""

LabChip.add_drop([0,0], Droplet('A', [1,0,0,0,0], [1,0,0]))
LabChip.add_drop([1,0], Droplet('A', [1,0,0,0,0], [1,0,0]))
LabChip.add_drop([0,1], Droplet('A', [1,0,0,0,0], [1,0,0]))
LabChip.add_drop([1,1], Droplet('A', [1,0,0,0,0], [1,0,0]))
LabChip.add_drop([3,0], Droplet('E', [0,0,0,0,1], [0,0,1]))



#print(Get_Neighbours([0,0], LabChip))
#print(Get_Neighbours([1,0], LabChip))
#print(Get_Neighbours([0,1], LabChip))
#print(Get_Neighbours([1,1], LabChip))

#print bfs(LabChip, [1,0], [3,0])
#print '------'
#print get_path(LabChip, [1,0], [3,0])
#print '################'

"""
move_drop(LabChip,[0,0],[3,3])

LabChip.display()
moves = get_moves(LabChip,[1,0],[3,3])
path = get_path(LabChip,[1,0],[3,3])
curr = path[0]
i = 0
for a in moves:
    LabChip.actions[a](curr)
    i += 1
    curr = path[i]
    LabChip.display()

moves = get_moves(LabChip,[3,3],[3,0])
path = get_path(LabChip,[3,3],[3,0])
curr = path[0]
i = 0
for a in moves:
    LabChip.actions[a](curr)
    i += 1
    curr = path[i]
    LabChip.display()
"""
LabChip.display()
mix_species(LabChip, 'E', 'A')
LabChip.display()
