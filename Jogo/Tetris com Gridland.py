import pygame
import random
import time 
from sys import exit

class Jogo:
    def __init__(self,tam_cel):
        pygame.init()
        self.janela = pygame.display.set_mode((tam_cel*14,tam_cel*20)) # tamanho da tela
        pygame.display.set_caption("JOGO") # nome da janela
        self.Taxa_de_frames = pygame.time.Clock() # variavel dos ticks do jogo
        self.tempo = 0 # tempo do jogo
        self.font = pygame.font.Font(None, 36) # fonte para o texto

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
        self.exibi_restart = False # mostra o butao restart
        self.tam_celulas = tam_cel # tamalho das celulas do jogo
        self.proximas_forma = ['', '', '', ''] # armazena as proximas peças do jogo
        self.pontuacao = 0 # pontuaçao do jogo
        self.velocidade = 1 # velocidade do jogo
        self.forma_jogavel = 'forma_1' #formas que esta em jogo
        self.posicao_forma = [4,0] #posição da forma em jogo
        self.layout_forma = [[]] # o "desenho" da dorma em jogo
        self.nova_forma = True # quando uma nova forma aparecera
        self.forma_reserva = None #reserva (hold) de peça: None significa sem reserva
        self.hold_usado = False # impede varias peças reservas na mesma rodada
    
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
        
    def guarda_forma(self):
        """Guarda a peça atual na reserva (hold) ao apertar 'c'.
        Regras simples:
        - Se não houver peça reserva, move a peça atual para a reserva e puxa a próxima.
        - Se já houver uma reserva, troca a peça reserva pela atual.
        - Só permite uma operação de hold por queda (usa `self.hold_usado`).
        """
        if self.hold_usado:
            return  # já usou hold nesta queda

        # se não existe peça na reserva: guarda a atual e pega próxima
        if self.forma_reserva is None:
            self.forma_reserva = self.forma_jogavel
            # solicita nova forma (puxa a próxima)
            self.nova_forma = True
            self.add_forma_jogo()
        else:
            # troca a forma atual com a reserva
            antiga = self.forma_jogavel
            self.forma_jogavel = self.forma_reserva
            self.forma_reserva = antiga
            # atualiza layout e posição da peça atual
            self.layout_forma = self.formas[self.forma_jogavel]['formado']
            self.posicao_forma = [4, 0]

        # marca que hold foi usado até a peça ser bloqueada
        self.hold_usado = True
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
    
    def recb_codigo_cod(self, cor):        # essa função e o contrario da anterior. Essa recebe uma cor e retorna um codigo de cor
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

    #def desenha_formas_Jogo(self):
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
    

    def tabuleiro(self):# desenha o tabuleiro do jogo
        tabuleiro_L = self.tam_celulas * 10 # largura do tabuleiro
        tabuleiro_A = self.tam_celulas * 20 # altura do tabuleiro
        # calcula top_h para caber na janela (não empurrar o tabuleiro para fora)
        altura_maxima = self.janela.get_height() - tabuleiro_A # calcula a altura máxima da tela
        topo_largura = min(self.tam_celulas * 3, max(0, altura_maxima)) # define a margem superior do tabuleiro

        x_tabuleiro = (self.janela.get_width() - tabuleiro_L) // 2 # centraliza horizontalmente
        y_tabuleiro = topo_largura # define a margem superior do tabuleiro
        
        pygame.draw.rect(self.janela, self.preta, (x_tabuleiro, 0, tabuleiro_L, topo_largura)) # pinta a área acima do tabuleiro de preto
        for y in range(20): # percorre todas as linhas do tabuleiro
            for x in range(10): # percorre todas as coluna no tabuleiro
                rx = x_tabuleiro + self.tam_celulas * x # calcula a posição x do retângulo
                ry = y_tabuleiro + self.tam_celulas * y # calcula a posição y do retângulo
                
                pygame.draw.rect(self.janela, self.branco, (rx, ry, self.tam_celulas, self.tam_celulas), 1) # desenha grade do tabuleiro
                
                if self.mapa[y][x] != '': #procura quadrados diferente de 'vazio'
                    cor = self.recb_cor(self.mapa[y][x]) # vai 'ver' a cor que esta atribuida a esse quadrado
                    pygame.draw.rect(self.janela, cor, (rx, ry, self.tam_celulas, self.tam_celulas)) #pinta o quadrado com a cor atribuida a ele

        pygame.draw.rect(self.janela, self.branco, (x_tabuleiro, y_tabuleiro, tabuleiro_L, tabuleiro_A), 2) # desenha a borda do tabuleiro

        posicao_forma_x = self.posicao_forma[0] # posição x da forma em jogo
        posicao_forma_y = self.posicao_forma[1] # posição y da forma em jogo
        cor = self.formas[self.forma_jogavel]['cor'] # cor da peça em jogo
        for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
            for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                if self.layout_forma[y][x] == 1: #se o layout da forma for == 1
                    rx = x_tabuleiro + self.tam_celulas * (x + posicao_forma_x) # calcula a posição x do retângulo da peça em jogo
                    ry = y_tabuleiro + self.tam_celulas * (y + posicao_forma_y) # calcula a posição y do retângulo da peça em jogo
                    pygame.draw.rect(self.janela, cor, (rx, ry, self.tam_celulas, self.tam_celulas)) #pinta o quadrado em jogo com a cor atribuida a ele
              
    def colisao_lateral(self): #verifica se teve colisão lateral
        posicao_forma_x = self.posicao_forma[0] #localização x da forma em jogavel
        posicao_forma_y = self.posicao_forma[1] #localização y da forma em jogavel
        for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
            for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                if self.layout_forma[y][x] == 1: #se o layout da forma for == 1
                    forma_tab_pos_x = posicao_forma_x + x # adiciona a posição x da forma com a posição x do layout no tabuleiro
                    forma_tab_pos_y = posicao_forma_y + y # adiciona a posição y da forma com a posição y do layout no tabuleiro
                    if  self.mapa[forma_tab_pos_y][forma_tab_pos_x] == '': #verifica se a posição no tabuleiro esta vazia
                        pass # se estiver vazia não faz nada
                    else: 
                        return True # se não estiver vazia entao deve colisão
        return False # se não tiver colisão retorna falso
    
    def rotacao_direita(self): #gira a peça para direita
        girar = list(zip(*self.layout_forma)) # pega a linha do layout e junta os numeros das linhas em uma lista
        self.layout_forma =[list(linha[::-1]) for linha in girar] # inverte os numeros e pecorre as linhas e tranforma novamente em matriz
        
    def rotacao_esquerda(self): #gira a peça para esquerda
        girar = list(zip(*self.layout_forma)) # pega a linha do layout e junta os numeros das linhas em uma lista
        self.layout_forma = [list(linha) for linha in girar[::-1]] #inverte a ordem da lista e percorre as linhas e tranforma novamente em matriz
        
    def bloqueia_peca (self): # bloqueia a peça quando ela chega no final
        posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
        posicao_forma_y = self.posicao_forma[1] #posição y da forma em jogo
        peca_acima = False # variavel para verificar se a peça esta acima do tabuleiro
        for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
            for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                if self.layout_forma[y][x] == 1: # se o layout da forma for == 1
                    forma_tab_pos_x = posicao_forma_x + x # saber onde a peça esta no tabuleiro
                    forma_tab_pos_y = posicao_forma_y + y # saber onde a peça esta no tabuleiro
                    if forma_tab_pos_y < 0: #verifica se a peça chegou no topo do tabuleiro
                        peca_acima = True # se chegou no topo sinaliza que a peça esta acima do tabuleiro
                        continue
                    if 0 <= forma_tab_pos_x < 10 and 0 <= forma_tab_pos_y < 20: #verifica se a peça esta dentro do tabuleiro
                        self.mapa[forma_tab_pos_y][forma_tab_pos_x] = self.recb_codigo_cod(self.formas[self.forma_jogavel]['cor']) #adiciona no tabuleiro a cor da peça que esta em chegada no final
        self.nova_forma = True # sinaliza que uma nova peça aparecera
        self.remove_linhas() # chama a def remove_linhas para remover as linhas completas
        self.layout_forma = [[]] # limpa a peça ativa para evitar que a verificação de game_over detecte sobreposição
        # permite novo uso do hold após a peça ser bloqueada
        self.hold_usado = False
        if peca_acima: # se a peça estiver acima do tabuleiro
            self.exibi_restart = True # exibe o restart

    
    def colocar_peca_fim(self): #coloca a peça direto no final do tabuleiro
        for i in range(20): # percorre todas as linhas do tabuleiro
            self.posicao_forma[1] += 1 # move a peça para baixo
            posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
            posicao_forma_y = self.posicao_forma[1] #posição y da forma em jogo
            for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
                for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                    if self.layout_forma[y][x] == 1: #se o layout da forma for == 1
                        try: # tenta verificar se a posição no tabuleiro esta vazia
                            if self.mapa[y + posicao_forma_y][x + posicao_forma_x] != '': #verifica se a posição no tabuleiro e difernete de vazio
                                self.posicao_forma[1] -= 1 # move a peça para cima
                                self.bloqueia_peca() # bloqueia a peça
                                return 
                        except: # se nao encontra nenhuma peça em baixo
                            self.posicao_forma[1] -= 1 # move a peça para cima pois atravesou o final do tabuleiro
                            self.bloqueia_peca() # bloqueia a peça
                            return
    
    def sair_tabuleiro(self): #verifica se a peça saiu do tabuleiro
        posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
        for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
            for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                if self.layout_forma[y][x] == 1: #se o layout da forma for == 1
                    forma_fora = posicao_forma_x + x # aadicina a posição x da forma com a posiçao x do loop para verificar se ...
                    if forma_fora >= 0 and forma_fora <= 9: # ... se a peça esta entre 0 e 9 nop tabuleiro
                        pass # se estiver dentro não faz nada
                    else:
                        return False # se estiver fora retorna False
        return True # se estiver dentro retorna True
                        
    def movimento(self, key): #movimentação do jogo
        if key == 'left': #se precionar a seta para esquerda
            self.posicao_forma[0] -= 1 # move a peça para esquerda
            if self.sair_tabuleiro() == False or self.colisao_lateral(): #verifica se a peça saiu do tabuleiro ou teve colisão lateral
                self.posicao_forma[0] += 1 #se teve colisão ou saiu do tabuleiro move a peça para direita
        elif key == 'down': #se precionar a seta para baixo
            self.posicao_forma[1] += 1 # move a peça para baixo
        elif key == 'right': #se precionar a seta para direita
            self.posicao_forma[0] += 1 # move a peça para direita
            if self.sair_tabuleiro() == False or self.colisao_lateral(): #verifica se a peça saiu do tabuleiro ou teve colisão lateral
                self.posicao_forma[0] -= 1 #se teve colisão ou saiu do tabuleiro move a peça para esquerda
        elif key == 'q': #se precionar a letra 'q'
            self.rotacao_esquerda() # gira a peça para esquerda
            if self.sair_tabuleiro() == False: #verifica se a peça saiu do tabuleiro
                self.rotacao_direita() #se saiu do tabuleiro gira a peça para direita
        elif key == 'e' or key == 'up': #se precionar a letra 'e' ou a seta para cima
            self.rotacao_direita() # gira a peça para direita
            if self.sair_tabuleiro() == False: #verifica se a peça saiu do tabuleiro
                self.rotacao_esquerda() #se saiu do tabuleiro gira a peça para esquerda
        elif key == 'space': #se precionar a barra de espaço
            self.colocar_peca_fim() #coloca a peça direto no final do tabuleiro se nao tiver nada em baixo
        elif key == 'c': # guarda/troca a peça com a reserva
            self.guarda_forma()

    def caimento_peça(self):
        self.tempo += 1 # o tempo do jogo aumenta em um
        if self.tempo == 61 - self.velocidade: # se o tempo for igual a 61 menos a velocidade do jogo
            self.posicao_forma[1] += 1 # move a peça para baixo
            self.tempo = 0 # zera o tempo
        posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
        posicao_forma_y = self.posicao_forma[1] #posição y da forma em jogo
        for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
            for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                if self.layout_forma[y][x] == 1: #se o layout da forma for == 1
                    tabuleiro_x = posicao_forma_x + x # posição x da forma com a posição x do layout no tabuleiro
                    tabuleiro_y = posicao_forma_y + y # posição y da forma com a posição y do layout no tabuleiro
                    if tabuleiro_y >= 20: # se a peça chegou no final do tabuleiro
                        self.posicao_forma[1] -= 1 # move a peça para cima
                        self.bloqueia_peca() # bloqueia a peça
                        return
                    if tabuleiro_x < 0 or tabuleiro_x >= 10: # verifica se a peça esta em um intervalo entre 0 e 9 para saber se saiu do tabuleiro
                        continue 
                    if tabuleiro_y < 0: #verifica se a peça chego no topo do tabuleiro
                        self.bloqueia_peca() # se chegou = bloqueia a peça
                        self.exibi_restart = True # e exibe o restart
                        return
                    if self.mapa[tabuleiro_y][tabuleiro_x] != '': #verifica se a posição no tabuleiro e difernete de vazio
                        self.posicao_forma[1] -= 1 #se for diferente de vazio move a peça para cima
                        self.bloqueia_peca() # bloqueia a peça ao colidir com outra
                        return
                      
    def velocidade_jogo(self):# ajusta a velocidade do jogo conforme a pontuação
        self.velocidade = min(1 + (self.pontuacao // 100), 50) # aumenta a velocidade a cada 100 pontos, até um máximo de 50 de velocidade
    
    def adicionar_pontos(self,linhas):# adiciona pontos conforme as linhas completadas
        self.pontuacao += linhas * 10 # adiciona 10 pontos por linha completada
        self.velocidade_jogo() # ajusta a velocidade do jogo conforme a pontuação
        self.time = 0 # zera o tempo do jogo
    
    def remove_linhas(self): #remove as linhas completas do tabuleiro
        remover = 0 # contador de linhas removidas
        y = 19 # começa da última linha do tabuleiro
        while y >= 0: # percorre as linhas do tabuleiro de baixo para cima
            if all(self.mapa[y][x] != '' for x in range(10)): # verifica se na linha todas as colunas estão preenchidas 
                del self.mapa[y] # remove a linha completa
                self.mapa.insert(0, [''] * 10) # adiciona uma nova linha vazia no topo do tabuleiro
                remover += 1 # incrementa o contador de linhas removidas 
            else:
                y -= 1 

        if remover > 0: # se houver linhas para remover
            self.adicionar_pontos(remover) # adiciona pontos conforme as linhas completadas
            self.limpar_janela() # limpa a janela
            self.tabuleiro() # redesenha o tabuleiro
            pygame.display.update() # atualiza a tela
        
    def game_over(self): #verifica se o jogo acabou
        posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
        posicao_forma_y = self.posicao_forma[1] #posição y da forma em jogo
        if self.exibi_restart == False: # se o restart ja foi exibido
            for y in range(len(self.layout_forma)): #percorre as linhas do layout da forma
                for x in range(len(self.layout_forma[0])): #percorre as colunas do layout da forma
                    if self.layout_forma[y][x] == 1 and self.mapa[posicao_forma_y + y][posicao_forma_x + x] != '': #se o layout da forma for == 1 e a posição no tabuleiro não for vazia
                        self.exibi_restart = True # exibe o restart
                        self.layout_forma = [[]] # limpa o layout da forma
                        return 
    
    
    def restart_game(self, restart=False): # reinicia o jogo
        if self.sort_1peças or restart: # se for a primeira peça ou se o restart for True
            self.inic_forma_aleatoria() # inicia as peças aleatorias
            self.pontuacao = 0 # zera a pontuação
            self.velocidade = 1 # zera a velocidade
            self.tempo = 0 # zera o tempo
            for y in range(20): # percorre todas as linhas do tabuleiro
                for x in range(10): # percorre todas as colunas no tabuleiro
                    self.mapa[y][x] = '' # zera o tabuleiro
            self.exibi_restart = False # não exibe o restart
            self.sort_1peças = False # não é mais a primeira peça
            self.forma_reserva = None
            self.hold_usado = False
            self.nova_forma = True # uma nova forma aparecera
            self.add_forma_jogo() # adiciona a peça em jogo
    
    def butao_restart(self):
        if self.exibi_restart:
            button_color = (0, 200, 0)
            button_width = self.janela.get_width() / 2.5
            button_height = button_width / 2.5
            button_x = (self.janela.get_width() / 2) - (button_width / 2)
            button_y = (self.janela.get_height() / 2) - (button_height / 2)
            button_border = int(self.tam_celulas / 5)
            
            if pygame.key.get_pressed()[pygame.K_RETURN]: #
                self.restart_game(restart=True) # 
            else:
                pygame.draw.rect(self.janela, button_color, (button_x, button_y, button_width, button_height))
            pygame.draw.rect(self.janela, self.branco, (button_x, button_y, button_width, button_height), button_border)
            text = self.font.render('Restart', True, self.preta)
            blit_x = (self.janela.get_width() / 2) - (text.get_width() / 2)
            blit_y = (self.janela.get_height() / 2) - (text.get_height() / 2)
            self.janela.blit(text, (blit_x, blit_y))
    
sensibilidade = 15
tetris= Jogo(40)        
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and tetris.exibi_restart:
                tetris.restart_game(restart=True)
            else:
                tetris.movimento(pygame.key.name(event.key))

    if pygame.key.get_pressed()[pygame.K_LEFT] and tetris.tempo % sensibilidade == 0:
        tetris.movimento('left')
    if pygame.key.get_pressed()[pygame.K_RIGHT] and tetris.tempo % sensibilidade == 0:
        tetris.movimento('right')
    if pygame.key.get_pressed()[pygame.K_DOWN] and tetris.tempo % sensibilidade == 0:
        tetris.movimento('down')
    #if pygame.key.get_pressed()[pygame.K_SPACE] and tetris.tempo % sensibilidade == 0:
        #tetris.movimento('space')
                  
    tetris.Taxa_de_frames.tick(60)
    tetris.limpar_janela()

    if tetris.nova_forma:
        tetris.inic_forma_aleatoria()
        tetris.add_forma_jogo()
    tetris.tabuleiro()
    tetris.caimento_peça()
    tetris.game_over()
    
    tetris.butao_restart()
    pygame.display.update()