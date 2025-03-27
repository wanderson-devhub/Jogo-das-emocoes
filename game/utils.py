# Funções utilitárias
import math
import random
import pygame
from game.config import LARGURA, ALTURA

def desenhar_botao(superficie, texto, fonte, cor_texto, cor_botao, rect, sombra_cor=(0, 0, 0), hover=False):
    """Desenha um botão com texto e efeito hover"""
    # Desenhar o botão com sombra
    sombra_rect = rect.copy()
    sombra_rect.x += 3
    sombra_rect.y += 3
    pygame.draw.rect(superficie, sombra_cor, sombra_rect, border_radius=10)

    # Desenhar o botão principal
    cor_atual = (cor_botao[0] + 30, cor_botao[1] + 30, cor_botao[2] + 30) if hover else cor_botao
    pygame.draw.rect(superficie, cor_atual, rect, border_radius=10)

    # Desenhar o texto
    texto_renderizado = fonte.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=rect.center)
    superficie.blit(texto_renderizado, texto_rect)

    return rect

def desenhar_texto_com_sombra(superficie, texto, fonte, cor, posicao, sombra_cor=(0, 0, 0)):
    """Desenha texto com sombra para melhor visibilidade"""
    sombra = fonte.render(texto, True, sombra_cor)
    superficie.blit(sombra, (posicao[0] + 2, posicao[1] + 2))
    texto_renderizado = fonte.render(texto, True, cor)
    superficie.blit(texto_renderizado, posicao)


def calcular_distancia(x1, y1, x2, y2):
    """Calcula a distância entre dois pontos"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def gerar_posicoes_emocoes(quantidade, distancia_minima):
    """Gera posições para as emoções com distância mínima entre elas"""
    posicoes = []
    tentativas_maximas = 100  # Limite de tentativas para evitar loop infinito

    for _ in range(quantidade):
        posicao_valida = False
        tentativas = 0

        while not posicao_valida and tentativas < tentativas_maximas:
            # Gerar posição aleatória
            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)

            # Verificar distância com outras posições
            posicao_valida = True
            for pos in posicoes:
                if calcular_distancia(x, y, pos[0], pos[1]) < distancia_minima:
                    posicao_valida = False
                    break

            tentativas += 1

        if posicao_valida:
            posicoes.append((x, y))
        else:
            # Se não conseguir encontrar posição válida após várias tentativas,
            # relaxar a restrição de distância
            x = random.randint(100, LARGURA - 100)
            y = random.randint(100, ALTURA - 100)
            posicoes.append((x, y))

    return posicoes