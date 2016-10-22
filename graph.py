class graph:
	def __init__(self):
		self.cask  = {}	# casks characteristics
		self.stack = {}	# stack has what cask?
		self.node  = {}	# nodes connections
		
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
		self.state_space = setup[0]		# [position,Cask,nº of loads]
		self.parent 	 = setup[1]		# previous state space
		self.children 	 = setup[2]		# next state spaces
		self.depth 		 = setup[3]		# depth level
		self.gx 		 = setup[4]		# total cost until current node
		self.last_op 	 = setup[5]		# [op,arg1,arg2,cost]
	
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

