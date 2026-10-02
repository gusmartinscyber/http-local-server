# HTTP Local Server

Projeto didático para observar, de forma prática, como uma comunicação HTTP funciona sobre TCP. O repositório inclui uma página HTML simples, testes HTTP manuais e uma implementação mínima de cliente e servidor utilizando a biblioteca `socket` do Python.

O projeto utiliza exclusivamente o endereço de loopback `127.0.0.1` e a porta `8080`, portanto cliente e servidor executam na mesma máquina por padrão.

## Funcionalidades

- servidor HTTP local utilizando o módulo nativo `http.server` do Python;
- acesso à página `index.html` pelo navegador;
- envio manual de requisições HTTP com `nc` (Netcat);
- comparação entre respostas HTTP `200 OK` e `404 Not Found`;
- servidor TCP próprio implementado com `socket`;
- cliente TCP próprio implementado com `socket`;
- exibição da requisição e da resposta HTTP no terminal;
- registro de IP, porta e quantidade de bytes transmitidos;
- exemplos de cálculos de atraso de transmissão, atraso de propagação e vazão fim a fim.

## Estrutura do projeto

```text
exercicio_http_local/
├── cliente.py
├── index.html
├── servidor.py
└── README.md
```

### `index.html`

Página utilizada pelo servidor HTTP local. Ao acessá-la pelo navegador, ela confirma que o conteúdo foi entregue pela porta `8080`.

### `servidor.py`

Servidor TCP mínimo que:

1. cria um socket IPv4/TCP;
2. associa o socket a `127.0.0.1:8080`;
3. aguarda uma conexão;
4. recebe uma requisição HTTP;
5. exibe IP e porta do cliente;
6. exibe a requisição recebida;
7. envia uma resposta `HTTP/1.1 200 OK`;
8. exibe a resposta enviada;
9. encerra a conexão e registra data e hora.

O servidor atende uma conexão por execução, propositalmente, para manter o fluxo de comunicação simples de observar.

### `cliente.py`

Cliente TCP que:

1. conecta ao servidor em `127.0.0.1:8080`;
2. envia uma requisição `GET / HTTP/1.1`;
3. informa a quantidade de bytes enviados;
4. recebe a resposta completa;
5. informa a quantidade de bytes recebidos;
6. exibe a resposta HTTP no terminal;
7. encerra a conexão.

## Requisitos

- Python 3;
- Netcat (`nc`) para o teste HTTP manual;
- navegador web para visualizar `index.html`.

Não são necessárias bibliotecas Python externas.

Para verificar o Python:

```bash
python3 --version
```

Para verificar o Netcat:

```bash
nc -h
```

## Como utilizar

Entre na pasta do projeto:

```bash
cd exercicio_http_local
```

### 1. Servidor HTTP local

O Python possui um servidor HTTP simples embutido. Para disponibilizar os arquivos da pasta em `127.0.0.1:8080`, execute:

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

O terminal deverá exibir uma mensagem semelhante a:

```text
Serving HTTP on 127.0.0.1 port 8080 ...
```

Abra no navegador:

```text
http://localhost:8080
```

Nesse cenário:

- **cliente:** navegador web;
- **servidor:** processo `python3 -m http.server`;
- **endereço:** `127.0.0.1`;
- **porta:** `8080`;
- **protocolo de aplicação:** HTTP;
- **protocolo de transporte:** TCP.

`127.0.0.1` é o endereço de loopback. O tráfego permanece na própria máquina.

### 2. Teste HTTP manual com Netcat

Com o servidor HTTP anterior ainda executando, abra outro terminal:

```bash
nc 127.0.0.1 8080
```

Envie a seguinte requisição:

```http
GET / HTTP/1.1
Host: localhost

```

É necessário deixar uma linha vazia depois de `Host: localhost`.

Uma requisição válida para `/` deverá produzir uma resposta iniciada por algo equivalente a:

```http
HTTP/1.0 200 OK
```

O código `200` indica que o recurso solicitado foi encontrado e entregue.

Para testar um recurso inexistente, conecte novamente:

```bash
nc 127.0.0.1 8080
```

E envie:

```http
GET /nao-existe.html HTTP/1.1
Host: localhost

```

A resposta deverá indicar `404`, por exemplo:

```http
HTTP/1.0 404 File not found
```

`404 Not Found` significa que o servidor recebeu e compreendeu a requisição, mas não encontrou o recurso solicitado.

#### Por que a linha vazia é necessária?

No HTTP/1.x, as linhas dos cabeçalhos terminam com `CRLF` (`\r\n`). O final dos cabeçalhos é indicado por uma linha vazia, formando:

```text
\r\n\r\n
```

Essa sequência informa ao servidor que a seção de cabeçalhos terminou. Sem ela, o servidor pode continuar esperando mais dados antes de processar a requisição.

### 3. Cliente e servidor próprios com sockets

Antes de iniciar `servidor.py`, encerre o servidor `http.server` anterior com `Ctrl+C`, pois ambos utilizam a porta `8080`.

No primeiro terminal, execute:

```bash
python3 servidor.py
```

Saída inicial esperada:

```text
Servidor aguardando conexão em 127.0.0.1:8080...
```

Em outro terminal, execute:

```bash
python3 cliente.py
```

O cliente estabelecerá uma conexão TCP e enviará:

```http
GET / HTTP/1.1
Host: localhost
Connection: close

```

O servidor responderá com uma mensagem HTTP semelhante a:

```http
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: ...
Connection: close

<h1>Resposta do servidor com sockets</h1>
```

No terminal do servidor serão exibidos:

- IP e porta de origem do cliente;
- conteúdo completo da requisição;
- resposta HTTP enviada;
- data e hora do encerramento da conexão.

No terminal do cliente serão exibidos:

- endereço do servidor;
- porta utilizada;
- quantidade de bytes enviados;
- quantidade de bytes recebidos;
- resposta HTTP recebida.

Como `servidor.py` atende uma única conexão, execute-o novamente para realizar outro teste. Ele recebe os cabeçalhos até a linha vazia, inclusive quando TCP os entrega em partes, e responde sempre `200 OK`. Não interpreta o caminho solicitado nem lê `index.html`; o teste de `404` e a entrega desse arquivo são feitos com `http.server`.

## Fluxo da comunicação com sockets

```text
cliente.py
    |
    |  conexão TCP para 127.0.0.1:8080
    v
servidor.py
    |
    |  GET / HTTP/1.1
    |  Host: localhost
    |  Connection: close
    v
processamento da requisição
    |
    |  HTTP/1.1 200 OK
    |  cabeçalhos
    |  corpo HTML
    v
cliente.py recebe e exibe a resposta
```

TCP fornece a conexão e o transporte confiável dos bytes entre os processos. HTTP define o formato e o significado dos dados enviados nessa conexão.

## Execução em outro computador da mesma rede

Por padrão, o servidor aceita apenas conexões originadas da própria máquina porque utiliza:

```python
HOST = "127.0.0.1"
```

Para aceitar conexões vindas da rede local, o servidor pode ser associado a todas as interfaces:

```python
HOST = "0.0.0.0"
```

O endereço IP da máquina servidora pode ser consultado no Linux com:

```bash
hostname -I
```

No outro computador, configure `HOST` em `cliente.py` com o IP da máquina servidora, por exemplo:

```python
HOST = "192.168.1.50"
```

A porta permanece `8080`. O firewall local também precisa permitir a conexão. Este servidor é apenas didático e não deve ser exposto diretamente à Internet.

## Conceitos observados

### HTTP e TCP

HTTP é um protocolo da camada de aplicação. Neste projeto, suas mensagens são transportadas por uma conexão TCP.

Uma requisição HTTP possui uma linha inicial, cabeçalhos e uma linha vazia que marca o final dos cabeçalhos. Uma resposta HTTP possui, de forma semelhante, uma linha de status, cabeçalhos e opcionalmente um corpo.

### `200 OK` e `404 Not Found`

`200 OK` indica que a requisição foi processada com sucesso e que o recurso solicitado pôde ser retornado.

`404 Not Found` indica que o servidor recebeu a requisição, porém o caminho solicitado não corresponde a um recurso disponível.

### Endereço IP e porta

O endereço IP identifica o host/interface envolvido na comunicação. A porta identifica o processo ou serviço que recebe as conexões naquele host.

Neste projeto, o servidor utiliza:

```text
IP:    127.0.0.1
Porta: 8080
```

O cliente usa uma porta de origem efêmera escolhida pelo sistema operacional. Por isso, o número exibido pelo servidor para a porta do cliente pode mudar a cada execução.

## Análise de atraso e vazão

### Mensagem de 7,5 Mbits em dois enlaces de 1,5 Mbps

Dados:

```text
L = 7,5 Mbits
R = 1,5 Mbps
N = 2 enlaces
```

O atraso de transmissão em um enlace é:

```text
d_trans = L / R
d_trans = 7,5 / 1,5
d_trans = 5 s
```

Com dois enlaces e transmissão store-and-forward, desconsiderando propagação, processamento e fila:

```text
atraso total = N × L/R
atraso total = 2 × 5
atraso total = 10 s
```

**Resultado: 10 segundos.**

### Três pacotes de 2,5 Mbits

Cada pacote possui:

```text
L_pacote = 2,5 Mbits
```

O tempo de transmissão de cada pacote em um enlace é:

```text
d_trans = 2,5 / 1,5
d_trans ≈ 1,6667 s
```

Para dois enlaces e três pacotes, com store-and-forward e pipeline, desconsiderando propagação, processamento, filas e cabeçalhos:

```text
(N + P - 1) × L_pacote/R
(2 + 3 - 1) × 1,6667
≈ 6,67 s
```

**Resultado aproximado: 6,67 segundos.**

O tempo é menor porque, depois de receber completamente o primeiro pacote, o roteador pode transmiti-lo pelo segundo enlace enquanto a origem já envia o próximo pacote pelo primeiro enlace. Esse paralelismo é chamado de **pipeline**.

### Vazão fim a fim

Para um caminho formado por enlaces de:

```text
1 Gbps
100 Mbps
10 Mbps
500 Mbps
```

Sem tráfego concorrente ou outras limitações, a vazão fim a fim máxima é limitada pelo enlace de menor capacidade:

```text
min(1000, 100, 10, 500) Mbps = 10 Mbps
```

**Vazão fim a fim: 10 Mbps.**  
**Gargalo: enlace de 10 Mbps.**

### Atraso de transmissão

Para:

```text
R = 100 Mbps
L = 10 Mbits
```

Temos:

```text
d_trans = L / R
d_trans = 10 / 100
d_trans = 0,1 s = 100 ms
```

**Resultado: 100 ms.**

### Atraso de propagação

Para:

```text
d = 1.000 km
s = 2 × 10^8 m/s
```

Primeiro, converte-se a distância:

```text
1.000 km = 1.000.000 m = 10^6 m
```

Então:

```text
d_prop = d / s
d_prop = 10^6 / (2 × 10^8)
d_prop = 0,005 s = 5 ms
```

**Resultado: 5 ms.**

### Quando cada atraso pode dominar

Nos dois exemplos, a velocidade de propagação é `2 × 10^8 m/s`. Comparamos apenas transmissão e propagação em um enlace.

**Transmissão dominante:** pacote de 10 Mbits, enlace de 1 Mbps e distância de 1 km.

```text
d_trans = 10 × 10^6 / 10^6 = 10 s
d_prop = 1.000 / (2 × 10^8) = 0,000005 s = 0,005 ms
```

Transmitir os bits demora muito mais do que propagá-los pelo enlace.

**Propagação dominante:** pacote de 1.000 bytes, enlace de 1 Gbps e distância de 10.000 km.

```text
L = 1.000 × 8 = 8.000 bits
d_trans = 8.000 / 10^9 = 0,000008 s = 0,008 ms
d_prop = 10.000.000 / (2 × 10^8) = 0,05 s = 50 ms
```

O deslocamento do sinal demora muito mais do que transmitir os bits.

## Referência rápida

Servidor HTTP nativo:

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

Conexão HTTP manual:

```bash
nc 127.0.0.1 8080
```

Servidor com sockets:

```bash
python3 servidor.py
```

Cliente com sockets:

```bash
python3 cliente.py
```

## Observação

O código foi mantido pequeno de propósito para tornar visíveis as etapas fundamentais da comunicação: criação do socket, conexão TCP, envio de bytes, recepção de bytes, formação das mensagens HTTP e encerramento da conexão. Não se trata de um servidor HTTP de produção.
