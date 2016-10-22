import sys
import time
import graph


def unload(G, current,open_list, closed_list):
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
	children = []
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
	
	
	

def choose_next_node(open_list, algorithm):	

	if len(open_list)==1: return open_list.pop()
	
	if algorithm == 'BFS':
		total_cost = 0
		for ch in open_list:
			total_cost += ch. ?????
		
	



def main()
	G=open_file(sys.argv[1])
	print()
	print(G.cask)
	print()
	print(G.stack)
	print()
	print(G.node)
	
	algorithm = 'BFS'
	
	open_list=[state_node([["EXIT","",0],[],[],0,0,[]])]	# comeca em EXIT, sem cask
	closed_list=[]
	
	while 1:
		
		if len(open_list)==0:	# if empty(frontier) return failure
			print ("FAILURE")
			return
		
		
		#current=open_list.pop()	#TODO: choose the lowest cost node in frontier
		current = choose_next_node(open_list, algorithm)
		print()
		print (current.state_space)
		
		# test if goal
		if current.state_space[0:2] == ["EXIT",sys.argv[2]]:	# win
			print()
			print("FINISH!!!")
			print(current.state_space)
			print_output(current,closed_list)
			return
			
		# add node to explored
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
		
		# add children to open_list
		open_list=find_children(G,current,open_list,closed_list)
		
		
if __name__ == "__main__":
	main()
