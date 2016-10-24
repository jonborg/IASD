import sys

class graph:
	def __init__(self):
		self.cask={} #casks characteristics
		self.stack={} #stack has what cask?
		self.node={} #nodes connections
		
	def add_cask(self,id,l,w):
		self.cask[id]=[l,w]
		
	def add_stack(self,id,S,s,c=[]):
		self.stack[id]=[S,s,c]

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
				occupied=0
				print(w[3:len(w)])
				casks=w[3:len(w)]
				G.add_stack(w[0],w[1],occupied,casks)
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
		self.parent=setup[1] #previous state space
		self.children=setup[2] #next state spaces
		self.depth=setup[3] #depth level
		self.gx=setup[4] #total cost until current node
		self.last_op=setup[5]	#[op,arg1,arg2,cost]
	
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

	
	def find_children(self,stacks,nodes,open_list):
		if self.state_space[0] in stacks:
			print(1)
			
def un_load(G, current):
	if current.state_space[0] is "":
		load=G.stack[current.state_space[0]].pop()
		
		ss=[current.state_space[0],load,current.state_space[2]+1]
		setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],["LOAD",load,current.state_space[0],1+G.stack[load][1]]]
		state_node(new,setup)
	else:
		
		load=current.state_space[1]
		if G.stack[current.state_space[0]][0]:
			G.stack[current.state_space[0]].append(load)
			ss=[current.state_space[0],"",current.state_space[2]+1]
			setup=[ss,current.state_space,[],current.depth+1,current.gx+1+G.cask[load][1],["UNLOAD",load,current.state_space[0],1+G.stack[load][1]]]
			state_node(new,setup)
		
def move(current,dest,cost):
	setup=[[dest,current.state_space[1],current.state_space[2]],current.state_space,[],current.depth+1,current.gx+cost,["move",current.state_space[0],dest,cost]]
	new=state_node(setup)
	current.children=[new.state_space]
	return new

																						
	
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
		if len(open_list)==0:
			print ("FAILURE")
			return
		current=open_list.pop()
		if current.state_space[0:2] is ["EXIT",sys.argv[2]]:
			print (current.state_space)
			return
		closed_list.append(current)
if __name__ == "__main__":
	main()
