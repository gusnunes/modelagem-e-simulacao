# importando os modulos
import pandas as pd
import numpy as np
import csv
from random import random

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

# calcula a quantidade de casas decimais que um numero tem
def precisao(numero):
  numero = str(numero)
  casas_decimais = numero[::-1].find('.')
  return casas_decimais

# insere as frequencias, frequencias acumuladas
# e intervalo de valores no data frame
def insere_calculos_tabela(df,intervalos,n):
  freq_acumulada = 0.0
  tempo = 0.0
  for idx, intervalo in enumerate(intervalos):
    valores = []
    valores.append(tempo)   # tempo inicial do intervalo

    qtd = intervalo[2]   # quantidade de valores presentes no intervalo
    frequencia = qtd/n   # frequência em relação a quantidade total dos dados
    freq_acumulada += frequencia
    
    valores.append(freq_acumulada)   # tempo final do intervalo
    
    # tempo de inicio do próximo intervalo
    proximo_inicio = 10**(-1 * precisao(freq_acumulada))
    if proximo_inicio == 0.1:
      proximo_inicio = 0.01
    tempo = proximo_inicio + freq_acumulada

    df.loc[idx,"Frequência"] = frequencia
    df.loc[idx,"Frequência Acumulada"] = freq_acumulada
    df.loc[idx,"Intervalo de Valores"] = valores

# determina a quantidade de valores em cada intervalo
def calcula_quantidade_valoes(data,intervalos):
  for valor in data:
    for intervalo in intervalos:
      inicio, fim, qtd = intervalo
      if (valor >= inicio) and (valor < fim):   # valor pertencente ao intervalo
        qtd += 1
        intervalo[2] = qtd
        break   # valor pertence somente a um intervalo
    
  # final do último intervalo é igual ao ultimo valor,
  # na representação de float, às vezes fica diferente
  if data[-1] >= intervalos[-1][1]:
    intervalos[-1][2] = qtd+1
  
  return intervalos

def calcula_intervalos_classes(df,K,h):
  # cada intervalo = [inicio, fim, qtd_dados]
  intervalos = [[] for _ in range(K)]
  tempo = 0.0
  for i in range(K):
    intervalos[i].append(tempo)   # tempo inicial do intervalo
    tempo += h
    intervalos[i].append(tempo)   # tempo final do intervalo
    
    # insere intervalo da classe na tabela
    df.loc[i,"Classes"] = intervalos[i][:]

    # inicialmente a quantidade de dados é zero no intervalo
    intervalos[i].append(0)

  return intervalos
  
# método de Monte Carlo
def mmc(data):
  # data frame pra montar a tabela
  colunas = ["Classes","Frequência", "Frequência Acumulada", 
             "Intervalo de Valores"]
  df = pd.DataFrame(columns=colunas)

  n = len(data)   # numero de dados
  
  # número de classes
  K = 1 + 3.3*(np.log10(n))
  K = int(np.ceil(K))   # arredonda pra cima

  amplitude_amostra = max(data)   # maior valor sem outlier
  h = amplitude_amostra/K   # tamanho de cada classe
  
  intervalos = calcula_intervalos_classes(df,K,h)
  intervalos = calcula_quantidade_valoes(data,intervalos)
  insere_calculos_tabela(df,intervalos,n)
  
  return df

# tratamento dos dados para remoção de outliers
def trata_dados(data):
  data = np.sort(data)   # ordena os dados

  # calcula os quartis
  Q1 = np.percentile(data, 25)
  Q2 = np.percentile(data, 50)
  Q3 = np.percentile(data, 75)

  IQR = Q3 - Q1   # amplitude inter-quartil
  lim_inf = Q1 - (1.5 * IQR)   # limite inferior
  lim_sup = Q3 + (1.5 * IQR)   # limite superior

  # remove outliers
  data = np.delete(data, np.argwhere( (data < lim_inf) | (data > lim_sup) ))
  return data

# lê os dados da tabela de tempos (entre chegadas ou serviços)
def le_dados(nome_arquivo):
  with open(nome_arquivo, 'r') as csvfile:
    valores = []
    
    for linha in csv.reader(csvfile, delimiter=','):
      valores.extend(map(float,linha))

  return valores

def main():
  tec = le_dados("TEC.csv")
  #tec = trata_dados(tec)
  tec = mmc(sorted(tec))
  print(tec)

  # por enquanto 
  ts = tec

  resultado = realiza_simulacao(tec,ts)
  
if __name__ == "__main__":
  main()