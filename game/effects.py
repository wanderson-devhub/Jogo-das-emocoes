# Efeitos visuais e especiais
import random
import math
import pygame
from game.entities import Particle


def aplicar_efeito_emocao(emocao, jogador, particulas, camera_shake):
    """Aplica efeitos visuais baseados na emoção atual"""
    if emocao.texto == "Alegria":
        # Partículas brilhantes ao redor da tela
        if random.random() < 0.2:
            for _ in range(3):
                x = random.randint(0, pygame.display.get_surface().get_width())
                y = random.randint(0, pygame.display.get_surface().get_height())
                p = Particle(x, y, emocao.cor, random.uniform(0.5, 2), random.randint(5, 15), random.randint(30, 60))
                particulas.append(p)

    elif emocao.texto == "Tristeza":
        # Efeito de chuva
        if random.random() < 0.3:
            for _ in range(2):
                x = random.randint(0, pygame.display.get_surface().get_width())
                y = random.randint(-10, 0)
                p = Particle(x, y, emocao.cor, 3, 3, 60)
                p.angulo = math.pi / 2  # Cair para baixo
                particulas.append(p)

    elif emocao.texto == "Raiva":
        # Efeito de tremor na tela
        if emocao.intensidade > 50:
            camera_shake = max(camera_shake, emocao.intensidade / 20)

        # Partículas de fogo
        if random.random() < 0.2:
            for _ in range(2):
                x = random.randint(0, pygame.display.get_surface().get_width())
                y = pygame.display.get_surface().get_height() - random.randint(0, 50)
                p = Particle(x, y, emocao.cor, random.uniform(1, 3), random.randint(10, 20), random.randint(20, 40))
                p.angulo = -math.pi / 2  # Subir
                particulas.append(p)

    elif emocao.texto == "Medo":
        # Escurecer os cantos da tela
        s = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
        for i in range(100):
            alpha = int(2.55 * i * (emocao.intensidade / 100))
            pygame.draw.rect(s, (0, 0, 0, alpha),
                             (i, i, pygame.display.get_surface().get_width() - 2 * i,
                              pygame.display.get_surface().get_height() - 2 * i), 1)
        pygame.display.get_surface().blit(s, (0, 0))

        # Sombras aleatórias
        if random.random() < 0.05 and emocao.intensidade > 30:
            x = random.choice([0, pygame.display.get_surface().get_width()])
            y = random.randint(0, pygame.display.get_surface().get_height())
            tamanho = random.randint(50, 100)
            s = pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)
            pygame.draw.circle(s, (0, 0, 0, 100), (tamanho // 2, tamanho // 2), tamanho // 2)
            pygame.display.get_surface().blit(s, (x - tamanho // 2, y - tamanho // 2))

    elif emocao.texto == "Paz":
        # Efeito de brilho suave
        s = pygame.Surface(pygame.display.get_surface().get_size(), pygame.SRCALPHA)
        raio = int(200 + 50 * math.sin(pygame.time.get_ticks() * 0.001))
        pygame.draw.circle(s, (255, 255, 255, 30), (jogador.x, jogador.y), raio)
        pygame.display.get_surface().blit(s, (0, 0))

        # Partículas de luz
        if random.random() < 0.1:
            for _ in range(2):
                angulo = random.uniform(0, 2 * math.pi)
                distancia = random.randint(50, 150)
                x = jogador.x + math.cos(angulo) * distancia
                y = jogador.y + math.sin(angulo) * distancia
                p = Particle(x, y, emocao.cor, random.uniform(0.5, 1.5), random.randint(5, 15), random.randint(40, 80))
                particulas.append(p)

    return camera_shake


def aplicar_efeito_powerup(powerup, tela, jogador, pulso):
    """Aplica efeitos visuais para power-ups ativos"""
    if powerup.efeito == "velocidade" and jogador.powerups_ativos["velocidade"]["ativo"]:
        # Efeito de rastro para velocidade
        s = pygame.Surface((jogador.tamanho * 4, jogador.tamanho * 4), pygame.SRCALPHA)
        for i in range(3):
            alpha = 100 - i * 30
            tamanho = jogador.tamanho - i * 3
            pygame.draw.circle(s, (50, 255, 50, alpha), (jogador.tamanho * 2, jogador.tamanho * 2), tamanho)
        tela.blit(s, (jogador.x - jogador.tamanho * 2, jogador.y - jogador.tamanho * 2))

    elif powerup.efeito == "pontos":
        # Efeito de brilho para multiplicador de pontos
        raio = 50 + int(10 * math.sin(pulso * 2))
        s = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 50, 50), (raio, raio), raio)
        tela.blit(s, (jogador.x - raio, jogador.y - raio))

    elif powerup.efeito == "congelar":
        # Efeito de congelamento ao redor da tela
        s = pygame.Surface(tela.get_size(), pygame.SRCALPHA)
        for i in range(20):
            alpha = 5
            pygame.draw.rect(s, (200, 200, 255, alpha),
                             (i, i, tela.get_width() - 2 * i, tela.get_height() - 2 * i), 1)
        tela.blit(s, (0, 0))


def desenhar_indicadores_powerup(tela, fontes, jogador, powerups_ativos):
    """Desenha indicadores para power-ups ativos"""
    y = 80  # Posição inicial

    for powerup in powerups_ativos:
        if powerups_ativos[powerup]["ativo"]:
            # Criar um painel para o indicador
            painel = pygame.Surface((200, 30), pygame.SRCALPHA)
            painel.fill((0, 0, 0, 150))
            tela.blit(painel, (10, y))

            # Texto do power-up
            if powerup == "velocidade":
                texto = fontes['pequena'].render(
                    f"Velocidade: {int(powerups_ativos[powerup]['tempo_restante'] / 1000)}s", True, (50, 255, 50))
            elif powerup == "pontos":
                texto = fontes['pequena'].render(
                    f"2x Pontos: {int(powerups_ativos[powerup]['tempo_restante'] / 1000)}s", True, (255, 255, 50))
            elif powerup == "congelar":
                texto = fontes['pequena'].render(
                    f"Congelamento: {int(powerups_ativos[powerup]['tempo_restante'] / 1000)}s", True, (50, 150, 255))

            tela.blit(texto, (20, y + 5))
            y += 35  # Espaçamento para o próximo indicador