from uninformed2 import *

# trying to implement uniform cost, this way we can garantee optimality with
# a resonable complexity

def choose_next_node(open_list, closed_list):
    """Apply Uniform cost algorithm to choose next node/step in tree"""
    
    selected_node = open_list[0]
    minimum_cost = selected_node.gx
    for node in open_list:  # select the node with the minimum cost
        if node.gx < minimum_cost:
            minimum_cost = node.gx
            selected_node = node
    
    # send nodes with the same state but with higher cost to closed list
    for node in open_list:
        if ( (node.state_space[:2] == selected_node.state_space[:2]) and (node != selected_node) ):
            closed_list.append(node)

    # just doing refular BFS for debugging
    selected_node = open_list[0]
    
    open_list.remove(selected_node)
    return selected_node
