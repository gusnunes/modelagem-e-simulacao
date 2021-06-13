import pandas as pd

from distribuicoes import *
from relatorio_estatisticas import *

import random

class Atendente:
    def __init__(self, nome):
        self.nome = nome
        self.TS_I = 0
        self.TS = 0
        self.TS_F = 0

    def gera_tempo_servico(self, opcao):
        if opcao == "exponencial":
            ts = distribuicao_exponencial(10)
        
        elif opcao == "normal":
            ts = distribuicao_normal(10,20)
       
        return random.randint(0,30)


def realiza_simulacao(qtd_atendentes=2):
    TR = TEC = TF = 0
    fila = []

    # data frame que guarda as informações da simulação
    colunas = ["Cliente","TEC","TR","Atendente","TS-I","TS","TS-F","TF"]
    simulacao = pd.DataFrame(columns=colunas)
    
    # quantidade de atendentes do sistema
    atendentes = [Atendente(i+1) for i in range(qtd_atendentes)]

    chegadas = 10   # limite da execução da simulação
    for i in range(chegadas):
        for atendente in atendentes:
            # atendente está desocupado
            if TR >= atendente.TS_F:
                atendente.TS_I = TR
                atendente_disponivel = atendente
                break
        
        # todos os atendentes estão ocupados
        else:
            # qual atendente ficará disponível primeiro
            atendente_disponivel = min(atendentes, key=lambda x: x.TS_F)
            atendente_disponivel.TS_I = atendente_disponivel.TS_F
            
            # controlar quantidade de entidades presentes na fila
            for entidade in fila:
                tempo_inicio = entidade   # quando a entidade da fila vai ser atendida
                if TR >= tempo_inicio:
                    fila.remove(tempo_inicio) 

            fila.append(atendente_disponivel.TS_I)
            
            print(fila)

        
        atendente_disponivel.TS = atendente_disponivel.gera_tempo_servico(1)
        atendente_disponivel.TS_F = atendente_disponivel.TS_I + atendente_disponivel.TS

        TF = atendente_disponivel.TS_I - TR

        simulacao.loc[i] = [i+1,TEC,TR,atendente_disponivel.nome,atendente_disponivel.TS_I, 
            atendente_disponivel.TS,atendente_disponivel.TS_F,TF] 
        
        #TEC = distribuicao_exponencial(10)
        TEC = random.randint(0,20)
        TR += TEC
    
    return simulacao

def main():
    atendentes = 2
    resultado_simulacao = realiza_simulacao(qtd_atendentes=atendentes)
    print(resultado_simulacao.to_string(index=False))

    print("")
    entidades_fila(resultado_simulacao)
    tempo_fila(resultado_simulacao)
    ocupacao_servidores(resultado_simulacao,atendentes)
    tempo_sistema(resultado_simulacao)
    
main()