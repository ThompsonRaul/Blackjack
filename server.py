import socket
import pickle
import threading
from main import Baralho, calcular_pontos, comparar_jogadores

HOST = '0.0.0.0'
PORT = 65432

class ServidorBlackjack:

    def __init__(self, ip, porta):
        self.ip = ip
        self.porta = porta
        self.socket_servidor = None
        self.cliente = {}  
        self.estado_jogo = {
            'jogadores': {
                0: {'mao': [], 'pronto': False},
                1: {'mao': [], 'pronto': False}
            },
            'turno_atual': 0,
            'baralho': None,
            'jogo_finalizado': False
        }
        self.lock = threading.Lock()
        self.arquivo_log = open("log.txt", "a", encoding="utf-8")

    def log(self, msg):
        self.arquivo_log.write(msg + "\n")
        self.arquivo_log.flush()
        print(msg)

    def start(self):
        self.log("Iniciando servidor Blackjack...")
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.ip, self.porta))
        self.socket_servidor.listen(2)
        self.log(f"Servidor aguardando conexões em {self.ip}:{self.porta}...")

  
        for id_jogador in range(2):
            socket_cliente, addr = self.socket_servidor.accept()
            self.log(f"Jogador {id_jogador} conectado: {addr}")
            self.cliente[id_jogador] = socket_cliente
            msg_id = {'jogador_id': id_jogador}
            self.log(f"Enviando ID para jogador {id_jogador}: {msg_id}")
            self.enviar_jogador(id_jogador, msg_id)

        
        self.iniciar_jogo()

        for id_jogador in range(2):
            t = threading.Thread(target=self.processar_cliente, args=(id_jogador,))
            t.start()

    def iniciar_jogo(self):
        with self.lock:
            self.estado_jogo['baralho'] = Baralho()
            for p_id in [0,1]:
                self.estado_jogo['jogadores'][p_id]['mao'] = [
                    self.estado_jogo['baralho'].puxar_carta(),
                    self.estado_jogo['baralho'].puxar_carta()
                ]
                self.estado_jogo['jogadores'][p_id]['pronto'] = False
            
            self.estado_jogo['turno_atual'] = 0
            self.estado_jogo['jogo_finalizado'] = False
        
        self.log("Jogo iniciado. Estado inicial:")
        self.log(str(self.estado_jogo))
        self.enviar_estado()

    def processar_cliente(self, id_jogador):
        socket_cliente = self.cliente[id_jogador]
        socket_cliente.settimeout(None)

        self.log(f"Iniciando loop de recebimento para jogador {id_jogador}.")
        while True:
            try:
                data = socket_cliente.recv(4096)
                if not data:
                    self.log(f"Jogador {id_jogador} desconectou.")
                    self.cliente[id_jogador].close()
                    break

                mensagem = pickle.loads(data)
                self.log(f"Mensagem recebida do jogador {id_jogador}: {mensagem}")

                if 'tipo' in mensagem:
                    self.acao_player(id_jogador, mensagem['tipo'])

            except Exception as e:
                self.log(f"Erro no tratamento do jogador {id_jogador}: {e}")
                break

    def acao_player(self, id_jogador, acao):
        self.log(f"Processando ação do jogador {id_jogador}: {acao}")
        with self.lock:
            if self.estado_jogo['jogo_finalizado']:
                self.log("Ação ignorada: jogo já finalizado.")
                return

            if self.estado_jogo['turno_atual'] == id_jogador:
                if acao == 'puxar':
                    carta = self.estado_jogo['baralho'].puxar_carta()
                    if carta:
                        self.estado_jogo['jogadores'][id_jogador]['mao'].append(carta)
                        self.log(f"Jogador {id_jogador} puxou {carta}.")
                        pontos = calcular_pontos(self.estado_jogo['jogadores'][id_jogador]['mao'])
                        self.log(f"Pontuação do jogador {id_jogador}: {pontos}")
                        if pontos > 21:
                            self.log(f"Jogador {id_jogador} estourou!")
                            self.passar_vez()
                    else:
                        self.log("Baralho vazio. Passando vez automaticamente.")
                        self.passar_vez()

                elif acao == 'passar':
                    self.log(f"Jogador {id_jogador} passou a vez.")
                    self.passar_vez()

        self.verificar_fim()
        if not self.estado_jogo['jogo_finalizado']:
            self.enviar_estado()

    def passar_vez(self):
        jogador_atual = self.estado_jogo['turno_atual']
        self.estado_jogo['jogadores'][jogador_atual]['pronto'] = True
        outro_jogador = (jogador_atual + 1) % 2
        self.log(f"Jogador {jogador_atual} está pronto. Verificando o outro jogador.")
        if self.estado_jogo['jogadores'][outro_jogador]['pronto']:
            self.log("Ambos os jogadores prontos. Jogo será finalizado.")
            self.estado_jogo['jogo_finalizado'] = True
        else:
            self.estado_jogo['turno_atual'] = outro_jogador
            self.log(f"Agora é a vez do jogador {outro_jogador}.")

    def verificar_fim(self):
        if self.estado_jogo['jogo_finalizado']:
            resultados = {
                0: calcular_pontos(self.estado_jogo['jogadores'][0]['mao']),
                1: calcular_pontos(self.estado_jogo['jogadores'][1]['mao'])
            }
            comparacao = comparar_jogadores(self.estado_jogo['jogadores'])
            msg = {
                'acao': 'fim',
                'resultados': resultados,
                'comparacao': comparacao
            }
            self.log("Jogo finalizado. Resultados:")
            self.log(str(resultados))
            self.log("Comparação: " + comparacao)
            self.enviar_todos(msg)

    def enviar_estado(self):
        self.log("Enviando estado para ambos os jogadores.")
        for p_id in [0,1]:
            estado_envio = {
                'acao': 'estado',
                'estado': {
                    'jogador': self.estado_jogo['jogadores'][p_id],
                    'turno_atual': self.estado_jogo['turno_atual']
                }
            }
            self.log(f"Estado para jogador {p_id}: {estado_envio}")
            self.enviar_jogador(p_id, estado_envio)

    def enviar_jogador(self, id_jogador, data):
        try:
            self.log(f"Enviando para jogador {id_jogador}: {data}")
            self.cliente[id_jogador].sendall(pickle.dumps(data))
        except Exception as e:
            self.log(f"Erro ao enviar dados para jogador {id_jogador}: {e}")

    def enviar_todos(self, data):
        self.log(f"Enviando para todos: {data}")
        for p_id in self.cliente:
            self.enviar_jogador(p_id, data)

    def __del__(self):
        if hasattr(self, 'arquivo_log') and self.arquivo_log:
            self.arquivo_log.close()


if __name__ == "__main__":
    servidor = ServidorBlackjack(HOST, PORT)
    servidor.start()
