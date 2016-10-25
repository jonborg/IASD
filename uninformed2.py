

import sys
import time

import uninformed

class graph:
    def __init__(self):
        self.cask  = {} # list of casks, a cask has length and weight
        self.stack = {} # list of stacks, a stack has size and casks
        self.node  = {} # list of node conenctions, a node has neighbours and costs
        
    def add_cask(self, id, l, w):
        self.cask[id] = [float(l), float(w)]
        
    def add_stack(self, id, S, s=0, c=[]):
        self.stack[id] = [float(S), float(s), c]

    def add_node(self, node, neighbour, cost):
        self.node.update( {node:{neighbour:float(cost)}} )
        
    def add_connection(self, node, neighbour, cost):
        self.node[node].update( {neighbour:float(cost)} )
    


class state_node:
    def __init__(self,setup):
        self.state_space = setup[0]   # [position, Cask, nº of loads]
        self.parent   = setup[1]      # previous state space
        self.children = setup[2]      # next state spaces
        self.depth    = setup[3]      # depth level
        self.gx       = setup[4]      # total cost until current node
        self.last_op  = setup[5]      # [op, arg1, arg2, cost]
        
#    def has_cask(self):
#        """checks if robot has a cask in current node"""
#        return (self.state_space[1]=="")
    
    def show(self):
        print()
        print("-------------------------")
        print("Space State: ",end="")
        print(self.state_space)
        print("Parent Node: ",end="")
        print(self.parent)
        print("Children Nodes: ",end="")
        print(self.children)
        print("Depth: ",end="")
        print(self.depth)
        print("Path Cost: ",end="")
        print(self.gx)
        print("Last Operation: ",end="")
        print(self.last_op)
        print("-------------------------")
        print()










def open_file(file):
    """reads input file and creates graph of the problem"""

    G = graph()
     
    f = open(file)
    lines = f.readlines()

    for x in lines:
        w = x.split()   # get words from current line
        print(w)
        i=list(x)
        if i[0]=="C": # if first letter in line = 'C' then cask
            G.add_cask(w[0],w[1],w[2])
        if i[0]=="S": # if first letter in line = 'S' then stack
            if len(w)>2:
                occupied=0
                for C in w[2:len(w)]:
                    occupied=occupied+G.cask[C][0]
                G.add_stack(w[0],w[1],occupied,w[2:len(w)])
            else:
                G.add_stack(w[0],w[1])
        if i[0]=="E": # if first letter in line = 'E' then edge
            if w[1] in G.node:
                G.add_connection(w[1],w[2],w[3])
            else:
                G.add_node(w[1],w[2],w[3])
                
            if w[2] in G.node:
                G.add_connection(w[2],w[1],w[3])
            else:
                G.add_node(w[2],w[1],w[3])

    f.close()
    return G

    



        
def unload(G, current, open_list, closed_list):
    """load cask to robot or unload cask to a given stack
    unable to unload on a stack without room for the cask
    unable to load from an empty stack"""
    
    if current.state_space[1] is "": # no cask on robot
        if G.stack[current.state_space[0]][2]==[]: # no casks on stack
            return []
        else: # has casks on stack
            load = G.stack[current.state_space[0]][2].pop()  # load cask from top of stack on robot
            ss = [current.state_space[0], load, current.state_space[2]+1]
            if any (node.state_space==ss for node in (open_list+closed_list)):
                G.stack[current.state_space[0]].append(load)
                return []
            else:
                print(load)
                setup = [ss, current.state_space, [], current.depth+1, current.gx+1+G.cask[load][1], ["load", load, current.state_space[0], 1+G.cask[load][1]]]
                new = state_node(setup)
                return new
    else: # robot has a cask
        load = current.state_space[1]
        if G.stack[current.state_space[0]][0] >= G.stack[current.state_space[0]][1]+G.cask[load][0]: # stack has free space for the new cask
            G.stack[current.state_space[0]].append(load)    # unload cask on stack
            ss = [current.state_space[0], "", current.state_space[2]+1]
            if any (node.state_space == ss for node in (open_list + closed_list)):
                G.stack[current.state_space[0]].pop()
                return[]
            else:    # stack has no space for cask
                setup = [ss, current.state_space, [], current.depth+1, current.gx+1+G.cask[load][1], ["unload",load,current.state_space[0],1+G.cask[load][1]]]
                new = state_node(setup)
                return new
        else:
            return[]
        
        
def move(G, current, dest, cost):
    """move robot from current location to adjacent node"""
    
    # get total cost
    if current.state_space[1] == "":
        tcost = cost
    else:
        tcost = (1+G.cask[current.state_space[1]][1])*cost

    # build new setup for the children
    #   [position, Cask, nº of loads]
    #   previous state space
    #   next state spaces
    #   depth level
    #   total cost until current node
    #   [op, arg1, arg2, cost]
    setup = [ [dest, current.state_space[1], current.state_space[2] ], current.state_space, [], current.depth+1, current.gx+tcost, ["move", current.state_space[0], dest, tcost] ]
    new = state_node(setup)
    current.children = [new.state_space]
    return new
    
    
    

def belong_to_open_list(open_list, closed_list, child):
    """Checks if child exists in open_list"""
    
    if child in open_list:
        return True
    else:
        return False
        
        
        

def find_children(G, current, open_list, closed_list):
    """Appends children from current node to open_list, 
    as per the general search algorithm"""
    
    children = []

    # to expand the children, we need to see if we are in a stack node
    # if so,  then we can either load or unload (or move)
    # the unload function will give us all the children that result
    # in either a load action or unload action
    if current.state_space[0] in G.stack.keys():    # current node is a stack
        children = unload(G, current, open_list, closed_list)
        if children == []:
            pass
        else:
            # need to send child to closed_list if duplicate already exists in 
            # open_list
            if not belong_to_open_list(open_list, closed_list, children):
                open_list.append(children)
            else:
                closed_list.append(children)
    
    # iterate through the neighbours of current node to see if
    # any children result from the move action
    for neighbour in G.node[current.state_space[0]]:
        if any (node.state_space == [str(neighbour), current.state_space[1], current.state_space[2]] for node in (open_list + closed_list)):
            pass
        else:
            children = move(G, current, str(neighbour), G.node[current.state_space[0]][str(neighbour)])
            # need to send child to closed_list if duplicate already exists in 
            # open_list
            if not belong_to_open_list(open_list, closed_list, children):
                open_list.append(children)
            else:
                closed_list.append(children)
        
    return open_list



def print_output(final,closed_list):
    
    current = final
    commands = []
    total = 0
    
    while current.parent != []:
        commands.append(current.last_op)
        for index, item in enumerate(closed_list):
            if item.state_space == current.parent:
                break
        current = closed_list[index]

    f = open('results.txt','wt')
    while commands != []:
        line = commands.pop()
        print(*line, sep=' ', file=f)
    print(final.gx, file=f)
    f.close()




    
def main():
    
    # create graph of the problem
    G=open_file(sys.argv[1])
    print()     
    print(G.cask)
    print()     
    print(G.stack)
    print()     
    print(G.node)


    open_list = [state_node([["EXIT","",0],[],[],0,0,[]])]    # the CTS starts at the EXIT node, with no casks
    closed_list = []

    while 1:
        
        #time.sleep(5)
        if len(open_list) == 0:
            print()
            print("FAILURE")
            return
            
        #current = open_list.pop()
        current = uninformed.choose_next_node(open_list, closed_list)
        print()
        print (current.state_space)
        print("Action: " + str(current.last_op))
        
        if current.state_space[0:2] == ["EXIT",sys.argv[2]]:    # args: 'python', 'general.py', 's1.dat', 'Cb'
            print()
            print("FINISH!!!")
            print(current.state_space)
            print_output(current, closed_list)
            return
        

        closed_list.append(current)
        print()
        print("Open List:")
        print("----------------------")      
        for node in open_list:
            print(node.state_space)    
        print("----------------------")
        print()
        print("Closed List:")
        print("----------------------")      
        for node in closed_list:
            print(node.state_space)    
        print("----------------------")
        
        open_list=find_children(G,current,open_list,closed_list)
        
        
if __name__ == "__main__":
    main()
