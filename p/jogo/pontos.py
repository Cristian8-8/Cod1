import pygame
from config import *
class Pontos:
    def __init__(self):
        #colocar o retangulo na superfice do jogo
        self.superfice = pygame.Surface((larg_barra_lat,alt_jogo*pontos_barra_lat - tam_celula))
        #criando o retangulo
        self.bloco = self.superfice.get_rect(bottomright = (larg_janela - tam_celula,alt_janela - tam_celula))
        #pega o tamanho total da tela
        self.tela = pygame.display.get_surface()

    def run(self):
        #desenha o retangulo na tela
        self.tela.blit(self.superfice,self.bloco)