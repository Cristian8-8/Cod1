import pygame
import random
from sys import exit

class Jogo:
    def __init__(self,tam_cel):
        pygame.init()
        self.janela = pygame.display.set_mode((tam_cel*14,tam_cel*20)) # tamanho da tela
        pygame.display.set_caption("JOGO") # nome da janela
        self.Taxa_de_frames = pygame.time.Clock() # variavel dos ticks do jogo

        
        self.branco = (255, 255, 255)# cor branca
        self.preta = (  0,   0,   0) # cor preta
        self.azul = ( 23,  31, 223) # cor azul
        self.azul_c = (  3, 133, 166) # cor azul claro
        self.vermelho = (246,  51,  73) # cor vermelho
        self.cinza = (150, 150, 150) # cor cinza
        self.verde = ( 99, 209,  21) # cor verde
        self.laranja = (250, 123,  21) # cor laranja
        self.amarelo = (245, 198,  42) # cor amarelo
        self.roxo = (171,  57, 219) # cor roxo
        
        
        # peças do jogo
        self.formas = {
            'forma_1': {
                'formado': [[1, 1],
                            [1, 1]],
                'cor': self.amarelo
            },
            'forma_2': {
                'formado':[[0, 1, 0],
                           [1, 1, 1]],
                'cor': self.roxo
            },
            'forma_3': {
                'formado': [[1, 1, 1, 1]],
                'cor': self.azul_c
            },
            'forma_4': {
                'formado':[[1, 1, 0],
                           [0, 1, 1]],
                'cor': self.vermelho
            },
            'forma_5': {
                'formado':[[0, 1, 1],
                           [1, 1, 0]],
                'cor': self.verde
            },
            'forma_6': {
                'formado':[[1, 0, 0],
                           [1, 1, 1]],
                'cor': self.azul
            },
            'forma_7': {
                'formado':[[0, 0, 1],
                           [1, 1, 1]],
                'cor': self.laranja
            }
        }

        self.mapa = [['', '', '', '', '', '', '', '', '', ''],  # mapa do jogo
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', ''],
                    ['', '', '', '', '', '', '', '', '', '']]


        self.sort_1peças = True # primerias peças do jogo
        self.exibi_restart = True # mostra o butao restart
        self.tam_celulas = tam_cel # tamalho das celulas do jogo
        self.proximas_pecas = ['', '', '', ''] # armazena as proximas peças do jogo
        self.pontuacao = 0 # pontuaçao do jogo
        self.velocidade = 1 # velocidade do jogo
        self.forma_jogavel = 'forma_1' #formas que esta em jogo
        self.posicao_forma = [4, 0] #posição da forma em jogo
        self.layout_forma = [[]] # o "desenho" da dorma em jogo
        self.nova_forma = True # quando uma nova forma aparecera
        
    def limpar_janela(self): #limpa a janela
        pygame.draw.rect(self.janela, self.preta, (0, 0, self.janela.get_width(), self.janela.get_height()))
        
        
        
        
        
        
        
        
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pygame.quit()
            exit()
    tetris.clock.tick(60)
    tetris.clear_window()