from dbz import *
from cosmetico import *
from heapq import heapify
from queue import PriorityQueue
#fila de prioridade importada

#global variables
spheresToFind=list()
path=None
pathSet=False
pathCounter=0
pathEnd=None
lookingForSphere=False
oldDir=None

#Provide map point's neighbors
#determina os visinhos do ponto atual no mapa
def neighbors(map,point):
	ne=list()
	
	#Test to get neighbors inside the map
	if(point[1]>0):
		nUp=(point[0],point[1]-1)
		ne.append(nUp)
		#print("Cima",point[0],",",point[1]-1)

	if(point[1]<len(map)-1):
		nDown=(point[0],point[1]+1)
		ne.append(nDown)
		#print("Baixo",point[1])
	if(point[0]>0):
		nLeft=(point[0]-1,point[1])
		ne.append(nLeft)
		#print("Esquerda",point[1])
	if(point[0]<len(map[0])-1):
		nRight=(point[0]+1,point[1])
		ne.append(nRight)
		#print("Direita",point[1])
	return ne

#Heuristic used: Manhattan distance
#dado o ponto de inicio e o objetivo, tracassa-se a distancia de manhattan (diferenca absoluta das coordenadas).
def heuristic(start,goal):
	return ( abs(start[0]-goal[0])+abs(start[1]-goal[1]) )

#Cost to traverse each position in the map
#Dado o mapa e o ponto, esta função retorna o custo para atravessar o ponto
def costPoint(map,point):
	if(map[point[0]][point[1]]==TERRENO_GRAMA):
		return CUSTO_GRAMA
	if(map[point[0]][point[1]]==TERRENO_AGUA):
		return CUSTO_AGUA
	if(map[point[0]][point[1]]==TERRENO_MONTANHA):
		return CUSTO_MONTANHA*5

#Take AStar sequence of positions and create a sequence of instructions to follow
#Pega o ultimo no do caminho e retrassar o caminho inversamente com instruções de direção
def rebuildPath(parent,end):
	path=list()
	aux=end
	while(parent[aux] is not None):
		dir=None
		
		if(aux[1]<parent[aux][1]):
			dir=CIMA
			#print("CIMA:", aux[1],"<", parent[aux][1])
			
		if(aux[1]>parent[aux][1]):
			dir=BAIXO
			#print("Baixo:", aux[1],">", parent[aux][1])
		
		if(aux[0]>parent[aux][0]):
			dir=DIREITA
			#print("Direita:", aux[0],">", parent[aux][0])
			
		if(aux[0]<parent[aux][0]):
			dir=ESQUERDA
			#print("Esquerda:", aux[0],"<", parent[aux][0])
		
		path.append(dir)
		
		aux=parent[aux]
	
	path.reverse()
	
	return path

#Set the points for exploration	
def extremeDir(map,dir,currentPos,home):
	#          0      1      2        3     4            5           6          7
	dirMap=["norte","sul","leste","oeste","nordeste","noroeste","suldeste","suldoeste"]
	goal=None
	
	x=currentPos[0]
	y=currentPos[1]
	#print("currentPos[0]: ", currentPos[0])
	
	#get the most extreme point inside the radar
	if(dir==0):
		y-=3
				
	if(dir==1):
		y+=3
		
	if(dir==2):
		x+=3
	
	if(dir==3):
		x-=3
	
	if(dir==4):
		x+=3
		y-=3
	
	if(dir==5):
		x-=3
		y-=3
	
	if(dir==6):
		x+=3
		y+=3
	
	if(dir==7):
		x-=3
		y+=3
	#verificar posições negativas ou maior que o mapa ja definido
	if(x<0):
		x=0
	if(y<0):
		y=0
	if(x>len(map)-1):
		x=len(map)-1
	if(y>len(map)-1):
		y=len(map)-1
	
	goal=(x,y)
	
	#Small path to correct a very unlikely error situation
	#evita de ir para casa antes da hora
	if(goal==home):
				
		if(x>0):
			x-=1
		else:
			x+=1
		
		if(y>0):
			y-=1
		else:
			y+=1
		
		goal=(x,y)
	
	return goal
	
	
#Choose partial random direction
#tenta selecionar uma direcao de forma aleatoria mas limitada, seguindo uma pequena variação da direcao antiga.
def selectDir(infoDir,oldDir=None):
	#reference direction map
	dirMap=["norte","sul","leste","oeste","nordeste","noroeste","suldeste","suldoeste"]
	#norte 0
	#sul 1
	#leste 2
	#oeste 3
	#nordeste 4
	#noroeste 5
	#suldeste 6
	#suldoeste 7
	
	
	dirLimit=[
	[0,4,5], #norte
	[1,6,7], #sul
	[2,4,6], #leste
	[3,5,7], #oeste
	[0,2,4], #nordeste
	[0,3,5], #noroeste
	[1,2,6], #suldeste
	[1,3,7] #suldoeste
	]
	
	dir=0
	
	check=False
	
	#restric rotation for maximum area coverage
	if(oldDir is not None):
		for i in dirLimit[oldDir]:
			if infoDir[dirMap[i]]==1:
				check=True
				#print("infoDir[dirMap[i]]: ",infoDir[dirMap[i]] )
	
	#if valid direction found chose one close
	#se ouver uma direção valida então encontre o proximo.
	if(check):	
		while True:
			dir=dirLimit[oldDir][int(random()*3)]
			#print("dir: ", dir)
			if infoDir[dirMap[dir]]==1:
				#print("infoDir[dirMap[dir]]: ",infoDir[dirMap[dir]] )
				break;
		return dir
	
	
	#if no valid direction found try random
	#se não validar a direção encontre de forma randomica
	while True:
		dir=int(random()*8)
		#print("dir aleatoria: ", dir)
		if infoDir[dirMap[dir]]==1:
			#print("infoDir[dirMap[dir]]: ", infoDir[dirMap[dir]])
			break;
			
	return dir

#AStar algorithm to find cheapest path
def AStar(map,start,goal,goHome=False,home=None):
	success=False
	end=None
	toCheck = PriorityQueue()
	#fila de prioridade de nos para explorar

	parent ={} 
	cost={}

	#add fist point to the queue
	toCheck.put([0+heuristic(start,goal),start])
	parent[start]=None
	cost[start]=0

	while(not toCheck.empty()):
		
		current=toCheck.get()[1]
		#atual = objetivo
		if(current==goal):
			#goal reached stop path
			success=True
			end=current
			break
		
		for n in neighbors(map,current):
			if( not goHome and n == home):
				#Avoid the home location if indicated
				#evitar localizacao da casa
				continue
			
			#Calculate g cost
			newCost=costPoint(map,n)+cost[current]				
						
			if n not in cost or newCost<cost[n]:  
				#if new node add it to the queue
				#verificar o custo de uma determinada posição, se for menor adicione na fila.
				cost[n]=newCost
				#print ("n / cost[n]:", n, " / ",cost[n])
				f=cost[n]+heuristic(n,goal)
				#print ("heuristic(n,goal):", heuristic(n,goal))
				parent[n]=current
				#print ("f, n: ",f,", ", n)
				toCheck.put([f,n])
		
		if(toCheck.empty()):
			#If no path found finisth here with error
			end=current
		
	if(success):
		#successful run, return data
		return {
			"success":True,
			"path":rebuildPath(parent,end),
			"cost":cost[end]
			}
	else:
		#unsuccessfull run, return data
		return {
			"success":False,
			"path":rebuildPath(parent,end),
			"cost":cost[end]
			}

#Fully integrated agent
def sphereFinder(info):
	# reference direction map dirMap=["norte","sul","leste","oeste","nordeste","noroeste","suldeste","suldoeste"]
	
	#Set Global Variables
	global spheresToFind
	global path
	global pathSet
	global pathCounter
	global pathEnd
	global lookingForSphere
	global oldDir
		
	currentPos=(info["pos"][0],info["pos"][1])
	#print("pos em tupla: ",info["pos"][0],",",info["pos"][1])
	
	#adicionar novas esferar no radar se tiver
	if(len(info["radar-proximo"])>0):
		#If there is new spheres in the radar add them
		for i in info["radar-proximo"]:
			if i not in spheresToFind:
				spheresToFind.append(i)
	
	#se a posição atual for igual o caminho atingido, retire da lista
	if(lookingForSphere and currentPos==pathEnd):
		#If destination is reached, take it out of the list
		print("Sphere found!")
		pathSet=False
		lookingForSphere=False
		spheresToFind.remove(currentPos)
	
	#se tiver explorando e encontrar uma esfera pare de explorar
	if(not lookingForSphere and pathSet and len(spheresToFind)>0):
		#If exploring and find sphere, stop exploring
		pathSet=False
	#se tiver explorando e não encontrar uma esfera continue explorando
	if(not lookingForSphere and pathSet and currentPos==pathEnd):
		#If exploring and no sphere, continue exploring
		pathSet=False
		
	if(not pathSet):
		#If we need to set a destiny
		if(len(spheresToFind)>0):
			#Set a search for one Sphere
			spheresDistances=PriorityQueue()
			for s in spheresToFind:
				pointAStar=AStar(info["mapa"],currentPos,s,False,info["casa-kame"])
				spheresDistances.put([pointAStar["cost"],s])
				#print(info["mapa"])
			
			#choose the closest sphere and look for it
			#escolher a esfera mais proxima e procure por ela
			destinyPoint=spheresDistances.get()[1]
			destinyAStar=AStar(info["mapa"],currentPos,destinyPoint,False,info["casa-kame"])
			
			#set search global variables
			pathEnd=destinyPoint
			path=destinyAStar["path"]
			pathSet=True
			pathCounter=0
			lookingForSphere=True
		elif(info["esferas"]==0):
			#return home
			print("GO HOME!")
			#voltar para casa do kame apos nao ter mais esferas 
			destinyAStar=AStar(info["mapa"],currentPos,info["casa-kame"],True)
			# set global search variables
			pathEnd=info["casa-kame"]
			path=destinyAStar["path"]
			pathSet=True
			pathCounter=0
			lookingForSphere=False
		else:
			#exploration mode

				#choose a direction and follow it
				#escolhe uma direcao e siga-a
			dir=selectDir(info["radar-direcao"],oldDir)
			oldDir=dir
			goal=extremeDir(info["mapa"],dir,currentPos,info["casa-kame"])
							
			destinyAStar=AStar(info["mapa"],currentPos,goal,False,info["casa-kame"])
			#set global search variables
			pathEnd=goal
			path=destinyAStar["path"]
						
			pathSet=True
			pathCounter=0
			lookingForSphere=False
		
	if pathSet and pathCounter<len(path):
		#print("Path:", path)
		#siga o caminho
		#follow the path
		dir=path[pathCounter]
		pathCounter+=1
		return dir
	
	
#Main execution	
if __name__ == "__main__":
	dbz = DragonBallZ(sphereFinder,93,17993)
	executar_jogo(dbz)