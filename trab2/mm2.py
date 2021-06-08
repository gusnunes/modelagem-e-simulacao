from trab2.distribuicoes import distribuicao_exponencial
from distribuicoes import *

class Atendente:
    def __init__(self, nome):
        self.nome = nome
        self.ocupado = 0
        self.TS_I = 0
        self.TS = 0
        self.TS_F = 0

    def tempo_servico():
        ts = distribuicao_exponencial(10)
        return ts


def realiza_simulacao():
    TR = TEC = TF = 0

    # numero de atendentes
    n = 2
    
    atendentes = [Atendente(i+1) for i in range(n)]

    for _ in range(30):
        # menor tempo final de serviço
        menor_tempo = float("inf")

        for atendente in atendentes:
            # qual atendente ficará desocupado primeiro (se tiver fila)
            if atendente.TS_F < menor_tempo:
                menor_tempo = atendente.TS_F
                atendente_disponivel = atendente
            
            # qual atendente está desocupado (sem fila)
            if TR >= atendente.TS_F:
                atendente_disponivel = atendente

                TF = 0
                break
        
        else:   # todos atendentes estão ocupados
            TF += 1

        atendente_disponivel.TS_I = TR
        atendente_disponivel.TS = atendente.tempo_servico()
        atendente_disponivel.TS_F = atendente.TS_I + atendente.TS


    TEC = distribuicao_exponencial(10)
    TR += TEC

def main():
    realiza_simulacao()

main()