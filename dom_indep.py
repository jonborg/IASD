class state_node:
    def __init__(self,setup):
        self.state_space  = setup[0]            # [position,Cask,nº of loads]
        self.parent       = setup[1]            # previous state space
        self.children     = setup[2]            # next state spaces
        self.depth        = float(setup[3])     # depth level
        self.gx           = float(setup[4])     # total cost until current node
        self.hx           = float(setup[5])     # heuristic cost
        self.last_op      = setup[6]            # [op,arg1,arg2,cost]
        self.stack_status = setup[7]            # {Stack: occupied space}
    
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


def belong_to_open_list(open_list, closed_list, child):
    """Checks if child exists in open_list"""
    
    if child in open_list:
        return True
    else:
        return False

