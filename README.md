# Blackjack Multiplayer

## Propósito do Software

Este software implementa um jogo de Blackjack multiplayer, permitindo que dois jogadores se conectem a um servidor e joguem uma partida de Blackjack em tempo real. O jogo é desenvolvido em Python e utiliza a biblioteca Pygame para a interface gráfica.

## Motivação da Escolha do Protocolo de Transporte

O protocolo de transporte escolhido foi o TCP (Transmission Control Protocol) devido às suas características de confiabilidade e controle de fluxo. O TCP garante que todas as mensagens enviadas entre o servidor e os clientes sejam entregues na ordem correta e sem perdas, o que é essencial para a integridade do estado do jogo.

## Requisitos Mínimos de Funcionamento

- Python 3.6 ou superior
- Biblioteca Pygame instalada (`pip install pygame`)
- Conexão de rede para comunicação entre o servidor e os clientes
- Imagens das cartas localizadas no diretório `cartas`

## Funcionamento do Software

### Servidor

O servidor é responsável por:

- Aceitar conexões de dois jogadores
- Inicializar o estado do jogo e distribuir cartas
- Gerenciar o turno dos jogadores
- Processar as ações dos jogadores (puxar carta, passar vez)
- Verificar o fim do jogo e calcular os resultados
- Enviar atualizações do estado do jogo para os jogadores

### Cliente

O cliente é responsável por:

- Conectar-se ao servidor
- Receber o estado do jogo e atualizações do servidor
- Exibir a interface gráfica do jogo usando Pygame
- Enviar ações do jogador (puxar carta, passar vez) para o servidor

## Protocolo da Camada de Aplicação

### Eventos e Mensagens

### Logs

O servidor registra eventos importantes no arquivo `log.txt`. Cada entrada de log inclui:

- Informações sobre conexões e desconexões dos jogadores.
- Ações realizadas pelos jogadores, como puxar uma carta ou passar a vez.
- Estado do jogo ao final de cada ação.
- Mensagens de erro ou exceções capturadas.

Exemplo de log completo:

```
Iniciando servidor Blackjack...
Servidor aguardando conexões em :::65432...
Jogador 0 conectado: ('2804:14d:ed28:832e:4010:f18f:4ad9:60a8', 5859, 0, 0)
Enviando ID para jogador 0: {'jogador_id': 0}
Enviando para jogador 0: {'jogador_id': 0}
Jogador 1 conectado: ('2804:14d:ed27:84ce:8116:64c1:87db:abf2', 49807, 0, 0)
Enviando ID para jogador 1: {'jogador_id': 1}
Enviando para jogador 1: {'jogador_id': 1}
Jogo iniciado. Estado inicial:
{'jogadores': {0: {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>], 'pronto': False}, 1: {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}}, 'turno_atual': 0, 'baralho': <main.Baralho object at 0x0000025D0ECBB410>, 'jogo_finalizado': False}
Enviando estado para ambos os jogadores.
Estado para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>], 'pronto': False}, 'turno_atual': 0}}
Enviando para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>], 'pronto': False}, 'turno_atual': 0}}
Estado para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 0}}
Enviando para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 0}}
Iniciando loop de recebimento para jogador 0.
Iniciando loop de recebimento para jogador 1.
Mensagem recebida do jogador 0: {'tipo': 'puxar'}
Processando ação do jogador 0: puxar
Jogador 0 puxou 6 de Paus.
Pontuação do jogador 0: 18
Enviando estado para ambos os jogadores.
Estado para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': False}, 'turno_atual': 0}}
Enviando para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': False}, 'turno_atual': 0}}
Estado para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 0}}
Enviando para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 0}}
Mensagem recebida do jogador 0: {'tipo': 'passar'}
Processando ação do jogador 0: passar
Jogador 0 passou a vez.
Jogador 0 está pronto. Verificando o outro jogador.
Agora é a vez do jogador 1.
Enviando estado para ambos os jogadores.
Estado para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': True}, 'turno_atual': 1}}
Enviando para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': True}, 'turno_atual': 1}}
Estado para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 1}}
Enviando para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>], 'pronto': False}, 'turno_atual': 1}}
Mensagem recebida do jogador 1: {'tipo': 'puxar'}
Processando ação do jogador 1: puxar
Jogador 1 puxou 6 de Ouros.
Pontuação do jogador 1: 19
Enviando estado para ambos os jogadores.
Estado para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': True}, 'turno_atual': 1}}
Enviando para jogador 0: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711C830>, <main.Carta object at 0x0000025D0FFC58E0>, <main.Carta object at 0x0000025D2711CDD0>], 'pronto': True}, 'turno_atual': 1}}
Estado para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>, <main.Carta object at 0x0000025D2711C560>], 'pronto': False}, 'turno_atual': 1}}
Enviando para jogador 1: {'acao': 'estado', 'estado': {'jogador': {'mao': [<main.Carta object at 0x0000025D2711CD70>, <main.Carta object at 0x0000025D2711C9B0>, <main.Carta object at 0x0000025D2711C560>], 'pronto': False}, 'turno_atual': 1}}
Mensagem recebida do jogador 1: {'tipo': 'passar'}
Processando ação do jogador 1: passar
Jogador 1 passou a vez.
Jogador 1 está pronto. Verificando o outro jogador.
Ambos os jogadores prontos. Jogo será finalizado.
Jogo finalizado. Resultados:
{0: 18, 1: 19}
Comparação: Jogador 2 venceu com 19 pontos contra 18 pontos
Enviando para todos: {'acao': 'fim', 'resultados': {0: 18, 1: 19}, 'comparacao': 'Jogador 2 venceu com 19 pontos contra 18 pontos'}
Enviando para jogador 0: {'acao': 'fim', 'resultados': {0: 18, 1: 19}, 'comparacao': 'Jogador 2 venceu com 19 pontos contra 18 pontos'}
Enviando para jogador 1: {'acao': 'fim', 'resultados': {0: 18, 1: 19}, 'comparacao': 'Jogador 2 venceu com 19 pontos contra 18 pontos'}
Jogador 0 desconectou.
```

O arquivo de log é mantido no mesmo diretório do servidor e pode ser usado para depuração ou análise posterior.

### Estados do Jogo

1. **Inicialização**

   - O servidor aguarda a conexão de dois jogadores.
   - Após a conexão, o servidor envia o ID do jogador para cada cliente.

2. **Distribuição de Cartas**

   - O servidor inicializa o baralho e distribui duas cartas para cada jogador.
   - O estado inicial do jogo é enviado para os jogadores.

3. **Turno dos Jogadores**

   - O servidor gerencia o turno dos jogadores.
   - O jogador atual pode puxar uma carta ou passar a vez.
   - O estado atualizado do jogo é enviado para os jogadores após cada ação.

4. **Fim do Jogo**
   - O servidor verifica se o jogo terminou (todos os jogadores passaram a vez ou estouraram).
   - Os resultados finais e a comparação dos jogadores são enviados para os clientes.

## Como Executar

### Iniciar o Servidor

1.  Abra um terminal.
2.  Navegue até o diretório onde o arquivo server.py está localizado.
3.  Execute o servidor com o comando:

        python server.py

### Iniciar o Cliente

1.  Abra outro terminal.
2.  Navegue até o diretório onde o arquivo client.py está localizado.
3.  Execute o cliente com o comando:

        python client.py

4.  Digite o IPv4 público do servidor e a porta

### Conectar Dois Clientes

Repita o processo de iniciar o cliente em outro terminal ou em outra máquina para conectar o segundo jogador ao servidor.

### Referências

- [Cartas](https://cardscans.piwigo.com/index?/search/psk-20241212-OkVovpUMTA)
