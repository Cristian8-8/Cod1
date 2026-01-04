import pygame
import random
import time 
from sys import exit

class Jogo:
    def __init__(self,tam_cel): 
        # Lista de pedidos ativos (cada pedido é uma lista de códigos de cor)
        # (adiada para depois de self.inventario)
        pygame.init()
        # calcula largura suficiente para tabuleiro (10 células) + painéis laterais
        largura_total = self.calcula_largura_janela(tam_cel)
        self.janela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) # modo tela cheia
        pygame.display.set_caption("JOGO") # nome da janela
        self.Taxa_de_frames = pygame.time.Clock() # variavel dos ticks do jogo
        self.tempo = 0 # tempo do jogo
        self.font = pygame.font.Font(None, 36) # fonte para o texto
        self.recurso_slot_max = 5
        self.item_slot = None
        self.fila_fonte = []  # filas de fontes para o transportador

        #bloco movel
        self.transportador_pos = None 
        self.transportador_item = None 
        self.transportador_estado = 'idle' 
        self.transportador_vel = 1 # velocidade do transportador

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
        # inventário de recursos agora armazena códigos de cor das peças
        self.turno = 0
        self.dia = True
        self.inimigos = []  # lista de inimigos (blocos vermelhos)
        self.inventario = {
            'Y': 0,  # amarelo
            'R': 0,  # roxo
            'C': 0,  # azul claro
            'V': 0,  # vermelho
            'G': 0,  # verde
            'A': 0,  # azul
            'L': 0   # laranja
        }

        # Agora que inventario existe, pode gerar pedidos
        self.pedidos_ativos = [self.gerar_pedido_aleatorio() for _ in range(1)]

	def calcula_largura_janela(self,tam_cel):
	       multiplicador_total=22
	       return tam_cel*multiplicador_total
	       
        
    def passar_turno(self):
        self.turno += 1
        if self.turno % 10 == 0: # a cada 5 turnos
            self.dia = not self.dia # alterna entre dia e noite
            if not self.dia:
                self.ataque_noturno()
            else:
                self.inimigos.clear()
    
    def ataque_noturno(self):
        if self.dia:
        		return
		linhas = 1 + self.turno // 10 #dificuldade escala

		for _ in range(lfor
        # remove a removee do topo
        	self.mapa.pop(0)

        # cria nova linha inimiga embaixo
        	nova_linha = ['V' for _ in range(10)]
        	self.mapa.append(nova_linha)
        
    def faz_pedido_armazem(self, requisicoes):
            """
            Tenta atender um pedido ao armazém (inventário).
            requisicoes: lista de códigos de cor (ex: ['Y', 'R', 'C'])
            Consome 1 unidade de cada bloco requisitado se houver no inventário.
            Retorna True se todos os itens foram atendidos, False caso contrário.
            """
            # Verifica se todos os itens estão disponíveis
            for cod_cor in requisicoes:
                if self.inventario.get(cod_cor, 0) <= 0:
                    return False
            # Consome os itens
            for cod_cor in requisicoes:
                self.inventario[cod_cor] -= 1
            return True
    def desenha_pedidos(self, x, y):
        """
        Exibe os pedidos ativos em uma caixa, com o título 'Pedidos'.
        """
        largura_caixa = self.tam_celulas * 5
        altura_caixa = (self.tam_celulas + 10) * max(3, len(self.pedidos_ativos)) + 40
        deslocamento = 20
        pygame.draw.rect(self.janela, (40, 40, 40), (x - 10 + deslocamento, y - 40, largura_caixa, altura_caixa))
        pygame.draw.rect(self.janela, self.branco, (x - 10 + deslocamento, y - 40, largura_caixa, altura_caixa), 2)
        # Título
        titulo = self.font.render('Pedidos', True, self.branco)
        self.janela.blit(titulo, (x - 10 + deslocamento + (largura_caixa - titulo.get_width()) // 2, y - 40 + 8))
        # Lista de pedidos
        margem = 10
        for i, pedido in enumerate(self.pedidos_ativos):
            for j, cod_cor in enumerate(pedido):
                cor = self.recb_cor(cod_cor)
                x_bloco = x + deslocamento + j * (self.tam_celulas + 8)
                y_bloco = y + i * (self.tam_celulas + margem)
                pygame.draw.rect(self.janela, cor, (x_bloco, y_bloco, self.tam_celulas, self.tam_celulas))
                pygame.draw.rect(self.janela, self.branco, (x_bloco, y_bloco, self.tam_celulas, self.tam_celulas), 2)
                txt_cod = self.font.render(cod_cor, True, self.preta)
                txt_cx = x_bloco + (self.tam_celulas - txt_cod.get_width()) // 2
                txt_cy = y_bloco + (self.tam_celulas - txt_cod.get_height()) // 2
                self.janela.blit(txt_cod, (txt_cx, txt_cy))
    
    def derrotar_inimigos(self):
        """Remove todos inimigos do tabuleiro (chamada ao completar uma linha)."""
        for x, y in self.inimigos:
            if self.mapa[y][x] == 'V':
                self.mapa[y][x] = ''
        self.inimigos.clear()

    
    def limpar_janela(self): #limpa a janela
        pygame.draw.rect(self.janela, self.preta, (0, 0, self.janela.get_width(), self.janela.get_height()))
        
    def gerar_pedido_aleatorio(self, tamanho=None):
            """
            Gera um pedido aleatório de materiais (lista de códigos de cor).
            """
            opcoes = list(self.inventario.keys())
            if tamanho is None:
                tamanho = random.randint(2, 4)
            return [random.choice(opcoes) for _ in range(tamanho)]

    def processar_pedidos(self):
            """
            Tenta atender os pedidos ativos, removendo-os se forem completados.
            Sempre que um pedido for atendido, gera um novo pedido automaticamente.
            """
            pedidos_restantes = []
            pedidos_atendidos = 0
            for pedido in self.pedidos_ativos:
                if self.faz_pedido_armazem(pedido):
                    pedidos_atendidos += 1
                else:
                    pedidos_restantes.append(pedido)
            self.pedidos_ativos = pedidos_restantes
            # Gera um novo pedido para cada pedido atendido
            for _ in range(pedidos_atendidos):
                self.pedidos_ativos.append(self.gerar_pedido_aleatorio())
                
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

    #def recursos(self, entrada):
        """Retorna o recurso associado a uma cor ou a uma forma.

        Entrada pode ser:
        - tupla RGB (ex.: self.amarelo)
        - nome da forma (ex.: 'forma_1')
        Retorna uma string com o recurso ou None se não houver mapeamento.
        """
        # obter cor a partir do parâmetro
      #  cor = None
     #   if isinstance(entrada, str):
            # se for nome de forma, pega a cor da forma
           # if entrada in self.formas:
           #     cor = self.formas[entrada]['cor']
           # else:
                # aceita também códigos únicos usados em mapa (ex: 'Y', 'R')
           #     try:
                    # converte código para cor usando recb_cor se possível
                 #   cor = self.recb_cor(entrada)
             #   except Exception:
           #         cor = None
       # else:
            # assume que é uma tupla RGB
          #  cor = entrada

       """mapping = {
            self.amarelo: 'pedra',
            self.roxo: 'madeira',
            self.azul_c: 'pano',
            self.vermelho: 'ferro',
            self.verde: 'cobre',
            self.azul: 'comida',
            self.laranja: 'barro'
        }

        return mapping.get(cor)"""
    
    def atualiza_transportador(self, fonte_pos, slot_pos):
        if self.transportador_estado == 'idle':
            self.transportador_estado ='indo_pegar'
        if self.transportador_pos is None:
            self.transportador_pos = list(fonte_pos)

    # estado: indo pegar
        if self.transportador_estado == 'indo_pegar':
            self._mover_transportador(fonte_pos)

            if self.transportador_pos == list(fonte_pos):
                if self.fila_fonte:
                    self.transportador_item = self.fila_fonte.pop(0)
                    self.transportador_estado = 'indo_entregar'
                else:
                    self.transportador_estado = 'idle'

    # estado: indo entregar
        elif self.transportador_estado == 'indo_entregar':
            self._mover_transportador(slot_pos)

            if self.transportador_pos == list(slot_pos):
                # Incrementa o inventário ao entregar
                if self.transportador_item:
                    cod_cor = None
                    if isinstance(self.transportador_item, tuple):
                        cod_cor = self.recb_codigo_cod(self.transportador_item)
                    elif isinstance(self.transportador_item, str):
                        cod_cor = self.transportador_item
                    if cod_cor and cod_cor in self.inventario:
                        self.inventario[cod_cor] += 1
                self.transportador_item = None
                self.transportador_estado = 'idle'
                self.passar_turno()  # Avança o turno ao entregar
    
    def _mover_transportador(self, destino):
        for i in (0, 1):
            if self.transportador_pos[i] < destino[i]:
                self.transportador_pos[i] += self.transportador_vel
            elif self.transportador_pos[i] > destino[i]:
                self.transportador_pos[i] -= self.transportador_vel

        # evita passar do ponto
            if abs(self.transportador_pos[i] - destino[i]) < self.transportador_vel:
                self.transportador_pos[i] = destino[i]

    def desenha_transportador(self):
        if not self.transportador_pos:
            return

        cor = (180, 180, 255)
        if self.transportador_item:
            cor = self.transportador_item if isinstance(self.transportador_item, tuple) else {
                'pedra': self.amarelo,
                'madeira': self.roxo,
                'pano': self.azul_c,
                'ferro': self.vermelho,
                'cobre': self.verde,
                'comida': self.azul,
                'barro': self.laranja
            }.get(self.transportador_item, (180, 180, 255))

        pygame.draw.rect(self.janela, cor,(*self.transportador_pos, self.tam_celulas, self.tam_celulas))
        pygame.draw.rect(self.janela,self.branco,(*self.transportador_pos, self.tam_celulas, self.tam_celulas),2)



    
    def verificar_slot_por_inventario(self):
        if self.transportador_estado != 'idle':
            return 
        for recurso, quantidade in self.inventario.items():
            if quantidade >= self.recurso_slot_max:
                self.inventario[recurso] -= self.recurso_slot_max

                # converte recurso em COR
                cor_recurso = {
                    'pedra': self.amarelo,
                    'madeira': self.roxo,
                    'pano': self.azul_c,
                    'ferro': self.vermelho,
                    'cobre': self.verde,
                    'comida': self.azul,
                    'barro': self.laranja
                    }[recurso]

                self.fila_fonte.append(cor_recurso)
                break
    
    def tabuleiro(self):# desenha o tabuleiro do jogo
        tabuleiro_L = self.tam_celulas * 10 # largura do tabuleiro
        tabuleiro_A = self.tam_celulas * 20 # altura do tabuleiro
        # calcula top_h para caber na janela (não empurrar o tabuleiro para fora)
        altura_maxima = self.janela.get_height() - tabuleiro_A # calcula a altura máxima da tela
        topo_largura = min(self.tam_celulas * 3, max(0, altura_maxima)) # define a margem superior do tabuleiro

        x_tabuleiro = (self.janela.get_width() - tabuleiro_L) // 2 # centraliza horizontalmente
        y_tabuleiro = int(topo_largura * 2.7) # define a margem superior do tabuleiro
        pygame.draw.rect(self.janela,self.preta,(x_tabuleiro,0,tabuleiro_L,topo_largura)) # pinta a área acima do tabuleiro de preto

        # Exibe turno e dia/noite centralizado acima do tabuleiro
        try:
            txt_turno = f"Turno: {self.turno} - {'Dia' if self.dia else 'Noite'}"
            txt_t = self.font.render(txt_turno, True, self.branco)
            txt_x = x_tabuleiro + (tabuleiro_L - txt_t.get_width()) // 2
            txt_y = max(10, y_tabuleiro - self.tam_celulas - txt_t.get_height() - 10)
            self.janela.blit(txt_t, (txt_x, txt_y))
        except Exception:
            pass

        # Exibe os pedidos ativos à direita do tabuleiro
        pedidos_x = x_tabuleiro + tabuleiro_L + 60
        pedidos_y = y_tabuleiro + 40
        self.desenha_pedidos(pedidos_x, pedidos_y)

        # ---- LINHA ACIMA DO TABULEIRO ----
        y_linha_acima = y_tabuleiro - self.tam_celulas
        pygame.draw.line(
            self.janela,(255, 255, 255),(x_tabuleiro, y_linha_acima + self.tam_celulas),(x_tabuleiro + tabuleiro_L, y_linha_acima + self.tam_celulas),2)

        # --- POSIÇÕES DOS QUADRADOS NO TOPO ---
        fonte_pos = (x_tabuleiro, y_linha_acima)
        destino_pos = (x_tabuleiro + tabuleiro_L - self.tam_celulas, y_linha_acima)
        # --- QUADRADO DESTINO ---
        pygame.draw.rect(self.janela,(70, 70, 70),(destino_pos[0], destino_pos[1], self.tam_celulas, self.tam_celulas))
        pygame.draw.rect(self.janela,self.branco,(destino_pos[0], destino_pos[1], self.tam_celulas, self.tam_celulas),2)

        # ---- CASA ACIMA DO TABULEIRO ----
        pygame.draw.rect(
            self.janela,(200, 200, 200),(x_tabuleiro,y_linha_acima,self.tam_celulas,self.tam_celulas))

        pygame.draw.rect(self.janela,(255, 255, 255),(x_tabuleiro,y_linha_acima,self.tam_celulas,self.tam_celulas))
        pygame.draw.rect(self.janela,(255, 255, 255),(x_tabuleiro,y_linha_acima,self.tam_celulas,self.tam_celulas), 2)

        # --- DESENHA FILA DE ITENS NA FONTE ---
        for i, item in enumerate(self.fila_fonte[:3]):  # mostra até 3
            cor_item = {
                'pedra': self.amarelo,
                'madeira': self.roxo,
                'pano': self.azul_c,
                'ferro': self.vermelho,
                'cobre': self.verde,
                'comida': self.azul,
                'barro': self.laranja
            }.get(item, self.branco)

            margem = 4
            tamanho = self.tam_celulas // 3

            pygame.draw.rect(self.janela,cor_item,(fonte_pos[0] + margem + i * (tamanho + 2),fonte_pos[1] + self.tam_celulas - tamanho - margem,tamanho,tamanho))

        # atualiza e desenha transportador
        self.atualiza_transportador(fonte_pos, destino_pos)
        self.desenha_transportador()

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
        # desenha a área de Hold (peça reserva)
        self.desenha_hold(x_tabuleiro, y_tabuleiro)

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
    
    def blocos_requisitados(self, requisicoes):
        """
        requisicoes: lista de códigos de cor (ex: ['Y', 'R', 'C'])
        Consome 1 unidade de cada bloco requisitado se houver no inventário.
        Retorna lista dos blocos que foram atendidos.
        """
        atendidos = []
        for cod_cor in requisicoes:
            if self.inventario.get(cod_cor, 0) > 0:
                self.inventario[cod_cor] -= 1
                atendidos.append(cod_cor)
        return atendidos

    def desenha_requisicoes(self, requisicoes, x, y):
        """
        Exibe na tela os blocos requisitados, em linha horizontal.
        """
        tam_bloco = self.tam_celulas
        margem = 8
        for i, cod_cor in enumerate(requisicoes):
            cor = self.recb_cor(cod_cor)
            x_bloco = x + i * (tam_bloco + margem)
            y_bloco = y
            pygame.draw.rect(self.janela, cor, (x_bloco, y_bloco, tam_bloco, tam_bloco))
            pygame.draw.rect(self.janela, self.branco, (x_bloco, y_bloco, tam_bloco, tam_bloco), 2)
            txt_cod = self.font.render(cod_cor, True, self.preta)
            txt_cx = x_bloco + (tam_bloco - txt_cod.get_width()) // 2
            txt_cy = y_bloco + (tam_bloco - txt_cod.get_height()) // 2
            self.janela.blit(txt_cod, (txt_cx, txt_cy))

    def desenha_hold(self, x_tabuleiro, y_tabuleiro):
        """Desenha a caixa de Hold e a peça armazenada (se houver)."""
        hold_w = self.tam_celulas * 4
        hold_h = self.tam_celulas * 4
        hold_margin = self.tam_celulas
        tabuleiro_L = self.tam_celulas * 18
        # tenta posicionar à esquerda; se não couber, posiciona à direita do tabuleiro
        hold_x = x_tabuleiro - hold_w - hold_margin
        if hold_x < hold_margin:
            hold_x = x_tabuleiro + tabuleiro_L + hold_margin
        hold_y = y_tabuleiro
        pygame.draw.rect(self.janela, self.preta, (hold_x, hold_y, hold_w, hold_h))
        pygame.draw.rect(self.janela, self.branco, (hold_x, hold_y, hold_w, hold_h), 2)
        try:
            label = self.font.render('Hold', True, self.branco)
            self.janela.blit(label, (hold_x + (hold_w - label.get_width())/2, hold_y - label.get_height() - 5))
        except Exception:
            pass

        if self.forma_reserva is not None:
            layout_res = self.formas[self.forma_reserva]['formado']
            cor_res = self.formas[self.forma_reserva]['cor']
            cor_borda_res = tuple(min(rgb + 50, 255) for rgb in cor_res)
            layout_h = len(layout_res)
            layout_w = len(layout_res[0])
            offset_x = (4 - layout_w) // 2
            offset_y = (4 - layout_h) // 2
            for ry in range(layout_h):
                for rx_ in range(layout_w):
                    if layout_res[ry][rx_] == 1:
                        px = hold_x + self.tam_celulas * (rx_ + offset_x)
                        py = hold_y + self.tam_celulas * (ry + offset_y)
                        pygame.draw.rect(self.janela, cor_res, (px, py, self.tam_celulas, self.tam_celulas))
                        pygame.draw.rect(self.janela, cor_borda_res, (px, py, self.tam_celulas, self.tam_celulas), 1)

        # Esquerda: itens no receptor (fila_fonte), Direita: itens no armazém (inventário)
        try:
            margem = 8
            tam_bloco = self.tam_celulas
            # Centraliza o receptor em relação ao hold e desce 30 pixels
            caixa_larg = tam_bloco * 2 + margem * 3
            inv_x = hold_x + (hold_w - caixa_larg) // 2
            inv_y = hold_y + hold_h + 40
            # Centralizar armazém com pedidos e descer 50 pixels
            tabuleiro_L = self.tam_celulas * 10
            # Posição da caixa de pedidos
            pedidos_x = x_tabuleiro + tabuleiro_L + 60
            pedidos_y = y_tabuleiro + 40
            largura_caixa_pedidos = self.tam_celulas * 5
            deslocamento_pedidos = 20
            # Centraliza armazém com a caixa de pedidos
            req_x = pedidos_x - 10 + deslocamento_pedidos + (largura_caixa_pedidos - caixa_larg) // 2
            req_y = pedidos_y + 140
            # Dimensões das caixas
            caixa_alt = tam_bloco * 4 + margem * 5
            # Caixa do receptor
            pygame.draw.rect(self.janela, (40, 40, 40), (inv_x - margem, inv_y - margem, caixa_larg, caixa_alt))
            pygame.draw.rect(self.janela, self.branco, (inv_x - margem, inv_y - margem, caixa_larg, caixa_alt), 2)
            label_rec = self.font.render('Receptor', True, self.branco)
            self.janela.blit(label_rec, (inv_x - margem + (caixa_larg - label_rec.get_width()) // 2, inv_y - margem - label_rec.get_height() - 2))
            # Caixa do armazém
            pygame.draw.rect(self.janela, (40, 40, 40), (req_x - margem, req_y - margem, caixa_larg, caixa_alt))
            pygame.draw.rect(self.janela, self.branco, (req_x - margem, req_y - margem, caixa_larg, caixa_alt), 2)
            label_arm = self.font.render('Armazém', True, self.branco)
            self.janela.blit(label_arm, (req_x - margem + (caixa_larg - label_arm.get_width()) // 2, req_y - margem - label_arm.get_height() - 2))

            # Contagem dos itens no receptor (fila_fonte)
            fila_contagem = {k: 0 for k in self.inventario.keys()}
            for item in self.fila_fonte:
                cod = None
                if isinstance(item, tuple):
                    cod = self.recb_codigo_cod(item)
                elif isinstance(item, str):
                    cod = item
                if cod and cod in fila_contagem:
                    fila_contagem[cod] += 1
            # Exibir itens 2 em 2 (duas colunas)
            for idx, cod_cor in enumerate(self.inventario):
                cor = self.recb_cor(cod_cor)
                col = idx % 2
                row = idx // 2
                # Receptor (esquerda)
                x_bloco = inv_x + col * (tam_bloco + margem)
                y_bloco = inv_y + row * (tam_bloco + margem)
                pygame.draw.rect(self.janela, cor, (x_bloco, y_bloco, tam_bloco, tam_bloco))
                pygame.draw.rect(self.janela, self.branco, (x_bloco, y_bloco, tam_bloco, tam_bloco), 2)
                txt_valor = self.font.render(str(fila_contagem[cod_cor]), True, self.preta)
                txt_cx = x_bloco + (tam_bloco - txt_valor.get_width()) // 2
                txt_cy = y_bloco + (tam_bloco - txt_valor.get_height()) // 2
                self.janela.blit(txt_valor, (txt_cx, txt_cy))
                # Armazém (direita)
                x_req = req_x + col * (tam_bloco + margem)
                y_req = req_y + row * (tam_bloco + margem)
                pygame.draw.rect(self.janela, cor, (x_req, y_req, tam_bloco, tam_bloco))
                pygame.draw.rect(self.janela, self.branco, (x_req, y_req, tam_bloco, tam_bloco), 2)
                txt_cod = self.font.render(str(self.inventario[cod_cor]), True, self.preta)
                txt_cod_x = x_req + (tam_bloco - txt_cod.get_width()) // 2
                txt_cod_y = y_req + (tam_bloco - txt_cod.get_height()) // 2
                self.janela.blit(txt_cod, (txt_cod_x, txt_cod_y))
        except Exception:
            pass

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
            for y in range(len(self.layout_forma)):
                for x in range(len(self.layout_forma[0])):
                    if self.layout_forma[y][x] == 1:
                        try:
                            if (0 <= y + posicao_forma_y < 20) and (0 <= x + posicao_forma_x < 10):
                                if self.mapa[y + posicao_forma_y][x + posicao_forma_x] != '':
                                    self.posicao_forma[1] -= 1
                                    self.bloqueia_peca()
                                    return
                            else:
                                self.posicao_forma[1] -= 1
                                self.bloqueia_peca()
                                return
                        except Exception:
                            self.posicao_forma[1] -= 1
                            self.bloqueia_peca()
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
                        # Só bloqueia se a peça realmente está caindo, não durante ataque inimigo
                        if not self.exibi_restart:
                            self.bloqueia_peca() # bloqueia a peça
                        return
                    if tabuleiro_x < 0 or tabuleiro_x >= 10: # verifica se a peça esta em um intervalo entre 0 e 9 para saber se saiu do tabuleiro
                        continue 
                    if tabuleiro_y < 0: #verifica se a peça chego no topo do tabuleiro
                        # Só bloqueia se a peça realmente está caindo, não durante ataque inimigo
                        if not self.exibi_restart:
                            self.bloqueia_peca() # se chegou = bloqueia a peça
                            self.exibi_restart = True # e exibe o restart
                        return
                    if self.mapa[tabuleiro_y][tabuleiro_x] != '': #verifica se a posição no tabuleiro e difernete de vazio
                        self.posicao_forma[1] -= 1 #se for diferente de vazio move a peça para cima
                        # Só bloqueia se a peça realmente está caindo, não durante ataque inimigo
                        if not self.exibi_restart:
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
            if all(self.mapa[y][x] != '' for x in range(10)):
                # coletar recursos da linha antes de removê-la
                for x in range(10):
                    codigo = self.mapa[y][x]
                    recurso = self.recursos(codigo)
                    if recurso:
                        if recurso in self.inventario:
                            self.inventario[recurso] += 1
                        else:
                            self.inventario[recurso] = 1
                self.verificar_slot_por_inventario()
                del self.mapa[y]
                self.mapa.insert(0, [''] * 10)
                remover += 1
                # derrotar inimigos ao completar linha
                self.derrotar_inimigos()
            else:
                y -= 1

        if remover > 0:
            self.adicionar_pontos(remover)
            self.limpar_janela()
            self.tabuleiro()
            pygame.display.update()
                # Exibe se é dia ou noite
            try:
                txt_turno = f"Turno: {self.turno} - {'Dia' if self.dia else 'Noite'}"
                txt_t = self.font.render(txt_turno, True, self.branco)
                self.janela.blit(txt_t, (hold_x, hold_y - txt_t.get_height() - 30))
            except Exception:
                pass
        
    def game_over(self): #verifica se o jogo acabou
        posicao_forma_x = self.posicao_forma[0] #posição x da forma em jogo
        posicao_forma_y = self.posicao_forma[1] #posição y da forma em jogo
        if self.exibi_restart == False:
            for y in range(len(self.layout_forma)):
                for x in range(len(self.layout_forma[0])):
                    if (0 <= posicao_forma_y + y < 20) and (0 <= posicao_forma_x + x < 10):
                        if self.layout_forma[y][x] == 1 and self.mapa[posicao_forma_y + y][posicao_forma_x + x] != '':
                            self.exibi_restart = True
                            self.layout_forma = [[]]
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
            # Zera o inventário (armazém)
            for k in self.inventario:
                self.inventario[k] = 0
            self.fila_fonte.clear() # limpa fila do transportador
            self.exibi_restart = False # não exibe o restart
            self.sort_1peças = False # não é mais a primeira peça
            self.forma_reserva = None
            self.hold_usado = False
            self.nova_forma = True # uma nova forma aparecera
            self.pedidos_ativos = [self.gerar_pedido_aleatorio() for _ in range(3)] # gera 3 pedidos novos
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
    # Ataque dos inimigos à noite
    tetris.ataque_noturno()
    tetris.butao_restart()
    pygame.display.update()
