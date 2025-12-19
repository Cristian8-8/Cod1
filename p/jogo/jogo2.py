import pygame
from config import *

class Jogo:
    def __init__(self):
        #superficie
        self.superficie = pygame.Surface((larg_barra_lat,alt_jogo))
        self.tela = pygame.display.get_surface()
    
    def run(self):
        #cobinar superficie
        self.tela.blit(self.superficie,(tam_celula,tam_celula))