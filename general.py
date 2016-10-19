import sys
import time

class graph:
    def __init__(self):
        self.cask={} #casks characteristics
        self.stack={} #stack has what cask?
        self.node={} #nodes connections
        
    def add_cask(self,id,l,w):
        self.cask[id]=[float(l),float(w)]
        
    def add_stack(self,id,S,s=0,c=[]):
        self.stack[id]=[float(S),float(s),c]

    def add_node(self,node,neighbour,cost):
        self.node.update({node:{neighbour:float(cost)}})
        
    def add_connection(self,node,neighbour,cost):
        self.node[node].update({neighbour:float(cost)})


class state_node:
    def __init__(self,setup):
        self.state_space=setup[0] #[position,Cask,nº of loads]
        self.parent=setup[1] #previous state space
        self.children=setup[2] #next state spaces
        self.depth=setup[3] #depth level
        self.gx=setup[4] #total cost until current node
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
                occupied=0
                for C in w[2:len(w)]:
                    occupied=occupied+G.cask[C][0]
                G.add_stack(w[0],w[1],occupied,w[2:len(w)])
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

    



        
def un_load(G, current,open_list, closed_list):
    if current.state_space[1] is "": #No cask in robot
        if G.stack[current.state_space[0]][2]==[]: #Se não tiver casks no stack
            return []
        else: #Se tiver casks no stack
            load=G.stack[current.state_space[0]][2].pop()  #faz load da cask do topo da pilha          
            ss=[current.state_space[0],load,current.state_space[2]+1]
            if any (node.state_space==ss for node in (open_list+closed_list)):
                G.stack[current.state_space[0]].append(load)
                return []
            else:
                print(load)
                setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],["load",load,current.state_space[0],1+G.cask[load][1]]]
                new=state_node(setup)
                return new
    else: # O robo tem uma cask consigo
        load=current.state_space[1]
        if G.stack[current.state_space[0]][0]>G.stack[current.state_space[0]][1]+G.cask[load][0]: # verifica se ha espaco na stack
            G.stack[current.state_space[0]].append(load)
            ss=[current.state_space[0],"",current.state_space[2]+1]
            if any (node.state_space==ss for node in (open_list + closed_list)):
                G.stack[current.state_space[0]].pop()
                return[]
            else:    
                setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],["unload",load,current.state_space[0],1+G.cask[load][1]]]
                new=state_node(setup)
                return new
        else:
            return[]
        
        
def move(G,current,dest,cost):
    if current.state_space[1]=="":
        tcost=cost
    else:
        tcost=(1+G.cask[current.state_space[1]][1])*cost
    setup=[[dest,current.state_space[1],current.state_space[2]],current.state_space,[],current.depth+1,current.gx+tcost,["move",current.state_space[0],dest,tcost]]
    new=state_node(setup)
    current.children=[new.state_space]
    return new

                                                                                        
def find_children(G,current,open_list,closed_list):
    children=[]
    if current.state_space[0] in G.stack.keys():
        children=un_load(G,current,open_list,closed_list)
        if children==[]:
            pass
        else:
            open_list.append(children)
            
    for neighbour in G.node[current.state_space[0]]:
        children=[]
        if any (node.state_space==[str(neighbour),current.state_space[1],current.state_space[2]] for node in (open_list + closed_list)):
            
            pass
        else:
            children=move(G,current,str(neighbour),G.node[current.state_space[0]][str(neighbour)])
            open_list.append(children)
    return open_list


def print_output(final,closed_list):
    current=final
    commands=[]
    total=0
    while current.parent !=[]:
        commands.append(current.last_op)
        for index, item in enumerate(closed_list):
            if item.state_space == current.parent:
                break
        current=closed_list[index]
    sys.stdout=open('results.txt','w')
    while commands!=[]:
        line=commands.pop()
        print(line)
    print(final.gx)




    
def main():
    G=open_file(sys.argv[1])
    print()     
    print(G.cask)
    print()     
    print(G.stack)
    print()     
    print(G.node)


    open_list=[state_node([["EXIT","",0],[],[],0,0,[]])]
    closed_list=[]
    while 1:
        #time.sleep(5)
        if len(open_list)==0:
            print()
            print("FAILURE")
            return
        current=open_list.pop()
        print()
        print (current.state_space)
        if current.state_space[0:2] == ["EXIT",sys.argv[2]]:
            print()
            print("FINISH!!!")
            print(current.state_space)
            print_output(current,closed_list)
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
