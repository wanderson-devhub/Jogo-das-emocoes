# Funções para renderização
import pygame
from game.config import LARGURA, ALTURA, BRANCO, CIANO, VERDE, VERMELHO, AMARELO, PRETO, MODO_PASSEIO, MODO_DESAFIO, MODO_AVENTUREIRO
from game.utils import desenhar_botao


def desenhar_tela_menu(tela, fontes, assets, botoes, botao_hover, pulso):
    """Desenha a tela do menu principal"""
    # Desenhar fundo
    tela.blit(assets.imagens['fundo_menu'], (0, 0))

    # Título com efeito
    import math
    titulo_texto = "Jogo das Emoções"
    titulo_tamanho = int(60 + 3 * math.sin(pulso))
    fonte_titulo = pygame.font.SysFont('Arial', titulo_tamanho, bold=True)
    titulo = fonte_titulo.render(titulo_texto, True, CIANO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

    # Subtítulo
    subtitulo = fontes['grande'].render("Escolha um modo de jogo:", True, AMARELO)
    tela.blit(subtitulo, (LARGURA // 2 - subtitulo.get_width() // 2, 200))

    # Desenhar botões
    for i, (texto, rect) in enumerate(botoes):
        hover = (i == botao_hover)
        desenhar_botao(tela, texto, fontes['grande'], BRANCO, (50, 50, 150), rect, hover=hover)

    # Desenhar informações sobre os modos
    info_y = 465
    if botao_hover == 0:  # Modo Passeio
        info = fontes['normal'].render("Explore livremente as emoções sem pressão", True, AMARELO)
        tela.blit(info, (LARGURA // 2 - info.get_width() // 2, info_y))
    elif botao_hover == 1:  # Modo Desafio
        info = fontes['normal'].render("Emoções em movimento e missões para completar", True, AMARELO)
        tela.blit(info, (LARGURA // 2 - info.get_width() // 2, info_y))
    elif botao_hover == 2:  # Modo Aventureiro
        info = fontes['normal'].render("Desafios + buffs para ajudar na sua jornada", True, AMARELO)
        tela.blit(info, (LARGURA // 2 - info.get_width() // 2, info_y))

    # Desenhar créditos
    creditos = fontes['pequena'].render("Desenvolvido com Pygame", True, BRANCO)
    tela.blit(creditos, (LARGURA - creditos.get_width() - 10, ALTURA - 30))


def desenhar_tela_instrucoes(tela, fontes, assets, pulso, modo_jogo):
    """Desenha a tela de instruções"""
    if modo_jogo == MODO_PASSEIO:
        tela.blit(assets.imagens['fundo_instrucao'], (0, 0))
    elif modo_jogo == MODO_DESAFIO:
        tela.blit(assets.imagens['fundo_instrucao2'], (0, 0))
    elif modo_jogo == MODO_AVENTUREIRO:
        tela.blit(assets.imagens['fundo_instrucao3'], (0, 0))

    # Título com efeito
    import math
    titulo_texto = "Jogo das Emoções"
    titulo_tamanho = int(50 + 5 * math.sin(pulso))
    fonte_titulo = pygame.font.SysFont('Arial', titulo_tamanho, bold=True)
    titulo = fonte_titulo.render(titulo_texto, True, BRANCO)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 100))

    # Instruções comuns
    instrucoes = [
        "Use as setas do teclado para mover o personagem",
        "Aproxime-se das emoções para senti-las",
        "Cada emoção tem sons e efeitos visuais únicos",
        "Tente experimentar todas as emoções!",
        "Quanto mais tempo passar perto de uma emoção,",
        "mais intensamente você a sentirá"
    ]

    # Instruções específicas do modo
    if modo_jogo == MODO_PASSEIO:
        modo_texto = "MODO PASSEIO"
        instrucoes_modo = [
            "Explore livremente sem pressão",
            "As emoções ficam paradas no mapa"
        ]
    elif modo_jogo == MODO_DESAFIO:
        modo_texto = "MODO DESAFIO"
        instrucoes_modo = [
            "Algumas emoções se movem pelo mapa",
            "Complete missões ficando sobre emoções específicas",
        ]
    elif modo_jogo == MODO_AVENTUREIRO:
        modo_texto = "MODO AVENTUREIRO"
        instrucoes_modo = [
            "Igual ao Modo Desafio, mas com power-ups",
            "onde você pode ganhar pontos e intensidade",
        ]

    if modo_jogo == MODO_PASSEIO:
        modo = fontes['grande'].render(modo_texto, True, VERDE)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 170))
    elif modo_jogo == MODO_DESAFIO:
        modo = fontes['grande'].render(modo_texto, True, VERMELHO)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 170))
    elif modo_jogo == MODO_AVENTUREIRO:
        modo = fontes['grande'].render(modo_texto, True, CIANO)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 170))

    # Desenhar instruções comuns
    for i, linha in enumerate(instrucoes):
        texto = fontes['normal'].render(linha, True, BRANCO)
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, 220 + i * 30))

    # Desenhar instruções específicas do modo
    y_offset = 220 + len(instrucoes) * 30 + 20
    for i, linha in enumerate(instrucoes_modo):
        texto = fontes['normal'].render(linha, True, (200, 200, 255))
        tela.blit(texto, (LARGURA // 2 - texto.get_width() // 2, y_offset + i * 30))

        # Pressione espaço para começar
    espaco_texto = fontes['grande'].render("Pressione ESPAÇO para começar", True, BRANCO)
    tela.blit(espaco_texto, (LARGURA // 2 - espaco_texto.get_width() // 2, ALTURA - 100))


def desenhar_tela_fim_jogo(tela, fontes, assets, pontuacao, emocoes, modo_jogo):
    """Desenha a tela de fim de jogo"""
    # Desenhar fundo
    tela.blit(assets.imagens['fundo_resultado'], (0, 0))

    texto_fim = fontes['grande'].render("Tempo Esgotado!", True, BRANCO)
    tela.blit(texto_fim, (LARGURA // 2 - texto_fim.get_width() // 2, ALTURA // 2 - 150))

    # Mostrar modo de jogo
    if modo_jogo == MODO_PASSEIO:
        modo_texto = "MODO PASSEIO"
    elif modo_jogo == MODO_DESAFIO:
        modo_texto = "MODO DESAFIO"
    elif modo_jogo == MODO_AVENTUREIRO:
        modo_texto = "MODO AVENTUREIRO"

    # Mudar cor do nome do modo
    if modo_jogo == MODO_PASSEIO:
        modo = fontes['normal'].render(modo_texto, True, VERDE)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 100))
    elif modo_jogo == MODO_DESAFIO:
        modo = fontes['normal'].render(modo_texto, True, VERMELHO)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 100))
    elif modo_jogo == MODO_AVENTUREIRO:
        modo = fontes['normal'].render(modo_texto, True, CIANO)
        tela.blit(modo, (LARGURA // 2 - modo.get_width() // 2, 100))

    texto_pontuacao = fontes['grande'].render(f"Pontuação Final: {pontuacao}", True, BRANCO)
    tela.blit(texto_pontuacao, (LARGURA // 2 - texto_pontuacao.get_width() // 2, ALTURA // 2 - 50))

    # Mostrar emoções experimentadas
    texto_emocoes = fontes['normal'].render("Emoções experimentadas:", True, BRANCO)
    tela.blit(texto_emocoes, (LARGURA // 2 - texto_emocoes.get_width() // 2, ALTURA // 2 + 20))

    emocoes_sentidas = [e.texto for e in emocoes if e.intensidade > 0]
    if emocoes_sentidas:
        texto_lista = fontes['normal'].render(", ".join(emocoes_sentidas), True, BRANCO)
        tela.blit(texto_lista, (LARGURA // 2 - texto_lista.get_width() // 2, ALTURA // 2 + 60))
    else:
        texto_nenhuma = fontes['normal'].render("Nenhuma emoção foi sentida profundamente", True, BRANCO)
        tela.blit(texto_nenhuma, (LARGURA // 2 - texto_nenhuma.get_width() // 2, ALTURA // 2 + 60))

    texto_reiniciar = fontes['normal'].render("Pressione R para jogar novamente", True, VERDE)
    tela.blit(texto_reiniciar, (LARGURA // 2 - texto_reiniciar.get_width() // 2, ALTURA // 2 + 120))

    texto_menu = fontes['normal'].render("Pressione M para voltar ao menu", True, VERDE)
    tela.blit(texto_menu, (LARGURA // 2 - texto_menu.get_width() // 2, ALTURA // 2 + 160))


def desenhar_interface(tela, fontes, tempo_restante, tempo_jogo, pontuacao, emocao_atual=None, missao_atual=None,
                       multiplicador_pontos=1, modo_jogo=MODO_PASSEIO):
    """Desenha a interface do usuário"""
    # Barra de tempo
    tempo_percentual = tempo_restante / tempo_jogo
    largura_barra_tempo = LARGURA - 40
    pygame.draw.rect(tela, (100, 100, 100), (20, 20, largura_barra_tempo, 15))

    # Cor da barra
    if modo_jogo == MODO_PASSEIO:
        pygame.draw.rect(tela, (117, 251, 149), (20, 20, int(largura_barra_tempo * tempo_percentual), 15))
    elif modo_jogo == MODO_DESAFIO:
        pygame.draw.rect(tela, (250, 81, 113), (20, 20, int(largura_barra_tempo * tempo_percentual), 15))
    elif modo_jogo == MODO_AVENTUREIRO:
        pygame.draw.rect(tela, (127, 236, 250), (20, 20, int(largura_barra_tempo * tempo_percentual), 15))

    # Texto de tempo
    segundos_restantes = tempo_restante // 1000
    texto_tempo = fontes['normal'].render(f"Tempo: {segundos_restantes}s", True, BRANCO)
    tela.blit(texto_tempo, (20, 40))

    # Pontuação
    cor_pontuacao = (255, 255, 50) if multiplicador_pontos > 1 else BRANCO
    texto_pontuacao = fontes['normal'].render(f"Pontuação: {pontuacao}", True, cor_pontuacao)
    tela.blit(texto_pontuacao, (LARGURA - texto_pontuacao.get_width() - 20, 40))

    texto_saida = fontes['normal'].render(f"Pressione ESC para voltar", True, BRANCO)
    tela.blit(texto_saida, (LARGURA // 2 - texto_saida.get_width() // 2, 60))

    # Mostrar multiplicador se ativo
    if multiplicador_pontos > 1:
        texto_multi = fontes['pequena'].render(f"x{multiplicador_pontos}", True, (255, 255, 50))
        tela.blit(texto_multi, (LARGURA - 20, 50))

    # Mostrar missão atual se existir
    if missao_atual:
        # Criar um painel para a missão
        painel_missao = pygame.Surface((400, 40), pygame.SRCALPHA)
        painel_missao.fill((0, 0, 0, 110))
        tela.blit(painel_missao, (LARGURA // 2 - 200, 20))

        texto_missao = fontes['normal'].render(f"Missão: Alcançar {missao_atual.texto}", True, missao_atual.cor)
        tela.blit(texto_missao, (LARGURA // 2 - texto_missao.get_width() // 2, 30))

    # Mostrar emoção atual e sua descrição
    if emocao_atual:
        # Criar um painel para a descrição
        painel = pygame.Surface((400, 80), pygame.SRCALPHA)
        painel.fill((0, 0, 0, 110))
        tela.blit(painel, (LARGURA // 2 - 200, ALTURA - 100))

        # Texto da emoção atual
        texto_emocao = fontes['normal'].render(f"Sentindo: {emocao_atual.texto}", True, emocao_atual.cor)
        tela.blit(texto_emocao, (LARGURA // 2 - texto_emocao.get_width() // 2, ALTURA - 90))

        # Descrição da emoção
        texto_descricao = fontes['pequena'].render(emocao_atual.descricao, True, BRANCO)
        tela.blit(texto_descricao, (LARGURA // 2 - texto_descricao.get_width() // 2, ALTURA - 60))

        # Intensidade
        texto_intensidade = fontes['pequena'].render(f"Intensidade: {int(emocao_atual.intensidade)}%", True, BRANCO)
        tela.blit(texto_intensidade, (LARGURA // 2 - texto_intensidade.get_width() // 2, ALTURA - 40))

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

