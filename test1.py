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

    def calcula_largura_janela(self, tam_cel):
        """Retorna a largura total da janela em pixels.

        A fórmula atual reserva espaço para o tabuleiro (10 células) e painéis laterais,
        representados por um multiplicador. Ajuste o multiplicador se quiser mais/menos espaço.
        """
        multiplicador_total = 22
        return tam_cel * multiplicador_total
        
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

    	linhas = 1 + self.turno // 10  # dificuldade escala

    	for _ in range(linhas):
        # remove a linha do topo
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

    def recursos(self, entrada):
        """Retorna o recurso associado a uma cor ou a uma forma.

        Entrada pode ser:
        - tupla RGB (ex.: self.amarelo)
        - nome da forma (ex.: 'forma_1')
        Retorna uma string com o recurso ou None se não houver mapeamento.
        """
        # obter cor a partir do parâmetro
        cor = None
        if isinstance(entrada, str):
            # se for nome de forma, pega a cor da forma
            if entrada in self.formas:
                cor = self.formas[entrada]['cor']
            else:
                # aceita também códigos únicos usados em mapa (ex: 'Y', 'R')
                try:
                    # converte código para cor usando recb_cor se possível
                    cor = self.recb_cor(entrada)
                except Exception:
                    cor = None
        else:
            # assume que é uma tupla RGB
            cor = entrada

        mapping = {
            self.amarelo: 'pedra',
            self.roxo: 'madeira',
            self.azul_c: 'pano',
            self.vermelho: 'ferro',
            self.verde: 'cobre',
            self.azul: 'comida',
            self.laranja: 'barro'
        }

        return mapping.get(cor)
    
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

        x_tabuleiro 