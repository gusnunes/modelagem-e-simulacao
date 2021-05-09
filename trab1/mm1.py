# importando os modulos
import pandas as pd
import numpy as np
import csv
from random import random

# Lê os dados da tabela de tempos (entre chegadas e serviços)
def le_dados(nome_arquivo):
  with open(nome_arquivo, 'r') as csvfile:
    valores = []
    
    for linha in csv.reader(csvfile, delimiter=','):
      valores.extend(map(float,linha))
  
  return valores

def main():
  tec = le_dados("TEC.csv")
  print(tec)

if __name__ == "__main__":
  main()