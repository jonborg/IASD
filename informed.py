import sys
import copy

from dom_indep import *
from dom_dep import *

        
def un_load(G, current,open_list, closed_list):
    """load cask to robot or unload cask to a given stack
    unable to unload on a stack without room for the cask
    unable to load from an empty stack"""
    
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
    """move robot from current location to adjacent node"""
    
    if current.state_space[1]=="":
        gcost=cost
    else:
        gcost=(1+G.cask[current.state_space[1]][1])*cost
    hcost=current.hx
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
    """Appends children from current node to open_list,
    as per the general search algorithm"""
    
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
    
    hx_parameters(G)
    init_stack_occupied={}
    for stack in G.stack.keys():
        init_stack_occupied[stack]=[0, []]
        for cask in G.stack[stack][1]:
            init_stack_occupied[stack][0]=init_stack_occupied[stack][0]+G.cask[cask][0]
            init_stack_occupied[stack][1].append(cask)
   
    open_list = [state_node([["EXIT","",0],[],[],0,0,(1+min_w)*(2*(n_cask_objective-ind)-1),[],init_stack_occupied])]
    closed_list = []

    while 1:
        
        if len(open_list)==0:
            return
            
        current=open_list.pop()
        
        if current.state_space[0:2] == ["EXIT",sys.argv[2]]:
            print_output(current,closed_list)
            return
            
        closed_list.append(current)
        
        open_list=find_children(G,current,open_list,closed_list)
        open_list.sort(key=lambda node: node.gx+node.hx,reverse=True)
        
        
if __name__ == "__main__":
    main()
