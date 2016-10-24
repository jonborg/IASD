from general import *

# trying to implement uniform cost, this way we can garantee optimality

def choose_next_node(open_list):
    
    selected_node = open_list[0]
    minimum_cost = selected_node.gx
    for node in open_list:  # select the node with the minimum cost
        if node.gx < minimum_cost:
            minimum_cost = node.gx
            selected_node = node
    
    # expand this node
    for c in selected_node.children:
        open_list.append(c)
    
    open_list.remove(selected_node)
    return selected_node