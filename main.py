import os
import random
import sys
import pygame

pygame.init()

class Carta:
    CARDS_PATH = os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))),'cartas')
    _imagens_cache = {}

    def __init__(self, valor, naipe):
        self.valor = valor
        self.naipe = naipe
        self.cor = 'vermelho' if naipe in ['Copas', 'Ouros'] else 'preto'
        self._imagem = None

    def __getstate__(self):
        state = self.__dict__.copy()
        state['_imagem'] = None
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

    def __str__(self):
        return f"{self.valor} de {self.naipe}"

    def pontos(self):
        if self.valor in ['J', 'Q', 'K']:
            return 10
        elif self.valor == 'A':
            return 11
        return int(self.valor)

    def _gerar_chave_cache(self):
        return f"{self.cor}_{self.valor}_{self.naipe}"

    @property
    def imagem(self):
        if self._imagem is None:
            self.carregar_imagem()
        return self._imagem

    def carregar_imagem(self):
        chave = self._gerar_chave_cache()
        if chave in Carta._imagens_cache:
            self._imagem = Carta._imagens_cache[chave]
            return

        naipe_map = {
            'Copas': 'copas',
            'Ouros': 'ouros',
            'Espadas': 'espadas',
            'Paus': 'paus'
        }

        cor_prefix = 'vermelho' if self.cor == 'vermelho' else 'preto'
        naipe_nome = naipe_map[self.naipe]
        nome_arquivo = f"{cor_prefix}_{self.valor}_{naipe_nome}.jpg"
        caminho_imagem = os.path.join(self.CARDS_PATH, nome_arquivo)

        try:
            imagem_original = pygame.image.load(caminho_imagem)
            imagem_redimensionada = pygame.transform.scale(imagem_original, (100, 150))
            Carta._imagens_cache[chave] = imagem_redimensionada
            self._imagem = imagem_redimensionada
        except Exception as e:
            print(f"Erro ao carregar imagem da carta {nome_arquivo}: {e}")

class Baralho:
    def __init__(self):
        naipes = ['Copas', 'Ouros', 'Espadas', 'Paus']
        valores = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cartas = [Carta(valor, naipe) for naipe in naipes for valor in valores]
        random.shuffle(self.cartas)

    def puxar_carta(self):
        return self.cartas.pop() if self.cartas else None

    def __str__(self):
        return f"Baralho com {len(self.cartas)} cartas restantes."

def calcular_pontos(mao):
    pontos = sum(carta.pontos() for carta in mao)
    ases = sum(1 for carta in mao if carta.valor == 'A')
    while pontos > 21 and ases:
        pontos -= 10
        ases -= 1
    return pontos

def comparar_jogadores(jogadores):
    pontos = {jogador_id: calcular_pontos(dados['mao']) for jogador_id, dados in jogadores.items()}
    jogador_ids = list(pontos.keys())
    
    if pontos[jogador_ids[0]] > 21 and pontos[jogador_ids[1]] > 21:
        return "Empate! Ambos os jogadores estouraram."
    elif pontos[jogador_ids[0]] > 21:
        return f"Jogador 2 venceu com {pontos[jogador_ids[1]]} pontos! (Jogador 1 estourou)"
    elif pontos[jogador_ids[1]] > 21:
        return f"Jogador 1 venceu com {pontos[jogador_ids[0]]} pontos! (Jogador 2 estourou)"
    elif pontos[jogador_ids[0]] > pontos[jogador_ids[1]]:
        return f"Jogador 1 venceu com {pontos[jogador_ids[0]]} pontos contra {pontos[jogador_ids[1]]} pontos"
    elif pontos[jogador_ids[0]] < pontos[jogador_ids[1]]:
        return f"Jogador 2 venceu com {pontos[jogador_ids[1]]} pontos contra {pontos[jogador_ids[0]]} pontos"
    else:
        return f"Empate! Ambos os jogadores fizeram {pontos[jogador_ids[0]]} pontos"
