# Classes para entidades do jogo (jogador, emoções, partículas, power-ups)
import math
import random
import pygame
from game.config import LARGURA, ALTURA, JOGADOR_TAMANHO, JOGADOR_VELOCIDADE, COR_JOGADOR
from game.utils import calcular_distancia


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanho = JOGADOR_TAMANHO
        self.velocidade = JOGADOR_VELOCIDADE
        self.velocidade_original = JOGADOR_VELOCIDADE
        self.rotacao = 0
        self.brilho = 0  # Para efeito de brilho pulsante

        # Power-ups ativos
        self.powerups_ativos = {
            "velocidade": {"ativo": False, "tempo_restante": 0, "valor": 1}
        }

    def mover(self, teclas):
        """Move o jogador com base nas teclas pressionadas"""
        movimento_x, movimento_y = 0, 0

        # Aplicar modificador de velocidade se o power-up estiver ativo
        velocidade_atual = self.velocidade
        if self.powerups_ativos["velocidade"]["ativo"]:
            velocidade_atual *= self.powerups_ativos["velocidade"]["valor"]

        if teclas[pygame.K_LEFT] and self.x > self.tamanho:
            movimento_x = -velocidade_atual
            self.rotacao = 90
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - self.tamanho:
            movimento_x = velocidade_atual
            self.rotacao = 270
        if teclas[pygame.K_UP] and self.y > self.tamanho:
            movimento_y = -velocidade_atual
            self.rotacao = 0
        if teclas[pygame.K_DOWN] and self.y < ALTURA - self.tamanho:
            movimento_y = velocidade_atual
            self.rotacao = 180

        # Movimento diagonal
        if movimento_x != 0 and movimento_y != 0:
            movimento_x *= 0.7071  # 1/sqrt(2)
            movimento_y *= 0.7071

            # Ajustar rotação para diagonais
            if movimento_x < 0 and movimento_y < 0:
                self.rotacao = 45
            elif movimento_x > 0 and movimento_y < 0:
                self.rotacao = 315
            elif movimento_x < 0 and movimento_y > 0:
                self.rotacao = 135
            elif movimento_x > 0 and movimento_y > 0:
                self.rotacao = 225

        self.x += movimento_x
        self.y += movimento_y

        # Limitar posição do jogador
        self.x = max(self.tamanho, min(LARGURA - self.tamanho, self.x))
        self.y = max(self.tamanho, min(ALTURA - self.tamanho, self.y))

    def atualizar(self, delta_tempo):
        """Atualiza o estado do jogador"""
        self.brilho = (self.brilho + 0.05) % (2 * math.pi)

        # Atualizar power-ups ativos
        for powerup, dados in self.powerups_ativos.items():
            if dados["ativo"]:
                dados["tempo_restante"] -= delta_tempo
                if dados["tempo_restante"] <= 0:
                    dados["ativo"] = False
                    dados["valor"] = 1  # Resetar para o valor padrão

    def ativar_powerup(self, tipo, duracao, valor):
        """Ativa um power-up para o jogador"""
        if tipo == "velocidade":
            self.powerups_ativos["velocidade"]["ativo"] = True
            self.powerups_ativos["velocidade"]["tempo_restante"] = duracao
            self.powerups_ativos["velocidade"]["valor"] = valor

    def desenhar(self, tela, assets, camera_offset_x=0, camera_offset_y=0, cor_aura=None):
        """Desenha o jogador na tela"""
        try:
            # Rotacionar a imagem do jogador
            jogador_rotacionado = pygame.transform.rotate(assets.imagens['jogador'], self.rotacao)

            # Desenhar aura ao redor do jogador para destacá-lo
            raio_aura = self.tamanho + 5 + int(3 * math.sin(self.brilho))
            s = pygame.Surface((raio_aura * 2, raio_aura * 2), pygame.SRCALPHA)

            # Cor da aura baseada na emoção atual ou branca se nenhuma
            if cor_aura is None:
                cor_aura = COR_JOGADOR

            # Desenhar aura com transparência
            pygame.draw.circle(s, cor_aura + (150,), (raio_aura, raio_aura), raio_aura)
            tela.blit(s, (self.x - raio_aura + camera_offset_x,
                          self.y - raio_aura + camera_offset_y))

            # Desenhar o jogador
            tela.blit(jogador_rotacionado,
                      (self.x - jogador_rotacionado.get_width() // 2 + camera_offset_x,
                       self.y - jogador_rotacionado.get_height() // 2 + camera_offset_y))
        except:
            # Fallback para círculo com destaque
            # Desenhar aura ao redor do jogador
            raio_aura = self.tamanho + 5 + int(3 * math.sin(self.brilho))
            pygame.draw.circle(tela, (255, 255, 255, 150),
                               (self.x + camera_offset_x, self.y + camera_offset_y), raio_aura)

            # Desenhar o jogador com cor destacada
            pygame.draw.circle(tela, COR_JOGADOR,
                               (self.x + camera_offset_x, self.y + camera_offset_y), self.tamanho)


class Emotion:
    def __init__(self, texto, cor, x, y, descricao, comportamento="estatico"):
        self.texto = texto
        self.cor = cor
        self.x = x
        self.y = y
        self.ativa = False
        self.intensidade = 0
        self.particulas = []
        self.descricao = descricao
        self.som_tocando = False
        self.comportamento = comportamento
        self.velocidade = 0.5  # Velocidade base para movimento
        self.direcao = random.uniform(0, 2 * math.pi)  # Direção aleatória inicial
        self.tempo_mudanca_direcao = 0
        self.congelado = False
        self.missao_alvo = False
        self.tempo_missao = 0
        self.missao_completa = False

    def verificar_proximidade(self, jogador, distancia_ativacao):
        """Verifica se o jogador está próximo da emoção"""
        distancia = calcular_distancia(jogador.x, jogador.y, self.x, self.y)
        return distancia < distancia_ativacao

    def atualizar(self, jogador, distancia_ativacao, delta_tempo, dificuldade=1, emocoes_congeladas=False,
                  modo_passeio=False):
        """Atualiza o estado da emoção"""
        # Movimento da emoção (se não estiver congelada e não estiver no modo passeio)
        if not self.congelado and not emocoes_congeladas and self.comportamento != "estatico" and not modo_passeio:
            self._mover(jogador, delta_tempo, dificuldade)

        # Verificar proximidade com o jogador
        proximidade = self.verificar_proximidade(jogador, distancia_ativacao)

        # Atualizar estado de ativação
        if proximidade:
            if not self.ativa:
                # Primeira ativação
                self.ativa = True
                return True  # Indica que a emoção foi ativada neste frame

            # Aumentar intensidade da emoção
            self.intensidade = min(100, self.intensidade + 1)

            # Atualizar tempo de missão se for alvo
            if self.missao_alvo and not self.missao_completa:
                self.tempo_missao += delta_tempo

            return False  # Emoção já estava ativa
        else:
            # Diminuir intensidade gradualmente
            self.intensidade = max(0, self.intensidade - 0.5)
            self.ativa = False

            # Resetar tempo de missão se não estiver próximo
            if self.missao_alvo and not self.missao_completa:
                self.tempo_missao = 0

            return False

    def _mover(self, jogador, delta_tempo, dificuldade):
        """Move a emoção com base em seu comportamento"""
        # Aplicar dificuldade à velocidade - aumenta com o tempo
        velocidade_atual = self.velocidade * dificuldade

        # Atualizar tempo para mudança de direção
        self.tempo_mudanca_direcao -= delta_tempo
        if self.tempo_mudanca_direcao <= 0:
            self.direcao = random.uniform(0, 2 * math.pi)
            self.tempo_mudanca_direcao = random.uniform(1000, 3000)  # 1-3 segundos

        # Comportamento de fuga
        if self.comportamento == "fuga" and self.verificar_proximidade(jogador, 200):
            # Calcular ângulo de fuga (oposto à direção do jogador)
            angulo_jogador = math.atan2(self.y - jogador.y, self.x - jogador.x)
            self.direcao = angulo_jogador
            velocidade_atual *= 2.5  # Fugir mais rápido

        # Aplicar movimento
        dx = math.cos(self.direcao) * velocidade_atual
        dy = math.sin(self.direcao) * velocidade_atual

        # Atualizar posição
        self.x += dx
        self.y += dy

        # Manter dentro dos limites da tela
        if self.x < 50:
            self.x = 50
            self.direcao = random.uniform(-math.pi / 2, math.pi / 2)
        elif self.x > LARGURA - 50:
            self.x = LARGURA - 50
            self.direcao = random.uniform(math.pi / 2, 3 * math.pi / 2)

        if self.y < 50:
            self.y = 50
            self.direcao = random.uniform(0, math.pi)
        elif self.y > ALTURA - 50:
            self.y = ALTURA - 50
            self.direcao = random.uniform(math.pi, 2 * math.pi)

    def desenhar(self, tela, assets, fontes, pulso, camera_offset_x=0, camera_offset_y=0):
        """Desenha a emoção na tela"""
        # Escolher a fonte com base no estado da emoção
        if self.ativa:
            tamanho_texto = int(24 + 10 * math.sin(pulso))
            fonte_pulso = pygame.font.SysFont('Arial', tamanho_texto)
            texto = fonte_pulso.render(self.texto, True, self.cor)
        else:
            texto = fontes['normal'].render(self.texto, True, self.cor)

        # Desenhar imagem da emoção ou círculo como fallback
        try:
            img = assets.imagens['emocoes'][self.texto]
            tamanho_img = int(60 + 10 * math.sin(pulso) if self.ativa else 60)
            img_scaled = pygame.transform.scale(img, (tamanho_img, tamanho_img))

            # Adicionar efeito de brilho se for alvo de missão
            if self.missao_alvo and not self.missao_completa:
                # Criar uma superfície para o brilho
                brilho_tamanho = tamanho_img + 20
                brilho = pygame.Surface((brilho_tamanho, brilho_tamanho), pygame.SRCALPHA)

                # Desenhar círculos concêntricos pulsantes
                for i in range(3):
                    raio = int(brilho_tamanho / 2 - i * 5 + 5 * math.sin(pulso * 2))
                    alpha = max(0, 150 - i * 50)
                    pygame.draw.circle(brilho, self.cor + (alpha,),
                                       (brilho_tamanho // 2, brilho_tamanho // 2), raio)

                # Desenhar o brilho
                tela.blit(brilho, (self.x - brilho_tamanho // 2 + camera_offset_x,
                                   self.y - brilho_tamanho // 2 - 30 + camera_offset_y))

            # Desenhar a imagem da emoção
            tela.blit(img_scaled, (self.x - tamanho_img // 2 + camera_offset_x,
                                   self.y - tamanho_img // 2 - 30 + camera_offset_y))

            # Desenhar indicador de congelamento se estiver congelada
            if self.congelado:
                pygame.draw.circle(tela, (200, 200, 255, 150),
                                   (self.x + camera_offset_x, self.y - 30 + camera_offset_y),
                                   tamanho_img // 2 + 5, 3)
        except:
            # Fallback para círculo
            raio = int(30 + 5 * math.sin(pulso) if self.ativa else 30)
            pygame.draw.circle(tela, self.cor,
                               (self.x + camera_offset_x, self.y + camera_offset_y), raio)

        # Desenhar texto da emoção
        tela.blit(texto, (self.x - texto.get_width() // 2 + camera_offset_x,
                          self.y - texto.get_height() // 2 + 30 + camera_offset_y))

        # Desenhar barra de intensidade se a emoção já foi sentida
        if self.intensidade > 0:
            largura_barra = 50
            altura_barra = 5
            pygame.draw.rect(tela, (255, 255, 255),
                             (self.x - largura_barra // 2 + camera_offset_x,
                              self.y + 50 + camera_offset_y,
                              largura_barra, altura_barra))
            pygame.draw.rect(tela, self.cor,
                             (self.x - largura_barra // 2 + camera_offset_x,
                              self.y + 50 + camera_offset_y,
                              int(largura_barra * (self.intensidade / 100)), altura_barra))

        # Desenhar barra de progresso da missão se for alvo
        if self.missao_alvo and not self.missao_completa:
            from game.config import TEMPO_MISSAO
            progresso = min(1.0, self.tempo_missao / TEMPO_MISSAO)

            largura_barra = 60
            altura_barra = 8

            # Fundo da barra
            pygame.draw.rect(tela, (50, 50, 50),
                             (self.x - largura_barra // 2 + camera_offset_x,
                              self.y + 60 + camera_offset_y,
                              largura_barra, altura_barra))

            # Progresso
            pygame.draw.rect(tela, (50, 255, 50),
                             (self.x - largura_barra // 2 + camera_offset_x,
                              self.y + 60 + camera_offset_y,
                              int(largura_barra * progresso), altura_barra))


class PowerUp:
    def __init__(self, texto, cor, x, y, descricao, efeito, duracao, valor):
        self.texto = texto
        self.cor = cor
        self.x = x
        self.y = y
        self.descricao = descricao
        self.efeito = efeito
        self.duracao = duracao
        self.valor = valor
        self.ativo = True
        self.tempo_reaparecimento = 0
        self.brilho = 0

    def verificar_colisao(self, jogador):
        """Verifica se o jogador colidiu com o power-up"""
        if not self.ativo:
            return False

        distancia = calcular_distancia(jogador.x, jogador.y, self.x, self.y)
        return distancia < jogador.tamanho + 20

    def atualizar(self, delta_tempo):
        """Atualiza o estado do power-up"""
        self.brilho = (self.brilho + 0.05) % (2 * math.pi)

        # Se não estiver ativo, atualizar tempo de reaparecimento
        if not self.ativo:
            self.tempo_reaparecimento -= delta_tempo
            if self.tempo_reaparecimento <= 0:
                self.ativo = True

    def coletar(self, tempo_reaparecimento):
        """Coleta o power-up e define o tempo para reaparecer"""
        self.ativo = False
        self.tempo_reaparecimento = tempo_reaparecimento

        # Gerar nova posição para quando reaparecer
        self.x = random.randint(100, LARGURA - 100)
        self.y = random.randint(100, ALTURA - 100)

    def desenhar(self, tela, assets, fontes, camera_offset_x=0, camera_offset_y=0):
        """Desenha o power-up na tela"""
        if not self.ativo:
            return

        try:
            # Desenhar imagem do power-up
            img = assets.imagens['powerups'][self.texto]
            tamanho_img = 40 + int(5 * math.sin(self.brilho))
            img_scaled = pygame.transform.scale(img, (tamanho_img, tamanho_img))

            # Criar efeito de brilho
            brilho_tamanho = tamanho_img + 20
            brilho = pygame.Surface((brilho_tamanho, brilho_tamanho), pygame.SRCALPHA)

            # Desenhar círculos concêntricos pulsantes
            for i in range(3):
                raio = int(brilho_tamanho / 2 - i * 5 + 5 * math.sin(self.brilho * 2))
                alpha = max(0, 150 - i * 50)
                pygame.draw.circle(brilho, self.cor + (alpha,),
                                   (brilho_tamanho // 2, brilho_tamanho // 2), raio)

            # Desenhar o brilho
            tela.blit(brilho, (self.x - brilho_tamanho // 2 + camera_offset_x,
                               self.y - brilho_tamanho // 2 + camera_offset_y))

            # Desenhar a imagem do power-up
            tela.blit(img_scaled, (self.x - tamanho_img // 2 + camera_offset_x,
                                   self.y - tamanho_img // 2 + camera_offset_y))
        except:
            # Fallback para círculo
            raio = 20 + int(5 * math.sin(self.brilho))
            pygame.draw.circle(tela, self.cor,
                               (self.x + camera_offset_x, self.y + camera_offset_y), raio)

        # Desenhar texto flutuante com o nome do power-up
        texto = fontes['pequena'].render(self.texto, True, self.cor)
        tela.blit(texto, (self.x - texto.get_width() // 2 + camera_offset_x,
                          self.y + 25 + camera_offset_y))


class Particle:
    def __init__(self, x, y, cor, velocidade=1, tamanho=5, vida=30):
        self.x = x
        self.y = y
        self.cor = cor
        self.tamanho = tamanho
        self.vida = vida
        self.vida_max = vida
        self.velocidade = velocidade
        self.angulo = random.uniform(0, 2 * math.pi)

    def atualizar(self):
        """Atualiza o estado da partícula"""
        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade
        self.vida -= 1
        self.tamanho = int(self.tamanho * (self.vida / self.vida_max))
        return self.vida > 0

    def desenhar(self, superficie, particula_img):
        """Desenha a partícula na tela"""
        alpha = int(255 * (self.vida / self.vida_max))
        if alpha <= 0:
            return

        # Desenhar usando imagem ou círculo
        try:
            img_temp = particula_img.copy()
            img_temp.fill((0, 0, 0, 0))
            img_temp.blit(particula_img, (0, 0))
            img_temp.set_alpha(alpha)
            img_temp = pygame.transform.scale(img_temp, (self.tamanho, self.tamanho))
            superficie.blit(img_temp, (int(self.x - self.tamanho / 2), int(self.y - self.tamanho / 2)))
        except:
            # Fallback para círculo se a imagem falhar
            s = pygame.Surface((self.tamanho * 2, self.tamanho * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.cor + (alpha,), (self.tamanho, self.tamanho), self.tamanho)
            superficie.blit(s, (int(self.x - self.tamanho), int(self.y - self.tamanho)))


def criar_particulas_emocao(emocao, quantidade=5):
    """Cria partículas para uma emoção"""
    for _ in range(quantidade):
        velocidade = random.uniform(0.5, 2)
        tamanho = random.randint(5, 15)
        vida = random.randint(20, 60)
        particula = Particle(emocao.x, emocao.y, emocao.cor, velocidade, tamanho, vida)
        emocao.particulas.append(particula)


def criar_particulas_jogador(jogador, particulas, quantidade=1, cor=None):
    """Cria partículas ao redor do jogador"""
    if cor is None:
        cor = COR_JOGADOR

    for _ in range(quantidade):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(jogador.tamanho, jogador.tamanho + 10)
        x = jogador.x + math.cos(angulo) * distancia
        y = jogador.y + math.sin(angulo) * distancia

        velocidade = random.uniform(0.2, 1.0)
        tamanho = random.randint(3, 8)
        vida = random.randint(10, 30)
        particula = Particle(x, y, cor, velocidade, tamanho, vida)
        particulas.append(particula)


def criar_particulas_powerup(powerup, particulas, quantidade=10):
    """Cria partículas para um power-up coletado"""
    for _ in range(quantidade):
        angulo = random.uniform(0, 2 * math.pi)
        distancia = random.uniform(5, 30)
        x = powerup.x + math.cos(angulo) * distancia
        y = powerup.y + math.sin(angulo) * distancia

        velocidade = random.uniform(1.0, 3.0)
        tamanho = random.randint(5, 15)
        vida = random.randint(20, 40)
        particula = Particle(x, y, powerup.cor, velocidade, tamanho, vida)
        particulas.append(particula)

