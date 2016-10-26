import sys
import copy

class graph:
    def __init__(self):
        self.cask={} #casks characteristics
        self.stack={} #stack has what cask?
        self.node={} #nodes connections
        
    def add_cask(self,id,l,w):
        self.cask[id]=[float(l),float(w)]
        
    def add_stack(self,id,S,c=[]):
        self.stack[id]=[float(S),c]

    def add_node(self,node,neighbour,cost):
        self.node.update({node:{neighbour:float(cost)}})
        
    def add_connection(self,node,neighbour,cost):
        self.node[node].update({neighbour:float(cost)})


class state_node:
    def __init__(self,setup):
        self.state_space=setup[0] #[position,Cask,nº of loads]
        self.parent=setup[1] #previous state space
        self.children=setup[2] #next state spaces
        self.depth=float(setup[3]) #depth level
        self.gx=float(setup[4]) #total cost until current node
        self.hx=float(setup[5])
        self.last_op=setup[6]    #[op,arg1,arg2,cost]
        self.stack_status=setup[7] #{Stack: occupied space}
    
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
        print("Estimated Cost to go: ",end="")
        print(self.hx)
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

    



        
def un_load(G, current,open_list, closed_list):
    if current.state_space[1] is "": #No cask in robot-LOAD
        if current.last_op[0] != "unload":
            if current.stack_status[current.state_space[0]][1]==[]: #Se não tiver casks no stack
                return []
            else: #Se tiver casks no stack
                new_status=copy.deepcopy(current.stack_status)
                load=new_status[current.state_space[0]][1].pop()  #faz load da cask do topo da pilha          
                new_status[current.state_space[0]][0]=new_status[current.state_space[0]][0]-G.cask[load][0]
                
                
                ss=[current.state_space[0],load,current.state_space[2]+1]
                if any (node.state_space==ss for node in (open_list+closed_list)):               
                    return []
                else:
                    if current.state_space[0]==stack_loc:
                        hcost=current.hx-(1+min_w)
                    else:
                        hcost=current.hx+(1+min_w)
                    setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],hcost,["load",load,current.state_space[0],1+G.cask[load][1]],new_status]
                    new=state_node(setup)
                    return new
        else:
            return[]

    else: # O robo tem uma cask consigo_UNLOAD
        if current.last_op[0] != "load":
            load=current.state_space[1]
            print()
            print("STACK STATUS")
            print(current.stack_status)
            print()
            if G.stack[current.state_space[0]][0]>=current.stack_status[current.state_space[0]][0]+G.cask[load][0] : # verifica se ha espaco na stack
                new_status=copy.deepcopy(current.stack_status)
                new_status[current.state_space[0]][0]=new_status[current.state_space[0]][0]+G.cask[load][0]
                new_status[current.state_space[0]][1].append(load)
                
                ss=[current.state_space[0],"",current.state_space[2]+1]

                if any (node.state_space==ss for node in (open_list + closed_list)):
                    return[]
                else:
                    hcost=current.hx-(1+min_w)
                    setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],hcost,["unload",load,current.state_space[0],1+G.cask[load][1]],new_status]
                    new=state_node(setup)
                    return new
            else:
                return[]
        else:
            return[]
        
        
def move(G,current,dest,cost,open_list):
    
    if current.state_space[1]=="":
        gcost=cost
    else:
        gcost=(1+G.cask[current.state_space[1]][1])*cost
    hcost=current.hx
    print("MOVE" ,current.stack_status)
    setup=[[dest,current.state_space[1],current.state_space[2]],current.state_space,[],current.depth+1,current.gx+gcost,hcost,["move",current.state_space[0],dest,gcost,hcost],current.stack_status]
    new=state_node(setup)
    if any (node.state_space==new.state_space for node in open_list):
        for i,j in enumerate(open_list):
            
            if j.gx+j.hx>new.gx+new.hx:
                if j.state_space==new.state_space:
                    open_list.pop(i)
                    current.children=[new.state_space]
                    open_list.append(new)
                    break
    else:
        current.children=[new.state_space]
        open_list.append(new)
            
                                                                                            
def find_children(G,current,open_list,closed_list):
    children=[]
    if current.state_space[0] in G.stack.keys():
        children=un_load(G,current,open_list,closed_list)
        if children==[]:
            pass
        else:
            open_list.append(children)
            
    for neighbour in G.node[current.state_space[0]]:
        if any (node.state_space==[str(neighbour),current.state_space[1],current.state_space[2]] for node in closed_list):
            pass
        else:
            move(G,current,str(neighbour),G.node[current.state_space[0]][str(neighbour)],open_list)
            
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

    output_f=sys.argv[1].replace(".dat","")
    print(output_f)
    output_f=output_f+"_"+sys.argv[2]+".out"
    sys.stdout=open(output_f,'w')
    while commands!=[]:
        line=commands.pop()
        print(line[0],line[1],line[2],line[3])
    print(final.gx)






def hx_parameters(G):
    global ind
    global n_cask_objective
    global min_w
    global stack_loc
    min_w=-1

    for stack in G.stack.keys(): # for future heuristic functions that may need the location of tha goal cask in the stack
        casks=G.stack[stack][1]
        for cask in casks:
            if cask==sys.argv[2]:
                ind=G.stack[stack][1].index(sys.argv[2])
                n_cask_objective=len(casks)
                stack_loc=stack
    for cask in G.cask.keys():
        if G.cask[cask][1]<min_w:
            min_w=G.cask[cask][1]
            continue
        if min_w==-1:
            min_w=G.cask[cask][1]
    



    
def main():
    G=open_file(sys.argv[1])
    print()     
    print(G.cask)
    print()     
    print(G.stack)
    print()     
    print(G.node)
    
    hx_parameters(G)
    init_stack_occupied={}
    for stack in G.stack.keys():
        init_stack_occupied[stack]=[0, []]
        for cask in G.stack[stack][1]:
            
            init_stack_occupied[stack][0]=init_stack_occupied[stack][0]+G.cask[cask][0]
            init_stack_occupied[stack][1].append(cask)
   
    open_list=[state_node([["EXIT","",0],[],[],0,0,(1+min_w)*(2*(n_cask_objective-ind)-1),[],init_stack_occupied])]
    closed_list=[]
    while 1:
        #a=input("waiting: ")
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
            print("Number of nodes opened: ", end="")
            print(len(closed_list))
            print_output(current,closed_list)
            return
        closed_list.append(current)
        
        open_list=find_children(G,current,open_list,closed_list)
        open_list.sort(key=lambda node: node.gx+node.hx,reverse=True)
        
        print()
        print("Open List:")
        print("----------------------")      
        for node in open_list:
            print("{} <-- {} h= {}".format(node.state_space,node.parent,node.stack_status))    
        print("----------------------")
        print()
        print("Closed List:")
        print("----------------------")      
        for node in closed_list:
            print("{} <-- {} h= {}".format(node.state_space,node.parent,node.stack_status))    
        print("----------------------")
        
        for node in open_list:
            print(node.gx+node.hx)        
        
if __name__ == "__main__":
    main()
