import pygame  # pyright: ignore[reportMissingImports]
from pygame.locals import *  # pyright: ignore[reportMissingImports]

import random

import time

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600
BLOCK = 10
POS_INICIAL_X = (WINDOWS_WIDTH // 2) // BLOCK * BLOCK
POS_INICIAL_Y = (WINDOWS_HEIGHT // 2) // BLOCK * BLOCK

pontos = 0
velocidade = 10

pygame.font.init()
font = pygame.font.SysFont('arial', 35, True, True) #Negrito e italico
#pygame.font.get_fonts()

def colisao(pos1, pos2):
    return pos1 == pos2

def verifica_margens(pos):
    if 0 <= pos[0] < WINDOWS_WIDTH and 0 <= pos[1] < WINDOWS_HEIGHT:
        return False
    else:
        return True

def gera_posicao_aleatoria():
    x = random.randint(0, (WINDOWS_WIDTH - BLOCK) // BLOCK) * BLOCK
    y = random.randint(0, (WINDOWS_HEIGHT - BLOCK) // BLOCK) * BLOCK
    pos = (x, y)
    
    # Evita posições ocupadas por obstáculos ou pela cobra
    while pos in obstaculo_pos or pos in cobra_pos:
        x = random.randint(0, (WINDOWS_WIDTH - BLOCK) // BLOCK) * BLOCK
        y = random.randint(0, (WINDOWS_HEIGHT - BLOCK) // BLOCK) * BLOCK
        pos = (x, y)
     
    return pos

def game_over():
    font = pygame.font.SysFont('arial', 60, True, True)
    font_button = pygame.font.SysFont('arial', 30, True, True)
    
    gameOver = 'GAME OVER'
    text_over = font.render(gameOver, True, (255,255,255))
    
    # Botão de restart
    restart_text = 'Pressione ESPAÇO para reiniciar'
    restart_surface = font_button.render(restart_text, True, (255,255,255))
    
    # Desenha tela de game over
    window.fill((68, 189, 50))
    window.blit(text_over, (110, 250))
    window.blit(restart_surface, (150, 350))
    
    # Desenha pontuação final
    score_text = f'Pontuação Final: {pontos}'
    score_surface = font_button.render(score_text, True, (255,255,255))
    window.blit(score_surface, (200, 300))
    
    pygame.display.update()
    
    # Aguarda input do usuário
    waiting = True
    while waiting:
        for evento in pygame.event.get():
            if evento.type == QUIT:  # pyright: ignore[reportUndefinedVariable]
                pygame.quit()
                quit()
            elif evento.type == KEYDOWN:  # pyright: ignore[reportUndefinedVariable]
                if evento.key == K_SPACE:  # pyright: ignore[reportUndefinedVariable]
                    waiting = False
                    restart_game()
                elif evento.key == K_ESCAPE:  # pyright: ignore[reportUndefinedVariable]
                    pygame.quit()
                    quit()

def restart_game():
    global pontos, velocidade, cobra_pos, direcao, obstaculo_pos, maca_pos
    
    # Reset das variáveis
    pontos = 0
    velocidade = 10
    direcao = K_LEFT  # pyright: ignore[reportUndefinedVariable]
    obstaculo_pos = []
    
    # Reset da cobra
    cobra_pos = [(POS_INICIAL_X,POS_INICIAL_Y),(POS_INICIAL_X + BLOCK, POS_INICIAL_Y),(POS_INICIAL_X + 2 * BLOCK, POS_INICIAL_Y)]
    
    # Nova posição da maçã
    maca_pos = gera_posicao_aleatoria()

pygame.init()
window = pygame.display.set_mode ((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption('Jogo da Cobrinha')
clock = pygame.time.Clock()

cobra_pos = [(POS_INICIAL_X,POS_INICIAL_Y),(POS_INICIAL_X + BLOCK, POS_INICIAL_Y),(POS_INICIAL_X + 2 * BLOCK, POS_INICIAL_Y)]
cobra_surface = pygame.Surface((BLOCK,BLOCK))
cobra_surface.fill((53,59,72))
direcao = K_LEFT  # pyright: ignore[reportUndefinedVariable]

obstaculo_pos= []
obstaculo_surface = pygame.Surface((BLOCK,BLOCK))
obstaculo_surface.fill((0,0,0))

maca_surface = pygame.Surface((BLOCK,BLOCK))
maca_surface.fill((255, 0, 0))
maca_pos = gera_posicao_aleatoria()

while True:
    clock.tick(velocidade)
    window.fill((68, 189, 50))

    mensagem = f'Pontos:{pontos}'
    texto = font.render(mensagem, True, (255,255,255))

    for evento in pygame.event.get():
        if evento.type == QUIT:  # pyright: ignore[reportUndefinedVariable]
            pygame.quit()
            quit()
        
        elif evento.type == KEYDOWN:  # pyright: ignore[reportUndefinedVariable]
            if evento.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:  # pyright: ignore[reportUndefinedVariable]
                if evento.key == K_UP and direcao == K_DOWN:  # pyright: ignore[reportUndefinedVariable]
                    continue
                elif evento.key == K_DOWN and direcao == K_UP:  # pyright: ignore[reportUndefinedVariable]
                    continue
                elif evento.key == K_RIGHT and direcao == K_LEFT:  # pyright: ignore[reportUndefinedVariable]
                    continue
                elif evento.key == K_LEFT and direcao == K_RIGHT:  # pyright: ignore[reportUndefinedVariable]
                    continue
                else:
                    direcao = evento.key
    
    window.blit(maca_surface, maca_pos)

    if (colisao(cobra_pos[0], maca_pos)):
        cobra_pos.append((-10,-10))
        maca_pos = gera_posicao_aleatoria()
        # Gera obstáculo apenas se não for o primeiro ponto
        if pontos > 0:
            obstaculo_pos.append(gera_posicao_aleatoria())
        pontos += 1
        if pontos % 5 == 0:
            velocidade += 2

    for pos in obstaculo_pos:
        if colisao(cobra_pos[0],pos):
            game_over()
        window.blit(obstaculo_surface, pos)    

    for pos in cobra_pos:
        window.blit(cobra_surface, pos)
    
    for item in range(len(cobra_pos) -1,0,-1):
        if colisao(cobra_pos[0],cobra_pos[item]):
            game_over()
        cobra_pos[item] = cobra_pos[item-1]
    
    if verifica_margens(cobra_pos[0]):
        game_over()
    
    if direcao == K_RIGHT:  # pyright: ignore[reportUndefinedVariable]
       cobra_pos[0] = cobra_pos [0][0] + BLOCK, cobra_pos[0][1] #Movimenta para direita
    
    elif direcao == K_LEFT:  # pyright: ignore[reportUndefinedVariable]
        cobra_pos[0] = cobra_pos [0][0] - BLOCK, cobra_pos[0][1] #Movimenta para esquerda

    elif direcao == K_UP:    # pyright: ignore[reportUndefinedVariable]
        cobra_pos[0] = cobra_pos [0][0], cobra_pos[0][1] - BLOCK #Movimenta para cima

    elif direcao == K_DOWN:  # pyright: ignore[reportUndefinedVariable]
        cobra_pos[0] = cobra_pos [0][0], cobra_pos[0][1] + BLOCK #Movimenta para baixo
    

    window.blit(texto,(420,30))
    
    pygame.display.update()