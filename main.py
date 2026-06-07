import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

import pyttsx3

def falar(texto):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(texto)
    engine.runAndWait()

limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()

pygame.init()

while True:
    nome = input("Informe o Nome do Competidor:")
    if len(nome) > 0:
        break
    else:
        print("Nome Invalido!")

tamanho = (1000, 700)
pygame.display.set_caption("Iron Man do Marcao")
icone = pygame.image.load("bases/bafoDragao.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 220, 0)
vermelho = (200, 0, 0)
laranja = (255, 165, 0)
cinza_lua = (210, 210, 230)
cinza_lua_escuro = (150, 150, 170)

fundo = pygame.image.load("bases/end.png")
fundoDead = pygame.image.load("bases/backgroundMorte.png")
fundoStart = pygame.image.load("bases/backgroundInicio.png")

iron = pygame.image.load("bases/steveElytra.png")
iron = pygame.transform.scale(iron, (210, 120))
missel = pygame.image.load("bases/bafoDragao.png")
missel = pygame.transform.scale(missel, (80, 80))
enderman = pygame.image.load("bases/enderman.png")
missileSound = pygame.mixer.Sound("bases/enderDragon.wav")
explosaoSound = pygame.mixer.Sound("bases/explosao.wav")
pygame.mixer.music.load("bases/musicend.mp3")
fonteMenu = pygame.font.SysFont("comicsans", 18)
fontePausa = pygame.font.SysFont("comicsans", 72, bold=True)
fonteGrande = pygame.font.SysFont("comicsans", 24, bold=True)

# Lua vibrante — posicao base no canto superior direito
_LUA_X_BASE = 950
_LUA_Y_BASE = 50
_LUA_RAIO = 35
_VIBRA_AMPLI = 3        # amplitude da vibracao em pixels
_VIBRA_SPEED = 4        # frames por passo de vibracao


def desenhar_lua(superficie):
    """Desenha uma lua crescente que vibra levemente usando o tempo atual."""
    passo = (pygame.time.get_ticks() // (1000 // _VIBRA_SPEED * 10)) % 4
    if passo == 0:
        ox, oy = 0, 0
    elif passo == 1:
        ox, oy = _VIBRA_AMPLI, -_VIBRA_AMPLI
    elif passo == 2:
        ox, oy = 0, 0
    else:
        ox, oy = -_VIBRA_AMPLI, _VIBRA_AMPLI

    x = _LUA_X_BASE + ox
    y = _LUA_Y_BASE + oy

    pygame.draw.circle(superficie, cinza_lua, (x, y), _LUA_RAIO)
    pygame.draw.circle(superficie, (30, 20, 60), (x + 14, y - 6), _LUA_RAIO - 4)
    pygame.draw.circle(superficie, cinza_lua_escuro, (x, y), _LUA_RAIO, 2)


def jogar():
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

    # Objetos decorativos (4 endermen) — cada um teleporta a cada 2 segundos
    obj_x  = random.randint(300, 900)
    obj_y  = random.randint(500, 620)
    obj2_x = random.randint(300, 900)
    obj2_y = random.randint(500, 620)
    obj3_x = random.randint(300, 900)
    obj3_y = random.randint(500, 620)
    obj4_x = random.randint(300, 900)
    obj4_y = random.randint(500, 620)
    obj_ultimo_teleporte  = pygame.time.get_ticks()
    obj2_ultimo_teleporte = pygame.time.get_ticks()
    obj3_ultimo_teleporte = pygame.time.get_ticks()
    obj4_ultimo_teleporte = pygame.time.get_ticks()
    OBJ_INTERVALO = 2000

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                if pausado:
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()
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
        tela.blit(fundo, (0, 0))

        # Endermen teleportam a cada 2 segundos
        agora = pygame.time.get_ticks()
        if agora - obj_ultimo_teleporte >= OBJ_INTERVALO:
            obj_x = random.randint(0, 900)
            obj_y = random.randint(500, 620)
            obj_ultimo_teleporte = agora
        if agora - obj2_ultimo_teleporte >= OBJ_INTERVALO:
            obj2_x = random.randint(0, 900)
            obj2_y = random.randint(500, 620)
            obj2_ultimo_teleporte = agora
        if agora - obj3_ultimo_teleporte >= OBJ_INTERVALO:
            obj3_x = random.randint(0, 900)
            obj3_y = random.randint(500, 620)
            obj3_ultimo_teleporte = agora
        if agora - obj4_ultimo_teleporte >= OBJ_INTERVALO:
            obj4_x = random.randint(0, 900)
            obj4_y = random.randint(500, 620)
            obj4_ultimo_teleporte = agora
        tela.blit(enderman, (obj_x,  obj_y))
        tela.blit(enderman, (obj2_x, obj2_y))
        tela.blit(enderman, (obj3_x, obj3_y))
        tela.blit(enderman, (obj4_x, obj4_y))

        tela.blit(iron, (posicaoXPersona, posicaoYPersona))
        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        texto = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (700, 15))

        dica_pausa = fonteMenu.render("Press Space to Pause Game", True, (200, 200, 200))
        tela.blit(dica_pausa, (10, 670))

        # Lua vibrante
        desenhar_lua(tela)

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
    falar("Game Over")

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

        startButton = pygame.draw.rect(tela, branco, (10, 10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 20))

        txt_pontos = fonteGrande.render(f"Sua pontuacao: {pontos_jogador}", True, branco)
        rect_pontos = txt_pontos.get_rect(topright=(990, 45))
        tela.blit(txt_pontos, rect_pontos)

        if nome_top:
            txt_top = fonteGrande.render(f"Recorde: {nome_top} - {pts_top} pts - {data_top}", True, amarelo)
            rect_top = txt_top.get_rect(topright=(990, 15))
            tela.blit(txt_top, rect_top)

        pygame.display.update()
        relogio.tick(60)


def boasVindas():
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

        overlay = pygame.Surface((1000, 700), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        tela.blit(overlay, (0, 0))

        txt_bemvindo = fontePausa.render(f"Ola, {nome}!", True, amarelo)
        rect_bv = txt_bemvindo.get_rect(center=(500, 120))
        tela.blit(txt_bemvindo, rect_bv)

        mecanica = [
            "Como jogar:",
            "  * Use W e S para mover o personagem CIMA e BAIXO",
            "  * Desvie do bafo do dragao para marcar pontos",
            "  * Cada desvio vale 1 ponto - quanto mais esquiva, mais rapido fica!",
            "  * Pressione ESPACO para pausar o jogo",
            "  * Pressione ESC para sair a qualquer momento",
        ]
        y_mec = 220
        for linha in mecanica:
            surf = fonteGrande.render(linha, True, branco)
            tela.blit(surf, (100, y_mec))
            y_mec += 36

        if nome_maior:
            txt_recorde = fonteGrande.render(
                f"Recorde atual: {nome_maior} - {maior_pontos} pts - {dataJogada}", True, amarelo
            )
        else:
            txt_recorde = fonteGrande.render("Nenhum recorde ainda. Seja o primeiro!", True, amarelo)
        rect_rec = txt_recorde.get_rect(center=(500, 530))
        tela.blit(txt_recorde, rect_rec)

        btnIniciar = pygame.draw.rect(tela, branco, (400, 590, larguraBtn, alturaBtn), border_radius=20)
        txt_btn = fonteGrande.render("INICIAR PARTIDA", True, preto)
        rect_btn = txt_btn.get_rect(center=btnIniciar.center)
        tela.blit(txt_btn, rect_btn)

        pygame.display.update()
        relogio.tick(60)


boasVindas()
