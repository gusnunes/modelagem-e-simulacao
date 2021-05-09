# importando os modulos
import pandas as pd
import numpy as np
import csv
from random import random

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

if __name__ == "__main__":
  main()