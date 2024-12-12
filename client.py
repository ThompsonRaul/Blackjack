import socket
import pygame
import pickle
import sys
from main import calcular_pontos, Carta
import time

LARGURA_TELA, ALTURA_TELA = 1280, 720
pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Blackjack Multiplayer")
relogio = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE_BG = (1, 50, 32)
VERMELHO = (255, 0, 0)
VERDE = (0, 200, 0)

fonte = pygame.font.Font(None, 36)

pygame.scrap.init()

def desenhar_texto_centralizado(texto, y, cor):
    texto_surface = fonte.render(texto, True, cor)
    texto_rect = texto_surface.get_rect(center=(LARGURA_TELA // 2, y))
    tela.blit(texto_surface, texto_rect)

def desenhar_caixa_texto(caixa, texto, ativo):
    pygame.draw.rect(tela, BRANCO, caixa, 2 if ativo else 1)
    texto_surface = fonte.render(texto.replace('\x00', ''), True, BRANCO)
    tela.blit(texto_surface, (caixa.x + 5, caixa.y + 10))

def desenhar_botao(texto, x, y, largura, altura, cor, cor_texto):
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    texto_surface = fonte.render(texto, True, cor_texto)
    texto_rect = texto_surface.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_surface, texto_rect)
    return pygame.Rect(x, y, largura, altura)

def exibir_tela_configuracao():
    caixa_entrada_ip = pygame.Rect(LARGURA_TELA // 2 - 350, ALTURA_TELA // 2 - 50, 700, 50)
    caixa_entrada_porta = pygame.Rect(LARGURA_TELA // 2 - 75, ALTURA_TELA // 2 + 20, 150, 50)
    botao_conectar = pygame.Rect(LARGURA_TELA // 2 - 100, ALTURA_TELA // 2 + 100, 200, 50)

    texto_ip = ''
    texto_porta = ''
    ativo_ip = False
    ativo_porta = False

    while True:
        tela.fill(VERDE_BG)
        desenhar_texto_centralizado("Configuração de Conexão", ALTURA_TELA // 2 - 150, BRANCO)
        desenhar_texto_centralizado("Insira o IP e a Porta do Servidor", ALTURA_TELA // 2 - 100, BRANCO)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if caixa_entrada_ip.collidepoint(evento.pos):
                    ativo_ip = True
                    ativo_porta = False
                elif caixa_entrada_porta.collidepoint(evento.pos):
                    ativo_ip = False
                    ativo_porta = True
                elif botao_conectar.collidepoint(evento.pos):
                    if texto_ip and texto_porta.isdigit():
                        return texto_ip, int(texto_porta)
            elif evento.type == pygame.KEYDOWN:
                if ativo_ip:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_ip = texto_ip[:-1]
                    elif evento.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        texto_clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if texto_clipboard:
                            texto_ip += texto_clipboard.decode("utf-8").replace('\x00', '').strip()
                    else:
                        texto_ip += evento.unicode
                elif ativo_porta:
                    if evento.key == pygame.K_BACKSPACE:
                        texto_porta = texto_porta[:-1]
                    elif evento.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                        texto_clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
                        if texto_clipboard:
                            texto_porta += texto_clipboard.decode("utf-8").replace('\x00', '').strip()
                    else:
                        texto_porta += evento.unicode

        desenhar_caixa_texto(caixa_entrada_ip, texto_ip, ativo_ip)
        desenhar_caixa_texto(caixa_entrada_porta, texto_porta, ativo_porta)
        desenhar_botao("Conectar", botao_conectar.x, botao_conectar.y, botao_conectar.width, botao_conectar.height, VERDE, BRANCO)

        pygame.display.flip()
        relogio.tick(30)

def mostrar_mao_pygame(mao, x, y):
    for idx, carta in enumerate(mao):
        if not hasattr(carta, 'imagem_carregada'):
            carta.carregar_imagem()
            carta.imagem_carregada = True
        if carta.imagem:
            rect = carta.imagem.get_rect()
            rect.topleft = (x + idx * 110, y)
            tela.blit(carta.imagem, rect)

def exibir_tela_espera():
    tela.fill(VERDE_BG)
    titulo_fonte = pygame.font.Font(None, 72)
    titulo_surface = titulo_fonte.render("Blackjack", True, PRETO)
    titulo_rect = titulo_surface.get_rect(center=(LARGURA_TELA//2, ALTURA_TELA//2 - 100))
    tela.blit(titulo_surface, titulo_rect)
    desenhar_texto_centralizado("Aguardando outros jogadores...", ALTURA_TELA // 2, PRETO)
    pygame.display.flip()

def exibir_estado(jogador_id, estado):
    tela.fill(VERDE_BG)
    desenhar_texto_centralizado(f"Jogador {(jogador_id + 1) % 2 + 1}: ?", 50, PRETO)
    oponente_mao = estado['jogador'].get('mao', [])
    for i in range(len(oponente_mao)):
        carta_costas = pygame.Surface((100, 150))
        carta_costas.fill((0, 0, 139))
        tela.blit(carta_costas, (LARGURA_TELA // 2 - len(oponente_mao) * 55 + i * 110, 100))

    jogador = estado['jogador']
    if jogador and 'mao' in jogador:
        pontos = calcular_pontos(jogador['mao'])
        texto = f"Sua mão: {pontos} pontos"
        desenhar_texto_centralizado(texto, ALTURA_TELA - 50, PRETO)
        mostrar_mao_pygame(jogador['mao'], LARGURA_TELA // 2 - len(jogador['mao']) * 55, ALTURA_TELA - 300)

    if not estado['jogador'].get('pronto', False):
        if estado['turno_atual'] == jogador_id:
            desenhar_texto_centralizado("Sua vez!", ALTURA_TELA // 2, VERDE)
            botao_puxar = desenhar_botao("Puxar", 50, ALTURA_TELA - 100, 200, 50, VERDE, BRANCO)
            botao_passar = desenhar_botao("Passar", 300, ALTURA_TELA - 100, 200, 50, VERMELHO, BRANCO)
            return botao_puxar, botao_passar
        else:
            desenhar_texto_centralizado("Vez do oponente...", ALTURA_TELA // 2, VERMELHO)
    return None, None

def exibir_resultado_final(jogador_id, resultados, comparacao):
    tela.fill(VERDE_BG)
    desenhar_texto_centralizado("Fim de Jogo!", 150, PRETO)
    
    pontos_jogador = resultados.get(jogador_id, 0)
    pontos_oponente = resultados.get((jogador_id + 1) % 2, 0)
    
    desenhar_texto_centralizado(f"Sua pontuação: {pontos_jogador}", ALTURA_TELA // 2 - 100, PRETO)
    desenhar_texto_centralizado(f"Pontuação do oponente: {pontos_oponente}", ALTURA_TELA // 2 - 50, PRETO)
    
    pygame.draw.line(tela, PRETO, 
                    (LARGURA_TELA//4, ALTURA_TELA//2),
                    (3*LARGURA_TELA//4, ALTURA_TELA//2), 2)
    
    desenhar_texto_centralizado("Resultado Final:", ALTURA_TELA // 2 + 50, PRETO)
    cor_resultado = VERDE if f"Jogador {jogador_id + 1} venceu" in comparacao else VERMELHO
    desenhar_texto_centralizado(comparacao, ALTURA_TELA // 2 + 100, cor_resultado)
    
    botao_sair = desenhar_botao("Sair", LARGURA_TELA/2 - 110, ALTURA_TELA - 150, 200, 50, VERMELHO, BRANCO)
    
    pygame.display.flip()
    return botao_sair

def iniciar_cliente():
    ip, porta = exibir_tela_configuracao()
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            try:
                cliente.connect((ip, porta))
                print("Conectado ao servidor.")

                dados = cliente.recv(4096)
                mensagem = pickle.loads(dados)
                jogador_id = mensagem.get('jogador_id')
                print(f"Você é o jogador {jogador_id}.")

                cliente.settimeout(0.1)

                estado = None
                rodando = True
                botao_puxar = None
                botao_passar = None
                em_tela_final = False
                botao_sair = None
                resultados = None
                comparacao = None
                jogo_iniciado = False
                ultimo_update = time.time()
                INTERVALO_UPDATE = 0.5  

                while rodando:
                    tempo_atual = time.time()
                    
                    # Processa eventos do Pygame
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            return False
                        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                            pos_mouse = pygame.mouse.get_pos()
                            if em_tela_final:
                                if botao_sair and botao_sair.collidepoint(pos_mouse):
                                    return False
                            elif estado and estado['turno_atual'] == jogador_id:
                                if botao_puxar and botao_puxar.collidepoint(pos_mouse):
                                    cliente.sendall(pickle.dumps({'tipo': 'puxar'}))
                                elif botao_passar and botao_passar.collidepoint(pos_mouse):
                                    cliente.sendall(pickle.dumps({'tipo': 'passar'}))

                    if tempo_atual - ultimo_update >= INTERVALO_UPDATE:
                        try:
                            while True:  
                                try:
                                    dados = cliente.recv(4096)
                                    if dados:
                                        mensagem = pickle.loads(dados)
                                        if mensagem['acao'] == 'estado':
                                            estado = mensagem['estado']
                                            jogo_iniciado = True
                                        elif mensagem['acao'] == 'fim':
                                            print("Jogo finalizado!")
                                            resultados = mensagem.get('resultados', {})
                                            comparacao = mensagem.get('comparacao', "Sem comparação disponível.")
                                            em_tela_final = True
                                except socket.timeout:
                                    break  

                        except Exception as e:
                            if not isinstance(e, socket.timeout):
                                print(f"Erro ao receber dados: {e}")

                        if em_tela_final:
                            botao_sair = exibir_resultado_final(jogador_id, resultados, comparacao)
                        elif jogo_iniciado and estado:
                            botao_puxar, botao_passar = exibir_estado(jogador_id, estado)
                        else:
                            exibir_tela_espera()
                        
                        pygame.display.flip()
                        ultimo_update = tempo_atual

                    relogio.tick(60)

            except Exception as e:
                print(f"Erro de conexão: {e}")
                return False

if __name__ == "__main__":
    iniciar_cliente()
    pygame.quit()