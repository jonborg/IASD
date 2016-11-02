from dom_indep import *

class graph:
    def __init__(self):
        self.cask  = {} # casks characteristics
        self.stack = {} # stack has what cask?
        self.node  = {} # nodes connections
        
    def add_cask(self,id,l,w):
        self.cask[id]=[float(l), float(w)]
        
    def add_stack(self,id,S,c=[]):
        self.stack[id]=[float(S), c]

    def add_node(self,node,neighbour,cost):
        self.node.update({node:{neighbour:float(cost)}})
        
    def add_connection(self,node,neighbour,cost):
        self.node[node].update({neighbour:float(cost)})


        
        
def open_file(file):
    """reads input file and creates graph of the problem"""
    
    G = graph()
    
    f = open(file)
    lines = f.readlines()

    for x in lines:
        w = x.split()
        i = list(x)
        if i[0] == "C": #cask
            G.add_cask(w[0], w[1], w[2])
        if i[0] == "S": #stack
            if len(w)>2:
                G.add_stack(w[0], w[1], w[2:len(w)])
            else:
                G.add_stack(w[0], w[1])
        if i[0] == "E": #edge
            if w[1] in G.node:
                G.add_connection(w[1], w[2], w[3])
            else:
                G.add_node(w[1], w[2], w[3])
                
            if w[2] in G.node:
                G.add_connection(w[2], w[1], w[3])
            else:
                G.add_node(w[2], w[1], w[3])

    f.close()    
    return G


    
    
def print_output(final, closed_list):
    """Prints results"""
    
    current = final
    commands = []
    while current.parent != []:
        commands.append(current.last_op)
        for index, item in enumerate(closed_list):
            if item.state_space == current.parent:
                break
        current = closed_list[index]

    output_f=sys.argv[1].replace(".dat","")+"_"+sys.argv[2]+".out"
    sys.stdout=open(output_f,'w')

    while commands != []:
        line = commands.pop()
        print(line[0], line[1], line[2], line[3])
    print(final.gx)


