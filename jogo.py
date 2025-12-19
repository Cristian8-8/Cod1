import pygame
from pygame.locals import *
from sys import exit

larg_janela = 600
alt_janela = 480
x = larg_janela/2
y = 0
vel_y = 1

pygame.init()
tela = pygame.display.set_mode((larg_janela,alt_janela))
pygame.display.set_caption("JOGO")
Taxa_de_frames = pygame.time.Clock()

while True:
    Taxa_de_frames.tick(60)
    tela.fill((0,0,0))
    # Comando para fecha o jogo
    for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit() 
    # movimentação
    if pygame.key.get_pressed()[K_a]:
        x = x - 5
    if pygame.key.get_pressed()[K_d]:
        x = x + 5
    if pygame.key.get_pressed()[K_s]:
        y = y + 5
    if pygame.key.get_pressed()[K_w]:
        y = y - 5
    # objetos na tela
    red_quadrado = pygame.draw.rect(tela,(255,0,0),(x,y,40,40))
    linha = pygame.draw.line(tela,(255,255,255),(0,400),(600,400))
    
    # "animação do quadrado"
    y += 2
        
    if red_quadrado.colliderect(linha):
        vel_y = 0
        y = linha.top - 40
    

    

    
    
    
    
    pygame.display.update()