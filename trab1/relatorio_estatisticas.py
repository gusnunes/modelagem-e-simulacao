# Tempo Médio de uma Entidade na Fila
def tempo_entidade_fila(simulacao):
  # clientes que enfrentaram fila
  clientes_fila = simulacao.loc[(simulacao['Evento'] == "Chegada") 
                                & (simulacao["TF"]>0)]

  # clientes que entraram e sairam da fila
  qtd_clientes = 0

  for idx, cliente in clientes_fila.iterrows():
    entrada = cliente["TR"]   # tempo da entrada
    nome_cliente = cliente["Cliente"]
    
    # informações do tempo de saida do cliente anterior
    cliente_anterior = simulacao.loc[(simulacao["Evento"] == "Saida") 
                                & (simulacao["Cliente"]==nome_cliente-1)]
    
    # serviço está disponível para o proximo cliente da fila
    if not cliente_anterior.empty:
      qtd_clientes += 1
      saida = cliente_anterior["TR"].values[0]
      tempo_fila = saida - entrada

  # nao teve fila
  if clientes_fila.empty:
      print("Tempo Médio de uma Entidade na Fila:", 0.0)
  
  # somente chegadas e nenhuma saida (no periodo da simulação)
  # ou teve fila, mas sem o tempo que o cliente permanceceu nela (nao tem a saida dele) 
  elif not clientes_fila.empty and qtd_clientes==0:
      print("Tempo Médio de uma Entidade na Fila:", 0.0)

  else:
    media = tempo_fila/qtd_clientes
    print("Tempo Médio de uma Entidade na Fila:", media)

# Tempo Médio no Sistema
def tempo_medio_sistema(simulacao):
  tempo_sistema = 0

  # clientes que entraram e sairam do sistema
  saidas = simulacao.loc[simulacao['Evento']=="Saida"]
  for idx, cliente in saidas.iterrows():
    nome_cliente = cliente["Cliente"]
    
    chegada = simulacao.loc[(simulacao['Evento'] == "Chegada")
                            & (simulacao["Cliente"] == nome_cliente)]
    
    # pega o horário de chegada e saida do cliente
    chegada = chegada["TR"].values[0]
    saida = cliente["TR"]

    tempo_sistema += saida - chegada

  qtd_entidade = saidas.shape[0]

  # nenhum cliente saiu do sistema (durante o periodo de simulacao)
  if qtd_entidade == 0:
      print("Tempo Médio no Sistema: nenhum cliente saiu do sistema ainda")
  
  else:
    media = tempo_sistema/qtd_entidade
    print("Tempo Médio no Sistema:", media)

# Número Médio de Entidades nas Filas
# Taxa Média de Ocupação dos Servidores:
def medio_fila_media_ocupacao(simulacao):
  tempo_fila = 0
  tempo_servidor = 0
  tempo_total = 0

  linhas = simulacao.shape[0]
  for idx in range(linhas-1):
    # intervalo de tempo entre dois eventos
    intervalo = simulacao.loc[idx+1,"TR"] - simulacao.loc[idx,"TR"] 
    
    # tempo que a fila permaneceu com a mesma quantidade
    TF = simulacao.loc[idx,"TF"]   # TF é peso do intervalo
    tempo_fila += intervalo * TF

    # tempo que o servidor permaneceu constante
    ES = simulacao.loc[idx,"ES"] # ES é peso do intervalo
    tempo_servidor += intervalo * ES

    tempo_total += intervalo

  # Número Médio de Entidades nas Filas
  entidade_fila = tempo_fila/tempo_total
  print("\nNúmero Médio de Entidades nas Filas:", entidade_fila)

  # Taxa Média de Ocupação dos Servidores:
  ocupacao_servidor = tempo_servidor/tempo_total
  print("Taxa Média de Ocupação dos Servidores:", ocupacao_servidor)