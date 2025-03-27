# Gerenciador de áudio
import pygame



class AudioManager:
    def __init__(self, assets):
        self.assets = assets
        self.musica_tocando = False
        self.emocao_tocando_som = None


    def iniciar_musica_fundo(self):
        """Inicia a música de fundo"""
        try:
            if self.assets.musica_fundo:
                pygame.mixer.music.load(self.assets.musica_fundo)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # Para loop infinito
                self.musica_tocando = True

                # Configurar evento para detectar quando a música termina
                pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
        except Exception as e:
            print(f"Erro ao tocar música de fundo: {e}")

    def pausar_musica_fundo(self):
        """Pausa a música de fundo"""
        if self.musica_tocando:
            pygame.mixer.music.pause()
            self.musica_tocando = False

    def retomar_musica_fundo(self):
        """Retoma a música de fundo"""
        if not self.musica_tocando and self.assets.musica_fundo:
            try:
                pygame.mixer.music.unpause()
                self.musica_tocando = True
            except:
                # Se não conseguir retomar, tenta iniciar novamente
                self.iniciar_musica_fundo()

    def parar_todos_sons(self):
        """Para todos os sons de emoções"""
        for nome, som in self.assets.sons['emocoes'].items():
            if som:
                som.stop()

    def verificar_musica_fundo(self):
        """Verifica se a música de fundo ainda tá tocando e reinicia se necessário"""
        if not pygame.mixer.music.get_busy() and self.musica_tocando:
            try:
                pygame.mixer.music.play(-1)  # Reiniciar em loop
            except Exception as e:
                print(f"Erro ao reiniciar música de fundo: {e}")
                self.iniciar_musica_fundo()


    def tocar_som_emocao(self, emocao):
        """Toca o som de uma emoção"""
        if emocao and self.assets.sons['emocoes'][emocao.texto]:
            self.assets.sons['emocoes'][emocao.texto].play()
            return True
        return False

    def tocar_som_powerup(self, powerup):
        """Toca o som de um power-up"""
        if powerup and self.assets.sons['powerups'][powerup.texto]:
            self.assets.sons['powerups'][powerup.texto].play()
            return True
        return False

    def tocar_som_interface(self, nome):
        """Toca um som de interface"""
        if nome in self.assets.sons['interface'] and self.assets.sons['interface'][nome]:
            self.assets.sons['interface'][nome].play()

    """Gerencia a reprodução de áudio com base nas emoções ativas"""
    def gerenciar_audio(self, emocoes):
        emocao_ativa = None
        for emocao in emocoes:
            if emocao.ativa and emocao.intensidade > 0:
                emocao_ativa = emocao
                break

        # Gerenciar música de fundo e sons de emoções
        if emocao_ativa:
            # Caso nai tenha uma emoção ativa
            if emocao_ativa != self.emocao_tocando_som:

                # Parar todos os sons de emoções
                for e in emocoes:
                    if e.som_tocando and self.assets.sons['emocoes'][e.texto]:
                        self.assets.sons['emocoes'][e.texto].stop()
                        e.som_tocando = False

                # Parar música de fundo se estiver tocando
                self.pausar_musica_fundo()

                # Tocar o som da nova emoção
                if self.tocar_som_emocao(emocao_ativa):
                    emocao_ativa.som_tocando = True
                    self.emocao_tocando_som = emocao_ativa
        else:
            # Caso não tenha emoção ativa

            # Parar todos os sons de emoções
            for e in emocoes:
                if e.som_tocando and self.assets.sons['emocoes'][e.texto]:
                    self.assets.sons['emocoes'][e.texto].stop()
                    e.som_tocando = False

            self.emocao_tocando_som = None

            # Iniciar música de fundo se não estiver tocando
            if not self.musica_tocando:
                self.retomar_musica_fundo()