import sys

class cask:
    def __init__(self,id,l=1,w=0):
        self.id=id
        self.l=l
        self.w=w

class stack:
    def __init__(self,id,s):
        self.id=id
        self.s=s
        self.casks=[] #list- use append to insert and pop to remove (LIFO)
        self.adjacent={}

class graph:
    def __init__(self):
        self.n_casks=0
        self.n_nodes=0

        self.casks={}
        self.nodes={}

    def add_node(self,node):
        self.nodes.append(node)
        self.n_nodes=self.n_nodes+1
        
    def add_cask(self,id,l,w):
        self.casks[id]=[l,w]
        self.n_casks=self.n_casks+1


G=graph()

print(sys.argv[1])
file=open(sys.argv[1])
lines=file.readlines()
print (lines)

for x in lines:
    
    w=x.split()
    print (w)
    i=list(x)
    print(i[0])
    if i[0]=="C": #cask
        G.add_cask(w[0],w[1],w[2])
    if i[0]=="S": #stack
        
print(G.casks)
        
        
        
