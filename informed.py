import sys
import copy
import math

from dom_indep import *
from dom_dep import *

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
                    hcost=current.hx
                    setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],hcost,["load",load,current.state_space[0],1+G.cask[load][1]],new_status]
                    new=state_node(setup)
                    return new
        else:
            return[]

    else: # O robo tem uma cask consigo_UNLOAD
        if current.last_op[0] != "load":
            load=current.state_space[1]
            if G.stack[current.state_space[0]][0]>=current.stack_status[current.state_space[0]][0]+G.cask[load][0] : # verifica se ha espaco na stack
                new_status=copy.deepcopy(current.stack_status)
                new_status[current.state_space[0]][0]=new_status[current.state_space[0]][0]+G.cask[load][0]
                new_status[current.state_space[0]][1].append(load)
                
                ss=[current.state_space[0],"",current.state_space[2]+1]

                if any (node.state_space==ss for node in (open_list + closed_list)):
                    return[]
                else:
                    hcost=current.hx
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

    new_ss=[dest,current.state_space[1],current.state_space[2]]
    hcost=gen_hx(G,new_ss,1)
    setup=[new_ss,current.state_space,[],current.depth+1,current.gx+gcost,hcost,["move",current.state_space[0],dest,gcost,hcost],current.stack_status]
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



class dijkstra_node:
    def __init__(self,node,d=10**100):
        self.node=node
        self.d=d

    def check_small(self,new_path):
        if new_path<self.d:
            self.d=new_path
    



def dijkstra (G,start):
    visited=[]
    unvisited=[]
    
    for node in G.node.keys():
        if node==start:
            n=dijkstra_node(node,0)    
        else:
            n=dijkstra_node(node)
        unvisited.append(n)

    while unvisited:
        unvisited.sort(key=lambda n: n.d, reverse=True)
        current=unvisited.pop()
        for neighbour in G.node[current.node].keys():
            for n in unvisited:
                if n.node==neighbour:
                    n.check_small(current.d+G.node[current.node][neighbour])
        visited.append(current)

    distance={}
    for n in visited:
        distance[n.node]=n.d

    return distance

def parameters_hx(G):
    global stack_loc
    global obj_cask_w
    
    for stack in G.stack.keys(): # for future heuristic functions that may need the location of tha goal cask in the stack
        casks=G.stack[stack][1]
        for cask in casks:
            if cask==sys.argv[2]:
                stack_loc=stack
    for cask in G.cask.keys():
        if cask==sys.argv[2]:
            obj_cask_w=G.cask[cask][1]


def gen_hx(G,state_space,i=1):
    if i:
        distance_toEXIT=dijkstra(G,"EXIT")
        distance_toSTACK=dijkstra(G,stack_loc)
        
        if state_space[2]==0:
            hx=(1+obj_cask_w)*distance_toEXIT[stack_loc]+distance_toSTACK[state_space[0]]       
        else:
            if state_space[1]==sys.argv[2]:
                hx=(1+obj_cask_w)*distance_toEXIT[state_space[0]]
            else:
                hx=(1+obj_cask_w)*distance_toEXIT[stack_loc]
        return hx
    else:
        return 0

    
    
def main():
    G=open_file(sys.argv[1]) #abre ficheiro e inicializa o grafo
    parameters_hx(G) #inicializa a heuristica do grafo
    
    init_stack_occupied={} #Taxa de ocupação das stacks inicial 
    for stack in G.stack.keys():
        init_stack_occupied[stack]=[0, []] #Inicializa com 0 de ocupação e com uma lista vazia de casks na stack "stack"
        for cask in G.stack[stack][1]: #para cada cask do stack
            
            init_stack_occupied[stack][0]=init_stack_occupied[stack][0]+G.cask[cask][0] 
            init_stack_occupied[stack][1].append(cask)
   
    open_list=[state_node([["EXIT","",0],[],[],0,0,gen_hx(G,["EXIT","",0],1),[],init_stack_occupied])] #Inicializa a open_list com o nó inicial
    closed_list=[]
    while 1:
        if len(open_list)==0: # Se não houver mais nós a analisar, quer dizer que o programa falhou a encontrar a solução
            return

        current=open_list.pop() #Escolhe o último nó da open_list para anailsar
        if current.state_space[0:2] == ["EXIT",sys.argv[2]]: #Se o nó tiver o state space da solução
            print_output(current,closed_list) # Escreve os passos necessários até à solução final
            return
        closed_list.append(current) #O nó analisado vai para a closed list para não ser analisado outra vez
        
        open_list=find_children(G,current,open_list,closed_list) #Adiciona os filhos do nó antigo à open list
        open_list.sort(key=lambda node: node.gx+node.hx,reverse=True) #Organiza a lista de forma a que o último elemento da lista tenha o menor f(x)

if __name__ == "__main__":
    main()
