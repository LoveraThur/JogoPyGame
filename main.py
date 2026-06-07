import pygame
import random
import math
import threading
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

try:
    import pyttsx3
    _tts_engine = pyttsx3.init()
    _tts_engine.setProperty("rate", 160)
    TTS_DISPONIVEL = True
except Exception:
    TTS_DISPONIVEL = False

def falar(texto):
    """Fala o texto em uma thread separada para não travar o jogo."""
    if not TTS_DISPONIVEL:
        return
    def _run():
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 160)
            engine.say(texto)
            engine.runAndWait()
        except Exception:
            pass
    t = threading.Thread(target=_run, daemon=True)
    t.start()


limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()

pygame.init()

while True:
    nome = input("Informe o Nome do Competidor: ")
    if len(nome) > 0:
        break
    else:
        print("Nome Inválido!")

tamanho = (1000, 700)
pygame.display.set_caption("Iron Man do Marcão")
icone = pygame.image.load("bases/bafoDragao.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 220, 0)
vermelho = (200, 0, 0)
laranja = (255, 165, 0)

fundo = pygame.image.load("bases/end.png")
fundoDead = pygame.image.load("bases/backgroundMorte.png")
fundoStart = pygame.image.load("bases/backgroundInicio.png")

iron = pygame.image.load("bases/steveElytra.png")
iron = pygame.transform.scale(iron, (210, 120))
missel = pygame.image.load("bases/bafoDragao.png")
missel = pygame.transform.scale(missel, (80, 80))
missileSound = pygame.mixer.Sound("bases/gast.mp3")
explosaoSound = pygame.mixer.Sound("bases/fogo.mp3")
pygame.mixer.music.load("bases/musicend.mp3")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fontePausa = pygame.font.SysFont("comicsans", 72, bold=True)
fonteGrande = pygame.font.SysFont("comicsans", 24, bold=True)

# Item 16: variáveis para o sol pulsante
_sol_tick = 0
_SOL_RAIO_BASE = 38
_SOL_RAIO_DELTA = 10   # quanto o raio varia
_SOL_X = 950           # canto superior direito
_SOL_Y = 50
_SOL_VELOCIDADE = 0.04  # velocidade da pulsação


def desenhar_sol(superficie, tick):
    """
    Item 16: desenha um sol amarelo pulsante (aumenta e diminui de raio)
    com raios ao redor, no canto superior direito da tela.
    """
    raio = int(_SOL_RAIO_BASE + _SOL_RAIO_DELTA * math.sin(tick))
    # Brilho externo (halo suave)
    halo_surf = pygame.Surface(((_SOL_RAIO_BASE + _SOL_RAIO_DELTA + 18) * 2,
                                 (_SOL_RAIO_BASE + _SOL_RAIO_DELTA + 18) * 2), pygame.SRCALPHA)
    halo_r = raio + 14
    pygame.draw.circle(halo_surf, (255, 220, 0, 60),
                       (halo_surf.get_width() // 2, halo_surf.get_height() // 2), halo_r)
    superficie.blit(halo_surf,
                    (_SOL_X - halo_surf.get_width() // 2,
                     _SOL_Y - halo_surf.get_height() // 2))
    # Raios do sol
    num_raios = 10
    comprimento_raio = raio + 16
    for i in range(num_raios):
        angulo = (2 * math.pi / num_raios) * i + tick * 0.5
        x1 = _SOL_X + int((raio + 4) * math.cos(angulo))
        y1 = _SOL_Y + int((raio + 4) * math.sin(angulo))
        x2 = _SOL_X + int(comprimento_raio * math.cos(angulo))
        y2 = _SOL_Y + int(comprimento_raio * math.sin(angulo))
        pygame.draw.line(superficie, (255, 200, 0), (x1, y1), (x2, y2), 3)
    # Círculo principal do sol
    pygame.draw.circle(superficie, amarelo, (_SOL_X, _SOL_Y), raio)
    pygame.draw.circle(superficie, laranja, (_SOL_X, _SOL_Y), raio, 3)


def jogar():
    global _sol_tick
    fundoMov1 = 0
    fundoMov2 = 1129
    posicaoXPersona = 50
    posicaoYPersona = 300
    movimentoYPersona = 0
    velocidadeMovPersona = 5
    posicaoXMissel = 1000
    posicaoYMissel = 100
    velocidadeMissel = 2
    pontos = 0
    pausado = False
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Item 20: ESC fecha o jogo completamente
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            # Pausa com Espaço (item 11)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                if pausado:
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
            # Movimento só em Y (item 13)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                movimentoYPersona = 0

        if pausado:
            texto_pausa = fontePausa.render("PAUSE", True, amarelo)
            rect_pausa = texto_pausa.get_rect(center=(500, 350))
            tela.blit(texto_pausa, rect_pausa)
            pygame.display.update()
            relogio.tick(60)
            continue

        posicaoYPersona = posicaoYPersona + movimentoYPersona
        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > 580:
            posicaoYPersona = 580

        posicaoXMissel = posicaoXMissel - velocidadeMissel
        if posicaoXMissel < -80:
            pygame.mixer.Sound.play(missileSound)
            posicaoXMissel = 1010
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoYMissel = random.randint(0, 620)

        tela.fill(branco)
        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))
        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -1129:
            fundoMov1 = 1129
        elif fundoMov2 <= -1129:
            fundoMov2 = 1129

        tela.blit(iron, (posicaoXPersona, posicaoYPersona))
        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (700, 15))

        # Dica de pausa discreta
        dica_pausa = fonteMenu.render("Press Space to Pause Game", True, (200, 200, 200))
        tela.blit(dica_pausa, (10, 670))

        # Item 16: sol pulsante no canto superior direito
        _sol_tick += _SOL_VELOCIDADE
        desenhar_sol(tela, _sol_tick)

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + 210))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + 120))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + 80))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + 80))

        if len(list(set(pixelsMisselY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsMisselX).intersection(set(pixelsPersonaX)))) > dificuldade:
                escreverDados(nome, pontos)
                dead(pontos)
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")

        pygame.display.update()
        relogio.tick(60)


def dead(pontos_jogador):
    global _sol_tick
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    # Item 19: fala a pontuação ao morrer
    falar(f"Game over! Você fez {pontos_jogador} pontos.")

    # Busca o maior pontuador atualizado
    nome_top, pts_top, data_top = maior_pontuador()

    larguraButtonStart = 150
    alturaButtonStart = 40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Item 20: ESC fecha o jogo completamente
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart = 35
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 150
                    alturaButtonStart = 40
                    jogar()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        # Botão reiniciar
        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 20))

        # Sua pontuação
        txt_pontos = fonteGrande.render(f"Sua pontuação: {pontos_jogador}", True, branco)
        rect_pontos = txt_pontos.get_rect(topright=(990, 45))
        tela.blit(txt_pontos, rect_pontos)

        # Maior pontuador
        if nome_top:
            txt_top = fonteGrande.render(f"Recorde: {nome_top} - {pts_top} pts - {data_top}", True, amarelo)
            rect_top = txt_top.get_rect(topright=(990, 15))
            tela.blit(txt_top, rect_top)

        # Item 16: sol pulsante na tela de morte também
        _sol_tick += _SOL_VELOCIDADE
        desenhar_sol(tela, _sol_tick)

        pygame.display.update()
        relogio.tick(60)


def boasVindas():
    global _sol_tick
    larguraBtn = 200
    alturaBtn = 50

    # Item 19: fala boas-vindas ao jogador ao entrar na tela inicial
    falar(f"Bem-vindo, {nome}! Prepare-se para jogar.")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Item 20: ESC fecha o jogo completamente
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if btnIniciar.collidepoint(evento.pos):
                    larguraBtn = 190
                    alturaBtn = 45
            elif evento.type == pygame.MOUSEBUTTONUP:
                if btnIniciar.collidepoint(evento.pos):
                    jogar()

        tela.fill(preto)
        tela.blit(fundoStart, (0, 0))

        # Sobreposição escura para legibilidade
        overlay = pygame.Surface((1000, 700), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        tela.blit(overlay, (0, 0))

        # Nome do jogador
        txt_bemvindo = fontePausa.render(f"Olá, {nome}!", True, amarelo)
        rect_bv = txt_bemvindo.get_rect(center=(500, 120))
        tela.blit(txt_bemvindo, rect_bv)

        # Mecânica do jogo
        mecanica = [
            "Como jogar:",
            "  • Use W e S para mover o personagem para CIMA e BAIXO",
            "  • Desvie do bafo do dragão para marcar pontos",
            "  • Cada desvio vale 1 ponto — quanto mais esquiva, mais rápido fica!",
            "  • Pressione ESPAÇO para pausar o jogo",
            "  • Pressione ESC para sair a qualquer momento",
        ]
        y_mec = 220
        for linha in mecanica:
            surf = fonteGrande.render(linha, True, branco)
            tela.blit(surf, (100, y_mec))
            y_mec += 36

        # Maior pontuador
        if nome_maior:
            txt_recorde = fonteGrande.render(
                f"Recorde atual: {nome_maior} — {maior_pontos} pts — {dataJogada}", True, amarelo
            )
            rect_rec = txt_recorde.get_rect(center=(500, 530))
            tela.blit(txt_recorde, rect_rec)
        else:
            txt_recorde = fonteGrande.render("Nenhum recorde ainda. Seja o primeiro!", True, amarelo)
            rect_rec = txt_recorde.get_rect(center=(500, 530))
            tela.blit(txt_recorde, rect_rec)

        # Botão iniciar
        btnIniciar = pygame.draw.rect(tela, branco, (400, 590, larguraBtn, alturaBtn), border_radius=20)
        txt_btn = fonteGrande.render("INICIAR PARTIDA", True, preto)
        rect_btn = txt_btn.get_rect(center=btnIniciar.center)
        tela.blit(txt_btn, rect_btn)

        # Item 16: sol pulsante no canto superior direito da tela de boas-vindas
        _sol_tick += _SOL_VELOCIDADE
        desenhar_sol(tela, _sol_tick)

        pygame.display.update()
        relogio.tick(60)


boasVindas()
