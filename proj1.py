import sys

class graph:
    def __init__(self):
        self.casks={} #casks characteristics
        self.stack={} #stack has what cask?
        self.nodes={} #nodes connections

    def add_node(self,node):
        self.nodes.append(node)
        
    def add_cask(self,id,l,w):
        self.casks[id]=[l,w]
        
    def add_stack(self,id,w,c=[]):
        self.stack[id]=[w,c]

G=graph()

file=open(sys.argv[1])
lines=file.readlines()

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

print()     
print(G.casks)
print(G.stack)
        
        
        
