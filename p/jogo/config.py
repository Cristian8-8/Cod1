import pygame 

# grade do jogo
coluna = 10
linhas = 20
tam_celula = 40
larg_jogo = coluna*tam_celula
alt_jogo = linhas*tam_celula

#barra lateral
larg_barra_lat = 200
vis_barra_lat = 0.7
pontos_barra_lat = 1 - vis_barra_lat

# janela do jogo
dist_borda = 40 
larg_janela = larg_jogo + dist_borda*3
alt_janela = alt_jogo + dist_borda*2