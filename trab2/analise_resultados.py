from distribuicoes import *
from mms import *
from relatorio_estatisticas import *

import matplotlib.pyplot as plt
import numpy as np

def plota_medias(medias,qtd_replicacoes):
    replicacoes = [i for i in range(1,qtd_replicacoes+1)]
    plt.plot(replicacoes, medias[0], label="entidades na fila")
    plt.plot(replicacoes, medias[1], label="tempo na fila")
    plt.plot(replicacoes, medias[2], label="tempo no sistema")

    plt.legend(loc='upper left')
    plt.title("Estatísticas")
    plt.xlabel("Replicação")
    plt.ylabel("Média")
    plt.show()

def replica_simulacao(qtd_replicacoes):
    # parâmetros da simulação
    atendentes = 2
    tec_distr = {"exponencial": 10}
    ts_distr = {"exponencial": 4}
    limite_fila = float("inf")

    entidades = []
    tempos_fila = [] 
    tempos_sistema = []
    ocupacoes = [[] for _ in range(atendentes)]

    for _ in range(qtd_replicacoes):
        resultado_simulacao = realiza_simulacao(atendentes,tec_distr,ts_distr,limite_fila)
        
        entidades.append(entidades_fila(resultado_simulacao))
        tempos_fila.append(tempo_fila(resultado_simulacao))
        tempos_sistema.append(tempo_sistema(resultado_simulacao))

        taxa_ocupacoes = ocupacao_servidores(resultado_simulacao,atendentes)
        for idx,atendente in enumerate(taxa_ocupacoes):
            ocupacoes[idx].append(atendente)
        
    medias = [entidades,tempos_fila,tempos_sistema, ocupacoes]
    return medias

def main():
    quantidade = 24
    medias = replica_simulacao(quantidade)

    plota_medias(medias,quantidade)

    # calcula o intervalo de confiança de 95%
    medias = medias[:-1]
    nova_estimativa = []
    replicar = False
    
    for media in medias:
        mean,sigma = np.mean(media), np.std(media)
        erro_padrao = sigma/(len(media)**0.5)
        
        valor_critico = 1.96 # valor tabelado para 0.475 (0.95/2)
        margem_erro = valor_critico*erro_padrao

        # alcançar valor de h <= 10% da média amostral
        valor_esperado = 0.10*mean
        if margem_erro > valor_esperado:
            nova_estimativa.append(quantidade*((margem_erro/valor_esperado)**2))
            replicar = True
        
    # Necessita replicar a simulação
    if replicar:
        maior_replicacao = max(nova_estimativa)
        #print(maior_replicacao)
        medias = replica_simulacao(round(maior_replicacao))

    plota_medias(medias,round(maior_replicacao))

    # relatório das estatísticas
    print("\nNúmero Médio de Entidades nas Filas:", np.mean(medias[0]))
    print("Tempo Médio de uma Entidade na Fila:", np.mean(medias[1]))
    print("Tempo Médio no Sistema:", np.mean(medias[2]))

    for atendente,media in enumerate(medias[3]):
        print(f"Taxa Média de Ocupação do Servidor {atendente+1}:", np.mean(media))

main()