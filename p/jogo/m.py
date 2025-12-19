
import pygame
from pygame.locals import *
from sys import exit
from pontos import Pontos
from config import *
from jogo2 import Jogo

class inicial:
    def __init__(self):
        #inicia o jogo
        pygame.init()
        #tamanho da tela
        self.tela = pygame.display.set_mode((larg_janela,alt_janela))
        #nome na janela do jogo
        pygame.display.set_caption("JOGO")
        #variavel do ticks do jogo
        self.Taxa_de_frames = pygame.time.Clock()
        #variavel que chama a classe que esta no arquivvo "jogo2"
        self.jogo = Jogo()
        self.pontos = Pontos()
        
    def exe_jogo(self):
        while True:
            #taxa de ticks
            self.Taxa_de_frames.tick(60)
            #objetos na tela
            self.tela.fill((125,125,125))
            self.jogo.run()
            self.pontos.run()
            
            
            
            #fecha o jogo
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit() 
            pygame.display.update()
            
#roda o jogo                        
if __name__ == "__main__":
    game = inicial()
    game.exe_jogo()