# Configurações do jogo
import pygame

# Fontes
def carregar_fontes():
    pygame.font.init()
    fontes = {
        'normal': pygame.font.SysFont('Arial', 24),
        'grande': pygame.font.SysFont('Arial', 36),
        'pequena': pygame.font.SysFont('Arial', 18),
        'titulo': pygame.font.SysFont('Arial', 48, bold=True)
    }
    return fontes

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 50, 50)       # Vermelho mais vibrante
VERDE = (50, 255, 100)         # Verde mais vibrante
AZUL = (50, 100, 255)          # Azul mais vibrante
AMARELO = (255, 255, 50)       # Amarelo mais vibrante
ROXO = (200, 50, 255)          # Roxo mais vibrante
CIANO = (0, 255, 255)          # Ciano vibrante
ROSA = (255, 50, 150)          # Rosa vibrante
LARANJA = (255, 150, 0)        # Laranja vibrante

# Configurações da tela
LARGURA, ALTURA = 800, 600
TITULO = "Jogo das Emoções"

# Configurações do jogo
TEMPO_JOGO = 60000  # 60 segundos
JOGADOR_TAMANHO = 20
JOGADOR_VELOCIDADE = 5
DISTANCIA_ATIVACAO = 100
DISTANCIA_MINIMA_EMOCOES = 150
TEMPO_MISSAO = 3000  # Precisará de 3 segundos para completar uma missão

# Modos de jogo
MODO_PASSEIO = 0
MODO_DESAFIO = 1
MODO_AVENTUREIRO = 2

# Cor do jogador
COR_JOGADOR = (158, 231, 255)

# Definições das emoções
DEFINICOES_EMOCOES = [
    {"texto": "Alegria", "cor": AMARELO, "descricao": "Apenas sinto uma energia contagiante!", "comportamento": "aleatorio"},
    {"texto": "Tristeza", "cor": AZUL, "descricao": "Estou tão melancólico...", "comportamento": "fuga"},
    {"texto": "Raiva", "cor": VERMELHO, "descricao": "Saia do meu espaço, estou furioso!", "comportamento": "fuga"},
    {"texto": "Medo", "cor": ROXO, "descricao": "Estou com medo de você...", "comportamento": "fuga"},
    {"texto": "Paz", "cor": VERDE, "descricao": "Quero apenas paz, sem pressão!", "comportamento": "estatico"}
]

# Definições dos power-ups
DEFINICOES_POWERUPS = [
    {"texto": "Tempo+", "cor": CIANO, "descricao": "-5 segundos", "efeito": "tempo", "duracao": 0, "valor": 5000},
    {"texto": "2x Pontos", "cor": AMARELO, "descricao": "Pontuação dobrada", "efeito": "pontos", "duracao": 5000, "valor": 2},
    {"texto": "Congelar", "cor": AZUL, "descricao": "Congela as emoções", "efeito": "congelar", "duracao": 5000, "valor": 0},
    {"texto": "Velocidade", "cor": VERDE, "descricao": "Velocidade aumentada", "efeito": "velocidade", "duracao": 10000, "valor": 2}
]

# Tempo para reaparecer power-ups
TEMPO_REAPARECIMENTO_POWERUP = 10000  # 10 segundos

# Diretórios
DIR_SONS = "sons"
DIR_IMAGENS = "imagens"