# importando os modulos
import pandas as pd
import numpy as np
import csv
from random import random

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
    #tempo = transforma(freq_acumulada) + freq_acumulada

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
  tec = trata_dados(tec)
  tec = mmc(tec)
  print(tec)

if __name__ == "__main__":
  main()