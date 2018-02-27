#!/usr/bin/python3
#-*-encoding:utf8-*-

from random import seed,random
from math import sin,cos,sqrt,degrees,atan2
from copy import deepcopy

"""
IMPLEMENTAÇÃO DO PROBLEMA DE BUSCA POR CAMINHO DBZ
"""

CIMA = 1
BAIXO = 2
ESQUERDA = 3
DIREITA = 4

#CIMA = 1
#BAIXO = 3
#ESQUERDA = 4
#DIREITA = 2

CUSTO_GRAMA = 1
CUSTO_AGUA = 10
CUSTO_MONTANHA = 35

TERRENO_GRAMA = 1
TERRENO_AGUA = 2
TERRENO_MONTANHA = 3

#!!!MODIFICADA!!!
def dentro_quadrado(ls,li,p):
	"""
	Verifica se o ponto p está dentro do
	quadrado formado formado por ls e li

	@param ls: Limite Superior do quadrado
	@param li: Limite Inferior do quadrado
	@param p: Ponto a ser avaliado
	@return: True se o ponto estiver dentro do quadrado
	"""
	return li[0] >= p[0] and li[1] >= p[1] and ls[0] <= p[0] and ls[1] <= p[1]


class DragonBallZ:
	"""Classe de controle do problema"""

	def __init__(self,agente,tamanho=50,semente=None):
		"""
		Construtor da classe

		@param agente: Função do Agente
		@param tamanho: Tamanho do mapa
		@param semente: Semente aleatória (None utiliza a semente default)
		"""

		self.agente = agente
		self.tamanho = tamanho

		if semente is not None:
			seed(semente)

		#
		# PASSO 1: GERA A POSIÇÃO NO MAPA DAS ESFERAS E DA CASA DO KAME
		#
		self.casa_kame = (int(random()*tamanho),int(random()*tamanho))
		self.esferas = list()

		# Gera a posição das esferas
		while len(self.esferas) < 7:
			pos = (int(random()*tamanho),int(random()*tamanho))

			if pos != self.casa_kame and pos not in self.esferas:
				self.esferas.append(pos)


		#
		# PASSO 2: GERA O MAPA
		#
		termos = [random() for _ in range(6)]
		self.mapa = [ [None] * tamanho for _ in range(tamanho) ]

		for x in range(tamanho):
			for y in range(tamanho):
				z = sin(termos[0]*x**2+termos[1]*y+termos[2]) + cos(termos[3]*y**2+termos[4]*x+termos[5])

				if z < -.5: self.mapa[x][y] = 1
				elif z < .5: self.mapa[x][y] = 2
				else: self.mapa[x][y] = 3 

		#
		# PASSO 3: INICIALIZA POSIÇÃO INICIAL DO AGENTE E CONTADOR DE ITERAÇÕES
		#
		self.agente_pos = list(self.casa_kame)
		self.iteracao = 0
		self.custo = 0

	def executar(self):
		"""
		Executa uma iteração do problema,
		a implementação será uma list comprehension 
		para facilitar no uso da GUI
		"""

		#
		# COMPUTA AS INFORMAÇÕES DO RADAR
		#
		radar_direcao = {
			"norte":0,
			"sul":0,
			"leste":0,
			"oeste":0,
			"nordeste":0,
			"noroeste":0,
			"suldeste":0,
			"suldoeste":0
		}
		radar_proximo = list()
		limite_sup = (self.agente_pos[0]-3,self.agente_pos[1]-3)
		limite_inf = (self.agente_pos[0]+3,self.agente_pos[1]+3)

		for p in self.esferas:
			if dentro_quadrado(limite_sup,limite_inf,p):
				radar_proximo.append(p)
			else:
				angulo = degrees(atan2((self.agente_pos[1]-p[1]),(p[0]-self.agente_pos[0])))

				#MODIFICADA if angulo < 0: angulo = 180.0-angulo
				
				if angulo < 0:
					angulo = 360+angulo
				
				if angulo < 22.5 or angulo > 337.5 : radar_direcao["leste"]=1
				elif angulo < 67.5: radar_direcao["nordeste"]=1
				elif angulo < 112.5: radar_direcao["norte"]=1
				elif angulo < 157.5: radar_direcao["noroeste"]=1
				elif angulo < 202.5: radar_direcao["oeste"]=1
				elif angulo < 247.5: radar_direcao["suldoeste"]=1
				elif angulo < 292.5: radar_direcao["sul"]=1
				else: radar_direcao["suldeste"]=1

		# Verifica se o agente voltou para a casa do kame
		if self.custo > 0 and tuple(self.agente_pos) == self.casa_kame:
			if len(self.esferas) > 0: raise Exception("O Objetivo do jogo não foi cumprido!")
			else: raise Exception("Você pegou todas as esferas!\nCusto Total: %d\nCusto/Iteração: %g"%(self.custo,float(self.custo)/self.iteracao))

		#
		# INVOCA O AGENTE E VALIDA RETORNO
		#
		direcao = self.agente({
			"pos":deepcopy(self.agente_pos),
			"radar-proximo":radar_proximo,
			"radar-direcao":radar_direcao,
			"mapa":deepcopy(self.mapa),
			"casa-kame":deepcopy(self.casa_kame),
			"esferas":len(self.esferas),
			#MODIFICADA
			"esferas-pos":deepcopy(self.esferas)
			
		})
		
		if type(direcao) is not int or direcao < 1 or direcao > 4: print(direcao);raise Exception("Direcao Inválida!")

		if direcao == CIMA and self.agente_pos[1] == 0: raise Exception("Não é possível passar o limite superior do mapa")

		if direcao == BAIXO and self.agente_pos[1] == self.tamanho-1: raise Exception("Não é possível passar o limite inferior do mapa")

		if direcao == ESQUERDA and self.agente_pos[0] == 0: raise Exception("Não é possível passar o limite da esquerda no mapa")

		if direcao == DIREITA and self.agente_pos[0] == self.tamanho-1: raise Exception("Não é possível passar o limite da direita no mapa")

		# Atualiza custo
		if self.mapa[self.agente_pos[0]][self.agente_pos[1]] == TERRENO_GRAMA: self.custo += CUSTO_GRAMA
		elif self.mapa[self.agente_pos[0]][self.agente_pos[1]] == TERRENO_MONTANHA: self.custo += CUSTO_MONTANHA
		else: self.custo += CUSTO_AGUA

		# Atualiza posição do agente
		if direcao == CIMA: self.agente_pos[1]-=1
		elif direcao == BAIXO: self.agente_pos[1]+=1
		elif direcao == ESQUERDA: self.agente_pos[0]-=1
		else: self.agente_pos[0]+=1

		# Verifica se o agente encontrou uma esfera do dragão
		if tuple(self.agente_pos) in self.esferas:
			self.esferas.remove(tuple(self.agente_pos))

		# Incrementa iteracao
		self.iteracao+=1