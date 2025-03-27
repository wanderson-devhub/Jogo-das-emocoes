# Gerenciador de recursos (imagens, sons)
import os
import math
import pygame
import random
from game.config import BRANCO, LARGURA, ALTURA

class AssetManager:
    def __init__(self):
        # Inicializar dicionários para armazenar recursos
        self.imagens = {}
        self.sons = {}
        self.musica_fundo = None

        # Cria os recursos se necessário
        self._criar_recursos()

        # Para carregar os recursos
        self._carregar_recursos()

    def _carregar_recursos(self):
        """Aqui carrega todos os recursos do jogo"""
        self.imagens['fundo'] = self.carregar_imagem("assets/imagens/fundo.png", (LARGURA, ALTURA))
        self.imagens['fundo2'] = self.carregar_imagem("assets/imagens/fundo2.png", (LARGURA, ALTURA))
        self.imagens['fundo3'] = self.carregar_imagem("assets/imagens/fundo3.png", (LARGURA, ALTURA))
        self.imagens['fundo_instrucao'] = self.carregar_imagem("assets/imagens/fundo_instrucao.png", (LARGURA, ALTURA))
        self.imagens['fundo_instrucao2'] = self.carregar_imagem("assets/imagens/fundo_instrucao2.png", (LARGURA, ALTURA))
        self.imagens['fundo_instrucao3'] = self.carregar_imagem("assets/imagens/fundo_instrucao3.png", (LARGURA, ALTURA))
        self.imagens['fundo_menu'] = self.carregar_imagem("assets/imagens/fundo_menu.png", (LARGURA, ALTURA))
        self.imagens['fundo_resultado'] = self.carregar_imagem("assets/imagens/fundo_resultado.png", (LARGURA, ALTURA))
        self.imagens['jogador'] = self.carregar_imagem("assets/imagens/personagem.png", (40, 40))
        self.imagens['particula'] = self.carregar_imagem("assets/imagens/particula.png", (10, 10))

        # Aqui carrega as imagens das emoções
        self.imagens['emocoes'] = {
            "Alegria": self.carregar_imagem("assets/imagens/alegria.png", (60, 60)),
            "Tristeza": self.carregar_imagem("assets/imagens/tristeza.png", (60, 60)),
            "Raiva": self.carregar_imagem("assets/imagens/raiva.png", (60, 60)),
            "Medo": self.carregar_imagem("assets/imagens/medo.png", (60, 60)),
            "Paz": self.carregar_imagem("assets/imagens/paz.png", (60, 60))
        }

        # Para carregar as imagens dos power-ups
        self.imagens['powerups'] = {
            "Congelar": self.carregar_imagem("assets/imagens/powerup_congelar.png", (40, 40)),
            "2x Pontos": self.carregar_imagem("assets/imagens/powerup_pontos.png", (40, 40)),
            "Velocidade": self.carregar_imagem("assets/imagens/powerup_velocidade.png", (40, 40)),
            "Tempo+": self.carregar_imagem("assets/imagens/powerup_tempo.png", (40, 40))
        }

        # Carregar sons
        self.sons['emocoes'] = {
            "Alegria": self.carregar_som("assets/sons/alegria.wav"),
            "Tristeza": self.carregar_som("assets/sons/tristeza.wav"),
            "Raiva": self.carregar_som("assets/sons/raiva.wav"),
            "Medo": self.carregar_som("assets/sons/medo.wav"),
            "Paz": self.carregar_som("assets/sons/paz.wav")
        }

        # Para carregar sons dos power-ups
        self.sons['powerups'] = {
            "Congelar": self.carregar_som("assets/sons/powerup_congelar.wav"),
            "2x Pontos": self.carregar_som("assets/sons/powerup_pontos.wav"),
            "Velocidade": self.carregar_som("assets/sons/powerup_velocidade.wav"),
            "Tempo+": self.carregar_som("assets/sons/powerup_tempo.wav")
        }

        # Para carregar sons de interface
        self.sons['interface'] = {
            "menu": self.carregar_som("assets/sons/menu.wav"),
            "selecao": self.carregar_som("assets/sons/selecao.wav"),
            "missao_completa": self.carregar_som("assets/sons/missao_completa.wav")
        }

        # Carregar música de fundo
        self.musica_fundo = self._criar_musica()

    @staticmethod
    def carregar_imagem(nome: str, tamanho=None):
        """Carrega uma imagem do disco ou cria um placeholder"""
        try:
            imagem = pygame.image.load(nome).convert_alpha()
            if tamanho:
                imagem = pygame.transform.scale(imagem, tamanho)
            return imagem
        except Exception as e:
            print(f"Erro ao carregar imagem {nome}: {e}")
            # Criar uma imagem placeholder se não conseguir carregar
            img = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(img, BRANCO, (25, 25), 25)
            if tamanho:
                img = pygame.transform.scale(img, tamanho)
            return img

    @staticmethod
    def carregar_som(nome: str):
        """Carrega um som do disco"""
        try:
            return pygame.mixer.Sound(nome)
        except Exception as e:
            print(f"Não foi possível carregar o som: {nome}. Erro: {e}")
            return None

    def _criar_recursos(self):
        """Cria recursos se eles não existirem"""
        # Criar sons
        self._criar_som("assets/sons/alegria.wav", 440, 1.0)
        self._criar_som("assets/sons/tristeza.wav", 220, 1.5)
        self._criar_som("assets/sons/raiva.wav", 880, 0.5)
        self._criar_som("assets/sons/medo.wav", 330, 1.2)
        self._criar_som("assets/sons/paz.wav", 277, 2.0)

        # Criar sons de power-ups
        self._criar_som("assets/sons/powerup_tempo.wav", 600, 0.3)
        self._criar_som("assets/sons/powerup_pontos.wav", 700, 0.3)
        self._criar_som("assets/sons/powerup_congelar.wav", 300, 0.3)
        self._criar_som("assets/sons/powerup_velocidade.wav", 500, 0.3)

        # Criar sons de interface
        self._criar_som("assets/sons/menu.wav", 350, 0.2)
        self._criar_som("assets/sons/selecao.wav", 450, 0.2)
        self._criar_som("assets/sons/missao_completa.wav", 550, 0.5)

        # Criar imagens
        from game.config import COR_JOGADOR, AMARELO, AZUL, VERMELHO, ROXO, VERDE, CIANO
        self._criar_imagem("assets/imagens/personagem.png", COR_JOGADOR, (40, 40))
        self._criar_imagem("assets/imagens/alegria.png", AMARELO, (60, 60))
        self._criar_imagem("assets/imagens/tristeza.png", AZUL, (60, 60))
        self._criar_imagem("assets/imagens/raiva.png", VERMELHO, (60, 60))
        self._criar_imagem("assets/imagens/medo.png", ROXO, (60, 60))
        self._criar_imagem("assets/imagens/paz.png", VERDE, (60, 60))
        self._criar_imagem("assets/imagens/particula.png", BRANCO, (10, 10))

        # Criar imagens de power-ups
        self._criar_imagem("assets/imagens/powerup_tempo.png", CIANO, (40, 40))
        self._criar_imagem("assets/imagens/powerup_pontos.png", AMARELO, (40, 40))
        self._criar_imagem("assets/imagens/powerup_congelar.png", AZUL, (40, 40))
        self._criar_imagem("assets/imagens/powerup_velocidade.png", VERDE, (40, 40))

        # Criar imagem de fundo
        self._criar_fundo("assets/imagens/fundo.png", LARGURA, ALTURA)
        self._criar_fundo("assets/imagens/fundo2.png", LARGURA, ALTURA)
        self._criar_fundo("assets/imagens/fundo3.png", LARGURA, ALTURA)

        # Criar imagem de fundo de instrucao
        self._criar_fundo("assets/imagens/fundo_instrucao.png", LARGURA, ALTURA)
        self._criar_fundo("assets/imagens/fundo_instrucao2.png", LARGURA, ALTURA)
        self._criar_fundo("assets/imagens/fundo_instrucao3.png", LARGURA, ALTURA)

        # Criar fundo do menu
        self._criar_fundo_menu("assets/imagens/fundo_menu.png", LARGURA, ALTURA)

        # Criar fundo de resultado
        self._criar_fundo_resultado("assets/imagens/fundo_resultado.png", LARGURA, ALTURA)

    @staticmethod
    def _criar_som(nome: str, frequencia: float, duracao: float):
        """Cria um arquivo de som se não existir"""
        if os.path.exists(nome):
            return

        try:
            # Criar um som básico usando pygame.mixer.Sound
            tamanho_amostra = 44100  # 44.1 kHz
            som = pygame.mixer.Sound(buffer=bytes(int(32767 * math.sin(2 * math.pi * frequencia * i / tamanho_amostra))
                                                  for i in range(int(tamanho_amostra * duracao))))
            with open(nome, 'wb') as f:
                som.write(f)
            print(f"Som criado: {nome}")
        except Exception as e:
            print(f"Não foi possível criar o som: {nome}. Erro: {e}")

    @staticmethod
    def _criar_imagem(nome: str, cor, tamanho=(60, 60)):
        """Cria uma imagem se não existir"""
        if os.path.exists(nome):
            return

        try:
            img = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.circle(img, cor, (tamanho[0] // 2, tamanho[1] // 2), tamanho[0] // 2)
            pygame.image.save(img, nome)
            print(f"Imagem criada: {nome}")
        except Exception as e:
            print(f"Não foi possível criar a imagem: {nome}. Erro: {e}")

    @staticmethod
    def _criar_fundo(nome: str, largura: int, altura: int):
        """Cria uma imagem de fundo se não existir"""
        if os.path.exists(nome):
            return

        try:
            img = pygame.Surface((largura, altura))
            # Criar um gradiente de cor
            for y in range(altura):
                cor = (max(0, 20 - y // 20), max(0, 10 - y // 40), min(50 + y // 5, 100))
                pygame.draw.line(img, cor, (0, y), (largura, y))
            pygame.image.save(img, nome)
            print(f"Imagem de fundo criada: {nome}")
        except Exception as e:
            print(f"Não foi possível criar a imagem de fundo: {nome}. Erro: {e}")

    @staticmethod
    def _criar_fundo_menu(nome: str, largura: int, altura: int):
        """Cria uma imagem de fundo para o menu se não existir"""
        if os.path.exists(nome):
            return

        try:
            img = pygame.Surface((largura, altura))
            # Criar um gradiente de cor mais vibrante para o menu
            for y in range(altura):
                # Gradiente de azul para roxo
                b = min(255, 100 + y // 2)
                r = min(255, max(0, y - 300) // 1)
                g = min(100, y // 10)
                pygame.draw.line(img, (r, g, b), (0, y), (largura, y))

            # Adicionar algumas estrelas/partículas
            for _ in range(100):
                x = random.randint(0, largura)
                y = random.randint(0, altura)
                tamanho = random.randint(1, 3)
                brilho = random.randint(150, 255)
                pygame.draw.circle(img, (brilho, brilho, brilho), (x, y), tamanho)

            pygame.image.save(img, nome)
            print(f"Imagem de fundo do menu criada: {nome}")
        except Exception as e:
            print(f"Não foi possível criar a imagem de fundo do menu: {nome}. Erro: {e}")

    @staticmethod
    def _criar_fundo_resultado(nome: str, largura: int, altura: int):
        """Cria uma imagem de fundo para a tela de resultado se não existir"""
        if os.path.exists(nome):
            return

        try:
            img = pygame.Surface((largura, altura))
            # Criar um gradiente de cor para a tela de resultado
            for y in range(altura):
                # Gradiente de verde para azul
                g = max(0, 150 - y // 3)
                b = min(255, 50 + y // 2)
                r = min(100, y // 10)
                pygame.draw.line(img, (r, g, b), (0, y), (largura, y))

            # Adicionar alguns efeitos visuais
            for _ in range(50):
                x = random.randint(0, largura)
                y = random.randint(0, altura)
                raio = random.randint(20, 50)
                alpha = random.randint(30, 100)
                s = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 255, alpha), (raio, raio), raio)
                img.blit(s, (x - raio, y - raio))

            pygame.image.save(img, nome)
            print(f"Imagem de fundo de resultado criada: {nome}")
        except Exception as e:
            print(f"Não foi possível criar a imagem de fundo de resultado: {nome}. Erro: {e}")

    def _criar_musica(self):
        """Cria uma música de fundo se não existir"""
        nome = "assets/sons/musica_fundo.wav"
        if os.path.exists(nome):
            return nome

        try:
            # Criar uma música simples
            tamanho_amostra = 44100  # 44.1 kHz
            duracao = 10.0  # 10 segundos

            # Criar uma melodia simples
            notas = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
            tempo_nota = 0.5

            # Criar buffer de som
            buffer = []
            for i in range(int(duracao / tempo_nota)):
                nota = notas[i % len(notas)]
                for j in range(int(tamanho_amostra * tempo_nota)):
                    valor = int(32767 * 0.5 * math.sin(2 * math.pi * nota * j / tamanho_amostra))
                    buffer.append(valor)

            # Converter para bytes
            buffer_bytes = bytes(buffer)

            # Salvar como arquivo WAV
            som = pygame.mixer.Sound(buffer=buffer_bytes)
            with open(nome, 'wb') as f:
                som.write(f)
            print(f"Música de fundo criada: {nome}")
            return nome
        except Exception as e:
            print(f"Não foi possível criar a música de fundo: {e}")
            return None