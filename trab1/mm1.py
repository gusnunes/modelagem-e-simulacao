# importando os modulos
import pandas as pd
import numpy as np
from random import random

from processamento_dados import*
from relatorio_estatisticas import*

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

def evento_saida(TR,ES,TF,HS,df_ts):
  TR = HS

  if TF > 0:
    TF = TF - 1
    TS = gera_tempo_servico(df_ts)
    HS = TR + TS   # agenda a próxima saida

  else:
    ES = 0
    HS = float("inf")
  
  return (TR,ES,TF,HS)

def evento_chegada(TR,ES,TF,HC,HS, df_tec, df_ts):
  TR = HC
  
  # servidor está ocioso
  if ES == 0:
    ES = 1
    TS = gera_tempo_servico(df_ts)
    HS = TR + TS   # agenda a próxima saida

  else:
    TF = TF + 1
  
  TEC = gera_tempo_chegada(df_tec)
  HC = TR + TEC   # agenda a próxima chegada

  return (TR,ES,TF,HC,HS)

def realiza_simulacao(tec,ts):
  evento = 1
  parada = 10

  # valores iniciais das variáveis
  TR = ES = TF = HC = 0
  HS = float("inf")

  # data frame que guarda as informações da simualação
  colunas = ["Evento","Cliente","TR","ES","TF","HC","HS"]
  simulacao = pd.DataFrame(columns=colunas)
  simulacao.loc[0] = ["inicio","_",TR,ES,TF,HC,HS]

  clientes = []
  nome_cliente = 1

  while evento <= parada:
    if HC < HS:
      TR,ES,TF,HC,HS = evento_chegada(TR,ES,TF,HC,HS,tec, ts)
      
      simulacao.loc[evento] = ["Chegada",nome_cliente,TR,ES,TF,HC,HS]
      clientes.insert(0,nome_cliente)
      nome_cliente+=1

    else:
      TR,ES,TF,HS = evento_saida(TR,ES,TF,HS,ts)
      cliente = clientes.pop()
      simulacao.loc[evento] = ["Saida",cliente,TR,ES,TF,HC,HS]

    evento+= 1
  
  return simulacao

def main():
  # Opções dos Tempos entre Chegadas
  tec_option = input("O TEC é deterministico? [s/n]: ")
  if tec_option == 's':
    tec_valor = input("Digite o TEC: ")
    escreve_arquivo("TEC_deterministico.csv", tec_valor)
    tec = le_dados("TEC_deterministico.csv")
  
  else:
    tec_file = input("Digite o nome do arquivo da coleta do TEC: ")
    tec = le_dados(tec_file)

  # # Opções dos Tempo de Serviços
  ts_option = input("\nO TS é deterministico? [s/n]: ")
  if ts_option == 's':
    ts_valor = input("Digite o TS: ")
    escreve_arquivo("TS_deterministico.csv", ts_valor)
    ts = le_dados("TS_deterministico.csv")
  
  else:
    ts_file = input("Digite o nome do arquivo da coleta do TS: ")
    ts = le_dados(ts_file)

  # realizada tratamento dos dados
  tec = trata_dados(tec)
  ts = trata_dados(ts)

  # tabela do Método de Monte Carlo
  tec = mmc(tec)
  print("\nFrequências e valores empregados no MMC: TEC\n")
  print(tec.to_string(index=False))
  
  ts = mmc(ts)
  print("\n\nFrequências e valores empregados no MMC: TS\n")
  print(ts.to_string(index=False))


  resultado_simulacao = realiza_simulacao(tec,ts)
  print("\n\nResultado da Simulação:\n")
  print(resultado_simulacao.to_string(index=False))

  print("\n\nRelatório final contendo todas as estatísticas:")
  medio_fila_media_ocupacao(resultado_simulacao)
  tempo_entidade_fila(resultado_simulacao)
  tempo_medio_sistema(resultado_simulacao)
  
if __name__ == "__main__":
  main()