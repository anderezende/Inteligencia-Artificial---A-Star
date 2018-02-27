from dbz import *
from cosmetico import *

destino=[None,None]
destinoSet=False
caminho=list()
caminhoPos=None
oldDir=ESQUERDA
retornar=False

caminhoTest=[CIMA,CIMA,DIREITA,BAIXO,ESQUERDA,ESQUERDA,CIMA]

def dummy_agent(info):
	#while True:
	#	continue
	
	print(info["mapa"])
	print(info["radar-proximo"])
	print(info["pos"])
	
	currentPos=info["pos"]
	
	#info["radar-proximo"]
	#info["radar-direcao"]
	#info["mapa"]
	#info["casa-kame"]
	#info["esferas"]
	
	global destino
	global destinoSet
	global caminho
	global caminhoPos
	global oldDir
	global retornar
	
	limit=3
	
	#print( info["radar-proximo"])
	#print(len(info["radar-proximo"]))
	
	
	if(info["esferas"]==0):
		retornar=True
		destino[0]=info["casa-kame"][0]
		destino[1]=info["casa-kame"][1]
		
	
	if(retornar):
		if(destino[1]<currentPos[1]):
			dir=CIMA
		
		if(destino[1]>currentPos[1]):
			dir=BAIXO
			

		if(destino[0]<currentPos[0]):
			dir=ESQUERDA
			

		if(destino[0]>currentPos[0]):
			dir=DIREITA
		
		return dir
	
		
	if(not destinoSet):
		if(len(info["radar-proximo"])>0):
			sl=int(random()*len(info["radar-proximo"]))
			destino[0]=info["radar-proximo"][sl][0]
			destino[1]=info["radar-proximo"][sl][1]
			destinoSet=True
			
			caminho.clear()
			caminhoPos=0
			
			if(destino[1]<currentPos[1]):
				print("Esfera em cima")
				for _ in range(0,currentPos[1]-destino[1]):
					caminho.append(CIMA)
			
			if(destino[1]>currentPos[1]):
				print("Esfera em baixo")
				for _ in range(0,destino[1]-currentPos[1]):
					caminho.append(BAIXO)
			
			if(destino[0]<currentPos[0]):
				print("Esfera a esquerda")
				for _ in range(0,currentPos[0]-destino[0]):
					caminho.append(ESQUERDA)
			
			if(destino[0]>currentPos[0]):
				print("Esfera a direita")
				for _ in range(0,destino[0]-currentPos[0]):
					caminho.append(DIREITA)
					
			dir=caminho.pop(0)
			
		else:
			while True:
				dir=int(random()*4)+1
				
				x=info["pos"][0]
				y=info["pos"][1]
			
				
				if(dir==CIMA):
					y=y-1
				elif(dir==DIREITA):
					x=x+1
				elif(dir==BAIXO):
					y=y+1
				elif(dir==ESQUERDA):
					x=x-1
				
				if(x==info["casa-kame"][0] and y==info["casa-kame"][1] and info["esferas"]>0):
					continue
				
				if(x<0 or y<0 or x>9 or y>9):
					continue
				
				if(dir==oldDir):
					continue
				
				if((oldDir==ESQUERDA and dir==DIREITA) or (oldDir==DIREITA and dir==ESQUERDA) or (oldDir==CIMA and dir==BAIXO) or (oldDir==BAIXO and dir==CIMA)):
					continue
					
				oldDir=dir
				break
		
		
		
	else:
		print("Tracking "+str(destino))
		dir=caminho.pop(0)
		
		x=info["pos"][0]
		y=info["pos"][1]
	
		
		if(dir==CIMA):
			y=y-1
		elif(dir==DIREITA):
			x=x+1
		elif(dir==BAIXO):
			y=y+1
		elif(dir==ESQUERDA):
			x=x-1
		
		
		if(destino[0]==x and destino[1]==y):
			destinoSet=False
		
		
	return dir

def moreDummyAgent(info):
	global caminhoTest
	dir=caminhoTest.pop(0)
	return dir

	
if __name__ == "__main__":
	dbz = DragonBallZ(dummy_agent,10,1)
	executar_jogo(dbz)
