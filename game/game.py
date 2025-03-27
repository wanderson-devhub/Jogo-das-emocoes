# Classe principal do jogo
import sys
import random
import pygame
from game.config import (
    LARGURA, ALTURA, TITULO, TEMPO_JOGO, DISTANCIA_ATIVACAO, DISTANCIA_MINIMA_EMOCOES,
    DEFINICOES_EMOCOES, DEFINICOES_POWERUPS, TEMPO_REAPARECIMENTO_POWERUP, TEMPO_MISSAO,
    MODO_PASSEIO, MODO_DESAFIO, MODO_AVENTUREIRO, carregar_fontes
)
from game.assets import AssetManager
from game.audio import AudioManager
from game.entities import (
    Player, Emotion, PowerUp, criar_particulas_emocao, criar_particulas_jogador, criar_particulas_powerup
)
from game.utils import gerar_posicoes_emocoes
from game.renderer import (
    desenhar_tela_menu, desenhar_tela_instrucoes, desenhar_tela_fim_jogo,
    desenhar_interface, desenhar_indicadores_powerup
)
from game.effects import aplicar_efeito_emocao, aplicar_efeito_powerup


class Game:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()

        # Configurar tela
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption(TITULO)

        # Carregar recursos
        self.assets = AssetManager()
        self.audio = AudioManager(self.assets)

        # Carregar fontes
        self.fontes = carregar_fontes()

        # Inicializar variáveis do jogo
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.estado = "menu"  # menu, instrucoes, jogando, fim_jogo
        self.modo_jogo = MODO_PASSEIO

        # Efeito de transição
        self.alpha_transicao = 255
        self.transicao_ativa = True

        # Efeito de câmera
        self.camera_shake = 0
        self.camera_offset_x, self.camera_offset_y = 0, 0

        # Efeito de pulso
        self.pulso = 0
        self.pulso_crescendo = True

        # Pontuação e tempo
        self.pontuacao = 0
        self.tempo_inicio = pygame.time.get_ticks()
        self.tempo_restante = TEMPO_JOGO

        # Variáveis para o menu
        self.botoes_menu = []
        self.botao_hover = -1
        self._criar_botoes_menu()

        # Inicializar entidades
        self.inicializar_entidades()

        # Variáveis para modos de jogo
        self.dificuldade = 1.0
        self.tempo_ultima_atualizacao_dificuldade = pygame.time.get_ticks()
        self.emocoes_congeladas = False
        self.tempo_congelamento = 0
        self.multiplicador_pontos = 1
        self.tempo_multiplicador = 0
        self.missao_atual = None
        self.tempo_ultima_missao = 0
        self.emocoes_ativas = 2  # Começar com 2 emoções no modo desafio

        # Iniciar música de fundo
        self.audio.iniciar_musica_fundo()

    def _criar_botoes_menu(self):
        """Cria os botões do menu principal"""
        largura_botao = 300
        altura_botao = 60
        espacamento = 20
        x = LARGURA // 2 - largura_botao // 2
        y_inicial = 250

        self.botoes_menu = [
            ("Modo Passeio", pygame.Rect(x, y_inicial, largura_botao, altura_botao)),
            ("Modo Desafio", pygame.Rect(x, y_inicial + altura_botao + espacamento, largura_botao, altura_botao)),
            ("Modo Aventureiro",
             pygame.Rect(x, y_inicial + 2 * (altura_botao + espacamento), largura_botao, altura_botao)),
            ("Sair", pygame.Rect(x, y_inicial + 3 * (altura_botao + espacamento), largura_botao, altura_botao))
        ]

    def inicializar_entidades(self):
        """Inicializa as entidades do jogo"""
        # Jogador
        self.jogador = Player(LARGURA // 2, ALTURA // 2)

        # Partículas
        self.particulas = []

        # Gerar posições para as emoções com distância mínima
        posicoes_emocoes = gerar_posicoes_emocoes(len(DEFINICOES_EMOCOES), DISTANCIA_MINIMA_EMOCOES)

        # Emoções
        self.emocoes = []
        for i, def_emocao in enumerate(DEFINICOES_EMOCOES):
            emocao = Emotion(
                def_emocao["texto"],
                def_emocao["cor"],
                posicoes_emocoes[i][0],
                posicoes_emocoes[i][1],
                def_emocao["descricao"],
                def_emocao["comportamento"]
            )
            self.emocoes.append(emocao)

        # Power-ups (apenas para o modo aventureiro)
        self.powerups = []
        if self.modo_jogo == MODO_AVENTUREIRO:
            posicoes_powerups = gerar_posicoes_emocoes(len(DEFINICOES_POWERUPS), DISTANCIA_MINIMA_EMOCOES)

            for i, def_powerup in enumerate(DEFINICOES_POWERUPS):
                powerup = PowerUp(
                    def_powerup["texto"],
                    def_powerup["cor"],
                    posicoes_powerups[i][0],
                    posicoes_powerups[i][1],
                    def_powerup["descricao"],
                    def_powerup["efeito"],
                    def_powerup["duracao"],
                    def_powerup["valor"]
                )
                self.powerups.append(powerup)

    def reiniciar_jogo(self):
        """Reinicia o jogo"""
        # Resetar pontuação e tempo
        self.pontuacao = 0
        self.tempo_inicio = pygame.time.get_ticks()
        self.tempo_restante = TEMPO_JOGO
        self.estado = "instrucoes"

        # Resetar variáveis de modo
        self.dificuldade = 1.0
        self.tempo_ultima_atualizacao_dificuldade = pygame.time.get_ticks()
        self.emocoes_congeladas = False
        self.tempo_congelamento = 0
        self.multiplicador_pontos = 1
        self.tempo_multiplicador = 0
        self.missao_atual = None
        self.tempo_ultima_missao = 0
        self.emocoes_ativas = 2  # Começar com 2 emoções no modo desafio

        # Resetar jogador
        self.jogador = Player(LARGURA // 2, ALTURA // 2)

        # Limpar partículas
        self.particulas = []

        # Gerar novas posições para as emoções com distância mínima
        posicoes_emocoes = gerar_posicoes_emocoes(len(DEFINICOES_EMOCOES), DISTANCIA_MINIMA_EMOCOES)

        # Resetar emoções com novas posições
        for i, emocao in enumerate(self.emocoes):
            emocao.x = posicoes_emocoes[i][0]
            emocao.y = posicoes_emocoes[i][1]
            emocao.ativa = False
            emocao.intensidade = 0
            emocao.particulas = []
            emocao.som_tocando = False
            emocao.congelado = False
            emocao.missao_alvo = False
            emocao.tempo_missao = 0
            emocao.missao_completa = False

        # Resetar power-ups (apenas para o modo aventureiro)
        self.powerups = []
        if self.modo_jogo == MODO_AVENTUREIRO:
            posicoes_powerups = gerar_posicoes_emocoes(len(DEFINICOES_POWERUPS), DISTANCIA_MINIMA_EMOCOES)

            for i, def_powerup in enumerate(DEFINICOES_POWERUPS):
                powerup = PowerUp(
                    def_powerup["texto"],
                    def_powerup["cor"],
                    posicoes_powerups[i][0],
                    posicoes_powerups[i][1],
                    def_powerup["descricao"],
                    def_powerup["efeito"],
                    def_powerup["duracao"],
                    def_powerup["valor"]
                )
                self.powerups.append(powerup)

        # Reiniciar música de fundo
        self.audio.emocao_tocando_som = None
        self.audio.retomar_musica_fundo()

        # Efeito de transição
        self.alpha_transicao = 255
        self.transicao_ativa = True

    def voltar_ao_menu(self):
        """Volta para o menu principal"""
        self.estado = "menu"
        self.audio.parar_todos_sons()
        self.audio.retomar_musica_fundo()

    def processar_eventos(self):
        """Processa eventos do Pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if self.estado == "jogando":
                        self.voltar_ao_menu()
                    else:
                        self.rodando = False

                elif evento.key == pygame.K_SPACE and self.estado == "instrucoes":
                    self.estado = "jogando"
                    self.tempo_inicio = pygame.time.get_ticks()
                    self.transicao_ativa = True
                    self.alpha_transicao = 255

                # Corrigido: Verificar se estamos no estado fim_jogo antes de verificar teclas específicas
                elif self.estado == "fim_jogo":
                    if evento.key == pygame.K_r:
                        self.reiniciar_jogo()
                    elif evento.key == pygame.K_m:
                        self.voltar_ao_menu()

            # Evento para reiniciar a música quando ela termina
            elif evento.type == pygame.USEREVENT + 1:
                if self.estado == "jogando" or self.estado == "menu":
                    self.audio.retomar_musica_fundo()

            elif evento.type == pygame.MOUSEMOTION and self.estado == "menu":
                # Verificar hover nos botões
                mouse_pos = pygame.mouse.get_pos()
                self.botao_hover = -1
                for i, (_, rect) in enumerate(self.botoes_menu):
                    if rect.collidepoint(mouse_pos):
                        self.botao_hover = i
                        break

            elif evento.type == pygame.MOUSEBUTTONDOWN and self.estado == "menu":
                # Verificar clique nos botões
                mouse_pos = pygame.mouse.get_pos()
                for i, (_, rect) in enumerate(self.botoes_menu):
                    if rect.collidepoint(mouse_pos):
                        self.audio.tocar_som_interface("selecao")
                        if i == 0:  # Modo Passeio
                            self.modo_jogo = MODO_PASSEIO
                            self.reiniciar_jogo()
                        elif i == 1:  # Modo Desafio
                            self.modo_jogo = MODO_DESAFIO
                            self.reiniciar_jogo()
                        elif i == 2:  # Modo Aventureiro
                            self.modo_jogo = MODO_AVENTUREIRO
                            self.reiniciar_jogo()
                        elif i == 3:  # Sair
                            self.rodando = False
                        break

    def atualizar_menu(self):
        """Atualiza o estado do menu"""
        # Atualizar o efeito de pulso
        if self.pulso_crescendo:
            self.pulso += 0.05
            if self.pulso >= 2:
                self.pulso_crescendo = False
        else:
            self.pulso -= 0.05
            if self.pulso <= 0:
                self.pulso_crescendo = True

    def atualizar_jogo(self, delta_tempo):
        """Atualiza o estado do jogo"""
        # Verificar se a música de fundo ainda tá tocando
        self.audio.verificar_musica_fundo()

        # Calcular tempo restante
        tempo_atual = pygame.time.get_ticks()
        tempo_passado = tempo_atual - self.tempo_inicio
        self.tempo_restante = max(0, TEMPO_JOGO - tempo_passado)

        if self.tempo_restante <= 0:
            self.estado = "fim_jogo"
            # Parar todos os sons ao finalizar o jogo
            for e in self.emocoes:
                if e.som_tocando and self.assets.sons['emocoes'][e.texto]:
                    self.assets.sons['emocoes'][e.texto].stop()
                    e.som_tocando = False

            if self.audio.musica_tocando:
                pygame.mixer.music.stop()
                self.audio.musica_tocando = False
            return

        # Efeito de transição
        if self.transicao_ativa:
            self.alpha_transicao -= 5
            if self.alpha_transicao <= 0:
                self.alpha_transicao = 0
                self.transicao_ativa = False

        # Movimento do jogador
        teclas = pygame.key.get_pressed()
        self.jogador.mover(teclas)
        self.jogador.atualizar(delta_tempo)

        # Aplicar efeito de câmera
        if self.camera_shake > 0:
            # Converter camera_shake para inteiro antes de usar com randint
            camera_shake_int = max(1, int(self.camera_shake))  # Garantir que seja pelo menos 1
            self.camera_offset_x = random.randint(-camera_shake_int, camera_shake_int)
            self.camera_offset_y = random.randint(-camera_shake_int, camera_shake_int)
            self.camera_shake -= 0.5
        else:
            self.camera_offset_x, self.camera_offset_y = 0, 0

        # Atualizar partículas
        novas_particulas = []
        for p in self.particulas:
            if p.atualizar():
                novas_particulas.append(p)
        self.particulas = novas_particulas

        # Atualizar partículas das emoções
        for emocao in self.emocoes:
            novas_particulas = []
            for p in emocao.particulas:
                if p.atualizar():
                    novas_particulas.append(p)
            emocao.particulas = novas_particulas

            # Adicionar novas partículas se a emoção estiver ativa
            if emocao.ativa and random.random() < 0.3:
                criar_particulas_emocao(emocao, 1)

        # Atualizar modos de jogo específicos
        if self.modo_jogo in [MODO_DESAFIO, MODO_AVENTUREIRO]:
            self._atualizar_modo_desafio(delta_tempo)

            if self.modo_jogo == MODO_AVENTUREIRO:
                self._atualizar_modo_aventureiro(delta_tempo)

        # Atualizar emoções
        self.emocao_atual = None

        # No modo desafio e aventureiro, mostrar apenas as emoções ativas
        emocoes_para_atualizar = self.emocoes
        if self.modo_jogo in [MODO_DESAFIO, MODO_AVENTUREIRO]:
            emocoes_para_atualizar = self.emocoes[:self.emocoes_ativas]

        for emocao in emocoes_para_atualizar:
            # Passar o parâmetro modo_passeio
            foi_ativada = emocao.atualizar(
                self.jogador,
                DISTANCIA_ATIVACAO,
                delta_tempo,
                self.dificuldade,
                self.emocoes_congeladas,
                self.modo_jogo == MODO_PASSEIO  # True se for modo passeio
            )

            if foi_ativada:
                # Primeira ativação
                pontos_ganhos = 10 * self.multiplicador_pontos
                self.pontuacao += pontos_ganhos
                criar_particulas_emocao(emocao, 20)

                # Efeitos especiais baseados na emoção
                if emocao.texto == "Raiva":
                    self.camera_shake = 10

            if emocao.ativa:
                self.emocao_atual = emocao

                # Verificar se a missão foi completada
                if emocao.missao_alvo and not emocao.missao_completa and emocao.tempo_missao >= TEMPO_MISSAO:
                    emocao.missao_completa = True
                    self.pontuacao += 50 * self.multiplicador_pontos
                    self.audio.tocar_som_interface("missao_completa")
                    self.missao_atual = None

                    # Criar nova missão após um tempo
                    self.tempo_ultima_missao = pygame.time.get_ticks() + 3000  # 3 segundos de pausa

        # Gerenciar áudio
        self.audio.gerenciar_audio(self.emocoes)

        # Criar partículas ao redor do jogador para destacá-lo
        if random.random() < 0.2:
            # Determinar a cor com base na emoção atual
            cor_particula = None
            if self.emocao_atual:
                cor_particula = self.emocao_atual.cor
            criar_particulas_jogador(self.jogador, self.particulas, 1, cor_particula)

        # Atualizar o efeito de pulso
        if self.pulso_crescendo:
            self.pulso += 0.1
            if self.pulso >= 2:
                self.pulso_crescendo = False
        else:
            self.pulso -= 0.1
            if self.pulso <= 0:
                self.pulso_crescendo = True

    def _atualizar_modo_desafio(self, delta_tempo):
        """Atualiza elementos específicos do modo desafio"""
        # Atualizar dificuldade a cada 10 segundos
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.tempo_ultima_atualizacao_dificuldade >= 10000:  # 10 segundos
            self.dificuldade += 0.2
            self.tempo_ultima_atualizacao_dificuldade = tempo_atual

            # Adicionar mais emoções conforme a dificuldade aumenta
            if self.emocoes_ativas < len(self.emocoes):
                self.emocoes_ativas += 1

        # Aumentar velocidade das emoções conforme o tempo vai acabando
        segundos_restantes = self.tempo_restante // 1000

        # Aumentar velocidade a cada 10 segundos que passam
        if segundos_restantes <= 10:
            # Nos últimos 10 segundos, velocidade muito alta
            self.dificuldade = max(self.dificuldade, 3.5)
        elif segundos_restantes <= 20:
            # Entre 10-20 segundos restantes, velocidade alta
            self.dificuldade = max(self.dificuldade, 3.0)
        elif segundos_restantes <= 30:
            # Entre 20-30 segundos restantes, velocidade média-alta
            self.dificuldade = max(self.dificuldade, 2.5)
        elif segundos_restantes <= 40:
            # Entre 30-40 segundos restantes, velocidade média
            self.dificuldade = max(self.dificuldade, 2.0)
        elif segundos_restantes <= 50:
            # Entre 40-50 segundos restantes, velocidade média-baixa
            self.dificuldade = max(self.dificuldade, 1.5)

        # Gerenciar missões - garantir que continuem aparecendo
        if self.missao_atual is None and tempo_atual >= self.tempo_ultima_missao:
            # Criar nova missão - usar todas as emoções disponíveis, não apenas as ativas
            # Isso permite missões com qualquer emoção, mesmo as que ainda não apareceram
            emocoes_disponiveis = [e for e in self.emocoes if not e.missao_completa]

            # Se todas as emoções já foram completadas, resetar para permitir novas missões
            if not emocoes_disponiveis:
                for e in self.emocoes:
                    e.missao_completa = False
                emocoes_disponiveis = self.emocoes

            if emocoes_disponiveis:
                self.missao_atual = random.choice(emocoes_disponiveis)
                self.missao_atual.missao_alvo = True

                # Garantir que a emoção da missão esteja visível (se ainda não estiver)
                if self.emocoes.index(self.missao_atual) >= self.emocoes_ativas:
                    # Adicionar temporariamente esta emoção às ativas
                    self.emocoes_ativas = max(self.emocoes_ativas, self.emocoes.index(self.missao_atual) + 1)

    def _atualizar_modo_aventureiro(self, delta_tempo):
        """Atualiza elementos específicos do modo aventureiro"""
        # Atualizar power-ups
        for powerup in self.powerups:
            powerup.atualizar(delta_tempo)

            if powerup.ativo and powerup.verificar_colisao(self.jogador):
                # Coletar power-up
                self.audio.tocar_som_powerup(powerup)
                criar_particulas_powerup(powerup, self.particulas)

                # Aplicar efeito do power-up
                if powerup.efeito == "tempo":
                    # Corrigido: Adicionar tempo ao jogo
                    # Adicionar o valor do power-up ao tempo restante
                    self.tempo_inicio -= powerup.valor  # Isso efetivamente adiciona tempo ao jogo
                elif powerup.efeito == "pontos":
                    # Ativar multiplicador de pontos
                    self.multiplicador_pontos = powerup.valor
                    self.tempo_multiplicador = powerup.duracao
                elif powerup.efeito == "congelar":
                    # Congelar emoções
                    self.emocoes_congeladas = True
                    self.tempo_congelamento = powerup.duracao
                elif powerup.efeito == "velocidade":
                    # Aumentar velocidade do jogador
                    self.jogador.ativar_powerup("velocidade", powerup.duracao, powerup.valor)

                # Desativar power-up e definir tempo para reaparecer
                powerup.coletar(TEMPO_REAPARECIMENTO_POWERUP)

        # Atualizar efeitos ativos
        if self.multiplicador_pontos > 1:
            self.tempo_multiplicador -= delta_tempo
            if self.tempo_multiplicador <= 0:
                self.multiplicador_pontos = 1

        if self.emocoes_congeladas:
            self.tempo_congelamento -= delta_tempo
            if self.tempo_congelamento <= 0:
                self.emocoes_congeladas = False

    def renderizar(self):
        """Renderiza o jogo na tela"""
        if self.estado == "menu":
            desenhar_tela_menu(self.tela, self.fontes, self.assets, self.botoes_menu, self.botao_hover, self.pulso)

        elif self.estado == "instrucoes":
            desenhar_tela_instrucoes(self.tela, self.fontes, self.assets, self.pulso, self.modo_jogo)

        elif self.estado == "fim_jogo":
            desenhar_tela_fim_jogo(self.tela, self.fontes, self.assets, self.pontuacao, self.emocoes, self.modo_jogo)

        elif self.estado == "jogando":
            # Limpar a tela e desenhar fundo
            self.tela.fill((0, 0, 0))
            try:

                #Muda o background referente ao modo
                if self.modo_jogo == MODO_PASSEIO:
                    self.tela.blit(self.assets.imagens['fundo3'],
                                (0 + self.camera_offset_x, 0 + self.camera_offset_y))
                elif self.modo_jogo == MODO_DESAFIO:
                    self.tela.blit(self.assets.imagens['fundo2'],
                                   (0 + self.camera_offset_x, 0 + self.camera_offset_y))
                elif self.modo_jogo == MODO_AVENTUREIRO:
                    self.tela.blit(self.assets.imagens['fundo'],
                                   (0 + self.camera_offset_x, 0 + self.camera_offset_y))

            except:
                # Fallback para fundo gradiente
                for y in range(0, ALTURA, 2):
                    cor = (max(0, 20 - y // 20), max(0, 10 - y // 40), min(50 + y // 5, 100))
                    pygame.draw.line(self.tela, cor, (0, y), (LARGURA, y))

            # Desenhar partículas
            for p in self.particulas:
                p.desenhar(self.tela, self.assets.imagens['particula'])

            # Desenhar partículas das emoções
            for emocao in self.emocoes:
                for p in emocao.particulas:
                    p.desenhar(self.tela, self.assets.imagens['particula'])

            # Desenhar emoções (apenas as ativas no modo desafio e aventureiro)
            emocoes_para_desenhar = self.emocoes
            if self.modo_jogo in [MODO_DESAFIO, MODO_AVENTUREIRO]:
                emocoes_para_desenhar = self.emocoes[:self.emocoes_ativas]

            for emocao in emocoes_para_desenhar:
                emocao.desenhar(self.tela, self.assets, self.fontes, self.pulso,
                                self.camera_offset_x, self.camera_offset_y)

            # Desenhar power-ups (apenas no modo aventureiro)
            if self.modo_jogo == MODO_AVENTUREIRO:
                for powerup in self.powerups:
                    powerup.desenhar(self.tela, self.assets, self.fontes,
                                     self.camera_offset_x, self.camera_offset_y)

            # Determinar a cor da aura do jogador
            cor_aura = None
            if self.emocao_atual:
                cor_aura = self.emocao_atual.cor

            # Desenhar o jogador
            self.jogador.desenhar(self.tela, self.assets, self.camera_offset_x,
                                  self.camera_offset_y, cor_aura)

            # Aplicar efeitos visuais da emoção atual
            if self.emocao_atual:
                self.camera_shake = aplicar_efeito_emocao(
                    self.emocao_atual, self.jogador, self.particulas, self.camera_shake)

            # Aplicar efeitos visuais de power-ups ativos (modo aventureiro)
            if self.modo_jogo == MODO_AVENTUREIRO:
                for powerup in self.powerups:
                    if (powerup.efeito == "velocidade" and self.jogador.powerups_ativos["velocidade"]["ativo"]) or \
                            (powerup.efeito == "pontos" and self.multiplicador_pontos > 1) or \
                            (powerup.efeito == "congelar" and self.emocoes_congeladas):
                        aplicar_efeito_powerup(powerup, self.tela, self.jogador, self.pulso)

                # Desenhar indicadores de power-ups ativos
                powerups_ativos = {
                    "velocidade": self.jogador.powerups_ativos["velocidade"],
                    "pontos": {"ativo": self.multiplicador_pontos > 1, "tempo_restante": self.tempo_multiplicador},
                    "congelar": {"ativo": self.emocoes_congeladas, "tempo_restante": self.tempo_congelamento}
                }
                desenhar_indicadores_powerup(self.tela, self.fontes, self.jogador, powerups_ativos)

            # Desenhar interface
            desenhar_interface(self.tela, self.fontes, self.tempo_restante,
                               TEMPO_JOGO, self.pontuacao, self.emocao_atual,
                               self.missao_atual, self.multiplicador_pontos, self.modo_jogo)

            # Desenhar transição
            if self.transicao_ativa:
                s = pygame.Surface((LARGURA, ALTURA))
                s.fill((0, 0, 0))
                s.set_alpha(self.alpha_transicao)
                self.tela.blit(s, (0, 0))

    def run(self):
        """Loop principal do jogo"""
        ultimo_tempo = pygame.time.get_ticks()

        while self.rodando:
            # Calcular delta tempo
            tempo_atual = pygame.time.get_ticks()
            delta_tempo = tempo_atual - ultimo_tempo
            ultimo_tempo = tempo_atual

            # Processar eventos
            self.processar_eventos()

            # Atualizar estado do jogo
            if self.estado == "menu":
                self.atualizar_menu()
            elif self.estado == "jogando":
                self.atualizar_jogo(delta_tempo)
            elif self.estado == "fim_jogo":
                # Garantir que o jogo não feche sozinho após finalizar a partida
                pass

            # Renderizar
            self.renderizar()

            # Atualizar a tela
            pygame.display.flip()
            self.clock.tick(60)

        # Encerrar o Pygame
        pygame.quit()
        sys.exit()