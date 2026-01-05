import pygame
import random
import time 
from sys import exit

class Jogo:
    def __init__(self,tam_cel): 
        pygame.init() # inica o pygame
        self.janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # modo tela cheia
        self.largura = self.janela.get_width() #largura da tela
        self.altura = self.janela.get_height() #altura da tela
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

        self.mapa = [['' for _ in range(10)] for _ in range(20)]

        self.sort_1pecas = True # primerias peças do jogo
        self.exibi_restart = False # mostra o butao restart
        self.tam_celulas = tam_cel # tamalho das celulas do jogo
        self.proximas_forma = [self.forma_aleatoria() for _ in range(4)] # armazena as proximas peças do jogo
        self.pontuacao = 0 # pontuaçao do jogo
        self.velocidade = 1 # velocidade do jogo
        self.forma_jogavel = self.proximas_forma[0] #formas que esta em jogo
        self.posicao_forma = [4,0] #posição da forma em jogo
        self.layout_forma = self.formas[self.forma_jogavel]['formado'] # o "desenho" da dorma em jogo
        self.nova_forma = True # quando uma nova forma aparecera
        self.forma_reserva = None #reserva (hold) de peça: None significa sem reserva
        self.hold_usado = False # impede varias peças reservas na mesma rodada
        self.turno = 0 # contador de turno geral
        self.turnos_fase=0 # contador de turnos por fase (dia/noite)
        self.dia = True # dia=True/noite=False
        self.inimigos = [] # lista de inimigos 
        self.vida_torre= 100 # vida da torre
        self.torre_pos = (self.largura//2 - 20,30) # posição da torre na tela
        self.altura_td=120 # altura do do topo da tela de tower defense
        self.altura_tabuleiro= self.altura - self.altura_td # altura do tabuleiro contando com a area de tower defense
        self.timer_noite=0 #temporizador da noite
        self.intervalo_spawn= 360 # intervalo de spawn dos inimigos
        self.inimigos_por_noite=5 # total de inimigos por noite
        self.inimigos_restantes=0 # inimigos restante para spawnar na noite

    def passar_turno(self): #passar o turno do jogo
        self.turno += 1 # a cada vez que a função for chamada incrementa no turno
        self.turnos_fase += 1 # a cada vez que a função for chamada incrementa no turno fase
        
        # troca dia/noite
        if self.turnos_fase >= 2: 
            self.turnos_fase = 0 # zera o turno fase
            self.dia = not self.dia # troca o dia para noite ou noite para dia

            if self.dia: # Se acabou de virar DIA
                self.limpar_todo_garbage() # Chama a nova função para limpar o lixo
                self.fim_noite() # chama a função fim_noite para ver se a torre sobreviveu a noite
            else: # se for noite
                self.timer_noite = 0 # zera o timer da noite
                self.inimigos_restantes = self.inimigos_por_noite # reseta os inimigos restantes para spawnar

    def limpar_todo_garbage(self): # Remove todas as linhas cinzas (X) de uma vez
        y = 19
        while y >= 0:
            if 'X' in self.mapa[y]: # se a linha tiver lixo
                del self.mapa[y] # deleta do mapa
                self.mapa.insert(0, [''] * 10) # substitui por uma vazia no topo
                # Não decrementamos o y aqui porque a linha de cima desceu para a posição atual
            else:
                y -= 1

    def adicionar_garbage(self): #adiciona linhas de lixo no tabuleiro
        buraco=random.randint(0,9) #sorteia a posição do buraco na linha
        linha=[] # cria uma linha vazia para adicionar os garbage
        for x in range(10): # percorre as colunas da linha
            if x == buraco: # se a posição for igual a buraco
                linha.append('') # coloque um bloco vazio
            else: # se não 
                linha.append('X') #coloque um bloco cinza

        self.mapa.pop(0) #remove uma linha do topo do tabuleiro para que as linhas de baixo subam
        self.mapa.append(linha) #adiciona a linha de lixo no fundo
        if self.posicao_forma[1]>0: #verifica se as peças nao chegara ao topo
            self.posicao_forma[1] -= 1 #empura a peça uma linha para cima
            
    def remover_garbage_superior(self): #remover uma linha de lixo
        for y in range(20): # pecorre todas as linhas do tabuleiro
            if 'X' in self.mapa[y]: # se a linha tiver lixo
                del self.mapa[y] #deleta do mapa
                self.mapa.insert(0, [''] * 10) #e substitui por uma vazia
                return
            
    def spawn_inimigo(self): #cria um inimigo
        self.inimigos.append({"vida": 1}) # tem um de vida
        self.adicionar_garbage() # adiciona uma linha de lixo no tabuleiro
        
    def atualizar_noite(self): # atualizar para noite
        if not self.dia and not self.exibi_restart and self.inimigos_restantes > 0:# se todas essas funçoes forem compridas 
            self.timer_noite += 1 # o tempo da noite incrementa 

            if self.timer_noite >= self.intervalo_spawn: #se o tempo da noite for = ao intervalo de spawn
                self.spawn_inimigo() #um inimigo aparece
                self.inimigos_restantes-=1 #decrementa na quantidade maxima de inimigos
                self.timer_noite = 0 # tempo da noite zera
    
    def fim_noite(self): #o que aconte quando a noite acaba
        if self.inimigos: # se ainda tiver inimigos vivos
            dano=len(self.inimigos)*10 #tomara dano no valor de (quantos inimigos vivos)*10
            self.vida_torre -= dano #tira a vida da torre 
            self.inimigos.clear() # limpa os inimigos vivos
        if self.vida_torre <= 0:#se a torre morrer
            self.exibi_restart = True #mostre o butao de restart
    
    def limpar_janela(self): #limpa a janela
         pygame.draw.rect(self.janela, self.preta, (0, 0, self.janela.get_width(), self.janela.get_height()))
        
    def forma_aleatoria(self): #escolhe uma forma aleatoria
        return random.choice(list(self.formas.keys())) #escolhe uma forma aleatoria da lista de formas
        
    def inic_forma_aleatoria(self): # adiciona a forma aletoria na lista 'proximas_forma'
        for i in range(4): #percorre a lista
            self.proximas_forma[i] = self.forma_aleatoria() #adiciona as formas na lista
            
    def desenhar_torre(self): #desenha a torre no jogo
        x,y=self.torre_pos # a posição da torre na tela
        pygame.draw.rect(self.janela,(120,120,255),(x,y,40,60)) #desenha o quadrado da torre
        
    def desenhar_inimigo(self):
        margem = 20
        largura_inimigo = 24
        espacamento = 6
        
        for i,inimigos in enumerate(self.inimigos):
            x = margem + i * (largura_inimigo+espacamento)
            y = 20
            pygame.draw.rect(self.janela,(200,50,50),(x,y,largura_inimigo,largura_inimigo))
            
    def desenhar_vida_torre(self):
        largura_barra = 200
        vida = max(self.vida_torre, 0)
        proporcao = vida / 100

        pygame.draw.rect(self.janela,(80, 80, 80),(20, self.altura_td - 25, largura_barra, 10))

        pygame.draw.rect(self.janela,(50, 200, 50),(20, self.altura_td - 25, largura_barra * proporcao, 10))
        
    def desenhar_area_td(self):
        tabuleiro_L = self.tam_celulas * 10 
        x_tabuleiro = (self.largura - tabuleiro_L) // 2
        pygame.draw.rect(self.janela,(20, 20, 20),(x_tabuleiro, 0, tabuleiro_L, self.altura_td))
        pygame.draw.line(self.janela,self.branco,(x_tabuleiro, self.altura_td),(x_tabuleiro + tabuleiro_L, self.altura_td),2)
        self.desenhar_torre()
        self.desenhar_inimigo()
        self.desenhar_vida_torre()

    def add_forma_aleatoria(self): #adicionar a uma casa a frente a forma aleatoria na variavel 'proximas_formas'
        for i in range(len(self.proximas_forma)): #percorre a lista 'self.proximas_forma'
            if i != 0: # não conta a posição 1 do loop
                self.proximas_forma[i-1] = self.proximas_forma[i] # movendo as formas para cima quando uma entra no jogo
        self.proximas_forma[len(self.proximas_forma)-1] = self.forma_aleatoria() #adiciona um nova forma na lista
        
    def add_forma_jogo(self): # adiciona o jogo uma peça
        self.forma_jogavel = self.proximas_forma[0] # substitui a peça do jogo pela proxima
        self.layout_forma = self.formas[self.forma_jogavel]['formado'] #sustitui o formado da peça
        self.add_forma_aleatoria() # chama def add_forma_aleatoria para adiciona uma forma á lista
        self.nova_forma = False # muda a variavel para que não coloque mais peças
        self.posicao_forma = [4,0] # local onde aparecera a nova forma
        
    def guarda_forma(self):
        if self.hold_usado:
            return  
        if self.forma_reserva is None:
            self.forma_reserva = self.forma_jogavel
            self.nova_forma = True
            self.add_forma_jogo()
        else:
            antiga = self.forma_jogavel
            self.forma_jogavel = self.forma_reserva
            self.forma_reserva = antiga
            self.layout_forma = self.formas[self.forma_jogavel]['formado']
            self.posicao_forma = [4, 0]
        self.hold_usado = True

    def recb_cor(self, cod_cor): 
        if cod_cor == 'R': return self.roxo
        elif cod_cor == 'A': return self.azul
        elif cod_cor == 'C': return self.azul_c
        elif cod_cor == 'V': return self.vermelho
        elif cod_cor == 'L': return self.laranja
        elif cod_cor == 'Y': return self.amarelo
        elif cod_cor == 'G': return self.verde     
        elif cod_cor == 'B' or cod_cor == 'X': return self.cinza
        else: return None           
    
    def recb_codigo_cod(self, cor):        
        if cor == self.roxo: return 'R'
        elif cor == self.azul: return 'A'
        elif cor == self.azul_c: return 'C'
        elif cor == self.vermelho: return 'V'
        elif cor == self.laranja: return 'L'
        elif cor == self.amarelo: return 'Y'
        elif cor == self.verde: return 'G'
        else: return None

    def tabuleiro(self):# desenha o tabuleiro do jogo
        tabuleiro_L = self.tam_celulas * 10 
        tabuleiro_A = self.tam_celulas * 20 

        x_tabuleiro = (self.janela.get_width() - tabuleiro_L) // 2 
        y_tabuleiro = self.altura_td + 20 
        
        # --- EXIBE TURNO E FASE DO LADO DIREITO ---
        try:
            status = "DIA" if self.dia else "NOITE"
            cor_fase = self.amarelo if self.dia else self.azul_c
            txt_t = self.font.render(f"Turno: {self.turno}", True, self.branco)
            txt_f = self.font.render(f"Fase: {status}", True, cor_fase)
            txt_x = x_tabuleiro + tabuleiro_L + 15
            self.janela.blit(txt_t, (txt_x, y_tabuleiro + 10))
            self.janela.blit(txt_f, (txt_x, y_tabuleiro + 45))
        except: pass

        for y in range(20): 
            for x in range(10): 
                rx = x_tabuleiro + self.tam_celulas * x 
                ry = y_tabuleiro + self.tam_celulas * y 
                pygame.draw.rect(self.janela, self.branco, (rx, ry, self.tam_celulas, self.tam_celulas), 1) 
                if self.mapa[y][x] != '': 
                    cor = self.recb_cor(self.mapa[y][x]) 
                    if cor: pygame.draw.rect(self.janela, cor, (rx, ry, self.tam_celulas, self.tam_celulas)) 

        pygame.draw.rect(self.janela, self.branco, (x_tabuleiro, y_tabuleiro, tabuleiro_L, tabuleiro_A), 2) 

        # Desenhar peça ativa
        cor_ativa = self.formas[self.forma_jogavel]['cor']
        for y in range(len(self.layout_forma)):
            for x in range(len(self.layout_forma[0])):
                if self.layout_forma[y][x] == 1:
                    rx = x_tabuleiro + self.tam_celulas * (x + self.posicao_forma[0])
                    ry = y_tabuleiro + self.tam_celulas * (y + self.posicao_forma[1])
                    if ry >= y_tabuleiro:
                        pygame.draw.rect(self.janela, cor_ativa, (rx, ry, self.tam_celulas, self.tam_celulas))
        
        self.desenha_hold(x_tabuleiro, y_tabuleiro)

    def colisao_lateral(self): 
        posicao_forma_x = self.posicao_forma[0] 
        posicao_forma_y = self.posicao_forma[1] 
        for y in range(len(self.layout_forma)): 
            for x in range(len(self.layout_forma[0])): 
                if self.layout_forma[y][x] == 1: 
                    forma_tab_pos_x = posicao_forma_x + x 
                    forma_tab_pos_y = posicao_forma_y + y 
                    if 0 <= forma_tab_pos_y < 20 and 0 <= forma_tab_pos_x < 10:
                        if self.mapa[forma_tab_pos_y][forma_tab_pos_x] != '':
                            return True
        return False 
    
    def desenha_hold(self, x_tabuleiro, y_tabuleiro):
        hold_w, hold_h = self.tam_celulas * 4, self.tam_celulas * 4
        hold_x = x_tabuleiro - hold_w - 10
        if hold_x < 0: hold_x = x_tabuleiro + (self.tam_celulas * 10) + 10
        
        pygame.draw.rect(self.janela, self.branco, (hold_x, y_tabuleiro, hold_w, hold_h), 2)
        if self.forma_reserva:
            layout = self.formas[self.forma_reserva]['formado']
            cor = self.formas[self.forma_reserva]['cor']
            for y, row in enumerate(layout):
                for x, val in enumerate(row):
                    if val == 1:
                        pygame.draw.rect(self.janela, cor, (hold_x + x*self.tam_celulas, y_tabuleiro + y*self.tam_celulas, self.tam_celulas, self.tam_celulas))

    def rotacao_direita(self): 
        self.layout_forma =[list(linha[::-1]) for linha in zip(*self.layout_forma)]
        
    def rotacao_esquerda(self): 
        self.layout_forma = [list(linha) for linha in zip(*self.layout_forma)][::-1]
        
    def bloqueia_peca (self): 
        for y in range(len(self.layout_forma)): 
            for x in range(len(self.layout_forma[0])): 
                if self.layout_forma[y][x] == 1: 
                    fx, fy = self.posicao_forma[0] + x, self.posicao_forma[1] + y 
                    if fy < 0: 
                        self.exibi_restart = True
                    elif 0 <= fx < 10 and 0 <= fy < 20:
                        self.mapa[fy][fx] = self.recb_codigo_cod(self.formas[self.forma_jogavel]['cor'])
        self.nova_forma = True
        self.remove_linhas()
        self.hold_usado = False

    def colocar_peca_fim(self): 
        while not self.colisao_fundo():
            self.posicao_forma[1] += 1
        self.posicao_forma[1] -= 1
        self.bloqueia_peca()

    def colisao_fundo(self):
        for y in range(len(self.layout_forma)):
            for x in range(len(self.layout_forma[0])):
                if self.layout_forma[y][x] == 1:
                    fx, fy = self.posicao_forma[0] + x, self.posicao_forma[1] + y
                    if fy >= 20 or (0 <= fy < 20 and self.mapa[fy][fx] != ''):
                        return True
        return False

    def sair_tabuleiro(self): 
        for y in range(len(self.layout_forma)): 
            for x in range(len(self.layout_forma[0])): 
                if self.layout_forma[y][x] == 1: 
                    fx = self.posicao_forma[0] + x 
                    if fx < 0 or fx > 9: return False 
        return True 
                        
    def movimento(self, key): 
        if key == 'left': 
            self.posicao_forma[0] -= 1 
            if not self.sair_tabuleiro() or self.colisao_lateral(): self.posicao_forma[0] += 1
        elif key == 'down': 
            self.posicao_forma[1] += 1
            if self.colisao_fundo(): self.posicao_forma[1] -= 1
        elif key == 'right': 
            self.posicao_forma[0] += 1 
            if not self.sair_tabuleiro() or self.colisao_lateral(): self.posicao_forma[0] -= 1
        elif key == 'up': 
            self.rotacao_direita()
            if not self.sair_tabuleiro() or self.colisao_lateral(): self.rotacao_esquerda()
        elif key == 'c': self.guarda_forma()

    def caimento_peça(self):
        self.tempo += 1 
        if self.tempo >= 61 - self.velocidade: 
            self.posicao_forma[1] += 1 
            self.tempo = 0
            if self.colisao_fundo():
                self.posicao_forma[1] -= 1
                self.bloqueia_peca()
                      
    def velocidade_jogo(self):
        self.velocidade = min(1 + (self.pontuacao // 100), 50) 
    
    def adicionar_pontos(self,linhas):
        self.pontuacao += linhas * 10 
        self.velocidade_jogo() 
    
    def remove_linhas(self): 
        remover = 0 
        y = 19 
        while y >= 0: 
            # Verifica se a linha está cheia
            if all(self.mapa[y][x] != '' for x in range(10)):
                # Se a linha sendo eliminada tiver blocos 'X' (garbage), remove um inimigo
                if 'X' in self.mapa[y]:
                    if self.inimigos:
                        self.inimigos.pop(0)
                
                del self.mapa[y]
                self.mapa.insert(0,['']*10)
                remover += 1
                # O turno só passa se uma linha for completada
                self.passar_turno() 
            else: y -= 1
            
        if remover > 0:
            self.adicionar_pontos(remover)
        
    def game_over(self): 
        if self.exibi_restart: return
        for y in range(len(self.layout_forma)):
            for x in range(len(self.layout_forma[0])):
                if self.layout_forma[y][x] == 1:
                    fx, fy = self.posicao_forma[0] + x, self.posicao_forma[1] + y
                    if 0 <= fy < 20 and 0 <= fx < 10:
                        if self.mapa[fy][fx] != '' and fy < 1:
                            self.exibi_restart = True
    
    def restart_game(self, restart=False): 
        self.__init__(self.tam_celulas)
        self.sort_1pecas = False
        self.add_forma_jogo()
    
    def butao_restart(self):
        if self.exibi_restart:
            pygame.draw.rect(self.janela, (0, 200, 0), (self.largura//4, self.altura//3, self.largura//2, 100))
            text = self.font.render('GAME OVER - Press ENTER', True, self.branco)
            self.janela.blit(text, (self.largura//2 - text.get_width()//2, self.altura//3 + 40))

sensibilidade = 15
tetris= Jogo(24)        
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

    if not tetris.exibi_restart:
        tetris.Taxa_de_frames.tick(60)
        tetris.limpar_janela()
        tetris.desenhar_area_td()
        if tetris.nova_forma:
            tetris.add_forma_jogo()
        tetris.tabuleiro()
        tetris.caimento_peça()
        tetris.atualizar_noite()
        tetris.game_over()
    
    tetris.butao_restart()
    pygame.display.update()
