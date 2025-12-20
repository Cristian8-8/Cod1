import pygame
import random
from sys import exit

class Jogo:
    def __init__(self,tam_cel):
        pygame.init()
        self.janela = pygame.display.set_mode((tam_cel*14,tam_cel*20)) # tamanho da tela
        pygame.display.set_caption("JOGO") # nome da janela
        self.Taxa_de_frames = pygame.time.Clock() # variavel dos ticks do jogo

        #cores do jogo
        self.branco = (255,255,255) # cor branca
        self.preta = (0,0,0)        # cor preta
        self.azul = (23,31,223)     # cor azul
        self.azul_c = (3,133,166)   # cor azul claro
        self.vermelho = (246,51,73) # cor vermelho
        self.cinza = (150,150,150)  # cor cinza
        self.verde = (99,209,21)    # cor verde
        self.laranja = (250,123,21) # cor laranja
        self.amarelo = (245,198,42) # cor amarelo
        self.roxo = (171,57,219)    # cor roxo
        
        
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

        self.mapa = [['', '', '', '', '', '', '', '', '', ''],  # mapa do jogo(10X20)
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
        self.proximas_forma = ['', '', '', ''] # armazena as proximas peças do jogo
        self.pontuacao = 0 # pontuaçao do jogo
        self.velocidade = 1 # velocidade do jogo
        self.forma_jogavel = 'forma_1' #formas que esta em jogo
        self.posicao_forma = [4,0] #posição da forma em jogo
        self.layout_forma = [[]] # o "desenho" da dorma em jogo
        self.nova_forma = True # quando uma nova forma aparecera
    
    def limpar_janela(self): #limpa a janela
        pygame.draw.rect(self.janela, self.preta, (0, 0, self.janela.get_width(), self.janela.get_height()))
    
    def forma_aleatoria(self): #randomiza as formas do jogo
        return "forma_" + str(random.randint(1,7)) #formata o resultado e usa o biblioteca 'random' para sortiar um numero de 1 a 7

    def inic_forma_aleatoria(self): # adiciona a forma aletoria na lista 'proximas_forma'
        for i in range(4): #percorre a lista
            self.proximas_forma[i] = self.forma_aleatoria() #adiciona as formas na lista

    def add_forma_aleatoria(self): #adicionar a uma casa a frente a forma aleatoria na variavel 'proximas_formas'
        for i in range(len(self.proximas_forma)): #percorre a lista 'self.proximas_forma'
            if i != 0: # não conta a posição 1 do loop
                self.proximas_forma[i-1] = self.proximas_forma[i] # movendo as formas para cima quando uma entra no jogo
        self.proximas_forma[i] = self.forma_aleatoria() #adiciona um nova forma na lista
        
    def add_forma_jogo(self): # adiciona o jogo uma peça
        self.forma_jogavel = self.proximas_forma[0] # substitui a peça do jogo pela proxima
        self.layout_forma = self.formas[self.forma_jogavel]['formado'] #sustitui o formado da peça
        self.add_forma_aleatoria() # chama def add_forma_aleatoria para adiciona uma forma á lista
        self.nova_forma = False # muda a variavel para que não coloque mais peças
        self.posicao_forma = [4,0] # local onde aparecera a nova forma
                
        
    def recb_cor(self, cod_cor): # essa função recebe um codigo de cor e retorna uma cor
        if cod_cor == 'R':        # se o codigo da cor for 'R' retorna a cor 'roxa'
            return self.roxo
        elif cod_cor == 'A':      # se o codigo da cor for 'A' retorna a cor 'azul'
            return self.azul
        elif cod_cor == 'C':      # se o codigo da cor for 'C' retorna a cor 'Azul Claro'
            return self.azul_c
        elif cod_cor == 'V':      # se o codigo da cor for 'V' retorna a cor 'Vermelho'
            return self.vermelho
        elif cod_cor == 'L':      # se o codigo da cor for 'L' retorna a cor 'Laranja'
            return self.laranja
        elif cod_cor == 'Y':      # se o codigo da cor for 'Y' retorna a cor 'Amarelo'. Amarelo = Y pois ja existe um 'A'
            return self.amarelo
        elif cod_cor == 'G':      # se o codigo da cor for 'G' retorna a cor 'Verde'. Verde = G pois ja existe um 'V'
            return self.verde     
        elif cod_cor == 'B':      # se o codigo da cor for 'B' retorna a cor 'Cinza'. Cinza = B pois ja existe um 'C'
            return self.cinza
        else:
            return None           # se não for nenhum dos outro retorna 'nada'
    
    def recb_codigo_cod(self, cor):        #essa função e o contrario da anterior. Essa recebe uma cor e retorna um codigo de cor
        if cor == self.roxo:              # se a cor recebida for 'roxo' vai retorna o codigo de cor 'R'
            return 'R'
        elif cor == self.azul:
            return 'A'
        elif cor == self.azul_c:
            return 'C'
        elif cor == self.vermelho:
            return 'V'
        elif cor == self.laranja:
            return 'L'
        elif cor == self.amarelo:
            return 'Y'
        elif cor == self.verde:
            return 'G'
        else:
            return None

    def desenha_formas_Jogo(self):
        for y in range(20): # percorre todas as linhas do tabuleiro
            for x in range(10): # percorre todas as coluna no tabuleiro
                if self.mapa[y][x] != '': #procura quadrados diferente de 'vazio'
                    cor = self.recb_cor(self.mapa[y][x]) # vai 'ver' a cor que esta atribuida a esse quadrado
                    cor_borda = tuple(min(rgb + 50, 255) for rgb in cor) # desenha uma borda
                    pygame.draw.rect(self.janela, cor, (self.tam_celulas * x, self.tam_celulas * y, self.tam_celulas, self.tam_celulas)) #pinta o quadrado com a cor atribuida a ele
                    pygame.draw.rect(self.janela, cor_borda, (self.tam_celulas * x, self.tam_celulas * y, self.tam_celulas, self.tam_celulas), 1) #pinta a borda do quadrado

        # desenho da peça em jogo
        posicao_forma_x = self.posicao_forma[0] # recebe a posição x da forma
        posicao_forma_y = self.posicao_forma[1] # recebe a posição y da forma
        cor = self.formas[self.forma_jogavel]['cor'] # recebe a cor do peça em jogo
        cor_borda = tuple(min(rgb + 50, 255) for rgb in cor) #desenha a borda dessa peça
        for y in range(len(self.layout_forma)): # recebe o layout da linhas da peça
            for x in range(len(self.layout_forma[0])): #recebe o layout das colunas da peça
                if self.layout_forma[y][x] == 1: # 'ver' no layout quais sao == 1 ou != 1 para saber se pinta ou não
                    pygame.draw.rect(self.janela, cor, (self.tam_celulas * (x + posicao_forma_x), self.tam_celulas * (y + posicao_forma_y), self.tam_celulas, self.tam_celulas)) # pinta o quadrado em jogo com a cor atribuida a ele
                    pygame.draw.rect(self.janela, cor_borda, (self.tam_celulas * (x + posicao_forma_x), self.tam_celulas * (y + posicao_forma_y), self.tam_celulas, self.tam_celulas), 1) #pinta a borda do quadrado
    
    #desenho o tabuleiro do jogo
    def tabuleiro(self):
        for y in range(20): # 20 linhas
            for x in range(10): # 10 colunas
                pygame.draw.rect(self.janela, self.cinza, (self.tam_celulas * x, self.tam_celulas * y, self.tam_celulas, self.tam_celulas), 1) # desenha as celulas do jogo
        pygame.draw.rect(self.janela, self.branco, (0, 0, self.tam_celulas * 10, self.tam_celulas * 20), 2) # desenha a borda do tabuleiro

        self.desenha_formas_Jogo() #desenha a peça que vai ser jogada

        #self.text_box('Next', 10, 0, 4, 1, True)
        #self.text_box('', 10, 1, 4, 13, False)
        #self.draw_next_shapes()

        #self.text_box('Score', 10, 14, 4, 1, True)
        #self.text_box(str(self.score), 10, 15, 4, 2, False)

        #self.text_box('Speed', 10, 17, 4, 1, True)
        #self.text_box(str(self.speed) + 'x', 10, 18, 4, 2, False)
        
    
    
    
        
        
        
        
        
tetris= Jogo(42)        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    tetris.Taxa_de_frames.tick(60)
    tetris.limpar_janela()
    
    if tetris.nova_forma:
        tetris.inic_forma_aleatoria()
        tetris.add_forma_jogo()
    tetris.tabuleiro()
    pygame.display.update()