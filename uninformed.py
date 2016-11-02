import sys
import copy

from dom_indep import *
from dom_dep import *


def unload(G, current, open_list, closed_list):
    """load cask to robot or unload cask to a given stack
    unable to unload on a stack without room for the cask
    unable to load from an empty stack"""

    if current.state_space[1] is "":  # No cask in robot-LOAD
        if current.last_op[0] != "unload":
            if current.stack_status[current.state_space[0]][1] == []:  # Se não tiver casks no stack
                return []
            else:  # Se tiver casks no stack
                new_status = copy.deepcopy(current.stack_status)
                load = new_status[current.state_space[0]][1].pop()  # faz load da cask do topo da pilha
                new_status[current.state_space[0]][0] = new_status[current.state_space[0]][0] - G.cask[load][0]

                ss = [current.state_space[0], load, current.state_space[2] + 1]
                if any(node.state_space == ss for node in (open_list + closed_list)):
                    return []
                else:
                    setup = [ss, current.state_space, [], current.depth + 1, current.gx + 1 + G.cask[load][1], 0, ["load", load, current.state_space[0], 1 + G.cask[load][1]], new_status]
                    new = state_node(setup)
                    return new
        else:
            return []

    else:  # O robo tem uma cask consigo_UNLOAD
        if current.last_op[0] != "load":
            load = current.state_space[1]
            if G.stack[current.state_space[0]][0] >= current.stack_status[current.state_space[0]][0] + G.cask[load][
                0]:  # verifica se ha espaco na stack
                new_status = copy.deepcopy(current.stack_status)
                new_status[current.state_space[0]][0] = new_status[current.state_space[0]][0] + G.cask[load][0]
                new_status[current.state_space[0]][1].append(load)

                ss = [current.state_space[0], "", current.state_space[2] + 1]

                if any(node.state_space == ss for node in (open_list + closed_list)):
                    return []
                else:
                    setup = [ss, current.state_space, [], current.depth + 1, current.gx + 1 + G.cask[load][1], 0,
                             ["unload", load, current.state_space[0], 1 + G.cask[load][1]], new_status]
                    new = state_node(setup)
                    return new
            else:
                return []
        else:
            return []





def move(G, current, dest, cost, open_list):
    """move robot from current location to adjacent node"""

    # get total cost
    if current.state_space[1] == "":
        tcost = cost
    else:
        tcost = (1 + G.cask[current.state_space[1]][1]) * cost

    # build new setup for the children
    #   [position, Cask, nº of loads]
    #   previous state space
    #   next state spaces
    #   depth level
    #   total cost until current node
    #   [op, arg1, arg2, cost]
    setup = [[dest, current.state_space[1], current.state_space[2]], current.state_space, [], current.depth + 1, current.gx + tcost, 0, ["move", current.state_space[0], dest, tcost], current.stack_status]
    new = state_node(setup)

    if any(node.state_space == new.state_space for node in open_list):
        for i, j in enumerate(open_list):

            if j.gx > new.gx:
                if j.state_space == new.state_space:
                    open_list.pop(i)
                    current.children = [new.state_space]
                    open_list.append(new)
                    break
    else:
        current.children = [new.state_space]
        open_list.append(new)


def find_children(G, current, open_list, closed_list):
    """Appends children from current node to open_list,
    as per the general search algorithm"""

    children = []

    # to expand the children, we need to see if we are in a stack node
    # if so,  then we can either load or unload (or move)
    # the unload function will give us all the children that result
    # in either a load action or unload action
    if current.state_space[0] in G.stack.keys():  # current node is a stack
        children = unload(G, current, open_list, closed_list)
        if children == []:
            pass
        else:
            # need to send child to closed_list if duplicate already exists in open_list
            if not belong_to_open_list(open_list, children):
                open_list.append(children)
#                elif not belong_to_open_list(closed_list, children):
#                    closed_list.append(children)
#            for node in children:
#                if node not in open_list:
#                    open_list.append(node)
#                else:
#                    closed_list.append(node)

    # iterate through the neighbours of current node to see if
    # any children result from the move action
    for neighbour in G.node[current.state_space[0]]:
        if any (node.state_space == [str(neighbour), current.state_space[1], current.state_space[2]] for node in (open_list + closed_list) ):
            pass
        else:
            move(G, current, str(neighbour), G.node[current.state_space[0]][str(neighbour)], open_list)
            # need to send child to closed_list if duplicate already exists in open_list
            if children != []:
                for c in children:
                    if not belong_to_open_list(open_list, children):
                        open_list.append(children)
#                    elif not belong_to_open_list(closed_list, children):
#                        closed_list.append(children)
#            for node in children:
#                if node not in open_list:
#                    open_list.append(node)
#                else:
#                    closed_list.append(node)

    return open_list


def choose_next_node(open_list, closed_list, i):
    """Apply Uniform cost algorithm to choose next node/step in tree"""

    selected_node = open_list[0]
    minimum_cost = selected_node.gx

    # select the node with the minimum cost
    for id,node in enumerate(open_list):
        if node.gx < minimum_cost:
            minimum_cost = node.gx
            selected_node = node

    # send nodes with the same state but with higher cost to closed list
    for node in open_list:
        if (node.state_space[:2] == selected_node.state_space[:2]) and (node != selected_node):
            closed_list.append(node)

    # for debug, do BFS
    #selected_node = open_list[0]

    open_list.remove(selected_node)
    return selected_node


def main():
    # create graph of the problem
    G = open_file(sys.argv[1])

    init_stack_occupied = {}
    for stack in G.stack.keys():
        init_stack_occupied[stack] = [0, []]
        for cask in G.stack[stack][1]:
            init_stack_occupied[stack][0] = init_stack_occupied[stack][0] + G.cask[cask][0]
            init_stack_occupied[stack][1].append(cask)

    # Initialise open_list
    # the CTS starts at the EXIT node, with no casks
    open_list = [state_node( [["EXIT", "", 0], [], [], 0, 0, 0, [], init_stack_occupied] )]
    closed_list = []

    i=0

    while 1:

        if len(open_list) == 0:  # FAILURE
            return

            
        # for i in open_list: i.show()
        # choose next node from open_list
        #current = open_list.pop()
        current = choose_next_node(open_list, closed_list, i)
        i+=1


        if current.state_space[0:2] == ["EXIT", sys.argv[2]]:  # FINISH
            print('i=%d' % i)
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

        open_list = find_children(G, current, open_list, closed_list)
        
        
        open_list.sort(key=lambda node: node.gx,reverse=True)


if __name__ == "__main__":
    main()