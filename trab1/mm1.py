# importando os modulos
import pandas as pd
import numpy as np
from random import random

from processamento_dados import*

def letra_c_d(simulacao):
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
  media = (tempo_sistema)/(qtd_entidade)
  print("Tempo Médio no Sistema:", media)

def letra_a_b(simulacao):
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

def gera_tempo_servico(ts):
  valor_aleatorio = random()   # gera um valor aleatório entre 0 e 1
  
  classes = ts["Classes"]
  intervalos = ts["Intervalo de Valores"]
  
  # verifica a qual intervalo o numero aleatório pertence
  for idx,intervalo in enumerate(intervalos):
    inicio, fim = intervalo
    valor_aleatorio = round(valor_aleatorio,precisao(fim))
    if (valor_aleatorio >= inicio) and (valor_aleatorio <= fim):
      x, y = classes.loc[idx]
      ponto_medio = (x+y)/2   # calcula o ponto medio do intervalo da classe
      break

  return ponto_medio

def gera_tempo_chegada(tec):
  valor_aleatorio = random()   # gera um valor aleatório entre 0 e 1
  
  classes = tec["Classes"]
  intervalos = tec["Intervalo de Valores"]
  
  # verifica a qual intervalo o numero aleatório pertence
  for idx,intervalo in enumerate(intervalos):
    inicio, fim = intervalo
    valor_aleatorio = round(valor_aleatorio,precisao(fim))
    if (valor_aleatorio >= inicio) and (valor_aleatorio <= fim):
      x, y = classes.loc[idx]
      ponto_medio = (x+y)/2   # calcula o ponto medio do intervalo da classe
      break

  return ponto_medio

def evento_saida(TR,ES,TF,HS, tempos_servicos, tempos_saidas, df_ts):
  TR = HS

  if TF > 0:
    TF = TF - 1
    TS = gera_tempo_servico(df_ts)
    tempos_servicos.append(TS)

    HS = TR + TS
    tempos_saidas.append(HS)

  else:
    ES = 0
    HS = float("inf")
  
  return (TR,ES,TF,HS)

def evento_chegada(TR,ES,TF,HC,HS, tempos_servicos, tempos_saidas, df_tec, df_ts):
  TR = HC
  
  if ES == 0:
    ES = 1
    TS = gera_tempo_servico(df_ts)
    tempos_servicos.append(TS)

    HS = TR + TS
    tempos_saidas.append(HS)

  else:
    TF = TF + 1
  
  TEC = gera_tempo_chegada(df_tec)
  HC = TR + TEC

  return (TR,ES,TF,HC,HS)

def realiza_simulacao(tec,ts):
  cont = 1
  parada = 10

  # valores iniciais das variáveis
  TR = ES = TF = HC = 0
  HS = float("inf")

  # data frame que guarda as informações da simualação
  colunas = ["Evento","Cliente","TR","ES","TF","HC","HS"]
  simulacao = pd.DataFrame(columns=colunas)
  simulacao.loc[0] = ["inicio","_",TR,ES,TF,HC,HS]

  # guarda os tempos de chegadas de todos os clientes
  tempos_chegadas = []

  # guarda os tempos de servicos de todos os clientes
  tempos_servicos = []

  # guarda os tempos de saidas de todos os clientes
  tempos_saidas = []

  clientes = []
  nome_cliente = 1

  while cont <= parada:
    if HC < HS:
      TR,ES,TF,HC,HS = evento_chegada(TR,ES,TF,HC,HS, tempos_servicos, tempos_saidas, tec, ts)
      
      simulacao.loc[cont] = ["Chegada",nome_cliente,TR,ES,TF,HC,HS]
      clientes.insert(0,nome_cliente)
      nome_cliente+=1

      tempos_chegadas.append(TR)

    else:
      TR,ES,TF,HS = evento_saida(TR,ES,TF,HS, tempos_servicos, tempos_saidas, ts)
      cliente = clientes.pop()
      simulacao.loc[cont] = ["Saida",cliente,TR,ES,TF,HC,HS]

    cont+= 1
  
  return simulacao

def main():
  tec = le_dados("TEC.csv")
  tec = trata_dados(tec)
  tec = mmc(tec)
  print("\nFrequências e valores empregados no MMC: TEC\n")
  print(tec.to_string(index=False))

  # por enquanto 
  ts = tec

  # fazer amanha, arrendodar os valores para 4 quando estiver inserindos eles
  # parece que fica mais facil com esse raciocionio

  resultado_simulacao = realiza_simulacao(tec,ts)
  print("\n\nResultado da Simualção:\n")
  print(resultado_simulacao.to_string(index=False))

  # relatório final contendo todas as estatísticas desejadas
  letra_a_b(resultado_simulacao)
  letra_c_d(resultado_simulacao)
  
if __name__ == "__main__":
  main()