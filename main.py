import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()

pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0:
        break
    else:
        print("Nome Inválido!")

tamanho = (1000, 700)
pygame.display.set_caption("Iron Man do Marcão")
icone = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 220, 0)
vermelho = (200, 0, 0)

fundo = pygame.image.load("bases/end.png")
fundoDead = pygame.image.load("bases/backgroundMorte.png")
fundoStart = pygame.image.load("bases/backgroundInicio.png")

iron = pygame.image.load("bases/steveElytra.png")
iron = pygame.transform.scale(iron, (210, 120))
missel = pygame.image.load("bases/bafoDragao.png")
missel = pygame.transform.scale(missel, (80, 80))
missileSound = pygame.mixer.Sound("bases/missile.wav")
explosaoSound = pygame.mixer.Sound("bases/explosao.wav")
pygame.mixer.music.load("bases/ironsound.mp3")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fontePausa = pygame.font.SysFont("comicsans", 72, bold=True)
fonteGrande = pygame.font.SysFont("comicsans", 24, bold=True)


def jogar():
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
                quit()
            # ESC fecha o jogo (item 20)
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
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
            # Exibe PAUSE no centro (item 11)
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

        # Dica de pausa discreta (item 12)
        dica_pausa = fonteMenu.render("Press Space to Pause Game", True, (200, 200, 200))
        tela.blit(dica_pausa, (10, 670))

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
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    # Busca o maior pontuador atualizado (item 18)
    nome_top, pts_top, data_top = maior_pontuador()

    larguraButtonStart = 150
    alturaButtonStart = 40

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
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

        # Maior pontuador (item 18)
        if nome_top:
            txt_top = fonteGrande.render(f"Recorde: {nome_top} - {pts_top} pts - {data_top}", True, amarelo)
            rect_top = txt_top.get_rect(topright=(990, 15))
            tela.blit(txt_top, rect_top)

        pygame.display.update()
        relogio.tick(60)


def boasVindas():
    # Tela de boas-vindas (item 9)
    larguraBtn = 200
    alturaBtn = 50

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
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

        pygame.display.update()
        relogio.tick(60)


boasVindas()
