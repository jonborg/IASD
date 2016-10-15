import sys

class graph:
    def __init__(self):
        self.cask={} #casks characteristics
        self.stack={} #stack has what cask?
        self.node={} #nodes connections
        
    def add_cask(self,id,l,w):
        self.cask[id]=[l,w]
        
    def add_stack(self,id,w,c=[]):
        self.stack[id]=[w,c]

    def add_node(self,node,neighbour,cost):
        self.node.update({node:{neighbour:float(cost)}})
        
    def add_connection(self,node,neighbour,cost):
        self.node[node].update({neighbour:float(cost)})

def open_file(file):

    G=graph()

    f=open(file)
    lines=f.readlines()

    for x in lines:
        w=x.split()
        print(w)
        i=list(x)
        if i[0]=="C": #cask
            G.add_cask(w[0],w[1],w[2])
        if i[0]=="S": #stack
            if len(w)>2:
                G.add_stack(w[0],w[1],w[2:len(w)])
            else:
                G.add_stack(w[0],w[1])
        if i[0]=="E": #edge
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

class state_node:
    def __init__(self,setup):
        self.state_space=setup[0] #[position,Cask,nº of loads]
        self.parent=setup[1]
        self.children=setup[2]
        self.depth=setup[3]
        self.gx=setup[4]
        self.last_op=setup[5]    #[op,arg1,arg2,cost]

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
def move(snode,dest,cost):
    setup=[[dest,snode.state_space[1],snode.state_space[2]],snode.state_space,[],snode.depth+1,snode.gx+cost,["move",snode.state_space[0],dest,cost]]
    new=state_node(setup)
    snode.children=[new.state_space]
    return new
    
        

G=open_file(sys.argv[1])
print()     
print(G.cask)
print()     
print(G.stack)
print()     
print(G.node)

ini_list=[state_node([["EXIT","",0],[],[],0,0,[]])]

if G.node["EXIT"]["C"]:
    current=move(ini_list[0],"C",G.node["EXIT"]["C"])
ini_list.append(current)

if G.node["C"]["B"]:
    current=move(ini_list[1],"B",G.node["C"]["B"])
ini_list.append(current)

ini_list[0].show()
ini_list[1].show()
ini_list[2].show()


        
        
