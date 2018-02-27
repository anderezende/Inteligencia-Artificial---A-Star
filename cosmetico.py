#!/usr/bin/python3
#-*-encoding:utf8-*-

from pygame import *
from sys import exit
from os import path,environ

"""
FIRULAS DE GUI
"""

from dbz import *

def executar_jogo(dbz):
	"""Executa a GUI do Jogo pelo PyGame"""
	init() # Inicializa o pygame

	environ["SDL_VIDEO_CENTERED"] = "1"
	agua = Color(0,137,255)
	montanha = Color(161, 79, 79)
	grama = Color(80,181,37)
	gohan = image.load(path.join("gohan.png"))
	kame_house = image.load(path.join("kame_house.png"))
	sphere = image.load(path.join("sphere.png"))
	screen = display.set_mode((612,612),0,32)
	delay = 150
	clock = time.Clock()

	# Inicia musica
	mixer.music.load("theme.mp3")
	mixer.music.play(-1)

	while True:
		for e in event.get():
			if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
				exit(0)

		# Desenha o Fundo
		screen.fill(Color(0,0,0))

		# Delay
		delay -= clock.tick()

		if delay < 0:
			dbz.executar()
			delay = 75 #150
			display.set_caption("DBZ - Custo total: "+str(dbz.custo)+", Iterações: "+str(dbz.iteracao))

		# Desenha o mapa
		for x,i in enumerate(range(-8,9)):
			for y,j in enumerate(range(-8,9)):
				p = (dbz.agente_pos[0]+i,dbz.agente_pos[1]+j)

                # Range gerado está dentro do mapa?
				if p[0] >= 0 and p[0] < dbz.tamanho and p[1] >= 0 and p[1] < dbz.tamanho:
					cor = agua

					if dbz.mapa[p[0]][p[1]] == TERRENO_MONTANHA: cor = montanha
					elif dbz.mapa[p[0]][p[1]] == TERRENO_GRAMA: cor = grama

					draw.rect(screen,cor,rect.Rect((x*36,y*36),(36,36)))

                    # Verifica se irá desenhar a casa do mestre Kame
					if p == dbz.casa_kame: screen.blit(kame_house,rect.Rect((x*36+5,y*36),(36,36)))

                    # Verifica se irá desenhar uma esfera do dragão
					if p in dbz.esferas: screen.blit(sphere,rect.Rect((x*36+6,y*36+8),(36,36)))

		# Desenha o gohan
		screen.blit(gohan,rect.Rect((294,288),(36,36)))

		# Desenha o quadro do radar próximo
		draw.lines(screen,Color(255,0,0),True,[(180,180),(180,432),(432,432),(432,180)],1)
		
		# Atualiza a tela
		display.update()





